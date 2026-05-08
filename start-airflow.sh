#!/bin/bash
set -e

airflow db migrate

airflow users create \
  --username airflow \
  --password airflow \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

airflow webserver --port ${PORT:-8080} --hostname 0.0.0.0
