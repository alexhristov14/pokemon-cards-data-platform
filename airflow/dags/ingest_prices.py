from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "ingest_pokemon_prices",
    start_date=datetime(2025, 1, 7),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    ingest = BashOperator(
        task_id="run_ingestion",
        bash_command="python3 /opt/airflow/ingestion/main.py",
    )
