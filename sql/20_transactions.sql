-- =====================================================
-- 20 - TRANSACTIONS
-- =====================================================

-- Exemple : transaction contrôlée

BEGIN;

UPDATE mart.fact_payments
SET payment_status = 'checked'
WHERE payment_status = 'paid';

-- Vérifier avant validation

SELECT payment_status, COUNT(*)
FROM mart.fact_payments
GROUP BY payment_status;

-- Si tout est OK :
COMMIT;

-- Si problème, utiliser à la place :
-- ROLLBACK;