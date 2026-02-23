from pyspark import pipelines as dp
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType


def spark():
    return SparkSession.getActiveSession()


# Schema for our expressive dataset
source_schema = StructType(
    [
        StructField("transaction_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("event_time", StringType(), True),
    ]
)


# 1. RAW Layer - Incremental Ingestion
# We use a Streaming Table to process only new files dropped in /app/data/landing
@dp.streaming_table(name="raw.transactions")
def ingest_raw():
    return (
        spark()
        .readStream.format("csv")
        .option("header", "true")
        .schema(source_schema)
        .load("/app/data/landing")
    )
