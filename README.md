# 📊 Data Engineering Project — E-commerce Pipeline

---

## 🎯 Objectif du projet

Ce projet a pour objectif de construire une **pipeline data complète de bout en bout** :

```text
Sources (CSV / API) → Python → PostgreSQL → SQL → (à venir : dbt / Airflow / BI)
```

Le projet est structuré en plusieurs étapes :

* Étape 1 : Ingestion des données
* Étape 2 : Modélisation PostgreSQL + staging
* Étapes suivantes : Data Warehouse, dbt, orchestration, BI

---

# 🧱 Architecture du projet

```text
project/
│
├── data/
│   ├── raw/
│   │   ├── simulated/
│   │   ├── api/
│   │   └── olist/
│   └── processed/
│
├── ingestion/
│   ├── generate_fake_data.py
│   ├── extract_api.py
│   ├── load_sources.py
│   └── utils.py
│
├── sql/
│   ├── 01_create_schemas.sql
│   ├── 02_create_raw_constraints.sql
│   ├── 03_checks_queries.sql
│   ├── 04_create_staging_tables.sql
│   ├── 05_insert_staging_tables.sql
│   ├── 06_staging_checks.sql
│   ├── 07_raw_analysis.sql
│   ├── 08_staging_analysis.sql
│   └── 09_create_views.sql
│
├── notebooks/
├── .env
├── requirements.txt
├── README.md
└── docker-compose.yml
```

---

# 📥 Étape 1 — Ingestion des données

## Sources utilisées

### 1. Données simulées (Faker)

* customers
* products
* orders
* order_items
* payments

Stockées dans :

```text
data/raw/simulated/
```

---

### 2. Données API (FakeStoreAPI)

* produits
* utilisateurs
* paniers

Stockées dans :

```text
data/raw/api/
```

---

## ⚙️ Pipeline d’ingestion

### Génération des données

```bash
python ingestion/generate_fake_data.py
```

---

### Extraction API

```bash
python ingestion/extract_api.py
```

---

### Chargement PostgreSQL

```bash
python ingestion/load_sources.py
```

---

## 🗄️ Résultat PostgreSQL

```text
Database : ecommerce_dw
Schema   : raw
```

Tables :

* raw.customers
* raw.products
* raw.orders
* raw.order_items
* raw.payments
* raw.fakestore_products
* raw.fakestore_users
* raw.fakestore_carts

---

# 🏗️ Étape 2 — Modélisation PostgreSQL

Objectif :

* structurer les données
* garantir la qualité
* préparer un Data Warehouse

---

## 🔹 2.1 Création des schemas

📄 `sql/01_create_schemas.sql`

```sql
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;
```

---

## 🔹 2.2 Ajout des contraintes (raw)

📄 `sql/02_create_raw_constraints.sql`

* Clés primaires
* Clés étrangères
* Contraintes CHECK

Exemples :

```sql
ALTER TABLE raw.orders
ADD PRIMARY KEY (order_id);

ALTER TABLE raw.orders
ADD CONSTRAINT fk_orders_customers
FOREIGN KEY (customer_id)
REFERENCES raw.customers(customer_id);
```

---

## 🔹 2.3 Vérification des données

📄 `sql/03_checks_queries.sql`

```sql
SELECT COUNT(*) FROM raw.customers;
SELECT COUNT(*) FROM raw.orders;
```

---

## 🔹 2.4 Création des tables staging

📄 `sql/04_create_staging_tables.sql`

Objectif :

* typage propre
* contraintes métier
* préparation analytique

---

## 🔹 2.5 Chargement vers staging

📄 `sql/05_insert_staging_tables.sql`

Transformation :

* cast des types
* nettoyage des données
* suppression des doublons

---

## 🔹 2.6 Vérification staging

📄 `sql/06_staging_checks.sql`

```sql
SELECT COUNT(*) FROM staging.orders;
```

---

## 🔹 2.7 Analyse sur données brutes (raw)

📄 `sql/07_raw_analysis.sql`

```sql
SELECT
    o.order_id,
    c.full_name,
    p.amount
FROM raw.orders o
JOIN raw.customers c
    ON o.customer_id = c.customer_id
LEFT JOIN raw.payments p
    ON o.order_id = p.order_id
LIMIT 10;
```

Objectif :

* valider ingestion
* détecter anomalies

---

## 🔹 2.8 Analyse sur données propres (staging)

📄 `sql/08_staging_analysis.sql`

```sql
SELECT
    o.order_id,
    c.full_name,
    p.amount
FROM staging.orders o
JOIN staging.customers c
    ON o.customer_id = c.customer_id
LEFT JOIN staging.payments p
    ON o.order_id = p.order_id
LIMIT 10;
```

Objectif :

* analyse fiable
* base pour reporting

---

## 🔹 2.9 Création de vues (mart)

📄 `sql/09_create_views.sql`

```sql
CREATE OR REPLACE VIEW mart.v_orders_summary AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.full_name,
    p.amount
FROM staging.orders o
JOIN staging.customers c
    ON o.customer_id = c.customer_id
LEFT JOIN staging.payments p
    ON o.order_id = p.order_id;
```

---

## 🧠 Concepts couverts

* Schémas PostgreSQL (raw / staging / mart)
* Clés primaires et étrangères
* Contraintes de qualité
* Nettoyage des données
* Jointures SQL
* Création de vues
* Architecture data engineering

---

## 🎯 Résultat de l’étape 2

```text
raw     → données brutes
staging → données nettoyées
mart    → vues analytiques
```

---

# 🚀 Prochaines étapes

* Création du Data Warehouse (star schema)
* Tables fact / dimension
* dbt (transformations)
* Airflow (orchestration)
* Dashboard BI

---

# 💬 Résumé global

> Pipeline data multi-sources avec ingestion Python, structuration PostgreSQL, nettoyage staging et premières vues analytiques (mart), suivant les bonnes pratiques data engineering.

---
