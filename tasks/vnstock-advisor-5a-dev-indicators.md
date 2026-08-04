# Task: vnstock-advisor-5a-dev-indicators

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature — analysis-engine: indicators module)
**Status:** ready (assign: DEV instance on `task/vnstock-advisor-5a-dev-indicators-dev`)

---

## Goal

Implement the real `indicators.py` computation module for the `analysis-engine`
service — SMA, EMA, RSI, MACD, Volume Profile (VWAP/Volume SMA/Volume Ratio) plus
ROC10, ATR14, OBV — and wire the `POST /indicators/compute` endpoint. This
replaces the current placeholder `/analyze` response with tested, exact
computation per `docs/specs/indicators.md` v1.0.

This is the **5a / indicators slice** of the umbrella task
`vnstock-advisor-5-dev-analysis-engine`. Screening (5b) and ranking (5c) consume
`indicators.py` output, so this must land and pass review first.

## Acceptance Criteria (traceable to UC-AE-1; formulas per indicators.md v1.0)

- [ ] `services/analysis-engine/src/indicators.py` exports per-indicator
      functions: `sma`, `ema` (Wilder's), `rsi` (Wilder's), `macd`,
      `volume_profile`, plus `roc`, `atr`, `obv` — formulas and edge cases
      matched to the `docs/specs/indicators.md` reference implementations.
- [ ] `compute_all_indicators(ohlcv) -> IndicatorsResult` aggregates the families
      into one structured, deterministic result per fixture.
- [ ] Edge cases implemented exactly as spec: insufficient data → `null` with
      warning `insufficient_data`, gaps propagate `null`, flat market → RSI=50 &
      MACD/signal/histogram=0, zero volume → VWAP falls back to close, Volume
      SMA=0 → Volume Ratio `null`, stock splits compute on raw prices (no
      `adj_close` in schema).
- [ ] `POST /indicators/compute` accepts symbols + date range, validates input
      (Pydantic), calls `compute_all_indicators`, returns a per-symbol structured
      result; rejects invalid params with Problem Details (RFC 7807), no stack
      traces in responses.
- [ ] Unit tests pass against fixture sets in `tests/fixtures/` (`normal-trading`,
      `insufficient-data`, `price-gaps`, `stock-splits`, `low-volume`,
      `flat-market`).
- [ ] Suite runs via ONE command (`pytest`); README documents exact run steps.
- [ ] Security gate: secret-scan & SAST clean; no secrets committed; all external
      input treated as hostile (validated).

## Implementation Plan (for DEV)

**Architecture seam — file boundary:** this task owns ONLY
`services/analysis-engine/src/indicators.py` (and its internal helpers), the
`indicators` endpoint/router in the service `main.py`, and
`tests/test_indicators*.py` + `tests/fixtures/`. It MUST NOT touch
`screening.py` (5b) or `ranking.py` (5c) — those are sibling, disjoint slices
built on top of this module's output by other DEV instances. Commit only files
under `apps/vnstock-advisor/`, nothing else.

**Worktree state (fixed this cycle):** on branch
`task/vnstock-advisor-5a-dev-indicators-dev` (worktree registered at
`/data/worktrees/dev`) there is currently NO `apps/vnstock-advisor` tree (the
scaffold was never merged to main). First, stage the existing scaffold from the
workspace on-disk copy (`/data/workspace/apps/vnstock-advisor/`) into your
worktree under `apps/vnstock-advisor/`, excluding `.venv`, `__pycache__`,
`.pytest_cache`, `*.egg-info`, `.env`. Commit that scaffold as your base commit
(coherent unit), then build 5a on top.

Ordered subtasks (each a committed unit):
1. Stage scaffold into worktree; commit base scaffold.
2. `src/indicators.py`: implement `sma`, `ema`, `rsi`, `macd` exactly per the
   reference impl. Test-first.
3. Implement volume profile (`vwap`, `volume_sma`, `volume_ratio`) + `roc`,
   `atr`, `obv` per indicators.md §5/§6; test-first.
4. Add `compute_all_indicators()` aggregator + edge-case handling; commit.
5. Add `POST /indicators/compute` endpoint + Pydantic request/response models.
6. Create `tests/fixtures/` (8 JSON sets per fixtures.md) + unit tests (happy
   path + edge cases, both good and worst flows). One-command suite.
7. Update the service `README.md` with real how-to-run + test steps.
8. Security: secret-scan & SAST pass; commit.

## Test Plan (for DEV and TESTER)

1. **Happy-path accuracy:** load `normal-trading.json`, call
   `compute_all_indicators` for a known symbol (e.g. VNM), compare last-bar
   values with expected. => within tolerance (prices 4dp, RSI/percent 2dp, vol 0dp).
2. **Insufficient data:** request for symbols with < required bars (ABC=10,
   XYZ=15, DEF=50, GHI=199). => `null` for uncomputable indicators with
   `insufficient_data` notice; no 500.
3. **Gap propagation:** run on `price-gaps.json`; gaps propagate `null` per spec.
4. **Flat market:** KLM flat series => RSI=50.0, MACD/signal/hist=0.
5. **Low/zero volume:** BCD zero-volume days => VWAP falls back to close; Volume
   Ratio `null` when Volume SMA=0.
6. **HTTP endpoint:** `POST /indicators/compute` happy path + invalid payload
   (bad symbol/date range) => clean Problem Details error, no stack trace.
7. **Crash-safety:** empty OHLCV list, single bar, malformed JSON => clean error.

## Dependencies

- Sibling slices 5b/5c consume this module's output; order: this must be APPROVED
  before 5b/5c building.
- Base: `service/analysis-engine` scaffold + `shared/python/src/vnstock_shared/models.py`.
- Spec: `docs/specs/indicators.md` v1.0, `docs/testing/fixtures.md`.
- Feeds: `vnstock-advisor-{tester-indicators, qa-indicators}` onwards.