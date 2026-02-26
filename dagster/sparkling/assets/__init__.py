from sparkling.assets.dbt import sparkling_dbt_assets
from sparkling.assets.transactions import all_transactions_assets

all_assets = [sparkling_dbt_assets, *all_transactions_assets]
