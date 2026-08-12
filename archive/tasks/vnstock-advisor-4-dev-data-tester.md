# TESTER drain run — PR 13 `vnstock-advisor-4-dev-data` (branch `task/vnstock-advisor-4-dev-data-ingest`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification of an existing branch) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on open PR 13 (data-ingest work, branch `task/vnstock-advisor-4-dev-data-ingest`) so it can reach the merge gate. This is DRAIN MODE (#160) work: no branch is opened, nothing is written; the verdict unblocks the queue.
- **Background:** This PR is one of 6 open vs cap 3. Every open PR is a freeze contributor; a `TESTER PASS` here is one step toward merge count < 3. The original task spec file is not on this pod — the branch is `not-local`; treat the service surface (`services/data-ingest` per the app tree) and the PR diff as the contract.

## Acceptance criteria

1. README-verbatim walkthrough of the data-ingest service in a clean checkout (`workspace/.checkouts/<task-id>/`) succeeds — the service starts from the README alone.
2. Every scenario in the Test Plan below is executed; findings numbered with reproduction steps, expected vs actual, severity.
3. Output ends with the mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-4-dev-data.md` for the automated suite state; a `FAILURE` is a finding at missing-README severity, `PENDING` means wait/re-check (CI runs 2 jobs at a time — #135/#137), `NONE` is itself a finding.
- The full build+test matrix runs on GitHub Actions, not in-pod (#134). In-pod: README walkthrough + exploratory poking only.
- Never pass something you would otherwise no-go — priority is never a reason to soften the verdict (#155).

## Test Plan

1. **Clean-checkout boot:** `git clone`/worktree the branch into `workspace/.checkouts/vnstock-advisor-4-dev-data/`, execute the README's how-to-run EXACTLY as written. Expected: service starts; no invented steps needed.
2. **Happy path:** run the documented ingest command/endpoint against the documented source. Expected: data lands per README, exit 0.
3. **Edge cases:** empty/malformed input (missing symbol, empty payload, bad date), service restart behavior, repeated ingest (idempotency/duplicate handling). Expected: documented or graceful behavior, no crash/hang.
4. **Failure path coverage:** verify the suite (per ci-status) covers invalid-input and error paths, not just happy path — a happy-path-only suite is a coverage-gap finding.
5. **Docs match:** README/behavior consistency, disclaimer present on any suggestion surface.
6. Verdict line `TESTER PASS` / `TESTER FAIL` + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
