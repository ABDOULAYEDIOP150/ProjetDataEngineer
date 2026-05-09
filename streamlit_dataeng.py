import streamlit as st
import psycopg2

st.title("Test connexion PostgreSQL")

try:
    conn = psycopg2.connect(
        host="dpg-d7v3hcfaqgkc73d4ni60-a.oregon-postgres.render.com",
        port=5432,
        dbname="ecommerce_dw_ykh0",
        user="airflow",
        password="4PcMUEqxPiA4dLdNielXI11t50tujGOw",
        connect_timeout=5
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]

    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog','information_schema')
        ORDER BY table_schema, table_name
    """)
    tables = cur.fetchall()
    conn.close()

    st.success("Connexion réussie !")
    st.info(version.split(',')[0])

    st.markdown("### Tables trouvées")
    if tables:
        for schema, table in tables:
            st.write(f"• {schema}.{table}")
    else:
        st.warning("Aucune table trouvée.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
