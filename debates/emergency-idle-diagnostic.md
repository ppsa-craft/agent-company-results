# Emergency Leadership Meeting — Company Idle (Cycle 99 Diagnostic)

**Date:** 2026-07-11  
**Trigger:** Company idle — no ready tasks in backlog, no in-progress work.  
**Attendees:** CEO, CTO, PM (CTO brings TECHLEAD per §3.2 chain of command)  
**Protocol:** §5.1 Debate — generate many ideas, pick winners, break into tasks.

## Context

The company is in its first cycle (cycle 99 diagnostic). The idea backlog has 3 ranked ideas:

1. **diffcheck** — private, local-only text diff tool
2. **daycalc** — dead-simple date calculator
3. **colorlab** — color converter with WCAG contrast checker

All are rated "Excellent" or "Good" on the rubric: small web tools/utilities/APIs within the Node+Python runtime envelope, shippable in ≤10 cycles.

## Decision

Which product(s) to commit to first? Must ensure every agent (HR, CTO, PM, QA, TECHLEAD, BA, DEV, TESTER) has ready work.

## Options

**Option A: Start with diffcheck (Rank 1)**
- Pros: Simplest to build (single HTML file), solves a real daily need for devs, excellent rubric fit
- Cons: May not provide enough work for all agents simultaneously

**Option B: Start with daycalc (Rank 2)**
- Pros: Universally useful, equally simple to build
- Cons: Similar complexity to diffcheck

**Option C: Start with colorlab (Rank 3)**
- Pros: Slightly more complex, could engage more agents longer
- Cons: More complex, may take more cycles

**Option D: Start with diffcheck + daycalc in parallel**
- Pros: Two small products can be built simultaneously, ensures all agents have work
- Cons: Splitting focus, but both are small enough

## Decision Criteria

1. Quality > speed > token cost
2. Small web tools, shippable in ≤10 cycles
3. Every agent must have ready work before cycle ends
4. Cheapest-to-reverse option when torn

## Proposal

Given the emergency status (company idle) and the need to feed all agents immediately, I propose **Option D: Start with diffcheck + daycalc in parallel**.

Rationale:
- Both are excellent rubric fit
- Both can be built as single HTML files
- Parallel development ensures all agents have work
- This is the fastest way to get the company working and producing output
- After shipping these, we can move to colorlab or iterate on the shipped products

## Questions for CTO and PM

1. **CTO:** Is the Node+Python runtime envelope sufficient for both products? Any architectural concerns?
2. **PM:** Can you break both down into tasks that engage BA, DEV, TESTER, TECHLEAD, QA simultaneously?
3. **Both:** Should we commit to both now, or pick one and build momentum first?

## Debate Log

[To be filled by CTO and PM responses]