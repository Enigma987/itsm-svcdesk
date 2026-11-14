---
lab5_triage:
  image: ghcr.io/enigma987/itsm-svcdesk@sha256:418bca8817cced7e54b88cc7872685636cf3c46af83b015012c463834d1a162d
  sarif_receipt: 393
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

The measured input is the five unchanged SARIF reports from canary CI run 43603440511, commit 820c042. SARIF receipt [#393](https://github.com/swasik/itsm-2026-submissions/issues/393) binds their hashes and names that canary commit. The course revealed nine labelled defects after accepting that receipt. The committed bakeoff.json is computed by bakeoff.py from those reports and the revealed bakeoff/labels.json. The same implementation reproduces the published practice matrix. Results outside lab5-canary are excluded from this matrix and covered by the triage table above.

Gitleaks found two defects, with TP 2, FP 0 and FN 7. Its precision is 1.0000, recall 0.2222 and F1 0.3636. Grype and OSV-Scanner each have exactly the same cells and scores because they both found the two labelled vulnerable packages, python-multipart and urllib3. Their raw report sizes, 22 and 44 findings, do not mean 22 or 44 detected defects. Multiple advisories and duplicate results on those two pins count as two true positives under the published rule.

Trivy found the two vulnerable pins and one labelled secret, giving TP 3, FP 0, FN 6, precision 1.0000, recall 0.3333 and F1 0.5000. Semgrep found three code defects and two secrets, giving TP 5, FP 3, FN 4, precision 0.6250, recall 0.5556 and F1 0.5882. The three false positives have concrete explanations. Disabling Jinja autoescaping in email_render.py is appropriate for these plain-text messages. The SQL expression in ticket_counts.py casts the supplied identifier to int before formatting it. Two distinct Semgrep rules flag that same safe statement, and each has a distinct ruleId, so the counting rule retains two false positives there.

I would keep gitleaks and Trivy as blocking gates with reviewed, expiring exceptions, while retaining Grype, OSV-Scanner and Semgrep as reports for triage. The two gates correctly changed from green on the identical parent pipeline to red after the canary files were added. Their observed precision of 1.0000 supports that choice on this set, but their low recall means a green result cannot establish that the code is secure. Semgrep adds valuable code findings, and its three false positives show why its current broad rules should receive contextual review before becoming blocking policy.

Across all five tools, seven distinct defects were found. None found the password-reset token made with random.choice in reset_tokens.py or the hard-coded JWT secret in jwt_secret.py. These need semantic knowledge of security-sensitive randomness and the credential's role, beyond the signatures that fired here. The union finding seven of nine is separate from each tool's recall. This is a small, seeded set selected from a known pool. Seeded defects flatter detectors, and the measured recalls should be treated as upper bounds for this exercise rather than predictions of performance on arbitrary production defects. No detector's score was adjusted to improve its appearance.
