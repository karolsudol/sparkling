import os

# Base paths
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "/app/dbt")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR", "/app/dbt")

# Spark Connect
SPARK_REMOTE = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")

# Iceberg
ICEBERG_CATALOG = os.getenv("ICEBERG_CATALOG", "spark_catalog")
