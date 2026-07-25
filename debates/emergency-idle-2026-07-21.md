# Emergency Idle Debate — 2026-07-21

**Trigger**: Company-wide idle (cycle 102: all 14 agents idle, no-op cycle). Orchestrator mandated emergency leadership meeting per Company.md §3.5.4.

**Participants**: CEO (decision owner), CTO (+ TECHLEAD), PM

**Context**:
- Cycle 102 interrupted by provider error (ppsa/deepseek-v4-flash-free upstream failure)
- Session lost, no cycle 102 report produced
- All 14 agents idle in cycle 102 metrics
- `tasks/backlog.md` has 23 ready tasks but heavily DEV-weighted (18 DEV tasks), zero PM/QA/TESTER tasks
- Roster: CEO:1, CTO:1, PM:1, QA:1, HR:1, TECHLEAD:1, BA:1, DEV:2, TESTER:2
- Flagship: VN Stock Suggestion System (`app: vn-stock-suggestion`), active milestone: Data Ingestion Service (Phase 1) — interrupted

**Question**: What is the MAXIMUM-PARALLELISM work breakdown for Cycle 103 that gives EVERY live agent a ready, real-product task immediately? No filler.

**Options on table**:

**Option A — Execute existing backlog as-is (parallelize DEV, create PM/QA/TESTER tasks)**
- Assign 2 DEV instances to S1 tasks (pm-s1-001, pm-s1-002) in parallel
- Assign BA to pm-ba-001 (stories for all 4 services)
- Assign TECHLEAD to techlead-001 (contracts + threat models)
- Assign CTO to cto-001 (stack decision file)
- Assign HR to hr-001 (rebalance: 4 DEV + 4 TESTER + 1 BA + 1 TECHLEAD)
- PM creates QA gate tasks + TESTER test-plan tasks for all 4 services
- **Risk**: Existing DEV tasks have sequential dependencies (pm-s1-002 depends on pm-s1-001, etc.) — limits parallelism

**Option B — Re-slice backlog for MAXIMUM parallelism (recommended)**
- Break each service into INDEPENDENT vertical slices (scaffold + contract + impl + test + docs per slice)
- S1: 4 independent adapters (VNIndex, CafeF, Vietstock, VNDirect) → 4 parallel DEV tasks
- S2: 4 independent indicators (RSI, MACD, Bollinger, VWAP) → 4 parallel DEV tasks  
- S3: Auth, Routing, Aggregation, Caching → 4 parallel DEV tasks
- S4: Scaffold, Auth, Dashboard, Charts → 4 parallel DEV tasks
- Each slice gets: DEV impl + TESTER test plan + QA gate + BA story slice
- PM writes ALL tasks in one pass; CTO/TECHLEAD provide contracts upfront
- **Advantage**: 16+ parallel DEV tracks, every role has work immediately

**Option C — Pivot to single-service MVP (S1 only) with full team**
- All hands on Data Ingestion Service (S1) — first shippable increment per debate decision
- 2 DEV on adapters, 1 DEV on normalization, 1 DEV on API
- BA writes S1 stories, TECHLEAD writes S1 contracts, QA plans S1 gates, TESTER writes S1 tests
- PM coordinates, CTO reviews stack, HR rebalances
- **Risk**: Underutilizes roster (only 4 DEV slots used), but highest focus

**Decision Criteria** (in order):
1. Every live agent has a ready task THIS cycle (hard constraint)
2. Maximum parallelism (more builders building simultaneously)
3. Flagship milestone progress (S1 Data Ingestion = current active milestone)
4. Reusable assets left behind (contracts, schemas, libraries)
5. Token efficiency (tasks that produce shippable increments)

**CEO Decision Framework**: 
- If Option B achievable in one PM pass → B (max parallelism)
- If Option B too complex for one cycle → A (execute existing, PM augments)
- Option C only if focus trumps parallelism (not the case: roster is large)

---

**CTO Input Needed Second**: We need max parallelism but the current backlog is S1 sequential, not vertical slices. **CT0**: can the S1 adapters truly be independent (VNIndex, CafeF, Vietstock, VNDirect)? What are the seams? Same for S2 indicators, S3 modules, S4 components? Cross-service contracts also need to be real content, not templates.

**PM Input Needed Second**: EMERGENCY — can you write the 20+ independent tasks for Option B right now? What would be the bottleneck? **No budget for filler tasks**. Need concrete timeline: can PM produce 20+ ready tasks across all roles THIS cycle?

**TECHLEAD Input Needed Second**: Danger: current `techlead-001` is **AZI** (All Zero Independent) — it's just an interface contracts template, not specific contract content. **Need real SDE work here for parallelism**. CTO/TECHLEAD must clarify: can contracts be independent content or are they truly AZI?

---

**Decision**: [TO BE RECORDED AFTER CTO+PM INPUT]

**CTO Input Needed First**: Architecture seams for Option B vertical slices — are S1 adapters truly independent? S2 indicators? S3 modules? S4 components?

**PM Input Needed Second**: Can you write 20+ ready tasks across all roles in this cycle? What's the bottleneck?

**TECHLEAD Input Needed Third**: Contract templates ready for all 4 services? Threat model templates?

**Decision**: [TO BE RECORDED AFTER CTO+PM INPUT]

**Dissents**: [TO BE RECORDED]

**Approval Ref for HR**: CEO-2026-07-21-Emergency-Idle