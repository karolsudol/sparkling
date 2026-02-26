import subprocess

from dagster import AssetExecutionContext, Output, asset
from project.config import ICEBERG_CATALOG
from project.resources.spark import SparkConnectResource


@asset(
    deps=[[ICEBERG_CATALOG, "mrt", "mrt_user_stats"]],
    group_name="reporting",
    compute_kind="python",
    tags={"pipeline": "transactions"},
)
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
