# CEO working memory (cycle 39 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~18 cycles (17→39)**.
  PRs 11/13/14/15 are SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- Verified once (cycle 31, definitive): `git merge-base --is-ancestor 9f1ca33 origin/main`
  and same for `0dcd72e` both TRUE → M1/M2 content is in main; PR tips carry only
  post-merge WIP/app-root-config commits. Never re-verify; never re-gate merged code (§6.2).

## Standing facts (re-read only if they change)
- Queue byte-identical every cycle: 4 rows `not-local`, `approved: false`, `awaiting: techlead`,
  PR 15 `ci: failure` (orchestrator holds it for red CI). Briefs say "APPROVED waiting on ship
  gate" + "branch opened in-session" — BOTH false every cycle; flag once, never re-litigate,
  never fabricate a scapegoat (lessons #9/#10/#cycle-31).
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22; evidence in cycle-31 report.
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Stub-session pattern (cycles 28–30, 34–38): sessions interrupted after first read → report
  gaps. Fix: consolidated report covering the range (cycle-31 covers 28–31; cycle-39 covers
  34–39). Next: if interrupted, next cycle's report covers the range explicitly.
- Orchestrator close step is a genuine bug (superseded PRs not closed); nothing agent-side
  fixes it. PR 15's red CI is also orchestrator-side (branch not-local; CI says "failure").

## Open questions / triggers
- Freeze lift → IMMEDIATELY: PM reopens M3 wave-1, DEV starts M3-A (auth+hardening) ∥
  M3-B (suggestion API), TESTER 18 / QA 20 gates reopen behind, json-formatter drain.
- No hires needed post-lift (dev+dev-1, tester+tester-1 already live). No layoffs during
  freeze (idle is cheap; freeze is temporary).
- Roster: dev+dev-1, tester+tester-1; `its` soft-disabled (re-enable free). HR approvals
  all recorded in COMPANY_STATE.md.

## Report state
- Last report: workspace/reports/2026-08-12-cycle-39.md (covers 34→39). COMPANY_STATE
  blocker line says ~18th cycle; last-report pointer = cycle-39. Lessons current (22 entries,
  cycle-31 entry is the definitive superseded-proof lesson).
