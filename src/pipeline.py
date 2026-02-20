from pyspark import pipelines as dp
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from assets import TABLE_RAW_SOURCE, TABLE_STG_SOURCE, TABLE_FCT_EVENS, TABLE_MRT_STATS

def spark():
    return SparkSession.getActiveSession()

# 1. RAW Layer
@dp.materialized_view(name=TABLE_RAW_SOURCE)
def create_raw():
    return spark().range(0, 100).select(col("id").alias("number"))

# 2. STG Layer: Staging (Type Casting, Renaming)
@dp.materialized_view(name=TABLE_STG_SOURCE)
def create_stg():
    # Example: Explicitly casting to ensure data types are correct for the DW
    return spark().table(TABLE_RAW_SOURCE).select(
        col("number").cast("long").alias("id")
    )

# 3. DW Layer: Fact Table (Filtered Data)
@dp.materialized_view(name=TABLE_FCT_EVENS)
def create_fct():
    return spark().table(TABLE_STG_SOURCE).filter(col("id") % 2 == 0)

# 4. MRT Layer: Final Aggregates (Marts)
@dp.materialized_view(name=TABLE_MRT_STATS)
def create_mrt():
    return spark().table(TABLE_FCT_EVENS).selectExpr("sum(id) as total_sum")
