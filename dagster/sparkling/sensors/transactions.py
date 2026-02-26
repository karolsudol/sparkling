import os

from dagster import DagsterRunStatus, RunRequest, sensor
from dagster._core.storage.pipeline_run import RunsFilter

from ..jobs.transactions import transactions_job

LANDING_DIR = "/app/data/landing"


@sensor(job=transactions_job)
def transactions_landing_sensor(context):
    """
    Monitors the landing zone for new CSV files.
    Only triggers if the pipeline is not already running.
    """
    if not os.path.exists(LANDING_DIR):
        return

    # 1. Concurrency Check: Don't fire if the job is already in progress
    active_runs = context.instance.get_runs(
        filters=RunsFilter(
            job_name="transactions_job",
            statuses=[
                DagsterRunStatus.STARTED,
                DagsterRunStatus.STARTING,
                DagsterRunStatus.QUEUED,
            ],
        ),
        limit=1,
    )

    if active_runs:
        context.log.info(
            "Transactions job is already in progress. Skipping sensor check."
        )
        return

    # 2. File Check
    new_files = [
        f
        for f in os.listdir(LANDING_DIR)
        if f.endswith(".csv") and os.path.isfile(os.path.join(LANDING_DIR, f))
    ]

    if not new_files:
        return

    # Use the file list as a cursor to identify new batches
    last_seen_files = context.cursor or ""
    current_files_str = ",".join(sorted(new_files))

    if current_files_str != last_seen_files:
        context.update_cursor(current_files_str)
        yield RunRequest(
            run_key=current_files_str,
            message=f"New data detected: {current_files_str}",
        )
