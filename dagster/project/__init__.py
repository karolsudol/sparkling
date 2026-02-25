from dagster import Definitions, load_assets_from_modules

from .assets import dbt_assets, spark_assets
from .resources import dbt_resource, spark_resource

all_assets = load_assets_from_modules([spark_assets, dbt_assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "spark": spark_resource,
        "dbt": dbt_resource,
    },
)
