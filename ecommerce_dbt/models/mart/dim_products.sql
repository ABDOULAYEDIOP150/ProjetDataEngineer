SELECT
    product_id,
    product_name,
    category,
    price,
    created_at
FROM {{ ref('stg_products') }}