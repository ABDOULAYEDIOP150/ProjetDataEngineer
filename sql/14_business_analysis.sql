-- 1. Chiffre d'affaires total

SELECT
    SUM(line_total) AS total_revenue
FROM mart.fact_sales;


-- 2. Chiffre d'affaires par mois

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.line_total) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM mart.fact_sales f
JOIN mart.dim_date d
    ON f.order_date = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 3. Top 10 produits par chiffre d'affaires

SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.line_total) AS total_revenue
FROM mart.fact_sales f
JOIN mart.dim_products p
    ON f.product_id = p.product_id
GROUP BY
    p.product_name,
    p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Panier moyen

SELECT
    ROUND(
        SUM(line_total) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM mart.fact_sales;


-- 5. Top 10 clients par chiffre d'affaires

SELECT
    c.full_name,
    c.city,
    c.country,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.line_total) AS total_revenue
FROM mart.fact_sales f
JOIN mart.dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.full_name,
    c.city,
    c.country
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. Commandes par statut

SELECT
    status,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(line_total) AS total_revenue
FROM mart.fact_sales
GROUP BY status
ORDER BY total_orders DESC;


-- 7. Montant payé par méthode de paiement

SELECT
    payment_method,
    COUNT(*) AS total_payments,
    SUM(amount) AS total_amount
FROM mart.fact_payments
GROUP BY payment_method
ORDER BY total_amount DESC;