from config import SPARK_REMOTE
from pyspark.sql import SparkSession
from utils import Colors, get_logger

logger = get_logger("Verify")


def verify_pipeline_results(spark):
    logger.info("--- VERIFYING HYBRID SDP + DBT PIPELINE ---")

    tables = [
        "raw.transactions",
        "stg.stg_transactions",
        "dw.fct_transactions",
        "mrt.mrt_user_stats",
    ]

    for t in tables:
        logger.info(f"Checking Table: {t}")
        try:
            df = spark.table(t)
            df.show(5)

            # Show snapshots for Iceberg tables
            logger.info(f"Recent snapshots for {t}:")
            spark.sql(
                f"SELECT snapshot_id, committed_at, operation FROM {t}.snapshots"
            ).show(1, truncate=False)

        except Exception as e:
            logger.error(f"Table {t} could not be read: {e}")


def main():
    spark = (
        SparkSession.builder.appName("IcebergVerifier")
        .remote(SPARK_REMOTE)
        .getOrCreate()
    )

    try:
        verify_pipeline_results(spark)
    finally:
        logger.info(f"{Colors.BOLD}Verification Complete! 🥂{Colors.END}")
        spark.stop()


if __name__ == "__main__":
    main()
