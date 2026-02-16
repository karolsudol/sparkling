.PHONY: up down build logs

up:
	docker-compose up -d --build

down:
	docker-compose down

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
	@echo "JupyterLab running at http://localhost:8888/?token=sparkling"
	docker-compose exec jupyterlab /bin/bash

# Clean up
clean:
	docker-compose down -v --rmi all --remove-orphans
