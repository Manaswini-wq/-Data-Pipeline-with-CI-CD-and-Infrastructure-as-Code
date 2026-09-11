with source as (
    select * from {{ source('ecommerce_raw', 'raw_products') }}
)

select
    product_id,
    product_name,
    category,
    base_price,
    cost_price,
    round(base_price - cost_price, 2) as margin,
    round((base_price - cost_price) / nullif(base_price, 0) * 100, 1) as margin_pct
from source
