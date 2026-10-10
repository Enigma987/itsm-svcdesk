---
lab3_slo:
  service: svcdesk
  route: /kb/search
  window: 30d
  slis:
    availability:
      objective: 0.99
      good: 'sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search", http_response_status_code!~"5.."}[5m]))'
      valid: 'sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search"}[5m]))'
      error_budget: {fraction: 0.01, minutes: 432}
    latency:
      objective: 0.95
      threshold_seconds: 0.135
      good: 'sum(rate(http_server_request_duration_seconds_bucket{job="svcdesk", http_route="/kb/search", le="0.135"}[5m]))'
      valid: 'sum(rate(http_server_request_duration_seconds_count{job="svcdesk", http_route="/kb/search"}[5m]))'
      error_budget: {fraction: 0.05, minutes: 2160}
  alerts:
    - {alert: KbSearchErrorsBurnFast, sli: availability, burn_rate: 14.4, long_window: 1h, short_window: 5m}
    - {alert: KbSearchErrorsBurnSlow, sli: availability, burn_rate: 6, long_window: 6h, short_window: 30m}
---
<!-- ai-generated: 90% - AI drafted from the published SLO contract and measured kb-index latency. -->

# SLO for `GET /kb/search`

## Availability

Availability is the share of `/kb/search` responses that are not HTTP 5xx over 30 days. I set the objective to 99%: the measured dependency returned 9 failures among 2,399 responses in the first run, about 0.38%, before accounting for any independent service failures. A 99.9% objective would leave less budget than the dependency's observed failures alone. The 1% budget is 432 minutes in a 30-day window.

## Latency

The latency SLI is the share of search requests completed within 135 ms. The first measured distribution had p50 17.8 ms and p99 130.8 ms, with a small slow mode around 115–162 ms. The 135 ms threshold sits just above p99 and is a finite histogram boundary, so the SLI can count good requests directly. A 95% objective leaves room for the observed slow tail while still exposing a material regression; its 5% budget is 2,160 minutes per 30 days.

## Alerts

| alert | SLI | burn rate | long / short window | budget spent when it fires | severity: page or chat |
|---|---|---:|---|---|---|
| KbSearchErrorsBurnFast | availability | 14.4 | 1h / 5m | 14.4% per hour, if sustained | P1 page |
| KbSearchErrorsBurnSlow | availability | 6 | 6h / 30m | 6% per hour, if sustained | P2 chat |

The fast alert uses the classic 14.4x burn and requires both windows to agree; at 1h / 30d it spends about 2% of the monthly budget in an hour, so a page is justified. The slow alert catches a less extreme but persistent failure rate and goes to chat; at 6x over six hours it spends about 5% of the budget. Both thresholds are calibrated to the 99% objective, and both filter to this route.

## Buckets

The final ladder is `[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15, 0.2, 0.25, 0.5, 1, 2.5, 5, 10]`. In the first measurement p99 was 0.1308 s, in `(0.13, 0.135]`, a 3.8% relative width. The dense band from 0.115 to 0.15 s resolves the measured slow mode and p99 with margin for run-to-run variation; the other boundaries retain useful coverage from 5 ms to 10 s without exceeding 30 buckets.
