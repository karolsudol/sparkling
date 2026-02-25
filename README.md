# Sparkling 🥂🥂🥂

A Spark 4.1.1 development environment featuring **Spark Connect**, **dbt**, and **Spark Declarative Pipelines (SDP)**.

## Features
- **Spark 4.1.1**: Official Apache Spark environment.
- **Spark Connect**: Decoupled client-server architecture using gRPC (`sc://localhost:15002`).
- **dbt-spark**: SQL-based transformations using the `session` method (Spark Connect).
- **Schema Enforcement**: Strong data contracts using **dbt Model Contracts** to ensure Spark/Iceberg table integrity.
- **Data Quality**: Automated testing (`unique`, `not_null`) integrated into the transformation pipeline.
- **Declarative Pipelines (SDP)**: Advanced orchestration using `@dp.materialized_view` and `@dp.table` (Streaming).
- **Apache Iceberg**: High-performance table format using the **REST Catalog** for centralized metadata management.
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
   This will set up pre-commit hooks.

## Architecture
- **Iceberg REST Catalog (`iceberg-rest`)**: The central metadata service. All tools (Spark, dbt) talk to this service to discover tables.
- **Spark Connect (`spark-connect`)**: The permanent gateway. It manages the **Spark Driver** and logical query plans.
- **Raw Transactions App (`spark-raw-transactions`)**: A containerized Spark Connect client responsible for running the `raw_transactions_pipeline`.
- **Master (`spark-master`)**: The central orchestrator for resource allocation. Also hosts the **dbt** transformation client.
- **Worker (`spark-worker`)**: The computational engine that executes tasks.
- **dbt Engine**: Executed inside the `spark-master` container, connecting to the cluster via Spark Connect.
- **Warehouse**: Data is stored in `spark-warehouse/iceberg/`.

### System Architecture
This project uses a decoupled client-server architecture via **Spark Connect**. Multiple clients communicate with a single Spark gateway:

```text
[ Clients ]                       [ Server / Gateway ]          [ Cluster ]

(Python / SDP)
[ spark-raw-transactions ] --+
                             |
(SQL / dbt)                  |
[ dbt (in master) ]  --------+--> [ spark-connect ] -- (RPC) --> [ spark-master ]
                             |      (Spark Driver)                    |
(Local Development)          |                                        v
[ Host (python3) ]  ---------+                                 [ spark-worker ]
                                                                      |
                                                                      v
                                                               [ Iceberg REST ]
                                                                      |
                                                               [ File System ]
```

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

Always ensure both files are kept in sync when adding new libraries.

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

**Full Automated Sequence**
- `make run-transaction-pipeline`: Chains all steps below. It generates fresh data, ingests it to RAW, runs all dbt layers, and prints the final stats.

**Individual Incremental Steps**
- `make generate-transactions`: Simulate a new batch of data arriving in the landing zone.
- `make ingest-transactions`: Run the Spark SDP pipeline to incrementally load only new CSVs into `raw`.
- `make transform-transactions`: Run dbt transformations (`stg` -> `dw` -> `mrt`) incrementally.
- `make show-marts`: View the final user statistics directly from your host.

### Cluster Lifecycle
- `make up`: Build and start the entire cluster, fixes permissions and sets up namespaces.
- `make start`: Start existing containers without rebuilding.
- `make clean`: Deep clean (removes containers, volumes, and built images).
- `make clean-warehouse`: Wipes all Iceberg data, checkpoints, and landing files.

## Apache Iceberg
The project is configured with an Iceberg catalog named `spark_catalog`. Tables created under this catalog benefit from snapshot isolation and time travel.

## Schema Enforcement & Testing
This project implements **Data Contracts** to ensure reliability in the Spark environment:

- **Model Contracts**: Every dbt model in `stg`, `dw`, and `mrt` layers has `enforced: true`. This means dbt will fail the build if the SQL output doesn't exactly match the schema (column names and Spark types) defined in the `.yml` files.
- **Financial Precision**: All `amount` and `total_spent` columns are strictly typed as `decimal(18,2)` to prevent floating-point errors common with `double`.
- **Integrity Tests**:
    - `unique`: Ensures no duplicate IDs (e.g., `transaction_id`) exist in the warehouse or marts.
    - `not_null`: Ensures critical fields like `user_id` and `event_at` are never missing.

To run these checks manually:
```bash
# Runs both transformations and all tests
make transform-transactions
```

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
