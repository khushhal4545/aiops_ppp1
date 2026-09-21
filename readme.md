# AIOps Practical Assessment

## 1. Project Overview

This project demonstrates an end-to-end AIOps workflow for monitoring
operational data, detecting anomalies, generating events, and processing
those events to produce the final AIOps output.

The workflow is:

Operational Data → Anomaly Detection → Event Generation → Producer
→ Topic → Consumer → Final AIOps Output

---

## 2. Objective

The main objectives of this practical assessment are:

- Analyse the provided operational data.
- Identify relevant metrics and log information.
- Distinguish normal and abnormal behaviour.
- Detect anomalies using the provided anomaly detection component.
- Generate events from detected anomalies.
- Verify the producer and consumer workflow.
- Troubleshoot and correct issues in the provided system.
- Validate the complete end-to-end AIOps workflow.

---

## 3. Repository Components

The main components identified in the repository are:

| Component | Purpose |
|---|---|
| Operational Data | Provides the input data for the AIOps workflow. |
| Metrics | Contains operational measurements used for analysis. |
| Logs | Provides information about system behaviour and events. |
| Anomaly Detection | Identifies unusual or abnormal behaviour. |
| Event Generation | Creates an event when an anomaly is detected. |
| Producer | Sends the generated event to the event topic. |
| Topic | Acts as the communication channel for events. |
| Consumer | Receives and processes events from the topic. |
| AIOps Processing | Performs the final processing and produces the output. |

---

## 4. Operational Data Analysis

The provided operational data was analysed to understand normal
and abnormal system behaviour.

The relevant operational information includes metrics and logs
associated with system activity.

Normal values represent expected system behaviour, while unusual
values or patterns can indicate an anomaly.

---

## 5. Anomaly Detection

The anomaly detection component analyses the operational data and
identifies unusual behaviour.

When an abnormal condition is detected, an anomaly is generated
for further processing.

The detected anomaly is then used to generate an operational event.

---

## 6. Event Generation

After anomaly detection, the system generates an event containing
information about the detected abnormal behaviour.

The event is then passed to the producer component.

---

## 7. Producer → Topic → Consumer

The event-processing flow is:

Producer → Topic → Consumer

The producer sends the generated event to the topic.

The topic acts as the communication channel between the producer
and consumer.

The consumer receives the event and passes it to the next stage
for AIOps processing.

---

## 8. Troubleshooting

During validation, the provided workflow was examined to identify
any issues in the system.

The affected component was identified by tracing the event flow
from anomaly detection through event generation, producer, topic,
consumer, and final processing.

### Issue Identified

[WRITE THE ACTUAL ISSUE FOUND DURING THE PRACTICAL]

### Root Cause

[WRITE THE ACTUAL ROOT CAUSE]

### Correction

[WRITE WHAT YOU CHANGED TO FIX THE ISSUE]

---

## 9. Validation

The provided validation/tests were executed after making the
required correction.

The workflow was tested again to verify that the correction
worked correctly.

### Validation Result

[WRITE ACTUAL TEST/WORKFLOW RESULT HERE]

---

## 10. End-to-End Workflow Result

The complete workflow was executed successfully:

Operational Data
↓
Anomaly Detection
↓
Event Generation
↓
Producer
↓
Topic
↓
Consumer
↓
Final AIOps Processing

The final output was verified after the event passed through
the complete workflow.

---

## 11. Reproduction Steps

1. Open the repository in GitHub Codespaces.
2. Set up the required Python environment.
3. Install the required dependencies.
4. Run the provided workflow.
5. Analyse the operational data and logs.
6. Observe the anomaly detection result.
7. Verify event generation.
8. Verify producer and consumer processing.
9. Identify and correct the reported issue.
10. Run the validation/tests again.
11. Execute the complete end-to-end workflow.
12. Verify the final AIOps output.

---

## 12. Evidence

The following evidence was collected during the practical:

- Repository/project structure
- Operational data analysis
- Anomaly detection output
- Event generation
- Producer output
- Consumer output
- Final AIOps output
- Validation/test results
- Git commit and push
- Pull Request

---

## 13. Conclusion

The AIOps workflow was analysed and validated from operational
data to final AIOps output.

The identified issue was investigated, the required correction
was applied, and the complete workflow was executed again to
verify the result.
