from project.assets.transactions.dw import all_dw_assets
from project.assets.transactions.mrt import all_mrt_assets
from project.assets.transactions.raw import all_raw_assets
from project.assets.transactions.stg import all_stg_assets

all_transactions_assets = [
    *all_raw_assets,
    *all_stg_assets,
    *all_dw_assets,
    *all_mrt_assets,
]
