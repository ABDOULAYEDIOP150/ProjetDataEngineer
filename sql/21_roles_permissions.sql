-- =====================================================
-- 21 - ROLES AND PERMISSIONS
-- =====================================================

-- Créer un utilisateur lecture seule

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles WHERE rolname = 'readonly_user'
    ) THEN
        CREATE ROLE readonly_user LOGIN PASSWORD 'readonly_password';
    END IF;
END
$$;


-- Donner accès à la base

GRANT CONNECT ON DATABASE ecommerce_dw TO readonly_user;


-- Donner accès au schema mart

GRANT USAGE ON SCHEMA mart TO readonly_user;


-- Donner lecture seule sur toutes les tables du mart

GRANT SELECT ON ALL TABLES IN SCHEMA mart TO readonly_user;


-- Donner lecture seule sur les futures tables

ALTER DEFAULT PRIVILEGES IN SCHEMA mart
GRANT SELECT ON TABLES TO readonly_user;


-- Vérification

SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'readonly_user';