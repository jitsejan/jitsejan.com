Title: Modernizing GitHub Data Pipelines with dlt, DuckDB, and dbt
Date: 2025-08-11 10:00
Modified: 2025-08-11 10:00
Category: posts
Tags: data engineering, dlt, duckdb, dbt, github, pipeline
Slug: modernizing-github-pipelines-with-duckdb-dlt-dbt
Authors: Jitse-Jan
Summary: How I replaced brittle Python request scripts with a modern, fast, and cheap local data stack using dlt, DuckDB, and dbt.

When analyzing huge amounts of ecosystem data from GitHub, the traditional approach usually involves writing endless `requests.get()` loops, explicitly managing complex pagination, and fighting with deeply nested JSON payloads. I did exactly that for a while, but it was fragile. 

For my [GitHub Cardano ecosystem Insights](https://github.com/jitsejan/github-trend-insights) repository, I decided it was time to level up. I dropped the old custom Python request scripts and entirely embraced a modern, local-first data stack: **dlt**, **DuckDB**, and **dbt**.

Here is a breakdown of why this stack is incredible, fast, and practically free to run.

## 1. Extraction: Replacing requests with `dlt`
Before, handling the GitHub API meant manually constructing endpoints, figuring out rate limits, dropping nested dictionaries, and keeping track of pagination cursors. 

By switching to [dlt (data load tool)](https://dlthub.com/), the extraction phase became declarative. `dlt` natively understands REST APIs and handles pagination, schema inference, and table creation out of the box. 
- **Auto-normalization:** Nested JSON responses (like PR labels or user metadata) are automatically unnested into relational tables without writing custom parsing logic.
- **Resilience:** It seamlessly handles rate limiting and retries.
- **Incremental loads:** It keeps state locally, so subsequent runs only fetch new PRs and issues.

## 2. Ingestion: The magic of DuckDB
Why spin up a costly cloud data warehouse (like Snowflake or BigQuery) when the data easily fits on a laptop? 

[DuckDB](https://duckdb.org/) is the SQLite for analytics. `dlt` pipes the GitHub data directly into a local DuckDB file (`github_insights.duckdb`). 
- **Lightning fast:** Because of its columnar vectorized execution engine, aggregating tens of thousands of PRs takes milliseconds.
- **Zero Infrastructure:** No servers to provision, no network latency. It's just a file on disk.
- **Ecosystem integration:** DuckDB is constantly extending its functionality and acts as the perfect backend for the next step: transformation.

## 3. Transformation: Medallion architecture with `dbt`
Once the raw GitHub data lands in DuckDB, we need to clean it and extract business metrics (e.g., classifying PRs as "bug fix", "feature", or "refactor"). This is where [dbt (data build tool)](https://www.getdbt.com/) shines. 

I structured the `dbt` pipeline following the standard Medallion architecture:
- **Bronze:** Raw data exactly as it was extracted by `dlt`.
- **Silver:** Cleaned, deduplicated data with parsed timestamps and automated PR classification logic.
- **Gold:** Aggregations, monthly trends, and ecosystem comparison tables ready for analytics.

Using `dbt`, this logic is written purely in SQL, heavily tested using `pytest` and `dbt test`, and documented alongside the code. 

## The benefit of the Local Stack
Combining `dlt`, DuckDB, and `dbt` gives you an enterprise-grade ETL pipeline right on your local machine. It allows for crazy fast iteration cycles, completely free storage and compute (since it's local), and outputs highly structured Parquet files ready for dashboards. 

If you are still writing manual Python `requests` loops to ingest APIs, do yourself a favor and try `dlt` and DuckDB. 
