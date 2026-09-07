Title: Branch-based schema overrides for local dbt and Dagster development
Date: 2026-08-07 10:00
Modified: 2026-08-07 10:00
Category: posts
Tags: data engineering, dbt, dagster, snowflake, ci/cd
Slug: branch-based-dbt-schema-overrides
Authors: Jitse-Jan
Summary: How I gave every branch its own throwaway Snowflake schema so local dbt and Dagster development stops colliding with shared dev environments.

While working on a dbt project running on top of Dagster for an investment firm, I kept hitting the same problem: testing a model change end to end meant running against a shared `dev` schema, and shared schemas mean collisions. Two people testing at once, one half-finished model breaking another's run, nobody quite sure whose change caused the failure. Nobody wants to be the person who breaks dev on a Friday afternoon.

The fix I landed on is simple: give every branch its own throwaway Snowflake schema, generated automatically from context that's already available, and torn down when you're done.

## The problem with shared dev schemas

A typical setup looks like this:

- `DEV` — shared, mutable, always slightly broken
- `UAT` — gated, more stable
- `PROD` — obviously off-limits for testing

Local development usually means one of two bad options: point at `DEV` and hope nobody else is running anything conflicting, or provision a full personal Snowflake environment (new database, new roles, new grants), which is expensive to set up and easy to let rot once nobody's using it.

Neither scales past a couple of engineers.

## Schema names derived from git state

The pattern ties the schema name directly to the thing you're already using to track your work: the branch.

    TEST__YOUR_NAME__RAW__ABC12345
    TEST__YOUR_NAME__STG__ABC12345
    TEST__YOUR_NAME__CURATED__ABC12345

`ABC12345` is a short suffix, whether that's the branch name, a commit hash, or a random run ID. The layer names (`RAW`, `STG`, `CURATED`) match the layering the dbt project already uses, so nothing downstream needs to know it's running against a throwaway schema.

## Wiring it into environment variables

Both dbt and the Dagster resources read their target database and schema from environment variables, so the override just needs to land there before either tool runs:

    import os
    from unittest.mock import patch

    config = LiveTestConfig.from_env(provider_env_prefix="SQL_SERVER")
    overrides = config.build_schema_overrides(
        default_landing_database="DEV_DATA_PLATFORM",
        default_dbt_database="DEV_DATA_PLATFORM",
    )

    with patch.dict(os.environ, overrides.as_env(), clear=False):
        snowflake = get_snowflake_resource()
        try:
            # dbt run, Dagster asset materialization, whatever needs real Snowflake
            ...
        finally:
            if not config.keep_artifacts:
                overrides.cleanup(snowflake)

The overrides resolve to a handful of env vars:

    SQL_SERVER_LANDING_DATABASE_OVERRIDE
    SQL_SERVER_DBT_DATABASE_OVERRIDE
    SQL_SERVER_RAW_SCHEMA_OVERRIDE
    SQL_SERVER_STG_SCHEMA_OVERRIDE
    SQL_SERVER_CURATED_SCHEMA_OVERRIDE
    LIVE_TEST_KEEP_ARTIFACTS=1   # skip cleanup, inspect the schema afterwards

Nothing about `profiles.yml` or the Dagster resource definitions needs to change. The override is purely additive at runtime, which means the same code path runs identically in CI, on a laptop, and against a real deploy. Only the environment variables differ.

## Injecting the right Snowflake role without touching your profile

The other piece is the Snowflake role. Rather than hardcoding a role per developer in `profiles.yml`, the role gets injected via a temporary profiles directory:

    with SnowflakeLiveTestHelper.build_dbt_profiles_dir_with_role(
        os.environ.get("SNOWFLAKE_ROLE")
    ) as dbt_profiles_dir:
        with patch.dict(os.environ, {"DBT_PROFILES_DIR": str(dbt_profiles_dir)}, clear=False):
            # dbt picks up SNOWFLAKE_ROLE automatically here
            ...

`DBT_PROFILES_DIR` is one of the few dbt settings meant to be swapped at runtime, so this composes cleanly with the schema overrides above. Both are just environment manipulation scoped to a `with` block, and nothing persists beyond it.

## Why this is worth doing

- **Isolation without provisioning cost.** Every branch gets its own sandbox without a new Snowflake database, roles, or grants. It's just schemas within an existing database.
- **No config drift.** `profiles.yml` and the Dagster resource definitions stay untouched. The override lives entirely in environment variables, so it can't silently diverge from what CI or prod actually run.
- **Cleanup is a boolean.** Keep the schema around while debugging (`LIVE_TEST_KEEP_ARTIFACTS=1`), drop it automatically otherwise.
- **Same code path everywhere.** Local, CI, and any future automated integration test go through the identical override mechanism. Only the suffix source changes.

The next logical step, not done yet, is folding this into CI itself, so every pull request gets a disposable schema for the duration of the run instead of relying on shared `dev`. That turns "did this actually work against real Snowflake" from a local-only sanity check into something enforced on every PR.
