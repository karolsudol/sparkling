from pyspark import pipelines as dp
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# In SDP, the 'spark' session is automatically available
# but we define it here for local IDE support if needed.

@dp.materialized_view(name="source_numbers")
def create_source():
    spark = SparkSession.getActiveSession()
    return spark.range(0, 100).select(col("id").alias("number"))

@dp.materialized_view(name="filtered_evens")
def process_numbers():
    spark = SparkSession.getActiveSession()
    return spark.table("source_numbers").filter(col("number") % 2 == 0)

@dp.materialized_view(name="final_stats")
def compute_stats():
    spark = SparkSession.getActiveSession()
    return spark.table("filtered_evens").selectExpr("sum(number) as total_sum")
