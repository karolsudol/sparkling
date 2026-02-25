import os
import subprocess

from dagster import AssetExecutionContext, Output, asset


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


@asset(deps=[transactions_csv], group_name="raw", key_prefix=["spark_catalog", "raw"])
def transactions(context: AssetExecutionContext):
    """Ingests transactions from CSV into the Iceberg raw.transactions table."""
    # Trigger the SDP pipeline via shell command (consistent with Makefile)
    cmd = [
        "spark-pipelines",
        "run",
        "--spec",
        "/app/pipelines/raw_transactions.yml",
        "--remote",
        os.getenv("SPARK_REMOTE", "sc://spark-connect:15002"),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    context.log.info(result.stdout)

    return Output(
        value=None,
        metadata={
            "table": "spark_catalog.raw.transactions",
        },
    )
