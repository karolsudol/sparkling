from pyspark.sql import SparkSession
import os

def main():
    remote_url = os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")
    spark = SparkSession.builder.remote(remote_url).getOrCreate()
    
    namespaces = ["raw", "stg", "dw", "mrt"]
    for ns in namespaces:
        print(f"Creating namespace: {ns}")
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {ns}")
    
    spark.stop()

if __name__ == "__main__":
    main()
