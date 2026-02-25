from config import SPARK_REMOTE
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()
    print("--- Transactions in DW ---")
    spark.table("spark_catalog.dw.fct_transactions").orderBy(
        "event_at", ascending=False
    ).show(20, truncate=False)

    print("--- User Stats in MRT ---")
    spark.table("spark_catalog.mrt.mrt_user_stats").show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
