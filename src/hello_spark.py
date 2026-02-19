import os
from pyspark.sql import SparkSession

# Get the Spark master URL from an environment variable
spark_master_url = os.environ.get("SPARK_MASTER_URL", "spark://spark-master:7077")
app_name = os.environ.get("SPARK_APP_NAME", "PySparkHelloWorld")

def main():
    """
    A simple PySpark hello world application.
    """
    print("="*50)
    print(f"SPARK_APP_NAME: {app_name}")
    print(f"Connecting to Spark master at: {spark_master_url}")
    print("="*50)

    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .master(spark_master_url) \
            .getOrCreate()

        print(f"Successfully created SparkSession for app: {spark.sparkContext.appName}")
        print(f"Spark version: {spark.version}")

        # Create a simple DataFrame
        data = [("hello", 1), ("world", 2), ("from", 3), ("pyspark", 4)]
        columns = ["message", "id"]
        df = spark.createDataFrame(data, columns)

        # Show the DataFrame
        print("DataFrame created successfully:")
        df.show()

        # Perform a simple operation
        df_filtered = df.filter(df["id"] >= 3)
        print("DataFrame after filtering (id >= 3):")
        df_filtered.show()

        spark.stop()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()