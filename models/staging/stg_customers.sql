{{ config(materialized='view') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    created_at
from {{ source('raw', 'customers') }}
where customer_id is not null
