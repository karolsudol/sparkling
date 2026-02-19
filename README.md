# Sparkling 🥂

A simple Spark 4.1.1 development environment using Docker and `uv`.

## Features
- **Spark 4.1.1**: Official Apache Spark image.
- **UV**: Fast Python package installer included in the Spark images.
- **PySpark Hello World**: Sample application in `src/hello_spark.py`.
- **Docker Compose**: Easy management of Spark Master, Worker, and App containers.

## Prerequisites
- Docker and Docker Compose
- `make`

## Getting Started

### 1. Start the Cluster
To build the images and start the Spark Master and Worker:
```bash
make up
```

### 2. Run the Sample Application
To run the PySpark hello world application:
```bash
make run
```

### 3. Access Spark UI
- **Spark Master UI**: [http://localhost:8080](http://localhost:8080)
- **Spark Worker UI**: [http://localhost:8081](http://localhost:8081)

## Project Structure
- `src/`: PySpark source code.
- `data/`: Local data directory mounted to `/data` in the container.
- `Dockerfile.spark`: Custom Spark image with `uv` and Python 3.
- `docker-compose.yml`: Defines the Spark infrastructure.

## Available Commands
- `make up`: Build and start the cluster.
- `make down`: Stop and remove the cluster.
- `make stop`: Stop the containers.
- `make build`: Rebuild the images.
- `make logs`: View container logs.
- `make clean`: Deep clean of containers and images.
- `make run`: Run the sample PySpark application.
- `make spark-shell`: Open an interactive PySpark shell on the master.
