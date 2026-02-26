from dagster import AssetSelection, define_asset_job

# The processing pipeline ONLY (starts from Iceberg Raw ingestion)
transactions_job = define_asset_job(
    name="transactions_job",
    selection=AssetSelection.groups("transactions_raw")
    | AssetSelection.groups("transactions_stg")
    | AssetSelection.groups("transactions_dw")
    | AssetSelection.groups("transactions_mrt")
    | AssetSelection.groups("transactions_reporting"),
)
