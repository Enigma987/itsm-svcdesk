---
lab3_first_draft:
  source: ai
  tool: "OpenAI Codex (GPT-6), Codex desktop, 10 October 2026"
  ladder: [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10]
  verdict: TODO
  evidence: {p99_seconds: TODO, bucket: [TODO, TODO], relative_width: TODO}
lab3_flawed_ladder:
  verdict: refuted
  evidence: {p99_seconds: TODO, bucket: [TODO, TODO], relative_width: TODO}
---
<!-- ai-generated: 90% - AI supplied the exchange verbatim; assistant will add measured evidence and verdicts. -->

# The assistant's first draft, and two verdicts

## Prompt

Act as a practical observability assistant. For a FastAPI service exposing GET /kb/search that calls a knowledge-base index, recommend a Prometheus histogram bucket ladder (finite boundaries, in seconds) suitable for p99 monitoring, plus one actionable Prometheus alert rule for availability. Assume a 30-day SLO window and 99.9% availability objective. Give the buckets in increasing order and the alert in YAML/PromQL, and briefly explain the choices. I have not measured this service's latency distribution yet.

## Answer

Use a histogram in seconds with a conventional logarithmic ladder that covers quick requests through multi-second slowdowns. These boundaries are a practical starting point for a general HTTP service:

`[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10]`

The denser buckets below 100 ms describe the normal fast path, while the wider upper buckets keep the number of time series manageable and still show whether requests are becoming unusually slow. Keep the unit in seconds and use the same boundaries for every label set.

For a 99.9% availability objective, a 14.4x burn over both a one-hour and a five-minute window is a useful fast alert. It means the service is consuming its 30-day error budget rapidly, and the short window confirms the problem is still active. The rule filters to the search route and counts HTTP 5xx responses as bad:

```yaml
- alert: KbSearchAvailabilityBurnFast
  expr: |
    sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search", http_response_status_code=~"5.."}[1h]))
      / sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search"}[1h]))
      > 14.4 * (1 - 0.999)
    and
    sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search", http_response_status_code=~"5.."}[5m]))
      / sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search"}[5m]))
      > 14.4 * (1 - 0.999)
  for: 2m
  labels:
    service: svcdesk
    slo: availability
    severity: P1
  annotations:
    summary: "The /kb/search availability budget is burning rapidly"
```

This is a generic starting point. Once the service's actual latency distribution is measured, check whether the bucket containing p99 is narrow enough for a trustworthy percentile; if not, add boundaries around that part of the distribution.

## Verdict on the draft ladder

TODO: after measurement, record the measured p99, its bucket and relative width, then state the verdict.

## The draft alert rule

TODO: after selecting the SLO, explain what the draft alert would do and which parts were retained.

## Verdict on the instructor's flawed ladder

TODO: after measurement, record the measured p99, its bucket and relative width, then explain why the verdict is refuted.
