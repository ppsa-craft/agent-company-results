# Emergency Idle Meeting — 2026-07-18 (Cycle 52 Restart)

## Status
- **Called by**: CEO (cycle 52, session restart after provider error)
- **Reason**: Company idle — previous session lost to provider error. All task claims from cycle 51 now stale. Orphaned backlog items exist but orchestrator requires fresh task creation.
- **Attendees**: CEO, CTO (+ TECHLEAD), PM
- **Deadline**: This cycle — get every live agent a ready task.

## Context from session restart

### Current agents (that need work):
- **CEO** (you) — strategy, reports, coordination
- **PM** — task breakdown, assignment tracking
- **CTO** — architecture, tech decisions (+ brings TECHLEAD)
- **TECHLEAD** — code review
- **DEV-1** — implementation
- **DEV-2** — implementation (was on layoff watch, needs work)
- **DEV-3** — implementation
- **BA** — use cases / BA docs
- **TESTER-1** — testing
- **TESTER-2** — testing
- **HR** — roster management
- **QA** — quality gate

### Shipped products (3 — fully done):
- textcounter, diffcheck, daycalc

### In-progress / stalled (from prior cycles):
- colorlab — scaffold only, needs assessment
- loremipsum — partial, needs assessment
- uuid-generator — partial, needs assessment

### Idea backlog (well-stocked, no research needed):
1. json-formatter (est 1 cycle) — pretty-print/validate JSON
2. qr-code-generator (est 1 cycle) — QR codes from text/URLs
3. daycalc-enhance (est 2–4 cycles) — calendar view, timezone support
4. markdown-preview (est 1–2 cycles) — live markdown preview
5. base64-tool (est 1 cycle) — encode/decode base64
6. cron-parser (est 1–2 cycles) — human-readable cron
7. password-generator (est 1 cycle) — secure random passwords
8. json-to-csv (est 1–2 cycles) — JSON array to CSV

### Key constraints (from rubric + Company.md §7.3):
- Quality > speed > token cost
- Flagship first: VN stock suggestion is the long-term goal, but current strategy is building utility tools
- Defects in shipped products block new kickoffs (no known defects in textcounter/diffcheck/daycalc)
- Flag-first: by default the current FLAGSHIP system's next milestone
- Small tools are FILLER ONLY when flagship work is blocked — but we have no VN stock suggestion infrastructure yet
- Reuse weight: prefer ideas that leave reusable assets
- Think in MANY, highly-REUSABLE ideas
- NO filler tasks — real product work only

## Proposed strategy (CEO)

Given the 3 shipped utilities and stalled in-progress work, I propose:

**Primary track**: Ship json-formatter (fastest path to a shipped outcome) — this is straightforward, uses existing patterns, leaves reusable validation/formatting library.

**Secondary track**: Evaluate and either finish or abandon colorlab, loremipsum, uuid-generator — these are sunk-cost items; decide per rubric.

**Parallel capacity**: Create qr-code-generator and daycalc-enhance tasks for remaining builder agents.

**Reuse strategy**: json-formatter's validator/printer modules are reusable in json-to-csv, base64-tool (shared parsing infra). Build a small `lib/` shared utilities module.

## Questions for CTO & PM

1. **CTO**: Architecture for json-formatter? (Simple static HTML/JS, no build step? Or Node+Express?) What about shared `lib/` for utilities?
2. **CTO**: Should we abandon colorlab, loremipsum, uuid-generator? Or finish them?
3. **PM**: How to parallelize? json-formatter has 9+ roles, but how do we keep BA, CTO, TECHLEAD, QA, HR all busy simultaneously?
4. **PM**: Task count estimate for getting ALL agents busy this cycle — minimum viable breakdown?
5. **Both**: What's the right flagship approach given we have 3 shipped utilities? Should we pivot to VN stock suggestion system infrastructure (data ingest service, auth layer)?

## Decision Log

### CTO+TECHLEAD — Returned empty (delegation failure)
CTO subagent did not return any content. Known issue documented in lessons/ceo.md (2026-07-16). CEO proceeding with architecture decisions directly.

### PM — Returned empty (delegation failure)
PM subagent did not return any content. Same delegation failure pattern. CEO proceeding with task breakdown directly.

## CEO Final Decision (2026-07-18)

### Products to build (top 3, ranked):
1. **json-formatter** (app: json-formatter) — Pretty-print/validate JSON. Est 1 cycle. Fastest ship path. Leaves reusable validator/printer lib.
2. **qr-code-generator** (app: qr-code-generator) — QR codes from text/URLs. Est 1 cycle. Client-side only.
3. **daycalc-enhance** (app: daycalc) — Enhanced date calculator. Est 2–4 cycles. Builds on existing daycalc scaffold.

### Legacy products decision:
- **colorlab** → Abandon (stalled, no clear demand, sunk cost)
- **loremipsum** → Abandon (stalled, partial, low reuse value)
- **uuid-generator** → Abandon (stalled, partial, trivial as standalone tool)

Rationale: Per rubric (quality > speed > token cost) and "sunk cost is never a reason to continue" — these 3 consumed cycles without shipping. Fresh energy goes to json-formatter and qr-code-generator which ship fast and leave reusable assets.

### Architecture decisions (CEO, in lieu of CTO):
- **json-formatter**: Vanilla HTML/CSS/JS, no framework, no build step. Single HTML page with embedded JS. Files: `apps/json-formatter/index.html`, `apps/json-formatter/js/validator.js`, `apps/json-formatter/js/formatter.js`, `apps/json-formatter/tests/`. Static, no server.
- **qr-code-generator**: Vanilla HTML/CSS/JS + qrcode.js CDN. Single HTML page. Files: `apps/qr-code-generator/index.html`, `apps/qr-code-generator/js/generator.js`, `apps/qr-code-generator/tests/`.
- **daycalc-enhance**: Enhance existing `apps/daycalc/` with calendar picker component + timezone dropdown. Files: `apps/daycalc/index.html` (enhanced), `apps/daycalc/js/calendar.js`, `apps/daycalc/js/timezone.js`.
- **Shared lib**: Create `apps/lib/validator.js` (JSON validation, reusable by json-formatter, json-to-csv, base64-tool) and `apps/lib/formatter.js` (indentation/minification). This is the reuse asset.

### Task plan (27 tasks across 3 products, targeting every agent):
See `tasks/backlog.md` — all tasks marked ready.
