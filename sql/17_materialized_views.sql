-- =====================================================
-- 17 - MATERIALIZED VIEWS
-- =====================================================

DROP MATERIALIZED VIEW IF EXISTS mart.mv_sales_by_month;

CREATE MATERIALIZED VIEW mart.mv_sales_by_month AS
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.line_total) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_quantity
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


-- Index sur la vue matérialisée

CREATE INDEX IF NOT EXISTS idx_mv_sales_by_month_year_month
ON mart.mv_sales_by_month(year, month);


-- Lire la vue matérialisée

SELECT *
FROM mart.mv_sales_by_month;


-- Rafraîchir la vue matérialisée après nouvelles données

REFRESH MATERIALIZED VIEW mart.mv_sales_by_month;