from sparkling.assets.transactions.dw import all_dw_assets
from sparkling.assets.transactions.mrt import all_mrt_assets
from sparkling.assets.transactions.raw import all_raw_assets
from sparkling.assets.transactions.stg import all_stg_assets

all_transactions_assets = [
    *all_raw_assets,
    *all_stg_assets,
    *all_dw_assets,
    *all_mrt_assets,
]
