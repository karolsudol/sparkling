# Sparkling ✨

PySpark with Datafusion and Declarative Pipelines.

## Usage

*   `make build`: Build the Docker images for all services.
*   `make start`: Start the services. If containers are stopped, it will restart them. If they don't exist, they will be created.
*   `make up`: A shortcut to build the images and then start the services.
*   `make stop`: Stop the running services without removing the containers.
*   `make down`: Stop and remove the containers.
*   `make clean`: Stop and remove all containers, volumes, and images associated with the project.
*   `make logs`: View the logs from all services.

### Spark

*   `make spark-4.0.1-shell`: Open a Spark shell in the Spark 4.0.1 cluster with Comet enabled.
*   `make spark-4.1.0-shell`: Open a Spark shell in the standard Spark 4.1.0 cluster.

### JupyterLab

*   `make jupyter`: Display the URL to access JupyterLab. Once you run `make up`, JupyterLab will be available at `http://localhost:8888` with the access token `sparkling`.

### Running the Example Application

*   `make run-hello-spark-4.0.1`: Run the application on the Spark 4.0.1 cluster with Comet.
*   `make run-hello-spark-4.1.0`: Run the application on the standard Spark 4.1.0 cluster.
