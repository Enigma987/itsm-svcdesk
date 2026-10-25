---
lab4_postmortem:
  ticket: "4dad5d92-4e99-4171-81bd-eff5de44ad44"
  detecting_alert: CheckoutLatencyHigh
  onset: "2026-10-25T15:26:04Z"
  detection: "2026-10-25T15:31:19Z"
  acknowledgement: "2026-10-25T15:31:43Z"
  recovery: "2026-10-25T15:38:19Z"
  mttd_seconds: 315
  mtta_seconds: 24
  mttr_seconds: 735
  identified_flags: [adFailure, productCatalogLockContention, recommendationCacheFailure]
---
<!-- ai-generated: 95% - Codex drafted from actual live API records, saved Prometheus queries, and official incident recomputation. -->

# Postmortem: catalog contention delayed checkout and storefront requests

## Date

The incident occurred on 25 October 2026. This review was written after recovery on the same day; every time below is UTC.

## Authors

Prepared for Enigma987's on-call exercise with Codex assistance. The AI scorecard evaluates the instructor-supplied qwen3:4b-instruct transcript against this live run.

## Status

Service is restored and the P1 ticket is resolved. The problem record remains open, with the preventive and process actions below still to be implemented.

## Summary

Run ec32ba4dcd5b15ca enabled three fault flags at the observed onset, 15:26:04Z. Catalog lock contention delayed catalog-dependent requests, ad calls failed, and the recommendation cache-failure path was enabled. Checkout latency triggered the P1 page. All three flags were disabled separately; the detecting alert resolved at 15:38:19Z, giving an alert-defined incident duration of 735 seconds.

## Impact

Ten simulated users were shopping. These measurements describe server spans, not a count of distinct customers or lost orders. All values are reproduced in incident/impact-evidence.json.

At 15:32:39Z, the five-minute histogram p99 estimate for checkout was 14,600 ms, compared with 49.6 ms at the healthy baseline, 15:21:04Z. Product catalog, recommendation, frontend and frontend-proxy each returned a 15,000 ms p99 estimate. Their ladder ends at 15,000 ms before +Inf, so that value is a saturated estimate and cannot describe the actual upper tail accurately.

The latency query, evaluated at each named instant, was:

    histogram_quantile(0.99, sum by (service_name, le) (rate(traces_span_metrics_duration_milliseconds_bucket{span_kind="SPAN_KIND_SERVER"}[5m])))

Frontend server-span throughput fell from 4.129 calls/s on the baseline to 2.375 calls/s during the fault, about 42%. This is reduced observed throughput, not a direct estimate of demand or abandoned orders. The query was:

    sum by (service_name) (rate(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER"}[5m]))

Over onset to alert recovery, the following are rounded estimates from increase(), which extrapolates counters at sample boundaries:

| Service | Completed server spans | Error server spans |
|---|---:|---:|
| frontend-proxy | 1,180 | 98 |
| frontend | 2,163 | 24 |
| ad | 109 | 12 |
| checkout | 57 | No error series observed |

Both queries were evaluated at 15:38:19Z, using the 735-second incident window:

    sum by (service_name) (increase(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER"}[735s]))
    sum by (service_name) (increase(traces_span_metrics_calls_total{span_kind="SPAN_KIND_SERVER",status_code="STATUS_CODE_ERROR"}[735s]))

At the fault measurement, ad's five-minute error fraction was 0.2174, frontend's 0.01754, and frontend-proxy's 0.1693. Checkout had successful traffic without a server-error series; its harmful symptom was latency. By 15:41:00Z, checkout p99 was back to 49.6 ms and the observed frontend, proxy and ad error rates were zero.

## Root Causes

The live flag document showed adFailure, productCatalogLockContention and recommendationCacheFailure enabled. Every corresponding off call returned changed: true.

The catalog fault path acquires an ACCESS EXCLUSIVE database lock on catalog.products for 30 seconds. This blocks reads used by catalog, storefront, recommendation and checkout paths. The observed catalog-dependent latency and the restoration after rollback support it as the principal cause of the checkout latency page. It was lock contention, not the productCatalogFailure error-injection flag.

adFailure introduced ad request failures. The ad error rate was measured independently from server spans and its flag was rolled back after catalog contention.

The recommendation cache-failure path grows a process-wide cached list on misses, including repeated copies of existing entries. Its activation and code path were confirmed, but this run does not establish severe memory pressure: the measured process-memory value changed only from 70,131,712 bytes at the baseline to 70,389,760 bytes at the fault instant. Recommendation latency also depended on the blocked catalog, so attributing all of its 15-second p99 estimate to the cache would overstate the evidence.

## Trigger

The course injector was armed at 15:20:48Z after an empty P1 baseline gate. Its first seeded_fault_active sample was at 15:26:04Z. The simultaneous feature-flag activation exposed the unsafe locking, failure and cache paths; the preceding ten-minute P1 window was quiet.

## Resolution

Catalog contention was disabled first at 15:32:45Z because it affected order placement and several dependent services. adFailure was disabled at 15:34:10Z to stop the observed ad failures. recommendationCacheFailure was disabled at 15:35:13Z to remove the remaining injected cache behavior. Each response confirmed changed: true; subsequent fault activity was zero.

The detecting alert resolved at 15:38:19Z after its five-minute measurement window and two-minute keep_firing_for behavior cleared. Its resolved webhook reached the pager at 15:38:39Z. We observed an additional 70 seconds without firing alerts before taking the snapshot. The ticket was moved through start and resolve and reached resolved state at 15:42:01Z.

Disabling the flags is the operational workaround. The problematic code paths still exist and require the preventive actions below.

## Detection

CheckoutLatencyHigh detected the incident at 15:31:19Z, 315 seconds after onset. It checks checkout SERVER-span histogram p99 over five minutes against 2,000 ms, with a one-minute pending period. Span metrics arrive once a minute; the pending period, sparse checkout completions and rolling measurement window all contribute to delay, although this snapshot cannot isolate each contribution exactly.

The pager received the firing notification at 15:31:39Z. Ticket creation was at 15:31:41Z and acknowledgement at 15:31:43Z, so MTTA is 24 seconds from detection, rather than from webhook delivery. An error-only checkout page would have missed this run: no checkout server-error series was observed at the investigation instant. Without the latency page, a person would have had to notice the slower storefront or the throughput drop manually.

The official clocks are MTTD 315 s, MTTA 24 s and MTTR 735 s. MTTR ends at the detecting alert's recovery, which differs from the last flag-off time.

## Action Items

| Action Item | Type | Owner | Bug |
|---|---|---|---|
| Add bounded catalog query timeouts and a tested degraded-response path so a catalog lock cannot stall order placement indefinitely. | mitigate | Catalog service owner | ITSM-401 |
| Guard the catalog contention flag and add a rollout check that detects blocking database locks before enabling it for shopping traffic. | prevent | Catalog and release owners | ITSM-402 |
| Replace the unbounded recommendation list with a cache size budget, eviction policy and sustained-load memory test. | prevent | Recommendation service owner | ITSM-403 |
| Add a graceful ad-failure fallback and verify that ad faults do not produce storefront errors. | prevent | Frontend and ad owners | ITSM-404 |
| Maintain a rehearsed runbook covering the pager, P1 acknowledgement, staged flag rollback and snapshot verification before cleanup. | process | On-call role | ITSM-405 |

## Lessons Learned

### What went well

The quiet-baseline check preceded arming. The latency page covered a checkout incident that did not present as checkout server errors. Severity routes and the equal-label inhibition pair had been tested on an isolated Alertmanager, and both ticket requests were visible in Prometheus. The snapshot preserved the run and the service-generated ticket without manual timestamp edits.

### What went wrong

An exclusive catalog lock propagated latency across several user paths. Detection took more than five minutes, and the 15-second finite histogram ceiling obscured the full tail. The recommendation cache path is unbounded even though the short run did not produce a large measured memory increase. Cumulative error counts in the recorded investigator transcript were insufficient evidence for its claims about load and failure growth.

### Where we got lucky

The injected faults had a direct rollback interface and the exercise used simulated shoppers. Catalog rollback did not require a database restart. We also had enough retained telemetry to distinguish payment's healthy traffic from the catalog slowdown and to preserve all four incident clocks before stopping the stack.

## Timeline

| UTC | Observation or action |
|---|---|
| 15:20:46 | Baseline gate returned no P1 firing samples in ten minutes and no pending or firing alerts. |
| 15:20:48 | Injector accepted POST /arm with HTTP 202. |
| 15:25:40 | Final recorded quiet observation before the onset: no active alerts or pager notifications. |
| 15:26:04 | Onset: first seeded_fault_active sample in the snapshot. |
| 15:29:26 | A monitoring check saw ad/frontend errors while checkout's five-minute p99 estimate was still 49.6 ms. |
| 15:31:19 | Detection: CheckoutLatencyHigh began its firing run. |
| 15:31:24 | Live configuration inspection identified the three enabled flags. |
| 15:31:39 | The firing P1 webhook reached the pager. |
| 15:31:41 | P1 ticket 4dad5d92-4e99-4171-81bd-eff5de44ad44 was created. |
| 15:31:43 | The service stamped the P1 acknowledgement. |
| 15:32:39 | Measured checkout p99 14.6 s and saturated 15 s catalog/recommendation estimates. |
| 15:32:45 | Disabled productCatalogLockContention; response confirmed a change. |
| 15:34:10 | Disabled adFailure; response confirmed a change. |
| 15:35:13 | Disabled recommendationCacheFailure; response confirmed a change. |
| 15:38:19 | Recovery: the detecting alert's firing run ended. |
| 15:38:39 | The resolved webhook reached the pager. |
| 15:39:47 | Confirmed 70 seconds without firing alerts, with fault activity zero. |
| 15:42:01 | Incident ticket reached resolved state. |
| 15:42:06 | Official snapshot and ticket export were captured. |

The instructor transcript was scored retrospectively. No recorded investigator hypothesis was used to choose a live mitigation; the rollback decisions used the visible flag document and measured service symptoms.

## Supporting information

incident/recomputed-output.txt holds the official command's four timestamps and durations. incident/operations.jsonl records the actual gate, arm, pager, ticket and rollback API responses. incident/impact-evidence.json stores every impact query above, its evaluation time, and the returned data. The immutable evidence is incident/tsdb-snapshot.tar.gz and incident/ticket.json.

The instructor-supplied transcript is preserved verbatim in ai-rca/transcript.md, with provenance in ai-rca/README.md. ai-rca-eval.json quotes all four hypotheses and ai-rca/query-results.json retains their evaluation results at 15:32:39Z and at the healthy baseline, 15:21:04Z. H1, H3 and H4 were contradicted by this run. H2 was partially correct: product catalog was slow, without the asserted catalog server-error mechanism.

H2 tests the component beyond what the checkout alert itself named, using:

    histogram_quantile(0.99,sum by(le)(rate(traces_span_metrics_duration_milliseconds_bucket{service_name="product-catalog",span_kind="SPAN_KIND_SERVER"}[5m]))) > 2000 unless on() sum(rate(traces_span_metrics_calls_total{service_name="product-catalog",span_kind="SPAN_KIND_SERVER",status_code="STATUS_CODE_ERROR"}[5m])) > 0.01

It returned a value of 15,000 at the fault instant and no result on the baseline. The absence of a result here means the filtering prediction is false, rather than a zero-valued measurement. The other rejected claims retain their own explicit comparisons and returned results in the ledger.

## Problem record

- Incident record: P1 ticket 4dad5d92-4e99-4171-81bd-eff5de44ad44 is resolved after service restoration.
- Root cause: Unsafe catalog locking propagated delay through user paths, while ad failure and an unbounded recommendation cache path were enabled concurrently.
- Known error: The exclusive-lock and unbounded-cache code paths remain available behind feature flags and can reproduce the failure until corrected and guarded.
- Workaround: Keep all three identified flags disabled and verify checkout latency, ad errors and recommendation resource behavior after each configuration change.