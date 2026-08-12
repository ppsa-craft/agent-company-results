# Lessons — CEO

> Writers: **CEO (self)** + **owner** (Company.md §7.3). The only self-written
> lessons file, kept honest by the code-computed KPIs in `metrics/`.
> Entries marked `[OWNER]` come from the owner — NEVER prune or contradict them.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

- 2026-08-12 — Cap-violation claim ("branch opened in-session despite the freeze"): activity.json shows ALL 6 open PRs were opened by the **orchestrator's lane queue** (actor: orchestrator; PRs 13/14 are a 3-second duplicate race on data-ingest; the rest batch-opened 12:18) — no agent opened a branch in-session, and the WIP-checkpoint commits landed on already-open branches. → Fabricating a scapegoat would have been dishonest; the real defect is orchestrator-internal cap enforcement. Lesson: verify cap/violation claims against pr-queue.json + activity.json BEFORE acting; the brief also said "APPROVED" when pr-queue.json said `awaiting: techlead` — trust the queue file for drain sequencing, and flag the discrepancy once in the report.
- 2026-08-12 — Dirty TESTER worktree (`tester-di-task14/apps/vnstock-advisor/uv.lock`): an interrupted TESTER run left a generated lockfile behind, and the orchestrator flagged the workspace dirty. TESTER runs `edit: deny` so this was a build artifact from following the README, not a product edit — but leftover artifacts still dirty the workspace. → Lesson: TESTER should remove generated files (uv.lock, .venv, __pycache__) from its worktree when a run is interrupted, and the CEO should sweep untracked artifacts in tester worktrees after interrupted runs (rm only — TESTER never commits).
