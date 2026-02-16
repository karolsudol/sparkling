# Sparkling ✨

PySpark with two different Spark versions using Docker.

## Usage

This project is managed via the `Makefile`. Here are the most common commands:

*   `make up`: Build the Docker images and start the services in detached mode.
*   `make down`: Stop the services.
*   `make clean`: Stop and remove all containers, volumes, and images associated with the project.
*   `make logs`: View the logs from all services.

### Spark

*   `make spark-4.0.1-shell`: Open a Spark shell in the Spark 4.0.1 cluster with Comet enabled.
*   `make spark-4.1.0-shell`: Open a Spark shell in the standard Spark 4.1.0 cluster.

### JupyterLab

*   `make jupyter`: Display the URL to access JupyterLab. Once you run `make up`, JupyterLab will be available at `http://localhost:8888` with the access token `sparkling`.
