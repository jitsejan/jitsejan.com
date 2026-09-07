Title: Multiplying dev environments without multiplying infrastructure
Date: 2026-09-14 10:00
Modified: 2026-09-14 10:00
Category: posts
Tags: data engineering, dagster, dbt, snowflake, terraform, ci/cd
Slug: multiplying-dev-environments-dagster-oss
Authors: Jitse-Jan
Summary: How three developers sharing one Snowflake dev environment turned into three isolated sandboxes, built on Dagster OSS without touching the existing managed setup.

At an investment firm I worked with, the data platform had four environments: dev, uat, int, prod. That's a normal setup, except dev was shared by everyone, and "everyone" was starting to mean two or three engineers actively working on different projects at the same time. One person's half-finished Terraform apply would knock over another person's dbt run. Nobody had done anything wrong, there just wasn't enough isolation for the number of people using it.

The fix wasn't a bigger dev environment. It was three smaller ones.

## Why not just scale up the existing setup

The platform's orchestration ran on a managed Dagster+ deployment. Adding two more full environments there looked simple on paper, but it wasn't: it meant provisioning through the managed service for every new environment, and any mistake in that config was visible platform-wide, not scoped to one team's sandbox. Wider blast radius for a problem that was really just "three people need three lanes."

The team was also weighing a longer-term move to Dagster OSS at some point. Building the new sandboxes on the managed service would have been throwaway work once that migration happened anyway.

So the decision was: leave the existing prod-facing setup completely alone, and build the new dev sandboxes directly on Dagster OSS, as pure addition. That got isolation for the team immediately, and got real-world testing of OSS ahead of any full migration decision, without any risk to what was already running.

## Three environments, one shared account

`dev1`, `dev2`, `dev3`, not five, not per-person. The number came from a simple constraint: two to three people work on different projects concurrently, so three lanes covers it without over-provisioning.

All three point at the same non-prod AWS account and the same Snowflake instance as the original dev. They're not separate infrastructure stacks, they're separate Terraform variable files:

```
variables-dev1.tfvars
variables-dev2.tfvars
variables-dev3.tfvars
```

Same `account_id`, same shared database, same environment-friendly name pattern as the original dev, just three parallel copies of the pipeline targets. Both the ingestion/orchestration repo and the dbt repo got `dev1`/`dev2`/`dev3` added as valid deploy targets in their pipeline YAML, all mapped to the same underlying AWS environment.

## What "addition only" actually meant in practice

Saying "don't touch the existing setup" is easy. Making it true takes discipline, because the obvious shortcuts all involve reusing something that already exists:

- **Don't reuse the existing service role across all three sandboxes.** It's tempting, one role, one set of grants, less Terraform. But it defeats the isolation you're building, if `dev2` can accidentally touch `dev1`'s data through a shared role, you've recreated the shared-dev problem with extra steps.
- **Don't point every sandbox's external test endpoints at the same shared instance.** If sandbox environments share a mutable external dependency, whatever isolation you built stops at the edge of your own Terraform. This one is easy to miss because it doesn't show up until two sandboxes are actually used at the same time.
- **Leave UAT and INT alone entirely.** It's tempting to fold "should INT become a proper test gate" into the same piece of work, but that's a separate decision with separate stakeholders. Scoping the sandbox work strictly to dev kept it shippable in days instead of becoming a platform redesign.

None of these are exotic problems. They're the ordinary traps of "just clone the config three times" that only bite once more than one sandbox is actually in active use.

## The gap between "pipeline runs" and "environment works"

The part that took longest wasn't the Terraform, it was discovering that a green pipeline run doesn't mean the environment is live. There are two separate pipelines involved: one applies the Terraform that provisions the actual orchestration agent, and a second one deploys code to that agent. The second pipeline assumes the agent already exists, it doesn't provision it.

Running the code-deploy pipeline against a sandbox that never had its agent provisioned fails with an error that looks like a code problem, but is actually a sequencing problem: nothing is listening on the other end. Confirming an environment is actually usable meant checking the agent's own status, not just reading pipeline exit codes.

## Why this is worth doing

- **Isolation scoped to what's actually needed.** Three lanes for three concurrent workstreams, not a personal environment per engineer.
- **Zero risk to the existing platform.** Nothing about the managed prod-facing setup changed. The new sandboxes are additive, and can be torn down without touching anything else.
- **A real testbed for a future migration.** If a move to Dagster OSS happens later, there's already operational experience running it, instead of a cold start.
- **The failure modes are cheap to catch early.** Shared roles, shared external state, and the provision-vs-deploy pipeline gap are all easy to check for once you know to look, and expensive to debug once three people are relying on the environment being isolated.

The obvious next step is making the RBAC and grants for each sandbox explicit rather than inherited from the original dev config, so `dev1`/`dev2`/`dev3` are isolated all the way down, not just at the compute layer.
