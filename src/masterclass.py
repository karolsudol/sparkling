import time
from pyspark.sql import SparkSession
from utils import get_logger, Colors

# Get our Spark-style logger
logger = get_logger("Masterclass")

def demo_lazy_evaluation(spark):
    logger.info("--- CONCEPT 1: LAZY EVALUATION ---")
    df = spark.range(0, 10000000)
    
    start = time.time()
    # Transformation (Lazy)
    plan = df.filter("id % 2 == 0").filter("id % 3 == 0")
    logger.info(f"Defined Transformations in {time.time() - start:.4f}s (Did nothing yet!)")
    
    start = time.time()
    # Action (Trigger)
    count = plan.count()
    logger.info(f"Executed Action in {time.time() - start:.4f}s (Actually did the work!)")
    logger.info(f"Result: {count} rows")

def verify_pipeline_results(spark):
    logger.info("--- CONCEPT 2: DECLARATIVE PIPELINE RESULTS ---")
    tables = ["source_numbers", "filtered_evens", "final_stats"]
    for t in tables:
        logger.info(f"Checking Materialized View: {t}")
        try:
            df = spark.read.parquet(f"/app/spark-warehouse/{t}")
            # df.show() is still useful for table visualization
            df.show(5)
        except Exception as e:
            logger.error(f"Table {t} could not be read: {e}")

def main():
    spark = SparkSession.builder.appName("SparkMasterclass").getOrCreate()
    
    demo_lazy_evaluation(spark)
    verify_pipeline_results(spark)
    
    logger.info(f"{Colors.BOLD}Masterclass Complete! 🥂{Colors.END}")
    spark.stop()

if __name__ == "__main__":
    main()
