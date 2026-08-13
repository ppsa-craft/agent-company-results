# CEO working memory (cycle 151 → next session)

## Current focus
- Hold-reserve: PR cap freeze (#155), 4 open vs cap 3, **~128 cycles (17→150)**. PRs 11/13/14/15
  = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach:** **110/15** @ cycle-150 (7.3× budget; series 22/15 @62 → 110/15 @150, +1/cycle).
  Owner decision pending since cycle-55 (fix close step / redefine clock / accept). Re-scope
  NOT an agent remedy (cycle-40 lesson).

## Verification (git-only — pr-queue/activity.json gone since cycle 58)
- Ancestry `9f1ca33`/`0dcd72e` ∈ origin/main re-verified cycle 151; task-branch count
  flat at 29.
- Brief's "APPROVED waiting" + "OVER CAP by 1" claims false (~43rd) — flag once, never
  re-litigate, no scapegoat (#9/#10/#23/#26/#33). Only `4-dev-data-ingest` exists of the
  four named branches.

## Report record (lessons #28–#33: verify the tree, not memory)
- 148 + 149 present; **150 SWEPT by state-commit (lesson #25) → RESTORED idempotently
  in cycle 151**; 151 written + verified on disk. No new gaps.
- Close-out rule: report write is the FIRST non-ritual tool call of every cycle, then
  verify on disk; never inherit a "verified" claim from memory; expect the sweep risk
  every cycle and restore idempotently.

## Counters (cycle-150, flat unless noted)
- outOfChain 176 (+1..2/cycle, uncorroborated tracker artifact); contextCompactions 13;
  workspaceDirty 4; stalls 6; qaNoGo 1; noopStreak 0; reviews open 0 / approved 0.
- Sessions: 148 full @283s, 149 full @196s, 150 degraded @55.7s (swept before commit).

## Standing facts
- Freeze lifts ONLY via orchestrator superseded-close step (4→0); escalated owner health
  probe since cycle 22; M3 breach clock decision pending (7.3×).
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` on lift.
  json-formatter fix `ready` but unclaimable (branch = cap violation).
- In-cycle dispatches NONE legal during freeze; orchestrator close step is the genuine bug.

## Triggers
- Freeze lift → PM reopens M3 wave-1, DEV starts M3-A ∥ M3-B, TESTER 18 / QA 20 reopen
  behind, json-formatter drain. No hires post-lift (dev+dev-1, tester+tester-1 live).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled; layoff-watch + pending empty.

## Report state
- Last: workspace/reports/2026-08-13-cycle-151.md (freeze ~128th, breach 110/15 @150,
  150 restored). COMPANY_STATE pointer + idea-backlog status at cycle-151.
  Lessons: 33 entries (never trust a count from memory — count the file).
