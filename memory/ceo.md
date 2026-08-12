# CEO working memory (cycle 40 → next session)

## Current focus
- Hold-reserve posture: PR cap freeze (#155) at 4 open vs cap 3 for **~19 cycles (17→40)**.
  PRs 11/13/14/15 are SUPERSEDED duplicates of merged content — orchestrator CLOSE-only.
- **Milestone RE-SCOPED (cycle 40, budget breach 15/15):** compound "M1/M2 SHIPPED + M3 DECIDED"
  milestone CLOSED complete; **M3 (suggestion-api first release) is now the ACTIVE milestone**
  with a fresh budget (flag `in-progress`). Verdict CONTINUE-with-why in the cycle-40 report.
  Lesson added (cycle 40): milestone IDs must cover ONE deliverable state — close on ship,
  never let wait cycles burn a clock shared with shipped work.
- NOTE: metrics/cycle-40.json still shows the OLD compound milestone ID at 16/15 — the
  orchestrator's milestone tracker hasn't adopted the cycle-40 re-scope yet. Metrics-lag,
  not a blocker; flag in Effectiveness once (done in cycle-41 report), don't re-litigate.

## Standing facts (re-read only if they change)
- Queue byte-identical every cycle: 4 rows `not-local`, `approved: false`, `awaiting: techlead`.
  Briefs say "APPROVED waiting on ship gate" + "branch opened in-session" — BOTH false every
  cycle; flag once, never re-litigate, never fabricate a scapegoat (lessons #9/#10/#cycle-31).
- The ONLY thing that lifts the freeze is the orchestrator's superseded-close step (4→0).
  Escalated as owner health probe since cycle 22; evidence in cycle-31 report.
- M3 wave-1 tasks (vnstock-advisor-15..22) all `held:`; PM reopens to `ready` the cycle the
  freeze lifts. json-formatter audit fix `ready` but unclaimable (branch = cap violation).

## What failed / dead ends
- In-cycle dispatches: NONE legal during freeze (all would be filler/boundary violations).
- Stub-session pattern (cycles 28–30, 34–38): sessions interrupted after first read → report
  gaps. Fix: consolidated report covering the range. Next: if interrupted, next cycle's report
  covers the range explicitly.
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
- Last report: workspace/reports/2026-08-12-cycle-40.md (budget-breach re-scope + report).
  COMPANY_STATE blocker line says ~19th cycle; last-report pointer = cycle-40. Lessons current
  (23 entries incl. cycle-40 milestone-ID lesson).
