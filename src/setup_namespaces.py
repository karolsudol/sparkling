from config import ICEBERG_CATALOG, NAMESPACES, SPARK_REMOTE, WAREHOUSE_PATH
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()

    for ns in NAMESPACES:
        full_ns = f"{ICEBERG_CATALOG}.{ns}"
        location = f"{WAREHOUSE_PATH}/{ns}"
        print(f"Ensuring namespace: {full_ns} with location: {location}")
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {full_ns} LOCATION '{location}'")

        # Verify it exists
        spark.sql(f"DESCRIBE NAMESPACE {full_ns}").show()

    spark.stop()


if __name__ == "__main__":
    main()
