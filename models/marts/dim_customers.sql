{{ config(materialized='table') }}

select
    customer_id,
    concat(first_name, ' ', last_name) as full_name,
    email,
    date(created_at) as customer_created_date
from {{ ref('stg_customers') }}
