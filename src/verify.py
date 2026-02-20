from pyspark.sql import SparkSession
from utils import get_logger, Colors

# Get our Spark-style logger
logger = get_logger("Verify")

def verify_pipeline_results(spark):
    logger.info("--- VERIFYING PIPELINE RESULTS ---")
    tables = ["source_numbers", "filtered_evens", "final_stats"]
    for t in tables:
        logger.info(f"Checking Materialized View: {t}")
        try:
            df = spark.read.parquet(f"/app/spark-warehouse/{t}")
            df.show(5)
        except Exception as e:
            logger.error(f"Table {t} could not be read: {e}")

def main():
    spark = SparkSession.builder.appName("PipelineVerifier").getOrCreate()
    
    verify_pipeline_results(spark)
    
    logger.info(f"{Colors.BOLD}Verification Complete! 🥂{Colors.END}")
    spark.stop()

if __name__ == "__main__":
    main()
