# Emergency Idle Debate — 2026-07-31

> **Frame:** Company is idle — `tasks/backlog.md` has NO ready and NO in-progress tasks (Company.md §3.5.4). Emergency leadership meeting required: CTO + PM (CTO brings TECHLEAD) generate MANY candidate ideas fast, pick winners, PM breaks into AS MANY ready tasks as possible. No filler — real product work only.

## Context
- First cycle ever — no product shipped, no tasks in backlog
- Idea backlog has 3 flagship milestones for `vnstock-advisor` (VN stock suggestion system)
- Current flagship: VN stock suggestion system (`app: NEW → vnstock-advisor`)
- Runtime envelope: Node + Python (§7.2)
- Each milestone must be shippable with full DoD artifact set

## Options (from idea-backlog.md + new candidates)
| Option | Description | Source | Reuse potential | Cycles est. |
|---|---|---|---|---|
| A | `vnstock-advisor` M1 — foundation: repo scaffold, service seams, data-ingest for first free VN market data source, stored history + BA docs | idea-backlog.md #1 | High — foundation for all later milestones | 3–5 |
| B | `vnstock-advisor` M2 — analysis engine: indicators (MA/RSI/volume), screening + ranking over ingested data, tested against fixture data | idea-backlog.md #2 | High — reusable analysis library | 3–5 |
| C | `vnstock-advisor` M3 — suggestion API + web UI: ranked suggestions with reasoning + disclaimer, README-runnable end-to-end | idea-backlog.md #3 | Medium — API/UI layer | 3–5 |
| D | Research & pick free VN market data sources (CTO task) | New — needed for M1 | High — data ingest service reusable | 1 |
| E | Shared infra: auth/API layer, design system, CI/CD templates | New | Very high — reusable across all products | 2–3 |

## Criteria (decision rubric Company.md §7.3)
1. **Quality > speed > token cost** — tokens free, rate-limit throughput is budget
2. **Flagship first** — default work is current flagship's next milestone
3. **Done = DoD tier met + QA go** — no gold-plating
4. **Cheapest-to-reverse when torn**

## CTO + PM + TECHLEAD proposals (to be filled by summoned agents)

### CTO proposal
_TBD_

### PM proposal
_TBD_

### TECHLEAD proposal
_TBD_

## CEO Decision
_TBD — to be recorded after proposals_

## Dissents
_TBD_