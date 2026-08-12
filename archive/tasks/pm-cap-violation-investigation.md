# PM — cap-violation investigation + lesson (#160)

- **App:** vnstock-advisor (the violation is on flagship branches) | **DoD tier:** 3 (process/lesson work, no code) | **Assignee:** pm (claimed + closed out 2026-08-12)
- **Goal:** Identify which agent opened a task branch in-session DESPITE the PR-cap freeze (a lane queue cannot do this by itself — some agent created/opened a branch), and record the §7.3 lesson so it cannot recur. Branch stays; cap is not optional.
- **Background:** Debate file `debates/emergency-idle-2026-08-12.md` line 14 flags: "a task branch was opened in-session DESPITE the freeze (lane queue cannot do this) → find which agent, record lesson." Two of the 6 open PRs (13 `vnstock-advisor-4-dev-data` / 14 `vnstock-advisor-4-dev-data-ingest`) look like a duplicate pair opened ~simultaneously by different authors (`ingest` vs `dev`) — a likely violation locus. This is claimable by PM during the freeze: reads logs/reports, writes a lesson; no branch.

## Acceptance criteria

1. Investigation performed: trace branch creation + authorship from `logs/`, `workspace/reports/` (cycle reports 2026-08-10..12), orchestrator artifacts, and the PR metadata in `.orchestrator/pr-queue.json`/`state.json` (author fields, openedAt, title mismatches).
2. Culprit named (or "unresolvable — evidence insufficient" honestly stated with what IS known) in the task output.
3. Dated lesson appended to `lessons/dev.md` (and `lessons/pm.md` note if PM's own breakdown contributed) per §7.3, `- YYYY-MM-DD — what happened → why wrong → what to do next time`.
4. If PR 13/14 are confirmed duplicates, flag for CEO/TECHLEAD whether closing the superseded one as hygiene (not cap-gaming) is appropriate.

## Implementation Plan (for PM)

- Read `logs/orchestrator.log`, `logs/debug-trace.log`, recent cycle reports for 2026-08-10..12, and the PR metadata (author fields: `ingest` vs `dev`, `openedAt` within 3s of each other for PR 13/14).
- Cross-check against the freeze chronology in `debates/emergency-idle-2026-08-12.md` and decision #160.
- Record the lesson; report findings + recommendation to CEO.

## Test Plan (verification of the lesson loop)

1. Lesson is dated, concrete, and actionable — not a platitude ("don't open branches during a freeze" without the how-to-prevent).
2. If a duplicate PR is confirmed, the CEO's decision to close/keep it is recorded in the cycle report.
3. No branch was created or pushed by this task (cap absolute).

**Report to CEO at task end:** culprit + evidence, lesson written, duplicate-PR recommendation, status.

## Conclusion (formal, evidence-cited — 2026-08-12, cycle 6 close-out)

**Verdict: none — no agent opened any branch in-session. All 6 open vnstock-advisor branches
were opened by the orchestrator's lane queue.** The "cap violation" claim (flagged a third
time this cycle) is a misreading; the cap was exceeded only by the lane batch, and the real
defect is orchestrator-internal cap enforcement.

**(a) Origin of the 6 open branches — per `.orchestrator/pr-queue.json` openedAt (all
`local: false`, no in-session actor):**

| PR | branch | author | openedAt (Z) |
|----|--------|--------|--------------|
| 11 | vnstock-advisor-5-dev-analysis-engine-dev | dev | 2026-08-10T22:27:39 |
| 13 | vnstock-advisor-4-dev-data-ingest | ingest | 2026-08-11T08:51:17 |
| 14 | vnstock-advisor-4-dev-data-ingest-dev | dev | 2026-08-11T08:51:20 |
| 15 | vnstock-advisor-5c-dev-ranking-dev | dev | 2026-08-11T11:06:36 |
| 16 | vnstock-advisor-14-dev-data-ingest-security-gate-dev | dev | 2026-08-11T12:18:09 |
| 17 | vnstock-advisor-15-dev-analysis-engine-security-gate-dev | dev | 2026-08-11T12:18:12 |

Timestamps form three orchestrator lane-queue batches (08-10 22:27; 08-11 08:51 [PRs 13/14 —
3 s apart]; 08-11 12:18 [PRs 16/17 — 3 s apart]). `.orchestrator/activity.json` `recent`
shows ONLY `ceo` (cycle runs) and `tester` (drain runs) — no DEV/PM/BA/QA session was live
when any branch opened; `logs/orchestrator.log` shows the cap gate mechanically active and
holding ("PR cap reached — no new task branches this cycle", "lane queue: ALL DEVs held
back", open:6 cap:3) across every cycle. No agent opened a branch in-session.

**(b) Duplicate-race root cause:** PRs 13/14 are a 3-second duplicate race (08:51:17Z vs
08:51:20Z) on the same data-ingest task (`vnstock-advisor-4-dev-data` vs
`vnstock-advisor-4-dev-data-ingest`, authors `ingest` vs `dev`) — the lane queue dispatched
two near-simultaneous branch opens for the same seam with no dedupe window. TECHLEAD's
canonical-lineage ruling (reviews/vnstock-advisor-4-dev-data-ingest.md): PR 14 is a strict
subset of PR 13, both superseded by PR 16.

**(c) Cap-enforcement defect location:** the orchestrator's lane queue (batch dispatch
without a cap check/dedupe before each open), NOT any agent. Cap 3 was exceeded (6 open)
by the lane batch alone; no agent-side action could have opened these (all `local: false`,
`actor: ""`, no agent session contemporaneous).

**(d) Recommended mechanical fix (to the orchestrator/CEO, not agent discipline):**
close the 4 superseded PRs 11/13/14/15 per TECHLEAD's canonical-lineage rulings
(reviews/vnstock-advisor-5-dev-analysis-engine.md → close 11; reviews/
vnstock-advisor-4-dev-data.md → close 13; reviews/vnstock-advisor-4-dev-data-ingest.md →
close 14; reviews/vnstock-advisor-5c-dev-ranking.md → close 15) — closing drops the count
6→2 and lifts the freeze. Then transcribe TESTER/QA verdicts onto `.orchestrator/pr-queue.json`
so the machine gate sees: PR 17 merge-ready (TESTER PASS + QA GO on record,
backlog lines 13/18) and PR 16 DEV-fix-required (TESTER FAIL F1–F6, backlog line 17 +
`vnstock-advisor-14-dev-data-ingest-security-gate-fix`). Root-cause fix for the defect in
(c): the lane queue must re-check the open-PR count and dedupe by taskId/branch BEFORE
opening each branch in a batch.

**(e) Lesson reference:** the §7.3 lesson is already recorded on `lessons/ceo.md`
(2026-08-12): "activity.json shows ALL 6 open PRs were opened by the orchestrator's lane
queue (actor: orchestrator; PRs 13/14 are a 3-second duplicate race) — no agent opened a
branch in-session… the real defect is orchestrator-internal cap enforcement." Per the
close-out scope (single-purpose, do not modify other files) and because the culprit is the
orchestrator — not DEV or PM — no `lessons/dev.md`/`lessons/pm.md` entry was warranted or
written; the acceptance-criteria lesson requirement is satisfied by the referenced ceo.md
entry. AC-4: PRs 13/14 confirmed duplicates — CEO/TECHLEAD already ruled close-superseded
as hygiene (not cap-gaming); the recommendation above repeats that ruling for the
orchestrator to execute. Test plan: no branch was created or pushed by this task (cap
absolute); lesson is dated, concrete, and actionable (dedupe + pre-open cap re-check).
