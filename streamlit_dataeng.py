import os,,,
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Data Pipeline",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1d2e 0%, #16213e 100%);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892b0;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .section-title {
        font-size: 1.1rem;
        color: #00d4ff;
        border-left: 3px solid #00d4ff;
        padding-left: 12px;
        margin: 20px 0 15px 0;
    }
    div[data-testid="stSidebarContent"] { background-color: #1a1d2e; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SECRETS / ENV
# ─────────────────────────────────────────
def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

# ─────────────────────────────────────────
# CONNEXION POSTGRESQL
# ─────────────────────────────────────────
@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host=get_secret("DB_HOST"),
            port=int(get_secret("DB_PORT", 5432)),
            dbname=get_secret("DB_NAME"),
            user=get_secret("DB_USER"),
            password=get_secret("DB_PASSWORD"),
            connect_timeout=10,
            sslmode="require",
        )
        return conn
    except Exception as e:
        st.error(f"❌ Erreur connexion PostgreSQL : {e}")
        return None

@st.cache_data(ttl=30)
def query(sql_query):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        return pd.read_sql_query(sql_query, conn)
    except Exception as e:
        st.error(f"❌ Erreur SQL : {e}")
        return pd.DataFrame()

def get_tables(schema):
    df = query(f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{schema}'
          AND table_type IN ('BASE TABLE', 'VIEW')
        ORDER BY table_name;
    """)
    return df["table_name"].tolist() if not df.empty else []

def load_table(schema, table, limit=1000):
    return query(f'SELECT * FROM "{schema}"."{table}" LIMIT {int(limit)};')

# ─────────────────────────────────────────
# EXPLORATION
# ─────────────────────────────────────────
def show_exploration(df, key_suffix=""):
    if df is None or df.empty:
        st.warning("Aucune donnée dans cette table.")
        return

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(df):,}</div>
            <div class='metric-label'>Lignes</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(df.columns)}</div>
            <div class='metric-label'>Colonnes</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{int(df.isnull().sum().sum())}</div>
            <div class='metric-label'>Valeurs nulles</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{int(df.duplicated().sum())}</div>
            <div class='metric-label'>Doublons</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 Aperçu", "📈 Distributions", "🔍 Qualité"])

    with tab1:
        st.markdown("<div class='section-title'>Données</div>", unsafe_allow_html=True)
        st.dataframe(df.astype(str), width="stretch", height=350)

        st.markdown("<div class='section-title'>Types & complétude</div>", unsafe_allow_html=True)
        meta = pd.DataFrame({
            "Colonne": df.columns,
            "Type": df.dtypes.astype(str).values,
            "Non-nuls": df.count().values,
            "Nulls": df.isnull().sum().values,
            "% Complet": (df.count().values / len(df) * 100).round(1),
        })
        st.dataframe(meta, width="stretch", hide_index=True)

        num_df = df.select_dtypes(include=np.number)
        if not num_df.empty:
            st.markdown("<div class='section-title'>Statistiques descriptives</div>", unsafe_allow_html=True)
            st.dataframe(num_df.describe().round(2), width="stretch")

    with tab2:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

        if num_cols:
            st.markdown("<div class='section-title'>Colonnes numériques</div>", unsafe_allow_html=True)
            sel = st.selectbox("Colonne numérique", num_cols, key=f"num_{key_suffix}")

            ca, cb = st.columns(2)

            with ca:
                fig = px.histogram(
                    df,
                    x=sel,
                    nbins=30,
                    template="plotly_dark",
                    color_discrete_sequence=["#00d4ff"],
                    title=f"Distribution — {sel}",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, width="stretch")

            with cb:
                fig2 = px.box(
                    df,
                    y=sel,
                    template="plotly_dark",
                    color_discrete_sequence=["#7c3aed"],
                    title=f"Box plot — {sel}",
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig2, width="stretch")

        if cat_cols:
            st.markdown("<div class='section-title'>Colonnes catégorielles</div>", unsafe_allow_html=True)
            sel_cat = st.selectbox("Colonne catégorielle", cat_cols, key=f"cat_{key_suffix}")
            vc = df[sel_cat].astype(str).value_counts().head(15)

            fig3 = px.bar(
                x=vc.index,
                y=vc.values,
                template="plotly_dark",
                labels={"x": sel_cat, "y": "Nombre"},
                title=f"Top valeurs — {sel_cat}",
                color=vc.values,
                color_continuous_scale="Blues",
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            st.plotly_chart(fig3, width="stretch")

        if len(num_cols) >= 2:
            st.markdown("<div class='section-title'>Matrice de corrélation</div>", unsafe_allow_html=True)
            corr = df[num_cols].corr().round(2)

            fig4 = px.imshow(
                corr,
                template="plotly_dark",
                color_continuous_scale="RdBu_r",
                title="Corrélations",
                zmin=-1,
                zmax=1,
                text_auto=True,
            )
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=400,
            )
            st.plotly_chart(fig4, width="stretch")

    with tab3:
        st.markdown("<div class='section-title'>Complétude par colonne</div>", unsafe_allow_html=True)

        quality = pd.DataFrame({
            "Colonne": df.columns,
            "% Complet": (df.count() / len(df) * 100).round(1),
            "Valeurs uniques": df.nunique(),
            "Type": df.dtypes.astype(str),
        }).reset_index(drop=True)

        fig_q = px.bar(
            quality,
            x="Colonne",
            y="% Complet",
            color="% Complet",
            color_continuous_scale=["#ff4444", "#ffaa00", "#00d4ff"],
            range_color=[0, 100],
            template="plotly_dark",
            title="Complétude (%)",
        )
        fig_q.add_hline(
            y=95,
            line_dash="dash",
            line_color="#00d4ff",
            annotation_text="Seuil 95%",
        )
        fig_q.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_q, width="stretch")
        st.dataframe(quality, width="stretch", hide_index=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <div style='font-size:1.4rem; color:#00d4ff; font-weight:700;'>
            🛒 DATA PIPELINE
        </div>
        <div style='color:#8892b0; font-size:0.8rem; margin-top:5px;'>
            E-Commerce Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    conn = get_connection()
    if conn:
        st.success("✅ PostgreSQL connecté")
    else:
        st.error("❌ Connexion échouée")
        st.stop()

    st.divider()

    module = st.radio(
        "MODULE",
        [
            "🗂️ RAW — Données Brutes",
            "🔄 STAGING — Données Transformées",
            "📊 MART — Analyse & KPIs",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("""
    <div style='color:#8892b0; font-size:0.75rem;'>
        PostgreSQL · dbt · Airflow<br/>
        CI/CD GitHub Actions ✅
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# DEBUG SCHEMAS
# ─────────────────────────────────────────
raw_tables = get_tables("raw")
staging_tables = get_tables("staging")
mart_tables = get_tables("mart")

st.sidebar.write("DB_USER:", get_secret("DB_USER"))
st.sidebar.write("DB_NAME:", get_secret("DB_NAME"))
st.sidebar.write("RAW TABLES:", raw_tables)
st.sidebar.write("STAGING TABLES:", staging_tables)
st.sidebar.write("MART TABLES:", mart_tables)

with st.sidebar.expander("🔎 Debug tables"):
    st.write("raw:", raw_tables)
    st.write("staging:", staging_tables)
    st.write("mart:", mart_tables)

# ─────────────────────────────────────────
# MODULE RAW
# ─────────────────────────────────────────
if "RAW" in module:
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        🗂️ Données Brutes <span style='color:#00d4ff'>RAW</span>
    </h2>
    <p style='color:#8892b0;'>
        Données ingérées avant transformation — schéma <code>raw</code>
    </p>
    """, unsafe_allow_html=True)

    if raw_tables:
        col_sel, col_lim = st.columns([3, 1])

        with col_sel:
            selected = st.selectbox("Table RAW", raw_tables)

        with col_lim:
            limit = st.number_input(
                "Limite",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100,
                key="limit_raw",
            )

        df = load_table("raw", selected, limit)
        show_exploration(df, key_suffix="raw")
    else:
        st.error("Aucune table dans le schéma raw.")

# ─────────────────────────────────────────
# MODULE STAGING
# ─────────────────────────────────────────
elif "STAGING" in module:
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        🔄 Données <span style='color:#7c3aed'>STAGING</span>
    </h2>
    <p style='color:#8892b0;'>
        Données nettoyées et transformées — schéma <code>staging</code>
    </p>
    """, unsafe_allow_html=True)

    if staging_tables:
        col_sel, col_lim = st.columns([3, 1])

        with col_sel:
            selected = st.selectbox("Table STAGING", staging_tables)

        with col_lim:
            limit = st.number_input(
                "Limite",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100,
                key="limit_staging",
            )

        df_stg = load_table("staging", selected, limit)

        if selected in raw_tables:
            df_raw_cmp = load_table("raw", selected, 10000)

            st.markdown("<div class='section-title'>Impact des transformations</div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)

            raw_n = len(df_raw_cmp)
            stg_n = len(df_stg)
            diff = raw_n - stg_n

            with c1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{raw_n:,}</div>
                    <div class='metric-label'>Lignes RAW</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{stg_n:,}</div>
                    <div class='metric-label'>Lignes STAGING</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                color = "#ff4444" if diff > 0 else "#00d4ff"
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='color:{color};'>{diff:,}</div>
                    <div class='metric-label'>Filtrées</div>
                </div>
                """, unsafe_allow_html=True)

            fig_cmp = go.Figure(data=[
                go.Bar(name="RAW", x=["Lignes"], y=[raw_n], marker_color="#ff4444"),
                go.Bar(name="STAGING", x=["Lignes"], y=[stg_n], marker_color="#00d4ff"),
            ])
            fig_cmp.update_layout(
                barmode="group",
                template="plotly_dark",
                title="RAW vs STAGING",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_cmp, width="stretch")
            st.markdown("---")

        show_exploration(df_stg, key_suffix="staging")
    else:
        st.error("Aucune table dans le schéma staging.")

# ─────────────────────────────────────────
# MODULE MART
# ─────────────────────────────────────────
elif "MART" in module:
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        📊 Data Mart <span style='color:#00d4ff'>& KPIs</span>
    </h2>
    <p style='color:#8892b0;'>
        Tables agrégées pour l'analyse métier — schéma <code>mart</code>
    </p>
    """, unsafe_allow_html=True)

    if mart_tables:
        fact_sales = load_table("mart", "fact_sales", 10000) if "fact_sales" in mart_tables else pd.DataFrame()
        fact_payments = load_table("mart", "fact_payments", 10000) if "fact_payments" in mart_tables else pd.DataFrame()
        dim_customers = load_table("mart", "dim_customers", 10000) if "dim_customers" in mart_tables else pd.DataFrame()
        dim_products = load_table("mart", "dim_products", 10000) if "dim_products" in mart_tables else pd.DataFrame()

        st.markdown("<div class='section-title'>📌 KPIs Principaux</div>", unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)

        df_fact = fact_sales if not fact_sales.empty else fact_payments

        rev_col = next(
            (
                c for c in [
                    "total_amount",
                    "amount",
                    "revenue",
                    "sale_amount",
                    "payment_amount",
                ]
                if c in df_fact.columns
            ),
            None,
        )

        total_rev = df_fact[rev_col].sum() if rev_col and not df_fact.empty else 0
        n_orders = df_fact["order_id"].nunique() if "order_id" in df_fact.columns else len(df_fact)
        n_customers = dim_customers["customer_id"].nunique() if not dim_customers.empty and "customer_id" in dim_customers.columns else 0
        n_products = dim_products["product_id"].nunique() if not dim_products.empty and "product_id" in dim_products.columns else 0
        avg_basket = total_rev / n_orders if n_orders > 0 else 0

        with c1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total_rev:,.0f}€</div>
                <div class='metric-label'>Chiffre d'affaires</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{n_orders:,}</div>
                <div class='metric-label'>Commandes</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{n_customers:,}</div>
                <div class='metric-label'>Clients</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{n_products:,}</div>
                <div class='metric-label'>Produits</div>
            </div>
            """, unsafe_allow_html=True)

        with c5:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{avg_basket:.1f}€</div>
                <div class='metric-label'>Panier moyen</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        if not fact_sales.empty and rev_col:
            st.markdown("<div class='section-title'>📈 Analyse des ventes</div>", unsafe_allow_html=True)

            date_col = next((c for c in fact_sales.columns if "date" in c.lower()), None)

            ca, cb = st.columns(2)

            with ca:
                if date_col:
                    ts = fact_sales.copy()
                    ts[date_col] = pd.to_datetime(ts[date_col], errors="coerce")
                    ts = ts.dropna(subset=[date_col])
                    ts["month"] = ts[date_col].dt.to_period("M").astype(str)

                    monthly = ts.groupby("month")[rev_col].sum().reset_index()

                    fig = px.area(
                        monthly,
                        x="month",
                        y=rev_col,
                        template="plotly_dark",
                        title="CA mensuel",
                        color_discrete_sequence=["#00d4ff"],
                    )
                    fig.update_traces(fill="tozeroy", fillcolor="rgba(0,212,255,0.1)")
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(fig, width="stretch")

            with cb:
                fig2 = px.histogram(
                    fact_sales,
                    x=rev_col,
                    nbins=40,
                    template="plotly_dark",
                    title="Distribution du CA",
                    color_discrete_sequence=["#7c3aed"],
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig2, width="stretch")

        if not dim_customers.empty:
            st.markdown("<div class='section-title'>👥 Analyse Clients</div>", unsafe_allow_html=True)
            show_exploration(dim_customers, key_suffix="customers")

        if not dim_products.empty:
            st.markdown("<div class='section-title'>📦 Analyse Produits</div>", unsafe_allow_html=True)
            show_exploration(dim_products, key_suffix="products")

        st.markdown("---")
        st.markdown("<div class='section-title'>🔍 Exploration libre</div>", unsafe_allow_html=True)

        sel_table = st.selectbox("Choisir une table mart", mart_tables)
        lim = st.slider("Nombre de lignes", 100, 5000, 1000, 100)
        df_sel = load_table("mart", sel_table, lim)

        show_exploration(df_sel, key_suffix="mart_libre")

    else:
        st.error("Aucune table dans le schéma mart.")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#8892b0; font-size:0.75rem;'>
    PostgreSQL → dbt (raw → staging → mart) → Airflow → CI/CD GitHub Actions → Docker Hub
</div>
""", unsafe_allow_html=True)
