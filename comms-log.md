---
lab4_comms:
  awareness: "2026-10-25T15:31:39Z"
  detection: "2026-10-25T15:31:19Z"
  classification: "2026-10-25T15:32:39Z"
  nis2:
    early_warning_due: "2026-10-26T15:31:39Z"
    notification_due: "2026-10-28T15:31:39Z"
    notification_sent: "2026-10-27T09:00:00Z"
    final_report_due: "2026-11-27T09:00:00Z"
  ksc:
    early_warning_due: "2026-10-26T15:31:19Z"
    notification_due: "2026-10-28T15:31:19Z"
    notification_sent: "2026-10-27T09:00:00Z"
    final_report_due: "2026-11-27T09:00:00Z"
  dora:
    initial_due: "2026-10-25T19:32:39Z"
    initial_sent: "2026-10-25T15:45:00Z"
    intermediate_due: "2026-10-28T15:45:00Z"
    intermediate_sent: "2026-10-28T10:00:00Z"
    final_due: "2026-11-28T10:00:00Z"
  log:
    - at: "2026-10-25T15:45:00Z"
      to: "financial supervisor (exercise)"
      what: "DORA initial notification of the classified ICT incident"
    - at: "2026-10-26T09:00:00Z"
      to: "CSIRT (exercise)"
      what: "NIS2 and KSC early warnings with scope and observed mitigation"
    - at: "2026-10-27T09:00:00Z"
      to: "CSIRT (exercise)"
      what: "NIS2 and KSC incident notifications with confirmed timeline and impact"
    - at: "2026-10-28T10:00:00Z"
      to: "financial supervisor (exercise)"
      what: "DORA intermediate report with recovery and corrective actions"
---
<!-- ai-generated: 95% - Codex calculated the course's regulator clocks from the actual incident and a hypothetical report schedule. -->

# Communications log

## The three instants

Detection is 2026-10-25T15:31:19Z, the automated detecting alert's first firing timestamp. Awareness of a significant incident is 2026-10-25T15:31:39Z, when its P1 notification reached the on-call pager. The earlier monitoring checks showed individual errors; the page established a sustained checkout symptom warranting incident handling. Classification as major is 2026-10-25T15:32:39Z, the investigation measurement that quantified a 14.6-second checkout p99 and widespread catalog-dependent latency.

For this exercise we assume the shop and incident meet the applicability and significance conditions stated in the course. These are hypothetical report submissions; no notifications were actually sent. The choice of classification time reflects the confirmed impact, rather than treating every initial metric anomaly as a completed classification.

## Report schedule

| UTC submission | Recipient | Content |
|---|---|---|
| 2026-10-25T15:45:00Z | financial supervisor (exercise) | DORA initial notification of the classified ICT incident |
| 2026-10-26T09:00:00Z | CSIRT (exercise) | NIS2 and KSC early warnings with scope and observed mitigation |
| 2026-10-27T09:00:00Z | CSIRT (exercise) | NIS2 and KSC incident notifications with confirmed timeline and impact |
| 2026-10-28T10:00:00Z | financial supervisor (exercise) | DORA intermediate report with recovery and corrective actions |

NIS2 runs from awareness, while KSC runs from detection. Their early warnings are due 24 elapsed hours later and their incident notifications 72 hours later. The planned CSIRT notifications precede both deadlines; each final report is due one UTC calendar month after its own notification submission.

DORA's initial deadline is 2026-10-25T19:32:39Z: four hours after classification is earlier than awareness plus 24 hours. The planned initial submission at 2026-10-25T15:45:00Z is within that deadline. Its intermediate deadline is 72 hours after that initial submission, and its final deadline is one UTC calendar month after the intermediate submission.

The calculations use the course's I-30 arithmetic, including its instruction to ignore DORA weekend relief. Instants and month arithmetic remain in UTC; local clock changes do not alter elapsed-hour deadlines.
