"""
Question 3 — Python Kafka Consumer
-------------------------------------
Connects to the Kafka broker, subscribes to 'server_metrics', continuously
receives messages, displays them, and raises an alert when CPU usage > 80%.

Prerequisites:
    1. Kafka broker running on localhost:9092.
    2. pip install kafka-python
    3. Producer (Q2) should be sending messages to 'server_metrics'.

Run:
    python consumer.py
Stop with Ctrl+C.
"""

import json

from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ["localhost:9092"]
TOPIC_NAME = "server_metrics"
CPU_ALERT_THRESHOLD = 80


def build_consumer(bootstrap_servers, topic_name):
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",   # read from the start if no committed offset
        enable_auto_commit=True,
        group_id="aiops-monitor-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
    )


def handle_message(message: dict):
    server_id = message.get("server_id", "unknown")
    cpu = message.get("cpu_usage", 0)
    memory = message.get("memory_usage", 0)

    print("Received:")
    print(f"Server: {server_id}")
    print(f"CPU: {cpu}%")
    print(f"Memory: {memory}%")

    if cpu > CPU_ALERT_THRESHOLD:
        print(f"\nALERT: High CPU detected on {server_id}\n")
    else:
        print()


def main():
    consumer = build_consumer(BOOTSTRAP_SERVERS, TOPIC_NAME)
    print(f"Subscribed to '{TOPIC_NAME}'. Waiting for messages... (Ctrl+C to stop)\n")

    try:
        for record in consumer:
            handle_message(record.value)
    except KeyboardInterrupt:
        print("\nConsumer stopped by user.")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
