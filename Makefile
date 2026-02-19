.PHONY: up down build logs clean spark-shell run-hello-spark

up:
	docker-compose up -d --build

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all --remove-orphans

spark-shell:
	docker-compose exec spark-master spark-shell

run-hello-spark:
	docker-compose exec \
		-e SPARK_MASTER_URL=spark://spark-master:7077 \
		jupyterlab spark-submit /opt/src/hello_spark.py