-- =====================================================
-- 16 - INDEXES AND PERFORMANCE
-- =====================================================

-- Index sur les clés étrangères des facts

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id
ON mart.fact_sales(customer_id);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product_id
ON mart.fact_sales(product_id);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date
ON mart.fact_sales(order_date);

CREATE INDEX IF NOT EXISTS idx_fact_payments_customer_id
ON mart.fact_payments(customer_id);

CREATE INDEX IF NOT EXISTS idx_fact_payments_payment_date
ON mart.fact_payments(payment_date);


-- Index sur les colonnes souvent filtrées

CREATE INDEX IF NOT EXISTS idx_fact_sales_status
ON mart.fact_sales(status);

CREATE INDEX IF NOT EXISTS idx_dim_products_category
ON mart.dim_products(category);


-- Analyser les tables pour mettre à jour les statistiques PostgreSQL

ANALYZE mart.fact_sales;
ANALYZE mart.fact_payments;
ANALYZE mart.dim_customers;
ANALYZE mart.dim_products;
ANALYZE mart.dim_date;


-- Exemple EXPLAIN ANALYZE

EXPLAIN ANALYZE
SELECT
    p.category,
    SUM(f.line_total) AS total_revenue
FROM mart.fact_sales f
JOIN mart.dim_products p
    ON f.product_id = p.product_id
WHERE f.status = 'delivered'
GROUP BY p.category
ORDER BY total_revenue DESC;