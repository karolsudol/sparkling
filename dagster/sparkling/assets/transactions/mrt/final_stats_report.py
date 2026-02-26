from dagster import AssetExecutionContext, AutomationCondition, Output, asset
from sparkling.config import ICEBERG_CATALOG
from sparkling.resources.spark import SparkConnectResource


@asset(
    deps=[[ICEBERG_CATALOG, "mrt", "mrt_user_stats"]],
    group_name="transactions_reporting",
    compute_kind="python",
    tags={"pipeline": "transactions"},
    automation_condition=AutomationCondition.eager(),
)
def final_stats_report(context: AssetExecutionContext, spark: SparkConnectResource):
    """Fetches and logs the final user statistics with metadata."""
    # Use the injected spark resource instead of a subprocess to avoid double sessions
    session = spark.get_session("DagsterReporter")
    session.sql(f"USE {ICEBERG_CATALOG}")

    table_name = f"{ICEBERG_CATALOG}.mrt.mrt_user_stats"
    context.log.info(f"Fetching statistics from {table_name}...")

    df = session.table(table_name)

    # Sort and log a preview to Dagster compute logs
    df_sorted = df.orderBy("total_spent", ascending=False)
    # We can't use .show() easily for logs, so we'll log the top 10
    preview = df_sorted.limit(10).toPandas().to_string()
    context.log.info(f"Top 10 users by spend:\n{preview}")

    total_users = df.count()
    max_spent = df.agg({"total_spent": "max"}).collect()[0][0]

    return Output(
        value=None,
        metadata={
            "total_users": total_users,
            "max_individual_spend": float(max_spent) if max_spent else 0.0,
            "preview_top_10": preview,
        },
    )
