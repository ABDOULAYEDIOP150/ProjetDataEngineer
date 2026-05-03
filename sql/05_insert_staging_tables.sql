INSERT INTO staging.customers
SELECT DISTINCT
    customer_id,
    full_name,
    LOWER(email) AS email,
    phone,
    city,
    country,
    created_at::timestamp
FROM raw.customers;

INSERT INTO staging.products
SELECT DISTINCT
    product_id,
    product_name,
    category,
    price::numeric(10,2),
    created_at::timestamp
FROM raw.products;

INSERT INTO staging.orders
SELECT DISTINCT
    order_id,
    customer_id,
    order_date::timestamp,
    status
FROM raw.orders;

INSERT INTO staging.order_items
SELECT DISTINCT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price::numeric(10,2),
    line_total::numeric(10,2)
FROM raw.order_items;

INSERT INTO staging.payments
SELECT DISTINCT
    payment_id,
    order_id,
    payment_method,
    amount::numeric(10,2),
    payment_date::timestamp,
    payment_status
FROM raw.payments;