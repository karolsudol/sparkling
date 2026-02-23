from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from config import SPARK_REMOTE, ICEBERG_CATALOG, RAW

def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()
    
    table_name = f"{ICEBERG_CATALOG}.{RAW}.source_numbers"
    # Write to raw schema in spark_catalog
    print(f"Seeding {table_name}...")
    df = spark.range(0, 100).select(col("id").alias("number"))
    df.write.format("iceberg").mode("overwrite").saveAsTable(table_name)
    
    print("Done!")
    spark.stop()

if __name__ == "__main__":
    main()
