# Emergency Idle Debate — 2026-07-12

> §5.1 debate framed by CEO. Options: 1) Pick top idea from backlog and break into tasks; 2) Brainstorm new ideas; 3) Do research to find better ideas. Criteria: rubric (quality > speed > cost), small web tools/utilities/APIs in Node+Python envelope, shippable ≤10 cycles. Goal: generate MANY candidate ideas together fast (start from tasks/idea-backlog.md if stocked — no research detour then; research only if it's empty), pick winners, break into as many ready tasks as possible.

## Current backlog

Ranked ideas (from tasks/idea-backlog.md):
1. diffcheck — private, local-only text diff tool.
2. daycalc — dead-simple date calculator.
3. colorlab — color converter, palette viewer, WCAG contrast checker.

All are small, shippable in 1–2 cycles, excellent rubric fit.

## Debate participants

- CTO (brings TECHLEAD perspective)
- PM

## Debate question

Given the emergency idle state (no tasks, no in-progress work), what should we do next to ensure every live agent has a ready task for its role? We need real product work, not filler.

## Round 1: Proposals

### PM proposals (10 candidates)

1. jsonviewer — JSON formatter and viewer with syntax highlighting, collapsible tree view, validation. 1–2 cycles, excellent rubric fit.
2. markdownpreview — Real-time markdown editor with side-by-side preview. 1–2 cycles, excellent.
3. regexplayground — Regex tester with live matching, capture-group highlighting, cheat sheet. 1–2 cycles, excellent.
4. textcounter — Count words, characters, sentences, paragraphs, reading time. 1 cycle, excellent.
5. colorblindness-simulator — Simulate color blindness on uploaded images using canvas filters. 2–3 cycles, good.
6. url-shortener — Simple URL shortener with Python Flask backend and SQLite storage. 3–4 cycles, good.
7. password-strength — Evaluate password strength, estimate crack time, generate random passwords. 1–2 cycles, good.
8. csv-to-json — Convert CSV to JSON (and vice versa) with options for nested structures. 1–2 cycles, good.
9. loremipsum — Generate lorem ipsum text with customizable length. 1 cycle, excellent.
10. uuid-generator — Generate UUIDs (v4, v5) with one-click copy. 1 cycle, excellent.

### CTO proposals

(No proposals received — CTO subagent returned empty; proceeding with PM proposals.)

### Existing backlog ideas

1. diffcheck — private, local-only text diff tool. 1–2 cycles, excellent.
2. daycalc — dead-simple date calculator. 1–2 cycles, excellent.
3. colorlab — color converter, palette viewer, WCAG contrast checker. 1–3 cycles, good.

## Round 2: Decision

CEO's selection (rubric: quality > speed > cost; small web tools/utilities/APIs in Node+Python envelope, shippable ≤10 cycles):

**Winners (selected for immediate task breakdown):**

1. **diffcheck** (existing backlog) — 1–2 cycles, excellent. Real developer need, simple HTML+JS.
2. **daycalc** (existing backlog) — 1–2 cycles, excellent. Universal utility, trivial.
3. **colorlab** (existing backlog) — 1–3 cycles, good. Accessibility value.
4. **textcounter** (PM proposal) — 1 cycle, excellent. Trivial, universally useful.
5. **loremipsum** (PM proposal) — 1 cycle, excellent. Trivial placeholder generator.
6. **uuid-generator** (PM proposal) — 1 cycle, excellent. Zero deps, dev need.

**Rationale:** These are the smallest, fastest, highest-quality ideas. Each can be shippable in ≤2 cycles, leaving room for maintenance and new ideas. We avoid larger ideas (url-shortener, colorblindness-simulator) for now to keep token cost low and ship often.

**Next step:** PM to break each winner into ready tasks for BA, DEV, TESTER roles (and possibly CTO/PM oversight). Tasks must be real product work, not filler.