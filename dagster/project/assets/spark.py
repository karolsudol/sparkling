import subprocess

from dagster import AssetExecutionContext, Output, asset

from ..config import ICEBERG_CATALOG, SPARK_REMOTE
from ..resources.spark import SparkConnectResource


@asset(group_name="raw")
def transactions_csv(context: AssetExecutionContext):
    """Generates the raw transaction CSV files in the landing zone."""
    # We can reuse the existing script
    result = subprocess.run(
        ["python3", "/app/src/generate_transactions.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    context.log.info(result.stdout)
    return "data/landing"


@asset(deps=[transactions_csv], group_name="raw", key_prefix=[ICEBERG_CATALOG, "raw"])
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


@asset(deps=[[ICEBERG_CATALOG, "mrt", "mrt_user_stats"]], group_name="mrt")
def final_stats_report(context: AssetExecutionContext, spark: SparkConnectResource):
    """Fetches and logs the final user statistics with metadata."""
    # 1. Run the existing show_marts.py for console output
    subprocess.run(["python3", "/app/src/show_marts.py"], check=True)

    # 2. Capture specific metrics for Dagster UI
    session = spark.get_session("DagsterReporter")
    session.sql(f"USE {ICEBERG_CATALOG}")
    df = session.table(f"{ICEBERG_CATALOG}.mrt.mrt_user_stats")

    total_users = df.count()
    max_spent = df.agg({"total_spent": "max"}).collect()[0][0]

    return Output(
        value=None,
        metadata={
            "total_users": total_users,
            "max_individual_spend": float(max_spent) if max_spent else 0.0,
        },
    )
