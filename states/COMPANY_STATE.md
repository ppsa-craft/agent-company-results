# COMPANY_STATE.md — Index (single source of truth between sessions)

> INDEX ONLY (Company.md §4). Writers: CEO (company-level), PM (task-level section).
> Every agent reads this at session start and follows the links relevant to its
> assignment. Detail lives in the linked per-topic files, never here.

## Current product / milestone

- **Product:** `vnstock-advisor` (VN stock suggestion system)
- **Active milestone:** M1 + M2 parallel start — foundation (repo scaffold + data-ingest) + analysis-engine
- **Milestone flag:** `in-progress` <!-- values: in-progress | done (done triggers ideation, §5) -->
- **DoD tier:** 2 (Feature)

## Strategy (CEO, one line — full version in the latest report)

Build the VN stock suggestion system as flagship: parallelize M1 (data-ingest) and M2 (analysis-engine) from day one via clean service seams; each service independently buildable, quality-gated, security-gated; M3 (API+UI) follows. Reuse potential drives architecture — shared scaffold, ingest service, and analysis engine become reusable assets.

## Active work

<!-- PM maintains this section -->
| Task | Assignee | Status | Review |
|---|---|---|---|
| vnstock-advisor-1-repo-scaffold | DEV-1 | done | |
| vnstock-advisor-2-ba-data-ingest | BA-1 | done | |
| vnstock-advisor-3-ba-analysis-engine | BA-1 | done | |
| vnstock-advisor-4-dev-data-ingest | DEV-1 | done | |
| vnstock-advisor-5-dev-analysis-engine (umbrella, OPEN) | DEV | in-progress (split 5a/5b/5c) | |
| vnstock-advisor-5a-dev-indicators | dev | in-progress | |
| vnstock-advisor-5b-dev-screening | — | ready (dep 5a) | |
| vnstock-advisor-5c-dev-ranking | — | ready (dep 5a,5b) | |
| vnstock-advisor-6-tester-data-ingest | TESTER-1 | ready | |
| vnstock-advisor-7-tester-analysis-engine | TESTER-2 | ready | |
| vnstock-advisor-8-qa-data-ingest | QA-1 | ready | |
| vnstock-advisor-9-qa-analysis-engine | QA-2 | ready | |
| vnstock-advisor-11-ba-suggestion-api | BA-2 (pending) | ready | |
| vnstock-advisor-12-ba-web-ui | BA-2 (pending) | ready | |

## Open debates

- [emergency-idle-2026-07-31](debates/emergency-idle-2026-07-31.md) — **DECIDED: Option D (Parallel M1 + M2 start)**

## Blockers

- None

## Last CEO report

- [Cycle 25 report](workspace/reports/2026-08-02-cycle-25.md)

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas).

## Delegation violations (owner 2026-07-12)

| Violation ID | Out-of-chain delegation | Timestamp | Status |
|---|---|---|---|
| DELEGVIOL-001 | CTO→PM direct (bypass TECHLEAD) | 2026-07-31 | **FIXED** |
| DELEGVIOL-002 | CEO→DEV direct (bypass CTO/TECHLEAD) | 2026-07-31 | **FIXED** |
| DELEGVIOL-003 | PM→DEV claimed tasks without review record | 2026-07-31 | **FIXED** |
| DELEGVIOL-004 | CEO→CTO direct delegation chain intact but TECHLEAD not current on open PRs | 2026-08-01 | **FIXED** |
| DELEGVIOL-005 | CEO→PM direct bypassing CTO for critical path decisions | 2026-08-01 | **FIXED** |

**Current Status:** All delegation violations have been addressed through:
- Delegation chain enforcement validation for all PM task claims
- Automatic TECHLEAD orchestration dispatch for all open PRs
- Removal of out-of-chain delegations
- Clear enforcement of CEO → CTO → PM → {DEV, TESTER, QA, BA} chain

**Active Ready Tasks Staged:**
- [DEV] vnstock-advisor-5a-dev-indicators.md — status: ready
- [DEV] vnstock-advisor-5b-dev-screening.md — status: ready
- [DEV] vnstock-advisor-5c-dev-ranking.md — status: ready
- [TESTER] vnstock-advisor-8-tester-analysis-engine.md — status: ready
- [QA] vnstock-advisor-8-qa-data-ingest.md — status: ready
- [QA] vnstock-advisor-9-qa-analysis-engine.md — status: ready
- [BA] vnstock-advisor-11-ba-suggestion-api.md — status: ready (awaiting BA-2 activation)
- [BA] vnstock-advisor-12-ba-web-ui.md — status: ready (awaiting BA-2 activation)
