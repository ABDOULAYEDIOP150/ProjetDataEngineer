import streamlit as st
import psycopg2
import os

st.title("Test connexion PostgreSQL")

# ─── Variables de connexion ───
host     = os.getenv("DB_HOST",     "localhost")
port     = int(os.getenv("DB_PORT", 5432))
dbname   = os.getenv("DB_NAME",     "ecommerce_dw")
user     = os.getenv("DB_USER",     "postgres")
password = os.getenv("DB_PASSWORD", "postgres")

st.markdown("### Paramètres utilisés")
st.code(f"host={host}  port={port}  db={dbname}  user={user}")

# ─── Test de connexion ───
if st.button("Tester la connexion"):
    try:
        conn = psycopg2.connect(
            host=host, port=port,
            dbname=dbname, user=user, password=password,
            connect_timeout=5
        )
        cur = conn.cursor()

        # Version PostgreSQL
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]

        # Liste des schémas
        cur.execute("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog','information_schema')
            ORDER BY schema_name
        """)
        schemas = [r[0] for r in cur.fetchall()]

        # Liste des tables
        cur.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog','information_schema')
            ORDER BY table_schema, table_name
        """)
        tables = cur.fetchall()

        conn.close()

        st.success("Connexion réussie !")
        st.info(f"Version : {version.split(',')[0]}")

        st.markdown("**Schémas trouvés :**")
        st.write(schemas)

        if tables:
            st.markdown("**Tables trouvées :**")
            for schema, table in tables:
                st.write(f"  • {schema}.{table}")
        else:
            st.warning("Aucune table trouvée.")

    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
2
