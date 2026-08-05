"""Pure-Python technical indicator computations for the vnstock-advisor analysis-engine.

This module intentionally has **zero external runtime dependencies** (no FastAPI,
no database, no network, no pydantic/sqlalchemy). It only uses the Python
standard library (``dataclasses``, ``math``). This makes it importable from any
environment and trivially testable in isolation.

Formulas follow ``docs/specs/indicators.md`` v1.0 exactly:
  * SMA/EMA use the reference implementations from the spec (Wilder seeding).
  * RSI uses Wilder smoothing.
  * MACD propagates ``None`` gaps through EMA -> MACD line -> signal -> histogram.
  * Volume Profile supports rolling VWAP with zero-volume fallback to close.
  * ROC10, ATR14 and OBV are computed per spec section 6 for the ranking consumer.

Rounding conventions (spec §Conventions)
  * prices           -> 4 decimals
  * RSI / percentages -> 2 decimals
  * volume           -> 0 decimals

Edge-case conventions
  * Insufficient data -> ``None`` plus a warning string recorded in the result
  * Price gaps from the ingest layer arrive as bars whose price/volume inputs may
    be missing; those propagate ``None`` per the spec's gap rules.
  * Flat market (no price change) -> RSI = 50.0 by the 0/0 convention.
  * Zero-volume window -> VWAP falls back to the close price.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field as dc_field
from typing import List, Optional, Union

__all__ = [
    "OHLCV",
    "IndicatorsResult",
    "sma",
    "ema",
    "rsi",
    "macd",
    "volume_profile",
    "roc",
    "atr",
    "obv",
    "compute_all_indicators",
]


@dataclass(frozen=True)
class OHLCV:
    """A single price bar. Minimal stand-in for the market-data row.

    The analysis-engine ``compute_all_indicators`` accepts any object exposing the
    ``open``/``high``/``low``/``close``/``volume`` attributes (duck-typed), so this
    dataclass is a convenience default rather than a hard requirement.
    """

    time: Optional[str]
    open: float
    high: float
    low: float
    close: float
    volume: int


# --------------------------------------------------------------------------- #
# Low level helpers
# --------------------------------------------------------------------------- #
_NUM = Union[float, int, None]


def _num(value) -> Optional[float]:
    """Coerce a numeric-ish value to ``float`` or ``None`` (if NaN/missing)."""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


# --------------------------------------------------------------------------- #
# 1. Simple Moving Average (SMA)
# --------------------------------------------------------------------------- #
def sma(closes: List[Optional[float]], period: int) -> List[Optional[float]]:
    """Simple moving average over ``period`` bars (spec §1).

    Missing values in the window make that ``t`` a ``None`` (gap rule). Output
    rounded to 4 decimals.
    """
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result: List[Optional[float]] = [None] * n
    if n < period:
        return result
    # Ring buffer to avoid O(n*P) rescanning.
    acc = 0.0
    window: List[Optional[float]] = []
    for t in range(n):
        value = _num(closes[t])
        window.append(value)
        acc += value if value is not None else 0.0
        if len(window) > period:
            old = window.pop(0)
            acc -= old if old is not None else 0.0
        if len(window) < period:
            continue
        if any(v is None for v in window):
            result[t] = None
        else:
            result[t] = round(acc / period, 4)
    return result


# --------------------------------------------------------------------------- #
# 2. Exponential Moving Average (EMA, Wilder)
# --------------------------------------------------------------------------- #
def ema(
    closes: List[Optional[float]],
    period: int,
    alpha: Optional[float] = None,
) -> List[Optional[float]]:
    """Wilder-smoothed EMA (spec §2). Seed = SMA of first ``period`` closes.

    A gap in the seed window or after the seed propagates ``None`` forward --
    matching the spec's reference implementation, where once the running value
    becomes ``None`` it never self-heals (gaps reset the series).
    """
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result: List[Optional[float]] = [None] * n
    if n < period:
        return result
    a = alpha if alpha is not None else 1.0 / period
    # Seed with SMA of the first `period` closes; any gap => all None.
    seed_values = [_num(c) for c in closes[:period]]
    if any(v is None for v in seed_values):
        return result
    seed = sum(seed_values) / period  # type: ignore[arg-type]
    result[period - 1] = round(seed, 4)
    for t in range(period, n):
        cur = _num(closes[t])
        if cur is None or result[t - 1] is None:
            result[t] = None
        else:
            result[t] = round(cur * a + result[t - 1] * (1 - a), 4)
    return result


# --------------------------------------------------------------------------- #
# 3. Relative Strength Index (RSI, Wilder)
# --------------------------------------------------------------------------- #
def rsi(closes: List[Optional[float]], period: int = 14) -> List[Optional[float]]:
    """Wilder RSI (spec §3). Rounded to 2 decimals.

    Flat market (all deltas zero) yields RSI = 50.0 (the 0/0 convention).
    A gap in a delta sets that index to ``None`` and (matching the reference
    implementation) leaves it ``None`` thereafter.
    """
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result: List[Optional[float]] = [None] * n
    if n <= period:
        return result
    deltas: List[Optional[float]] = [None] * n
    for i in range(1, n):
        pc = _num(closes[i - 1])
        cc = _num(closes[i])
        deltas[i] = (cc - pc) if (pc is not None and cc is not None) else None
    gains = [max(d, 0.0) if d is not None else None for d in deltas]
    losses = [max(-d, 0.0) if d is not None else None for d in deltas]

    first_idx = period
    valid_gains = [g for g in gains[1 : first_idx + 1] if g is not None]
    valid_losses = [l for l in losses[1 : first_idx + 1] if l is not None]
    if len(valid_gains) < period or len(valid_losses) < period:
        return result

    avg_gain = sum(valid_gains) / period  # type: ignore[arg-type]
    avg_loss = sum(valid_losses) / period  # type: ignore[arg-type]

    def _rsi_value(ag: float, al: float) -> float:
        if al == 0 and ag == 0:
            return 50.0
        if al == 0:
            return 100.0 if ag > 0 else 0.0
        rs = ag / al
        return round(100 - 100 / (1 + rs), 2)

    result[first_idx] = _rsi_value(avg_gain, avg_loss)
    for t in range(first_idx + 1, n):
        if gains[t] is None or losses[t] is None:
            result[t] = None
            continue
        avg_gain = (avg_gain * (period - 1) + gains[t]) / period  # type: ignore[operator]
        avg_loss = (avg_loss * (period - 1) + losses[t]) / period  # type: ignore[operator]
        result[t] = _rsi_value(avg_gain, avg_loss)
    return result


# --------------------------------------------------------------------------- #
# 4. Moving Average Convergence Divergence (MACD)
# --------------------------------------------------------------------------- #
def macd(
    closes: List[Optional[float]],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> List[Optional[dict]]:
    """MACD line / signal / histogram (spec §4). Rounded to 4 decimals.

    Returns a per-index list of ``None`` (insufficient data / gap) or a dict with
    keys ``macd``, ``signal``, ``histogram``.
    """
    if fast >= slow:
        raise ValueError("fast_period must be < slow_period")
    n = len(closes)
    result: List[Optional[dict]] = [None] * n
    if n < slow + signal - 1:
        return result

    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)

    macd_line: List[Optional[float]] = [None] * n
    for t in range(n):
        if ema_fast[t] is not None and ema_slow[t] is not None:
            macd_line[t] = round(ema_fast[t] - ema_slow[t], 4)  # type: ignore[operator]

    # Signal line: EMA of the (filtered) MACD line, then remapped to original idx.
    valid_macd = [(i, v) for i, v in enumerate(macd_line) if v is not None]
    if len(valid_macd) < signal:
        return result
    macd_values = [v for _, v in valid_macd]
    signal_ema = ema(macd_values, signal)
    signal_line: List[Optional[float]] = [None] * n
    for (idx, _), sig in zip(valid_macd[signal - 1 :], signal_ema[signal - 1 :]):
        if sig is not None:
            signal_line[idx] = round(sig, 4)

    for t in range(n):
        if macd_line[t] is not None and signal_line[t] is not None:
            result[t] = {
                "macd": macd_line[t],
                "signal": signal_line[t],
                "histogram": round(macd_line[t] - signal_line[t], 4),
            }
    return result


# --------------------------------------------------------------------------- #
# 5. Volume Profile (VWAP / Volume SMA / Volume Ratio)
# --------------------------------------------------------------------------- #
def volume_profile(
    highs: List[Optional[float]],
    lows: List[Optional[float]],
    closes: List[Optional[float]],
    volumes: List[Optional[int]],
    volume_sma_period: int = 20,
) -> List[Optional[dict]]:
    """Rolling VWAP, volume SMA and volume ratio (spec §5).

    Edge behaviour:
      * all-volume-zero window -> VWAP falls back to ``closes[t]``
      * volume SMA == 0 or missing -> volume ratio ``None`` (never 0 / INF)
    """
    if volume_sma_period < 2:
        raise ValueError("volume_sma_period must be >= 2")
    n = len(closes)
    result: List[Optional[dict]] = [None] * n
    if n < volume_sma_period:
        return result

    typical: List[Optional[float]] = [None] * n
    for i in range(n):
        h, lo, c = _num(highs[i]), _num(lows[i]), _num(closes[i])
        if h is not None and lo is not None and c is not None:
            typical[i] = (h + lo + c) / 3

    vol_sma = sma([_num(v) for v in volumes], volume_sma_period)

    vwap: List[Optional[float]] = [None] * n
    for t in range(volume_sma_period - 1, n):
        pv_sum = 0.0
        v_sum = 0
        for i in range(t - volume_sma_period + 1, t + 1):
            tv = typical[i]
            v = volumes[i] if volumes[i] is not None else 0
            if tv is not None:
                pv_sum += tv * v
            v_sum += v
        if v_sum > 0:
            vwap[t] = round(pv_sum / v_sum, 4)
        else:
            vwap[t] = (_num(closes[t]) if _num(closes[t]) is not None else None)

    vol_ratio: List[Optional[float]] = [None] * n
    for t in range(n):
        if vol_sma[t] is not None and vol_sma[t] > 0:
            vol_ratio[t] = round((volumes[t] or 0) / vol_sma[t], 4)

    for t in range(n):
        if vol_sma[t] is not None:
            result[t] = {
                "vwap": vwap[t],
                "volume_sma": round(vol_sma[t], 0),
                "volume_ratio": vol_ratio[t],
            }
    return result


# --------------------------------------------------------------------------- #
# 6. Additional indicators used by the ranker
# --------------------------------------------------------------------------- #
def roc(closes: List[Optional[float]], period: int = 10) -> List[Optional[float]]:
    """Rate of change (spec §6.1), in percent, rounded to 2 decimals."""
    if period < 1:
        raise ValueError("period must be >= 1")
    n = len(closes)
    result: List[Optional[float]] = [None] * n
    for t in range(period, n):
        prev = _num(closes[t - period])
        cur = _num(closes[t])
        if prev is not None and cur is not None and prev != 0:
            result[t] = round((cur - prev) / prev * 100, 2)
        else:
            result[t] = None
    return result


def atr(
    highs: List[Optional[float]],
    lows: List[Optional[float]],
    closes: List[Optional[float]],
    period: int = 14,
) -> List[Optional[float]]:
    """Average True Range with Wilder smoothing (spec §6.2). Rounded 4 decimals."""
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result: List[Optional[float]] = [None] * n
    if n < period:
        return result

    tr: List[Optional[float]] = [None] * n
    for t in range(n):
        h, lo, c = _num(highs[t]), _num(lows[t]), _num(closes[t])
        if h is None or lo is None:
            tr[t] = None
            continue
        if t == 0:
            tr[t] = h - lo
            continue
        prev_c = _num(closes[t - 1])
        if prev_c is None:
            tr[t] = None
            continue
        tr[t] = max(h - lo, abs(h - prev_c), abs(lo - prev_c))

    # Seed = SMA of first `period` TR values (indices 1..period per spec).
    seed_vals = [v for v in tr[1 : period + 1] if v is not None]
    if len(seed_vals) < period:
        return result
    atr_val = sum(seed_vals) / period  # type: ignore[arg-type]
    result[period] = round(atr_val, 4)
    for t in range(period + 1, n):
        tv = tr[t]
        if tv is None:
            result[t] = None
            continue
        atr_val = (atr_val * (period - 1) + tv) / period
        result[t] = round(atr_val, 4)
    return result


def obv(closes: List[Optional[float]], volumes: List[Optional[int]]) -> List[Optional[int]]:
    """On-Balance Volume (spec §6.3). Rounded to integer volume."""
    n = len(closes)
    result: List[Optional[int]] = [None] * n
    if n == 0:
        return result
    result[0] = volumes[0] if volumes[0] is not None else 0
    for t in range(1, n):
        c_prev = _num(closes[t - 1])
        c_cur = _num(closes[t])
        obv_prev = result[t - 1]
        v = volumes[t] if volumes[t] is not None else 0
        if c_prev is None or c_cur is None or obv_prev is None:
            result[t] = None
            continue
        if c_cur > c_prev:
            result[t] = obv_prev + v
        elif c_cur < c_prev:
            result[t] = obv_prev - v
        else:
            result[t] = obv_prev
    return result


# --------------------------------------------------------------------------- #
# Aggregator
# --------------------------------------------------------------------------- #
@dataclass
class IndicatorsResult:
    """Structured result of ``compute_all_indicators``.

    Each list is aligned to the (ascending) input bars. ``None`` means the value
    is not computable at that index (insufficient data / gap).
    """

    symbol: str = ""
    # trend / momentum
    sma20: List[Optional[float]] = dc_field(default_factory=list)
    sma50: List[Optional[float]] = dc_field(default_factory=list)
    sma200: List[Optional[float]] = dc_field(default_factory=list)
    ema12: List[Optional[float]] = dc_field(default_factory=list)
    ema26: List[Optional[float]] = dc_field(default_factory=list)
    ema9: List[Optional[float]] = dc_field(default_factory=list)
    rsi14: List[Optional[float]] = dc_field(default_factory=list)
    macd: List[Optional[dict]] = dc_field(default_factory=list)
    # volume
    vwap: List[Optional[float]] = dc_field(default_factory=list)
    volume_sma: List[Optional[float]] = dc_field(default_factory=list)
    volume_ratio: List[Optional[float]] = dc_field(default_factory=list)
    # ranking-consumer indicators
    roc10: List[Optional[float]] = dc_field(default_factory=list)
    atr14: List[Optional[float]] = dc_field(default_factory=list)
    obv: List[Optional[int]] = dc_field(default_factory=list)
    # diagnostics
    warnings: List[str] = dc_field(default_factory=list)
    closes: List[Optional[float]] = dc_field(default_factory=list)

    def last(self, idx: int = -1) -> dict:
        """Return a compact dict of the last *computable* bar's indicators.

        Useful for callers/tests that want a single "as of now" snapshot.
        """
        n = len(self.rsi14)
        if n == 0:
            return {}
        return {
            "sma20": self.sma20[idx],
            "sma50": self.sma50[idx],
            "sma200": self.sma200[idx],
            "ema12": self.ema12[idx],
            "ema26": self.ema26[idx],
            "ema9": self.ema9[idx],
            "rsi14": self.rsi14[idx],
            "macd": self.macd[idx],
            "vwap": self.vwap[idx],
            "volume_sma": self.volume_sma[idx],
            "volume_ratio": self.volume_ratio[idx],
            "roc10": self.roc10[idx],
            "atr14": self.atr14[idx],
            "obv": self.obv[idx],
        }


def _extract(ohlcv: List) -> tuple:
    """Pull per-field arrays from a list of OHLCV-like objects."""
    closes: List[Optional[float]] = []
    highs: List[Optional[float]] = []
    lows: List[Optional[float]] = []
    volumes: List[Optional[int]] = []
    for row in ohlcv:
        closes.append(_num(getattr(row, "close", None)))
        highs.append(_num(getattr(row, "high", None)))
        lows.append(_num(getattr(row, "low", None)))
        v = getattr(row, "volume", None)
        volumes.append(None if v is None else int(v))
    return closes, highs, lows, volumes


def compute_all_indicators(
    ohlcv: List[OHLCV],
    volume_sma_period: int = 20,
) -> IndicatorsResult:
    """Compute all 8 indicator families over an ascending OHLCV series.

    ``ohlcv`` may be a list of ``indicators.OHLCV`` dataclasses or of any object
    exposing ``open``/``high``/``low``/``close``/``volume`` attributes (duck-typed),
    so the market-data rows from ``vnstock_shared`` work directly.
    """
    closes, highs, lows, volumes = _extract(ohlcv)
    n = len(closes)
    warnings: List[str] = []

    symbol = ""
    if ohlcv:
        symbol = str(getattr(ohlcv[0], "symbol", "")) or ""

    def _need_warn(indicator: str, need: int) -> None:
        if n < need:
            warnings.append(f"insufficient_data ({indicator}: need {need}, have {n})")

    sma20 = sma(closes, 20)
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    ema9 = ema(closes, 9)
    rsi14 = rsi(closes, 14)
    macd_res = macd(closes, 12, 26, 9)
    vp = volume_profile(highs, lows, closes, volumes, volume_sma_period)
    roc10 = roc(closes, 10)
    atr14 = atr(highs, lows, closes, 14)
    obv_res = obv(closes, volumes)

    _need_warn("SMA20", 20)
    _need_warn("SMA50", 50)
    _need_warn("SMA200", 200)
    _need_warn("MACD", 26 + 9 - 1)
    _need_warn("RSI14", 14 + 1)
    _need_warn("volume_SMA20", 20)
    _need_warn("ATR14", 14 + 1)
    _need_warn("ROC10", 10 + 1)

    # split the volume_profile dict list into columns
    vwap = [d["vwap"] if d else None for d in vp]
    volume_sma = [d["volume_sma"] if d else None for d in vp]
    volume_ratio = [d["volume_ratio"] if d else None for d in vp]

    res = IndicatorsResult(
        symbol=symbol,
        sma20=sma20,
        sma50=sma50,
        sma200=sma200,
        ema12=ema12,
        ema26=ema26,
        ema9=ema9,
        rsi14=rsi14,
        macd=macd_res,
        vwap=vwap,
        volume_sma=volume_sma,
        volume_ratio=volume_ratio,
        roc10=roc10,
        atr14=atr14,
        obv=obv_res,
        warnings=list(dict.fromkeys(warnings)),
        closes=closes,
    )
    return res