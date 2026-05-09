# 🚀 ProjetDataEngineer — End-to-End Data Engineering Platform

![CI](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/cd.yml/badge.svg)

---

# 📌 Overview

**ProjetDataEngineer** est une plateforme complète de **Data Engineering** construite autour d’un cas métier e-commerce.

Le projet reproduit une architecture moderne utilisée en entreprise :

* ingestion multi-sources
* stockage PostgreSQL
* transformations analytiques avec dbt
* orchestration Airflow
* dashboard interactif Streamlit
* CI/CD GitHub Actions
* conteneurisation Docker
* monitoring et qualité des données
* architecture RAW → STAGING → MART

L’objectif est de démontrer la maîtrise d’un pipeline data industriel de bout en bout.

---

# 🏗️ Architecture globale

```text
CSV / API / Faker
        ↓
Python ingestion pipeline
        ↓
PostgreSQL (RAW layer)
        ↓
dbt transformations
        ↓
STAGING layer
        ↓
MART layer (Star Schema)
        ↓
Analytics / KPIs
        ↓
Streamlit Dashboard
        ↓
Airflow Orchestration
        ↓
GitHub Actions CI/CD
        ↓
Docker / Cloud Deployment
```

---

# 🧭 Architecture technique

## 🔹 Sources de données

Le pipeline ingère plusieurs types de sources :

* CSV (dataset e-commerce)
* API FakeStore
* données simulées avec Faker
* fichiers JSON

---

## 🔹 Ingestion Python

Les scripts Python :

* extraient les données
* nettoient les colonnes
* standardisent les types
* gèrent les erreurs
* chargent PostgreSQL
* loggent les exécutions

Technologies utilisées :

* pandas
* requests
* Faker
* SQLAlchemy
* psycopg2
* python-dotenv

---

## 🔹 PostgreSQL Data Warehouse

Le projet utilise PostgreSQL comme entrepôt de données principal.

Architecture en 3 couches :

```text
raw
staging
mart
```

### RAW

Données brutes ingérées.

Exemples :

```text
raw.customers
raw.orders
raw.products
raw.payments
raw.order_items
raw.fakestore_products
```

### STAGING

Nettoyage et standardisation.

Exemples :

```text
staging.stg_customers
staging.stg_orders
staging.fact_sales
```

### MART

Modèle analytique final.

Exemples :

```text
mart.fact_sales
mart.fact_payments
mart.dim_customers
mart.dim_products
mart.dim_date
```

---

# ⭐ Modélisation analytique

Le projet implémente un modèle en étoile (Star Schema).

## Facts

```text
fact_sales
fact_payments
fact_returns
```

## Dimensions

```text
dim_customers
dim_products
dim_date
```

---

# 🛠️ SQL avancé utilisé

Le projet couvre des fonctionnalités SQL avancées utilisées en entreprise :

## Fonctions fenêtres

```sql
ROW_NUMBER()
RANK()
DENSE_RANK()
LAG()
LEAD()
SUM() OVER()
AVG() OVER()
```

## PostgreSQL avancé

* vues
* vues matérialisées
* index
* index composites
* contraintes
* triggers
* procédures SQL
* fonctions PL/pgSQL
* colonnes générées
* JSONB
* EXPLAIN ANALYZE
* partitionnement
* transactions
* rôles et permissions

---

# 🔄 dbt Transformation Layer

dbt est utilisé pour industrialiser les transformations.

## Fonctionnalités implémentées

* models
* sources
* tests
* documentation
* snapshots
* incremental models
* matérialisation table/view

## Tests dbt

Le projet inclut :

```yaml
- unique
- not_null
- relationships
- accepted_values
```

---

# 🌪️ Apache Airflow

Airflow orchestre l’ensemble du pipeline.

## DAG principal

```text
extract_data
validate_data
load_raw_postgres
run_dbt_models
run_dbt_tests
refresh_materialized_views
export_metrics
send_alert
```

## Fonctionnalités

* scheduling
* retries automatiques
* dépendances entre tâches
* monitoring des jobs
* logs d’exécution

---

# 📊 Dashboard Streamlit

Le projet inclut une application Streamlit complète.

## Modules disponibles

### 🗂️ DataRaw

Exploration des données brutes.

### 🔄 STGen

Exploration des données transformées.

### 📊 Mart

Analyse métier et KPIs.

---

## Fonctionnalités du dashboard

* statistiques descriptives
* qualité des données
* distributions
* corrélations
* KPIs business
* exploration dynamique
* visualisations Plotly
* dashboard temps réel PostgreSQL

---

# 📈 KPIs métier

Le dashboard calcule automatiquement :

* chiffre d’affaires
* panier moyen
* nombre de commandes
* clients actifs
* top produits
* évolution mensuelle
* segmentation clients
* revenus par catégorie

---

# 🧪 Data Quality & Testing

Le projet implémente plusieurs niveaux de tests.

## Tests SQL

Contrôles :

* commandes sans client
* paiements négatifs
* doublons
* clés orphelines
* valeurs nulles
* cohérence des montants

---

## Tests dbt

Tests automatiques sur :

* clés primaires
* relations
* unicité
* complétude

---

## Tests Python

Tests d’intégration :

* connexion PostgreSQL
* présence des tables
* volume chargé
* validation schémas

---

# 📦 Docker & Conteneurisation

Le projet est entièrement dockerisé.

## Services

* PostgreSQL
* Airflow
* dbt
* Streamlit

---

# ⚙️ CI/CD — GitHub Actions

Le pipeline CI/CD automatise :

* tests
* build Docker
* validation dbt
* push Docker Hub
* déploiement cloud

---

# 🔐 Sécurité

Le projet applique plusieurs bonnes pratiques :

* variables d’environnement `.env`
* secrets Streamlit Cloud
* rôles PostgreSQL
* permissions par schéma
* séparation RAW/STAGING/MART
* SSL PostgreSQL

---

# 📂 Structure du projet

```text
ProjetDataEngineer/
│
├── airflow/
├── dashboards/
├── dbt/
├── docker/
├── ingestion/
├── sql/
├── tests/
├── docs/
├── streamlit/
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env.example
```

---

# 🚀 Lancement du projet

## 1. Cloner le repo

```bash
git clone https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer.git
cd ProjetDataEngineer
```

---

## 2. Variables d’environnement

Créer :

```bash
.env
```

Exemple :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## 3. Démarrer Docker

```bash
docker compose up -d
```

---

## 4. Lancer l’ingestion

```bash
python ingestion/load_sources.py
```

---

## 5. Exécuter dbt

```bash
cd ecommerce_dbt

dbt run
dbt test
```

---

## 6. Lancer Streamlit

```bash
streamlit run streamlit_dataeng.py
```

---

# 📊 Stack technologique

## Data Engineering

* Python
* PostgreSQL
* SQLAlchemy
* psycopg2
* pandas
* dbt
* Apache Airflow

## Analytics & BI

* Streamlit
* Plotly
* Power BI
* Looker Studio

## DevOps

* Docker
* GitHub Actions
* Docker Hub
* Render
* Streamlit Cloud

---

# 📸 Captures du projet

## Dashboard Streamlit

* RAW analytics
* STAGING analytics
* MART analytics
* KPIs métier
* distributions statistiques

## Airflow

* DAG orchestration
* scheduling
* monitoring

## PostgreSQL

* schémas RAW/STAGING/MART
* vues matérialisées
* optimisation SQL

---

# 📚 Compétences démontrées

Ce projet démontre :

## Data Engineering

* ingestion pipeline
* ETL/ELT
* modélisation analytique
* orchestration
* qualité des données
* optimisation SQL

## Software Engineering

* architecture modulaire
* Docker
* CI/CD
* monitoring
* logging
* testing

## Analytics Engineering

* dbt
* star schema
* data marts
* KPIs métier

---

# 🎯 Objectif du projet

Construire une plateforme data réaliste reproduisant les standards d’un environnement entreprise.

Le projet démontre la capacité à :

* construire un pipeline robuste
* industrialiser les transformations
* orchestrer des workflows
* monitorer des pipelines
* produire des dashboards analytiques
* déployer une stack data complète

---

# 👨‍💻 Auteur

**Abdoulaye Diop**

Data Engineering Project — End-to-End Modern Data Platform

GitHub :

```text
https://github.com/ABDOULAYEDIOP150
```

---

# 📌 Roadmap future

Améliorations prévues :

* PySpark pipeline
* Kafka streaming
* Great Expectations
* monitoring Prometheus/Grafana
* Terraform infrastructure
* Kubernetes deployment
* Snowflake/BigQuery version
* incremental pipelines avancés
* CDC pipelines

---

# ⭐ Résultat final

Ce projet couvre l’ensemble du cycle Data Engineering moderne :

```text
Sources → Ingestion → PostgreSQL → dbt → Airflow → Analytics → Dashboard → CI/CD → Cloud
```

et reproduit une architecture proche d’un environnement production réel.
