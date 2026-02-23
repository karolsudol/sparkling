from pyspark.sql import SparkSession
from config import SPARK_REMOTE, NAMESPACES, WAREHOUSE_PATH

def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()
    
    for ns in NAMESPACES:
        location = f"{WAREHOUSE_PATH}/{ns}"
        print(f"Ensuring namespace: {ns} with location: {location}")
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {ns} LOCATION '{location}'")
    
    spark.stop()

if __name__ == "__main__":
    main()
