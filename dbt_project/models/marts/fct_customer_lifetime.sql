with order_items as (
    select * from {{ ref('int_order_items') }}
)

select
    customer_id,
    customer_tier,
    min(order_date) as first_order_date,
    max(order_date) as last_order_date,
    count(distinct order_id) as total_orders,
    sum(line_total) as lifetime_revenue,
    sum(estimated_profit) as lifetime_profit,
    round(avg(line_total), 2) as avg_order_value,
    date_diff(max(order_date), min(order_date), day) as customer_lifespan_days,
    count(distinct category) as categories_purchased
from order_items
group by customer_id, customer_tier
