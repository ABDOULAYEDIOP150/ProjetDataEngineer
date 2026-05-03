SELECT
    customer_id,
    full_name,
    email,
    city,
    country,
    created_at
FROM {{ ref('stg_customers') }}