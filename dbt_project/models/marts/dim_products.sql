with products as (
    select * from {{ ref('stg_products') }}
),

order_stats as (
    select
        product_id,
        count(distinct order_id) as times_ordered,
        sum(quantity) as total_units_sold,
        sum(line_total) as total_revenue
    from {{ ref('int_order_items') }}
    group by product_id
)

select
    p.product_id,
    p.product_name,
    p.category,
    p.base_price,
    p.cost_price,
    p.margin,
    p.margin_pct,
    coalesce(o.times_ordered, 0) as times_ordered,
    coalesce(o.total_units_sold, 0) as total_units_sold,
    coalesce(o.total_revenue, 0) as total_revenue
from products p
left join order_stats o on p.product_id = o.product_id
