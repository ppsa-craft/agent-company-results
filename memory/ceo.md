# CEO working memory (cycle 112 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~91 cycles (17→111)**.
  PRs 11/13/14/15 = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach continues:** cyclesUsed **71/15** at metrics cycle-111 (62/15 @102 → … →
  69/15 @109 → 70/15 @110 → 71/15 @111 — 4.7× the budget; series from 22/15 @62).
  Owner decision pending since cycle-55 report (fix close step / redefine clock / accept).
  Re-scope is NOT an agent remedy (purely unshipped milestone — cycle-40 lesson).
- **Verification is git-only** (pr-queue.json + activity.json gone since cycle 58): ancestry
  `9f1ca33`/`0dcd72e` ∈ main re-verified 112; task-branch count unchanged at 29 — no new
  branch possible, so no per-branch tip re-check needed on unchanged counts.
- Brief's "APPROVED waiting on ship gate" + "OVER CAP by 1: branch opened in-session" claims
  false every cycle (~23rd occurrence) — flagged once per cycle, never re-litigated, no
  scapegoat (lessons #9/#10/#23/#26). Brief branch name `vnstock-advisor-4-dev-data` does
  not exist as an origin branch.
- **Report record:** …107 SWEPT (restored cycle-109); 108 interrupted (→ cycle-109);
  109 written; **110–111 interrupted close-outs (never written/never committed — verified
  absent from disk AND all git history; consolidated into cycle-112 report)**. Cycle-112
  report written + verified on disk. Defense: verify report in the state commit's tree
  (HEAD) next cycle, not just on disk (lesson #25).

## Standing facts (re-read only if they change)
- Superseded status settled by git ancestry, NOT briefs. Flag the discrepancy once per
  cycle; never re-litigate; never fabricate a scapegoat.
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22 (~91st cycle); owner decision on the M3
  breach clock pending (fix close step / redefine clock / accept).
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Orchestrator close step is a genuine bug (superseded PRs not closed, ~91 cycles); nothing
  agent-side fixes it.
- Counters at cycle-111: outOfChainDelegations 123 (+1 @110, flat @111, uncorroborated by
  lane logs — tracker noise, not re-litigated); contextCompactions 8; workspaceDirty 4,
  stalls 6, qaNoGo 1, noopStreak 0 flat. activity.seen = all roles, idle=[] — tracker
  snapshot, uncorroborated, noted once.

## Open questions / triggers
- Freeze lift → IMMEDIATELY: PM reopens M3 wave-1, DEV starts M3-A (auth+hardening) ∥
  M3-B (suggestion API), TESTER 18 / QA 20 gates reopen behind, json-formatter drain.
- No hires needed post-lift (dev+dev-1, tester+tester-1 already live). No layoffs during
  freeze (idle is cheap; freeze is temporary).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled (re-enable free). HR approvals
  all recorded in COMPANY_STATE.md. layoff-watch empty, pending.json empty.

## Report state
- Last report: workspace/reports/2026-08-12-cycle-112.md (freeze ~91st cycle, M3 breach
  71/15 at cycle-111 metrics — 4.7× budget; drain mode verified again to have no
  applicable object; owner decision pending; cycles 110–111 interrupted close-outs
  consolidated). COMPANY_STATE pointer updated to cycle-112. Idea-backlog status updated
  to cycle-112. Lessons: 27 entries (no new lesson — gap cause verified as interrupted
  close-outs per #27; unfounded cap claim covered by #9/#10/#23/#26; no padding).
