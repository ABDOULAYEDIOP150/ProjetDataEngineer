import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text

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

    div[data-testid="stSidebarContent"] {
        background-color: #1a1d2e;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONNEXION POSTGRESQL — fidèle à ton test
# ─────────────────────────────────────────
@st.cache_resource
def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://airflow:4PcMUEqxPiA4dLdNielXI11t50tujGOw@dpg-d7v3hcfaqgkc73d4ni60-a.oregon-postgres.render.com:5432/ecommerce_dw_ykh0",
        connect_args={"sslmode": "require", "connect_timeout": 10}
    )
    return engine


@st.cache_data(ttl=300)
def run_query(sql_query):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql_query(text(sql_query), conn)
        return df
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        return pd.DataFrame()


def get_tables(schema):
    return run_query(f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{schema}'
        ORDER BY table_name;
    """)


def load_table(schema, table, limit=1000):
    return run_query(f'SELECT * FROM "{schema}"."{table}" LIMIT {int(limit)};')


# ─────────────────────────────────────────
# OUTILS DASHBOARD
# ─────────────────────────────────────────
def detect_revenue_col(df):
    possible = [
        "total_amount",
        "amount",
        "revenue",
        "sale_amount",
        "payment_amount",
        "price",
        "unit_price"
    ]
    for col in possible:
        if col in df.columns:
            return col
    return None


def detect_date_col(df):
    for col in df.columns:
        if "date" in col.lower() or "created" in col.lower():
            return col
    return None


def show_kpis(df):
    revenue_col = detect_revenue_col(df)
    order_col = "order_id" if "order_id" in df.columns else None
    customer_col = "customer_id" if "customer_id" in df.columns else None

    total_rows = len(df)
    total_cols = len(df.columns)
    total_revenue = df[revenue_col].sum() if revenue_col else 0
    total_orders = df[order_col].nunique() if order_col else total_rows
    total_customers = df[customer_col].nunique() if customer_col else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_rows:,}</div>
            <div class='metric-label'>Lignes</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_cols}</div>
            <div class='metric-label'>Colonnes</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_orders:,}</div>
            <div class='metric-label'>Commandes</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_customers:,}</div>
            <div class='metric-label'>Clients</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_revenue:,.0f}€</div>
            <div class='metric-label'>Revenu</div>
        </div>
        """, unsafe_allow_html=True)


def show_exploration(df, key_prefix):
    if df.empty:
        st.warning("Aucune donnée dans cette table.")
        return

    st.markdown("<div class='section-title'>📌 KPIs</div>", unsafe_allow_html=True)
    show_kpis(df)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Données",
        "📊 Statistiques",
        "📈 Dashboard",
        "🔍 Qualité"
    ])

    with tab1:
        st.markdown("<div class='section-title'>Aperçu des données</div>", unsafe_allow_html=True)
        st.dataframe(df.astype(str), width="stretch", height=400)

    with tab2:
        st.markdown("<div class='section-title'>Statistiques descriptives</div>", unsafe_allow_html=True)

        numeric_df = df.select_dtypes(include=np.number)

        if not numeric_df.empty:
            st.dataframe(numeric_df.describe().round(2), width="stretch")
        else:
            st.info("Aucune colonne numérique détectée.")

        st.markdown("<div class='section-title'>Structure des colonnes</div>", unsafe_allow_html=True)

        meta = pd.DataFrame({
            "colonne": df.columns,
            "type": df.dtypes.astype(str).values,
            "valeurs_nulles": df.isnull().sum().values,
            "valeurs_uniques": df.nunique().values,
            "taux_complet_%": (df.count().values / len(df) * 100).round(2)
        })

        st.dataframe(meta, width="stretch", hide_index=True)

    with tab3:
        st.markdown("<div class='section-title'>Dashboard automatique</div>", unsafe_allow_html=True)

        revenue_col = detect_revenue_col(df)
        date_col = detect_date_col(df)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

        c1, c2 = st.columns(2)

        with c1:
            if revenue_col:
                fig = px.histogram(
                    df,
                    x=revenue_col,
                    nbins=40,
                    template="plotly_dark",
                    title=f"Distribution de {revenue_col}",
                    color_discrete_sequence=["#00d4ff"]
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, width="stretch")
            elif numeric_cols:
                selected_num = st.selectbox(
                    "Colonne numérique",
                    numeric_cols,
                    key=f"{key_prefix}_num_dashboard"
                )
                fig = px.histogram(
                    df,
                    x=selected_num,
                    nbins=40,
                    template="plotly_dark",
                    title=f"Distribution de {selected_num}",
                    color_discrete_sequence=["#00d4ff"]
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, width="stretch")

        with c2:
            if cat_cols:
                selected_cat = st.selectbox(
                    "Colonne catégorielle",
                    cat_cols,
                    key=f"{key_prefix}_cat_dashboard"
                )
                vc = df[selected_cat].astype(str).value_counts().head(15).reset_index()
                vc.columns = [selected_cat, "count"]

                fig = px.bar(
                    vc,
                    x=selected_cat,
                    y="count",
                    template="plotly_dark",
                    title=f"Top valeurs — {selected_cat}",
                    color="count",
                    color_continuous_scale="Blues"
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False
                )
                st.plotly_chart(fig, width="stretch")

        if revenue_col and date_col:
            st.markdown("<div class='section-title'>Évolution temporelle</div>", unsafe_allow_html=True)

            tmp = df.copy()
            tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
            tmp = tmp.dropna(subset=[date_col])

            if not tmp.empty:
                tmp["month"] = tmp[date_col].dt.to_period("M").astype(str)
                monthly = tmp.groupby("month")[revenue_col].sum().reset_index()

                fig = px.area(
                    monthly,
                    x="month",
                    y=revenue_col,
                    template="plotly_dark",
                    title=f"Évolution mensuelle de {revenue_col}",
                    color_discrete_sequence=["#00d4ff"]
                )
                fig.update_traces(fill="tozeroy", fillcolor="rgba(0,212,255,0.15)")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, width="stretch")

        if revenue_col and cat_cols:
            st.markdown("<div class='section-title'>Analyse métier</div>", unsafe_allow_html=True)

            selected_group = st.selectbox(
                "Analyser le revenu par",
                cat_cols,
                key=f"{key_prefix}_revenue_group"
            )

            grouped = (
                df.groupby(selected_group)[revenue_col]
                .sum()
                .sort_values(ascending=False)
                .head(15)
                .reset_index()
            )

            fig = px.bar(
                grouped,
                x=selected_group,
                y=revenue_col,
                template="plotly_dark",
                title=f"{revenue_col} par {selected_group}",
                color=revenue_col,
                color_continuous_scale="Purples"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )
            st.plotly_chart(fig, width="stretch")

    with tab4:
        st.markdown("<div class='section-title'>Qualité des données</div>", unsafe_allow_html=True)

        quality = pd.DataFrame({
            "colonne": df.columns,
            "type": df.dtypes.astype(str).values,
            "valeurs_nulles": df.isnull().sum().values,
            "valeurs_uniques": df.nunique().values,
            "taux_complet_%": (df.count().values / len(df) * 100).round(2)
        })

        fig = px.bar(
            quality,
            x="colonne",
            y="taux_complet_%",
            template="plotly_dark",
            title="Complétude par colonne",
            color="taux_complet_%",
            color_continuous_scale=["#ff4444", "#ffaa00", "#00d4ff"],
            range_color=[0, 100]
        )
        fig.add_hline(
            y=95,
            line_dash="dash",
            line_color="#00d4ff",
            annotation_text="Seuil 95%"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, width="stretch")

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

    try:
        test = run_query("SELECT current_database() AS database, current_user AS user;")
        if not test.empty:
            st.success("✅ PostgreSQL connecté")
            st.caption(f"DB : {test.iloc[0]['database']} · User : {test.iloc[0]['user']}")
        else:
            st.error("❌ Connexion échouée")
            st.stop()
    except Exception as e:
        st.error(f"❌ Connexion échouée : {e}")
        st.stop()

    st.divider()

    module = st.radio(
        "MODULE",
        [
            "🗂️ DataRaw",
            "🔄 STGen",
            "📊 Mart"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div style='color:#8892b0; font-size:0.75rem;'>
        PostgreSQL · dbt · Airflow<br/>
        CI/CD GitHub Actions ✅
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<h1 style='color:white; margin-bottom:5px;'>
    🛒 E-Commerce Data Pipeline
</h1>
<p style='color:#8892b0;'>
    Exploration PostgreSQL · RAW → STAGING → MART
</p>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MODULE DATARAW
# ─────────────────────────────────────────
if module == "🗂️ DataRaw":
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        🗂️ Module <span style='color:#00d4ff'>DataRaw</span>
    </h2>
    <p style='color:#8892b0;'>
        Exploration des données brutes dans le schéma <code>raw</code>.
    </p>
    """, unsafe_allow_html=True)

    tables_df = get_tables("raw")

    if tables_df.empty:
        st.error("Aucune table trouvée dans le schéma raw.")
    else:
        tables = tables_df["table_name"].tolist()

        c1, c2 = st.columns([3, 1])

        with c1:
            selected_table = st.selectbox("Table RAW", tables)

        with c2:
            limit = st.number_input(
                "Limite",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100,
                key="raw_limit"
            )

        df = load_table("raw", selected_table, limit)

        st.markdown(f"<div class='section-title'>Table : raw.{selected_table}</div>", unsafe_allow_html=True)
        show_exploration(df, key_prefix=f"raw_{selected_table}")


# ─────────────────────────────────────────
# MODULE STGEN
# ─────────────────────────────────────────
elif module == "🔄 STGen":
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        🔄 Module <span style='color:#7c3aed'>STGen</span>
    </h2>
    <p style='color:#8892b0;'>
        Exploration des données transformées dans le schéma <code>staging</code>.
    </p>
    """, unsafe_allow_html=True)

    tables_df = get_tables("staging")

    if tables_df.empty:
        st.error("Aucune table trouvée dans le schéma staging.")
    else:
        tables = tables_df["table_name"].tolist()

        c1, c2 = st.columns([3, 1])

        with c1:
            selected_table = st.selectbox("Table STAGING", tables)

        with c2:
            limit = st.number_input(
                "Limite",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100,
                key="staging_limit"
            )

        df = load_table("staging", selected_table, limit)

        st.markdown(f"<div class='section-title'>Table : staging.{selected_table}</div>", unsafe_allow_html=True)
        show_exploration(df, key_prefix=f"staging_{selected_table}")


# ─────────────────────────────────────────
# MODULE MART
# ─────────────────────────────────────────
elif module == "📊 Mart":
    st.markdown("""
    <h2 style='color:#fff; margin-bottom:5px;'>
        📊 Module <span style='color:#00d4ff'>Mart</span>
    </h2>
    <p style='color:#8892b0;'>
        Analyse métier des tables finales dans le schéma <code>mart</code>.
    </p>
    """, unsafe_allow_html=True)

    tables_df = get_tables("mart")

    if tables_df.empty:
        st.error("Aucune table trouvée dans le schéma mart.")
    else:
        tables = tables_df["table_name"].tolist()

        c1, c2 = st.columns([3, 1])

        with c1:
            selected_table = st.selectbox("Table MART", tables)

        with c2:
            limit = st.number_input(
                "Limite",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100,
                key="mart_limit"
            )

        df = load_table("mart", selected_table, limit)

        st.markdown(f"<div class='section-title'>Table : mart.{selected_table}</div>", unsafe_allow_html=True)
        show_exploration(df, key_prefix=f"mart_{selected_table}")


# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#8892b0; font-size:0.75rem;'>
    PostgreSQL → dbt RAW/STAGING/MART → Airflow → Docker Hub → CI/CD GitHub Actions
</div>
""", unsafe_allow_html=True)
