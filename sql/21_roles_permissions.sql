-- =====================================================
-- 21 - ROLES AND PERMISSIONS
-- =====================================================

-- ── 1. Rôle lecture seule ──────────────────────────
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles WHERE rolname = 'readonly_user'
    ) THEN
        CREATE ROLE readonly_user LOGIN PASSWORD 'readonly_password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE ecommerce_dw TO readonly_user;
GRANT USAGE ON SCHEMA mart TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA mart TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
    GRANT SELECT ON TABLES TO readonly_user;


-- ── 2. Rôle app_user (dashboard Streamlit) ─────────
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles WHERE rolname = 'app_user'
    ) THEN
        CREATE ROLE app_user LOGIN PASSWORD 'votre_mot_de_passe';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE ecommerce_dw TO app_user;

GRANT USAGE ON SCHEMA raw     TO app_user;
GRANT USAGE ON SCHEMA staging TO app_user;
GRANT USAGE ON SCHEMA mart    TO app_user;

GRANT SELECT ON ALL TABLES IN SCHEMA raw     TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA staging TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA mart    TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA raw
    GRANT SELECT ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging
    GRANT SELECT ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
    GRANT SELECT ON TABLES TO app_user;


-- ── 3. Vérification ────────────────────────────────
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee IN ('readonly_user', 'app_user')
  AND table_schema IN ('raw', 'staging', 'mart')
ORDER BY grantee, table_schema, table_name;
