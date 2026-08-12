# TESTER drain run — PR 16 `vnstock-advisor-14-dev-data-ingest-security-gate` (branch `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification of a security-hardening follow-up) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on PR 16 (data-ingest security-gate hardening). DRAIN MODE (#160): no branch opened, no files written, verdict unblocks the queue.
- **Background:** Security-gate follow-up on the data-ingest service. It should merge AFTER the base data-ingest PR it hardens (PR 13/14) for a clean rebase; if the base merges first, run this immediately after. Original task spec not on pod; branch `not-local`.

## Acceptance criteria

1. README-verbatim walkthrough in a clean checkout succeeds (run steps unchanged by hardening — or the hardening's changelog documents any change).
2. All Test Plan scenarios executed; findings numbered (repro steps, expected vs actual, severity).
3. Mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-14-dev-data-ingest-security-gate.md` first; `FAILURE` = finding, `PENDING` = wait/re-check, `NONE` = finding.
- Automated suite on GitHub Actions (#134); in-pod: README + exploratory poking.
- Never soften a verdict under freeze pressure (#155).

## Test Plan

1. **Clean-checkout boot** into `workspace/.checkouts/vnstock-advisor-14-dev-data-ingest-security-gate/`; README steps verbatim. Expected: service starts.
2. **Happy path:** documented ingest flow still works after hardening (no behavioral regression).
3. **Edge cases:** invalid/empty input, restart, repeated ingest. Expected: graceful, no new crash paths introduced by the hardening.
4. **Failure-path coverage** per ci-status; happy-path-only = coverage-gap finding.
5. **Changelog/docs match** the shipped behavior (README run steps changed → README updated).
6. Verdict line + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
