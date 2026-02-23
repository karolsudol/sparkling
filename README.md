# Sparkling 🥂🥂🥂

A Spark 4.1.1 development environment featuring **Spark Connect**, **dbt**, and **Spark Declarative Pipelines (SDP)**.

## Features
- **Spark 4.1.1**: Official Apache Spark environment.
- **Spark Connect**: Decoupled client-server architecture using gRPC (`sc://localhost:15002`).
- **dbt-spark**: SQL-based transformations using the `session` method (Spark Connect).
- **Declarative Pipelines (SDP)**: Advanced orchestration using `@dp.materialized_view`.
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

To initialize these tools, run:
```bash
make setup
```

## Available Commands

### Environment Setup
- `make setup`: Install dependencies and initialize pre-commit hooks.
- `make lint`: Manually run all linters and formatters.

### Cluster Lifecycle
- `make up`: Build and start the entire cluster.
- `make clean`: Deep clean (removes containers, volumes, and built images).

### Running Pipelines
- `make run`: The full automated sequence:
    1.  **Lint**: Checks code formatting and quality.
    2.  **Fix Permissions**: Ensures Docker can write to local `dbt/` folders.
    3.  **Clean Warehouse**: Wipes old Iceberg data and resets catalog.
    4.  **Setup Namespaces**: Re-creates `raw`, `stg`, `dw`, `mrt`.
    5.  **dbt Seed**: Loads CSV data into the cluster.
    6.  **dbt Run**: Executes the transformation pipeline.
    7.  **Verify**: Runs a Python script to check results.
### dbt Specifics
- `make dbt-seed`: Run only dbt seeds.
- `make dbt-run`: Execute dbt transformations.
- `make fix-permissions`: Use this if you hit `Permission Denied` in the `dbt/` folder.


## Apache Iceberg
The project is configured with an Iceberg catalog named `spark_catalog`. Tables created under this catalog benefit from snapshot isolation and time travel.

## Data Architecture
The pipeline follows a multi-layered Medallion-style architecture within the `spark_catalog` Iceberg catalog, as defined in `src/assets.py`.

### Layers
| Layer | Namespace | Description |
|---|---|---|
| **Raw** | `spark_catalog.raw` | Immutable source data landing zone. |
| **Staging** | `spark_catalog.stg` | Cleaned data with consistent types and naming. |
| **Warehouse** | `spark_catalog.dw` | Modeled facts and dimensions (Data Warehouse). |
| **Marts** | `spark_catalog.mrt` | Business-ready aggregates and final outputs. |

### Data Flow
```text
[ Raw ]             [ Staging ]         [ Warehouse ]       [ Marts ]
source_numbers  -->  stg_numbers  -->  fct_filtered_evens  -->  mrt_final_stats
(spark_catalog.raw) (spark_catalog.stg) (spark_catalog.dw)  (spark_catalog.mrt)
```

### Usage in SDP
To create an Iceberg table, use the `spark_catalog.` prefix in your view name:
```python
@dp.materialized_view(name="spark_catalog.default.my_table")
def create_data():
    ...
```

### Inspecting History
You can query Iceberg metadata directly:
```sql
SELECT * FROM spark_catalog.default.my_table.snapshots;
SELECT * FROM spark_catalog.default.my_table.history;
```

## Available Commands

### Cluster Lifecycle
- `make up`: Build and start the entire cluster (Master, Worker, Connect).
- `make start`: Quickly resume stopped containers.
- `make stop`: Pause the cluster.
- `make clean`: Deep clean (removes containers, volumes, and built images).

### Running Applications
- `make run`: Execute the default **SDP Pipeline** defined in `spark-pipeline.yml`.

### Utility
- `make logs`: Follow container logs.
- `make ps`: Check the status of all services.

## Access Spark UI
- **Spark Master UI**: [http://localhost:8080](http://localhost:8080)
- **Spark Worker UI**: [http://localhost:8081](http://localhost:8081)
- **Spark Connect**: `sc://localhost:15002`

## Project Structure
- `src/`: Python source code and SDP flow definitions.
- `spark-pipeline.yml`: Configuration for Declarative Pipelines.
- `spark-warehouse/`: Local directory where Materialized Views are persisted as Parquet files.
- `checkpoints/`: Storage for streaming and pipeline metadata.

## Local Development (VS Code / IDE)
To resolve import errors (like `pyspark` not found) in your IDE, create a local virtual environment:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Then, select the `.venv/bin/python` interpreter in your IDE settings.

### Running Scripts Locally
You can execute scripts on your host machine while the heavy lifting happens on the Docker cluster:

```bash
uv run src/verify.py
```

The scripts are configured to automatically detect if they are running locally and will connect to the Spark Connect endpoint at `sc://localhost:15002`.
