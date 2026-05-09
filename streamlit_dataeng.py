import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

st.title("Test lecture RAW")

try:
    engine = create_engine(
        "postgresql+psycopg2://dba_admin:Pipeline2024!@dpg-d7v3hcfaqgkc73d4ni60-a.oregon-postgres.render.com:5432/ecommerce_dw_ykh0",
        connect_args={"sslmode": "require", "connect_timeout": 10}
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(text('SELECT * FROM raw.orders LIMIT 100'), conn)
    st.success("Connexion réussie !")
    st.dataframe(df)
except Exception as e:
    st.error(f"Erreur : {e}")
