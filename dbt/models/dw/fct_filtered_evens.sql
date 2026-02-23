select id from {{ ref('stg_numbers') }} where id % 2 = 0
