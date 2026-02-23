select cast(number as long) as id from {{ source('raw', 'source_numbers') }}
