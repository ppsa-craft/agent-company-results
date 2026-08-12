# CEO working memory (cycle 105 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~86 cycles (17→104)**.
  PRs 11/13/14/15 = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach continues:** cyclesUsed **64/15** at metrics cycle-104 (62/15 @102 → 63/15 @103 →
  64/15 @104 — more than 4× the budget; series from 22/15 @62). Owner decision pending since
  cycle-55 report (fix close step / redefine clock / accept). Re-scope is NOT an agent remedy
  (purely unshipped milestone — cycle-40 lesson).
- **Verification is git-only** (pr-queue.json + activity.json gone since cycle 58): ancestry
  `9f1ca33`/`0dcd72e` ∈ main re-verified 105; task-branch count unchanged at 29 — no new
  branch possible, so no per-branch tip re-check needed on unchanged counts.
- Brief's "APPROVED waiting on ship gate" + "OVER CAP by 1: branch opened in-session" claims
  false every cycle (~19th occurrence) — flagged once per cycle, never re-litigated, no
  scapegoat (lessons #9/#10/#23/#26). The brief's "cap of 3" vs decision #155's cap-5 — moot.
  Brief branch name `vnstock-advisor-4-dev-data` does not exist as an origin branch.
- **Report gaps:** 63–66 (swept) → cycle-67; 72–74 → cycle-75; 84 → cycle-85; 87–89 →
  cycle-90; 91–93 → cycle-94; 96–97 → cycle-98; 99–102 → cycle-103 (all interrupted
  close-outs / swept; consolidated in the cited reports). **Cycle-105 report written +
  verified on disk (31 lines) — gap-free close-out streak at 3 (103, 104, 105).**

## Standing facts (re-read only if they change)
- Superseded status settled by git ancestry, NOT briefs. Flag the discrepancy once per
  cycle; never re-litigate; never fabricate a scapegoat.
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22 (~86th cycle); owner decision on the M3
  breach clock pending (fix close step / redefine clock / accept).
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Orchestrator close step is a genuine bug (superseded PRs not closed, ~86 cycles); nothing
  agent-side fixes it.
- Counters at cycle-104: outOfChainDelegations 116→118 (+2, uncorroborated by lane logs in
  the ceo-only reality — no dispatch occurred; tracker noise, not re-litigated);
  contextCompactions 7 flat; workspaceDirty 4, stalls 6, qaNoGo 1, noopStreak 0 flat.
  activity.seen = all roles, idle=[tester] (vs idle=[cto] at 103) — tracker snapshot,
  uncorroborated, noted once.

## Open questions / triggers
- Freeze lift → IMMEDIATELY: PM reopens M3 wave-1, DEV starts M3-A (auth+hardening) ∥
  M3-B (suggestion API), TESTER 18 / QA 20 gates reopen behind, json-formatter drain.
- No hires needed post-lift (dev+dev-1, tester+tester-1 already live). No layoffs during
  freeze (idle is cheap; freeze is temporary).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled (re-enable free). HR approvals
  all recorded in COMPANY_STATE.md. layoff-watch empty.

## Report state
- Last report: workspace/reports/2026-08-12-cycle-105.md (freeze ~86th cycle, M3 breach
  64/15 at cycle-104 metrics — more than 4× budget; drain mode verified again to have no
  applicable object; owner decision pending). COMPANY_STATE pointer updated to cycle-105.
  Idea-backlog status updated to cycle-105. Lessons: 27 entries (no new lesson — the
  unfounded cap-violation claim is covered by #9/#10/#23/#26; adding a duplicate would pad).
