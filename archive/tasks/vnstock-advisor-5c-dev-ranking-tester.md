# TESTER drain run — PR 15 `vnstock-advisor-5c-dev-ranking` (branch `task/vnstock-advisor-5c-dev-ranking-dev`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on PR 15 (ranking over analysis-engine output). DRAIN MODE (#160): no branch opened, no files written, verdict unblocks the queue.
- **Background:** M2 ranking surface; depends on analysis-engine contracts. Original task spec not on pod; branch `not-local`; contract = service surface + PR diff.

## Acceptance criteria

1. README-verbatim walkthrough of the ranking surface in a clean checkout succeeds.
2. All Test Plan scenarios executed; findings numbered (repro steps, expected vs actual, severity).
3. Mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-5c-dev-ranking.md` first; `FAILURE` = finding, `PENDING` = wait/re-check, `NONE` = finding.
- Automated suite on GitHub Actions (#134); in-pod: README + exploratory poking.
- Never soften a verdict under freeze pressure (#155).

## Test Plan

1. **Clean-checkout boot** into `workspace/.checkouts/vnstock-advisor-5c-dev-ranking/`; README steps verbatim. Expected: ranking runs.
2. **Happy path:** rank the fixture/ingested universe per README. Expected: deterministic ordering, bounded scores, exit 0.
3. **Edge cases:** empty universe, ties/equal scores, malformed input, restart. Expected: graceful, documented behavior.
4. **Failure-path coverage** per ci-status; happy-path-only = coverage-gap finding.
5. **Docs match + disclaimer** on any suggestion surface.
6. Verdict line + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
