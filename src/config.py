import os

# Spark Connect Configuration
SPARK_REMOTE = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")

# Iceberg Catalog Configuration
ICEBERG_CATALOG = os.getenv("ICEBERG_CATALOG", "spark_catalog")
ICEBERG_URI = os.getenv("ICEBERG_URI", "http://iceberg-rest:8181")
WAREHOUSE_PATH = os.getenv("WAREHOUSE_PATH", "file:///app/spark-warehouse/iceberg")

# Namespaces (Medallion Layers)
RAW = "raw"
STG = "stg"
DW  = "dw"
MRT = "mrt"

NAMESPACES = [RAW, STG, DW, MRT]

def get_table_name(namespace, table):
    """Returns the fully qualified table name."""
    return f"{ICEBERG_CATALOG}.{namespace}.{table}"
