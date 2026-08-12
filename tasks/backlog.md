# Task backlog — the company-wide ready-queue (Company.md §4, §3.5.4)

> Single writer: **PM**. Idle agents take the next `ready` task tagged for their
> role (ask PM to record the claim; Phase 5 lanes are assigned by the
> orchestrator). Ideas graduate here from `idea-backlog.md` once a product is
> committed. Format, one line per task, ranked:
>
> `- [role] [product] tasks/<id>.md — status: ready | claimed:<agent> | done`

- [dev] vnstock-advisor tasks/vnstock-advisor-14-dev-data-ingest-security-gate-fix.md — status: done
- [dev] [json-formatter] tasks/audit-json-formatter.md (note: still blocked on the PR cap freeze #155, no new branch until a merge lifts it) — status: ready

Drain order: TECHLEAD review → TESTER pass → QA go → merge (cap freeze lifts only on merge). TESTER tasks: wait for the branch's TECHLEAD APPROVED before running. Gate-state records live in `reviews/<task-id>.md` — if the queue resets (records archived), TECHLEAD restores from `archive/reviews/` + QA re-affirms; never re-review approved code.

Drain status 2026-08-12 (cycle 15): PR 16 (data-ingest security-gate, task-14) MERGED — `workspace/main` tip `9f1ca33` "merge task/vnstock-advisor-14-dev-data-ingest-security-gate-dev (TECHLEAD approved, §6.2 merge gate #128)" at 18:46Z; QA GO consumed by that merge; `worktrees/dev-di-task14` checkout removed post-merge; fix task stays `status: done` above. PR 17 (analysis-engine security-gate, task-15) = QA NO-GO (record `metrics/agents/14/qa.md`, cycle 14): branch `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev` at `38b129a` predates the PR 16 merge → 7 add/add conflicts vs new main (all in the data-ingest subtree it carries in pre-fix form) — merging it would regress the shipped F1/F2/F3/C1/C2 fixes. DEV re-sync IN FLIGHT on the existing PR 17 branch (no new branch, no new task file): merge origin/main, resolve conflicts taking main's data-ingest side, preserve the analysis-engine subtree byte-identical to `38b129a`, push, CI re-runs, then TESTER re-verify (merged tree only) → QA re-gate → merge. PRs 11/13/14/15 superseded-close pending (orchestrator mechanical action). Freeze holds: 5 open PRs vs cap 3; closing the 4 superseded drops 5→1; merging 17 lifts it fully.

**Hardening flag (cycle 14):** no authn/z on vnstock-advisor endpoints — TECHLEAD flagged twice (PRs 16/17 records); acceptable only at current tier; must go on the backlog as a hardening task before any public exposure (needs a branch — post-freeze).
