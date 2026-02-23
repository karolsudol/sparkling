include .env
export

.PHONY: up start stop clean run pipeline verify clean-warehouse logs ps dbt-seed dbt-run fix-permissions cleanup-dbt chown-me

# Build and start the cluster
up:
	docker compose up -d --build iceberg-rest spark-master spark-worker spark-connect
	@$(MAKE) urls

# Start existing containers without rebuilding
start:
	docker compose up -d iceberg-rest spark-master spark-worker spark-connect
	@$(MAKE) urls

# Display Spark Web UI URLs
urls:
	@echo "--------------------------------------------------"
	@echo "Spark Master UI:  http://localhost:8080"
	@echo "Spark Worker UI:  http://localhost:8081"
	@echo "Spark Connect:    sc://localhost:15002"
	@echo "Iceberg REST:     http://localhost:8181"
	@echo "--------------------------------------------------"

# Stop the containers without removing them
stop:
	docker compose stop

# Clean everything: containers, volumes, and local images
clean:
	docker compose down -v --rmi local --remove-orphans

# Fix permissions
fix-permissions:
	@echo "${BLUE}Fixing permissions...${END}"
	@docker exec -u 0 spark-master chmod -R 777 /app/dbt /app/spark-warehouse || true
	@sudo chmod -R 777 dbt/ spark-warehouse/ || true

# Chown back to user
chown-me:
	@echo "${BLUE}Reclaiming ownership...${END}"
	@sudo chown -R $(USER):$(USER) dbt/

# Deep cleanup
cleanup-dbt:
	@echo "${BLUE}Deep cleanup of dbt...${END}"
	@docker exec -u 0 spark-master rm -rf /app/dbt/target /app/dbt/metastore_db /app/dbt/spark-warehouse /app/dbt/derby.log /app/dbt/logs

# --- Pipeline Lifecycle Commands ---

# 1. Remove old warehouse data and reset REST catalog metadata
clean-warehouse:
	@echo "${BLUE}Cleaning up old warehouse data and catalog...${END}"
	@sudo rm -rf spark-warehouse/iceberg/
	@sudo mkdir -p spark-warehouse/iceberg/
	@sudo chmod -R 777 spark-warehouse/
	@echo "${BLUE}Restarting Iceberg REST...${END}"
	@docker compose restart iceberg-rest
	@echo "${BLUE}Waiting for Iceberg REST to initialize...${END}"
	@sleep 5

# 2. Setup namespaces
setup-namespaces:
	@echo "${BLUE}Setting up namespaces...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/setup_namespaces.py

# 3. dbt Seed
dbt-seed:
	@echo "${BLUE}Running dbt seed...${END}"
	@docker exec -w /app/dbt -e SPARK_REMOTE=${SPARK_REMOTE} spark-master dbt seed --profiles-dir .

# 4. dbt Run
dbt-run:
	@echo "${BLUE}Running dbt pipeline...${END}"
	@docker exec -w /app/dbt -e SPARK_REMOTE=${SPARK_REMOTE} spark-master dbt run --profiles-dir .

# 5. Run the Verification Script
verify:
	@echo "${BLUE}Running Verification...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/verify.py

# Consolidated Run: Fix -> Clean -> Namespaces -> Seed -> dbt
run: fix-permissions clean-warehouse
	@echo "${BLUE}Setting up namespaces...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/setup_namespaces.py
	@echo "${BLUE}Synchronizing permissions for Spark workers...${END}"
	@docker exec -u 0 spark-master chmod -R 777 /app/spark-warehouse
	@sleep 2
	@echo "${BLUE}Final permission fix...${END}"
	@sudo chmod -R 777 spark-warehouse/ dbt/
	@docker exec -w /app/dbt -e SPARK_REMOTE=${SPARK_REMOTE} spark-master dbt seed --profiles-dir .
	@docker exec -w /app/dbt -e SPARK_REMOTE=${SPARK_REMOTE} spark-master dbt run --profiles-dir .
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/verify.py

# Helpers for colors
BLUE=\033[94m
END=\033[0m

# View logs
logs:
	docker compose logs -f

# Check status
ps:
	docker compose ps
