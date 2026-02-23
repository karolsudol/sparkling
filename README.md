# Sparkling 🥂🥂🥂

A Spark 4.1.1 development environment featuring **Spark Connect**, **dbt**, and **Spark Declarative Pipelines (SDP)**.

## Features
- **Spark 4.1.1**: Official Apache Spark environment.
- **Spark Connect**: Decoupled client-server architecture using gRPC (`sc://localhost:15002`).
- **dbt-spark**: SQL-based transformations using the `session` method (Spark Connect).
- **Declarative Pipelines (SDP)**: Advanced orchestration using `@dp.materialized_view` and `@dp.streaming_table`.
- **Apache Iceberg**: High-performance table format using the **REST Catalog** for centralized metadata management.
- **UV Powered**: High-performance Python package management.
- **Shared Warehouse**: Persistent data storage across the entire cluster.
- **Code Quality**: Pre-configured **Ruff** (Python) and **sqlfmt** (SQL) for consistent styling.

## Getting Started

1. **Clone the repository**
2. **Setup Environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if you need to change any default ports or paths.
3. **Initialize the project**:
   ```bash
   make setup
   ```
   This will install dependencies and set up pre-commit hooks.

## Architecture
- **Iceberg REST Catalog (`iceberg-rest`)**: The central metadata service. All tools (Spark, dbt) talk to this service to discover tables.
- **Spark Connect (`spark-connect`)**: The permanent gateway. It manages the **Spark Driver** and logical query plans.
- **Master (`spark-master`)**: The central orchestrator for resource allocation.
- **Worker (`spark-worker`)**: The computational engine that executes tasks.
- **dbt Engine**: Executed inside the cluster containers to leverage pre-configured Iceberg JARs and gRPC connectivity.
- **Warehouse**: Data is stored in `spark-warehouse/iceberg/`.

## Data Flow
```text
[ File System ]       [ Spark SDP ]       [ Iceberg RAW ]       [ dbt Core ]       [ Iceberg MRT ]
CSV Batches    --->  Streaming Table  --->  raw.transactions  --->  SQL Models  --->  mrt.user_stats
```

## Hybrid Workflow
This project demonstrates a modern hybrid transformation architecture organized by dataset:

1. **Spark SDP (`pipelines/`)**: Handles the **Ingestion** layer. It uses Python-based `Streaming Tables` to incrementally pick up CSV files from `./data/landing` and write them into the Iceberg `raw` namespace.
2. **dbt Core (`dbt/models/`)**: Handles the **Modeling** layers. It picks up where SDP left off, using incremental SQL models to transform the data through `stg`, `dw`, and `mrt` layers.

## Dependencies
This project uses two ways to manage dependencies:
1. **`pyproject.toml`**: The primary source of truth for **local development**. It is used by `uv` to manage the virtual environment and tools like `ruff`.
2. **`requirements.txt`**: Used by **Docker** during the build phase (`Dockerfile.spark`) to install packages inside the cluster.

## Code Quality
The project uses automated tools to ensure consistent code style and quality:
- **Ruff**: An extremely fast Python linter and formatter.
- **sqlfmt**: A formatter for dbt SQL models.
- **Pre-commit**: Hooks that automatically run these tools before every commit.

To initialize these tools, run `make setup`.

## Available Commands

### Environment Setup
- `make setup`: Install dependencies and initialize pre-commit hooks.
- `make lint`: Manually run all linters and formatters.

### Transactions Dataset Pipeline
- `make run-transactions`: The full automated sequence (Fresh start).
- `make generate-transactions`: Simulate a new batch of data arriving in the landing zone.
- `make ingest-transactions`: Run the Spark SDP pipeline to incrementally load CSV into `raw`.
- `make transform-transactions`: Run dbt transformations (`stg` -> `dw` -> `mrt`) incrementally.
- `make show-marts`: View the final user statistics directly from your host.
- `make show-marts-docker`: View the final user statistics from within the Spark cluster.

### Cluster Lifecycle
- `make up`: Build and start the entire cluster.
- `make clean`: Deep clean (removes containers, volumes, and built images).
- `make clean-warehouse`: Wipes all Iceberg data, checkpoints, and landing files.

## Apache Iceberg
The project is configured with an Iceberg catalog named `spark_catalog`. Tables created under this catalog benefit from snapshot isolation and time travel.

## Data Architecture (Medallion)
| Layer | Namespace | Description |
|---|---|---|
| **Raw** | `spark_catalog.raw` | Immutable source data landing zone (Managed by SDP). |
| **Staging** | `spark_catalog.stg` | Cleaned data with consistent types and naming (Managed by dbt). |
| **Warehouse** | `spark_catalog.dw` | Modeled facts and dimensions (Managed by dbt). |
| **Marts** | `spark_catalog.mrt` | Business-ready aggregates and final outputs (Managed by dbt). |

## Access Spark UI
- **Spark Master UI**: [http://localhost:8080](http://localhost:8080)
- **Spark Worker UI**: [http://localhost:8081](http://localhost:8081)
- **Spark Connect**: `sc://localhost:15002`
- **Iceberg REST**: `http://localhost:8181`
