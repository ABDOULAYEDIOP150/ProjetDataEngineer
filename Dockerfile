FROM apache/airflow:2.9.1-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall -y \
    apache-airflow-providers-google \
    google-cloud-secret-manager \
    google-cloud-compute \
    protobuf \
    proto-plus || true

COPY --chown=airflow:root . /opt/airflow/project

USER root

COPY start-airflow.sh /start-airflow.sh
RUN chmod +x /start-airflow.sh

USER airflow

WORKDIR /opt/airflow

ENTRYPOINT []
CMD ["/start-airflow.sh"]
