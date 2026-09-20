"""
Question 4 — Build an AIOps Workflow using Airflow
-----------------------------------------------------
A basic AIOps pipeline DAG:

    collect_metrics >> process_metrics >> detect_anomaly >> generate_report

Install (in your Airflow environment):
    pip install apache-airflow

Deploy:
    Copy this file into your Airflow DAGS_FOLDER (e.g. ~/airflow/dags/)
    then run:
        airflow db init          # first time only
        airflow webserver -p 8080
        airflow scheduler
    Trigger the DAG 'aiops_workflow_dag' from the Airflow UI or CLI:
        airflow dags trigger aiops_workflow_dag
"""

from datetime import datetime, timedelta
import random

from airflow import DAG
from airflow.operators.python import PythonOperator

CPU_THRESHOLD = 80

default_args = {
    "owner": "aiops-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


# --------------------------------------------------------------------------
# Task callables
# --------------------------------------------------------------------------
def collect_metrics(**context):
    """Task 1: generate/sample server metrics and push them via XCom."""
    metrics = {
        "cpu": random.randint(50, 99),
        "memory": random.randint(40, 90),
        "response_time_ms": random.randint(150, 600),
    }
    print(f"Collected metrics -> CPU = {metrics['cpu']}, "
          f"Memory = {metrics['memory']}, "
          f"Response Time = {metrics['response_time_ms']}ms")

    context["ti"].xcom_push(key="metrics", value=metrics)


def process_metrics(**context):
    """Task 2: process (here: validate/normalize) the collected metrics."""
    metrics = context["ti"].xcom_pull(key="metrics", task_ids="collect_metrics")
    print("Processing metrics...")
    print(f"CPU: {metrics['cpu']}%")
    print(f"Memory: {metrics['memory']}%")
    print(f"Response Time: {metrics['response_time_ms']}ms")
    print("Metrics processed successfully")

    context["ti"].xcom_push(key="metrics", value=metrics)


def detect_anomaly(**context):
    """Task 3: check CPU threshold and flag anomalies."""
    metrics = context["ti"].xcom_pull(key="metrics", task_ids="process_metrics")
    is_anomaly = metrics["cpu"] > CPU_THRESHOLD

    if is_anomaly:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")

    context["ti"].xcom_push(key="anomaly_detected", value=is_anomaly)


def generate_report(**context):
    """Task 4: print the final AIOps report."""
    anomaly_detected = context["ti"].xcom_pull(key="anomaly_detected", task_ids="detect_anomaly")

    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print(f"Result: {'Anomaly Found' if anomaly_detected else 'System Normal'}")
    print("========================")


# --------------------------------------------------------------------------
# DAG definition
# --------------------------------------------------------------------------
with DAG(
    dag_id="aiops_workflow_dag",
    description="Basic AIOps lifecycle: collect -> process -> detect -> report",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["aiops", "demo"],
) as dag:

    t1_collect_metrics = PythonOperator(
        task_id="collect_metrics",
        python_callable=collect_metrics,
    )

    t2_process_metrics = PythonOperator(
        task_id="process_metrics",
        python_callable=process_metrics,
    )

    t3_detect_anomaly = PythonOperator(
        task_id="detect_anomaly",
        python_callable=detect_anomaly,
    )

    t4_generate_report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report,
    )

    t1_collect_metrics >> t2_process_metrics >> t3_detect_anomaly >> t4_generate_report
