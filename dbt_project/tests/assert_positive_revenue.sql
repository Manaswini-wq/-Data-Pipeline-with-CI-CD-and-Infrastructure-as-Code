select order_id, line_total
from {{ ref('stg_orders') }}
where line_total < 0
