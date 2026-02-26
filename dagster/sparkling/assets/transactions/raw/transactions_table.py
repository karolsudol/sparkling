import subprocess

from dagster import AssetExecutionContext, Output, asset
from sparkling.assets.transactions.raw.transactions_csv import transactions_csv
from sparkling.config import ICEBERG_CATALOG, SPARK_REMOTE
from sparkling.resources.spark import SparkConnectResource


@asset(
    deps=[transactions_csv],
    group_name="transactions_raw",
    key_prefix=[ICEBERG_CATALOG, "raw"],
    compute_kind="spark",
    tags={"pipeline": "transactions"},
)
def transactions(context: AssetExecutionContext, spark: SparkConnectResource):
    """Ingests transactions from CSV into the Iceberg raw.transactions table."""
    # 1. Trigger the SDP pipeline
    cmd = [
        "spark-pipelines",
        "run",
        "--spec",
        "/app/pipelines/raw_transactions.yml",
        "--remote",
        SPARK_REMOTE,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    context.log.info(result.stdout)

    # 2. Capture Metadata using the Spark Connect resource
    session = spark.get_session("DagsterMetadataGatherer")
    try:
        table_path = f"{ICEBERG_CATALOG}.raw.transactions"
        row_count = session.table(table_path).count()
    except Exception as e:
        context.log.warning(f"Could not fetch row count: {e}")
        row_count = 0

    return Output(
        value=None,
        metadata={
            "table": f"{ICEBERG_CATALOG}.raw.transactions",
            "num_rows": row_count,
            "preview": f"{ICEBERG_CATALOG}.raw.transactions",
        },
    )
