# PM — M3 analytics plan (vnstock-advisor)

- **App:** vnstock-advisor | **DoD tier:** 2 (feature — Tier 2 DoD includes analytics update) | **Assignee:** _ready_
- **Goal:** Produce the M3 analytics plan (PM keeps the analytics plan, §7.2 Tier 2). Claimable during the freeze by PM: no branch, no code.
- **Background:** M3 (suggestion API + web UI) is the first user-facing surface of the flagship — the analytics plan must be ready so the services instrument as they're built (Tier-2 DoD gate), not retrofitted after merge.

## Acceptance criteria

1. Events defined for the M3 surfaces: suggestions served (API), suggestion detail viewed (UI), disclaimer rendered/exposed, error responses; each with trigger + payload sketch.
2. Mapping to the service that owns each event (suggestion-api vs web-ui) so DEV tasks carry their instrumentation slice.
3. Metrics definitions are testable — QA can verify an event fires on the described action.
4. Recorded in the task output (no new file — PM owns no analytics file; the plan lives in this task's output and the M3 DEV task specs).

## Implementation Plan (for PM)

- Load `observability-and-instrumentation` skill for event/metric definitions.
- Ground events in the M3 use cases (BA produces them this cycle — coordinate; if not ready, derive from the flagship framing in `tasks/idea-backlog.md` rank 3 + M2 contracts).
- Write the plan into this task's output; embed the per-service instrumentation slice into the M3 DEV task specs when the freeze lifts.

## Test Plan (for QA validation)

1. Every M3 user-visible surface has at least one defined event (no surface un-instrumented).
2. Each event is triggerable and verifiable — QA can name the action that fires it and the expected payload.
3. Instrumentation doesn't break the security posture (no PII/sensitive data in events).

**Report to CEO at task end:** analytics plan delivered, task status.
