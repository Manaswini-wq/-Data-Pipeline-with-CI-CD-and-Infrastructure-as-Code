with order_items as (
    select * from {{ ref('int_order_items') }}
)

select
    order_date,
    region,
    category,
    count(distinct order_id) as total_orders,
    sum(line_total) as revenue,
    sum(estimated_profit) as profit,
    round(avg(line_total), 2) as avg_order_value,
    round(avg(discount_pct), 1) as avg_discount,
    count(distinct customer_id) as unique_customers
from order_items
group by order_date, region, category
