# Sparkling ✨

PySpark with Datafusion and Declarative Pipelines.

## Usage

*   `make up`: Build the Docker images and start the services in detached mode.
*   `make down`: Stop the services.
*   `make clean`: Stop and remove all containers, volumes, and images associated with the project.
*   `make logs`: View the logs from all services.

### Spark

*   `make spark-4.0.1-shell`: Open a Spark shell in the Spark 4.0.1 cluster with Comet enabled.
*   `make spark-4.1.0-shell`: Open a Spark shell in the standard Spark 4.1.0 cluster.

### JupyterLab

*   `make jupyter`: Display the URL to access JupyterLab. Once you run `make up`, JupyterLab will be available at `http://localhost:8888` with the access token `sparkling`.

### Running the Example Application

This project includes a "Hello World" PySpark application in `notebooks/hello_spark.py`. You can run this application on either of the configured Spark clusters.

*   `make run-hello-spark-4.0.1`: Run the application on the Spark 4.0.1 cluster with Comet.
*   `make run-hello-spark-4.1.0`: Run the application on the standard Spark 4.1.0 cluster.
