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

## Architecture
- **Iceberg REST Catalog (`iceberg-rest`)**: The central metadata service. All tools (Spark, dbt) talk to this service to discover tables.
- **Spark Connect (`spark-connect`)**: The permanent gateway. It manages the **Spark Driver** and logical query plans.
- **Master (`spark-master`)**: The central orchestrator for resource allocation.
- **Worker (`spark-worker`)**: The computational engine that executes tasks.
- **dbt Engine**: Executed inside the cluster containers to leverage pre-configured Iceberg JARs and gRPC connectivity.
- **Warehouse**: Data is stored in `spark-warehouse/iceberg/`.

## Execution Model
```text
   [ Client ]           (uv run, dbt, SDP CLI)
       |
    (gRPC)
       |
[ Spark Connect ]       (Session & Driver)
       |
     (REST)
       |
[ Iceberg REST ]        (Metadata Service)
       |
[ Spark Master ]        (Cluster Scheduler)
       |
[ Spark Worker ]        (Task Execution)
```

- **Gateway**: `spark-connect` is a persistent gRPC gateway that manages the Spark Driver.
- **Scheduling**: `spark-master` acts as the Standalone Cluster Manager.
- **Session Isolation**: Every client connection (including every dbt model run) receives a unique, isolated **Spark Session**.
- **Persistence**: Iceberg metadata is persisted in the shared warehouse, ensuring tables created in one session are visible to the next.

## Available Commands

### Cluster Lifecycle
- `make up`: Build and start the entire cluster.
- `make clean`: Deep clean (removes containers, volumes, and built images).

### Running Pipelines
- `make run`: The full automated sequence:
    1.  **Fix Permissions**: Ensures Docker can write to local `dbt/` folders.
    2.  **Clean Warehouse**: Wipes old Iceberg data.
    3.  **Setup Namespaces**: Re-creates `raw`, `stg`, `dw`, `mrt`.
    4.  **dbt Seed**: Loads CSV data into the cluster.
    5.  **dbt Run**: Executes the transformation pipeline.
    6.  **Verify**: Runs a Python script to check results.

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
