"""Deterministic, versioned screening module for the vnstock-advisor analysis-engine.

This module implements the v1.0 screening criteria (AND logic):
  1. Price > SMA20
  2. RSI14 < 70
  3. Volume > 1.5 * Volume_SMA20

Thresholds are configurable via environment variables but v1.0 defaults are immutable.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field as dc_field
from typing import List, Optional, Dict, Any

from .indicators import IndicatorsResult


# --------------------------------------------------------------------------- #
# Configuration (v1.0 defaults — immutable per versioning policy)
# --------------------------------------------------------------------------- #
SCREEN_PRICE_GT_SMA20 = os.getenv("SCREEN_PRICE_GT_SMA20", "true").lower() == "true"
SCREEN_RSI_MAX = float(os.getenv("SCREEN_RSI_MAX", "70"))
SCREEN_VOLUME_RATIO_MIN = float(os.getenv("SCREEN_VOLUME_RATIO_MIN", "1.5"))

SCREEN_VERSION = "v1.0"
MIN_BARS_REQUIRED = 20


@dataclass(frozen=True)
class CriterionEvaluation:
    """Per-criterion evaluation result."""
    pass_: bool
    price: Optional[float] = None
    sma20: Optional[float] = None
    diff_pct: Optional[float] = None
    rsi: Optional[float] = None
    threshold: Optional[float] = None
    volume: Optional[float] = None
    avg_volume: Optional[float] = None
    ratio: Optional[float] = None


@dataclass(frozen=True)
class ScreenResult:
    """Screening result for a single symbol."""
    symbol: str
    passed: bool
    evaluations: Dict[str, CriterionEvaluation] = dc_field(default_factory=dict)
    excluded: bool = False
    exclusion_reason: Optional[str] = None
    version: str = SCREEN_VERSION


def _get_last_valid(values: List[Optional[float]]) -> Optional[float]:
    """Get the last non-None value from a list."""
    for v in reversed(values):
        if v is not None:
            return v
    return None


def _evaluate_price_gt_sma20(result: IndicatorsResult) -> CriterionEvaluation:
    """Evaluate criterion 1: Price > SMA20."""
    price = _get_last_valid(result.closes)
    sma20 = _get_last_valid(result.sma20)
    
    if price is None or sma20 is None:
        return CriterionEvaluation(pass_=False, price=price, sma20=sma20)
    
    diff_pct = round((price - sma20) / sma20 * 100, 2)
    return CriterionEvaluation(
        pass_=price > sma20,
        price=price,
        sma20=sma20,
        diff_pct=diff_pct,
    )


def _evaluate_rsi_lt_70(result: IndicatorsResult) -> CriterionEvaluation:
    """Evaluate criterion 2: RSI14 < 70."""
    rsi = _get_last_valid(result.rsi14)
    
    if rsi is None:
        return CriterionEvaluation(pass_=False, rsi=rsi, threshold=SCREEN_RSI_MAX)
    
    return CriterionEvaluation(
        pass_=rsi < SCREEN_RSI_MAX,
        rsi=rsi,
        threshold=SCREEN_RSI_MAX,
    )


def _evaluate_volume_gt_avg(result: IndicatorsResult) -> CriterionEvaluation:
    """Evaluate criterion 3: Volume > 1.5 * Volume_SMA20."""
    # Get last volume from the raw data - we need to get it from the closes/volumes
    # The IndicatorsResult doesn't store raw volume, but we can compute from volume_sma and volume_ratio
    # Actually, we need the raw volume. Let's check what's available.
    # The IndicatorsResult has volume_ratio = volume / volume_sma
    # And volume_sma is available. So volume = volume_ratio * volume_sma
    
    volume_ratio = _get_last_valid(result.volume_ratio)
    volume_sma = _get_last_valid(result.volume_sma)
    
    if volume_ratio is None or volume_sma is None or volume_sma == 0:
        return CriterionEvaluation(
            pass_=False,
            volume=None,
            avg_volume=volume_sma,
            ratio=volume_ratio,
        )
    
    volume = volume_ratio * volume_sma
    return CriterionEvaluation(
        pass_=volume_ratio > SCREEN_VOLUME_RATIO_MIN,
        volume=round(volume),
        avg_volume=round(volume_sma),
        ratio=round(volume_ratio, 2),
    )


def _has_sufficient_data(result: IndicatorsResult) -> bool:
    """Check if symbol has at least 20 valid bars for screening."""
    # Need SMA20 (20 bars), RSI14 (15 bars), Volume_SMA20 (20 bars)
    # Most restrictive is 20 bars
    sma20_last = _get_last_valid(result.sma20)
    rsi14_last = _get_last_valid(result.rsi14)
    vol_sma_last = _get_last_valid(result.volume_sma)
    
    return all(v is not None for v in [sma20_last, rsi14_last, vol_sma_last])


def screen_symbols(
    indicators_by_symbol: Dict[str, IndicatorsResult],
    as_of_date: Optional[str] = None,
    version: str = SCREEN_VERSION,
) -> Dict[str, ScreenResult]:
    """Screen symbols against v1.0 criteria.
    
    Args:
        indicators_by_symbol: Mapping of symbol -> IndicatorsResult from compute_all_indicators
        as_of_date: Optional date string for audit trail (not used in computation)
        version: Screening version (only "v1.0" supported)
    
    Returns:
        Dict mapping symbol -> ScreenResult with passed/evaluations or excluded/reason
    
    Deterministic: same input + same version -> bit-identical output.
    """
    if version != "v1.0":
        raise ValueError(f"Unsupported screening version: {version}. Only v1.0 is implemented.")
    
    results: Dict[str, ScreenResult] = {}
    
    for symbol, ind_result in indicators_by_symbol.items():
        if not _has_sufficient_data(ind_result):
            results[symbol] = ScreenResult(
                symbol=symbol,
                passed=False,
                excluded=True,
                exclusion_reason="insufficient_data",
                version=version,
            )
            continue
        
        eval_price = _evaluate_price_gt_sma20(ind_result)
        eval_rsi = _evaluate_rsi_lt_70(ind_result)
        eval_volume = _evaluate_volume_gt_avg(ind_result)
        
        all_passed = eval_price.pass_ and eval_rsi.pass_ and eval_volume.pass_
        
        evaluations = {
            "price_gt_sma20": eval_price,
            "rsi_lt_70": eval_rsi,
            "volume_gt_1_5x_avg": eval_volume,
        }
        
        results[symbol] = ScreenResult(
            symbol=symbol,
            passed=all_passed,
            evaluations=evaluations,
            version=version,
        )
    
    return results


def screen_result_to_dict(result: ScreenResult) -> Dict[str, Any]:
    """Convert ScreenResult to JSON-serializable dict."""
    if result.excluded:
        return {
            "symbol": result.symbol,
            "passed": False,
            "excluded": True,
            "exclusion_reason": result.exclusion_reason,
            "version": result.version,
        }
    
    evals = {}
    for key, eval_ in result.evaluations.items():
        evals[key] = {
            k: v for k, v in {
                "pass": eval_.pass_,
                "price": eval_.price,
                "sma20": eval_.sma20,
                "diff_pct": eval_.diff_pct,
                "rsi": eval_.rsi,
                "threshold": eval_.threshold,
                "volume": eval_.volume,
                "avg_volume": eval_.avg_volume,
                "ratio": eval_.ratio,
            }.items() if v is not None
        }
    
    return {
        "symbol": result.symbol,
        "passed": result.passed,
        "evaluations": evals,
        "version": result.version,
    }


def screen_symbols_to_dict(
    indicators_by_symbol: Dict[str, IndicatorsResult],
    as_of_date: Optional[str] = None,
    version: str = SCREEN_VERSION,
) -> Dict[str, Dict[str, Any]]:
    """Screen symbols and return JSON-serializable dict."""
    results = screen_symbols(indicators_by_symbol, as_of_date, version)
    return {sym: screen_result_to_dict(res) for sym, res in results.items()}