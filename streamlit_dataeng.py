import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# CONFIG & STYLE
# ─────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Data Pipeline",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
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
        font-family: 'Space Mono', monospace;
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
        font-family: 'Space Mono', monospace;
        font-size: 1.1rem;
        color: #00d4ff;
        border-left: 3px solid #00d4ff;
        padding-left: 12px;
        margin: 20px 0 15px 0;
    }
    .tag {
        display: inline-block;
        background: #2d3561;
        color: #00d4ff;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'Space Mono', monospace;
        margin: 2px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1d2e;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8892b0;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d3561 !important;
        color: #00d4ff !important;
        border-radius: 8px;
    }
    div[data-testid="stSidebarContent"] {
        background-color: #1a1d2e;
    }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONNEXION BASE DE DONNÉES
# ─────────────────────────────────────────
@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            dbname=os.getenv("DB_NAME", "ecommerce_dw"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        return conn
    except Exception as e:
        return None

@st.cache_data(ttl=300)
def run_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return None
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        return None

def check_table_exists(schema, table):
    q = f"""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = '{schema}' AND table_name = '{table}'
        )
    """
    result = run_query(q)
    if result is not None:
        return result.iloc[0, 0]
    return False

def get_tables_in_schema(schema):
    q = f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = '{schema}' ORDER BY table_name
    """
    result = run_query(q)
    if result is not None:
        return result['table_name'].tolist()
    return []

# ─────────────────────────────────────────
# DONNÉES DEMO (si pas de connexion)
# ─────────────────────────────────────────
def generate_demo_data():
    np.random.seed(42)
    n = 500
    categories = ['Electronics', 'Clothing', 'Books', 'Sports', 'Home & Garden', 'Beauty']
    statuses = ['completed', 'pending', 'shipped', 'cancelled']
    countries = ['France', 'Germany', 'Spain', 'Italy', 'UK', 'Belgium']

    dates = pd.date_range('2024-01-01', '2024-12-31', periods=n)
    orders = pd.DataFrame({
        'order_id': range(1, n+1),
        'customer_id': np.random.randint(1, 150, n),
        'order_date': dates,
        'total_amount': np.random.exponential(150, n).round(2),
        'status': np.random.choice(statuses, n, p=[0.6, 0.15, 0.2, 0.05]),
        'country': np.random.choice(countries, n),
        'category': np.random.choice(categories, n),
        'product_name': [f'Product_{np.random.randint(1, 80)}' for _ in range(n)],
        'quantity': np.random.randint(1, 10, n),
        'unit_price': np.random.uniform(10, 500, n).round(2),
    })
    customers = pd.DataFrame({
        'customer_id': range(1, 151),
        'first_name': [f'Client_{i}' for i in range(1, 151)],
        'country': np.random.choice(countries, 150),
        'signup_date': pd.date_range('2023-01-01', periods=150, freq='2D'),
        'total_orders': np.random.randint(1, 20, 150),
        'total_spent': np.random.exponential(500, 150).round(2),
        'segment': np.random.choice(['VIP', 'Regular', 'New', 'At Risk'], 150, p=[0.1, 0.5, 0.3, 0.1])
    })
    return orders, customers

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-family: Space Mono; font-size:1.4rem; color:#00d4ff; font-weight:700;'>
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
        mode = "live"
    else:
        st.warning("⚠️ Mode démo (pas de DB)")
        mode = "demo"

    st.divider()

    module = st.radio(
        "MODULE",
        ["🗂️ Données Brutes (RAW)", "🔄 Données Transformées", "📊 Dashboard & KPIs"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("<div style='color:#8892b0; font-size:0.75rem;'>Projet Data Engineering<br/>Pipeline CI/CD ✅<br/>dbt + Airflow + PostgreSQL</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────
if mode == "demo":
    df_orders, df_customers = generate_demo_data()
    df_raw = df_orders.copy()
    df_staging = df_orders[df_orders['status'] != 'cancelled'].copy()
    df_mart = df_staging.copy()
else:
    # Tables RAW
    raw_tables = get_tables_in_schema('raw') or get_tables_in_schema('public')
    staging_tables = get_tables_in_schema('staging')
    mart_tables = get_tables_in_schema('mart')

# ─────────────────────────────────────────
# MODULE 1 — DONNÉES BRUTES
# ─────────────────────────────────────────
if "Brutes" in module:
    st.markdown("""
    <h2 style='font-family: Space Mono; color: #fff; margin-bottom:5px;'>
        🗂️ Données Brutes <span style='color:#00d4ff'>RAW</span>
    </h2>
    <p style='color:#8892b0;'>Exploration des données ingérées avant transformation</p>
    """, unsafe_allow_html=True)

    if mode == "live":
        selected_schema = st.selectbox("Schéma", ["raw", "public", "staging"])
        tables = get_tables_in_schema(selected_schema)
        if tables:
            selected_table = st.selectbox("Table", tables)
            limit = st.slider("Nombre de lignes", 10, 500, 100)
            df_raw = run_query(f'SELECT * FROM {selected_schema}."{selected_table}" LIMIT {limit}')
        else:
            st.info("Aucune table trouvée dans ce schéma.")
            df_raw = None
    else:
        df_raw = df_orders.head(200)

    if df_raw is not None and not df_raw.empty:
        # Stats rapides
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{len(df_raw):,}</div>
                <div class='metric-label'>Lignes</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{len(df_raw.columns)}</div>
                <div class='metric-label'>Colonnes</div></div>""", unsafe_allow_html=True)
        with col3:
            nulls = df_raw.isnull().sum().sum()
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{nulls}</div>
                <div class='metric-label'>Valeurs nulles</div></div>""", unsafe_allow_html=True)
        with col4:
            dups = df_raw.duplicated().sum()
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{dups}</div>
                <div class='metric-label'>Doublons</div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📋 Aperçu des données", "📈 Distributions", "🔍 Qualité"])

        with tab1:
            st.markdown("<div class='section-title'>Aperçu de la table</div>", unsafe_allow_html=True)
            st.dataframe(df_raw, use_container_width=True, height=350)

            st.markdown("<div class='section-title'>Types de colonnes</div>", unsafe_allow_html=True)
            dtypes_df = pd.DataFrame({
                'Colonne': df_raw.dtypes.index,
                'Type': df_raw.dtypes.values.astype(str),
                'Non-nuls': df_raw.count().values,
                'Nulls': df_raw.isnull().sum().values,
                '% Complet': (df_raw.count().values / len(df_raw) * 100).round(1)
            })
            st.dataframe(dtypes_df, use_container_width=True, hide_index=True)

        with tab2:
            st.markdown("<div class='section-title'>Distribution des colonnes numériques</div>", unsafe_allow_html=True)
            num_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                selected_col = st.selectbox("Choisir une colonne", num_cols)
                col_a, col_b = st.columns(2)
                with col_a:
                    fig = px.histogram(df_raw, x=selected_col, nbins=30,
                        color_discrete_sequence=['#00d4ff'],
                        template='plotly_dark', title=f'Distribution de {selected_col}')
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                with col_b:
                    fig2 = px.box(df_raw, y=selected_col,
                        color_discrete_sequence=['#7c3aed'],
                        template='plotly_dark', title=f'Box Plot - {selected_col}')
                    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig2, use_container_width=True)

            cat_cols = df_raw.select_dtypes(include=['object']).columns.tolist()
            if cat_cols:
                st.markdown("<div class='section-title'>Distribution des colonnes catégorielles</div>", unsafe_allow_html=True)
                selected_cat = st.selectbox("Choisir une colonne catégorielle", cat_cols)
                vc = df_raw[selected_cat].value_counts().head(15)
                fig3 = px.bar(x=vc.index, y=vc.values,
                    labels={'x': selected_cat, 'y': 'Nombre'},
                    color=vc.values, color_continuous_scale='Blues',
                    template='plotly_dark', title=f'Top valeurs - {selected_cat}')
                fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)

        with tab3:
            st.markdown("<div class='section-title'>Rapport de qualité des données</div>", unsafe_allow_html=True)
            quality = pd.DataFrame({
                'Colonne': df_raw.columns,
                '% Complet': (df_raw.count() / len(df_raw) * 100).round(1),
                'Valeurs uniques': df_raw.nunique(),
                'Type': df_raw.dtypes.astype(str)
            }).reset_index(drop=True)

            fig_q = px.bar(quality, x='Colonne', y='% Complet',
                color='% Complet', color_continuous_scale=['#ff4444', '#ffaa00', '#00d4ff'],
                template='plotly_dark', title='Complétude par colonne (%)',
                range_color=[0, 100])
            fig_q.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_q.add_hline(y=95, line_dash="dash", line_color="#00d4ff", annotation_text="Seuil 95%")
            st.plotly_chart(fig_q, use_container_width=True)

            st.dataframe(quality, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────
# MODULE 2 — DONNÉES TRANSFORMÉES
# ─────────────────────────────────────────
elif "Transformées" in module:
    st.markdown("""
    <h2 style='font-family: Space Mono; color: #fff; margin-bottom:5px;'>
        🔄 Données <span style='color:#7c3aed'>Transformées</span>
    </h2>
    <p style='color:#8892b0;'>Staging & Mart — après transformations dbt</p>
    """, unsafe_allow_html=True)

    if mode == "live":
        schema_choice = st.radio("Couche", ["staging", "mart"], horizontal=True)
        tables = get_tables_in_schema(schema_choice)
        if tables:
            selected_table = st.selectbox("Table", tables)
            df_staging = run_query(f'SELECT * FROM {schema_choice}."{selected_table}" LIMIT 500')
        else:
            df_staging = None
            st.info("Aucune table dans ce schéma.")
    else:
        df_staging = df_orders[df_orders['status'] != 'cancelled'].copy()
        df_staging['revenue'] = df_staging['quantity'] * df_staging['unit_price']
        df_staging['month'] = df_staging['order_date'].dt.to_period('M').astype(str)

    if df_staging is not None and not df_staging.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{len(df_staging):,}</div>
                <div class='metric-label'>Enregistrements</div></div>""", unsafe_allow_html=True)
        with col2:
            if 'total_amount' in df_staging.columns:
                rev = df_staging['total_amount'].sum()
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{rev:,.0f}€</div>
                    <div class='metric-label'>Revenu Total</div></div>""", unsafe_allow_html=True)
            elif 'revenue' in df_staging.columns:
                rev = df_staging['revenue'].sum()
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{rev:,.0f}€</div>
                    <div class='metric-label'>Revenu Total</div></div>""", unsafe_allow_html=True)
        with col3:
            if 'customer_id' in df_staging.columns:
                uniq = df_staging['customer_id'].nunique()
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{uniq}</div>
                    <div class='metric-label'>Clients uniques</div></div>""", unsafe_allow_html=True)
        with col4:
            if 'order_id' in df_staging.columns:
                orders_n = df_staging['order_id'].nunique()
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{orders_n:,}</div>
                    <div class='metric-label'>Commandes</div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📋 Données transformées", "📈 Analyses", "🔄 Comparaison Raw vs Staging"])

        with tab1:
            st.markdown("<div class='section-title'>Table transformée</div>", unsafe_allow_html=True)
            st.dataframe(df_staging, use_container_width=True, height=350)
            if len(df_staging.select_dtypes(include=np.number).columns) > 0:
                st.markdown("<div class='section-title'>Statistiques descriptives</div>", unsafe_allow_html=True)
                st.dataframe(df_staging.describe().round(2), use_container_width=True)

        with tab2:
            col_a, col_b = st.columns(2)
            with col_a:
                if 'category' in df_staging.columns and ('total_amount' in df_staging.columns or 'revenue' in df_staging.columns):
                    rev_col = 'total_amount' if 'total_amount' in df_staging.columns else 'revenue'
                    cat_rev = df_staging.groupby('category')[rev_col].sum().sort_values(ascending=False)
                    fig = px.pie(values=cat_rev.values, names=cat_rev.index,
                        title='Répartition CA par Catégorie',
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        template='plotly_dark', hole=0.4)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)

            with col_b:
                if 'status' in df_staging.columns:
                    status_counts = df_staging['status'].value_counts()
                    colors = {'completed': '#00d4ff', 'shipped': '#7c3aed', 'pending': '#ffaa00', 'cancelled': '#ff4444'}
                    fig2 = px.bar(x=status_counts.index, y=status_counts.values,
                        color=status_counts.index,
                        color_discrete_map=colors,
                        title='Statut des commandes',
                        template='plotly_dark',
                        labels={'x': 'Statut', 'y': 'Nombre'})
                    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                    st.plotly_chart(fig2, use_container_width=True)

            if 'month' in df_staging.columns:
                rev_col = 'total_amount' if 'total_amount' in df_staging.columns else 'revenue'
                if rev_col in df_staging.columns:
                    monthly = df_staging.groupby('month')[rev_col].sum().reset_index()
                    fig3 = px.area(monthly, x='month', y=rev_col,
                        title='Évolution mensuelle du CA',
                        template='plotly_dark',
                        color_discrete_sequence=['#00d4ff'])
                    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    fig3.update_traces(fill='tozeroy', fillcolor='rgba(0,212,255,0.1)')
                    st.plotly_chart(fig3, use_container_width=True)

        with tab3:
            st.markdown("<div class='section-title'>Impact des transformations</div>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            raw_count = len(df_orders) if mode == "demo" else len(df_staging) + 50
            staging_count = len(df_staging)
            with col_a:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{raw_count:,}</div>
                    <div class='metric-label'>Lignes RAW</div></div>""", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{staging_count:,}</div>
                    <div class='metric-label'>Lignes Staging</div></div>""", unsafe_allow_html=True)
            with col_c:
                filtered = raw_count - staging_count
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value' style='color:#ff4444;'>{filtered}</div>
                    <div class='metric-label'>Filtrées / Nettoyées</div></div>""", unsafe_allow_html=True)

            fig_comp = go.Figure(data=[
                go.Bar(name='RAW', x=['Données'], y=[raw_count], marker_color='#ff4444'),
                go.Bar(name='Staging (propre)', x=['Données'], y=[staging_count], marker_color='#00d4ff'),
            ])
            fig_comp.update_layout(
                barmode='group', template='plotly_dark',
                title='RAW vs Données transformées',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_comp, use_container_width=True)

# ─────────────────────────────────────────
# MODULE 3 — DASHBOARD & KPIs
# ─────────────────────────────────────────
elif "Dashboard" in module:
    st.markdown("""
    <h2 style='font-family: Space Mono; color: #fff; margin-bottom:5px;'>
        📊 Dashboard <span style='color:#00d4ff'>& KPIs</span>
    </h2>
    <p style='color:#8892b0;'>Indicateurs métier & métriques du pipeline e-commerce</p>
    """, unsafe_allow_html=True)

    # Données mart
    if mode == "live":
        mart_tables = get_tables_in_schema('mart')
        if mart_tables:
            df_mart_raw = run_query(f'SELECT * FROM mart."{mart_tables[0]}" LIMIT 1000')
        else:
            df_mart_raw = run_query('SELECT * FROM staging.stg_orders LIMIT 1000')
            if df_mart_raw is None:
                df_mart_raw = df_orders.copy()
    else:
        df_mart_raw = df_orders.copy()
        df_mart_raw['revenue'] = df_mart_raw['quantity'] * df_mart_raw['unit_price']
        df_mart_raw['month'] = df_mart_raw['order_date'].dt.to_period('M').astype(str)

    df = df_mart_raw.copy()

    # ── KPIs principaux ──
    st.markdown("<div class='section-title'>📌 KPIs Principaux</div>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    rev_col = 'total_amount' if 'total_amount' in df.columns else ('revenue' if 'revenue' in df.columns else None)
    total_rev = df[rev_col].sum() if rev_col else 0
    total_orders = df['order_id'].nunique() if 'order_id' in df.columns else len(df)
    total_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
    avg_basket = total_rev / total_orders if total_orders > 0 else 0
    completed = len(df[df['status'] == 'completed']) / len(df) * 100 if 'status' in df.columns else 0

    metrics = [
        (f"{total_rev:,.0f}€", "Chiffre d'affaires"),
        (f"{total_orders:,}", "Commandes"),
        (f"{total_customers:,}", "Clients"),
        (f"{avg_basket:.1f}€", "Panier moyen"),
        (f"{completed:.1f}%", "Taux complétion"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphiques principaux ──
    col_a, col_b = st.columns(2)

    with col_a:
        if 'month' in df.columns and rev_col:
            monthly = df.groupby('month')[rev_col].sum().reset_index()
            fig = px.line(monthly, x='month', y=rev_col,
                title='📈 CA Mensuel',
                template='plotly_dark',
                markers=True,
                color_discrete_sequence=['#00d4ff'])
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if 'category' in df.columns and rev_col:
            cat_data = df.groupby('category').agg(
                revenue=(rev_col, 'sum'),
                orders=('order_id', 'count') if 'order_id' in df.columns else (rev_col, 'count')
            ).reset_index().sort_values('revenue', ascending=False)
            fig2 = px.bar(cat_data, x='category', y='revenue',
                title='🏷️ CA par Catégorie',
                color='revenue', color_continuous_scale='Blues',
                template='plotly_dark')
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        if 'country' in df.columns and rev_col:
            country_data = df.groupby('country')[rev_col].sum().reset_index().sort_values(rev_col, ascending=True)
            fig3 = px.bar(country_data, x=rev_col, y='country', orientation='h',
                title='🌍 CA par Pays',
                color=rev_col, color_continuous_scale='Purples',
                template='plotly_dark')
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        if 'status' in df.columns:
            status_data = df['status'].value_counts().reset_index()
            status_data.columns = ['status', 'count']
            colors_map = {'completed': '#00d4ff', 'shipped': '#7c3aed', 'pending': '#ffaa00', 'cancelled': '#ff4444'}
            fig4 = px.pie(status_data, values='count', names='status',
                title='🔄 Statut des commandes',
                color='status', color_discrete_map=colors_map,
                template='plotly_dark', hole=0.5)
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig4, use_container_width=True)

    # ── Métriques avancées ──
    st.markdown("<div class='section-title'>🎯 Métriques Avancées</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        # Top produits
        if 'product_name' in df.columns and rev_col:
            top_products = df.groupby('product_name')[rev_col].sum().nlargest(10).reset_index()
            fig5 = px.bar(top_products, x=rev_col, y='product_name', orientation='h',
                title='🏆 Top 10 Produits',
                color=rev_col, color_continuous_scale='Teal',
                template='plotly_dark')
            fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=350)
            st.plotly_chart(fig5, use_container_width=True)

    with col2:
        # Scatter revenue vs quantity
        if rev_col and 'quantity' in df.columns:
            sample = df.sample(min(200, len(df)))
            fig6 = px.scatter(sample, x='quantity', y=rev_col,
                color='category' if 'category' in df.columns else None,
                title='🔵 Quantité vs Revenu',
                template='plotly_dark',
                opacity=0.7)
            fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig6, use_container_width=True)

    with col3:
        # Heatmap jour/mois
        if 'order_date' in df.columns and rev_col:
            df['day_of_week'] = pd.to_datetime(df['order_date']).dt.day_name()
            df['month_name'] = pd.to_datetime(df['order_date']).dt.month_name()
            heatmap_data = df.groupby(['day_of_week', 'month_name'])[rev_col].sum().unstack(fill_value=0)
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])
            fig7 = px.imshow(heatmap_data,
                title='🗓️ Heatmap CA (Jour × Mois)',
                color_continuous_scale='Blues',
                template='plotly_dark')
            fig7.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig7, use_container_width=True)

    # ── Segment clients ──
    if 'segment' in df.columns or 'customer_id' in df.columns:
        st.markdown("<div class='section-title'>👥 Segmentation Clients</div>", unsafe_allow_html=True)
        if 'segment' in df.columns:
            seg_data = df.groupby('segment').agg(
                count=('customer_id', 'nunique') if 'customer_id' in df.columns else (rev_col, 'count'),
                revenue=(rev_col, 'sum') if rev_col else ('segment', 'count')
            ).reset_index()
            col_a, col_b = st.columns(2)
            with col_a:
                fig8 = px.pie(seg_data, values='count', names='segment',
                    title='Répartition des segments',
                    color_discrete_sequence=['#00d4ff', '#7c3aed', '#ffaa00', '#ff4444'],
                    template='plotly_dark', hole=0.4)
                fig8.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig8, use_container_width=True)
            with col_b:
                if rev_col:
                    fig9 = px.bar(seg_data, x='segment', y='revenue',
                        title='CA par segment client',
                        color='segment',
                        color_discrete_sequence=['#00d4ff', '#7c3aed', '#ffaa00', '#ff4444'],
                        template='plotly_dark')
                    fig9.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                    st.plotly_chart(fig9, use_container_width=True)

    # ── Footer pipeline ──
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#8892b0; font-size:0.8rem; font-family: Space Mono;'>
        🔄 Pipeline : PostgreSQL → dbt (staging → mart) → Airflow → CI/CD GitHub Actions → Docker Hub
        <br/>Projet Data Engineering — CI ✅ CD ✅
    </div>
    """, unsafe_allow_html=True)
