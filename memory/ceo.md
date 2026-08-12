# CEO working memory (cycle 117 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~96 cycles (17→116)**.
  PRs 11/13/14/15 = SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **M3 breach continues:** cyclesUsed **76/15** at metrics cycle-116 (62/15 @102 → … →
  75/15 @115 → 76/15 @116 — 5.1× the budget; series from 22/15 @62).
  Owner decision pending since cycle-55 report (fix close step / redefine clock / accept).
  Re-scope is NOT an agent remedy (purely unshipped milestone — cycle-40 lesson).
- **Verification is git-only** (pr-queue.json + activity.json gone since cycle 58): ancestry
  `9f1ca33`/`0dcd72e` ∈ main re-verified 117; task-branch count unchanged at 29 — no new
  branch possible, so no per-branch tip re-check needed on unchanged counts.
- Brief's "APPROVED waiting on ship gate" + "OVER CAP by 1: branch opened in-session" claims
  false every cycle (~28th occurrence) — flagged once per cycle, never re-litigated, no
  scapegoat (lessons #9/#10/#23/#26). Brief branch name `vnstock-advisor-4-dev-data` does
  not exist as an origin branch.
- **Report record:** …107 SWEPT (restored cycle-109); 108 interrupted (→ cycle-109);
  109 written; 110–111 interrupted close-outs (→ cycle-112 report); 112–116 all written +
  verified in HEAD AND on disk (lesson #25 defense now proven 5 consecutive cycles —
  report chain gap-free since cycle 103); 117 written this cycle. Defense continues:
  verify report in HEAD's tree next cycle.
- Counters at cycle-116: outOfChainDelegations 132→134 (+2, uncorroborated by lane logs —
  no dispatch occurred; tracker artifact, noted once, not re-litigated);
  contextCompactions 8 flat; workspaceDirty 4, stalls 6, qaNoGo 1, noopStreak 0 flat.
  activity.idle empty @116 (cto idle @115 was a one-off tracker snapshot — no action).

## Standing facts (re-read only if they change)
- Superseded status settled by git ancestry, NOT briefs. Flag the discrepancy once per
  cycle; never re-litigate; never fabricate a scapegoat.
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22 (~96th cycle); owner decision on the M3
  breach clock pending (fix close step / redefine clock / accept).
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Orchestrator close step is a genuine bug (superseded PRs not closed, ~96 cycles); nothing
  agent-side fixes it.

## Open questions / triggers
- Freeze lift → IMMEDIATELY: PM reopens M3 wave-1, DEV starts M3-A (auth+hardening) ∥
  M3-B (suggestion API), TESTER 18 / QA 20 gates reopen behind, json-formatter drain.
- No hires needed post-lift (dev+dev-1, tester+tester-1 already live). No layoffs during
  freeze (idle is cheap; freeze is temporary).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled (re-enable free). HR approvals
  all recorded in COMPANY_STATE.md. layoff-watch empty, pending.json empty.

## Report state
- Last report: workspace/reports/2026-08-12-cycle-117.md (freeze ~96th cycle, M3 breach
  76/15 at cycle-116 metrics — 5.1× budget; drain mode verified again to have no
  applicable object; owner decision pending; cycle-116 report survival in HEAD confirmed).
  COMPANY_STATE pointer updated to cycle-117. Idea-backlog status updated to cycle-117.
  Lessons: 27 entries (no new lesson — unfounded cap claim covered by #9/#10/#23/#26;
  report-survival defense working per #25; no padding).
