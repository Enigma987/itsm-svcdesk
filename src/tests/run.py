# ai-generated: 95% - AI wrote HTTP contract tests from the published Lab 2 requirements.
"""Small standard-library integration suite used by the compose tests profile."""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
import urllib.request


BASE = os.environ.get("SVCDESK_URL", "http://127.0.0.1:8080").rstrip("/")
WINDOW = {"from": "2026-09-01T00:00:00Z", "to": "2026-09-22T00:00:00Z"}


def request(path: str, *, method: str = "GET", body=None, headers=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request_headers = {"Content-Type": "application/json"} if data is not None else {}
    request_headers.update(headers or {})
    req = urllib.request.Request(BASE + path, data=data, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "")
            return response.status, content_type, json.loads(payload) if payload else None
    except urllib.error.HTTPError as response:
        payload = response.read()
        return response.code, response.headers.get("Content-Type", ""), json.loads(payload) if payload else None


def metric_body(events=None):
    return {"window": dict(WINDOW), "events": [] if events is None else events}


class DoraHttpTests(unittest.TestCase):
    def test_01_health_is_ready(self):
        status, _, body = request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["service"], "svcdesk")

    def test_02_empty_metrics_return_success(self):
        status, content_type, body = request("/dora/metrics", method="POST", body=metric_body())
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertEqual(body["deployment_frequency_per_day"], 0.0)

    def test_03_empty_metrics_have_null_medians_and_ratios(self):
        _, _, body = request("/dora/metrics", method="POST", body=metric_body())
        for key in ("change_lead_time_seconds_p50", "failed_deployment_recovery_time_seconds_p50", "change_fail_rate", "deployment_rework_rate"):
            self.assertIsNone(body[key])

    def test_04_response_has_spec_version_and_window(self):
        _, _, body = request("/dora/metrics", method="POST", body=metric_body())
        self.assertEqual(body["spec_version"], "1.0.0")
        self.assertEqual(body["window"], WINDOW)

    def test_05_response_contains_all_metric_groups(self):
        _, _, body = request("/dora/metrics", method="POST", body=metric_body())
        self.assertTrue({"counts", "anomalies", "ground_truth"}.issubset(body))

    def test_06_missing_window_is_rejected(self):
        status, _, body = request("/dora/metrics", method="POST", body={"events": []})
        self.assertIn(status, (400, 422))
        self.assertIn("error", body)

    def test_07_non_array_events_are_rejected(self):
        status, _, body = request("/dora/metrics", method="POST", body={"window": WINDOW, "events": {}})
        self.assertIn(status, (400, 422))
        self.assertIn("error", body)

    def test_08_non_increasing_window_is_rejected(self):
        bad = {"from": WINDOW["to"], "to": WINDOW["from"]}
        status, _, body = request("/dora/metrics", method="POST", body={"window": bad, "events": []})
        self.assertIn(status, (400, 422))
        self.assertIn("error", body)

    def test_09_unknown_revert_sha_is_rejected(self):
        event = {"event_id": "bad-c", "type": "commit", "at": WINDOW["from"], "sha": "c1", "branch": "main", "change_id": None, "reverts": "missing"}
        status, _, body = request("/dora/metrics", method="POST", body=metric_body([event]))
        self.assertIn(status, (400, 422))
        self.assertIn("error", body)

    def test_10_event_order_does_not_change_metrics(self):
        commit = {"event_id": "c1", "type": "commit", "at": "2026-09-02T00:00:00Z", "sha": "s1", "branch": "release", "change_id": "ch1", "reverts": None}
        deploy = {"event_id": "d1", "type": "deployment", "at": "2026-09-03T00:00:00Z", "deployment_id": "dep1", "environment": "production", "outcome": "success", "commits": ["s1"], "unplanned": False, "caused_by": None}
        _, _, first = request("/dora/metrics", method="POST", body=metric_body([commit, deploy]))
        _, _, second = request("/dora/metrics", method="POST", body=metric_body([deploy, commit]))
        self.assertEqual(first, second)

    def test_11_duplicate_event_id_is_counted_once(self):
        deployment = {"event_id": "d1", "type": "deployment", "at": "2026-09-03T00:00:00Z", "deployment_id": "dep1", "environment": "production", "outcome": "success", "commits": [], "unplanned": False, "caused_by": None}
        _, _, once = request("/dora/metrics", method="POST", body=metric_body([deployment]))
        _, _, twice = request("/dora/metrics", method="POST", body=metric_body([deployment, deployment]))
        self.assertEqual(once, twice)

    def test_12_ticket_event_endpoint_returns_an_array(self):
        status, _, body = request("/dora/ticket-events")
        self.assertEqual(status, 200)
        self.assertIsInstance(body, list)

    def test_13_created_ticket_has_created_stream_event(self):
        status, _, ticket = request(
            "/tickets",
            method="POST",
            body={"title": "Stream test", "reporter": {"name": "Test User"}, "impact": 2, "urgency": 2},
            headers={"X-Test-Clock": "2026-10-01T10:00:00Z"},
        )
        self.assertEqual(status, 201)
        _, _, stream = request("/dora/ticket-events")
        entries = [event for event in stream if event["ticket_id"] == ticket["id"]]
        self.assertEqual([(event["phase"], event["state"]) for event in entries], [("created", "new")])

    def test_14_resolved_ticket_stream_has_real_lifecycle_instants(self):
        status, _, ticket = request(
            "/tickets",
            method="POST",
            body={"title": "Lifecycle test", "reporter": {"name": "Test User"}, "impact": 1, "urgency": 1},
            headers={"X-Test-Clock": "2026-10-02T10:00:00Z"},
        )
        self.assertEqual(status, 201)
        ticket_id = ticket["id"]
        for action, at in (("ack", "2026-10-02T10:01:00Z"), ("start", "2026-10-02T10:02:00Z"), ("resolve", "2026-10-02T10:03:00Z")):
            status, _, _ = request(f"/tickets/{ticket_id}/{action}", method="POST", headers={"X-Test-Clock": at})
            self.assertEqual(status, 200)
        _, _, stream = request("/dora/ticket-events")
        phases = [event["phase"] for event in stream if event["ticket_id"] == ticket_id]
        self.assertEqual(phases, ["created", "acknowledged", "resolved"])
        self.assertNotIn("in_progress", phases)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DoraHttpTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"ITSMLAB-TESTS: passed={passed} failed={len(result.failures) + len(result.errors)}")
    raise SystemExit(0 if result.wasSuccessful() else 1)
