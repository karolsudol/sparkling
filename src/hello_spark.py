
import os
from pyspark.sql import SparkSession

app_name = os.environ.get("SPARK_APP_NAME", "PySparkHelloWorld")

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def main():
    """
    A simple PySpark hello world application with colored output.
    """
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}SPARK_APP_NAME: {app_name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")

    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .getOrCreate()

        print(f"{Colors.GREEN}Successfully created SparkSession for app: {spark.sparkContext.appName}{Colors.END}")
        print(f"Spark version: {spark.version}")
        print(f"Spark master: {spark.sparkContext.master}")

        # Create a simple DataFrame
        data = [("hello", 1), ("world", 2), ("from", 3), ("pyspark", 4)]
        columns = ["message", "id"]
        df = spark.createDataFrame(data, columns)

        # Show the DataFrame
        print(f"{Colors.YELLOW}DataFrame created successfully:{Colors.END}")
        df.show()

        # Perform a simple operation
        df_filtered = df.filter(df["id"] >= 3)
        print(f"{Colors.YELLOW}DataFrame after filtering (id >= 3):{Colors.END}")
        df_filtered.show()

        spark.stop()

    except Exception as e:
        print(f"{Colors.RED}An error occurred: {e}{Colors.END}")

if __name__ == "__main__":
    main()
