from dagster import Definitions, load_assets_from_modules

from . import assets, resources

all_assets = load_assets_from_modules([assets.spark, assets.dbt])

defs = Definitions(
    assets=all_assets,
    resources={
        "spark": resources.spark_conn,
        "dbt": resources.dbt_resource,
    },
)
