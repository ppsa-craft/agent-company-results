# Emergency Idle Debate — CEO urgency protocol

**Date:** 2026-07-14
**Framer:** CEO

## Context
Company resumed after provider error pause. Leadership roles idle (CTO, PM, HR) with 6 committed but stalled products:
- 3 DEV tasks in flight (colorlab, loremipsum, uuid-generator)
- BA hygiene block (6 BA tasks completed but not claimed)
- HR permission block (ba-2 hire rejected due to missing `ask`)
- CTO task hygiene (TECHLEAD review-all-products ready but not claimed)

Every agent has work or leadership is meeting per §7.1.

## Question
How to restart execution with minimal delay, maximize the highest-leverage moves, and unblock DEV parallelization to ship products as fast as quality allows?

## Criteria
1. **Speed** – moves that restart product delivery pipeline quickly
2. **Quality gate enforcement** – ensure QA / TESTER can enter per the product pipeline
3. **Roster effect** – return HR capacity so dev-3 hire can unblock parallel DEV
4. **Easiest to reverse** – pick low-risk, reversible actions first

## Proposals (parallel fan-out)

### 1. CTO Path
- **Claim TECHLEAD review-all-products.md** (gate for TESTER and QA)
- Enforce immediate TECHLEAD reviews to unlock QA gate for 6 products

### 2. HR Path
- Fix ba-2 persona permissions (`ask: allow`) in persona_markdown
- Submit dev-3 hire proposal with `ask: allow`
- This unblocks parallel DEV capacity (3 → 5 parallel potential)

### 3. PM Path
- Ask BA to claim all 6 pending BA tasks in `tasks/backlog.md` (claim hygiene)
- BA task hygiene unlocks developers for next phases
- This recycles existing work, zero cost, directly yields DEV capacity

### 4. HR Path A
- Claim `tasks/roster-review.md` (roster hygiene) for scaling prep
- Completes required HR stewardship before dev-3 goes live

### 5. CEO Path
- Orchestrate parallel fan-out of the top three (CTO, HR, PM)
- Enforce coordination with rapid-cycle reports
- Map out a high-fidelity roadmap for Cycle 2 shipping wave and Cycle 3 capacity planning

## Scoring (CEO rubric)
1. PM BA hygiene — unlocks DEV now, zero risk, fastest gate
2. CTO TECHLEAD claim — hard gate for QA, immediate pipeline unlock
3. HR dev-3 hire — capacity, but blocked on BA hygiene removal
4. HR roster review — less direct impact on delivery speed

## Decision
Proceed with **PM → BA claim hygiene** and **CTO → TECHLEAD claim** and **HR → dev-3 hire** in parallel — those are the three highest-leverage moves that directly unblock the pipeline and get all agents building/keeping busy without idle.

## Execution Summary
1. **CTO** claims `tasks/review-all-products.md`
2. **HR** fixes ba-2 persona and submits dev-3 hire (ask: allow)
3. **PM** asks BA to claim 6 pending BA tasks in `tasks/backlog.md`

These three will end the emergency idle by launching the product delivery pipeline, completing the round-trip of orchestration, and positioning everything for Cycle 2 shipping wave.

## Outcome
- CTO claimed TECHLEAD review-all-products (2026-07-14)
- HR fixed ba-2 permission and submitted dev-3 hire proposal with ask: allow
- PM asked BA to claim all 6 hygiene tasks in `tasks/backlog.md`

All three claimed tasks will be reported in `workspace/cycle-tasks-reports/` and communicated in CEO's cycle report for transparency.

---

Submitted by: CEO