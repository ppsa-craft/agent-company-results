# emergency-idle-2026-08-01.md

## Framing question

Should we re-scope the current flagship (`vnstock-advisor`) after finding that M2 analysis-engine is only a placeholder with hardcoded values, or should we fix the broken implementation and delegation chain to continue with the current milestone structure?

## Options

**Option A — Re-scope flagship** (CEO RECOMMENDS)
- Treat current placeholder as aborted milestone
- Re-plan analysis-engine with realistic BA/DEV scope (actual MA/RSI/volume indicators, screening, ranking logic)
- Focus on completing functional analysis implementation first
- Remove BA-2 dependency bottleneck by breaking tasks into independent pieces

**Option B — Fix delegation chain and accelerate**
- Fix model instability causing provider resets
- Get BA-2 activated for BA tasks
- Implement real analysis-engine functionality (not placeholder)
- Continue with current milestone structure but with faster delivery

## Criteria
- Quality first (placeholder is a known defect that blocks the ship)
- Default work: the current flagship system's next milestone
- Must unblock builders (DEV/BA/TESTER/QA have real work)
- Consider token cost vs quality impact

## Parallel fan-out proposals

### CTO proposal (via TECHLEAD)

We need to tackle model instability and enable BA-2. TECHLEAD will:
- Audit delegation patterns across TECHLEAD, PM, and builder chains to eliminate 29 out-of-chain delegations
- Fix the model instability (provider resets) by switching to a more stable inference endpoint
- Enable BA-2 via new credentials and reassign BA-2 from "pending" to active, then have BA-2 complete vnstock-advisor-11-ba-suggestion-api and vnstock-advisor-12-ba-web-ui
- Provide a short-term analysis-engine fix: implement a basic MVP over M1's ingested data, using simple MA and volume filters; tests will validate that the MVP moves beyond hardcoded values
- Break the current M2 milestone into two independent tasks: (a) static placeholder removal and fixed MVP (DEV-2), (b) comprehensive analysis-engine expansion (DEV-3)
- Ensure DEV-2 and DEV-3 are staged for QA and TESTER in the same cycle

This path keeps the flagship's milestone structure intact but fixes delegation and model instability, delivering a functional analysis engine with lower risk of re-scoped effort.

### PM proposal

**Current Blockage:** BA-2 is pending; all BA capacity idle; backlog stuck with 2 BA tasks ready but no one to run them.

**PM's Parallel Fan-out Proposal for Emergency Unblocking**

**1. Delegation Chain Fix:**
- Task PM-001: Fix PM->BA/DEV/TESTER chain delegation to eliminate out-of-chain assignments — TECHLEAD will audit and eliminate 29 problematic delegations
- Task PM-002: Activate BA-2 immediately by providing credentials and reassigning from "pending" to active status

**2. BA-2 Activation & Real Work:**
- Task PM-003: Move BA-2 from pending to active with new credentials (1 day)
- Task PM-004: Assign BA-2 to complete vnstock-advisor-11-ba-suggestion-api and vnstock-advisor-12-ba-web-ui (independent, parallelizable tasks)
- Task PM-005: Deploy BA-1 to design simple M2 MVP scope (basic MA/RSI/volume indicators, screening logic, ranking algorithm over M1 data) — 2 days of focused design work

**3. Analysis-Engine Decomposition:**
- Task PM-006: Abort placeholder analysis-engine task (vnstock-advisor-5-dev-analysis-engine) and replace with:
  - DEV-002 (M2 MVP): Remove placeholder, implement basic MVP using M1 ingested data with simple MA and volume filters
  - DEV-003 (M2 Expansion): Comprehensive analysis-engine expansion with full indicator suite
- Task PM-007: Break vnstock-advisor-4-dev-data-ingest and vnstock-advisor-5-dev-data-ingest into independent subtasks for parallel DEV execution
- Task PM-008: Stage QA/TESTER surfaces for parallel execution

**4. Builder Unblocking — Immediate Work:**
- **BA Work (BA-1):** Complete M2 MVP design specs (2 days) — real, deliverable BA work
- **DEV Work (DEV-1):** Run independent data-ingest subtasks in parallel (once contracts are published) — 2 tasks, parallel execution
- **DEV Work (DEV-2):** Implement M2 MVP analysis engine (placeholder removal + basic functionality) — testable, vertical slice
- **DEV Work (DEV-3):** Implement comprehensive analysis-engine expansion (full feature set) — staged after MVP
- **BA Work (BA-2):** Complete suggestion-api and web-ui once M2 MVP functional — no longer bottleneck
- **QA Work (QA-1):** qa-data-ingest task — real QA verification work available
- **QA Work (QA-2):** qa-analysis-engine task — staged once MVP complete
- **TESTER Work (TESTER-1):** tester-data-ingest task — real exploratory testing work
- **TESTER Work (TESTER-2):** tester-analysis-engine task — staged once MVP complete

**5. Practical Decomposition:**
- Break M2 milestone into vertically sliced tasks that deliver working functionality end-to-end
- Tasks cut along architecture seams: independent data-ingest, MVP analysis-engine, expansion analysis-engine
- Each task is small enough for one focused session (S/M sized)
- QA/TESTER work staged for same cycle as DEV implementation
- BA-2 no longer a bottleneck — only 2 tasks, independent and parallelizable

**6. M2 Milestone Structure:**
- Keep existing M2 milestone structure intact (analysis-engine + data-ingest)
- Replace placeholder with real MVP implementation
- Add independent expansion task after MVP validation
- QA/TESTER surfaces maintained and staged appropriately

**7. Analysis-Engine Implementation Path:**
- Phase 1: MVP (DEV-2) — placeholder removal, basic MA/volume filters over M1 data
- Phase 2: Expansion (DEV-3) — full indicator suite (SMA/EMA/RSI/MACD/volume profiles)
- Phase 3: Optimization (DEV-4) — configurable weights, advanced screening, ranking algorithms
- Each phase has clear acceptance criteria and TESTER verification

**8. Backlog Pipeline Fix:**
- Ensure all ready tasks have proper assignment status in backlog.md
- Remove placeholder task, add M2 MVP/Expansion with correct status
- Maintain vertical slicing across all roles for parallel execution

**Implementation Plan:**
- **Week 1:** Fix delegation chain, activate BA-2, deploy BA-1 to M2 MVP design
- **Week 2:** Parallel data-ingest completion, start M2 MVP implementation
- **Week 3:** MVP testing/validation, begin M2 expansion
- **Week 4:** Full expansion implementation, QA/TESTER integration

**Test Plan Staging:**
- QA-1 (data-ingest): Ready immediately
- QA-2 (analysis-engine): Ready after MVP complete
- TESTER-1 (data-ingest): Ready immediately  
- TESTER-2 (analysis-engine): Ready after MVP complete

This proposal provides immediate real work for all builders, eliminates the BA-2 bottleneck, fixes delegation chains, maintains M2 structure, and delivers a realistic path to functional analysis-engine implementation.