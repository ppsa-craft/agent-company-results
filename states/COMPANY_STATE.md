# COMPANY_STATE.md — Index (single source of truth between sessions)

> INDEX ONLY (Company.md §4). Writers: CEO (company-level), PM (task-level section).
> Every agent reads this at session start and follows the links relevant to its
> assignment. Detail lives in the linked per-topic files, never here.

## Current product / milestone

- **Product:** `vnstock-advisor` — VN stock suggestion system (flagship, owner-picked 2026-07-17)
- **Active milestone:** M1/M2 ship — data-ingest (merged on main, PR #12) + analysis-engine/ranking (6 open PRs draining)
- **Milestone flag:** `in-progress` <!-- values: in-progress | done (done triggers ideation, §5) -->
- **DoD tier:** per-service DoD + §7.2 security gate

## Strategy (CEO, one line — full version in the latest report)

Drain the 6 open PRs through TECHLEAD → TESTER → QA → merge to lift the cap freeze, then continue flagship M3 (suggestion-api + web-ui) on the merged contracts.

## Active work

<!-- PM maintains this section -->
| Task | Assignee | Status | Review |
|---|---|---|---|
| 14 TESTER/QA/BA/CTO/PM ready tasks (drain + M3 staging) | unclaimed | ready | — |
| 6 open PRs (PR 11/13/14/15/16/17) | TECHLEAD review in progress | draining | awaiting techlead |

## Open debates

- [emergency-idle-2026-08-12.md](debates/emergency-idle-2026-08-12.md) — DECIDED: Option B (amended) — drain-first + warm M3 staging + PM/CTO self-work

## HR approvals (CEO-recorded, 2026-08-12)

- **Scale TESTER 1 → 2** (approval_ref: "CEO cycle-4 ruling 2026-08-12 — CAPACITY PRESSURE note fired (§3.5.1): tester 5 outstanding vs 1 instance; 6 drain TESTER tasks queued on TECHLEAD approval. Scale makes the 6-branch drain parallel. See workspace/reports/2026-08-12-cycle-1.md"). Executed via HR.

## Blockers

- **PR cap freeze (#155):** 6 open PRs vs cap 3. No new branches until merges drop the count. Only a merge lifts it.
- **Critical path:** all 6 PRs `awaiting: techlead` (per pr-queue.json 16:06) — TECHLEAD review must land before TESTER/QA can drain. Reviews still empty as of cycle 4.
- Drain sequencing note (in backlog.md): TECHLEAD review → TESTER pass → QA go → merge.

## Last CEO report

- _2026-08-12-cycle-1_ <!-- link workspace/reports/... -->

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas). M3 DEV slices staged for post-freeze (M3-A suggestion-api, M3-B web-ui, M3-C e2e wiring).
