from pyspark import pipelines as dp
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Helper to get session concisely
def spark():
    return SparkSession.getActiveSession()

@dp.materialized_view(name="local.default.source_numbers")
def create_source():
    return spark().range(0, 100).select(col("id").alias("number"))

@dp.materialized_view(name="local.default.filtered_evens")
def process_numbers():
    # Use the full name to refer to the Iceberg table
    return spark().table("local.default.source_numbers").filter(col("number") % 2 == 0)

@dp.materialized_view(name="local.default.final_stats")
def compute_stats():
    # Use the full name to refer to the Iceberg table
    return spark().table("local.default.filtered_evens").selectExpr("sum(number) as total_sum")
