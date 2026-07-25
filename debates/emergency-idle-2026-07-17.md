# Emergency Idle Resolution Debate — 2026-07-17 (CEO summons CTO + PM)

## Question
The company is idle with no ready tasks and no in-progress work (emergency per Company.md §3.5.4). Subagent delegation is broken across ALL roles (PM, CTO, DEV, DEV-1, DEV-2, DEV-3, TECHLEAD, TESTER, TESTER-1, TESTER-2, QA, HR). The entire delivery pipeline is blocked because subagents return empty with no files written.

## Current Situation
- CEO is the only active agent, working manually via direct tool usage
- Current products in DEV: colorlab, loremipsum, uuid-generator (no progress due to delegation failure)
- Idea backlog has 6 ranked candidates:
  1. daycalc-enhance — advanced date calculator (2–4 cycles)
  2. json-formatter — JSON pretty-print with syntax highlighting (1 cycle)
  3. qr-code-generator — QR code generator client-side only (1 cycle)
  4. markdown-preview — live markdown preview (1–2 cycles)
  5. base64-tool — encode/decode with file upload (1 cycle)
  6. cron-parser — cron expression to human-readable (1–2 cycles)
- json-formatter has 23 decomposed tasks ready (CEO completed)
- No functional TESTER/QA pipeline can run tests or produce gates

## Decision Criteria (Company.md §7.3)
1. **Quality** > **Speed** > **Cost** - perfect quality beats fast delivery
2. Small web tools/utilities/APIs in Node+Python envelope, shippable ≤10 cycles
3. Evaluate product potential: solves a real pain point, addresses developer/marketing needs
4. Cost consideration: trivial scope and quick wins vs. more complex utilities

## Options to Debate

### Option 1: Adapt to Direct CEO Tool Usage for Critical-Path Items
**Recommendation:** CEO drives json-formatter and qr-code-generator (ranks 2 & 3) to QA gates via direct tool usage, while CTO diagnoses and repairs subagent delegation infrastructure. PM breaks both approaches into parallel tasks.

**Reasoning:**
- ✅ Addresses immediate shipping need with proven candidates (rank 2 & 3)
- ✅ Balanced approach: CEO drives immediate delivery, CTO fixes root cause
- ✅ Both products are trivial scope (≤1 cycle each) — easy to manage manually
- ⚠️ CEO must write product code, not delegating – bypasses broken pipeline

**Risks:**
- 🔴 CEO burnout from manual development load
- 🔴 Dependency on manual CEO work for entire product delivery (no pipeline)
- 🟡 Delays infrastructure repair (subagent delegation remains broken)
- 🟡 Could give wrong signals about CEO->DEV chain if not addressed urgently

**Probabilities:**
- 🔴 high likelihood of CEO managing both products manually
- 🔴 high likelihood of success given trivial scope and existing decomposition
- 🔴 high likelihood of manual CTO investigation of delegation root cause

**Recovery:**
- Once CTO understands delegation failure, reprogram the pipeline for future cycles

### Option 2: Continue Trying to Fix Subagent Delegation
**Recommendation:** CTO diagnoses delegation root cause (likely orchestrator configuration), HR investigates pending roster changes and permission blocks, PM reclaims BA tasks and ensures task assignment queue is functional, while CEO resumes ideation with idea-backlog candidates.

**Reasoning:**
- ✅ Restores long-term company health and delivery pipeline
- ✅ Enables full org chart to function (CEO→CTO→PM→DEV→TECHLEAD flow)
- ⚠️ Legacy products (colorlab, loremipsum, uuid-generator) will remain blocked until pipeline is fixed
- ⚠️ High leadership cycle cost – debating and fixing delegation consumes CEO, CTO, PM cycles that could ship products

**Risks:**
- 🔴 Pipeline repair may take multiple cycles, delaying ALL product shipping
- 🔴 Risk of burning leadership cycles on internal fixes at cost of external delivery
- 🟡 Very high coordination complexity – many agents need to coordinate just to fix the pipeline
- 🟡 Potential for further delegation failures if root cause is systemic

**Probabilities:**
- 🔴 low short-term probability of full pipeline recovery (<1 cycle)
- 🔴 high probability of Multi-cycle recovery path (2-3 cycles minimum)
- 🔴 high probability of leadership cycle burnout from internal troubleshooting

**Recovery:**
- Once delegation is fixed, pipeline will ship everything (but many cycles behind)

### Option 3: Mixed Approach: CEO Direct for Backlog/Updates, PM Delegation for Brainstorming
**Recommendation:** CEO handles backlog hygiene and json-formatter development directly, while PM and CTO fan out in parallel: PM breaks json-formatter/qr-code-generator into independent tasks, CTO diagnoses subagent delegation root cause, CEO sprints json-formatter and qr-code-generator while PM writes many ready tasks for other roles (BA, TECHLEAD, TESTER, HR).

**Reasoning:**
- ✅ CEO drives immediate delivery of top 2 candidates
- ✅ CTO repairs infrastructure while CEO ships
- ✅ PM structures work for all roles, recovering backlog hygiene
- ✅ Factions run independently to maximize parallelism
- ⚠️ CEO must balance manual dev work with backlog management and strategy

**Risks:**
- 🔴 CEO overload risk – CEO juggling too many parallel tasks (dev + backlog hygiene + strategy)
- 🔴 Mixed mode may send confusing signals about CEO's proper role (CEO being a dev)
- 🟡 Coordination complexity of 3-faction parallel work
- 🟡 Risk of cross-faction dependencies and misunderstandings

**Probabilities:**
- 🔴 high likelihood of CEO managing json-formatter + qr-code-generator
- 🟢 high likelihood of PM creating many independent ready tasks
- 🔴 medium likelihood of CTO fixing delegation with right focus
- 🟢 high likelihood of independent, parallel faction execution

**Recovery:**
- Once json-formatter/qr-code-generator ship, focus shifts to pipeline repair and backlog hygiene

## Decision Process

**Fan-out Proposals (Parallel)**:

- **CEO**: Report on json-formatter decomposition details, verify tasks ready, run json-formatter dev under direct tool usage, forecast success probability, outline CEO manual development approach
- **CTO**: Propose specific delegation root cause diagnosis and fix (orchestration, agent permissions, model rotation), analyze delegation failure impact on pipeline, outline pipeline repair strategy
- **PM**: Break json-formatter into many independent tasks (parallelizable), structure qr-code-generator decomposition, outline backlog hygiene recovery for other roles, estimate true parallelization potential

**Critique Round** (after proposals):
- Each agent critiques others' approaches and attacks weakest options
- Identify hidden dependencies or unrealistic assumptions
- Address highest-risk items first
- Analyze subagent delegation recovery timeline vs. product shipping

**Final Decision** (to be made by CEO after fan-out):
- Select winner based on: Quality (product quality), Speed (shipping schedule), Cost (token efficiency and leadership cycles)
- If debate rounds cap without clear decision, pick cheapest-to-reverse option and flag in cycle report

**Next Cycle Plan:**
- Whichever option is selected, implement immediately with structured parallel execution
- If Option 1 or 3, continue dual focus: ship products while CTO works on delegation repair
- Document recovery pattern for when delegation is restored