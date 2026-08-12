# QA ship gate — data-ingest service (PRs 13, 14, 16)

- **App:** vnstock-advisor | **DoD tier:** 3 (gate an existing service) | **Assignee:** _ready_
- **Goal:** Run the QA ship gate per branch for the data-ingest service's open PRs — 13 (`vnstock-advisor-4-dev-data`), 14 (`vnstock-advisor-4-dev-data-ingest`), 16 (`vnstock-advisor-14-dev-data-ingest-security-gate`) — so they reach the merge gate. DRAIN MODE (#160): QA is one of the two agents who can actually unblock the company; no branch opened, nothing written.
- **Background:** All 6 open PRs vs cap 3 are queued. QA dispatch is per-branch mechanical (#161) — this task covers the data-ingest service's branches so the drain order is explicit. The security-gate PR (16) also needs the security-gate checks run on the hardening it introduces.

## Acceptance criteria

1. DoD tier validated for each branch (escalate mislabeled tiers).
2. Ship gate per branch: artifact set complete, automated suite exists + runnable via one documented command + covers BOTH good and failure flows, TESTER pass recorded, CTO stack record best practices met.
3. Security gate (§7.2.1) per branch — data-ingest surface: secret-scan clean, SCA+SBOM clean of known-exploitable CVEs, SAST clean of high/critical, no dependency confusion; API-surface checks per OWASP API Top 10 as applicable; verify any `apps/vnstock-advisor/docs/security-review.md` findings are fixed or low-sev-accepted with rationale. Any unresolved high/critical = security NO-GO.
4. Mechanical verdict per branch, line-leading: `QA GO` / `QA NO-GO`, numbered findings.

## Implementation Plan (QA writes nothing)

- Load `code-review-and-quality` + `security-and-hardening` / SAST / secret-scanning / SCA skill paths per AGENTS.md routing for the surface.
- Read each branch's `reviews/<task-id>.md` record (TECHLEAD APPROVED + TESTER PASS) — do not re-run TESTER's suite or re-litigate its verdict (#161); gate what it leaves.
- Automated suite runs on GitHub Actions (#134); read `ci-status/<task-id>.md` for the authoritative pass/fail. `FAILURE`/`NONE` = no-go input.
- Never soften a verdict under freeze pressure (#155); a NO-GO during a freeze is still a NO-GO.

## Test Plan (ship-gate checklist per branch)

1. Verify the three merge-gate sign-offs' preconditions: TECHLEAD `APPROVED` + `TESTER PASS` recorded; if either is missing, do NOT gate yet — report "waiting on X" as the verdict-input status.
2. Validate tier, artifact completeness, README-runnable suite, good+failure-flow coverage.
3. Run security-gate checks for the data-ingest surface.
4. Output per-branch `QA GO` / `QA NO-GO` with numbered findings + tier rulings.

**Report to PM at task end:** gates run per branch, verdicts, findings, status.
