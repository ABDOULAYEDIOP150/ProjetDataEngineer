INSERT INTO mart.dim_customers (
    customer_id,
    full_name,
    email,
    phone,
    city,
    country,
    created_at
)
SELECT
    customer_id,
    full_name,
    email,
    phone,
    city,
    country,
    created_at
FROM staging.customers;

INSERT INTO mart.dim_products (
    product_id,
    product_name,
    category,
    price,
    created_at
)
SELECT
    product_id,
    product_name,
    category,
    price,
    created_at
FROM staging.products;

INSERT INTO mart.dim_date (
    date_id,
    year,
    month,
    day,
    month_name,
    quarter
)
SELECT DISTINCT
    order_date::date AS date_id,
    EXTRACT(YEAR FROM order_date)::integer AS year,
    EXTRACT(MONTH FROM order_date)::integer AS month,
    EXTRACT(DAY FROM order_date)::integer AS day,
    TO_CHAR(order_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM order_date)::integer AS quarter
FROM staging.orders

UNION

SELECT DISTINCT
    payment_date::date AS date_id,
    EXTRACT(YEAR FROM payment_date)::integer AS year,
    EXTRACT(MONTH FROM payment_date)::integer AS month,
    EXTRACT(DAY FROM payment_date)::integer AS day,
    TO_CHAR(payment_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM payment_date)::integer AS quarter
FROM staging.payments;