# 📊 Data Engineering Project — E-commerce Pipeline

## 🎯 Objectif du projet

Ce projet a pour objectif de construire une **pipeline data complète** de bout en bout :

```
Sources (CSV / API) → Python → PostgreSQL → (à venir : SQL / dbt / Airflow / BI)
```

Dans cette première étape, je me concentre sur **l’ingestion des données**.

---

## 🧱 Architecture (étape actuelle)

```
data/
  raw/
    simulated/   → données générées avec Faker
    api/         → données récupérées via API

ingestion/
  generate_fake_data.py
  extract_api.py
  load_sources.py
  utils.py
```

---

## 📥 Sources de données

### 1. Données simulées (CSV)

Des données e-commerce ont été générées avec Python et Faker :

* customers
* products
* orders
* order_items
* payments

Objectif :

* simuler un environnement réel
* contrôler la qualité et la structure des données

---

### 2. Données API

Données récupérées via une API externe (FakeStoreAPI) :

* produits
* utilisateurs
* paniers

Objectif :

* apprendre à consommer une API REST
* gérer des données JSON

---

## ⚙️ Pipeline d’ingestion

### Étape 1 — Génération des données

Script :

```
python ingestion/generate_fake_data.py
```

➡️ Génère des fichiers CSV dans :

```
data/raw/simulated/
```

---

### Étape 2 — Extraction API

Script :

```
python ingestion/extract_api.py
```

➡️ Récupère les données API et les stocke en CSV dans :

```
data/raw/api/
```

---

### Étape 3 — Chargement PostgreSQL

Script :

```
python ingestion/load_sources.py
```

➡️ Charge toutes les données dans PostgreSQL

---

## 🗄️ Stockage PostgreSQL

Base de données :

```
ecommerce_dw
```

Schema utilisé :

```
raw
```

Tables créées automatiquement :

* raw.customers
* raw.products
* raw.orders
* raw.order_items
* raw.payments
* raw.fakestore_products
* raw.fakestore_users
* raw.fakestore_carts

---

## 🔌 Connexion PostgreSQL

Connexion gérée via SQLAlchemy avec variables d’environnement :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=******
```

---

## 🧪 Vérification

Exemple de requête SQL :

```sql
SELECT * FROM raw.customers LIMIT 10;
```

---

## 🧠 Compétences démontrées

* Génération de données avec Faker
* Consommation d’API REST
* Manipulation de données avec pandas
* Chargement de données dans PostgreSQL
* Gestion de configuration (.env)
* Organisation d’un projet data engineering

---

## 🚀 Prochaines étapes

* Modélisation SQL (staging / marts)
* Création d’un Data Warehouse (schema en étoile)
* Transformation avec dbt
* Orchestration avec Airflow
* Dashboard (Power BI / Looker)

---

## 💬 Résumé

> Mise en place d’une ingestion multi-sources (CSV + API) avec Python, et stockage des données brutes dans PostgreSQL (schema raw) pour préparer les transformations analytiques.
