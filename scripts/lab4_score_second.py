# ai-generated: 95% - Codex independently evaluated the fresh investigator's verbatim claims on the preserved snapshot.
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "ai-rca/second/hypotheses.json").read_text(encoding="utf-8"))
transcript = (ROOT / "ai-rca/second/transcript.md").read_text(encoding="utf-8")
clocks = json.loads((ROOT / "incident/recomputed-output.txt").read_text(encoding="utf-8"))
baseline = (datetime.fromisoformat(clocks["onset"].replace("Z", "+00:00")) - timedelta(seconds=300)).isoformat().replace("+00:00", "Z")
at = "2026-10-25T15:32:39Z"


def query(expression, instant):
    url = "http://localhost:19090/api/v1/query?" + urllib.parse.urlencode({"query": expression, "time": instant})
    with urllib.request.urlopen(url, timeout=20) as response:
        body = json.load(response)
    assert body["status"] == "success", body
    return body["data"]["result"]


catalog = 'histogram_quantile(0.95,sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="product-catalog",span_name="astronomy-db",span_kind="SPAN_KIND_CLIENT"}[5m])))'
checkout = 'histogram_quantile(0.95,sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="checkout",span_kind="SPAN_KIND_SERVER"}[5m])))'
waits = 'sum(rate(db_sql_connection_wait_total{service_name="product-catalog"}[5m]))'
payment_client = 'histogram_quantile(0.95,sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="checkout",span_name="oteldemo.PaymentService/Charge",span_kind="SPAN_KIND_CLIENT"}[5m])))'
definitions = [
    {"component": "product-catalog", "predicts": f"({catalog} > 2000) and on() ({checkout} > 2000)", "verdict": "correct", "signals": {"catalog_db_client_p95_ms": catalog, "checkout_server_p95_ms": checkout}, "explanation": "The catalog-to-database and checkout paths are both slow at the incident instant and neither is slow on the healthy baseline. This supports the dependency-chain localization beyond the CheckoutLatencyHigh alert's service name. The precise database mechanism remains unproved by this comparison; the investigator explicitly stated that uncertainty. Histogram ceilings limit tail precision."},
    {"component": "product-catalog", "predicts": f"{waits} > 0", "verdict": "hallucinated", "signals": {"pool_waits_per_second": waits}, "explanation": "Pool wait counters exist but their five-minute rate is zero, contradicting capacity-wait exhaustion. This was an explicitly investigated and rejected candidate, not the investigator's asserted final diagnosis. The required ledger verdict labels the candidate prediction as contradicted; it does not mean the investigator ignored its own evidence."},
    {"component": "payment", "predicts": f"{payment_client} > 1000", "verdict": "hallucinated", "signals": {"checkout_payment_client_p95_ms": payment_client}, "explanation": "Checkout's payment call remains fast rather than carrying the seconds-scale latency needed to explain the incident. CPU magnitude alone does not establish saturation, and the investigator rejected this competing cause. The required ledger enum applies to the contradicted candidate, not to a confident false final conclusion."},
]
ledger = {"investigator": {"agent": "Codex fresh-context investigator (independent_investigator)", "model": "GPT-6 (inherited session model; exact API identifier not exposed)", "mcp_server": "prom_mcp.py (mcp 2.2.0), via lab4_mcp_client.py", "transcript": "ai-rca/second/transcript.md"}, "hypotheses": []}
proof = {"at": at, "baseline": baseline, "queries": []}
for index, definition in enumerate(definitions):
    claim = source["hypotheses"][index]["claim"]
    assert " ".join(claim.split()) in " ".join(transcript.split()), claim
    result = query(definition["predicts"], at)
    healthy = query(definition["predicts"], baseline)
    expected = definition["verdict"] == "correct"
    assert bool(result) == expected, {"claim": claim, "result": result}
    if expected:
        assert not healthy, healthy
    signals = {name: {"expression": expression, "fault": query(expression, at), "baseline": query(expression, baseline)} for name, expression in definition["signals"].items()}
    item = {"id": f"S{index+1}", "hypothesis": claim, "component": definition["component"], "predicts": definition["predicts"], "at": at, "result": bool(result), "verdict": definition["verdict"], "evidence": definition["explanation"] + " The scorecard re-evaluates five-minute windows, rather than relying on the investigator's noisier two-minute exploration. Numeric signals: " + json.dumps(signals)}
    ledger["hypotheses"].append(item)
    proof["queries"].append({"id": item["id"], "expression": item["predicts"], "at_result": result, "baseline_result": healthy, "signals": signals})
    print(item["id"], item["verdict"], json.dumps(signals), flush=True)
(ROOT / "ai-rca-eval-2.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
(ROOT / "ai-rca/second/query-results.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
