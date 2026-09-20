"""
Question 1 — AIOps Log Anomaly Detection
------------------------------------------
Generates/reads a sample server-metrics log dataset (timestamp, CPU usage,
memory usage, response time), computes basic statistics, flags anomalous
records using a threshold-based approach, prints them in a report, and
plots the metrics with anomalies highlighted.

Run:
    python anomaly_detection.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")  # safe for headless / server environments
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "server_logs.csv")
PLOT_FILE = os.path.join(os.path.dirname(__file__), "..", "output", "anomaly_plot.png")

CPU_THRESHOLD = 90          # % - above this is anomalous
MEMORY_THRESHOLD = 90       # %
RESPONSE_TIME_THRESHOLD = 800  # ms

RECORD_COUNT = 20
random.seed(42)  # reproducible sample data


# --------------------------------------------------------------------------
# Step 1: Create or read the sample dataset
# --------------------------------------------------------------------------
def generate_sample_dataset(path: str, n: int = RECORD_COUNT):
    """Generate a synthetic server log CSV with a few injected anomalies."""
    start_time = datetime.strptime("10:00", "%H:%M")
    rows = []

    # indices where we deliberately inject anomalies (spikes)
    anomaly_indices = {5, 12, 18}

    for i in range(n):
        ts = (start_time + timedelta(minutes=i)).strftime("%H:%M")

        if i in anomaly_indices:
            cpu = random.randint(91, 98)
            memory = random.randint(85, 96)
            response_time = random.randint(750, 950)
        else:
            cpu = random.randint(30, 75)
            memory = random.randint(40, 80)
            response_time = random.randint(150, 400)

        rows.append(
            {
                "timestamp": ts,
                "cpu_usage": cpu,
                "memory_usage": memory,
                "response_time": response_time,
            }
        )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "cpu_usage", "memory_usage", "response_time"]
        )
        writer.writeheader()
        writer.writerows(rows)

    return rows


def read_dataset(path: str):
    if not os.path.exists(path):
        return generate_sample_dataset(path)
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                {
                    "timestamp": r["timestamp"],
                    "cpu_usage": int(r["cpu_usage"]),
                    "memory_usage": int(r["memory_usage"]),
                    "response_time": int(r["response_time"]),
                }
            )
    return rows


# --------------------------------------------------------------------------
# Step 2: Basic statistics
# --------------------------------------------------------------------------
def compute_statistics(records):
    def stats_for(key):
        values = [r[key] for r in records]
        return {
            "min": min(values),
            "max": max(values),
            "avg": round(sum(values) / len(values), 2),
        }

    return {
        "cpu_usage": stats_for("cpu_usage"),
        "memory_usage": stats_for("memory_usage"),
        "response_time": stats_for("response_time"),
    }


# --------------------------------------------------------------------------
# Step 3: Threshold-based anomaly detection
# --------------------------------------------------------------------------
def detect_anomalies(records):
    for r in records:
        is_anomaly = (
            r["cpu_usage"] > CPU_THRESHOLD
            or r["memory_usage"] > MEMORY_THRESHOLD
            or r["response_time"] > RESPONSE_TIME_THRESHOLD
        )
        r["status"] = "ANOMALY" if is_anomaly else "NORMAL"
    return records


# --------------------------------------------------------------------------
# Step 4: Print report
# --------------------------------------------------------------------------
def print_report(records, statistics):
    anomalies = [r for r in records if r["status"] == "ANOMALY"]

    print("=" * 50)
    print("AIOPS LOG ANOMALY DETECTION REPORT")
    print("=" * 50)
    print(f"Total records: {len(records)}")
    print(f"Anomalies detected: {len(anomalies)}\n")

    print("Basic Statistics")
    print("-" * 50)
    for metric, s in statistics.items():
        print(f"{metric:15s} -> min: {s['min']:>4}  max: {s['max']:>4}  avg: {s['avg']:>6}")

    print("\nAnomalous Records")
    print("-" * 50)
    print(f"{'Timestamp':<10}{'CPU':<8}{'Memory':<10}{'Resp(ms)':<10}{'Status'}")
    for r in anomalies:
        print(
            f"{r['timestamp']:<10}{str(r['cpu_usage'])+'%':<8}"
            f"{str(r['memory_usage'])+'%':<10}{r['response_time']:<10}{r['status']}"
        )
    print("=" * 50)


# --------------------------------------------------------------------------
# Step 5: Plot metrics + anomalies
# --------------------------------------------------------------------------
def plot_metrics(records, save_path=PLOT_FILE):
    timestamps = [r["timestamp"] for r in records]
    cpu = [r["cpu_usage"] for r in records]
    memory = [r["memory_usage"] for r in records]
    response_time = [r["response_time"] for r in records]
    anomaly_idx = [i for i, r in enumerate(records) if r["status"] == "ANOMALY"]

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

    metric_data = [
        ("CPU Usage (%)", cpu, CPU_THRESHOLD, axes[0]),
        ("Memory Usage (%)", memory, MEMORY_THRESHOLD, axes[1]),
        ("Response Time (ms)", response_time, RESPONSE_TIME_THRESHOLD, axes[2]),
    ]

    for title, values, threshold, ax in metric_data:
        ax.plot(timestamps, values, marker="o", color="tab:blue", label=title)
        ax.axhline(threshold, color="red", linestyle="--", linewidth=1, label="Threshold")
        ax.scatter(
            [timestamps[i] for i in anomaly_idx],
            [values[i] for i in anomaly_idx],
            color="red",
            zorder=5,
            s=90,
            label="Anomaly",
        )
        ax.set_ylabel(title)
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel("Timestamp")
    plt.xticks(rotation=45)
    fig.suptitle("Server Metrics with Detected Anomalies", fontsize=14)
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    print(f"\nPlot saved to: {save_path}")
    # plt.show()  # uncomment when running locally with a display


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    records = read_dataset(DATA_FILE)
    statistics = compute_statistics(records)
    records = detect_anomalies(records)
    print_report(records, statistics)
    plot_metrics(records)


if __name__ == "__main__":
    main()
