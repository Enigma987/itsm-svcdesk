---
lab5_triage:
  image: ghcr.io/enigma987/itsm-svcdesk@sha256:418bca8817cced7e54b88cc7872685636cf3c46af83b015012c463834d1a162d
  sarif_receipt: 0
---
<!-- ai-generated: 95% - Codex inspected the real CI reports and drafted decisions and the measured scanner comparison. -->
# Triage

The initial main run, 43603105649 on commit 106468d, passed every CI job. Its dependency scanners and gitleaks reported no findings. Semgrep reported the two rule identifiers below. The Dockerfile pins the pulled Python 3.13 slim digest, applies Debian security upgrades, and removes pip after installation. The build log confirms the zlib1g upgrade to 1:1.3.dfsg+really1.3.1-1+deb13u1 and removal of pip 26.2.2. These changes reduce the installed runtime surface without hiding scanner results. Both ignore files contain no entries.

| Tool | Rule | Decision | Reason |
|---|---|---|---|
| semgrep | dockerfile.security.missing-user.missing-user | accept | Dockerfile runs the course service as root and stores SQLite in the existing named data volume. Accept this container privilege risk for the isolated university service until 2026-11-28. A later non-root migration must also assign ownership of existing data volumes so previously stored tickets remain accessible. |
| semgrep | python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected | false-positive | In src/svcdesk/main.py, GET /kb/search takes its upstream origin from the deployment-controlled KB_INDEX_URL. The request's q value is URL-encoded into a query parameter. A caller cannot supply a URL scheme, host, or local file path through q. The deployed origin is http://kb-index:8080. |
| semgrep | python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected | false-positive | scripts/lab4_live.py constructs a URL with a literal http://localhost origin. scripts/lab4_score_second.py fixes http://localhost:19090/api/v1/query and URL-encodes the query arguments. These are local incident tools, and their variable arguments cannot select file:// URLs. |
| semgrep | python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected | false-positive | Laboratory 4/agent/prom_mcp.py gets PROMETHEUS_URL from the operator's process environment and appends fixed Prometheus API paths. Its tool arguments are URL-encoded. There is no request-controlled URL origin in this local course investigator. |

## Bake-off

The comparison will be completed from the unchanged canary SARIF and the labels revealed after its receipt.
