import os

from pyspark.sql import SparkSession


def main():
    remote_url = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")
    spark = SparkSession.builder.remote(remote_url).getOrCreate()

    namespaces = ["raw", "stg", "dw", "mrt"]
    for ns in namespaces:
        print(f"\n--- Namespace: {ns} ---")
        try:
            spark.sql(f"DESCRIBE NAMESPACE EXTENDED {ns}").show(truncate=False)
        except Exception as e:
            print(f"Error describing {ns}: {e}")

    print("\n--- Catalog Configuration ---")
    spark.sql("SHOW CATALOGS").show()

    spark.stop()


if __name__ == "__main__":
    main()
