from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = "/opt/airflow/project/ecommerce_dbt"


default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ecommerce_data_pipeline",
    description="Pipeline e-commerce : ingestion + dbt + tests",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",  # 🔥 exécution tous les jours
    catchup=False,
    default_args=default_args,
    tags=["ecommerce", "python", "postgresql", "dbt"],
) as dag:

    extract_api = BashOperator(
        task_id="extract_api",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        echo "📥 Extraction API..." &&
        python ingestion/extract_api.py
        """,
    )

    load_csv_to_postgres = BashOperator(
        task_id="load_csv_to_postgres",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        echo "📦 Chargement CSV vers PostgreSQL..." &&
        python ingestion/load_csv_to_postgres.py
        """,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {DBT_DIR} &&
        echo "⚙️ dbt run..." &&
        dbt run --profiles-dir /opt/airflow/.dbt
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_DIR} &&
        echo "🧪 dbt test..." &&
        dbt test --profiles-dir /opt/airflow/.dbt
        """,
    )

    # 🔗 orchestration
    extract_api >> load_csv_to_postgres >> dbt_run >> dbt_test