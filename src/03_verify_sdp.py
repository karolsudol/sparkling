from pyspark.sql import SparkSession
from utils import Colors
import os

def main():
    spark = SparkSession.builder.appName("VerifySDP").getOrCreate()
    
    print(f"\n{Colors.BLUE}Verifying SDP Parquet Files in Warehouse...{Colors.END}")
    
    warehouse_dir = "/app/spark-warehouse"
    tables = ["source_numbers", "filtered_evens", "final_stats"]
    
    for table in tables:
        path = f"{warehouse_dir}/{table}"
        print(f"\n{Colors.YELLOW}Reading Path: {path}{Colors.END}")
        try:
            df = spark.read.parquet(path)
            df.show()
        except Exception as e:
            print(f"{Colors.RED}Error reading {table}: {e}{Colors.END}")

    spark.stop()

if __name__ == "__main__":
    main()
