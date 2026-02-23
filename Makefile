include .env
export

.PHONY: up start stop clean run-transactions verify clean-warehouse logs ps fix-permissions chown-me lint setup generate-transactions ingest-transactions transform-transactions

# --- Initialization ---

setup:
	@echo "${BLUE}Setting up local environment...${END}"
	@uv pip install -r requirements.txt
	@pre-commit install

lint:
	@echo "${BLUE}Running linting and formatting...${END}"
	@pre-commit run --all-files

fix-permissions:
	@echo "${BLUE}Fixing permissions...${END}"
	@docker exec -u 0 spark-master chmod -R 777 /app/dbt /app/spark-warehouse /app/data /app/checkpoints || true
	@sudo chmod -R 777 dbt/ spark-warehouse/ data/ checkpoints/ || true

# --- TRANSACTIONS DATASET PIPELINE ---

generate-transactions:
	@echo "${BLUE}Generating transactions data...${END}"
	@uv run src/generate_transactions.py

ingest-transactions:
	@echo "${BLUE}Ingesting Transactions to RAW...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-app spark-pipelines run --spec /app/pipelines/raw_transactions.yml

transform-transactions:
	@echo "${BLUE}Transforming Transactions (STG -> MRT)...${END}"
	@docker exec -w /app/dbt -e SPARK_REMOTE=${SPARK_REMOTE} spark-master dbt run --select transactions user_stats --profiles-dir .

run-transactions: lint fix-permissions clean-warehouse
	@$(MAKE) generate-transactions
	@$(MAKE) fix-permissions
	@$(MAKE) ingest-transactions
	@$(MAKE) transform-transactions
	@$(MAKE) verify

# --- Infrastructure ---

up:
	docker compose up -d --build iceberg-rest spark-master spark-worker spark-connect
	@$(MAKE) urls

start:
	docker compose up -d iceberg-rest spark-master spark-worker spark-connect
	@$(MAKE) urls

urls:
	@echo "--------------------------------------------------"
	@echo "Spark Master UI:  http://localhost:8080"
	@echo "Spark Worker UI:  http://localhost:8081"
	@echo "Spark Connect:    sc://localhost:15002"
	@echo "Iceberg REST:     http://localhost:8181"
	@echo "--------------------------------------------------"

stop:
	docker compose stop

clean:
	docker compose down -v --rmi local --remove-orphans

clean-warehouse:
	@echo "${BLUE}Cleaning up old warehouse data and catalog...${END}"
	@sudo rm -rf spark-warehouse/iceberg/
	@sudo rm -rf checkpoints/*
	@sudo rm -rf data/landing/*
	@sudo mkdir -p spark-warehouse/iceberg/
	@sudo chmod -R 777 spark-warehouse/ checkpoints/ data/
	@echo "${BLUE}Restarting Iceberg REST...${END}"
	@docker compose restart iceberg-rest
	@echo "${BLUE}Waiting for Iceberg REST to initialize...${END}"
	@sleep 5

setup-namespaces:
	@echo "${BLUE}Setting up namespaces...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} spark-master python3 /app/src/setup_namespaces.py

verify:
	@echo "${BLUE}Running Verification...${END}"
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
