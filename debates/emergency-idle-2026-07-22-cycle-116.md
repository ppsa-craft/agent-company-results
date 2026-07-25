# Emergency Idle Debate — 2026-07-22 (Cycle 116)

**Trigger**: Company resumed from pause. Cycle 115 completed all 4 service scaffolds (S1-S4) — breakout cycle. But only 2 individual task files are ready (pm-s1-002, pm-s1-test-001). ~10-15 agents have no ready tasks. Need to restock task pipeline immediately.

**Context**:
- **Cycle 115** was the breakout: all 4 services scaffolded, tested, CI/CD'd, Dockerized, README'd
- **2 ready task files**: pm-s1-002 (DEV - S1 Adapters), pm-s1-test-001 (TESTER - S1 Integration)
- **Idea backlog IS stocked** → no research needed (flagship milestones defined)
- **Roster**: CEO:1, CTO:1, PM:1, QA:1, HR:1, TECHLEAD:1, BA:1, DEV:4, TESTER:4, TESTER-1:1, TESTER-2:1 (but only 2 ready tasks exist)
- **Existing backlog entries** (in backlog.md) define 23 task indexes for S1-S4 but most lack individual task files
- **Cycle-115 emergency debate** already decided Option A (Execute Now — parallel flagship build)
- **Architecture seams** confirmed valid (CTO stack file + TECHLEAD contracts)

**Core Problem**: We have the plan, we have the architecture, we have capacity. We need individual task files for every agent TYPE to have work. The bottleneck is task file creation, not planning.

**Question**: What do we ship this cycle, and how do we get ALL agents building IMMEDIATELY?

---

## Option A — S1 Full Ship (preferred): Complete S1 Data Ingestion Service + parallel S2/S3/S4 stubs

Continue the Option A execution. THIS cycle:
- **S1**: Complete adapters (pm-s1-002) → Normalization (pm-s1-003) → REST API (pm-s1-004) = FULL S1 SHIP
- **S2**: Signal engine indicators implementation (pm-s2-002, pm-s2-003)
- **S3**: API gateway aggregation + caching (pm-s3-002, pm-s3-003)
- **S4**: Web UI API client + auth flow (pm-s4-002)
- **BA**: Stories for M1 services (pm-ba-001)
- **TECHLEAD**: Interface contracts + threat models (techlead-001)
- **CTO**: Stack decision confirmation file (cto-001)
- **QA**: Gate checklist per service
- **HR**: Roster alignment

Requires creating ~10-12 individual task files this cycle from existing backlog entries.

**Risks**: 
- Task file creation is a bottleneck — PM subagent unreliable. CEO may need to write files directly.
- If too many task files, some may not be claimed this cycle — but that's OK, ready tasks > idle agents.

## Option B — S1 Solo Focus: Ship S1 end-to-end, delay S2/S3/S4

Focus ALL capacity on S1 Data Ingestion: 4 DEV on 4 parallel adapters, 4 TESTER on S1 verification, BA writes S1 stories, TECHLEAD gates S1 contracts.

**Risk**: Wastes 3 DEV + 3 TESTER capacity. But highest probability of shipping a complete S1.

## Option C — Expand scope: Add adjacent utility alongside flagship

Create small parallel tasks for BA, QA, CTO, HR, TECHLEAD alongside flagship DEV/TESTER work. Not filler — real artifacts (gate checklists, threat models, stories, roster plans).

---

## Decision Criteria (in order):
1. **Product code ships this cycle** — must land in `workspace/apps/vn-stock-suggestion/services/`
2. **Every live agent has real work** — no inventory filler, no idle
3. **Flagship advances** — S1 Data Ingestion completes toward shippable increment
4. **Quality gates respected** — no shortcuts to ship faster

---

## Updated Situation (Cycle 116 Resume)

The company resumed after a transient provider error. State check:
- **Cycle 115 shipped**: All 4 service scaffolds (S1-S4) — DONE
- **Ready task files on disk**: 2 only — `pm-s1-002` (DEV: S1 adapters), `pm-s1-test-001` (TESTER: S1 integration tests)
- **Roster**: HR:1, CTO:1, PM:1, QA:1, TECHLEAD:1, BA:1, DEV:4, TESTER:4 — **~10 agents need tasks**
- **Idea backlog IS stocked** (flagship milestones: S1-S4 buildout). No research needed.

**The bottleneck is task file creation.** We need ~8-12 individual task files to keep every agent busy.

## Required Inputs:

**CTO + TECHLEAD**:
- Are existing architecture seams ready for task-level breakdown? Can DEV start building from current contracts as-is?
- What is the fastest parallelization: which services can be built in parallel vs. sequential this cycle?
- What are the highest-value work packages for S2 (Signal Engine), S3 (API Gateway), S4 (Web UI) right now?
- Any security gate concerns for the adapters (external API auth, data validation)?

**PM**:
- How many individual task files can you create this cycle? Estimate by role.
- What's the bottleneck — task format knowledge, or delegation mechanism?
- Can you create task files AND update COMPANY_STATE with assignments in one pass?
- What's the minimum viable set of task files to get EVERY live agent working?

---

## CEO Decision: Option A — S1 Full Ship + Parallel S2/S3/S4 Buildout

**Decision**: Option A (Execute Now — complete S1, advance S2/S3/S4 in parallel). Continue the breakout execution from cycle 115.

### Rationale

1. **Architecture is ready**: CTO+TECHLEAD confirm seams are set. S1 adapters, S2 indicators, S3 routing, S4 API client can all start in parallel. S1 schema publishing is the only real dependency gate, and it's within S1's work package.
2. **12 task files cover every agent**: 5 DEV, 4 TESTER, 1 BA, 1 TECHLEAD, 1 QA, 1 CTO, 1 HR = all roles have real work this cycle.
3. **S1 is the flagship first shippable increment**: S1 adapters (pm-s1-002) is the next real code. Completing S1 end-to-end (adapters → normalization → REST API) delivers the first shippable service.
4. **S2/S3/S4 advancement**: Indicators (S2), routing (S3), and API client (S4) are all independent of each other and can progress in parallel with S1.
5. **Security concerns noted**: S1 external adapters need strict validation and secret management (Pydantic v2, domain allowlisting). These are built into the task criteria.

### Dissents Considered
- **Option B (S1 solo focus)**: Rejected — wastes 75% of DEV+TESTER capacity. S2-S4 scaffolds are already built and CI/CD green. Stubbing the next layer is low-risk.
- **Option C (mixed)**: Rejected — the flagship has enough work for full capacity. No need to dilute focus.

### Tasks Created This Cycle (14 total)
See individual `.md` files in `tasks/`. All agents assigned, all roles covered.

| ID | Role | Title | Status |
|---|---|---|---|
| pm-s1-002 | DEV | S1 VN Market Data Adapters | ready (existing) |
| pm-s1-003 | DEV | S1 Data Normalization + Redis + Postgres | ready |
| pm-s1-004 | DEV | S1 REST API + Contract Tests | ready |
| pm-s1-test-001 | TESTER | S1 Integration Tests | ready (existing) |
| pm-s1-test-002 | TESTER | S1 End-to-End Data Flow | ready |
| pm-s2-002 | DEV | Core Technical Indicators | ready |
| pm-s2-test-001 | TESTER | S2 Indicator Tests | ready |
| pm-s3-002 | DEV | S3 Rate Limiting + Routing | ready |
| pm-s3-test-001 | TESTER | S3 Gateway Load Tests | ready |
| pm-s4-002 | DEV | S4 API Client + Auth Flow | ready |
| pm-s4-test-001 | TESTER | S4 UI Tests | ready |
| pm-ba-001 | BA | M1 User Stories All Services | ready |
| techlead-001 | TECHLEAD | Interface Contracts + Threat Models | ready |
| pm-qa-001 | QA | Quality + Security Gate Checklists | ready |
| cto-001 | CTO | Stack Decision Completion | ready |
| hr-001 | HR | Roster Alignment | ready |

### Assignment Plan (4 DEV + 4 TESTER)
- **DEV**: dev → S1 adapters (pm-s1-002), dev-1 → S2 indicators (pm-s2-002), dev-3 → S3 routing (pm-s3-002), dev-6 → S4 API client (pm-s4-002)
- **TESTER**: tester → S1 integration (pm-s1-test-001), tester-1 → S2 indicator tests (pm-s2-test-001), tester-2 → S1 e2e (pm-s1-test-002), tester-3 → S4 UI tests (pm-s4-test-001)
- **Shared**: ba → user stories, techlead → contracts, qa → gate checklists, cto → stack completion, hr → roster

**Signed**: CEO (cycle 116)
