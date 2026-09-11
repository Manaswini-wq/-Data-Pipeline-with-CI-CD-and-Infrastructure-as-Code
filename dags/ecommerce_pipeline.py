"""Airflow DAG: ingest → dbt → quality checks → alert."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["production", "ecommerce"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=lambda: __import__("src.ingest", fromlist=["run"]).run(),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /app/dbt_project && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /app/dbt_project && dbt test --profiles-dir .",
    )

    quality_check = PythonOperator(
        task_id="quality_checks",
        python_callable=lambda: __import__("data_quality.expectations", fromlist=["run_quality_checks"]).run_quality_checks(),
    )

    alert = PythonOperator(
        task_id="slack_alert",
        python_callable=lambda: __import__("data_quality.alert", fromlist=["send_slack_alert"]).send_slack_alert(*__import__("data_quality.expectations", fromlist=["run_quality_checks"]).run_quality_checks()),
        trigger_rule="all_done",
    )

    ingest >> dbt_run >> dbt_test >> quality_check >> alert
