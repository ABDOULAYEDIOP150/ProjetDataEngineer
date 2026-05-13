# 🚀 ProjetDataEngineer — Enterprise End-to-End Data Platform

![CI](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/cd.yml/badge.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![dbt](https://img.shields.io/badge/dbt-Core-orange)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Render](https://img.shields.io/badge/Render-Cloud-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![Analytics](https://img.shields.io/badge/Analytics-Engineering-brightgreen)
![DBA](https://img.shields.io/badge/PostgreSQL-DBA-darkblue)

---

# 📌 Overview

**ProjetDataEngineer** est une plateforme Data Engineering complète simulant une architecture moderne utilisée en entreprise.

Le projet reproduit l’intégralité du cycle de vie de la donnée :

```text
APIs / CSV / Faker / JSON
                ↓
Python Data Ingestion
                ↓
PostgreSQL RAW Layer
                ↓
SQL Transformations
                ↓
dbt STAGING Models
                ↓
dbt MART Models
                ↓
Star Schema Analytics
                ↓
Data Quality Testing
                ↓
Apache Airflow Orchestration
                ↓
Analytics Dashboard (Streamlit + Power BI)
                ↓
Docker Deployment
                ↓
CI/CD GitHub Actions
                ↓
Cloud Infrastructure
(Render + Streamlit Cloud)```

---

# 🎯 Project Goals

Construire une plateforme Data Engineering moderne capable de :

- ingérer des données depuis plusieurs sources
- automatiser les pipelines ETL/ELT
- construire un Data Warehouse PostgreSQL
- modéliser des couches analytiques
- transformer les données avec dbt
- orchestrer des workflows avec Airflow
- implémenter des contrôles qualité
- optimiser les performances SQL
- administrer PostgreSQL
- déployer des applications cloud
- produire des dashboards analytiques
- industrialiser les workflows avec Docker & CI/CD

---

# 🏛️ Enterprise Data Architecture

```text
                  ┌─────────────────────────┐
                    │ APIs / CSV / Faker       │
                    │ JSON / External Data     │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │ Python Ingestion Layer   │
                    │ pandas / requests        │
                    │ SQLAlchemy / logging     │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │ PostgreSQL RAW           │
                    │ Raw transactional data   │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │ dbt STAGING              │
                    │ Cleaning & Validation    │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │ dbt MART                 │
                    │ STAR SCHEMA              │
                    │ Fact & Dimension tables  │
                    └──────────┬──────────────┘
                               │
                    ┌──────────┴──────────────┐
                    │                         │
                    ▼                         ▼
         ┌──────────────────┐    ┌────────────────────┐
         │ Streamlit Cloud  │    │  Power BI Desktop  │
         │ Python Dashboard │    │  Connected to      │
         │ Plotly Charts    │    │  PostgreSQL Cloud  │
         └──────────────────┘    └────────────────────┘
```

---

# 🧠 Engineering Domains Covered

Ce projet couvre plusieurs domaines du Data & Software Engineering modernes.

---

## 🔹 Data Engineering

- ETL / ELT pipelines
- ingestion multi-sources
- Data Warehouse PostgreSQL
- orchestration Airflow
- transformations dbt
- optimisation SQL
- monitoring pipelines
- data quality
- modélisation analytique
- automatisation des workflows

---

## 🔹 Analytics Engineering

Le projet applique les principes modernes d’Analytics Engineering :

- architecture RAW / STAGING / MART
- STAR SCHEMA
- dbt models
- dbt tests
- dbt documentation
- snapshots
- incremental models
- semantic analytics layer
- business metrics standardization

---

## 🔹 Software Engineering

Le projet applique des pratiques Software Engineering professionnelles :

- architecture modulaire
- séparation des responsabilités
- Dockerisation
- CI/CD GitHub Actions
- cloud deployment
- logging
- monitoring
- gestion des erreurs
- variables d’environnement
- clean code architecture
- maintainable pipelines
- scalable project structure

---

## 🔹 Database Administration (DBA)

Le projet couvre plusieurs aspects d’administration PostgreSQL :

### Fonctionnalités DBA

- gestion des schémas PostgreSQL
- rôles SQL
- permissions SQL
- connexions SSL
- indexation
- optimisation SQL
- monitoring PostgreSQL
- vues matérialisées
- transactions SQL
- maintenance PostgreSQL
- sécurité base de données
- tuning SQL
- administration cloud PostgreSQL

---

## 🔹 Cloud & DevOps Engineering

- Docker containers
- GitHub Actions
- CI/CD automation
- Render PostgreSQL
- Streamlit Cloud
- Docker Hub
- environment management
- secrets management

---

## 🔹 Business Intelligence & Analytics

- dashboards interactifs Streamlit
- Power BI Desktop connecté à PostgreSQL
- visualisations Plotly
- KPIs métier
- analytics e-commerce
- reporting analytique
- BI self-service

---

# 🧱 Technology Stack

## 🔹 Data Engineering

- Python
- PostgreSQL
- SQLAlchemy
- psycopg2
- pandas
- Faker
- requests
- dbt
- Apache Airflow

---

## 🔹 Data Warehouse & SQL

- PostgreSQL 16
- PL/pgSQL
- Window Functions
- Materialized Views
- Triggers
- Stored Procedures
- Index Optimization
- Query Tuning

---

## 🔹 Analytics & BI

- Streamlit
- Plotly
- Power BI

---

## 🔹 DevOps & Cloud

- Docker
- Docker Compose
- GitHub Actions
- Docker Hub
- Render PostgreSQL
- Streamlit Cloud

---

# 📂 Enterprise Project Structure

```text
ProjetDataEngineer/
│
├── airflow/
│   ├── dags/
│   ├── plugins/
│   └── logs/
│
├── dashboards/
│   ├── streamlit/
│   └── powerbi/
│
├── dbt/
│   ├── models/
│   │   ├── raw/
│   │   ├── staging/
│   │   ├── mart/
│   │   └── intermediate/
│   │
│   ├── snapshots/
│   ├── macros/
│   ├── tests/
│   ├── analyses/
│   └── dbt_project.yml
│
├── ingestion/
│   ├── api/
│   ├── csv/
│   ├── faker/
│   ├── loaders/
│   ├── validators/
│   └── logs/
│
├── sql/
│   ├── ddl/
│   ├── dml/
│   ├── procedures/
│   ├── triggers/
│   ├── functions/
│   ├── indexes/
│   ├── views/
│   ├── monitoring/
│   └── optimization/
│
├── tests/
│   ├── integration/
│   ├── unit/
│   ├── quality/
│   └── performance/
│
├── docker/
│
├── docs/
│
├── monitoring/
│
├── streamlit_dataeng.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

---

# 🗄️ PostgreSQL Data Warehouse

## 🔹 Database Schemas

```text
raw
staging
mart
audit
monitoring
```

---

# 🧩 RAW Layer

Données brutes ingérées depuis les sources externes.

## 🔹 RAW Tables

```text
customers
products
orders
order_items
payments
shipments
returns
marketing_campaigns
customer_reviews

fakestore_products
fakestore_users
fakestore_carts
```

---

# 🔄 STAGING Layer

Données nettoyées et standardisées.

## 🔹 STAGING Tables

```text
stg_customers
stg_products
stg_orders
stg_order_items
stg_payments
stg_shipments
stg_returns
```

---

# ⭐ MART Layer

Couche analytique finale optimisée BI.

## 🔹 Fact Tables

```text
fact_sales
fact_payments
fact_returns
fact_shipments
```

---

## 🔹 Dimension Tables

```text
dim_customers
dim_products
dim_date
dim_campaigns
dim_regions
```

---

# 🧠 Advanced SQL Features

Le projet implémente des fonctionnalités SQL avancées utilisées en production.

---

## 🔹 SQL Window Functions

```sql
ROW_NUMBER()
RANK()
DENSE_RANK()
LAG()
LEAD()
SUM() OVER()
AVG() OVER()
```

---

## 🔹 PostgreSQL Advanced Features

- vues matérialisées
- triggers SQL
- procédures stockées
- fonctions PL/pgSQL
- contraintes SQL
- colonnes générées
- JSONB
- transactions SQL
- partitionnement
- index composites
- index partiels
- EXPLAIN ANALYZE
- VACUUM / ANALYZE

---

## 🔹 Materialized Views

```text
v_sales_by_month
v_customer_revenue
v_top_products
v_orders_summary
v_return_rates
v_customer_lifetime_value
```

---

# 🔄 Data Ingestion Layer

Le pipeline Python gère :

- ingestion API
- ingestion CSV
- ingestion JSON
- génération Faker
- validation données
- standardisation
- batch inserts PostgreSQL
- gestion erreurs
- logs ingestion
- monitoring

---

# 🔥 dbt Analytics Engineering

Le projet utilise dbt pour industrialiser les transformations analytiques.

---

## 🔹 dbt Features

- sources
- staging models
- mart models
- snapshots
- documentation
- tests
- incremental models
- macros
- lineage

---

## 🔹 dbt Tests

```yaml
unique
not_null
relationships
accepted_values
```

---

## 🔹 Incremental Models

Le projet implémente :

- chargements incrémentaux
- snapshots historiques
- SCD Type 2
- refresh partiels

---

# 🧪 Data Quality & Testing

Le projet implémente plusieurs niveaux de contrôle qualité.

---

## 🔹 SQL Quality Checks

- doublons
- commandes orphelines
- paiements négatifs
- incohérences montants
- emails invalides
- données manquantes
- validation dates

---

## 🔹 Python Tests

- tests unitaires
- tests intégration
- validation pipelines
- validation DataFrames
- validation schémas

---

## 🔹 Performance Tests

- benchmarking SQL
- optimisation requêtes
- tests volumétrie
- monitoring performance

---

# 📈 Monitoring & Observability

Le projet inclut une couche monitoring.

---

## 🔹 Monitoring Features

- logs pipeline
- logs Airflow
- pipeline_runs
- data_quality_checks
- monitoring erreurs
- temps exécution
- métriques pipelines

---

# ⏰ Apache Airflow Orchestration

Le pipeline est orchestré avec Apache Airflow.

---

## 🔹 DAG Principal

```text
extract_data
        ↓
validate_data
        ↓
load_raw_postgres
        ↓
run_staging_models
        ↓
run_mart_models
        ↓
run_dbt_tests
        ↓
refresh_materialized_views
        ↓
generate_reports
        ↓
send_alerts
```

---

## 🔹 Airflow Features

- scheduling automatique
- retries
- monitoring
- logs
- task dependencies
- alerting
- orchestration cloud

---

# 📊 Analytics Dashboard — Streamlit

Dashboard analytique interactif connecté au Data Warehouse PostgreSQL.

---

## 🔹 RAW Module

Exploration des données brutes :

- statistiques descriptives
- distributions
- exploration tables
- qualité données
- valeurs nulles
- doublons

---

## 🔹 STAGING Module

Analyse transformations :

- comparaison RAW vs STAGING
- monitoring nettoyage
- validation transformations
- suivi qualité

---

## 🔹 MART Module

Analytics métier :

- chiffre d’affaires
- revenus mensuels
- panier moyen
- top produits
- segmentation clients
- cohort analysis
- tendances business
- KPIs analytiques

---

# ☁️ Cloud Infrastructure

---

## 🔹 Render PostgreSQL

Le Data Warehouse PostgreSQL est hébergé sur Render.

### Fonctionnalités

- PostgreSQL managé
- stockage cloud
- SSL sécurisé
- haute disponibilité
- accès distant
- backups

---

## 🔹 Streamlit Cloud

Le dashboard est déployé sur Streamlit Community Cloud.

### URL publique

```text
https://endtoenddiopabdoulaye.streamlit.app
```

---

# 🐳 Docker Infrastructure

Le projet est entièrement conteneurisé.

---

## 🔹 Containers

- PostgreSQL
- Airflow
- dbt
- Streamlit

---

## 🔹 Docker Compose

```bash
docker compose up -d
```

---

# 🔄 CI/CD — GitHub Actions

Pipeline CI/CD complet.

---

## 🔹 Automated Workflows

- installation dépendances
- validation Python
- tests SQL
- dbt test
- build Docker
- push Docker Hub
- déploiement cloud

---

# 🔐 Security & Governance

---

## 🔹 Secrets Management

- `.env`
- `st.secrets`
- GitHub Secrets
- Render Secrets

---

## 🔹 PostgreSQL Security

- rôles SQL
- permissions schémas
- accès lecture seule
- connexions SSL
- isolation analytique

---

# 📊 Business KPIs

Le projet génère plusieurs indicateurs métier :

- chiffre d’affaires
- panier moyen
- revenus mensuels
- top produits
- taux retour
- performance paiements
- segmentation clients
- lifetime value
- cohort retention
- delivery performance

---

# 🚀 Running the Project

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer.git

cd ProjetDataEngineer
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure Environment Variables

Créer un fichier `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=password
```

---

## 4️⃣ Start Infrastructure

```bash
docker compose up -d
```

---

## 5️⃣ Run dbt

```bash
dbt run

dbt test
```

---

## 6️⃣ Launch Streamlit

```bash
streamlit run streamlit_dataeng.py
```

---

# 📚 Skills Demonstrated

---

## 🔹 Data Engineering

- ETL / ELT
- Data Warehousing
- dbt
- Airflow
- SQL optimization
- Data Modeling

---

## 🔹 Analytics Engineering

- STAR SCHEMA
- dbt transformations
- metrics modeling
- semantic analytics

---

## 🔹 Software Engineering

- modular architecture
- Dockerization
- CI/CD
- cloud deployment
- logging & monitoring

---

## 🔹 Database Administration

- PostgreSQL administration
- SQL tuning
- indexing
- security
- monitoring
- query optimization

---

## 🔹 Cloud & DevOps

- Render
- Streamlit Cloud
- Docker
- GitHub Actions
- Infrastructure automation

---

# 🎯 Final Result

Cette plateforme démontre la capacité à construire une architecture Data Engineering moderne complète :

✅ ingestion multi-sources  
✅ Data Warehouse PostgreSQL  
✅ transformations dbt  
✅ orchestration Airflow  
✅ monitoring pipelines  
✅ tests qualité  
✅ analytics engineering  
✅ administration PostgreSQL  
✅ dashboard analytique  
✅ Docker infrastructure  
✅ CI/CD automation  
✅ cloud deployment  
✅ architecture scalable & maintenable  

---

# 👨‍💻 Author

# Abdoulaye Diop

## 🔗 GitHub

https://github.com/ABDOULAYEDIOP150

---

# 🌍 Future Improvements

- Kafka streaming
- Spark cluster
- Great Expectations
- Terraform infrastructure
- Kubernetes deployment
- Snowflake integration
- BigQuery version
- Data Mesh architecture
- ML pipelines
- Real-time analytics

---

# ⭐ Portfolio Positioning

Projet conçu pour démontrer des compétences professionnelles en :

- Data Engineering
- Analytics Engineering
- Software Engineering
- Database Administration (DBA)
- SQL Engineering
- BI Engineering
- Cloud Data Platforms
- DevOps Data Infrastructure

---
