# CTO Decomposition Brief: VN Stock Suggestion System — Milestone 1 (Data Ingestion Service)

**Cycle:** 66 (Emergency)  
**Product:** `vn-stock-suggestion`  
**Stack Decision:** `/data/tasks/stack-vn-stock-suggestion.md` (APPROVED by TECHLEAD)  
**Target:** PM cuts into MAXIMUM parallel ready tasks for cycle 66

---

## 1. Service Seams (5 Internal Modules = 5 Future Services)

| # | Seam Name | Module Path | Protocol Interface | Primary DEV Pair | TESTER Pair | Parallelism |
|---|-----------|-------------|-------------------|------------------|-------------|-------------|
| **S1** | **Source Adapter Layer** | `src/ingestion/sources/` | `SourceAdapter` | **DEV-1** | TESTER-1 | ✅ Independent |
| **S2** | **Normalization & Validation** | `src/ingestion/normalize.py` | `Normalizer` | **DEV-3** | TESTER-1 (shared) | ✅ Independent |
| **S3** | **Ingestion Orchestrator** | `src/ingestion/orchestrator.py` | `IngestionOrchestrator` | **DEV-2** | TESTER-2 | ✅ Independent |
| **S4** | **Storage Adapter (SQLite)** | `src/ingestion/storage/` | `StorageAdapter` | **DEV-2** (shared) | TESTER-2 (shared) | ⚠️ Shared with S3 |
| **S5** | **Observability** | `src/ingestion/observability.py` | `Observability` | **DEV-1** (shared) | TESTER-1 (shared) | ⚠️ Shared with S1 |

**Parallelization Plan:** **3 independent DEV+TESTER pairs** (DEV-1/TESTER-1, DEV-2/TESTER-2, DEV-3/TESTER-1). S4 and S5 are shared utilities — build AFTER S1/S2/S3 interfaces are stable.

---

## 2. API Contracts Between Services (Protocol Signatures)

```python
# All protocols in src/ingestion/protocols.py — binding contracts

# S1 → S2: Source Adapter produces RawPricePoint stream
class SourceAdapter(Protocol):
    name: str
    rate_limit: int
    async def fetch_symbols(self, exchange: str) -> list[str]: ...
    async def fetch_ohlcv(self, symbol: str, start: datetime, end: datetime, interval: str = "1D") -> AsyncIterator[RawPricePoint]: ...
    async def health_check(self) -> bool: ...

# S2: Normalizer consumes RawPricePoint → CanonicalPricePoint
class Normalizer(Protocol):
    async def normalize(self, raw: RawPricePoint) -> CanonicalPricePoint: ...
    async def validate(self, canonical: CanonicalPricePoint) -> CanonicalPricePoint: ...
    async def deduplicate(self, points: list[CanonicalPricePoint]) -> list[CanonicalPricePoint]: ...

# S3: Orchestrator coordinates S1 + S2 + S4
class IngestionOrchestrator(Protocol):
    async def run_ingestion_cycle(self, sources: list[SourceAdapter], symbols: list[str]) -> IngestionMetrics: ...
    async def run_historical_backfill(self, source: SourceAdapter, symbols: list[str], start: datetime, end: datetime) -> IngestionMetrics: ...
    async def run_incremental_update(self, source: SourceAdapter, symbols: list[str]) -> IngestionMetrics: ...

# S4: Storage persists CanonicalPricePoint + Checkpoints
class StorageAdapter(Protocol):
    async def init_schema(self) -> None: ...
    async def upsert_price_points(self, points: list[CanonicalPricePoint]) -> int: ...
    async def get_latest_checkpoint(self, source: str, symbol: str) -> IngestionCheckpoint | None: ...
    async def upsert_checkpoint(self, checkpoint: IngestionCheckpoint) -> None: ...
    async def query_price_points(self, symbol: str, start: datetime, end: datetime, limit: int = 10000) -> list[CanonicalPricePoint]: ...
    async def health_check(self) -> bool: ...

# S5: Observability (cross-cutting, injected everywhere)
class Observability(Protocol):
    def log_ingestion_start(self, source: str, symbols: int) -> None: ...
    def log_ingestion_complete(self, metrics: IngestionMetrics) -> None: ...
    def log_error(self, source: str, symbol: str, error: Exception) -> None: ...
    def record_metric(self, name: str, value: float, tags: dict[str, str]) -> None: ...
    def health_check(self) -> dict[str, bool]: ...
```

---

## 3. Data Models / Schemas (Pydantic = Source of Truth)

| Model | File | Key Fields | VN-Specific Rules |
|-------|------|------------|-------------------|
| `RawPricePoint` | `contracts.py` | symbol, time, open/high/low/close (Decimal), volume (int), source, fetched_at | `source` = `vnstock:KBS\|VCI\|MSN` |
| `CanonicalPricePoint` | `contracts.py` | + exchange (Enum: HOSE/HNX/UPCOM), is_valid, validation_errors[] | Prices `ge=0`, volume `ge=0`, **VND integer only** (TECHLEAD risk #4) |
| `IngestionCheckpoint` | `contracts.py` | source, symbol, last_fetched_time, last_successful_time, records_processed, last_error | Enables exact resumption; **transactional checkpoint** (TECHLEAD risk #6) |
| `IngestionMetrics` | `contracts.py` | source, symbols_*, records_*, duration_seconds, started_at, completed_at | Per-run observability |
| `Exchange` / `MarketIndex` | `contracts.py` | Enums covering all VN exchanges + indices (VNINDEX, VN30, HNX, UPCOM) | **Add `is_index` flag** (TECHLEAD risk #1) |

---

## 4. Parallelization Plan for PM — Maximum Ready Tasks

### Phase 1: Foundation (Week 1 — All 3 DEV pairs start simultaneously)

| Task ID | Seam | DEV | TESTER | Description | DoD Tier |
|---------|------|-----|--------|-------------|----------|
| `vnstock-s1-scaffold` | S1 | DEV-1 | — | Scaffold `src/ingestion/sources/`, `protocols.py`, `contracts.py`, `config.py`, `pyproject.toml` | Tier 1 |
| `vnstock-s1-vnstock-adapter` | S1 | DEV-1 | TESTER-1 | Implement `VnstockKBSAdapter`, `VnstockVCIAdapter`, `VnstockMSNAdapter` implementing `SourceAdapter`; rate limiting, column mapping per source | Tier 2 |
| `vnstock-s1-source-registry` | S1 | DEV-1 | TESTER-1 | `SourceRegistry` — resolves source name → adapter instance; health checks | Tier 2 |
| `vnstock-s2-normalizer` | S2 | DEV-3 | TESTER-1 | Implement `Normalizer`: raw→canonical mapping, pydantic validation, VN market calendar rejection, VND integer enforcement, deduplication | Tier 2 |
| `vnstock-s3-orchestrator-core` | S3 | DEV-2 | TESTER-2 | Implement `IngestionOrchestrator`: cycle scheduling (APScheduler), token-bucket rate limiting per source, checkpoint coordination | Tier 2 |
| `vnstock-s3-backfill-incremental` | S3 | DEV-2 | TESTER-2 | `run_historical_backfill` + `run_incremental_update` with checkpoint resume | Tier 2 |
| `vnstock-s4-storage-sqlite` | S4 | DEV-2 | TESTER-2 | `SQLiteStorageAdapter`: schema (price_points, checkpoints), WAL mode, batch upsert with `ON CONFLICT`, migration runner | Tier 2 |
| `vnstock-s5-observability` | S5 | DEV-1 | TESTER-1 | `StructlogObservability`: JSON logs, correlation IDs, Prometheus metrics via `record_metric`, health endpoint | Tier 1 |

**Dependency Graph (Phase 1):**
```
vnstock-s1-scaffold ──┬──→ vnstock-s1-vnstock-adapter ──→ vnstock-s1-source-registry
                      │
                      ├──→ vnstock-s5-observability (injected into all)
                      │
vnstock-s2-normalizer ◄── (independent, uses contracts.py only)
                      │
vnstock-s3-orchestrator-core ◄── (uses S1 protocol, S2 protocol, S4 protocol, S5)
                      │
vnstock-s3-backfill-incremental ◄── (depends on s3-orchestrator-core)
                      │
vnstock-s4-storage-sqlite ◄── (independent, uses contracts.py only)
```

**Critical Path:** `s1-scaffold` → `s1-vnstock-adapter` + `s2-normalizer` + `s4-storage` → `s3-orchestrator-core` → `s3-backfill-incremental`  
**Parallelism:** 3 DEV pairs work on S1, S2, S3/S4 simultaneously after scaffold.

### Phase 2: Integration & E2E (Week 2)

| Task ID | DEV | TESTER | Description | DoD Tier |
|---------|-----|--------|-------------|----------|
| `vnstock-integration-contract-tests` | DEV-1/2/3 | TESTER-1/2 | Contract test suites for ALL 5 protocols (test doubles + real impl) | Tier 2 |
| `vnstock-integration-e2e-cycle` | DEV-2 | TESTER-2 | Full ingestion cycle: symbols → fetch → normalize → store → checkpoint → metrics | Tier 3 |
| `vnstock-integration-backfill` | DEV-2 | TESTER-1 | Historical backfill VN30 (30 symbols, 2 years daily) — performance + correctness | Tier 3 |
| `vnstock-worker-entrypoint` | DEV-1 | — | `src/ingestion/worker.py` — CLI entry: `run-cycle`, `backfill`, `health` | Tier 1 |
| `vnstock-readme-runbook` | DEV-1 | TESTER-1 | README.md: how to run worker, config via `.env`, test commands, troubleshooting | Tier 1 |

---

## 5. TECHLEAD Review Notes on Technical Coherence

**VERDICT: APPROVED** (see full review in session)

### Key Coherence Points Verified:
1. ✅ **5 Protocol seams = 5 future services** — zero-cost `typing.Protocol` interfaces
2. ✅ **M2+ extraction path** — each Protocol maps to a clean service boundary
3. ✅ **Data contracts validate VN stock OHLCV** — Decimal prices, VND integer enforcement, VN exchange/index enums
4. ✅ **TESTER in-pod compatible** — single Python process, SQLite file, no external deps
5. ✅ **Python 3.11 + vnstock 4.0.4 compatible** — async-native, httpx internal
6. ✅ **Conventions enforceable** — mypy strict, ruff async rules, contract tests for every Protocol

### 8 Additional Risks for PM to Acknowledge in Task Breakdown:

| # | Risk | Affected Tasks | Mitigation in Tasks |
|---|------|----------------|---------------------|
| 1 | VN market calendar (Tet, weekends, holidays) | `vnstock-s2-normalizer` | Add holiday calendar; reject non-trading day data in `validate()` |
| 2 | Source-specific schema drift (KBS/VCI/MSN column differences) | `vnstock-s1-vnstock-adapter` | Per-adapter column mapping; contract test per adapter |
| 3 | SQLite WAL + concurrent TESTER reads | `vnstock-s4-storage-sqlite` | Enable WAL mode; TESTER reads read-only |
| 4 | VND precision (no decimals) | `vnstock-s2-normalizer` | Custom validator: `decimal_places=0` on price fields |
| 5 | Symbol format variance (`VIC` vs `VIC.HM` vs `HOSE:VIC`) | `vnstock-s1-source-registry`, `vnstock-s2-normalizer` | Canonical symbol mapping in registry; normalizer maps variants |
| 6 | Checkpoint race on crash mid-batch | `vnstock-s3-orchestrator-core`, `vnstock-s4-storage-sqlite` | SQLite transaction per batch; checkpoint only after commit; add `batch_id` |
| 7 | vnstock async vs sync API confusion | `vnstock-s1-vnstock-adapter` | Enforce `AsyncIterator`; wrap sync in `asyncio.to_thread` |
| 8 | Data retention / partition strategy | `vnstock-s4-storage-sqlite` | Document policy; `query_price_points` supports partition pruning |

---

## 6. PM Task Cutting Guidance

### Priority Order (Maximize Parallelism):
1. **Immediate (Cycle 66 start):** `vnstock-s1-scaffold` (unblocks all) + `vnstock-s5-observability` (injected everywhere)
2. **Parallel Wave 1:** `vnstock-s1-vnstock-adapter`, `vnstock-s2-normalizer`, `vnstock-s4-storage-sqlite` (3 DEV pairs, independent)
3. **Parallel Wave 2:** `vnstock-s1-source-registry`, `vnstock-s3-orchestrator-core` (after Wave 1 protocols stable)
4. **Sequential:** `vnstock-s3-backfill-incremental` (depends on orchestrator)
5. **Integration Wave:** Contract tests → E2E cycle → Backfill → Worker entrypoint → README

### DEV/TESTER Allocation:
| DEV Instance | Primary Seam | TESTER Pair | Cycle 66 Tasks |
|--------------|--------------|-------------|----------------|
| **DEV-1** | S1 (Sources) + S5 (Obs) | TESTER-1 | scaffold, vnstock-adapters, source-registry, observability |
| **DEV-2** | S3 (Orchestrator) + S4 (Storage) | TESTER-2 | storage-sqlite, orchestrator-core, backfill-incremental |
| **DEV-3** | S2 (Normalizer) | TESTER-1 (shared) | normalizer |

### TESTER Work Split:
| TESTER | Primary Contract Tests | E2E Tests |
|--------|----------------------|-----------|
| **TESTER-1** | S1 (SourceAdapter), S2 (Normalizer), S5 (Observability) | Backfill correctness |
| **TESTER-2** | S3 (IngestionOrchestrator), S4 (StorageAdapter) | Full ingestion cycle, performance |

---

## 7. CTO Sign-off for PM

**This decomposition brief authorizes PM to cut the above tasks into `tasks/backlog.md` with `ready` status for Cycle 66.**

- All 5 service seams defined with Protocol contracts
- 3 independent DEV+TESTER pairs identified
- 8 TECHLEAD-identified risks mapped to specific tasks
- Stack decision approved and binding
- No external dependencies for M1 (TESTER in-pod verified)

**CTO:** ___________________  
**Date:** 2026-07-19 (Cycle 66 Emergency)

---

*PM: Cut maximum ready tasks. Every live agent must have work by end of Cycle 66. Report task count to CEO.*