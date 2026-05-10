import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ─────────────────────────────────────────
# CHARGEMENT .ENV
# ─────────────────────────────────────────
load_dotenv()

DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "ecommerce_dw")

DB_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ─────────────────────────────────────────
# CONFIG PAGE
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

# Layout Plotly de base — sans showlegend pour éviter tout conflit de kwarg
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#c9d1d9",
)


def apply_layout(fig, showlegend=False):
    """Applique PLOTLY_BASE + showlegend via une seule méthode — jamais de doublon."""
    fig.update_layout(showlegend=showlegend, **PLOTLY_BASE)
    return fig


# ─────────────────────────────────────────
# CONNEXION POSTGRESQL
# ─────────────────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine(DB_URL, connect_args={"connect_timeout": 10})


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
# DÉTECTION COLONNES
# ─────────────────────────────────────────
def detect_revenue_col(df):
    for col in ["total_amount", "amount", "revenue", "sale_amount",
                "payment_amount", "price", "unit_price"]:
        if col in df.columns:
            return col
    return None


def detect_date_col(df):
    for col in df.columns:
        if "date" in col.lower() or "created" in col.lower():
            return col
    return None


# ─────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────
def show_kpis(df):
    revenue_col  = detect_revenue_col(df)
    order_col    = "order_id"    if "order_id"    in df.columns else None
    customer_col = "customer_id" if "customer_id" in df.columns else None

    total_rows      = len(df)
    total_cols      = len(df.columns)
    total_revenue   = df[revenue_col].sum()      if revenue_col   else 0
    total_orders    = df[order_col].nunique()    if order_col     else total_rows
    total_customers = df[customer_col].nunique() if customer_col  else 0

    items = [
        (f"{total_rows:,}",        "Lignes"),
        (str(total_cols),          "Colonnes"),
        (f"{total_orders:,}",      "Commandes"),
        (f"{total_customers:,}",   "Clients"),
        (f"{total_revenue:,.0f}€", "Revenu"),
    ]
    for col, (val, label) in zip(st.columns(5), items):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPERS CHARTS
# ─────────────────────────────────────────
def _boxplot(df, col, title):
    fig = px.box(
        df, y=col,
        template="plotly_dark",
        title=title,
        color_discrete_sequence=["#00d4ff"],
        points="outliers"
    )
    return apply_layout(fig)


def _cat_bar_pct(df, col, title, top_n=15):
    vc = df[col].astype(str).value_counts().head(top_n).reset_index()
    vc.columns = [col, "count"]
    vc["pct"] = (vc["count"] / len(df) * 100).round(2)
    fig = px.bar(
        vc, x=col, y="pct",
        template="plotly_dark",
        title=title,
        color="pct",
        color_continuous_scale="Blues",
        text=vc["pct"].map(lambda x: f"{x:.1f}%"),
        labels={"pct": "% total lignes"}
    )
    fig.update_traces(textposition="outside")
    return apply_layout(fig)


def _cat_pie(df, col, title, top_n=12):
    vc = df[col].astype(str).value_counts().head(top_n).reset_index()
    vc.columns = [col, "count"]
    fig = px.pie(
        vc, names=col, values="count",
        template="plotly_dark",
        title=title,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(textinfo="percent+label")
    return apply_layout(fig, showlegend=True)


def _heatmap_corr(df, cols):
    sub  = df[cols].dropna()
    corr = sub.corr().round(2)
    fig  = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale="RdBu",
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text}",
        hoverongaps=False
    ))
    fig.update_layout(template="plotly_dark", title="Heatmap de corrélation",
                      **PLOTLY_BASE, showlegend=False)
    return fig


def _scatter(df, x_col, y_col, color_col=None):
    """
    Scatter plot sans trendline='ols' pour ne pas dépendre de statsmodels.
    Une ligne de tendance manuelle (numpy polyfit) est ajoutée à la place.
    """
    sub = df[[x_col, y_col] + ([color_col] if color_col else [])].dropna()

    kwargs = dict(template="plotly_dark", title=f"{x_col} vs {y_col}", opacity=0.6)
    if color_col:
        kwargs["color"] = color_col

    fig = px.scatter(sub, x=x_col, y=y_col, **kwargs)

    # Tendance linéaire manuelle (numpy) — uniquement si pas de couleur
    if not color_col and len(sub) > 1:
        x_vals = sub[x_col].values.astype(float)
        y_vals = sub[y_col].values.astype(float)
        try:
            m, b = np.polyfit(x_vals, y_vals, 1)
            x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
            y_line = m * x_line + b
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode="lines",
                name="Tendance",
                line=dict(color="#ff7f0e", width=2, dash="dash")
            ))
        except Exception:
            pass

    return apply_layout(fig, showlegend=color_col is not None)


# ─────────────────────────────────────────
# EXPLORATION PRINCIPALE
# ─────────────────────────────────────────
def show_exploration(df, key_prefix):
    if df.empty:
        st.warning("Aucune donnée dans cette table.")
        return

    st.markdown("<div class='section-title'>📌 KPIs</div>", unsafe_allow_html=True)
    show_kpis(df)
    st.markdown("---")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols     = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    revenue_col  = detect_revenue_col(df)
    date_col     = detect_date_col(df)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Données",
        "📊 Statistiques",
        "📈 Dashboard",
        "🔗 Corrélations",
        "🔍 Qualité",
    ])

    # ── TAB 1 : Données brutes ──────────────────
    with tab1:
        st.markdown("<div class='section-title'>Aperçu des données</div>", unsafe_allow_html=True)
        st.dataframe(df.astype(str), use_container_width=True, height=420)

    # ── TAB 2 : Statistiques ────────────────────
    with tab2:
        st.markdown("<div class='section-title'>Statistiques descriptives</div>", unsafe_allow_html=True)
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)
        else:
            st.info("Aucune colonne numérique détectée.")

        st.markdown("<div class='section-title'>Structure des colonnes</div>", unsafe_allow_html=True)
        meta = pd.DataFrame({
            "colonne":   df.columns,
            "type":      df.dtypes.astype(str).values,
            "nulles":    df.isnull().sum().values,
            "uniques":   df.nunique().values,
            "complet_%": (df.count().values / len(df) * 100).round(2),
        })
        st.dataframe(meta, use_container_width=True, hide_index=True)

    # ── TAB 3 : Dashboard ───────────────────────
    with tab3:
        st.markdown("<div class='section-title'>Dashboard automatique</div>", unsafe_allow_html=True)

        # Numériques → Boxplots
        if numeric_cols:
            st.markdown("<div class='section-title'>📦 Variables numériques — Boxplots</div>", unsafe_allow_html=True)
            num_select = st.multiselect(
                "Colonnes numériques à visualiser",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))],
                key=f"{key_prefix}_num_box"
            )
            if num_select:
                n_cols = min(2, len(num_select))
                rows_needed = (len(num_select) + n_cols - 1) // n_cols
                for row_i in range(rows_needed):
                    cols_ui = st.columns(n_cols)
                    for col_i in range(n_cols):
                        idx = row_i * n_cols + col_i
                        if idx < len(num_select):
                            with cols_ui[col_i]:
                                st.plotly_chart(
                                    _boxplot(df, num_select[idx], f"Boxplot — {num_select[idx]}"),
                                    use_container_width=True
                                )

        # Catégorielles → Bar % + Camembert
        if cat_cols:
            st.markdown("<div class='section-title'>🏷️ Variables catégorielles — Distribution</div>", unsafe_allow_html=True)
            cat_select = st.selectbox(
                "Colonne catégorielle",
                cat_cols,
                key=f"{key_prefix}_cat_select"
            )
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    _cat_bar_pct(df, cat_select, f"% par catégorie — {cat_select}"),
                    use_container_width=True
                )
            with c2:
                st.plotly_chart(
                    _cat_pie(df, cat_select, f"Répartition — {cat_select}"),
                    use_container_width=True
                )

        # Évolution temporelle
        if revenue_col and date_col:
            st.markdown("<div class='section-title'>📅 Évolution temporelle</div>", unsafe_allow_html=True)
            tmp = df.copy()
            tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
            tmp = tmp.dropna(subset=[date_col])
            if not tmp.empty:
                tmp["month"] = tmp[date_col].dt.to_period("M").astype(str)
                monthly = tmp.groupby("month")[revenue_col].sum().reset_index()
                fig = px.area(
                    monthly, x="month", y=revenue_col,
                    template="plotly_dark",
                    title=f"Évolution mensuelle de {revenue_col}",
                    color_discrete_sequence=["#00d4ff"]
                )
                fig.update_traces(fill="tozeroy", fillcolor="rgba(0,212,255,0.15)")
                apply_layout(fig)
                st.plotly_chart(fig, use_container_width=True)

        # Top produits / catégories
        if revenue_col and cat_cols:
            st.markdown("<div class='section-title'>🏆 Analyse produits / catégories</div>", unsafe_allow_html=True)
            group_col = st.selectbox(
                "Grouper par",
                cat_cols,
                key=f"{key_prefix}_group_col"
            )
            top_n = st.slider("Nombre d'éléments", 5, 30, 15, key=f"{key_prefix}_topn")

            grouped = (
                df.groupby(group_col)[revenue_col]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
                .reset_index()
            )
            total_rev  = df[revenue_col].sum()
            total_top  = grouped[revenue_col].sum()
            grouped["% vs top"]   = (grouped[revenue_col] / total_top  * 100).round(2)
            grouped["% vs total"] = (grouped[revenue_col] / total_rev  * 100).round(2)
            grouped["nb_lignes"]  = df.groupby(group_col).size().reindex(grouped[group_col]).values
            grouped["% lignes"]   = (grouped["nb_lignes"]  / len(df)   * 100).round(2)

            fig = px.bar(
                grouped,
                x=group_col, y=revenue_col,
                template="plotly_dark",
                title=f"Top {top_n} — {revenue_col} par {group_col}",
                color="% vs total",
                color_continuous_scale="Purples",
                text=grouped["% vs total"].map(lambda x: f"{x:.1f}%"),
                labels={"% vs total": "% revenu total"}
            )
            fig.update_traces(textposition="outside")
            apply_layout(fig)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<div class='section-title'>📋 Détail top éléments</div>", unsafe_allow_html=True)
            st.dataframe(
                grouped[[group_col, revenue_col, "% vs top", "% vs total", "nb_lignes", "% lignes"]]
                .rename(columns={revenue_col: "Revenu (€)"}),
                use_container_width=True,
                hide_index=True
            )

    # ── TAB 4 : Corrélations ────────────────────
    with tab4:
        st.markdown("<div class='section-title'>🔗 Heatmap de corrélation</div>", unsafe_allow_html=True)
        if len(numeric_cols) < 2:
            st.info("Pas assez de colonnes numériques (minimum 2).")
        else:
            corr_cols = st.multiselect(
                "Colonnes à inclure",
                numeric_cols,
                default=numeric_cols,
                key=f"{key_prefix}_corr_cols"
            )
            if len(corr_cols) >= 2:
                st.plotly_chart(_heatmap_corr(df, corr_cols), use_container_width=True)

                st.markdown("<div class='section-title'>📈 Scatter plot</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    x_col = st.selectbox("Variable X", corr_cols, key=f"{key_prefix}_scatter_x")
                with c2:
                    y_default = min(1, len(corr_cols) - 1)
                    y_col = st.selectbox("Variable Y", corr_cols, index=y_default, key=f"{key_prefix}_scatter_y")

                color_opt = st.selectbox(
                    "Couleur (optionnel)",
                    ["Aucune"] + cat_cols,
                    key=f"{key_prefix}_scatter_color"
                )
                color_arg = None if color_opt == "Aucune" else color_opt
                # Pas de trendline='ols' → pas besoin de statsmodels
                st.plotly_chart(_scatter(df, x_col, y_col, color_arg), use_container_width=True)
            else:
                st.warning("Sélectionne au moins 2 colonnes.")

    # ── TAB 5 : Qualité ─────────────────────────
    with tab5:
        st.markdown("<div class='section-title'>Qualité des données</div>", unsafe_allow_html=True)
        quality = pd.DataFrame({
            "colonne":   df.columns,
            "type":      df.dtypes.astype(str).values,
            "nulles":    df.isnull().sum().values,
            "uniques":   df.nunique().values,
            "complet_%": (df.count().values / len(df) * 100).round(2),
        })
        fig = px.bar(
            quality, x="colonne", y="complet_%",
            template="plotly_dark",
            title="Complétude par colonne",
            color="complet_%",
            color_continuous_scale=["#ff4444", "#ffaa00", "#00d4ff"],
            range_color=[0, 100]
        )
        fig.add_hline(y=95, line_dash="dash", line_color="#00d4ff", annotation_text="Seuil 95%")
        apply_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(quality, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <div style='font-size:1.4rem; color:#00d4ff; font-weight:700;'>🛒 DATA PIPELINE</div>
        <div style='color:#8892b0; font-size:0.8rem; margin-top:5px;'>E-Commerce Analytics</div>
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
        ["🗂️ DataRaw", "🔄 STGen", "📊 Mart"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("""
    <div style='color:#8892b0; font-size:0.75rem;'>
        PostgreSQL · dbt · Airflow<br/>CI/CD GitHub Actions ✅
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<h1 style='color:white; margin-bottom:5px;'>🛒 E-Commerce Data Pipeline</h1>
<p style='color:#8892b0;'>Exploration PostgreSQL · RAW → STAGING → MART</p>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MODULE DATARAW
# ─────────────────────────────────────────
if module == "🗂️ DataRaw":
    st.markdown("""
    <h2 style='color:#fff;'>🗂️ Module <span style='color:#00d4ff'>DataRaw</span></h2>
    <p style='color:#8892b0;'>Données brutes — schéma <code>raw</code>.</p>
    """, unsafe_allow_html=True)

    tables_df = run_query("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'raw'
        AND table_name != 'order_items'
        ORDER BY table_name
    """)

    if tables_df.empty:
        st.error("Aucune table trouvée dans le schéma raw.")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            selected_table = st.selectbox("Table RAW", tables_df["table_name"].tolist())
        with c2:
            limit = st.number_input("Limite", 100, 10000, 1000, 100, key="raw_limit")

        df = load_table("raw", selected_table, limit)
        st.markdown(f"<div class='section-title'>Table : raw.{selected_table}</div>", unsafe_allow_html=True)
        show_exploration(df, key_prefix=f"raw_{selected_table}")


# ─────────────────────────────────────────
# MODULE STGEN  (exclut tables déjà dans RAW + dim/fact)
# ─────────────────────────────────────────
elif module == "🔄 STGen":
    st.markdown("""
    <h2 style='color:#fff;'>🔄 Module <span style='color:#7c3aed'>STGen</span></h2>
    <p style='color:#8892b0;'>Tables transformées — schéma <code>staging</code> (hors doublons RAW, dim, fact).</p>
    """, unsafe_allow_html=True)

    raw_tables_df = run_query("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'raw'
        AND table_name != 'order_items'
    """)
    raw_names = raw_tables_df["table_name"].tolist() if not raw_tables_df.empty else []

    exclude_clause = (
        "AND table_name NOT IN (" + ",".join(f"'{t}'" for t in raw_names) + ")"
        if raw_names else ""
    )

    tables_df = run_query(f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'staging'
        AND table_name NOT LIKE 'dim_%'
        AND table_name NOT LIKE 'fact_%'
        {exclude_clause}
        ORDER BY table_name
    """)

    if tables_df.empty:
        st.info("Toutes les tables staging sont déjà dans RAW, ou seules des tables dim/fact existent.")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            selected_table = st.selectbox("Table STAGING", tables_df["table_name"].tolist())
        with c2:
            limit = st.number_input("Limite", 100, 10000, 1000, 100, key="staging_limit")

        df = load_table("staging", selected_table, limit)
        st.markdown(f"<div class='section-title'>Table : staging.{selected_table}</div>", unsafe_allow_html=True)
        show_exploration(df, key_prefix=f"staging_{selected_table}")


# ─────────────────────────────────────────
# MODULE MART
# ─────────────────────────────────────────
elif module == "📊 Mart":
    st.markdown("""
    <h2 style='color:#fff;'>📊 Module <span style='color:#00d4ff'>Mart</span></h2>
    <p style='color:#8892b0;'>Tables finales — schéma <code>mart</code>.</p>
    """, unsafe_allow_html=True)

    tables_df = get_tables("mart")

    if tables_df.empty:
        st.error("Aucune table trouvée dans le schéma mart.")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            selected_table = st.selectbox("Table MART", tables_df["table_name"].tolist())
        with c2:
            limit = st.number_input("Limite", 100, 10000, 1000, 100, key="mart_limit")

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