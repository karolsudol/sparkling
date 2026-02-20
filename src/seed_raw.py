from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

def main():
    remote_url = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")
    spark = SparkSession.builder.remote(remote_url).getOrCreate()
    
    # Write to raw schema in spark_catalog
    print("Seeding spark_catalog.raw.source_numbers...")
    df = spark.range(0, 100).select(col("id").alias("number"))
    df.write.format("iceberg").mode("overwrite").saveAsTable("spark_catalog.raw.source_numbers")
    
    print("Done!")
    spark.stop()

if __name__ == "__main__":
    main()
