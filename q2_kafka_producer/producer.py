"""
Question 2 — Kafka Topic and Producer
--------------------------------------
Configures a Kafka producer and sends server metric messages to the
'server_metrics' topic.

Prerequisites (see README.md at the project root):
    1. A Kafka broker running on localhost:9092 (docker-compose.yml provided).
    2. Topic 'server_metrics' created (script below can auto-create it too).
    3. pip install kafka-python

Run:
    python producer.py
"""

import json
import random
import time

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

BOOTSTRAP_SERVERS = ["localhost:9092"]
TOPIC_NAME = "server_metrics"
NUM_MESSAGES = 10


def ensure_topic_exists(bootstrap_servers, topic_name, num_partitions=1, replication_factor=1):
    """Create the topic if it does not already exist."""
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id="aiops-admin")
    try:
        admin.create_topics(
            [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        )
        print(f"Topic '{topic_name}' created.")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists.")
    finally:
        admin.close()


def build_producer(bootstrap_servers):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        acks="all",
    )


def generate_metric(server_id: str) -> dict:
    return {
        "server_id": server_id,
        "cpu_usage": random.randint(30, 98),
        "memory_usage": random.randint(30, 95),
    }


def main():
    ensure_topic_exists(BOOTSTRAP_SERVERS, TOPIC_NAME)
    producer = build_producer(BOOTSTRAP_SERVERS)

    print(f"\nSending {NUM_MESSAGES} messages to topic '{TOPIC_NAME}'...\n")

    for i in range(NUM_MESSAGES):
        server_id = f"server{(i % 5) + 1:02d}"
        message = generate_metric(server_id)

        future = producer.send(TOPIC_NAME, key=server_id, value=message)
        record_metadata = future.get(timeout=10)  # block until acked -> verifies publish

        print(
            f"Sent -> {json.dumps(message)} "
            f"[partition={record_metadata.partition}, offset={record_metadata.offset}]"
        )
        time.sleep(0.3)

    producer.flush()
    producer.close()
    print("\nAll messages published and acknowledged by the broker.")


if __name__ == "__main__":
    main()
