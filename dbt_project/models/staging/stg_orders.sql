with source as (
    select * from {{ source('ecommerce_raw', 'raw_orders') }}
),

cleaned as (
    select
        order_id,
        customer_id,
        product_id,
        quantity,
        unit_price,
        discount_pct,
        cast(order_date as date) as order_date,
        status,
        payment_method,
        region,
        round(quantity * unit_price * (1 - discount_pct / 100), 2) as line_total
    from source
    where status != 'cancelled'
      and quantity > 0
      and unit_price > 0
)

select * from cleaned
