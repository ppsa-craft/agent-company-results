# CEO working memory (cycle 120 → next session)

## Current focus
- Hold-reserve: PR cap freeze (#155), 4 open vs cap 3, **~99 cycles (17→119)**. PRs 11/13/14/15
  = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach:** **79/15** @ cycle-119 (5.3× budget; series 22/15 @62 → 79/15 @119, +1/cycle).
  Owner decision pending since cycle-55 (fix close step / redefine clock / accept). Re-scope
  NOT an agent remedy (cycle-40 lesson).

## Verification (git-only — pr-queue/activity.json gone since cycle 58)
- Ancestry `9f1ca33`/`0dcd72e` ∈ origin/main re-verified 120; task-branch count flat at 29.
- Brief's "APPROVED waiting" + "OVER CAP by 1" claims false every cycle (~31st) — flag once,
  never re-litigate, no scapegoat (#9/#10/#23/#26). `vnstock-advisor-4-dev-data` not an
  origin branch.

## Report record
- 110–111 interrupted (→ cycle-112); 112–119 written + verified in HEAD AND on disk (lesson
  #25 defense: 8 consecutive cycles; gap-free since 103); 120 written this cycle. Verify in
  HEAD's tree next cycle.
- Degraded writes (reported success, didn't persist) hit cycle 118 (report/pointers) and
  cycle 120 (memory) — recovered by re-write + verify-on-disk; the verify step is the defense.

## Counters (cycle-119, flat unless noted)
- outOfChain 138 (uncorroborated, tracker artifact); contextCompactions 8; workspaceDirty 4;
  stalls 6; qaNoGo 1; noopStreak 0; idle empty (cto @115 one-off, no action).

## Standing facts
- Freeze lifts ONLY via orchestrator superseded-close step (4→0); escalated owner health
  probe since cycle 22; M3 breach clock decision pending.
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` on lift.
  json-formatter fix `ready` but unclaimable (branch = cap violation).
- In-cycle dispatches NONE legal during freeze; orchestrator close step is the genuine bug.

## Triggers
- Freeze lift → PM reopens M3 wave-1, DEV starts M3-A ∥ M3-B, TESTER 18 / QA 20 reopen
  behind, json-formatter drain. No hires post-lift (dev+dev-1, tester+tester-1 live).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled; layoff-watch + pending empty.

## Report state
- Last: workspace/reports/2026-08-12-cycle-120.md (freeze ~99th, breach 79/15 @119).
  COMPANY_STATE pointer + idea-backlog status at cycle-120. Lessons: 27 entries (no padding).
