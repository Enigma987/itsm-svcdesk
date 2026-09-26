# ai-generated: 90% - AI drafted implementation from the published API and checks; student should review.
"""HTTP API for the course service desk."""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

app = FastAPI()
WARSAW = ZoneInfo("Europe/Warsaw")
PRIORITIES = (
    ("P1", "P2", "P3"),
    ("P2", "P3", "P4"),
    ("P3", "P4", "P4"),
)
TARGETS = {"P1": (15, 4 * 60), "P2": (60, 8 * 60), "P3": (4 * 60, 24 * 60), "P4": (8 * 60, 72 * 60)}
DB_PATH = os.environ.get("SVCDESK_DB", "/data/svcdesk.db")


def connect() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
    return db


def error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def parse_now(value: str | None) -> datetime:
    if value and os.environ.get("SVCDESK_TEST_CLOCK", "").lower() in ("1", "true"):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("timestamp must include an offset")
            return parsed.astimezone(timezone.utc)
        except (ValueError, OverflowError):
            raise ValueError("X-Test-Clock must be an RFC 3339 instant") from None
    return datetime.now(timezone.utc)


def iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_stored(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def next_business_open(day):
    day += timedelta(days=1)
    while day.weekday() >= 5:
        day += timedelta(days=1)
    return datetime.combine(day, time(8, 0), WARSAW)


def add_business_minutes(created: datetime, minutes: int) -> datetime:
    local = created.astimezone(WARSAW)
    opening = datetime.combine(local.date(), time(8, 0), WARSAW)
    closing = datetime.combine(local.date(), time(16, 0), WARSAW)
    if local.weekday() >= 5 or local >= closing:
        local = next_business_open(local.date())
    elif local < opening:
        local = opening
    remaining = timedelta(minutes=minutes)
    while True:
        closing = datetime.combine(local.date(), time(16, 0), WARSAW)
        available = closing - local
        if remaining <= available:
            return (local + remaining).astimezone(timezone.utc)
        remaining -= available
        local = next_business_open(local.date())


def priority_for(impact: int, urgency: int, vip: bool) -> str:
    priority = PRIORITIES[impact - 1][urgency - 1]
    if vip and priority in ("P3", "P4"):
        return "P2"
    return priority


def due_instants(ticket: dict[str, Any]) -> tuple[datetime, datetime]:
    ack_minutes, resolve_minutes = TARGETS[ticket["priority"]]
    created = parse_stored(ticket["created_at"])
    if ticket["priority"] == "P1":
        return created + timedelta(minutes=ack_minutes), created + timedelta(minutes=resolve_minutes)
    return add_business_minutes(created, ack_minutes), add_business_minutes(created, resolve_minutes)


def public_ticket(ticket: dict[str, Any]) -> dict[str, Any]:
    ack_due, resolve_due = due_instants(ticket)
    return {
        **ticket,
        "sla": {"ack_due_at": iso(ack_due), "resolve_due_at": iso(resolve_due)},
    }


def load_ticket(ticket_id: str) -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT data FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return json.loads(row["data"]) if row else None


def save_ticket(ticket: dict[str, Any]) -> None:
    with connect() as db:
        db.execute(
            "INSERT INTO tickets (id, data) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
            (ticket["id"], json.dumps(ticket, separators=(",", ":"))),
        )


@app.get("/health")
def health():
    return {"status": "ok", "service": "svcdesk"}


@app.post("/tickets")
async def create_ticket(request: Request, x_test_clock: str | None = Header(default=None)):
    try:
        now = parse_now(x_test_clock)
    except ValueError as exc:
        return error(400, "invalid_clock", str(exc))
    try:
        body = await request.json()
    except Exception:
        return error(400, "validation", "request body must be JSON")
    if not isinstance(body, dict):
        return error(400, "validation", "request body must be an object")
    title = body.get("title")
    reporter = body.get("reporter")
    if not isinstance(title, str) or not 1 <= len(title) <= 200:
        return error(422, "validation", "title must contain 1 to 200 characters")
    description = body.get("description", "")
    if not isinstance(description, str) or len(description) > 4000:
        return error(422, "validation", "description must be a string of at most 4000 characters")
    if not isinstance(reporter, dict):
        return error(422, "validation", "reporter is required")
    name = reporter.get("name")
    if not isinstance(name, str) or not 1 <= len(name) <= 100:
        return error(422, "validation", "reporter.name must contain 1 to 100 characters")
    email = reporter.get("email")
    if email is not None and not isinstance(email, str):
        return error(422, "validation", "reporter.email must be a string or null")
    vip = reporter.get("vip", False)
    if not isinstance(vip, bool):
        return error(422, "validation", "reporter.vip must be a boolean")
    impact, urgency = body.get("impact"), body.get("urgency")
    if type(impact) is not int or impact not in (1, 2, 3):
        return error(422, "validation", "impact must be an integer from 1 to 3")
    if type(urgency) is not int or urgency not in (1, 2, 3):
        return error(422, "validation", "urgency must be an integer from 1 to 3")
    related_to = body.get("related_to")
    if related_to is not None and not isinstance(related_to, str):
        return error(422, "validation", "related_to must be a string or null")
    ticket = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "reporter": {"name": name, "email": email, "vip": vip},
        "impact": impact,
        "urgency": urgency,
        "priority": priority_for(impact, urgency, vip),
        "state": "new",
        "created_at": iso(now),
        "acknowledged_at": None,
        "resolved_at": None,
        "closed_at": None,
        "related_to": related_to,
    }
    save_ticket(ticket)
    return JSONResponse(status_code=201, content=public_ticket(ticket))


@app.get("/tickets")
def list_tickets(state: str | None = None, priority: str | None = None):
    with connect() as db:
        rows = db.execute("SELECT data FROM tickets").fetchall()
    tickets = [json.loads(row["data"]) for row in rows]
    return [public_ticket(t) for t in tickets if (state is None or t["state"] == state) and (priority is None or t["priority"] == priority)]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = load_ticket(ticket_id)
    return public_ticket(ticket) if ticket else error(404, "not_found", "ticket not found")


@app.get("/tickets/{ticket_id}/sla")
def get_sla(ticket_id: str, x_test_clock: str | None = Header(default=None)):
    try:
        now = parse_now(x_test_clock)
    except ValueError as exc:
        return error(400, "invalid_clock", str(exc))
    ticket = load_ticket(ticket_id)
    if ticket is None:
        return error(404, "not_found", "ticket not found")
    ack_due, resolve_due = due_instants(ticket)
    acknowledged = parse_stored(ticket["acknowledged_at"])
    resolved = parse_stored(ticket["resolved_at"])
    closed = ticket["state"] == "closed"
    open_ticket = ticket["state"] not in ("resolved", "closed")
    business_clock = ticket["priority"] != "P1"
    local = now.astimezone(WARSAW)
    in_hours = local.weekday() < 5 and time(8, 0) <= local.timetz().replace(tzinfo=None) < time(16, 0)
    return {
        "priority": ticket["priority"],
        "ack_due_at": iso(ack_due),
        "resolve_due_at": iso(resolve_due),
        "ack_breached": (acknowledged > ack_due) if acknowledged else now > ack_due,
        "resolve_breached": (resolved > resolve_due) if resolved else now > resolve_due,
        "paused": bool(open_ticket and business_clock and not in_hours),
    }


@app.post("/tickets/{ticket_id}/{action}")
def transition(ticket_id: str, action: str, x_test_clock: str | None = Header(default=None)):
    if action not in ("ack", "start", "resolve", "close", "reopen"):
        return error(404, "not_found", "route not found")
    try:
        now = parse_now(x_test_clock)
    except ValueError as exc:
        return error(400, "invalid_clock", str(exc))
    ticket = load_ticket(ticket_id)
    if ticket is None:
        return error(404, "not_found", "ticket not found")
    state = ticket["state"]
    allowed = {
        "ack": state == "new",
        "start": state == "acknowledged",
        "resolve": state == "in_progress",
        "close": state == "resolved",
        "reopen": state == "resolved" and now <= parse_stored(ticket["resolved_at"]) + timedelta(days=7),
    }
    if action == "reopen" and state == "closed":
        return error(409, "ticket_closed", "closed tickets are immutable")
    if not allowed[action]:
        return error(409, "invalid_transition", "action is not allowed from the current state")
    if action == "ack":
        ticket["state"] = "acknowledged"
        ticket["acknowledged_at"] = iso(now)
    elif action == "start":
        ticket["state"] = "in_progress"
    elif action == "resolve":
        ticket["state"] = "resolved"
        ticket["resolved_at"] = iso(now)
    elif action == "close":
        ticket["state"] = "closed"
        ticket["closed_at"] = iso(now)
    else:
        ticket["state"] = "in_progress"
        ticket["resolved_at"] = None
        ticket["closed_at"] = None
    save_ticket(ticket)
    return public_ticket(ticket)
