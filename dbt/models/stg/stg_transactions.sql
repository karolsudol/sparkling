{{
    config(
        materialized='incremental',
        incremental_strategy='append'
    )
}}

select
    transaction_id,
    user_id,
    cast(amount as decimal(18, 2)) as amount,
    status,
    cast(event_time as timestamp) as event_at
from {{ source('raw', 'transactions') }}

{% if is_incremental() %}
    -- This filter will only be applied on an incremental run
    where cast(event_time as timestamp) > (select max(event_at) from {{ this }})
{% endif %}
