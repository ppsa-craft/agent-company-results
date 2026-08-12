"""FastAPI application for the vnstock-advisor analysis-engine.

Implements the frozen contract (``docs/specs/analysis-engine-api.md`` v1.0):

  * ``POST /indicators/compute`` — real indicator computation over an OHLCV series
  * ``POST /analyze``           — higher-level analysis (signals/trend/strength)
  * ``POST /rank``              — composite ranking with ``ranked[]``/``excluded[]`` split
  * ``GET /health``, ``GET /``  — liveness + banner

C2 fix: every endpoint computes indicators from real input data — no placeholder
literals. C3 fix: request/response shapes match the frozen contract
(``algorithm_version``, ranked/excluded split, ``weights_used``). C6 fix:
explicit input guards live in ``schemas.py`` (ticker pattern, ``as_of_date``,
``algorithm_version``, ``series`` map, no silent drops).
"""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException

from vnstock_shared.config import get_settings

import structlog

from .indicators import IndicatorsResult, compute_all_indicators
from .ranking import RankingError, rank_symbols
from .schemas import (
    SUPPORTED_ALGORITHM_VERSIONS,
    AnalyzeRequest,
    AnalyzeResponse,
    IndicatorComputeRequest,
    IndicatorComputeResponse,
    RankRequest,
    RankResponse,
    now_iso,
    problem_detail,
)

settings = get_settings()
logger = structlog.get_logger()

app = FastAPI(
    title="vnstock Analysis Engine",
    description="Technical analysis and signal generation service",
    version="0.1.0",
)

_DEFAULT_WEIGHTS: Dict[str, float] = {
    "momentum": 0.4,
    "trend": 0.3,
    "volume": 0.2,
    "volatility": 0.1,
}

_MIN_ANALYZE_BARS = 50  # SMA50 requires 50 bars (contract §2 error example)


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "analysis-engine",
        "version": "0.1.0",
        "timestamp": now_iso(),
        "checks": [
            {"name": "indicators_module", "status": "ok"},
        ],
    }


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "vnstock Analysis Engine Service"}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _require_supported_version(algorithm_version: str, instance: str) -> None:
    if algorithm_version not in SUPPORTED_ALGORITHM_VERSIONS:
        raise HTTPException(
            status_code=400,
            detail=problem_detail(
                400,
                "UNSUPPORTED_VERSION",
                "Algorithm version not supported",
                f"{algorithm_version} not supported; supported: "
                f"{list(SUPPORTED_ALGORITHM_VERSIONS)}",
                instance,
            ),
        )


def _last_computable_index(result: IndicatorsResult) -> int:
    """Rightmost index with at least one non-None key indicator, or -1."""
    for t in range(len(result.rsi14) - 1, -1, -1):
        if (
            result.rsi14[t] is not None
            or result.sma20[t] is not None
            or result.macd[t] is not None
        ):
            return t
    return -1


def _snapshot_at(result: IndicatorsResult, idx: int) -> Dict[str, Any]:
    """Compact indicator snapshot at ``idx`` (contract §1 ``last`` shape)."""
    if idx < 0:
        return {}
    return {
        "sma20": result.sma20[idx],
        "sma50": result.sma50[idx],
        "sma200": result.sma200[idx],
        "ema12": result.ema12[idx],
        "ema26": result.ema26[idx],
        "ema9": result.ema9[idx],
        "rsi14": result.rsi14[idx],
        "macd": result.macd[idx],
        "vwap": result.vwap[idx],
        "volume_sma": result.volume_sma[idx],
        "volume_ratio": result.volume_ratio[idx],
        "roc10": result.roc10[idx],
        "atr14": result.atr14[idx],
        "obv": result.obv[idx],
    }


def _last_non_null(values: List[Any]) -> Any:
    for v in reversed(values):
        if v is not None:
            return v
    return None


def _to_rank_inputs(symbol: str, result: IndicatorsResult) -> Dict[str, Any]:
    """Derive the ranking-consumer indicator dict from REAL computed values."""
    close = _last_non_null(result.closes)
    sma20 = _last_non_null(result.sma20)
    sma50 = _last_non_null(result.sma50)
    sma200 = _last_non_null(result.sma200)
    rsi = _last_non_null(result.rsi14)
    vol_ratio = _last_non_null(result.volume_ratio)
    roc10 = _last_non_null(result.roc10)
    atr_val = _last_non_null(result.atr14)

    macd_last = _last_non_null(result.macd)
    hist = macd_last["histogram"] if macd_last else None

    # OBV trend: direction of the last change (normalised to [-1, 1] band
    # expected by ranking.calculate_volume).
    obv_series = result.obv
    obv_last = _last_non_null(obv_series)
    obv_prev = None
    for v in reversed(obv_series[:-1]):
        if v is not None:
            obv_prev = v
            break
    obv_trend = 0.0
    if obv_last is not None and obv_prev is not None:
        obv_trend = 1.0 if obv_last > obv_prev else (-1.0 if obv_last < obv_prev else 0.0)

    # Trend conditions (7 per screening-ranking spec).
    trend_conditions = [
        bool(close is not None and sma20 is not None and close > sma20),
        bool(close is not None and sma50 is not None and close > sma50),
        bool(close is not None and sma200 is not None and close > sma200),
        bool(hist is not None and hist > 0),
        bool(rsi is not None and rsi > 50),
        bool(vol_ratio is not None and vol_ratio > 1.0),
        bool(obv_trend > 0),
    ]

    return {
        "roc10": roc10,
        "rsi": rsi,
        "trend_conditions": trend_conditions,
        "total_trend_conditions": 7,
        "volume_ratio": vol_ratio,
        "obv_trend": obv_trend,
        "atr_percentile": 50.0,  # neutral default — true percentile is not part of v1.0
        "atr": atr_val,
        "valid_bars": len(result.closes),
    }


_INDICATOR_MIN_BARS = [
    ("SMA20", 20),
    ("SMA50", 50),
    ("SMA200", 200),
    ("RSI14", 15),
    ("MACD", 34),
    ("ATR14", 15),
    ("ROC10", 11),
    ("Volume_SMA20", 20),
]


def _missing_indicators(result: IndicatorsResult) -> List[str]:
    n = len(result.closes)
    return [name for name, need in _INDICATOR_MIN_BARS if n < need]


# --------------------------------------------------------------------------- #
# POST /indicators/compute (contract §1)
# --------------------------------------------------------------------------- #
@app.post("/indicators/compute", response_model=IndicatorComputeResponse)
async def compute_indicators(req: IndicatorComputeRequest) -> IndicatorComputeResponse:
    _require_supported_version(req.algorithm_version, "/indicators/compute")
    try:
        result = compute_all_indicators(req.ohlcv, volume_sma_period=req.volume_sma_period)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=problem_detail(
                422, "COMPUTATION_ERROR", "Indicator computation failed",
                str(exc), "/indicators/compute",
            ),
        ) from exc

    indicators: Dict[str, Any] = {
        "sma20": result.sma20,
        "sma50": result.sma50,
        "sma200": result.sma200,
        "ema12": result.ema12,
        "ema26": result.ema26,
        "ema9": result.ema9,
        "rsi14": result.rsi14,
        "macd": result.macd,
        "vwap": result.vwap,
        "volume_sma": result.volume_sma,
        "volume_ratio": result.volume_ratio,
        "roc10": result.roc10,
        "atr14": result.atr14,
        "obv": result.obv,
    }
    return IndicatorComputeResponse(
        symbol=req.symbol,
        algorithm_version=req.algorithm_version,
        computed_at=now_iso(),
        bars_processed=len(req.ohlcv),
        indicators=indicators,
        warnings=result.warnings,
        last=_snapshot_at(result, _last_computable_index(result)),
    )


# --------------------------------------------------------------------------- #
# POST /analyze (data-ingest consumer contract, §2)
# --------------------------------------------------------------------------- #
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    # C2 fix: an explicit ascending bars series is required so the endpoint can
    # produce ACTUAL indicator values. A lone bar (MarketDataCreate shape with
    # no history) cannot — surface INSUFFICIENT_HISTORY instead of all-None.
    if req.bars is None or len(req.bars) == 0:
        raise HTTPException(
            status_code=422,
            detail=problem_detail(
                422, "INSUFFICIENT_HISTORY", "Not enough historical data for analysis",
                "Provide a `bars` series (ascending OHLCV) so indicators can be computed",
                "/analyze",
            ),
        )
    if len(req.bars) < _MIN_ANALYZE_BARS:
        raise HTTPException(
            status_code=422,
            detail=problem_detail(
                422, "INSUFFICIENT_HISTORY", "Not enough historical data for analysis",
                f"Need at least {_MIN_ANALYZE_BARS} bars for SMA50; have {len(req.bars)}",
                "/analyze",
            ),
        )

    result = compute_all_indicators(req.bars)
    idx = _last_computable_index(result)
    snap = _snapshot_at(result, idx)

    close: Any = snap["sma200"]  # placeholder replaced below
    if idx >= 0:
        close = float(req.bars[idx].close)
    sma20, sma50 = snap["sma20"], snap["sma50"]
    rsi = snap["rsi14"]
    macd_val = snap["macd"]
    vol_ratio = snap["volume_ratio"]
    hist = macd_val["histogram"] if macd_val else None
    prev_macd = result.macd[idx - 1] if idx > 0 else None
    prev_hist = prev_macd["histogram"] if prev_macd else None

    signals: List[str] = []
    if close is not None and sma20 is not None:
        signals.append("price_above_sma20" if close > sma20 else "price_below_sma20")
    if close is not None and sma50 is not None:
        signals.append("price_above_sma50" if close > sma50 else "price_below_sma50")
    if rsi is not None:
        if rsi > 50:
            signals.append("rsi_bullish")
        elif rsi < 50:
            signals.append("rsi_bearish")
        if rsi >= 70:
            signals.append("rsi_overbought")
        if rsi <= 30:
            signals.append("rsi_oversold")
    if hist is not None:
        if hist > 0:
            signals.append("macd_positive")
        elif hist < 0:
            signals.append("macd_negative")
        if prev_hist is not None:
            if hist > prev_hist:
                signals.append("macd_rising")
            elif hist < prev_hist:
                signals.append("macd_falling")
    if vol_ratio is not None:
        if vol_ratio > 1.5:
            signals.append("volume_surge")
        if vol_ratio < 0.5:
            signals.append("volume_dry")

    bullish = bool(
        close is not None and sma20 is not None and sma50 is not None
        and hist is not None and close > sma20 and close > sma50 and hist > 0
    )
    bearish = bool(
        close is not None and sma20 is not None and sma50 is not None
        and hist is not None and close < sma20 and close < sma50 and hist < 0
    )
    trend = "BULLISH" if bullish else ("BEARISH" if bearish else "SIDEWAYS")

    strength = (
        sum(
            [
                1 if (close is not None and sma20 is not None and close > sma20) else 0,
                1 if (close is not None and sma50 is not None and close > sma50) else 0,
                1 if (hist is not None and hist > 0) else 0,
                1 if (rsi is not None and rsi > 50) else 0,
                1 if (vol_ratio is not None and vol_ratio > 1.0) else 0,
            ]
        )
        / 5.0
    )

    return AnalyzeResponse(
        symbol=req.symbol,
        timeframe=req.timeframe,
        analysis={
            "indicators": {
                "ma_20": sma20,
                "ma_50": sma50,
                "rsi": rsi,
                "volume": (float(req.bars[idx].volume) if idx >= 0 else None),
                "macd": macd_val,
                "vwap": snap["vwap"],
            },
            "signals": signals,
            "trend": trend,
            "strength": strength,
        },
        timestamp=now_iso(),
    )


# --------------------------------------------------------------------------- #
# POST /rank (frozen UC-AE-3 contract, §4)
# --------------------------------------------------------------------------- #
@app.post("/rank", response_model=RankResponse)
async def rank(req: RankRequest) -> RankResponse:
    _require_supported_version(req.algorithm_version, "/rank")

    # C6: unresolvable symbols surface an explicit error — no silent drops.
    missing = [s for s in req.symbols if s not in req.series]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=problem_detail(
                400, "INVALID_INPUT", "Request validation failed",
                f"no OHLCV series provided for symbol(s): {', '.join(missing)}",
                "/rank",
                errors=[{"field": "series", "message": f"missing series for {s}"} for s in missing],
            ),
        )

    weights = req.weights or dict(_DEFAULT_WEIGHTS)

    indicators_by_symbol: Dict[str, Dict[str, Any]] = {}
    results_by_symbol: Dict[str, IndicatorsResult] = {}
    for symbol in req.symbols:
        result = compute_all_indicators(req.series[symbol])
        results_by_symbol[symbol] = result
        indicators_by_symbol[symbol] = _to_rank_inputs(symbol, result)

    try:
        results = rank_symbols(
            indicators_by_symbol=indicators_by_symbol,
            screened_symbols=req.symbols,
            weights=weights,
            version=req.algorithm_version,
        )
    except RankingError as exc:
        raise HTTPException(
            status_code=400,
            detail=problem_detail(
                400, "INVALID_INPUT", "Request validation failed", str(exc), "/rank"
            ),
        ) from exc

    # C3: split ranked[] / excluded[] (contract §4 response shape).
    ranked_out: List[Dict[str, Any]] = []
    excluded_out: List[Dict[str, Any]] = []
    for r in results:
        if r.get("excluded"):
            excluded_out.append(
                {
                    "symbol": r["symbol"],
                    "reason": r.get("exclusion_reason", "insufficient_data"),
                    "missing_indicators": _missing_indicators(results_by_symbol[r["symbol"]]),
                }
            )
        else:
            ranked_out.append(
                {
                    "rank": r["rank"],
                    "symbol": r["symbol"],
                    "composite_score": r["composite_score"],
                    "components": r["component_scores"],  # dict shape per contract
                    "sub_components": r["sub_components"],
                    "reasoning": r["reasoning"],
                }
            )
    # Re-number ranks sequentially over the ranked-only list (deterministic).
    for i, entry in enumerate(ranked_out):
        entry["rank"] = i + 1

    return RankResponse(
        algorithm_version=req.algorithm_version,
        as_of_date=req.as_of_date,
        ranked_at=now_iso(),
        weights_used=weights,
        ranked=ranked_out,
        excluded=excluded_out,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.analysis_engine_port)
