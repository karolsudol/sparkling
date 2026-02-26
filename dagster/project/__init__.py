from dagster import Definitions
from project import assets, resources

defs = Definitions(
    assets=assets.all_assets,
    resources={
        "spark": resources.spark_conn,
        "dbt": resources.dbt_resource,
    },
)
