.PHONY: up stop clean run logs ps

# Start the cluster (Master + Worker)
up:
	docker-compose up -d --build
	@echo "--------------------------------------------------"
	@echo "Spark Master UI: http://localhost:8080"
	@echo "Spark Worker UI: http://localhost:8081"
	@echo "--------------------------------------------------"

# Stop the containers without removing them
stop:
	docker-compose stop

# Clean everything: containers, volumes, and local images
clean:
	docker-compose down -v --rmi local --remove-orphans

# Run a PySpark application (default: hello_spark.py)
# Usage: make run [APP=your_script.py]
run:
	SPARK_APPLICATION_SCRIPT=/app/$(or $(APP),hello_spark.py) docker-compose run --rm spark-app

# View logs
logs:
	docker-compose logs -f

# Check status
ps:
	docker-compose ps
