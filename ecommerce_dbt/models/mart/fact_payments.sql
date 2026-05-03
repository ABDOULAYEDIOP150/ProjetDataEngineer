SELECT
    p.payment_id,
    p.order_id,
    o.customer_id,
    p.payment_date,
    p.payment_method,
    p.payment_status,
    p.amount
FROM {{ ref('stg_payments') }} p
JOIN {{ ref('stg_orders') }} o
    ON p.order_id = o.order_id