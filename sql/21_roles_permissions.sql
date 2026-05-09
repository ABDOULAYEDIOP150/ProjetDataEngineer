-- =====================================================
-- 21 - ROLES AND PERMISSIONS
-- =====================================================

-- ── 1. Rôle lecture seule (inchangé) ──────────────────
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles WHERE rolname = 'readonly_user'
    ) THEN
        CREATE ROLE readonly_user LOGIN PASSWORD 'readonly_password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE ecommerce_dw_ykh0 TO readonly_user;

GRANT USAGE ON SCHEMA mart TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA mart TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
    GRANT SELECT ON TABLES TO readonly_user;


-- ── 2. Permissions pour airflow (fix dashboard Streamlit) ─
GRANT USAGE ON SCHEMA raw     TO airflow;
GRANT USAGE ON SCHEMA staging TO airflow;
GRANT USAGE ON SCHEMA mart    TO airflow;

GRANT SELECT ON ALL TABLES IN SCHEMA raw     TO airflow;
GRANT SELECT ON ALL TABLES IN SCHEMA staging TO airflow;
GRANT SELECT ON ALL TABLES IN SCHEMA mart    TO airflow;

ALTER DEFAULT PRIVILEGES IN SCHEMA raw
    GRANT SELECT ON TABLES TO airflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging
    GRANT SELECT ON TABLES TO airflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
    GRANT SELECT ON TABLES TO airflow;


-- ── 3. Vérification ────────────────────────────────────
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee IN ('readonly_user', 'airflow')
  AND table_schema IN ('raw', 'staging', 'mart')
ORDER BY grantee, table_schema, table_name;
