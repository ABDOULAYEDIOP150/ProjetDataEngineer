#!/bin/bash
set -e

echo "PORT=$PORT"

airflow db migrate

airflow users create \
  --username airflow \
  --password airflow \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

exec airflow webserver --port "${PORT:-10000}" --hostname 0.0.0.0
