INSERT INTO mart.fact_sales (
    order_id,
    order_item_id,
    customer_id,
    product_id,
    order_date,
    status,
    quantity,
    unit_price,
    line_total
)
SELECT
    o.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    o.order_date::date AS order_date,
    o.status,
    oi.quantity,
    oi.unit_price,
    oi.line_total
FROM staging.orders o
JOIN staging.order_items oi
    ON o.order_id = oi.order_id;

INSERT INTO mart.fact_payments (
    payment_id,
    order_id,
    customer_id,
    payment_date,
    payment_method,
    payment_status,
    amount
)
SELECT
    p.payment_id,
    p.order_id,
    o.customer_id,
    p.payment_date::date AS payment_date,
    p.payment_method,
    p.payment_status,
    p.amount
FROM staging.payments p
JOIN staging.orders o
    ON p.order_id = o.order_id;