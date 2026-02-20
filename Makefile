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

# Consolidated Run: Clean -> Pipeline -> Verify
run:
	@echo "${BLUE}Cleaning up old warehouse data...${END}"
	@sudo rm -rf spark-warehouse/*
	@echo "${BLUE}Running Declarative Pipeline (SDP)...${END}"
	@docker-compose run --rm -e SPARK_APP_TYPE=sdp -e SPARK_APPLICATION_SCRIPT=/app/spark-pipeline.yml spark-app
	@echo "${BLUE}Running Verification...${END}"
	@docker-compose run --rm -e SPARK_APP_TYPE=submit -e SPARK_APPLICATION_SCRIPT=/app/src/verify.py spark-app

# Run a specific script
run-app:
	docker-compose run --rm -e SPARK_APP_TYPE=submit -e SPARK_APPLICATION_SCRIPT=/app/$(or $(APP),src/verify.py) spark-app

# Helpers for colors
BLUE=\033[94m
END=\033[0m

# View logs
logs:
	docker-compose logs -f

# Check status
ps:
	docker-compose ps
