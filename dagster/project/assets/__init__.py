from dagster import load_assets_from_modules

from . import dbt, spark

all_assets = load_assets_from_modules([dbt, spark])
