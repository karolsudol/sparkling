# Sparkling ✨

A simple PySpark project setup with Docker.

This project provides a development environment with:
- Spark 4.1.0 (a master and a worker)
- A `src` directory for your Python applications.
- JupyterLab with `pyspark` installed via `uv`.

## Project Structure
- `src/`: Your Python applications live here. Includes `hello_spark.py`.
- `notebooks/`: Your Jupyter notebooks live here. Includes `hello_jupyter.ipynb`.
- `data/`: A directory for your data files (mounted into Spark).

## Usage

First, start the services:
```bash
make up
```

This will build the Docker images and start the Spark cluster and JupyterLab.

### Running the example Spark Application

The `hello_spark.py` application is located in the `src` directory. To run it on the Spark cluster:
```bash
make run-hello-spark
```

### Spark Shell

To open a `spark-shell` in the master node:
```bash
make spark-shell
```

### JupyterLab

JupyterLab is running at [http://localhost:8888](http://localhost:8888).
The access token is `sparkling`.

The `notebooks` directory is available in JupyterLab for you to create and edit notebooks.

### Other commands
*   `make down`: Stop the services.
*   `make logs`: View the logs from all services.
*   `make build`: Build the docker images.
*   `make clean`: Stop and remove all containers, volumes, and images associated with the project.