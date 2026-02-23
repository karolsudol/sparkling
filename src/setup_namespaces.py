from config import NAMESPACES, SPARK_REMOTE, WAREHOUSE_PATH
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()

    for ns in NAMESPACES:
        location = f"{WAREHOUSE_PATH}/{ns}"
        print(f"Ensuring namespace: {ns} with location: {location}")
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {ns} LOCATION '{location}'")

    spark.stop()


if __name__ == "__main__":
    main()
