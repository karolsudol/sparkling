# Sparkling 🥂🥂🥂

A Spark 4.1.1 development environment featuring **Spark Connect**, **dbt**, and **Apache Iceberg**, orchestrated by **Dagster**.

## System Architecture

The project employs a decoupled client-server architecture where multiple thin clients communicate with a central Spark gateway, unified by a shared REST-based metadata catalog.

### Architecture Overview

```text
       [ ORCHESTRATION ]                 [ COMPUTE GATEWAY ]             [ CLUSTER ]
      +-----------------+               +-------------------+        +-----------------+
      |     Dagster     |               |   Spark Connect   | (RPC)  |  Spark Master   |
      | (Control Plane) |               |  (Gateway/Driver) |------->| (Resource Mgmt) |
      +---+---------+---+               +---------+---------+        +--------+--------+
          |         |                             ^                           |
          | trigger | trigger                     |                           v
          v         v                             | (gRPC)           +-----------------+
      +---------+ +---------+                     |                  |  Spark Workers  |
      |   dbt   | |Spark SDP|---------------------+                  |  (Execution)    |
      | (Models)| |(Ingest) |                     |                  +--------+--------+
      +----+----+ +----+----+                     |                           |
           |           |                          |                           |
           +-----------+--------------------------+                           |
                       |                                                      |
                       v                                                      |
            +--------------------+                                            |
            |  Iceberg REST API  |<-------------------------------------------+
            | (Metadata Catalog) |
            +----------+---------+
                                    |
                                    v
                         +--------------------+
                         |    Local Storage   |
                         | (Parquet/Metadata) |
                         +--------------------+
```

### Component Connectivity & Metadata Sharing

*   **Unified Metadata**: The **Iceberg REST Catalog** serves as the central source of truth. Every client (SDP, dbt, Dagster) is configured with a shared `spark_catalog` property, ensuring that a table created by any tool is immediately discoverable and readable by all others.
*   **Dual Orchestration**: **Dagster** acts as the unified control plane, triggering both **Spark SDP** for ingestion and **dbt** for transformations. It manages the dependencies between these disparate tools within a single asset graph.
*   **Decoupled Compute**: **Spark Connect** allows clients like SDP and dbt to run as lightweight processes that submit logical query plans to the server via gRPC. This eliminates the need for complex Spark installations on the client side.
*   **State Observation**: Dagster maintains its own **Spark Connect Resource**, allowing it to probe the Iceberg catalog for real-time table metrics and lineage without interfering with the primary data pipelines.
*   **Persistence**: Metadata is persisted in a local SQLite database (`metadata/iceberg_catalog.db`), while Parquet data files are managed within the `spark-warehouse/` directory.

## Getting Started

1.  **Initialize**:
    ```bash
    cp .env.example .env
    make setup
    ```
2.  **Start Cluster**:
    ```bash
    make up
    ```
3.  **Explore**:
    Run `make help` to see all available commands for managing the cluster and pipelines.

## Command Reference (`make help`)

The environment is managed via a comprehensive `Makefile`. Run `make help` to see the full documentation:

*   **Infrastructure**: `up`, `stop`, `clean`, `ps`.
*   **Pipelines**: `run-transaction-pipeline`, `ingest-transactions`, `transform-transactions`.
*   **Maintenance**: `lint`, `verify`, `clean-warehouse`.

## Access UIs

*   **Dagster UI**: [http://localhost:3000](http://localhost:3000)
*   **Spark Master**: [http://localhost:8080](http://localhost:8080)
*   **Iceberg REST**: `http://localhost:8181`
*   **Spark Connect**: `sc://localhost:15002`
