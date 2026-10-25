# ai-generated: 95% - Codex computed the fictional course reporting deadlines from the actual incident timeline.
import calendar
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
clocks = json.loads((root / "incident/recomputed-output.txt").read_text(encoding="utf-8"))
state = json.loads((root / "incident/live-state.json").read_text(encoding="utf-8"))
parse = lambda value: datetime.fromisoformat(value.replace("Z", "+00:00"))
fmt = lambda value: value.isoformat(timespec="seconds").replace("+00:00", "Z")
awareness = parse(state["page"]["received_at"]).replace(microsecond=0)
detection = parse(clocks["detection"])
classification = parse("2026-10-25T15:32:39Z")
notification = (awareness + timedelta(days=2)).replace(hour=9, minute=0, second=0)
initial = awareness.replace(hour=15, minute=45, second=0)
intermediate = (awareness + timedelta(days=3)).replace(hour=10, minute=0, second=0)
early_sent = (awareness + timedelta(days=1)).replace(hour=9, minute=0, second=0)

def month_after(value):
    month = value.month % 12 + 1
    year = value.year + (value.month == 12)
    return value.replace(year=year, month=month, day=min(value.day, calendar.monthrange(year, month)[1]))

initial_due = classification + timedelta(hours=4)
if classification <= awareness + timedelta(hours=24):
    initial_due = min(initial_due, awareness + timedelta(hours=24))
data = {
    "awareness": awareness, "detection": detection, "classification": classification,
    "nis2": {"early_warning_due": awareness+timedelta(hours=24), "notification_due": awareness+timedelta(hours=72), "notification_sent": notification, "final_report_due": month_after(notification)},
    "ksc": {"early_warning_due": detection+timedelta(hours=24), "notification_due": detection+timedelta(hours=72), "notification_sent": notification, "final_report_due": month_after(notification)},
    "dora": {"initial_due": initial_due, "initial_sent": initial, "intermediate_due": initial+timedelta(hours=72), "intermediate_sent": intermediate, "final_due": month_after(intermediate)},
}
entries = [(initial, "financial supervisor (exercise)", "DORA initial notification of the classified ICT incident"),
           (early_sent, "CSIRT (exercise)", "NIS2 and KSC early warnings with scope and observed mitigation"),
           (notification, "CSIRT (exercise)", "NIS2 and KSC incident notifications with confirmed timeline and impact"),
           (intermediate, "financial supervisor (exercise)", "DORA intermediate report with recovery and corrective actions")]
lines = ["---", "lab4_comms:"]
for key, value in data.items():
    if isinstance(value, dict):
        lines.append(f"  {key}:")
        lines.extend(f"    {name}: {json.dumps(fmt(instant))}" for name, instant in value.items())
    else:
        lines.append(f"  {key}: {json.dumps(fmt(value))}")
lines.append("  log:")
for at, to, what in entries:
    lines.extend([f"    - at: {json.dumps(fmt(at))}", f"      to: {json.dumps(to)}", f"      what: {json.dumps(what)}"])
lines.extend(["---", "<!-- ai-generated: 95% - Codex calculated the course's regulator clocks from the actual incident and a hypothetical report schedule. -->", "", "# Communications log", "",
"## The three instants", "",
f"Detection is {fmt(detection)}, the automated detecting alert's first firing timestamp. Awareness of a significant incident is {fmt(awareness)}, when its P1 notification reached the on-call pager. The earlier monitoring checks showed individual errors; the page established a sustained checkout symptom warranting incident handling. Classification as major is {fmt(classification)}, the investigation measurement that quantified a 14.6-second checkout p99 and widespread catalog-dependent latency.", "",
"For this exercise we assume the shop and incident meet the applicability and significance conditions stated in the course. These are hypothetical report submissions; no notifications were actually sent. The choice of classification time reflects the confirmed impact, rather than treating every initial metric anomaly as a completed classification.", "",
"## Report schedule", "",
"| UTC submission | Recipient | Content |", "|---|---|---|"])
lines.extend(f"| {fmt(at)} | {to} | {what} |" for at, to, what in entries)
lines.extend(["", "NIS2 runs from awareness, while KSC runs from detection. Their early warnings are due 24 elapsed hours later and their incident notifications 72 hours later. The planned CSIRT notifications precede both deadlines; each final report is due one UTC calendar month after its own notification submission.", "",
f"DORA's initial deadline is {fmt(initial_due)}: four hours after classification is earlier than awareness plus 24 hours. The planned initial submission at {fmt(initial)} is within that deadline. Its intermediate deadline is 72 hours after that initial submission, and its final deadline is one UTC calendar month after the intermediate submission.", "",
"The calculations use the course's I-30 arithmetic, including its instruction to ignore DORA weekend relief. Instants and month arithmetic remain in UTC; local clock changes do not alter elapsed-hour deadlines.", ""])
(root / "comms-log.md").write_text("\n".join(lines), encoding="utf-8")
for category in ("nis2", "ksc", "dora"):
    print(category, {key:fmt(value) for key,value in data[category].items()})
