# ai-generated: 95% - AI implemented the published metric rules; student should review.
"""Pure DORA metric calculation and event-log validation for Laboratory 2."""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


class MetricInputError(ValueError):
    """Raised when a metrics request or event log violates the published contract."""


_RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")


def _instant(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not _RFC3339.fullmatch(value):
        raise MetricInputError(f"{field} must be an RFC 3339 instant")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        if parsed.utcoffset() is None:
            raise ValueError
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        raise MetricInputError(f"{field} must be an RFC 3339 instant") from None


def _required_string(event: dict[str, Any], name: str, *, nullable: bool = False) -> str | None:
    value = event.get(name)
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value:
        raise MetricInputError(f"{event.get('type')} event {name} must be a non-empty string")
    return value


def _string_list(event: dict[str, Any], name: str) -> list[str]:
    value = event.get(name)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise MetricInputError(f"{event.get('type')} event {name} must be an array of non-empty strings")
    return value


def _rounded_seconds(seconds: float | Decimal) -> int:
    result = int(Decimal(str(seconds)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return max(0, result)


def _median(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return _rounded_seconds(Decimal(ordered[middle - 1] + ordered[middle]) / 2)


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return float((Decimal(numerator) / Decimal(denominator)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def _validate(events: Any) -> list[dict[str, Any]]:
    if not isinstance(events, list):
        raise MetricInputError("events must be an array")
    unique: list[dict[str, Any]] = []
    seen_event_ids: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            raise MetricInputError("every event must be an object")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not 1 <= len(event_id) <= 64:
            raise MetricInputError("event_id must contain 1 to 64 characters")
        if event_id in seen_event_ids:
            continue
        seen_event_ids.add(event_id)
        event_type = event.get("type")
        if event_type not in ("commit", "deployment", "incident"):
            raise MetricInputError("event type must be commit, deployment or incident")
        _instant(event.get("at"), f"event {event_id} at")
        if event_type == "commit":
            _required_string(event, "sha")
            _required_string(event, "branch")
            revert = _required_string(event, "reverts", nullable=True)
            change_id = _required_string(event, "change_id", nullable=True)
            if (revert is None) != (change_id is not None):
                raise MetricInputError("commit change_id must be present exactly when reverts is null")
        elif event_type == "deployment":
            _required_string(event, "deployment_id")
            environment = _required_string(event, "environment")
            outcome = _required_string(event, "outcome")
            if outcome not in ("success", "failure"):
                raise MetricInputError("deployment outcome must be success or failure")
            _string_list(event, "commits")
            if type(event.get("unplanned")) is not bool:
                raise MetricInputError("deployment unplanned must be a boolean")
            _required_string(event, "caused_by", nullable=True)
        else:
            _required_string(event, "incident_id")
            if event.get("phase") not in ("opened", "resolved"):
                raise MetricInputError("incident phase must be opened or resolved")
            _string_list(event, "deployments")
        unique.append(event)

    commits = {event["sha"]: event for event in unique if event["type"] == "commit"}
    if len(commits) != sum(event["type"] == "commit" for event in unique):
        raise MetricInputError("commit sha values must be unique")
    deployments = {event["deployment_id"]: event for event in unique if event["type"] == "deployment"}
    if len(deployments) != sum(event["type"] == "deployment" for event in unique):
        raise MetricInputError("deployment_id values must be unique")
    incident_phases: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for event in unique:
        if event["type"] == "commit" and event["reverts"] is not None and event["reverts"] not in commits:
            raise MetricInputError(f"reverts names missing sha {event['reverts']}")
        if event["type"] == "deployment":
            for sha in event["commits"]:
                if sha not in commits:
                    raise MetricInputError(f"deployment references missing sha {sha}")
            if event["caused_by"] is not None and not any(
                item["type"] == "incident" and item["incident_id"] == event["caused_by"] for item in unique
            ):
                raise MetricInputError(f"caused_by names missing incident {event['caused_by']}")
        elif event["type"] == "incident":
            incident_phases[event["incident_id"]][event["phase"]] += 1
            for deployment_id in event["deployments"]:
                if deployment_id not in deployments:
                    raise MetricInputError(f"incident references missing deployment {deployment_id}")
    if any("resolved" in phases and "opened" not in phases for phases in incident_phases.values()):
        raise MetricInputError("every resolved incident must also be opened")
    if any(count > 1 for phases in incident_phases.values() for count in phases.values()):
        raise MetricInputError("an incident may carry at most one event per phase")

    resolved: dict[str, str] = {}
    for sha in commits:
        trail: set[str] = set()
        current = sha
        while commits[current]["reverts"] is not None:
            if current in trail:
                raise MetricInputError("revert chain contains a cycle")
            trail.add(current)
            current = commits[current]["reverts"]
        resolved[sha] = commits[current]["change_id"]
    if any(not change for change in resolved.values()):
        raise MetricInputError("commit revert chain does not resolve to a change")
    return unique


def calculate(body: Any) -> dict[str, Any]:
    if not isinstance(body, dict):
        raise MetricInputError("request body must be an object")
    window = body.get("window")
    if not isinstance(window, dict):
        raise MetricInputError("window must be an object")
    start = _instant(window.get("from"), "window.from")
    end = _instant(window.get("to"), "window.to")
    if end <= start:
        raise MetricInputError("window.to must be after window.from")
    events = _validate(body.get("events"))

    commits = {event["sha"]: event for event in events if event["type"] == "commit"}
    commit_times = {sha: _instant(event["at"], f"commit {sha} at") for sha, event in commits.items()}
    changes_for_sha: dict[str, str] = {}
    for sha in commits:
        chain: list[str] = []
        current = sha
        while commits[current]["reverts"] is not None:
            chain.append(current)
            current = commits[current]["reverts"]
        changes_for_sha[sha] = commits[current]["change_id"]

    earliest_change_commit: dict[str, datetime] = {}
    for sha, change in changes_for_sha.items():
        earliest_change_commit[change] = min(earliest_change_commit.get(change, commit_times[sha]), commit_times[sha])

    deployments = [event for event in events if event["type"] == "deployment" and event["environment"] == "production"]
    in_window = [event for event in deployments if start <= _instant(event["at"], "deployment.at") < end]
    successful = [event for event in in_window if event["outcome"] == "success"]
    failed = [event for event in in_window if event["outcome"] == "failure"]

    first_success: dict[str, datetime] = {}
    lead_pairs: list[int] = []
    negative_lead_pairs = 0
    pair_seen: set[str] = set()
    for deployment in sorted(successful, key=lambda d: (_instant(d["at"], "deployment.at"), d["deployment_id"])):
        deployed_at = _instant(deployment["at"], "deployment.at")
        for sha in deployment["commits"]:
            change = changes_for_sha[sha]
            first_success.setdefault(change, deployed_at)
            if sha in pair_seen:
                continue
            pair_seen.add(sha)
            seconds = Decimal(str((deployed_at - commit_times[sha]).total_seconds()))
            if seconds < 0:
                negative_lead_pairs += 1
            lead_pairs.append(_rounded_seconds(seconds))

    # Pair uniqueness is per SHA: a SHA is counted at its first successful production delivery.
    lead_time_pairs = len(lead_pairs)
    successful_changes = set(first_success)
    ground_truth_leads = [
        _rounded_seconds(Decimal(str((first_success[change] - earliest_change_commit[change]).total_seconds())))
        for change in successful_changes
    ]

    incident_events = [event for event in events if event["type"] == "incident"]
    incidents: dict[str, dict[str, Any]] = {}
    for incident_id in {event["incident_id"] for event in incident_events}:
        phases = [event for event in incident_events if event["incident_id"] == incident_id]
        opened = next((event for event in phases if event["phase"] == "opened"), None)
        if opened is None:
            continue
        resolved_event = next((event for event in phases if event["phase"] == "resolved"), None)
        incidents[incident_id] = {
            "opened": _instant(opened["at"], "incident.at"),
            "resolved": _instant(resolved_event["at"], "incident.at") if resolved_event else None,
            "deployments": set(opened["deployments"]),
        }

    recovery_values: list[int] = []
    open_failures = 0
    for deployment in failed:
        deployment_id = deployment["deployment_id"]
        covering = [inc for inc in incidents.values() if deployment_id in inc["deployments"]]
        covering_ids = [
            (incident_id, incident)
            for incident_id, incident in incidents.items()
            if deployment_id in incident["deployments"]
        ]
        if not covering_ids:
            open_failures += 1
            continue
        incident_id, incident = min(covering_ids, key=lambda pair: (pair[1]["opened"], pair[0].encode("utf-8")))
        if incident["resolved"] is None:
            open_failures += 1
        else:
            delta = Decimal(str((incident["resolved"] - _instant(deployment["at"], "deployment.at")).total_seconds()))
            recovery_values.append(_rounded_seconds(delta))

    overlap_pairs = 0
    incident_items = list(incidents.items())
    for index, (_, left) in enumerate(incident_items):
        left_end = left["resolved"] if left["resolved"] is not None else end
        for _, right in incident_items[index + 1 :]:
            right_end = right["resolved"] if right["resolved"] is not None else end
            if left["opened"] < right_end and right["opened"] < left_end:
                overlap_pairs += 1

    total = len(in_window)
    failures_count = len(failed)
    rework_count = sum(event["unplanned"] is True and event["caused_by"] is not None for event in in_window)
    no_commit_count = sum(not event["commits"] for event in in_window)
    deployed_shas = {
        sha for event in in_window for sha in event["commits"]
    }
    off_main = sum(commits[sha]["branch"] != "main" for sha in deployed_shas)
    window_seconds = Decimal(str((end - start).total_seconds()))
    frequency = float((Decimal(total) / (window_seconds / Decimal(86400))).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))

    return {
        "spec_version": "1.0.0",
        "window": {"from": body["window"]["from"], "to": body["window"]["to"]},
        "deployment_frequency_per_day": frequency,
        "change_lead_time_seconds_p50": _median(lead_pairs),
        "failed_deployment_recovery_time_seconds_p50": _median(recovery_values),
        "change_fail_rate": _ratio(failures_count, total),
        "deployment_rework_rate": _ratio(rework_count, total),
        "counts": {
            "deployments": total,
            "successful_deployments": len(successful),
            "failed_deployments": failures_count,
            "recovered_failures": len(recovery_values),
            "open_failures": open_failures,
            "rework_deployments": rework_count,
            "lead_time_pairs": lead_time_pairs,
            "changes": len(set(changes_for_sha.values())),
        },
        "anomalies": {
            "negative_lead_time_pairs": negative_lead_pairs,
            "deployments_without_commits": no_commit_count,
            "commits_never_on_main": off_main,
            "revert_chains_collapsed": sum(event["reverts"] is not None for event in commits.values()),
            "overlapping_incident_pairs": overlap_pairs,
        },
        "ground_truth": {
            "changes_delivered": len(successful_changes),
            "true_change_lead_time_seconds_p50": _median(ground_truth_leads),
        },
    }
