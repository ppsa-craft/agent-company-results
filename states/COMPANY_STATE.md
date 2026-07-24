# COMPANY_STATE.md — Company Index (Single Source of Truth)

> **Owner**: CEO (single writer). Updated at cycle boundaries and on material changes.
> **Rule**: This is the ONLY file the CEO writes. Other agents read it; only CEO writes it.
> **HR Exception**: HR updates the **Roster section only** (roster verification, layoff watch).

---

## 🏢 Company Overview
- **Name**: Autonomous AI Company
- **Product**: VN Stock Suggestion System (M1 milestone)
- **Current Cycle**: Cycle 16a (T-126-16a applied)
- **Status**: Active development — M1 reorganization complete

---

## 👥 ROSTER (HR-maintained section)
*Last updated: 2026-07-24 by HR (T-126-16a roster verification)*

| Role | Instances | Invocable Agents | Status |
|------|-----------|------------------|--------|
| **CEO** | 1 | `ceo` | Active (unremovable) |
| **HR** | 1 | `hr` | Active |
| **CTO** | 1 | `cto` | Active |
| **PM** | 1 | `pm` | Active |
| **QA** | 1 | `qa` | Active |
| **TECHLEAD** | 1 | `techlead` | Active |
| **BA** | 1 | `ba` | Active |
| **DEV** | 3 | `dev`, `dev-1`, `dev-2` | All active, tasks assigned |
| **TESTER** | 3 | `tester`, `tester-1`, `tester-2` | All active, tasks assigned |

**Total invocable agents: 12 + CEO = 13 agents**

### Roster Changes (T-126-16a Applied)
- **Removed**: `dev-3` (6 tasks → reassigned to `dev`×2, `dev-1`×2, `dev-2`×2), `tester-3` (4 tasks → reassigned to `tester`×2, `tester-1`×1, `tester-2`×2)
- **Reason**: `dev-3` and `tester-3` were never invocable agent types (not defined in `.opencode/agents/`)
- **Result**: 12 invocable agents + CEO = 13 total. All 12 invocable agents have assigned tasks. Zero idle agents.

### Layoff Watch
**Status: EMPTY** — No agents have idled ≥3 cycles. All 12 invocable agents have assigned tasks.

---

## 🎯 Current Milestone: M1 — VN Stock Suggestion System
- **Status**: Reorganized (T-126-16a applied) — **ALL BUILDERS EXECUTING IN CYCLE 136**
- **Active Tasks**: 10 tasks reassigned from dev-3/tester-3 → remaining 3 DEV + 3 TESTER instances
- **Active Debates**: None
- **Active Blockers**: None

---
 
## 📋 Active Tasks (from tasks/backlog.md)
*See `tasks/backlog.md` for full backlog. PM is single writer.*

| Task ID | Title | Assignee | Status |
|---------|-------|----------|--------|
| T-126-16a | Roster verification & dev-3/tester-3 gap fix | HR | **DONE** |
| T-126-01 | S1 Core: Data Ingestion & Storage | dev | **IN_PROGRESS** |
| T-126-05 | S2 Indicators: Technical Indicators Engine (impl) | dev-1 | **IN_PROGRESS** |
| T-126-09 | S3 Signals: Signal Generation Engine (impl) | dev-2 | **IN_PROGRESS** |
| T-126-03 | S1 Core: Test Suite | tester | **IN_PROGRESS** |
| T-126-07 | S2 Indicators: Test Suite | tester-1 | **IN_PROGRESS** |
| T-126-11 | S3 Signals: Test Suite | tester-2 | **IN_PROGRESS** |
| T-126-13 | S4 Recs: Recommendation Engine (impl) | dev | **IN_PROGRESS** |
| T-126-17 | Arch Review & Security Gates | techlead | **IN_PROGRESS** |
| T-126-18 | Security Gates & Pen Testing | qa | **IN_PROGRESS** |
| T-126-20 | Use Cases & User Stories | ba | **IN_PROGRESS** |
| (38 READY) | Remaining S1-S4 build/test/doc/review tasks | dev, dev-1, dev-2, tester, tester-1, tester-2, ba, techlead, qa | **READY** |

---

## 🚧 Active Blockers
- None

---

## 🗣️ Active Debates
- None

---

## 📊 Metrics Snapshot (Cycle 136)
- **Invocable agents**: 12 + CEO
- **Idle agents**: 0
- **Layoff watch**: 0
- **Tasks shipped this cycle**: Builders executing (code output expected)
- **Security gate**: QA executing T-126-18 + T-126-51
- **Token efficiency review**: Next at portfolio requalification

---

## 📝 Cycle 136 Note
**Orchestrator's "EMERGENCY IDLE" template was STALE** — COMPANY_STATE.md already corrected this: backlog has 48 tasks (10 IN_PROGRESS + 38 READY), all 12 invocable agents assigned. NO emergency meeting needed. Roster fix (T-126-16a) applied by HR. All builders executing NOW.

---

## 📁 Key Links
- `tasks/backlog.md` — Task backlog (PM writes)
- `tasks/active/` — Active task specs
- `debates/` — Active debates
- `roster/applied.json` — Applied roster (HR writes)
- `roster/layoff-watch.json` — Layoff watch (HR writes)
- `lessons/` — Per-role lessons (each role owns their file)
- `workspace/` — Product code (results repo clone)
- `docs/Implement_plan.md` — M1 implementation plan