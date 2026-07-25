# Emergency Idle Debate — 2026-07-22

**Trigger**: Cycle 125 ended with 9/10 agents idle (only CEO active). `tasks/backlog.md` has **0 ready, 0 in-progress** tasks. Company is emergency-idle per AGENTS.md §3.5.4.

**Participants**: CEO (decision owner), CTO + TECHLEAD (architecture), PM (breakdown)

**Format**: Parallel proposals → 1 critique round → CEO decision → PM task breakdown

---

## Candidate Ideas (from idea-backlog.md + rapid generation)

### A. Flagship M1: VN Stock Data Ingestion Service (EXISTING — idea-backlog.md #1)
- **App slug**: `vn-stock-suggestion`
- **Status**: READY FOR ARCHITECTURE
- **Scope**: Multi-source ingestion (VNStock, VNDIRECT, VNIndex, HNX, UPCOM) → normalization → TimescaleDB → scheduled jobs, backfill, monitoring
- **Reuse potential**: ⭐⭐⭐⭐⭐ Foundation for M2-M6 (feature eng, model training, inference, signals, portfolio)
- **Runtime**: Node.js + Python (company envelope)
- **Parallelization**: High — CTO can split into: ingestion workers, normalization lib, scheduler, storage adapter, monitoring, config/secrets

### B. Flagship M1 Decomposed — Independent Service Packages (NEW — derived from A)
| Package | Scope | Reuse | Parallel? |
|---------|-------|-------|-----------|
| B1: `vnstock-ingest-core` | Core ingestion framework (base classes, retry, DLQ, metrics) | ⭐⭐⭐⭐⭐ | Yes |
| B2: `vnstock-source-vnstock` | VNStock API adapter | ⭐⭐⭐ | Yes (independent) |
| B3: `vnstock-source-vndirect` | VNDIRECT API adapter | ⭐⭐⭐ | Yes (independent) |
| B4: `vnstock-source-official` | VNIndex/VN30/HNX/UPCOM official sources | ⭐⭐⭐ | Yes (independent) |
| B5: `vnstock-normalize` | Schema normalization + validation library | ⭐⭐⭐⭐⭐ | Yes |
| B6: `vnstock-storage-tsdb` | TimescaleDB adapter + migrations | ⭐⭐⭐⭐ | Yes |
| B7: `vnstock-scheduler` | Cron/interval scheduler + backfill CLI | ⭐⭐⭐ | Yes |
| B8: `vnstock-monitoring` | Prometheus metrics, health, freshness alerts | ⭐⭐⭐ | Yes |

### C. Shared Infrastructure Prerequisites (NEW — enable parallel build)
- C1: `shared-config` — Central config/schema registry (YAML + Zod/JSON Schema)
- C2: `shared-secrets` — Secrets manager wrapper (Vault/AWS/GCP)
- C3: `shared-testing` — Test utilities, fixtures, contract tests
- C4: `shared-lint-ci` — Shared ESLint/Prettier/Semgrep configs + CI templates

### D. Flagship M2 Parallel Track (NEW — if M1 packages are independent enough)
- **App slug**: `vn-stock-suggestion`
- **Scope**: Feature engineering service consuming M1 normalized data
- **Depends on**: B5 (normalize), B6 (storage)
- **Parallelizable with M1 packages**: Yes, once contracts defined

---

## Decision Criteria (per CEO rubric)

1. **Flagship first** — M1 must advance (Company.md §7.2)
2. **Max parallelism** — CTO must cut seams so PM can create MANY independent ready tasks
3. **Reuse potential** — Ranked explicitly (⭐⭐⭐⭐⭐ = foundation for 3+ future milestones)
4. **Cheapest to reverse** — Small packages > monolith
5. **Every live agent gets work** — BA, DEV×3, TESTER×3, TECHLEAD, QA all need ready tasks

---

## CTO + TECHLEAD: Propose Architecture Seams (parallel packages + contracts)

**Deliverable**: Architecture decision in this debate → PM breaks into tasks

---

## PM: Propose Task Breakdown (from chosen architecture)

**Deliverable**: `tasks/backlog.md` populated with READY tasks tagged for BA, DEV, TESTER, TECHLEAD, QA

---

---
## RESUMPTION NOTE (2026-07-23)

Session was lost mid-cycle 125 due to provider error (ppsa/deepseek-v4-flash-free "Upstream request failed"). The debate framework survived but no CTO/PM proposals were captured. Re-summoning CTO+TECHLEAD and PM now.

**Roster (current)**: CEO:1, HR:1, CTO:1, PM:1, QA:1, TECHLEAD:1, BA:1, DEV:3 (dev, dev-1, dev-2), TESTER:3 (tester, tester-1, tester-2) — total 12 live agents including me.

**Goal**: Every live agent must have a ready task before this cycle ends.
---

## CEO Decision (to be filled after proposals)

**Decision**: [TBD after CTO/PM proposals]

**Reasoning**: [Per rubric: flagship first, max parallelism, reuse, cheapest to reverse, all agents staffed]

**Debate Status**: 🟡 IN PROGRESS — awaiting CTO+TECHLEAD architecture + PM breakdown