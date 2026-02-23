import os


def is_docker():
    """Checks if the script is running inside a Docker container."""
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/self/cgroup", "rt") as ifh:
            return "docker" in ifh.read()
    except Exception:
        return False


# Spark Connect Configuration
_DEFAULT_REMOTE = "sc://spark-connect:15002" if is_docker() else "sc://localhost:15002"
SPARK_REMOTE = os.getenv("SPARK_REMOTE", _DEFAULT_REMOTE)

# Iceberg Catalog Configuration
ICEBERG_CATALOG = os.getenv("ICEBERG_CATALOG", "spark_catalog")
ICEBERG_URI = os.getenv(
    "ICEBERG_URI",
    "http://iceberg-rest:8181" if is_docker() else "http://localhost:8181",
)
WAREHOUSE_PATH = os.getenv("WAREHOUSE_PATH", "file:///app/spark-warehouse/iceberg")

# Namespaces (Medallion Layers)
RAW = "raw"
STG = "stg"
DW = "dw"
MRT = "mrt"

NAMESPACES = [RAW, STG, DW, MRT]


def get_table_name(namespace, table):
    """Returns the fully qualified table name."""
    return f"{ICEBERG_CATALOG}.{namespace}.{table}"
