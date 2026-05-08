FROM apache/airflow:2.9.1-python3.11

USER root

# Installer les dépendances système si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir dbt-postgres

# Copier le projet
COPY --chown=airflow:root . /opt/airflow/project

WORKDIR /opt/airflow
