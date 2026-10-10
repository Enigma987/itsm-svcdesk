---
actual_minutes: 1
ratio: 0.01
---

The feature was the DORA metrics implementation in `src/svcdesk/dora.py`. I measured one minute from the first edit to the first checker run that passed the DORA API contract and reproduced the practice metrics. Against the 150-minute prediction, the actual-to-predicted ratio is 0.01 to two decimal places. The estimate overshot substantially because I initially budgeted for working through every unusual log case and integrating an unfamiliar endpoint. The implementation could reuse the existing FastAPI application and standard-library date, decimal, and collection tools, and the specification stated the edge-case rules explicitly. The first checker run confirmed the API shape and metric values; the checker also showed that the remaining work was preparing the required reports rather than changing the feature. This is one observation, not a reliable estimate for another project: the feature was unusually well specified, the practice answers were published, and an AI assistant produced most of the implementation.
