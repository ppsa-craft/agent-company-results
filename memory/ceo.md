# CEO working memory (cycle 61 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~44 cycles (17→61)**.
  PRs 11/13/14/15 = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach continues:** cyclesUsed **20/15** at metrics cycle-60 (15/15 @55, 16/15 @56,
  17/15 @57, 18/15 @58, 19/15 @59, 20/15 @60). Owner decision pending since cycle-55 report
  (fix close step / redefine clock / accept). Re-scope is NOT an agent remedy (purely
  unshipped milestone — cycle-40 lesson).
- **Verification is git-only** (pr-queue.json + activity.json gone since cycle 58): ancestry
  `9f1ca33`/`0dcd72e` ∈ main re-verified 61; branch count unchanged at 29 — no new branch
  possible, so no per-branch tip re-check needed on unchanged counts.
- Brief's "APPROVED waiting on ship gate" + "OVER CAP by 1: branch opened in-session" claims
  false every cycle — flagged once per cycle, never re-litigated, no scapegoat
  (lessons #9/#10/#23/#26).

## Standing facts (re-read only if they change)
- Superseded status settled by git ancestry, NOT briefs. Flag the discrepancy once per
  cycle; never re-litigate; never fabricate a scapegoat.
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22 (~44th cycle); owner decision on the M3
  breach clock pending (fix close step / redefine clock / accept).
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Orchestrator close step is a genuine bug (superseded PRs not closed, ~44 cycles); nothing
  agent-side fixes it.
- Metrics-tracker delta persists: cycle-60 `activity.seen` = all 9 roles, idle `[]`, while
  no lane logs/verdicts exist (ceo-only reality) — noted once, not re-litigated.
- Counters at cycle-60: outOfChainDelegations 77 (was 62 @55 → +15 over 55–60, no lane logs
  corroborate); workspaceDirty 4, stalls 6, qaNoGo 1 unchanged.

## Open questions / triggers
- Freeze lift → IMMEDIATELY: PM reopens M3 wave-1, DEV starts M3-A (auth+hardening) ∥
  M3-B (suggestion API), TESTER 18 / QA 20 gates reopen behind, json-formatter drain.
- No hires needed post-lift (dev+dev-1, tester+tester-1 already live). No layoffs during
  freeze (idle is cheap; freeze is temporary).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled (re-enable free). HR approvals
  all recorded in COMPANY_STATE.md.

## Report state
- Last report: workspace/reports/2026-08-12-cycle-61.md (freeze ~44th cycle, M3 breach
  20/15 at cycle-60 metrics — owner decision pending). COMPANY_STATE pointer updated to
  cycle-61. Lessons current (26 entries incl. the verification-sources lesson).
