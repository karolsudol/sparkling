include .env
export

.PHONY: up start stop clean run pipeline verify clean-warehouse logs ps dbt-seed dbt-run fix-permissions cleanup-dbt chown-me

# Build and start the cluster
up:
	docker compose up -d --build spark-master spark-worker spark-connect
	@$(MAKE) urls

# Start existing containers without rebuilding
start:
	docker compose up -d spark-master spark-worker spark-connect
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
	docker compose stop

# Clean everything: containers, volumes, and local images
clean:
	docker compose down -v --rmi local --remove-orphans

# Fix permissions
fix-permissions:
	@echo "${BLUE}Fixing permissions...${END}"
	@docker exec -u 0 spark-master chown -R 185:0 /app/dbt
	@docker exec -u 0 spark-master chmod -R 775 /app/dbt

# Chown back to user
chown-me:
	@echo "${BLUE}Reclaiming ownership...${END}"
	@sudo chown -R $(USER):$(USER) dbt/

# Deep cleanup
cleanup-dbt:
	@echo "${BLUE}Deep cleanup of dbt...${END}"
	@docker exec -u 0 spark-master rm -rf /app/dbt/target /app/dbt/metastore_db /app/dbt/spark-warehouse /app/dbt/derby.log /app/dbt/logs

# --- Pipeline Lifecycle Commands ---

# 1. Remove old warehouse data
clean-warehouse:
	@echo "${BLUE}Cleaning up old warehouse data...${END}"
	@sudo rm -rf spark-warehouse/*

# 2. Setup namespaces
setup-namespaces:
	@echo "${BLUE}Setting up namespaces...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/setup_namespaces.py

# 3. dbt Seed
dbt-seed:
	@echo "${BLUE}Running dbt seed...${END}"
	@docker exec -w /app/dbt spark-master dbt seed --profiles-dir .

# 4. dbt Run
dbt-run:
	@echo "${BLUE}Running dbt pipeline...${END}"
	@docker exec -w /app/dbt spark-master dbt run --profiles-dir .

# 5. Run the Verification Script
verify:
	@echo "${BLUE}Running Verification...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/verify.py

# Consolidated Run: Fix -> Clean -> Namespaces -> Seed -> dbt
run: fix-permissions clean-warehouse setup-namespaces dbt-seed dbt-run verify

# Helpers for colors
BLUE=\033[94m
END=\033[0m

# View logs
logs:
	docker compose logs -f

# Check status
ps:
	docker compose ps
