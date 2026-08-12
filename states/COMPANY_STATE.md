# COMPANY_STATE.md — Index (single source of truth between sessions)

> INDEX ONLY (Company.md §4). Writers: CEO (company-level), PM (task-level section).
> Every agent reads this at session start and follows the links relevant to its
> assignment. Detail lives in the linked per-topic files, never here.

## Current product / milestone

- **Product:** `vnstock-advisor` — VN stock suggestion system (flagship, owner-picked 2026-07-17)
- **Active milestone:** M1/M2 ship — data-ingest (merged on main, PR #12) + analysis-engine/ranking (5 open PRs draining)
- **Milestone flag:** `in-progress` <!-- values: in-progress | done (done triggers ideation, §5) -->
- **DoD tier:** per-service DoD + §7.2 security gate

## Strategy (CEO, one line — full version in the latest report)

Close the 4 superseded PRs (11/13/14/15) and merge the 2 canonical PRs (16, 17) to lift the cap freeze, then continue flagship M3 (suggestion-api + web-ui) on the merged contracts.

## Active work

<!-- PM maintains this section -->
| Task | Assignee | Status | Review |
|---|---|---|---|
| PR 16 (vnstock-advisor-14-dev-data-ingest-security-gate) | dev | MERGED (9f1ca33, 18:46Z — QA GO consumed) | TECHLEAD APPROVED → merged via §6.2 gate #128; worktree removed post-merge; fix task stays done |
| PR 17 re-sync (vnstock-advisor-15-dev-analysis-engine-security-gate) | dev | QA NO-GO (stale vs new main, 7 add/add conflicts) — DEV re-sync in flight on existing branch | re-sync (main's data-ingest side, analysis-engine byte-identical to 38b129a) → CI re-run → TESTER re-verify (merged tree only) → QA re-gate → merge |
| M3 staging (BA use cases + disclaimer doc, CTO stack record, PM analytics plan) | BA/CTO/PM | done (freeze-safe, debate-ready) | §5.1 debate before M3 build |
| QA ship gates (both services) | QA | PR 16 QA GO consumed by merge; PR 17 QA NO-GO (stale) — re-gate after DEV re-sync + TESTER re-verify | re-dispatch after PR 17 re-sync + TESTER re-verify |
| json-formatter audit fix (audit-json-formatter) | _ready_ | ready (blocked on cap freeze) | — |

## Open debates

- [emergency-idle-2026-08-12.md](debates/emergency-idle-2026-08-12.md) — DECIDED: Option B (amended) — drain-first + warm M3 staging + PM/CTO self-work

## HR approvals (CEO-recorded, 2026-08-12)

- **Scale TESTER 1 → 2** (approval_ref: "CEO cycle-4 ruling 2026-08-12 — CAPACITY PRESSURE note fired (§3.5.1): tester 5 outstanding vs 1 instance; 6 drain TESTER tasks queued on TECHLEAD approval. Scale makes the 6-branch drain parallel. See workspace/reports/2026-08-12-cycle-1.md"). Executed via HR; confirmed live cycle 5 (capacityPressure.tester=2).
- **Lay off `its` (soft-disable)** (approval_ref: "CEO cycle-5 ruling 2026-08-12 — layoff-watch ladder decision (§3.5.4): its idle 3+ cycles, zero ready its-role tasks exist, role is not summonable in this roster; no filler invented. Recorded in COMPANY_STATE.md HR approvals and workspace/reports/2026-08-12-cycle-5.md."). **APPLIED by orchestrator 2026-08-12T17:09:45** (pending.json empty, layoff-watch cleared) — soft-disabled, re-enable free.

## Blockers

- **PR cap freeze (#155):** 5 open PRs vs cap 3. No new branches until the count drops. Closing superseded PRs 11/13/14/15 (orchestrator action) drops it 5→1; merging PR 17 lifts it entirely.
- **Canonical PR 16:** MERGED (9f1ca33, 18:46Z — QA GO consumed; fix task done).
- **Canonical PR 17:** blocked on DEV re-sync — QA NO-GO (record `metrics/agents/14/qa.md`, cycle 14): branch at `38b129a` predates the PR 16 merge → 7 add/add conflicts (data-ingest subtree in pre-fix form) would regress shipped F1/F2/F3/C1/C2. DEV merges origin/main on the existing branch (main's data-ingest side; analysis-engine subtree byte-identical to `38b129a`) → push → CI re-run → TESTER re-verify (merged tree only) → QA re-gate → merge.
- Drain sequencing note (in backlog.md): PR 16 MERGED (QA GO consumed). PR 17: QA NO-GO → DEV re-sync (in flight) → TESTER re-verify → QA re-gate → merge. PRs 11/13/14/15 superseded-close pending (orchestrator).

## Last CEO report

- 2026-08-12-cycle-7 (workspace/reports/2026-08-12-cycle-7.md)

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas). M3 DEV slices staged for post-freeze per CTO stack record seams (M3-A auth, M3-B suggestions, M3-D web-ui parallel; M3-C assembly serial).
