<!-- ai-generated: 90% - AI drafted this specification from the course contract; student must review and own the decisions. -->
# svcdesk service specification

## Purpose and scope

Build a small HTTP service desk API for creating and tracking incidents, computing their priority, and reporting acknowledgement and resolution service levels. This specification is derived from Laboratory1/REQUIREMENTS.md (R-01–R-25), API.md, and CHECKS.md. The HTTP contract in API.md controls where it is more precise than a requirement. The service listens on port 8080, accepts and returns JSON, and provides no other interface (R-01).

## API behavior

`GET /health` returns HTTP 200 and `{"status":"ok","service":"svcdesk"}`. `POST /tickets` validates and creates a ticket, returning 201 and its full representation. `GET /tickets` returns all matching tickets in one array, optionally filtered by exact `state` and `priority`. `GET /tickets/{id}` and `GET /tickets/{id}/sla` return the ticket and SLA respectively. Unknown paths and ticket identifiers return JSON 404 responses. Successful state actions return the updated ticket; invalid actions return 409 with a top-level `error` object (R-02, R-08, R-19, R-25).

A ticket has a service-generated opaque non-empty unique ID; required title (1–200 characters), reporter name (1–100 characters), integer impact and urgency (each 1–3); optional description (default empty, at most 4000 characters), reporter email (default null), VIP flag (default false), and `related_to` (default null). The service stores creation and transition timestamps as RFC 3339 instants and emits UTC timestamps ending in `Z`. Priority, state, timestamps, ID, and SLA are service-owned. Client values for those fields and unknown request fields are ignored (R-03, R-17, R-18, R-20).

Priority comes from the impact/urgency matrix: rows for impact 1, 2, 3 are respectively `[P1,P2,P3]`, `[P2,P3,P4]`, and `[P3,P4,P4]` for urgency 1, 2, 3. The selected VIP rule is C3=`vip`: after applying the matrix, raise VIP priorities P3 and P4 to P2; preserve P1 and P2. The client cannot set priority (R-04–R-06; CHECKS L1-CORE-2.07–2.15, 2.46–2.48).

Invalid required fields, lengths, types, impact, urgency, or test-clock values return 400 or 422 with a JSON `error` object. When `SVCDESK_TEST_CLOCK` is `1` or `true`, a valid `X-Test-Clock` RFC 3339 value supplies `now` for that request only; otherwise use real UTC time. A malformed test clock is a client error (R-20, R-21).

## State and timestamp rules

Allowed actions are `new` → acknowledge → `acknowledged` → start → `in_progress` → resolve → `resolved` → close → `closed`. Acknowledge, resolve, and close record their respective event times. Reopening a resolved ticket within seven days of its resolution returns it to `in_progress` and clears its resolved timestamp; closure time is absent because it was not closed. The selected closed-ticket rule is C2=`immutable`: reopening a closed ticket always returns 409, including inside seven days. A new ticket may refer to the closed ticket through `related_to`. Reopening after the seven-day window and every other invalid transition return 409. Unknown IDs return 404 (R-07–R-11; CHECKS L1-CORE-2.25–2.35).

## SLA rules and decisions

Targets from creation are P1: 15 minutes / 4 hours; P2: 1 hour / 8 hours; P3: 4 hours / 24 hours; P4: 8 hours / 72 hours (acknowledgement / resolution). The selected clock rule is C1=`wallclock`: both P1 targets use elapsed wall time, including outside business hours. P2–P4 targets count business time Monday–Friday, 08:00–16:00 Europe/Warsaw, with DST handled by that time zone; Polish public holidays count as business days. Targets starting outside business hours begin at the next opening, and a target ending exactly at 16:00 is due at that closing instant. These rules determine the due instants returned in the ticket SLA block (R-12–R-15; CHECKS L1-CORE-2.36–2.41).

`GET /tickets/{id}/sla` reports priority, both due instants, `ack_breached`, `resolve_breached`, and `paused`. A target is breached only when its event occurred strictly after its due instant, or the event has not happened and now is strictly after the due instant. Acknowledgement and resolution exactly at due time are on time. A reopened ticket is unresolved again against its original resolution target. `paused` is true only while the ticket is open, its resolution clock is business-hours based, and now is outside business hours; it is always false for wall-clock P1 targets (R-16).

## Persistence and deployment

Tickets survive a service-container restart. Docker Compose builds the service from this repository, exposes port 8080, sets `SVCDESK_TEST_CLOCK`, uses persistent named storage, uses no host-path bind mounts, and requires no network after image build. `docker compose up` makes `/health` ready within 120 seconds (R-22–R-24).

## Decision record for implementation

The specification intentionally chooses one of each pair of admissible behaviors already declared in the repository's `DECISIONS.md`: C1=`wallclock`, C2=`immutable`, C3=`vip`. The matching checker observations are P1 Friday-after-hours due instants in L1-CORE-2.41, 409 reopening a recently closed ticket in L1-CORE-2.35, and P2 for a low-matrix-priority VIP ticket in L1-CORE-2.46. The remaining published checks exercise shared behavior and do not change these choices. These choices must be defended in the final decision artifact and the running service must exhibit them.
