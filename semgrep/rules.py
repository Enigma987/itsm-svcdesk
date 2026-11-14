# ai-generated: 100% - Codex wrote positive and negative Semgrep fixtures for svcdesk's two audit guards.
import os


def test_clock_enabled():
    # ruleid: svcdesk-test-clock-switch
    return os.environ.get("SVCDESK_TEST_CLOCK", "").lower() in ("1", "true")


def test_clock_with_another_default():
    # ruleid: svcdesk-test-clock-switch
    return os.environ.get("SVCDESK_TEST_CLOCK", "0")


def ordinary_configuration():
    # ok: svcdesk-test-clock-switch
    return os.environ.get("SVCDESK_DB", "/data/svcdesk.db")


def fixed_clock_configuration():
    # ok: svcdesk-test-clock-switch
    return {"SVCDESK_TEST_CLOCK": "0"}


def read_ticket_export(connection):
    # ruleid: svcdesk-bulk-ticket-read
    return connection.execute("SELECT data FROM tickets").fetchall()


def read_single_ticket(connection, ticket_id):
    # ok: svcdesk-bulk-ticket-read
    return connection.execute("SELECT data FROM tickets WHERE id = ?", (ticket_id,)).fetchone()


def count_tickets(connection):
    # ok: svcdesk-bulk-ticket-read
    return connection.execute("SELECT COUNT(*) FROM tickets").fetchall()


def read_other_table(connection):
    # ok: svcdesk-bulk-ticket-read
    return connection.execute("SELECT data FROM settings").fetchall()
