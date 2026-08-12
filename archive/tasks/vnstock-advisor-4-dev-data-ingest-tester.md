# TESTER drain run — PR 14 `vnstock-advisor-4-dev-data-ingest` (branch `task/vnstock-advisor-4-dev-data-ingest-dev`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on open PR 14 (data-ingest service). DRAIN MODE (#160): no branch opened, no files written, verdict unblocks the queue toward merge count < 3.
- **Background:** PR 14 is a sibling of PR 13 (both data-ingest, different branches). If TECHLEAD/orchestrator confirms they are duplicates, one may be closed as superseded — but this task's pass runs regardless for whichever stays open. Original task spec not on pod; branch is `not-local`; contract = service surface + PR diff.

## Acceptance criteria

1. README-verbatim walkthrough of the data-ingest service in a clean checkout succeeds.
2. All Test Plan scenarios executed; findings numbered (repro steps, expected vs actual, severity).
3. Mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-4-dev-data-ingest.md` first; `FAILURE` = finding at missing-README severity, `PENDING` = wait/re-check (#135/#137), `NONE` = finding.
- Automated suite runs on GitHub Actions (#134); in-pod is README walkthrough + exploratory poking only.
- Never soften a verdict under freeze pressure (#155).

## Test Plan

1. **Clean-checkout boot** into `workspace/.checkouts/vnstock-advisor-4-dev-data-ingest/`; README steps verbatim. Expected: service starts.
2. **Happy path:** documented ingest command/endpoint. Expected: data lands per README, exit 0.
3. **Edge cases:** empty/malformed input, restart behavior, repeated ingest idempotency. Expected: graceful, documented behavior.
4. **Failure-path coverage** of the automated suite per ci-status — happy-path-only = coverage-gap finding.
5. **Docs match + disclaimer** on any suggestion surface.
6. Verdict line + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
