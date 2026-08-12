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

Close the 4 superseded PRs (11/13/14/15) and merge the 2 canonical PRs (16, 17) to lift the cap freeze, then continue flagship M3 (suggestion-api + web-ui) on the merged contracts.

## Active work

<!-- PM maintains this section -->
| Task | Assignee | Status | Review |
|---|---|---|---|
| PR 17 merge (vnstock-advisor-15-dev-analysis-engine-security-gate, merge-ready) | orchestrator | merge-ready | TECHLEAD APPROVED + TESTER PASS + QA GO all on record → orchestrator merges next (CI re-checked mechanically at merge) |
| PR 16 DEV fix (vnstock-advisor-14-dev-data-ingest-security-gate-fix, drain-critical) | _ready_ | ready | TESTER FAIL F1/F2 on record → DEV fix, then TESTER re-run, then QA GO |
| M3 staging (BA use cases + disclaimer doc, CTO stack record, PM analytics plan) | BA/CTO/PM | done (freeze-safe, debate-ready) | §5.1 debate before M3 build |
| QA ship gates (both services) | QA | PR 17 = QA GO (merge-ready); PR 16 not gated (DEV fix + TESTER re-run pending) | re-dispatch after PR 16 TESTER re-run |
| json-formatter audit fix (audit-json-formatter) | _ready_ | ready (blocked on cap freeze) | — |

## Open debates

- [emergency-idle-2026-08-12.md](debates/emergency-idle-2026-08-12.md) — DECIDED: Option B (amended) — drain-first + warm M3 staging + PM/CTO self-work

## HR approvals (CEO-recorded, 2026-08-12)

- **Scale TESTER 1 → 2** (approval_ref: "CEO cycle-4 ruling 2026-08-12 — CAPACITY PRESSURE note fired (§3.5.1): tester 5 outstanding vs 1 instance; 6 drain TESTER tasks queued on TECHLEAD approval. Scale makes the 6-branch drain parallel. See workspace/reports/2026-08-12-cycle-1.md"). Executed via HR; confirmed live cycle 5 (capacityPressure.tester=2).
- **Lay off `its` (soft-disable)** (approval_ref: "CEO cycle-5 ruling 2026-08-12 — layoff-watch ladder decision (§3.5.4): its idle 3+ cycles, zero ready its-role tasks exist, role is not summonable in this roster; no filler invented. Recorded in COMPANY_STATE.md HR approvals and workspace/reports/2026-08-12-cycle-5.md."). **APPLIED by orchestrator 2026-08-12T17:09:45** (pending.json empty, layoff-watch cleared) — soft-disabled, re-enable free.

## Blockers

- **PR cap freeze (#155):** 6 open PRs vs cap 3. No new branches until the count drops. Closing superseded PRs 11/13/14/15 (orchestrator action) drops it 6→2; merging 16+17 lifts it entirely.
- **Canonical PR 16:** blocked on DEV fix (F1 README install/run BLOCKING, F2 DB-down crash HIGH — fix spec `vnstock-advisor-14-dev-data-ingest-security-gate-fix` ready) → TESTER re-run → QA GO.
- **Canonical PR 17:** merge-READY — TECHLEAD APPROVED + TESTER PASS + QA GO all on record; orchestrator merges next (mechanical CI re-check at merge). Merging 17 (and 16) plus closing 11/13/14/15 lifts the cap.
- Drain sequencing note (in backlog.md): TECHLEAD review (DONE, 6/6) → TESTER pass (17 done; 16 needs re-run after DEV fix) → QA go (17 = GO) → merge.

## Last CEO report

- 2026-08-12-cycle-6 (workspace/reports/2026-08-12-cycle-6.md)

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas). M3 DEV slices staged for post-freeze per CTO stack record seams (M3-A auth, M3-B suggestions, M3-D web-ui parallel; M3-C assembly serial).
