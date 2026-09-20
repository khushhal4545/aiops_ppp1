# AIOps Practical Exercises

Five self-contained exercises covering log-based anomaly detection, Kafka
producers/consumers, and an Airflow AIOps pipeline.

```
aiops-project/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .gitignore
├── data/                          # generated sample data (Q1)
├── output/                        # generated plots (Q1)
├── q1_log_anomaly_detection/
│   └── anomaly_detection.py
├── q2_kafka_producer/
│   └── producer.py
├── q3_kafka_consumer/
│   └── consumer.py
├── q4_airflow_dag/
│   └── aiops_dag.py
└── q5_integrated_aiops/
    └── aiops_monitor.py
```

## 0. Open in VS Code

```bash
code aiops-project
```

Recommended: create a virtual environment so VS Code's Python interpreter
picks up all dependencies cleanly.

```bash
cd aiops-project
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

In VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter" → choose
`.venv`.

---

## Q1 — Log Anomaly Detection (no external services needed)

Runs standalone — generates sample data, computes stats, flags anomalies,
prints a report, and saves a plot.

```bash
python q1_log_anomaly_detection/anomaly_detection.py
```

Output: console report + `output/anomaly_plot.png`.

---

## Q2 & Q3 & Q5 — Kafka

### Start Kafka locally with Docker

```bash
docker-compose up -d
```

This starts Zookeeper + a single-broker Kafka cluster on
`localhost:9092`.

### Create the topic (optional — the producer auto-creates it)

```bash
docker exec -it aiops-kafka kafka-topics \
  --create --topic server_metrics \
  --bootstrap-server localhost:9092 \
  --partitions 1 --replication-factor 1
```

### Q2 — Run the producer (sends 10 messages)

```bash
python q2_kafka_producer/producer.py
```

### Verify messages landed in the topic (optional sanity check)

```bash
docker exec -it aiops-kafka kafka-console-consumer \
  --topic server_metrics \
  --from-beginning \
  --bootstrap-server localhost:9092
```

### Q3 — Run the basic consumer

```bash
python q3_kafka_consumer/consumer.py
```

Prints each message and raises `ALERT: High CPU detected on <server>` when
CPU > 80%.

### Q5 — Run the integrated AIOps monitor

```bash
python q5_integrated_aiops/aiops_monitor.py
```

Same as Q3, plus a running anomaly counter and a summary printed when you
stop it with `Ctrl+C`.

> Tip: run the producer and a consumer in two separate terminals to see
> messages flow through in real time.

### Stop Kafka

```bash
docker-compose down
```

---

## Q4 — Airflow DAG

```bash
pip install apache-airflow
export AIRFLOW_HOME=~/airflow
airflow db init                       # first time only
cp q4_airflow_dag/aiops_dag.py $AIRFLOW_HOME/dags/

airflow webserver -p 8080 &
airflow scheduler &
```

Open http://localhost:8080, enable `aiops_workflow_dag`, and trigger it —
or from the CLI:

```bash
airflow dags trigger aiops_workflow_dag
airflow tasks list aiops_workflow_dag
```

Task order: `collect_metrics >> process_metrics >> detect_anomaly >> generate_report`

---

## Pushing this project to GitHub

From inside the `aiops-project` folder:

```bash
git init
git add .
git commit -m "Initial commit: AIOps exercises (log anomaly detection, Kafka, Airflow)"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Replace `<your-username>/<your-repo-name>` with your actual GitHub repo
(create an empty repo on GitHub first, with no README/license so there's
no merge conflict on first push).
