import subprocess

from dagster import AssetExecutionContext, asset


@asset(
    group_name="transactions_ingestion",
    compute_kind="python",
    tags={"pipeline": "transactions"},
)
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
