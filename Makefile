.PHONY: up start stop clean run logs ps

# Build and start the cluster
up:
	docker-compose up -d --build spark-master spark-worker spark-connect
	@$(MAKE) urls

# Start existing containers without rebuilding
start:
	docker-compose up -d spark-master spark-worker spark-connect
	@$(MAKE) urls

# Display Spark Web UI URLs
urls:
	@echo "--------------------------------------------------"
	@echo "Spark Master UI:  http://localhost:8080"
	@echo "Spark Worker UI:  http://localhost:8081"
	@echo "Spark Connect:    sc://localhost:15002"
	@echo "--------------------------------------------------"

# Stop the containers without removing them
stop:
	docker-compose stop

# Clean everything: containers, volumes, and local images
clean:
	docker-compose down -v --rmi local --remove-orphans

# Run a Spark Pipeline (SDP)
run:
	docker-compose run --rm -e SPARK_APP_TYPE=sdp -e SPARK_APPLICATION_SCRIPT=/app/spark-pipeline.yml spark-app

# Run a standard PySpark script
# Usage: make run-app APP=your_script.py
run-app:
	docker-compose run --rm -e SPARK_APP_TYPE=submit -e SPARK_APPLICATION_SCRIPT=/app/$(or $(APP),hello_spark.py) spark-app

# View logs
logs:
	docker-compose logs -f

# Check status
ps:
	docker-compose ps
