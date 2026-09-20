"""
Question 5 — Integrated AIOps Challenge
------------------------------------------
Extends the Q3 Kafka consumer into a simple AIOps monitoring system:
receives server metrics, checks CPU usage, flags anomalies, prints alerts,
and keeps a running count of anomalies detected during the session.

Prerequisites:
    1. Kafka broker running on localhost:9092.
    2. pip install kafka-python
    3. Producer (Q2) sending messages to 'server_metrics'.

Run:
    python aiops_monitor.py
Stop with Ctrl+C - a summary is printed on exit.
"""

import json

from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ["localhost:9092"]
TOPIC_NAME = "server_metrics"
CPU_ALERT_THRESHOLD = 80


class AIOpsMonitor:
    """Tracks messages processed and anomalies detected."""

    def __init__(self, cpu_threshold: int = CPU_ALERT_THRESHOLD):
        self.cpu_threshold = cpu_threshold
        self.total_messages = 0
        self.anomaly_count = 0

    def process(self, message: dict):
        server_id = message.get("server_id", "unknown")
        cpu = message.get("cpu_usage", 0)

        self.total_messages += 1
        is_anomaly = cpu > self.cpu_threshold

        print(f"Message received: {server_id} | CPU: {cpu}%")
        if is_anomaly:
            self.anomaly_count += 1
            print("ALERT: High CPU detected")
        else:
            print("Normal")
        print()

        return is_anomaly

    def summary(self):
        print("=" * 40)
        print(f"Total messages processed: {self.total_messages}")
        print(f"Total anomalies detected: {self.anomaly_count}")
        print("=" * 40)


def build_consumer(bootstrap_servers, topic_name):
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="aiops-integrated-monitor-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
    )


def main():
    consumer = build_consumer(BOOTSTRAP_SERVERS, TOPIC_NAME)
    monitor = AIOpsMonitor(cpu_threshold=CPU_ALERT_THRESHOLD)

    print(f"AIOps monitor subscribed to '{TOPIC_NAME}'. Waiting for messages... (Ctrl+C to stop)\n")

    try:
        for record in consumer:
            monitor.process(record.value)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        consumer.close()
        monitor.summary()


if __name__ == "__main__":
    main()
