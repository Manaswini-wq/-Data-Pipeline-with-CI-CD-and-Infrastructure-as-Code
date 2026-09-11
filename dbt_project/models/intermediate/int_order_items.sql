with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    o.order_id,
    o.order_date,
    o.customer_id,
    c.tier as customer_tier,
    c.days_since_signup,
    o.product_id,
    p.product_name,
    p.category,
    o.quantity,
    o.unit_price,
    o.discount_pct,
    o.line_total,
    p.margin_pct as product_margin_pct,
    round(o.line_total * p.margin_pct / 100, 2) as estimated_profit,
    o.payment_method,
    o.region,
    o.status
from orders o
left join customers c on o.customer_id = c.customer_id
left join products p on o.product_id = p.product_id
