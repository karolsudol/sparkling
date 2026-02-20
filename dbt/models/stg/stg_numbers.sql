select cast(number as long) as id from {{ ref('source_numbers') }}
