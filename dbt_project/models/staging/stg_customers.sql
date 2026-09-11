with source as (
    select * from {{ source('ecommerce_raw', 'raw_customers') }}
)

select
    customer_id,
    name,
    email,
    cast(signup_date as date) as signup_date,
    tier,
    date_diff(current_date(), cast(signup_date as date), day) as days_since_signup
from source
