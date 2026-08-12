# CEO working memory (cycle 122 → next session)

## Current focus
- Hold-reserve: PR cap freeze (#155), 4 open vs cap 3, **~101 cycles (17→121)**. PRs 11/13/14/15
  = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach:** **81/15** @ cycle-121 (5.4× budget; series 22/15 @62 → 81/15 @121, +1/cycle).
  Owner decision pending since cycle-55 (fix close step / redefine clock / accept). Re-scope
  NOT an agent remedy (cycle-40 lesson).

## Verification (git-only — pr-queue/activity.json gone since cycle 58)
- Ancestry `9f1ca33`/`0dcd72e` ∈ origin/main re-verified 122; task-branch count flat at 29.
- Brief's "APPROVED waiting" + "OVER CAP by 1" claims false every cycle (~33rd) — flag once,
  never re-litigate, no scapegoat (#9/#10/#23/#26). `vnstock-advisor-4-dev-data` not an
  origin branch.
- Benign anomaly: `reports/2026-07-22-cycle-122.md` = prior-era artifact (July 22,
  vn-stock-suggestion era) carried in state-commit tree — distinct filename from
  `2026-08-12-cycle-122.md`, no collision; noted once, not touched.

## Report record (lesson #28: verify the tree, not memory)
- 121 verified in HEAD + disk (the 119–120 gap was consolidated into 121); 122 written this
  cycle and verified on disk. Chain gap-free from 121.
- Close-out rule: `git ls-tree HEAD reports/` + disk check EVERY cycle; never inherit a
  "verified" claim from memory (lesson #28).

## Counters (cycle-121, flat unless noted)
- outOfChain 142 (uncorroborated, tracker artifact); contextCompactions 9; workspaceDirty 4;
  stalls 6; qaNoGo 1; noopStreak 0; idle [ba, cto, tester] (no legal work — correct).

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
- Last: workspace/reports/2026-08-12-cycle-122.md (freeze ~101st, breach 81/15 @121).
  COMPANY_STATE pointer + idea-backlog status at cycle-122. Lessons: 28 entries.
