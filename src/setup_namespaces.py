from pyspark.sql import SparkSession
from config import SPARK_REMOTE, NAMESPACES, WAREHOUSE_PATH

def main():
    spark = SparkSession.builder.remote(SPARK_REMOTE).getOrCreate()
    
    for ns in NAMESPACES:
        # Construct the location path explicitly
        # This resolves the 'Cannot open table: path is not set' error
        location = f"{WAREHOUSE_PATH}/{ns}"
        print(f"Creating namespace: {ns} with location: {location}")
        
        # We need to drop and re-create if we want to change the location, 
        # but for a fresh start CREATE NAMESPACE ... LOCATION is best
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {ns} LOCATION '{location}'")
    
    spark.stop()

if __name__ == "__main__":
    main()
