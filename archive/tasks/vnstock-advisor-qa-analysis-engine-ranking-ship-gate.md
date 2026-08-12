# QA ship gate — analysis-engine + ranking services (PRs 11, 17, 15)

- **App:** vnstock-advisor | **DoD tier:** 3 (gate existing services) | **Assignee:** _ready_
- **Goal:** Run the QA ship gate per branch for the analysis-engine service's PRs — 11 (`vnstock-advisor-5-dev-analysis-engine`), 17 (`vnstock-advisor-15-dev-analysis-engine-security-gate`) — and the ranking service's PR 15 (`vnstock-advisor-5c-dev-ranking`). DRAIN MODE (#160): no branch opened, nothing written.
- **Background:** All 6 open PRs vs cap 3 are queued. QA dispatch is per-branch mechanical (#161); this task makes the drain order explicit for M2 services. Security-gate PR 17 gets the security-gate checks on its hardening.

## Acceptance criteria

1. DoD tier validated per branch (escalate mislabeled tiers).
2. Ship gate per branch: artifact set complete, automated suite exists + runnable via one documented command + covers BOTH good and failure flows, TESTER pass recorded, CTO stack record best practices met.
3. Security gate (§7.2.1) per branch — analysis/ranking surface: secret-scan clean, SCA+SBOM clean, SAST clean of high/critical, no dependency confusion; API-surface checks as applicable; verify `apps/vnstock-advisor/docs/security-review.md` findings fixed or low-sev-accepted with rationale. Any unresolved high/critical = security NO-GO.
4. Mechanical verdict per branch, line-leading: `QA GO` / `QA NO-GO`, numbered findings.

## Implementation Plan (QA writes nothing)

- Load `code-review-and-quality` + security skill paths per AGENTS.md routing for the surface.
- Read each branch's `reviews/<task-id>.md` record (TECHLEAD APPROVED + TESTER PASS) — gate what it leaves; do not re-run TESTER's suite (#161).
- Automated suite on GitHub Actions (#134); read `ci-status/<task-id>.md`. `FAILURE`/`NONE` = no-go input.
- Never soften a verdict under freeze pressure (#155).

## Test Plan (ship-gate checklist per branch)

1. Verify preconditions per branch: TECHLEAD `APPROVED` + `TESTER PASS` recorded; missing sign-off = do not gate yet, report "waiting on X".
2. Validate tier, artifacts, README-runnable suite, good+failure-flow coverage (ranking: ties/empty universe covered).
3. Run security-gate checks for the analysis/ranking surface.
4. Output per-branch `QA GO` / `QA NO-GO` with numbered findings + tier rulings.

**Report to PM at task end:** gates run per branch, verdicts, findings, status.
