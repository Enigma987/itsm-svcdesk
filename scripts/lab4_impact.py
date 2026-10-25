# ai-generated: 95% - Codex collected reproducible impact measurements at explicit instants inside the snapshot.
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab4_live import ROOT, query

clocks = json.loads((ROOT / "incident/recomputed-output.txt").read_text(encoding="utf-8"))
times = {"baseline": "2026-10-25T15:21:04Z", "fault": "2026-10-25T15:32:39Z", "recovered": "2026-10-25T15:41:00Z"}
queries = {
    "p99_ms": 'histogram_quantile(0.99,sum by(service_name,le)(rate(traces_span_metrics_duration_milliseconds_bucket{span_kind="SPAN_KIND_SERVER"}[5m])))',
    "requests_per_second": 'sum by(service_name)(rate(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER"}[5m]))',
    "errors_per_second": 'sum by(service_name)(rate(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER",status_code="STATUS_CODE_ERROR"}[5m]))',
    "recommendation_rss_bytes": 'max(process_memory_usage_bytes{service_name="recommendation"})',
}
result = {"clocks": clocks, "measurements": {}}
for label, at in times.items():
    result["measurements"][label] = {"at": at, "queries": {}}
    for name, expression in queries.items():
        _, rows = query(expression, at)
        result["measurements"][label]["queries"][name] = {"expression": expression, "result": rows}
        compact = {r["metric"].get("service_name", "value"): r["value"][1] for r in rows}
        print(label, name, json.dumps(compact))
for label, status_filter in [("incident_calls", ""), ("incident_errors", ',status_code="STATUS_CODE_ERROR"')]:
    expression = 'sum by(service_name)(increase(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER"' + status_filter + '}[' + str(clocks["mttr_seconds"]) + 's]))'
    _, rows = query(expression, clocks["recovery"])
    result[label] = {"expression": expression, "at": clocks["recovery"], "result": rows}
    print(label, json.dumps({r["metric"]["service_name"]: r["value"][1] for r in rows}))
expression = 'sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="product-catalog",span_kind="SPAN_KIND_SERVER"}[5m]))'
_, rows = query(expression, times["fault"])
result["catalog_buckets_during_fault"] = {"expression": expression, "at": times["fault"], "result": rows}
print("catalog boundaries", [r["metric"]["le"] for r in rows])
(ROOT / "incident/impact-evidence.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
