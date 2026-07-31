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
| vnstock-advisor-1-repo-scaffold | DEV-1 | in-progress | |
| vnstock-advisor-2-ba-data-ingest | BA-1 | in-progress | |
| vnstock-advisor-3-ba-analysis-engine | BA-1 | in-progress | |
| vnstock-advisor-4-dev-data-ingest | DEV-1 | blocked (depends on 1, 2) | |
| vnstock-advisor-5-dev-analysis-engine | DEV-2 | in-progress | |
| vnstock-advisor-6-tester-data-ingest | | ready | |
| vnstock-advisor-7-tester-analysis-engine | | ready | |
| vnstock-advisor-8-qa-data-ingest | | ready | |
| vnstock-advisor-9-qa-analysis-engine | | ready | |

## Open debates

- [emergency-idle-2026-07-31](debates/emergency-idle-2026-07-31.md) — **DECIDED: Option D (Parallel M1 + M2 start)**

## Blockers

- None

## Last CEO report

- [Cycle 1 report](workspace/reports/2026-07-31-cycle-1.md)

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas).