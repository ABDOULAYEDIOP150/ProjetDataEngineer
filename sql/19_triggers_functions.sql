-- =====================================================
-- 19 - FUNCTIONS AND TRIGGERS
-- =====================================================

-- Table de logs

CREATE TABLE IF NOT EXISTS mart.data_change_logs (
    log_id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Fonction trigger

CREATE OR REPLACE FUNCTION mart.log_fact_sales_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO mart.data_change_logs (
        table_name,
        action_type
    )
    VALUES (
        'fact_sales',
        'INSERT'
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Trigger sur fact_sales

DROP TRIGGER IF EXISTS trg_log_fact_sales_insert
ON mart.fact_sales;

CREATE TRIGGER trg_log_fact_sales_insert
AFTER INSERT ON mart.fact_sales
FOR EACH ROW
EXECUTE FUNCTION mart.log_fact_sales_insert();


-- Fonction SQL simple : chiffre d'affaires par client

CREATE OR REPLACE FUNCTION mart.get_customer_revenue(customer_id_param INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC;
BEGIN
    SELECT
        COALESCE(SUM(line_total), 0)
    INTO total
    FROM mart.fact_sales
    WHERE customer_id = customer_id_param;

    RETURN total;
END;
$$ LANGUAGE plpgsql;


-- Tester la fonction

SELECT mart.get_customer_revenue(1) AS customer_1_revenue;


-- Voir les logs

SELECT *
FROM mart.data_change_logs
ORDER BY changed_at DESC;