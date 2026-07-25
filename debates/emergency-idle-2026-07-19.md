# Emergency Leadership Debate - Company Idle Resolution (Updated)

## Current State

- **ORCHESTRATOR ASSESSMENT**: Company idle (Company.md §3.5.4)
- **tasks/backlog.md**: NO ready and NO in-progress tasks
- **Trigger**: Critical: no live agent has assigned work

## Option A: PM Pillar for Techlead Gate + ONE Flagship Extra

**What's proposed:**
- **Pillar**: "Query Builder + Integration Foundation" (vn-stock-techlead-1-pillar-v01)
  - Clears TECHLEAD gate and READIES Stream C (6 tasks)
  - Leaves behind persistent architecture seam for future parallel work
- **Flagship Extra**: "vn-stock-analytics-sync" — lightweight horizontal analytics sync for flagship
  - Single short-duty dev task: syncs core analytics across products
  - Enables analytics for flagship in parallel with other teams
- **Outcome**: ALL 6 Stream C tasks become READY, flagship pipeline complete, unblocks entire S3/S6 pipeline

**Criteria:**
- ✅ Real product work only (no filler tasks)
- ✅ Massive parallel task generation (max ready tasks)
- ✅ End-of-day: all live agents have work
- ✅ Start from existing backlog (mega-cluster of techlead + analytics)
- ✅ Minimal TOSS: 2 tasks, one existing pillar + lightweight extra

## Option B: CTO: ONE Additional Team + ONE Seam Refactor

**What's proposed:**
- **Team boost**: Add ONE bright‑team NEW team to ready tasks
  - Seam‑aware DEV‑X (new hires) assigned to 20‑ready VIABLE backlog tasks
  - Focus only on TECHLEAD‑validated seams and READY‑status tasks
- **Seam refactor**: "future‑seams" architectural seam documents for modular contracts
  - TechLead team spends ONE hour documenting all existing major seams
  - Enables more parallelism in following cycles, not today
- **Outcome**: New capacity retained, inter‑team handball continuity, future grid stronger

**Criteria:**
- ✅ Real product work (seam‑focused docs)
- ⚠️ Slower (2 hours to ramp new team, + seam doc only)
- ✅ Quality (constrained to TECHLEAD seams)

## Option C: TECHLEAD: Seams for Future

**What's proposed:**
- **1 hour urgent seam enrichment**: TECHLEAD runs all existing architecture seams and expands with:
  - Visualize async patterns, circuit breakers, workflow syncs
  - Cross‑language contract mismatches highlighted
  - Future‑parallelism enable paths mapped for each seam
- **Goal**: Future SEAM‑driven parallelism, preventative blockage against
  - Cross‑module coupling creep
  - Interface fragility
  - Design drift between DEV streams

**Criteria:**
- ⚠️ More like process‑leaning; actual product work small
- ✅ Quality (seams = architecture backbone)
- ✅ Future speed (keeps parallel pipelines clean)

## Decision Matrix (Quality > Speed > Cost)

**Option A wins on:**
- **Quality**: Persistently unblocks flagship S3/S6, leaves durable architecture seam, enabling pipeline for flagship early
- **Speed**: FAST, TODAY: 2 PN tasks, clears techlead gate instantly, Stream C READY
- **Cost**: Minimal (0 hires, existing tech lead effort)

**Option B fails on:**
- **Quality**: New team needs 24‑48h ramp, seam refactor deferred tomorrow
- **Speed**: Slower ramp (→ 2 days)
- **Cost**: Higher (→ HR onboarding)

**Option C fails on:**
- **Quality**: Process work, not shipping real product today
- **Speed**: Small, SEAM‑focused; pipeline output tiny
- **Cost**: Not adding capacity, just structure

## Vote

- CTO (with TECHLEAD): Option A ✅
- PM (existing functional subagents): Option A ✅
- TECHLEAD: Option A ✅

### Executive Decision

**PICKED: Option A - PM Pillar for Techlead Gate + ONE Flagship Read‑only Extra**

**Execution:**
- **TODAY**: PM owns pillar and flagship extra from backlog.
- **MUST**: Finish TECHLEAD gate review by EOD, ready all Stream C tasks.
- **STILL**: CTO & TECHLEAD optional seam prep for future.

**Process note:**
- PM writes 1 DONE artifact + analytics extra.
- CTO and TECHLEAD OPTIONAL: quick seam scan of existing, add ONE hour to future.