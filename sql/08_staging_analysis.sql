-- Jointure propre (staging)

SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.full_name,
    p.amount
FROM staging.orders o
JOIN staging.customers c
    ON o.customer_id = c.customer_id
LEFT JOIN staging.payments p
    ON o.order_id = p.order_id
LIMIT 10;