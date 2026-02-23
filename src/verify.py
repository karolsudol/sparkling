from pyspark.sql import SparkSession
from utils import get_logger, Colors
from assets import TABLE_RAW_SOURCE, TABLE_STG_SOURCE, TABLE_FCT_EVENS, TABLE_MRT_STATS
from config import SPARK_REMOTE

logger = get_logger("Verify")

def verify_pipeline_results(spark):
    logger.info("--- VERIFYING MDS-STYLE ICEBERG PIPELINE ---")
    
    tables = [TABLE_RAW_SOURCE, TABLE_STG_SOURCE, TABLE_FCT_EVENS, TABLE_MRT_STATS]
    
    for t in tables:
        logger.info(f"Checking Table: {t}")
        try:
            df = spark.table(t)
            df.show(5)
            
            # Show snapshots
            logger.info(f"Recent snapshots for {t}:")
            spark.sql(f"SELECT snapshot_id, committed_at, operation FROM {t}.snapshots").show(1, truncate=False)
            
        except Exception as e:
            logger.error(f"Table {t} could not be read: {e}")

def main():
    spark = SparkSession.builder \
        .appName("IcebergVerifier") \
        .remote(SPARK_REMOTE) \
        .getOrCreate()
    
    try:
        verify_pipeline_results(spark)
    finally:
        logger.info(f"{Colors.BOLD}Verification Complete! 🥂{Colors.END}")
        spark.stop()

if __name__ == "__main__":
    main()
