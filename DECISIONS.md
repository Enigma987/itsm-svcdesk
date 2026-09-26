---
svcdesk_decisions:
  C1: wallclock      # wallclock | business
  C2: immutable      # reopen | immutable
  C3: vip            # matrix | vip
---
<!-- ai-generated: 75% - AI drafted from the course contract and student-selected values; student should review and own the reasoning. -->

# Decisions

## C1 - SLA clock for P1

**Decision:** Both P1 acknowledgement and resolution targets use elapsed wall-clock time, including nights and weekends.

**Rejected alternative:** I reject pausing P1 targets outside the Europe/Warsaw business window.

**Reason:** A P1 is a work-stopping emergency; the desk needs the same response expectation at 17:00 Friday as during a weekday shift.

**Service owner:** The Service Desk product owner approves the priority-based service commitments and owns the effect on desk staffing.

**Customer outcome:** People affected by a P1 receive a clear continuous-time promise; the desk bears the after-hours coverage burden.

## C2 - Closed tickets and reopening

**Decision:** A resolved ticket can be reopened within seven days, but a closed ticket cannot be changed; a new ticket links through `related_to`.

**Rejected alternative:** I reject reopening closed tickets during the seven-day window after closure.

**Reason:** Closure marks the reporter-confirmed record as final, preserving audit history; a linked follow-up keeps the original closure intact.

**Service owner:** The Service Desk product owner owns ticket lifecycle policy and must keep reporting records stable after closure.

**Customer outcome:** The reporter can still reopen an unresolved fix before closure; after closure, the follow-up remains visible without rewriting history.

## C3 - VIP reporters and the priority matrix

**Decision:** Apply the impact/urgency matrix as written, then raise VIP P3 or P4 tickets to P2; VIP P1 and P2 tickets stay unchanged.

**Rejected alternative:** I reject allowing VIP identity to have no effect when the matrix gives P3 or P4.

**Reason:** VIP visibility is a deliberate service commitment, but a P2 floor limits its effect and preserves the matrix for the most urgent issues.

**Service owner:** The Service Desk product owner approves prioritization rules and balances executive visibility against operational capacity.

**Customer outcome:** VIP reporters' lower-impact issues become visible at P2, while ordinary reporters retain the published matrix priority.
