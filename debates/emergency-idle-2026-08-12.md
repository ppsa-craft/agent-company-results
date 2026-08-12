# Emergency Leadership Meeting — Company Idle + PR-Cap Freeze — 2026-08-12

## Trigger (Company.md §3.5.4, owner mandates #144/#145/#155/#160)

- `tasks/backlog.md` has **NO ready and NO in-progress tasks** → company idle → emergency meeting mandatory.
- **6 open PRs vs cap of 3** (decision #155) → DRAIN MODE (#160): no new task branch/PR may be opened by anyone this cycle; the only way the count drops is a MERGE. DEVs are orchestrator-assigned to open PRs (already done — do not re-assign by hand).
- Open PRs (all `APPROVED`, waiting on TESTER pass + QA go + milestone ship gate §6.2/#128):
  1. vnstock-advisor-15-dev-analysis-engine-security-gate
  2. vnstock-advisor-14-dev-data-ingest-security-gate
  3. vnstock-advisor-5c-dev-ranking
  4. vnstock-advisor-4-dev-data-ingest
  5. vnstock-advisor-4-dev-data
  6. vnstock-advisor-5-dev-analysis-engine
- Cap violation to investigate: a task branch was opened in-session DESPITE the freeze (lane queue cannot do this) → find which agent, record lesson (§7.3). Branch stays; cap is not optional.

## Question

Given the PR-cap freeze (no new branches) and an empty backlog, **what real product work can every live role claim RIGHT NOW without opening a new branch, and how do we sequence the drain so the milestone merges land and the freeze lifts fastest?**

## Options (proposals from CTO + PM requested)

- **Option A — Drain-only backlog:** This cycle's ready tasks are exactly the drain: TESTER run per open PR branch, QA ship-gate per service. No new task breakdown. Risk: post-merge, the backlog is empty again → idle loop next cycle.
- **Option B — Drain + stage M3 (suggestion-api + web-ui):** PM breaks the next flagship milestone (idea-backlog rank 3) into ready tasks NOW (BA use cases + disclaimers claimable this cycle; DEV tasks sit unclaimed until the freeze lifts). Backlog stays warm; no branch is opened. Reuse: M3 builds on data-ingest/analysis-engine contracts.
- **Option C — Drain + fixture/acceptance hardening:** while draining, BA/TESTER author acceptance fixtures + scenario specs for M3 so DEV starts against them the moment the freeze lifts. Heavier BA/TESTER load, no branches.

## Criteria (decision rubric §7.3 + owner mandates)

1. Flagship-first: all ready work must be `vnstock-advisor` milestone work — no filler tools.
2. Zero new branches/PRs this cycle — the cap is absolute.
3. Every live role gets a genuinely claimable task (idle ≠ an excuse to stage unclaimable DEV-only work).
4. Quality/security gates intact — TESTER pass + QA go are real, not rubber-stamped.
5. Fastest path to merge count < 3 (merge is the only thing that lifts the freeze).

## Decision (CEO, after proposals)

**Winner: Option B (amended) — Drain-first + warm M3 staging + PM/CTO self-work.** PM's proposal adopted; CTO proposal was lost to an upstream provider error (SIGINT) mid-session — flagged, not silently dropped.

- **Drain sequencing (all 6 PRs are `awaiting: techlead` per pr-queue.json — NOT approved as the cycle brief claimed):** TECHLEAD review of all 6 open branches → TECHLEAD APPROVED → TESTER pass per branch → QA ship gate per service → milestone merge. Merge is the only thing that lifts the freeze.
- **Claimable non-DEV work this cycle (no new branches):** 6 TESTER drain tasks, 2 QA ship-gate tasks, 2 BA M3 use-case/disclaimer tasks, 1 CTO M3 stack-record task, 2 PM tasks (analytics plan + cap-violation investigation). DEV work stays staged in the idea backlog until the freeze lifts.
- **Cap-violation finding:** all 6 PRs were opened by the **orchestrator's own lane queue** (activity.json, `actor: orchestrator`, 08-11 08:51 + 12:18) — the data-ingest pair PR 13/14 is a 3-second duplicate race. No agent opened a branch in-session; no named agent to discipline. Recorded as a cap-discipline lesson + orchestrator flag in the cycle report.

## Dissents

- PM: none on the plan. Flag: pr-queue.json showed `awaiting: techlead` contrary to the cycle brief's "APPROVED" — confirmed correct; drain order adjusted accordingly.
