# TESTER drain run — PR 11 `vnstock-advisor-5-dev-analysis-engine` (branch `task/vnstock-advisor-5-dev-analysis-engine-dev`)

- **App:** vnstock-advisor | **DoD tier:** 3 (verification) | **Assignee:** _ready_
- **Goal:** Run the TESTER pass on PR 11 (analysis engine — indicators, screening, ranking over ingested data). DRAIN MODE (#160): no branch opened, no files written, verdict unblocks the queue. Oldest open PR (40.9h) — high drain priority.
- **Background:** M2 core service; builds on data-ingest contracts. Original task spec not on pod; branch `not-local`; contract = service surface + PR diff.

## Acceptance criteria

1. README-verbatim walkthrough of the analysis engine in a clean checkout succeeds.
2. All Test Plan scenarios executed; findings numbered (repro steps, expected vs actual, severity).
3. Mechanical verdict line `TESTER PASS` or `TESTER FAIL` (line-leading only).

## Implementation Plan (for the run — TESTER writes nothing)

- No code changes, no file writes, no branch creation. Read `ci-status/vnstock-advisor-5-dev-analysis-engine.md` first; `FAILURE` = finding, `PENDING` = wait/re-check, `NONE` = finding.
- Automated suite on GitHub Actions (#134); in-pod: README + exploratory poking.
- Never soften a verdict under freeze pressure (#155).

## Test Plan

1. **Clean-checkout boot** into `workspace/.checkouts/vnstock-advisor-5-dev-analysis-engine/`; README steps verbatim. Expected: engine runs (CLI/service per README).
2. **Happy path:** run indicators (MA/RSI/volume) and screening/ranking over the fixture/ingested data per README. Expected: sane outputs (bounded values, correct ordering for ranking), exit 0.
3. **Edge cases:** empty symbol list, missing history, malformed input, restart behavior. Expected: graceful errors, no crash/hang.
4. **Failure-path coverage** per ci-status; happy-path-only = coverage-gap finding.
5. **Docs match + disclaimer** on any suggestion surface.
6. Verdict line + findings.

**Report to PM at task end:** surface tested, verdict, findings count, status.
