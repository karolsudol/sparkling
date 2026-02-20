from pyspark.sql import SparkSession
from utils import get_logger, Colors

# Get our Spark-style logger
logger = get_logger("Verify")

def verify_pipeline_results(spark):
    logger.info("--- VERIFYING ICEBERG PIPELINE RESULTS ---")
    
    # We now use the full catalog name
    tables = [
        "local.default.source_numbers", 
        "local.default.filtered_evens", 
        "local.default.final_stats"
    ]
    
    for t in tables:
        logger.info(f"Checking Iceberg Table: {t}")
        try:
            # For Iceberg, we always use spark.table() to benefit from the catalog
            df = spark.table(t)
            df.show(5)
            
            # Bonus: Let's show Iceberg snapshots to prove it's working!
            logger.info(f"Recent snapshots for {t}:")
            spark.sql(f"SELECT snapshot_id, committed_at, operation FROM local.default.{t.split('.')[-1]}.snapshots").show(1, truncate=False)
            
        except Exception as e:
            logger.error(f"Table {t} could not be read: {e}")

def main():
    import os
    # Check if we are running inside Docker or locally
    remote_url = os.getenv("SPARK_REMOTE", "sc://localhost:15002")
    
    logger.info(f"Connecting to Spark Connect at: {remote_url}")
    
    spark = SparkSession.builder \
        .appName("IcebergVerifier") \
        .remote(remote_url) \
        .getOrCreate()
    
    try:
        verify_pipeline_results(spark)
    finally:
        logger.info(f"{Colors.BOLD}Verification Complete! 🥂{Colors.END}")
        spark.stop()

if __name__ == "__main__":
    main()
