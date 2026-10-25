# ai-generated: 95% - Codex wrote evidence-based scoring of the instructor's verbatim recorded hypotheses.
"""Evaluate recorded hypotheses on this live run; retain all returned query evidence."""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab4_live import ROOT, http, now, query, state

AT = "2026-10-25T15:32:39Z"
current = state()
params = {"query": "timestamp(seeded_fault_active)", "start": current["arm"]["armed_at"], "end": now(), "step": "1s"}
import urllib.parse
_, raw = http(9090, "/api/v1/query_range?" + urllib.parse.urlencode(params))
rows = raw["data"]["result"]
assert len(rows) == 1 and rows[0]["values"], raw
onset = datetime.fromtimestamp(int(float(rows[0]["values"][0][1])), timezone.utc)
baseline = (onset - timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
text = (ROOT / "ai-rca/transcript.md").read_text(encoding="utf-8")
quotes = [" ".join(item.split()) for item in re.findall(r"(Hypothesis \d+:.*?)\s+Query:", text, re.S)]
assert len(quotes) == 4, quotes
frontend = 'sum(rate(traces_span_metrics_calls_total{service_name="frontend",span_kind="SPAN_KIND_SERVER"}[5m]))'
_, baseline_traffic = query(frontend, baseline)
_, incident_traffic = query(frontend, AT)
assert len(baseline_traffic) == 1 and len(incident_traffic) == 1
load_threshold = float(baseline_traffic[0]["value"][1]) * 2
checkout_errors = 'sum(rate(traces_span_metrics_calls_total{service_name="checkout",span_kind="SPAN_KIND_SERVER",span_name="oteldemo.CheckoutService/PlaceOrder",status_code="STATUS_CODE_ERROR"}[5m])) > 0.01'
catalog_partial = 'histogram_quantile(0.99,sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="product-catalog",span_kind="SPAN_KIND_SERVER"}[5m]))) > 2000 unless on() sum(rate(traces_span_metrics_calls_total{service_name="product-catalog",span_kind="SPAN_KIND_SERVER",status_code="STATUS_CODE_ERROR"}[5m])) > 0.01'
payment_errors = 'sum(rate(traces_span_metrics_calls_total{service_name="payment",span_kind="SPAN_KIND_SERVER",status_code="STATUS_CODE_ERROR"}[5m])) > 0.01'
load_claim = f'({checkout_errors}) and on() ({frontend} > {load_threshold:.12g})'
definitions = [
    ("checkout", checkout_errors, "hallucinated", "The recorded claim describes steady failed PlaceOrder calls, but our checkout service had traffic and no server-error series at this instant. The actual page concerned latency. This is a hypothesis from another run, as permitted by the transcript route."),
    ("product-catalog", catalog_partial, "partially_correct", "The component was relevant, but its observed failure mode was latency rather than server errors. The query returns the slow-catalog comparison only when the error comparison is absent. This goes beyond the CheckoutLatencyHigh alert by testing the downstream catalog service. The live flag observation corroborates catalog contention."),
    ("payment", payment_errors, "hallucinated", "Payment had successful traffic and no server-error series in our fault window. Its histogram p99 was about 1.98 ms at the recorded investigation point. The transcript's payment-failure guess is contradicted by our run."),
    ("checkout", load_claim, "hallucinated", "The recorded statement inferred steady checkout error growth and high load from cumulative counters. Our live checkout error comparison is false, and frontend traffic did not exceed twice its healthy baseline. A recommendation cache flag was active, but that fact does not substantiate the claimed system-wide error spike or high load."),
]
ledger = {"investigator": {"agent": "course agent.py (instructor-supplied recorded investigation)", "model": "qwen3:4b-instruct", "mcp_server": "prom_mcp.py (mcp 2.2.0)", "transcript": "ai-rca/transcript.md"}, "hypotheses": []}
evidence = {"source": "instructor-supplied lab4-rec-3 transcript, tested on our live run", "run": current["run"], "onset": onset.isoformat().replace("+00:00", "Z"), "at": AT, "baseline": baseline, "frontend_baseline": baseline_traffic, "frontend_incident": incident_traffic, "queries": []}
for index, (component, expression, verdict, explanation) in enumerate(definitions, 1):
    _, result = query(expression, AT)
    _, healthy = query(expression, baseline)
    actual = bool(result)
    assert actual == (verdict != "hallucinated"), {"entry": index, "result": result}
    if actual:
        assert not healthy, {"entry": index, "baseline": healthy}
    info = {"id": f"H{index}", "hypothesis": quotes[index-1], "component": component, "predicts": expression, "at": AT, "result": actual, "verdict": verdict, "evidence": explanation + f" At {AT}: {json.dumps(result)}. At baseline {baseline}: {json.dumps(healthy)}."}
    ledger["hypotheses"].append(info)
    evidence["queries"].append({"id": info["id"], "expression": expression, "at_result": result, "baseline_result": healthy})
    print(info["id"], verdict, "result", actual, "baseline", bool(healthy), flush=True)
(ROOT / "ai-rca-eval.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
(ROOT / "ai-rca/query-results.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
print("onset", evidence["onset"], "baseline", baseline, "frontend rates", baseline_traffic[0]["value"][1], incident_traffic[0]["value"][1])
