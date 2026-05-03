-- Jointure brute (raw)

SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.full_name,
    p.amount
FROM raw.orders o
JOIN raw.customers c
    ON o.customer_id = c.customer_id
LEFT JOIN raw.payments p
    ON o.order_id = p.order_id
LIMIT 10;