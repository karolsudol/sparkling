from dagster import Definitions

from . import assets, jobs, resources, sensors

defs = Definitions(
    assets=assets.all_assets,
    resources={
        "spark": resources.spark_conn,
        "dbt": resources.dbt_resource,
    },
    jobs=[jobs.transactions_job],
    sensors=[sensors.transactions_landing_sensor],
)
