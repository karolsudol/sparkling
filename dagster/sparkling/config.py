import os
from pathlib import Path


def is_docker():
    return os.path.exists("/.dockerenv")


# Base paths
if is_docker():
    _DEFAULT_DBT_DIR = "/app/dbt"
else:
    _DEFAULT_DBT_DIR = str(Path(__file__).parent.parent.parent / "dbt")

DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", _DEFAULT_DBT_DIR)
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR", DBT_PROJECT_DIR)

# Spark Connect
SPARK_REMOTE = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")

# Iceberg
ICEBERG_CATALOG = os.getenv("ICEBERG_CATALOG", "spark_catalog")
