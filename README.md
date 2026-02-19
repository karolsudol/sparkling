# Sparkling ✨

A simple PySpark project setup with Docker for running Spark applications.

This project provides a development environment with:
- Spark 4.1.0 (a master and a worker).
- A `spark-client` service with Python and `pyspark` for submitting jobs.
- A `src` directory for your Python applications.

## Project Structure
- `src/`: Your Python applications live here. Includes `hello_spark.py`.
- `data/`: A directory for your data files (mounted into Spark).
- `docker/`: Contains the Dockerfile for the `spark-client` service.

## Usage

First, start the Spark cluster:
```bash
make up
```

This will build the Docker images and start the Spark master and worker.

### Running a Spark Application

The `hello_spark.py` application is in the `src` directory. To run it on the Spark cluster, use the following command:
```bash
make run-hello-spark
```
This command uses the `spark-client` service to submit the application to the Spark cluster.

### Spark Shell

To open a `spark-shell` in the master node:
```bash
make spark-shell
```

### Other commands
*   `make down`: Stop the services.
*   `make logs`: View the logs from all services.
*   `make build`: Build the docker images.
*   `make clean`: Stop and remove all containers, volumes, and images associated with the project.
