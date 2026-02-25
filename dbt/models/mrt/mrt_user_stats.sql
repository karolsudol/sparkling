{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='user_id',
        on_schema_change='append_new_columns'
    )
}}

select
    user_id,
    count(transaction_id) as total_transactions,
    sum(amount) as total_spent,
    max(event_at) as last_active_at
from {{ ref('fct_transactions') }}

{% if is_incremental() %}
    -- Recalculate only for users who have new transactions
    where
        user_id in (
            select distinct user_id
            from {{ ref('fct_transactions') }}
            where event_at > (select max(last_active_at) from {{ this }})
        )
{% endif %}

group by 1
