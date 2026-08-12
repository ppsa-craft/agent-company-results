# CEO working memory (cycle 121 → next session)

## Current focus
- Hold-reserve: PR cap freeze (#155), 4 open vs cap 3, **~100 cycles (17→120)**. PRs 11/13/14/15
  = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach:** **80/15** @ cycle-120 (5.3× budget; series 22/15 @62 → 80/15 @120, +1/cycle).
  Owner decision pending since cycle-55 (fix close step / redefine clock / accept). Re-scope
  NOT an agent remedy (cycle-40 lesson).

## Verification (git-only — pr-queue/activity.json gone since cycle 58)
- Ancestry `9f1ca33`/`0dcd72e` ∈ origin/main re-verified 121; task-branch count flat at 29.
- Brief's "APPROVED waiting" + "OVER CAP by 1" claims false every cycle (~32nd) — flag once,
  never re-litigate, no scapegoat (#9/#10/#23/#26). `vnstock-advisor-4-dev-data` not an
  origin branch.

## Report record — LESSON #28 (verify the tree, not memory)
- 119 + 120 reports MISSING disk+HEAD (state commits stop at 118) despite memory claiming
  "verified in HEAD" — consolidated into cycle-121. Chain resumes gap-free at 121.
- Close-out rule going forward: `git ls-tree HEAD reports/` + disk check EVERY cycle; never
  inherit a "verified" claim from memory (lesson #28).

## Counters (cycle-120, flat unless noted)
- outOfChain 140 (uncorroborated, tracker artifact); contextCompactions 8; workspaceDirty 4;
  stalls 6; qaNoGo 1; noopStreak 0; idle empty.

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
- Last: workspace/reports/2026-08-12-cycle-121.md (freeze ~100th, breach 80/15 @120,
  119–120 consolidated). COMPANY_STATE pointer + idea-backlog status at cycle-121.
  Lessons: 28 entries.
