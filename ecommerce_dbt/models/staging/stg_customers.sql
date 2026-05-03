SELECT
    customer_id,
    full_name,
    LOWER(email) AS email,
    city,
    country,
    created_at
FROM raw.customers