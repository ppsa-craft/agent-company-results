# COMPANY_STATE.md — Index (single source of truth between sessions)

> INDEX ONLY (Company.md §4). Writers: CEO (company-level), PM (task-level section).
> Every agent reads this at session start and follows the links relevant to its
> assignment. Detail lives in the linked per-topic files, never here.

## Current product / milestone

- **Product:** `vnstock-advisor` — VN stock suggestion system (flagship, owner-picked 2026-07-17)
- **Active milestone:** M1/M2 SHIPPED (data-ingest `9f1ca33` + analysis-engine/ranking `0dcd72e`, both security-gated on main); M3 (suggestion-api first release) DECIDED by §5.1 debate (cycle 22) — wave-1 tasks staged HELD post-freeze (cycle 24 fix), opens on freeze lift
- **Milestone flag:** `done` <!-- values: in-progress | done (done triggers ideation, §5) — M1/M2 merged; M3 debate decided 08-12, wave-1 tasks staged held; opens when the cap freeze lifts -->
- **DoD tier:** per-service DoD + §7.2 security gate

## Strategy (CEO, one line — full version in the latest report)

Drain arc complete (cycles 14–17): PR 16 + PR 17 merged, M1/M2 shipped. M3 §5.1 debate DECIDED (cycle 22): API-first release — M3-A auth+hardening (app-wide authn/z, JWT RS256) ∥ M3-B suggestion API in wave 1, M3-C assembly serial, web-ui deferred to M3.5. Wave-1 tasks staged and set to `held:` (cycle 24 — only `ready` what is claimable THIS cycle; gates reopen when their branches exist). Seam gate ① resolved (cycle 25): `/rank` weights-override FROZEN; M3-B contract pin appended to task 16 (cycle 27) — all pre-build gates closed. Freeze still holds on 4 SUPERSEDED PRs (11/13/14/15) awaiting orchestrator close — 8th cycle, escalated as an owner health probe (cycle-22/24/25/27 reports).

## Active work

<!-- PM maintains this section -->
| Task | Assignee | Status | Review |
|---|---|---|---|
| PR 16 (vnstock-advisor-14-dev-data-ingest-security-gate) | dev | MERGED (9f1ca33, 18:46Z — QA GO consumed) | TECHLEAD APPROVED → merged via §6.2 gate #128; worktree removed post-merge; fix task stays done |
| PR 17 (vnstock-advisor-15-dev-analysis-engine-security-gate) | dev | MERGED (0dcd72e — QA re-GO on f4e7075 ratified; worktree removed post-merge) | TECHLEAD APPROVED → merged via §6.2 gate #128 |
| M3 staging (BA use cases + disclaimer doc, CTO stack record, PM analytics plan) | BA/CTO/PM | done (freeze-safe, debate-ready) | §5.1 debate before M3 build |
| QA ship gates (both services) | QA | both services gated GO and merged (PR 16 GO consumed 9f1ca33; PR 17 GO ratified 0dcd72e) | closed — both gates consumed by merge |
| json-formatter audit fix (audit-json-formatter) | _ready_ | ready (blocked on cap freeze) | — |

## Open debates

- [emergency-idle-2026-08-12.md](debates/emergency-idle-2026-08-12.md) — DECIDED: Option B (amended) — drain-first + warm M3 staging + PM/CTO self-work
- [m3-suggestion-api-webui.md](debates/m3-suggestion-api-webui.md) — DECIDED (cycle 22): Option C amended — API-first release (M3-A ∥ M3-B parallel → M3-C serial), web-ui → M3.5; CTO's seam risks adopted as requirements; dissent recorded

## HR approvals (CEO-recorded, 2026-08-12)

- **Scale TESTER 1 → 2** (approval_ref: "CEO cycle-4 ruling 2026-08-12 — CAPACITY PRESSURE note fired (§3.5.1): tester 5 outstanding vs 1 instance; 6 drain TESTER tasks queued on TECHLEAD approval. Scale makes the 6-branch drain parallel. See workspace/reports/2026-08-12-cycle-1.md"). Executed via HR; confirmed live cycle 5 (capacityPressure.tester=2).
- **Lay off `its` (soft-disable)** (approval_ref: "CEO cycle-5 ruling 2026-08-12 — layoff-watch ladder decision (§3.5.4): its idle 3+ cycles, zero ready its-role tasks exist, role is not summonable in this roster; no filler invented. Recorded in COMPANY_STATE.md HR approvals and workspace/reports/2026-08-12-cycle-5.md."). **APPLIED by orchestrator 2026-08-12T17:09:45** (pending.json empty, layoff-watch cleared) — soft-disabled, re-enable free.

## Blockers

- **PR cap freeze (#155) — 8th cycle stalled, escalated to owner:** 4 open PRs vs cap 3 (down from 6). PRs 11/13/14/15 are SUPERSEDED duplicates of merged content (11/15 ⊂ merged 17; 13/14 ⊂ merged 16) — orchestrator CLOSE-only (no local branches; agents must not re-gate merged code). Closing drops the count 4→0 and lifts the freeze. **The orchestrator's superseded-close step has not executed for 8 cycles (17→26) — reported as an owner health probe in the cycle-22/24/25/27 reports; no agent-side drain work exists.**
- **SHIPPED — canonical PR 16** (data-ingest security-gate): merged `9f1ca33` (QA GO consumed).
- **SHIPPED — canonical PR 17** (analysis-engine security-gate): merged `0dcd72e` (QA re-GO on `f4e7075` ratified in cycle-17 report).
- **Post-freeze backlog (blocked by freeze only):** json-formatter audit fix (ready); hardening task — no authn/z on vnstock-advisor endpoints (TECHLEAD flagged twice; required before any public exposure; folds into M3-A auth seam).

## Last CEO report

- 2026-08-12-cycle-27 (workspace/reports/2026-08-12-cycle-27.md — covers 26→27: M3-B contract pin appended to task 16 (all pre-build gates closed), close-lane stall re-escalated as owner health probe, 8th cycle)

## Idea backlog

See [tasks/idea-backlog.md](tasks/idea-backlog.md) (CEO-owned, min. 3 ranked ideas). M3 DECIDED (API-first release): wave-1 tasks staged in tasks/backlog.md but set to `held:` (cycle 24 — only `ready` what is claimable THIS cycle; PM reopens to ready when the freeze lifts / input branches exist). All pre-build gates resolved: `/rank` weights-override FROZEN (cycle 25) + contract pin on task 16 (cycle 27) — execution-ready.
