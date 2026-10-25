<!-- ai-generated: 90% - Codex recorded the completed setup and observed pre-class trial results. -->
# Laboratory 4 preparation

Prepared on 25 October 2026 for GitHub login `Enigma987`.

## Local setup

- Demo clone: `D:\Studia\IT Network git\opentelemetry-demo`, tag `3.1.0`, commit `dedc0178918e260823323b8d95005a8cb924b007`.
- Course overlay copied to the demo's `itsm/` folder.
- The demo's `.env.override` preserves its original content and sets `DEMO_VERSION=3.1.0`, `IMAGE_VERSION=3.1.0`, `OTEL_RESOURCE_ATTRIBUTES=service.namespace=opentelemetry-demo,service.version=3.1.0`, `SVCDESK_REPO=D:/Studia/IT Network git/itsm-svcdesk`, and `ITSM_LOGIN=Enigma987`.
- All 29 required images pulled; only `svcdesk` built locally.
- Checker updated and confirmed as `itsmlab 0.8.6`.
- PC: about 32 GiB RAM; WSL ceiling 8 GB; Docker reports about 7.8 GiB available.
- Repository configuration: `lab: 4`, `baselines: {lab3: student}`.
- The supplied investigator transcripts are available under `Laboratory 4/Recordings/` for the handout's approved transcript route. The checker's recorded-path assignment is `lab4-rec-3`.

## Trial results

The unarmed trial started all 30 services, including our `svcdesk`. The shop, service health endpoint, Prometheus, Alertmanager, Grafana, Jaeger, pager, and injector health endpoint all returned HTTP 200. Grafana required extra time for first-start provisioning.

A practice P1 ticket was created and acknowledged. The service stamped its actual time despite a future `X-Test-Clock` header. Its histogram exposed `http_route="/tickets/{ticket_id}/ack"`, and Prometheus scraped the successful POST. A dedicated acknowledgement endpoint now delegates to the existing transition logic so Lab 4 can identify that operation in telemetry.

The injector remained unarmed. The trial was stopped with `down -v`, clearing its data and practice ticket. Downloaded images and the built service image remain available.

## Start the playground for the lab

Run in PowerShell:

```powershell
Set-Location 'D:\Studia\IT Network git\opentelemetry-demo'
docker compose --env-file .env --env-file .env.override -f compose.yaml -f compose.observability.yaml -f itsm/compose.itsm.yaml build svcdesk
docker compose --env-file .env --env-file .env.override -f compose.yaml -f compose.observability.yaml -f itsm/compose.itsm.yaml up -d
```

Build `svcdesk` alone when its code changes. Use the pulled images for the rest of the demo.

Open the shop at `http://localhost:8080`, Grafana at `http://localhost:8080/grafana`, and service health at `http://localhost:18080/health`.

## Work remaining during the lab

Step 2 is complete: three shop symptom alerts are loaded, P1 routes to pager, and P2/P3 route to chat. Six route cases and three inhibition cases are recorded in `alertmanager/routing-tests.yml`. The equal-label pair was proved on an isolated Alertmanager with networking disabled, and `itsmlab verify 4` reports L4-CORE-1 and L4-CORE-2 pass. The remaining bundles await the actual incident and written artifacts.

The live run is `ec32ba4dcd5b15ca`. Practice P4 ticket `fc787bd8-2906-44ce-aa89-e0b7a5bd1b90` was created and acknowledged at 2026-10-25T15:14:35Z; Prometheus scraped both successful POSTs. After reload, all five alerts were healthy and inactive, with no P1 firing in the preceding ten minutes. Recheck the baseline gate immediately before arming.

The live incident is complete. The official clocks are onset 15:26:04Z, detection 15:31:19Z, acknowledgement 15:31:43Z, and recovery 15:38:19Z on 25 October 2026: MTTD 315 s, MTTA 24 s, and MTTR 735 s. The P1 ticket is `4dad5d92-4e99-4171-81bd-eff5de44ad44`.

The official snapshot and ticket, operations log and impact evidence were committed as `9a96bb6` (`Lab 4 incident evidence`); the snapshot and ticket match the committed blobs byte for byte. The final incident verification passed all five Core bundles, with the two sealed-fault checks skipped locally, and passed the regulator-clock option. The user chose to finish Core and regulator clocks only for now; no second investigator or Kubernetes artifact is claimed.

The completed postmortem, scorecard and communications log await the implementation commit and push. The playground was stopped with `down -v` after the captured evidence was recomputed, verified and committed. Future checks can read the snapshot without restarting this incident.

## Stop the playground

After saving any real incident's snapshot and checking all four timestamps, run from the demo directory:

```powershell
docker compose --env-file .env --env-file .env.override -f compose.yaml -f compose.observability.yaml -f itsm/compose.itsm.yaml down -v
```

This removes the playground's data volumes. Keep the incident snapshot archive in the service repository before doing it for a graded run.
