# Sparkling 🥂🥂🥂

A Spark 4.1.1 development environment featuring **Spark Connect** and **Spark Declarative Pipelines (SDP)**.

## Features
- **Spark 4.1.1**: Official Apache Spark environment.
- **Spark Connect**: Decoupled client-server architecture using gRPC (`sc://localhost:15002`).
- **Declarative Pipelines (SDP)**: Advanced orchestration using `@dp.materialized_view` and `spark-pipelines` CLI.
- **UV Powered**: High-performance Python package management included.
- **Colored Logs**: Enhanced readability for both system and application logs.
- **Shared Warehouse**: Persistent data storage accessible across the entire cluster.

## Architecture
- **Spark Connect (`spark-connect`)**: The permanent server-side gateway. It hosts the **Spark Driver**, optimizes query plans, and manages the session.
- **Master (`spark-master`)**: The central orchestrator for cluster resource allocation.
- **Worker (`spark-worker`)**: The computational engine that executes tasks.
- **Client (`spark-app`)**: A short-lived container used to submit pipeline definitions and execute application code. It communicates with the server via gRPC.


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
