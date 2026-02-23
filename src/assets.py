from config import DW, MRT, RAW, STG

# --- TABLE NAMES ---
# Source -> Staging -> Fact -> Mart
TABLE_RAW_TRANS = f"{RAW}.transactions"
TABLE_STG_TRANS = f"{STG}.stg_transactions"
TABLE_FCT_TRANS = f"{DW}.fct_transactions"
TABLE_MRT_STATS = f"{MRT}.mrt_user_stats"
