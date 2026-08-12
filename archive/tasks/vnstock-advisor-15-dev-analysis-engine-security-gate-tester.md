# TESTER drain run — PR 17 `vnstock-advisor-15-dev-analysis-engine-security-gate` (branch `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification of a security-hardening follow-up) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on PR 17 (analysis-engine security-gate hardening). DRAIN MODE (#160): no branch opened, no files written, verdict unblocks the queue.
- **Background:** Security-gate follow-up on the analysis engine; merge AFTER the base analysis-engine PR (11) for a clean rebase. Original task spec not on pod; branch `not-local`.

## Acceptance criteria

1. README-verbatim walkthrough in a clean checkout succeeds (or changelog documents changed run steps).
2. All Test Plan scenarios executed; findings numbered (repro steps, expected vs actual, severity).
3. Mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-15-dev-analysis-engine-security-gate.md` first; `FAILURE` = finding, `PENDING` = wait/re-check, `NONE` = finding.
- Automated suite on GitHub Actions (#134); in-pod: README + exploratory poking.
- Never soften a verdict under freeze pressure (#155).

## Test Plan

1. **Clean-checkout boot** into `workspace/.checkouts/vnstock-advisor-15-dev-analysis-engine-security-gate/`; README steps verbatim. Expected: engine runs.
2. **Happy path:** indicators/screening/ranking still produce sane outputs after hardening (no behavioral regression).
3. **Edge cases:** empty input, malformed history, restart. Expected: graceful, no new crash paths.
4. **Failure-path coverage** per ci-status; happy-path-only = coverage-gap finding.
5. **Changelog/docs match** shipped behavior.
6. Verdict line + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
