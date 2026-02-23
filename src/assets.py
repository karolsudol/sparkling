from config import DW, MRT, RAW, STG

# --- TABLE NAMES ---
# Source -> Staging -> Fact -> Mart
TABLE_RAW_SOURCE = f"{RAW}.source_numbers"
TABLE_STG_SOURCE = f"{STG}.stg_numbers"
TABLE_FCT_EVENS = f"{DW}.fct_filtered_evens"
TABLE_MRT_STATS = f"{MRT}.mrt_final_stats"
