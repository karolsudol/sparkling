import time
from pyspark.sql import SparkSession
from utils import Colors

def main():
    spark = SparkSession.builder.appName("LazyEvaluationDemo").getOrCreate()
    
    print(f"
{Colors.BLUE}Step 1: Creating a large range of numbers (10 million)...{Colors.END}")
    # This is a Transformation. Spark just notes that it needs to create this.
    df = spark.range(0, 10000000)

    print(f"{Colors.BLUE}Step 2: Adding multiple filters (The 'Recipe')...{Colors.END}")
    start_time = time.time()
    
    # These are all Transformations. Spark is just building a execution plan.
    df_filtered = df.filter(df["id"] % 2 == 0) 
                    .filter(df["id"] % 3 == 0) 
                    .filter(df["id"] % 5 == 0)
    
    end_time = time.time()
    print(f"{Colors.GREEN}Transformations defined in {end_time - start_time:.4f} seconds! (Because Spark did nothing yet){Colors.END}")

    print(f"
{Colors.YELLOW}Step 3: Calling an ACTION (count)...{Colors.END}")
    start_time = time.time()
    
    # This is an ACTION. Spark now optimizes the filters and executes them on the cluster.
    result_count = df_filtered.count()
    
    end_time = time.time()
    print(f"{Colors.GREEN}Action finished in {end_time - start_time:.4f} seconds!{Colors.END}")
    print(f"{Colors.BOLD}Result Count: {result_count}{Colors.END}
")

    spark.stop()

if __name__ == "__main__":
    main()
