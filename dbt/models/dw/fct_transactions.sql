{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='transaction_id',
        on_schema_change='append_new_columns'
    )
}}

select transaction_id, user_id, amount, event_at
from {{ ref("stg_transactions") }}
where
    status = "COMPLETED"

    {% if is_incremental() %}
        and event_at > (select max(event_at) from {{ this }})
    {% endif %}
