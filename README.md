# 🚀 ProjetDataEngineer — End-to-End Data Engineering Platform

![CI](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer/actions/workflows/cd.yml/badge.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![dbt](https://img.shields.io/badge/dbt-Core-orange)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Render](https://img.shields.io/badge/Render-Cloud-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

---

# 📌 Présentation

Projet Data Engineering complet simulant une plateforme analytique e-commerce moderne.

Le projet couvre l’ensemble de la chaîne de traitement des données :

```text
API / CSV / Faker
        ↓
Python Ingestion
        ↓
PostgreSQL RAW
        ↓
SQL + dbt STAGING
        ↓
dbt MART
        ↓
Tests qualité
        ↓
Airflow orchestration
        ↓
Dashboard Streamlit
        ↓
CI/CD GitHub Actions
        ↓
Docker & Cloud Deployment
```

---

# 🎯 Objectifs du projet

Construire une plateforme Data Engineering complète permettant de :

- ingérer des données depuis plusieurs sources
- stocker les données dans PostgreSQL
- transformer les données avec dbt
- construire un mini Data Warehouse
- automatiser les pipelines avec Airflow
- mettre en place des tests qualité
- industrialiser le projet avec Docker & CI/CD
- déployer une application analytique cloud
- produire des dashboards métier interactifs

---

# 🏗️ Architecture Data Platform

```text
                    ┌────────────────────┐
                    │  APIs / CSV / Fake │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Python Ingestion   │
                    │ pandas / requests  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ PostgreSQL RAW     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ dbt STAGING        │
                    │ Cleaning & Models  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ dbt MART           │
                    │ Star Schema        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Streamlit BI       │
                    │ Analytics Dashboard│
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Cloud Deployment   │
                    │ Render + Streamlit │
                    └────────────────────┘
```

---

# 🧱 Stack Technique

## 🔹 Data Engineering

- Python
- PostgreSQL
- SQL avancé
- dbt
- Apache Airflow
- Docker
- SQLAlchemy
- psycopg2
- pandas
- Faker
- requests

## 🔹 Analytics & BI

- Streamlit
- Plotly
- Power BI / Looker Studio

## 🔹 DevOps & Cloud

- GitHub
- GitHub Actions
- Docker Hub
- Render PostgreSQL
- Streamlit Cloud

---

# 📂 Structure du Projet

```text
ProjetDataEngineer/
│
├── airflow/
│   ├── dags/
│   └── logs/
│
├── dashboards/
│   └── streamlit/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── mart/
│   │   └── sources.yml
│   │
│   ├── snapshots/
│   ├── tests/
│   └── dbt_project.yml
│
├── ingestion/
│   ├── api/
│   ├── csv/
│   ├── faker/
│   └── loaders/
│
├── sql/
│   ├── ddl/
│   ├── views/
│   ├── procedures/
│   ├── triggers/
│   └── indexes/
│
├── tests/
│   ├── data_quality/
│   ├── integration/
│   └── unit/
│
├── docker/
│
├── docs/
│
├── streamlit_dataeng.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 🗄️ Modélisation PostgreSQL

## 🔹 Schémas

```text
raw
staging
mart
audit
```

---

## 🔹 Tables RAW

```text
customers
products
orders
order_items
payments
fakestore_products
fakestore_users
fakestore_carts
```

---

## 🔹 Tables STAGING

```text
stg_customers
stg_orders
stg_products
stg_payments
stg_order_items
```

---

## 🔹 Tables MART

```text
fact_sales
fact_payments

dim_customers
dim_products
dim_date
```

---

# ⚙️ Fonctionnalités SQL Avancées

Le projet inclut des fonctionnalités SQL avancées utilisées en entreprise :

## 🔹 Vues & vues matérialisées

- v_sales_by_month
- v_customer_revenue
- v_top_products
- v_orders_summary

## 🔹 Index SQL

- indexes B-tree
- indexes composites
- indexes sur clés étrangères

## 🔹 Fonctions SQL

- procédures stockées
- fonctions PL/pgSQL
- triggers
- transactions

## 🔹 Optimisation SQL

- EXPLAIN ANALYZE
- VACUUM
- ANALYZE
- optimisation des requêtes analytiques

---

# 🔄 Ingestion des Données

Le pipeline d’ingestion récupère des données depuis :

- APIs e-commerce
- fichiers CSV
- données simulées Faker

## 🔹 Fonctionnalités

- validation des colonnes
- nettoyage des données
- logs ingestion
- gestion des erreurs
- batch loading PostgreSQL
- transactions SQL

---

# 🔥 dbt Transformation Layer

Le projet utilise dbt pour industrialiser les transformations.

## 🔹 Fonctionnalités dbt

- models staging
- models mart
- tests dbt
- documentation dbt
- snapshots
- sources
- materializations
- incremental models

---

# 🧪 Data Quality & Testing

Le projet implémente plusieurs niveaux de tests.

## 🔹 Tests dbt

- unique
- not null
- accepted values
- relationships

## 🔹 Tests SQL

- doublons
- cohérence montants
- commandes sans clients
- paiements négatifs
- dates invalides

## 🔹 Tests Python

- tests unitaires ingestion
- tests intégration pipeline
- validation DataFrames
- validation schémas

## 🔹 Monitoring Qualité

- logs pipeline
- data quality checks
- alertes erreurs
- suivi des exécutions

---

# ⏰ Apache Airflow

Le pipeline est orchestré avec Apache Airflow.

## 🔹 DAG principal

```text
extract_data
    ↓
validate_data
    ↓
load_raw_postgres
    ↓
run_dbt_models
    ↓
run_dbt_tests
    ↓
refresh_views
    ↓
export_metrics
```

## 🔹 Fonctionnalités

- scheduling automatique
- retry policies
- dépendances de tâches
- logs Airflow
- monitoring des jobs

---

# 📊 Dashboard Analytics — Streamlit

Application analytique interactive construite avec Streamlit.

## 🔹 Modules disponibles

### 🗂️ RAW

Exploration des données brutes :

- statistiques descriptives
- distributions
- qualité des données
- exploration interactive

### 🔄 STAGING

Analyse des données transformées :

- comparaison RAW vs STAGING
- nettoyage des données
- transformations dbt

### 📊 MART

Couche BI & KPIs :

- chiffre d’affaires
- panier moyen
- top produits
- clients
- tendances mensuelles
- analyses business

---

# ☁️ Cloud Deployment

## 🔹 Render PostgreSQL

Base PostgreSQL hébergée dans le cloud via Render.

Fonctionnalités :

- SSL sécurisé
- accès distant
- stockage persistant
- haute disponibilité

---

## 🔹 Streamlit Cloud

Dashboard déployé sur Streamlit Community Cloud.

### URL publique

```text
https://endtoenddiopabdoulaye.streamlit.app
```

---

# 🐳 Docker

Le projet est entièrement conteneurisé.

## 🔹 Containers

- PostgreSQL
- Airflow
- dbt
- Streamlit

## 🔹 Lancement

```bash
docker compose up -d
```

---

# 🔄 CI/CD — GitHub Actions

Pipeline CI/CD automatisé.

## 🔹 Vérifications automatiques

- installation dépendances
- validation Python
- tests SQL
- dbt test
- build Docker
- déploiement cloud

---

# 🔐 Sécurité

## 🔹 Gestion des secrets

- `.env`
- `st.secrets`
- GitHub Secrets
- variables Render

## 🔹 Sécurité PostgreSQL

- rôles SQL
- permissions par schéma
- accès lecture seule
- connexions SSL

---

# 📈 KPIs Métier

Le projet produit plusieurs indicateurs business :

- chiffre d’affaires
- panier moyen
- revenus mensuels
- top produits
- segmentation clients
- performance paiements
- qualité des données
- évolution des ventes

---

# 🚀 Lancer le Projet

## 1️⃣ Cloner le repository

```bash
git clone https://github.com/ABDOULAYEDIOP150/ProjetDataEngineer.git
cd ProjetDataEngineer
```

---

## 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configurer les variables d’environnement

Créer un fichier `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=password
```

---

## 4️⃣ Lancer PostgreSQL & Airflow

```bash
docker compose up -d
```

---

## 5️⃣ Lancer dbt

```bash
dbt run
dbt test
```

---

## 6️⃣ Lancer Streamlit

```bash
streamlit run streamlit_dataeng.py
```

---

# 📊 Captures & Dashboards

## 🔹 Dashboard RAW

- exploration données brutes
- distributions
- qualité des données

## 🔹 Dashboard STAGING

- données transformées
- comparaison pipelines
- monitoring qualité

## 🔹 Dashboard MART

- KPIs business
- analytics e-commerce
- visualisations interactives

---

# 📚 Compétences démontrées

## 🔹 Data Engineering

- ETL / ELT
- Data Warehouse
- SQL avancé
- dbt
- orchestration Airflow
- modélisation analytique

## 🔹 Cloud & DevOps

- Docker
- CI/CD
- Render
- Streamlit Cloud
- GitHub Actions

## 🔹 Data Analytics

- BI
- dashboards
- KPIs
- exploration de données

---

# 🎯 Résultat Final

Ce projet démontre la capacité à construire une plateforme Data Engineering complète :

✅ ingestion automatisée  
✅ Data Warehouse PostgreSQL  
✅ transformations dbt  
✅ orchestration Airflow  
✅ tests qualité  
✅ dashboard analytique  
✅ CI/CD automatisé  
✅ déploiement cloud  
✅ architecture scalable & maintenable  

---

# 👨‍💻 Auteur

## Abdoulaye Diop

### 🔗 GitHub

https://github.com/ABDOULAYEDIOP150

---

# ⭐ Objectif Portfolio

Projet conçu pour démontrer des compétences professionnelles en :

- Data Engineering
- Analytics Engineering
- SQL Engineering
- BI Engineering
- Cloud Data Platforms

---
