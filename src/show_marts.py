from config import SPARK_REMOTE
from pyspark.sql import SparkSession
from utils import Colors, get_logger

logger = get_logger("MartsViewer")


def show_final_stats(spark):
    logger.info(f"{Colors.BOLD}--- FINAL USER STATISTICS (MRT LAYER) ---{Colors.END}")

    try:
        # Load the final mart table
        df = spark.table("mrt.mrt_user_stats")

        # Sort by total_spent to make it interesting
        df_sorted = df.orderBy("total_spent", ascending=False)

        print("\n")
        df_sorted.show(truncate=False)
        print("\n")

        # Show some meta info
        total_users = df.count()
        logger.info(f"Summary: Tracking {total_users} unique users.")

    except Exception as e:
        logger.error(f"Could not load mrt.mrt_user_stats: {e}")
        logger.info("Make sure the pipeline has run at least once.")


def main():
    # Detects local vs docker automatically via config.py
    spark = (
        SparkSession.builder.appName("MartsViewer").remote(SPARK_REMOTE).getOrCreate()
    )

    try:
        show_final_stats(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
