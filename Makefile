.PHONY: up down build logs start stop

up:
	docker-compose up -d --build

start:
	docker-compose up -d

down:
	docker-compose down

stop:
	docker-compose stop

build:
	docker-compose build

logs:
	docker-compose logs -f

# Spark 4.0.1 with Comet
spark-4.0.1-shell:
	docker-compose exec spark-master-4.0.1-comet spark-shell

# Spark 4.1.0
spark-4.1.0-shell:
	docker-compose exec spark-master-4.1.0 spark-shell

# Jupyterlab
jupyter:
	@echo "JupyterLab is running. Access it at the following URL:"
	@echo "http://localhost:8888/?token=sparkling"

# Run hello_spark.py on Spark 4.0.1
run-hello-spark-4.0.1:
	docker-compose exec \
		-e SPARK_MASTER_URL=spark://spark-master-4.0.1-comet:7077 \
		jupyterlab spark-submit --conf spark.driver.host=jupyterlab /opt/notebooks/hello_spark.py

# Run hello_spark.py on Spark 4.1.0
run-hello-spark-4.1.0:
	docker-compose exec --user root jupyterlab \
		bash -c "uv pip install --system pyspark==4.1.0 && \
		SPARK_MASTER_URL=spark://spark-master-4.1.0:7077 \
		spark-submit /opt/notebooks/hello_spark.py"

# Spark-submit on jupyterlab for Spark 4.0.1
spark-submit-4.0.1:
	docker-compose exec jupyterlab spark-submit

# Spark-submit on jupyterlab for Spark 4.1.0
spark-submit-4.1.0:
	docker-compose exec --user root jupyterlab bash -c "uv pip install --system pyspark==4.1.0 && spark-submit"

# Clean up
clean:
	docker-compose down -v --rmi all --remove-orphans
