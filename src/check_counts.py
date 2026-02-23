from config import SPARK_REMOTE
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()
    tables = [
        "raw.transactions",
        "stg.stg_transactions",
        "dw.fct_transactions",
        "mrt.mrt_user_stats",
    ]
    for t in tables:
        try:
            count = spark.table(f"spark_catalog.{t}").count()
            print(f"Table {t:20} Count: {count}")
        except Exception as e:
            print(f"Table {t:20} Error: {e}")
    spark.stop()


if __name__ == "__main__":
    main()
