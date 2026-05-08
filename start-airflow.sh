#!/bin/bash
set -e

echo "Starting Airflow on Render..."
echo "PORT=${PORT:-10000}"

airflow db migrate

airflow users create \
  --username "${AIRFLOW_ADMIN_USERNAME:-airflow}" \
  --password "${AIRFLOW_ADMIN_PASSWORD:-airflow}" \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

exec airflow webserver --port "${PORT:-10000}" --hostname 0.0.0.0
