# ai-generated: 95% - Codex wrote a local incident operations recorder; all logged API responses are observed.
"""Record authorized Lab 4 operations against the live local playground."""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "incident"
STATE_PATH = DIRECTORY / "live-state.json"
EXPECTED_RUN = "ec32ba4dcd5b15ca"
POOL = {"adFailure", "adManualGc", "emailMemoryLeak", "intlShippingSlowdown", "loadGeneratorFloodHomepage", "paymentFailure", "productCatalogFailure", "productCatalogLockContention", "recommendationCacheFailure"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def http(port, path, body=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"http://localhost:{port}{path}", data=data,
                                     headers={"Content-Type": "application/json"} if data is not None else {}, method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.status, json.load(response)


def record(action, **data):
    event = {"at": now(), "action": action, **data}
    DIRECTORY.mkdir(exist_ok=True)
    with (DIRECTORY / "operations.jsonl").open("a", encoding="utf-8") as output:
        output.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)
    return event


def state():
    return json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {}


def save(data):
    DIRECTORY.mkdir(exist_ok=True)
    STATE_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def query(expression, at=None):
    at = at or now()
    _, response = http(9090, "/api/v1/query?" + urllib.parse.urlencode({"query": expression, "time": at}))
    assert response["status"] == "success", response
    return at, response["data"]["result"]


def checked_status():
    _, status = http(18090, "/status")
    assert status["run"] == EXPECTED_RUN, status
    return status


def arm():
    status = checked_status()
    assert not status["armed"], "Already armed; do not create another run."
    _, age = query("time() - seeded_injector_start_timestamp_seconds")
    assert len(age) == 1 and float(age[0]["value"][1]) >= 600, age
    at, recent = query('max_over_time(ALERTS{alertstate="firing",severity="P1"}[10m])')
    _, active = query('ALERTS{alertstate=~"pending|firing"}')
    assert not recent and not active, {"P1_last_10m": recent, "active": active}
    record("baseline_gate", status=status, evaluated_at=at, P1_last_10m=recent, firing_or_pending=active)
    code, response = http(18090, "/arm", method="POST")
    assert code == 202, response
    record("armed", http_status=code, response=response)
    save({"run": EXPECTED_RUN, "arm": response})


def dictionaries(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from dictionaries(child)
    elif isinstance(value, list):
        for child in value:
            yield from dictionaries(child)


def wait_page():
    current = state()
    assert current.get("run") == EXPECTED_RUN and checked_status()["armed"], current
    assert not current.get("ticket_id"), "Ticket already exists; inspect saved state."
    deadline = time.monotonic() + 1200
    last_heartbeat = 0
    while time.monotonic() < deadline:
        _, notifications = http(18091, "/notifications")
        for notification in notifications:
            for payload in dictionaries(notification):
                if payload.get("receiver") != "pager" or payload.get("status") != "firing":
                    continue
                alerts = [a for a in payload.get("alerts", []) if a.get("status") == "firing" and a.get("labels", {}).get("severity") == "P1"]
                if not alerts:
                    continue
                names = sorted({a["labels"]["alertname"] for a in alerts})
                record("page_received", notification=notification, alertnames=names)
                code, ticket = http(18080, "/tickets", {"title": "Shop checkout incident, paged by " + ", ".join(names),
                    "description": "A checkout symptom alert reached the course pager. Investigation and mitigation are in progress.",
                    "reporter": {"name": "on-call"}, "impact": 1, "urgency": 1})
                assert code == 201 and ticket["priority"] == "P1", ticket
                current.update(ticket_id=ticket["id"], page=notification, created_at=ticket["created_at"])
                save(current)
                record("ticket_created", http_status=code, ticket=ticket)
                code, ticket = http(18080, "/tickets/" + ticket["id"] + "/ack", method="POST")
                assert code == 200 and ticket["state"] == "acknowledged", ticket
                current["acknowledged_at"] = ticket["acknowledged_at"]
                save(current)
                record("ticket_acknowledged", http_status=code, ticket=ticket)
                return
        if time.monotonic() - last_heartbeat >= 30:
            at, alerts = query('ALERTS{alertstate=~"pending|firing"}')
            record("waiting_for_page", evaluated_at=at, alerts=alerts, notifications=len(notifications))
            last_heartbeat = time.monotonic()
        time.sleep(5)
    raise TimeoutError("No P1 page within 20 minutes; inspect symptoms before proceeding.")


def flags():
    checked_status()
    _, response = http(18090, "/flags.json")
    values = response.get("flags", response)
    active = {key: value["defaultVariant"] for key, value in values.items()
              if key in POOL and value.get("defaultVariant") != "off"}
    record("flag_state_observed", active_flags=active, document=response)
    current = state()
    current["observed_flags"] = active
    save(current)


def off(flag):
    assert flag in POOL and checked_status()["armed"], flag
    code, response = http(18090, f"/flags/{flag}/off", method="POST")
    record("flag_disabled", flag=flag, http_status=code, response=response)


def wait_recovery():
    current = state()
    assert current.get("ticket_id") and checked_status()["armed"], current
    quiet_since = None
    last_status = None
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        at, active = query('ALERTS{alertstate="firing"}')
        _, fault = query("seeded_fault_active")
        is_off = len(fault) == 1 and float(fault[0]["value"][1]) == 0
        names = sorted(row["metric"].get("alertname", "") for row in active)
        status = (tuple(names), is_off)
        if status != last_status:
            record("recovery_observation", evaluated_at=at, firing_alerts=names, fault_inactive=is_off)
            last_status = status
        if not active and is_off:
            quiet_since = quiet_since or time.monotonic()
            if time.monotonic() - quiet_since >= 70:
                record("recovery_confirmed", quiet_for_seconds=round(time.monotonic() - quiet_since))
                return
        else:
            quiet_since = None
        time.sleep(10)
    raise TimeoutError("Recovery not confirmed; preserve the running playground and inspect it.")


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "arm": arm()
    elif command == "wait-page": wait_page()
    elif command == "flags": flags()
    elif command == "off": off(sys.argv[2])
    elif command == "wait-recovery": wait_recovery()
    elif command == "query":
        at, result = query(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        record("prometheus_query", expression=sys.argv[2], evaluated_at=at, result=result)
    else: raise ValueError(command)
