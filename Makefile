include .env
export

.PHONY: up start stop clean run-transaction-pipeline verify clean-warehouse logs ps fix-permissions chown-me lint setup generate-transactions ingest-transactions transform-transactions show-marts clean-orphans

# --- Initialization ---

setup:
	@echo "${BLUE}Setting up local environment...${END}"
	@uv sync
	@pre-commit install

lint:
	@echo "${BLUE}Running linting and formatting...${END}"
	@uv run pre-commit run --all-files

fix-permissions:
	@echo "${BLUE}Fixing permissions...${END}"
	@docker exec -u 0 spark-master chmod -R 777 /app/dbt /app/spark-warehouse /app/data /app/checkpoints || true
	@sudo chmod -R 777 dbt/ spark-warehouse/ data/ checkpoints/ || true

# --- TRANSACTIONS DATASET PIPELINE ---

generate-transactions:
	@echo "${BLUE}Generating transactions data...${END}"
	@PYTHONWARNINGS=ignore uv run src/generate_transactions.py

ingest-transactions:
	@echo "${BLUE}Ingesting Transactions to RAW...${END}"
	@PYTHONWARNINGS=ignore uv run spark-pipelines run --spec pipelines/raw_transactions.yml --remote ${SPARK_REMOTE}

transform-transactions:
	@echo "${BLUE}Transforming Transactions (STG -> MRT)...${END}"
	@cd dbt && SPARK_REMOTE=${SPARK_REMOTE} PYTHONWARNINGS=ignore uv run dbt build --select "*transactions*" "*user_stats*" --profiles-dir .

# Show final marts data (runs locally)
show-marts:
	@echo "${BLUE}Fetching final stats (local)...${END}"
	@PYTHONWARNINGS=ignore uv run src/show_marts.py

run-transaction-pipeline:
	@$(MAKE) generate-transactions
	@$(MAKE) ingest-transactions
	@$(MAKE) transform-transactions
	@$(MAKE) show-marts

# --- Validation & Dry Runs ---

check-contracts:
	@echo "${BLUE}Running Dry Run for Ingestion...${END}"
	@PYTHONWARNINGS=ignore uv run spark-pipelines dry-run --spec pipelines/raw_transactions.yml --remote ${SPARK_REMOTE}
	@echo "${BLUE}Validating dbt SQL against YAML contracts...${END}"
	@cd dbt && SPARK_REMOTE=${SPARK_REMOTE} PYTHONWARNINGS=ignore uv run dbt build --select "*transactions*" "*user_stats*" --limit 0 --profiles-dir .

# --- Infrastructure ---

up:
	docker compose up -d --build iceberg-rest spark-master spark-worker spark-connect dagster-webserver dagster-daemon
	@$(MAKE) urls
	@$(MAKE) fix-permissions
	@$(MAKE) setup-namespaces

start:
	docker compose up -d iceberg-rest spark-master spark-worker spark-connect dagster-webserver dagster-daemon
	@$(MAKE) urls
	@$(MAKE) fix-permissions

urls:
	@echo "--------------------------------------------------"
	@echo "Spark Master UI:  http://localhost:8080"
	@echo "Spark Worker UI:  http://localhost:8081"
	@echo "Spark Connect:    sc://localhost:15002"
	@echo "Iceberg REST:     http://localhost:8181"
	@echo "Dagster UI:       http://localhost:3000"
	@echo "--------------------------------------------------"

stop:
	docker compose stop

clean-orphans:
	docker compose up -d --remove-orphans

clean:
	docker compose down -v --rmi local --remove-orphans

clean-warehouse:
	@echo "${BLUE}Cleaning up old warehouse data...${END}"
	@sudo rm -rf spark-warehouse/iceberg/*
	@sudo rm -rf checkpoints/*
	@sudo rm -rf data/landing/*
	@sudo mkdir -p spark-warehouse/iceberg/raw spark-warehouse/iceberg/stg spark-warehouse/iceberg/dw spark-warehouse/iceberg/mrt checkpoints/ data/landing/
	@sudo chmod -R 777 spark-warehouse/ checkpoints/ data/
	@echo "${BLUE}Data cleaned. Catalog metadata in SQLite will persist.${END}"

setup-namespaces:
	@echo "${BLUE}Setting up namespaces...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} -e PYTHONWARNINGS=ignore spark-master python3 /app/src/setup_namespaces.py

verify:
	@echo "${BLUE}Running Verification...${END}"
	@docker exec -e SPARK_REMOTE=${SPARK_REMOTE} -e PYTHONWARNINGS=ignore spark-master python3 /app/src/verify.py

# --- Helpers ---

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Infrastructure:"
	@echo "  up             Build and start the cluster"
	@echo "  stop           Stop all containers"
	@echo "  clean          Remove containers and volumes"
	@echo "  ps             List running containers"
	@echo ""
	@echo "Pipelines:"
	@echo "  run-transaction-pipeline  Execute the full E2E pipeline"
	@echo "  ingest-transactions       Run Spark SDP ingestion"
	@echo "  transform-transactions    Run dbt transformations"
	@echo ""
	@echo "Tools:"
	@echo "  lint           Run Python and SQL linters"
	@echo "  verify         Run data integrity verification"
	@echo "  clean-warehouse  Wipe all Iceberg data and checkpoints"

# Helpers for colors
BLUE=\033[94m
END=\033[0m

# View logs
logs:
	docker compose logs -f

# Check status
ps:
	docker compose ps
