select sum(id) as total_sum, current_timestamp() as calculated_at
from {{ ref('fct_filtered_evens') }}
