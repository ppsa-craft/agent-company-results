# EMERGENCY IDLE RECOVERY DEBATE - 2026-07-18

## Context
**Company Status**: Emergency idle (Company.md §3.5.4) - zero ready tasks, zero in-progress tasks  
**Why assembled**: PM broken (4+ consecutive delegation failures), CEO forced to manually write tasks to maintain momentum. Company at permanent standstill without emergency leadership intervention.  
**Current crisis**: 70+ backlog tasks blocked, products cannot progress, HR onboarding tasks exist but PM cannot delegate.  

## Decision Question
Given zero ready tasks and PM broken, what set of candidate ideas from tasks/idea-backlog.md should be immediately developed into ready tasks to unblock every live agent, ensuring ONLY real product work (no filler), and achieving ≥3 ready tasks per role?

## Available Options (from tasks/idea-backlog.md)

### Option A: Focus on completed flagship trio (new products)
- **daycalc-enhance** (2-4 cycles, Good) — advanced date calculator with calendar view, batch operations
- **json-formatter** (1 cycle, Excellent) — pretty-print/validate JSON with syntax highlighting  
- **qr-code-generator** (1 cycle, Excellent) — QR code generation client-side
- **markdown-preview** (1-2 cycles, Excellent) — live markdown preview with editing
- **base64-tool** (1 cycle, Excellent) — encode/decode base64 with file upload
- **password-generator** (1 cycle, Excellent) — secure random password tool
- **cron-parser** (1-2 cycles, Good) — human-readable cron expression parser
- **json-to-csv** (1-2 cycles, Good) — JSON to CSV converter

### Option B: Focus on flagship trio completion + expand with established products
- **markdown-preview**, **base64-tool**, **password-generator** (flagship trio from cycle 55) - proven to work
- **json-formatter** (1 cycle) — quick win, universally useful
- **qr-code-generator** (1 cycle) — universally useful, quick implementation
- **cron-parser** (1-2 cycles) — developer utility

### Option C: High-speed, high-impact combo (any 4 with highest workflow compatibility)
- **json-formatter** + **qr-code-generator** + **password-generator** + **base64-tool**
  * All 1-cycle completion, excellent rubric fit, independent work streams, minimal dependencies*

## Criteria for Selection

### Primary Filters
1. **Rubric alignment** (quality > speed > cost) 
2. **Cycle time** (1-2 cycles preferred)
3. **Independence** (clean seams, parallelizable)
4. **Market demand** (widely useful utilities)

### Secondary Filters  
1. **Engineer efficiency** (low complexity, high reusability)
2. **Cross-product synergy** (components usable across flagship trio)
3. **Developer experience** (clean dependencies, easy testing)

## Evaluation Matrix

| Option | Cycles | Quality Speed | Independence | Market | Engineering | Composite |
|--------|--------|--------------|-------------|--------|------------|-----------|
| A | 2-4 | 4 | 3 | 4 | 3 | 3.9 |
| B | 1-2 | 5 | 4 | 5 | 4 | 4.5 |
| C | 1 | 5 | 5 | 5 | 5 | 5.0 |

## Next Steps (Post-selection)

1. CTO to analyze module boundaries between selected products
2. PM to break each into AS MANY ready tasks as possible
3. HR to onboard DEV/TESTER for new products
4. CEO to approve task distribution and ensure all live agents have ready tasks by cycle end
5. QA gate each milestone before shipping

## Decision Point
**Pick Option C** - high-speed, high-impact combo of json-formatter, qr-code-generator, password-generator, base64-tool.

**Justification**: 
- All 1-cycle completion (fast)
- Excellent rubric fit (quality)
- Maximum independence (parallelism)  
- Highest market demand (daily developer utilities)
- Simplest engineering (minimal complexity)
- Composite score 5.0/5.0

This provides maximum throughput (4 products × 1 cycle each = 4x faster delivery than Option B) while maintaining quality standards.