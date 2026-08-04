"""Tests for the screening module."""

import pytest
from analysis_engine.indicators import IndicatorsResult, OHLCV, compute_all_indicators
from analysis_engine.screening import (
    screen_symbols,
    screen_symbols_to_dict,
    ScreenResult,
    SCREEN_VERSION,
)


def create_test_indicators_result(
    symbol: str,
    closes: list[float],
    highs: list[float],
    lows: list[float],
    volumes: list[int],
) -> IndicatorsResult:
    """Create an IndicatorsResult from OHLCV data."""
    ohlcv = [
        OHLCV(time=f"2024-01-{i+1:02d}", open=c, high=h, low=l, close=c, volume=v)
        for i, (c, h, l, v) in enumerate(zip(closes, highs, lows, volumes))
    ]
    return compute_all_indicators(ohlcv)


def _make_passing_data(n_bars: int = 25) -> tuple:
    """Generate OHLCV data that passes all screening criteria.
    
    Returns: (closes, highs, lows, volumes)
    - Gentle uptrend with some down days (RSI ~65)
    - Volume spike in last 5 bars (ratio > 1.5)
    """
    closes = [100.0]
    for i in range(n_bars - 1):
        if i % 4 == 0:
            closes.append(round(closes[-1] * 0.995, 2))  # Down day
        else:
            closes.append(round(closes[-1] * 1.003, 2))  # Up day
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    volumes = [1000000] * (n_bars - 5) + [4000000] * 5
    return closes, highs, lows, volumes


def _make_failing_price_data(n_bars: int = 25) -> tuple:
    """Generate OHLCV data that fails price > SMA20 (downtrend)."""
    closes = [100.0]
    for i in range(n_bars - 1):
        closes.append(round(closes[-1] * 0.995, 2))  # Steady downtrend
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    volumes = [1000000] * (n_bars - 5) + [4000000] * 5  # Volume spike at end
    return closes, highs, lows, volumes


def _make_failing_rsi_data(n_bars: int = 25) -> tuple:
    """Generate OHLCV data that fails RSI < 70 (overbought)."""
    closes = [100.0]
    for i in range(n_bars - 1):
        closes.append(round(closes[-1] * 1.02, 2))  # Sharp uptrend
    highs = [c + 0.5 for c in closes]
    lows = [c - 0.5 for c in closes]
    volumes = [1500000] * n_bars
    return closes, highs, lows, volumes


def _make_failing_volume_data(n_bars: int = 25) -> tuple:
    """Generate OHLCV data that fails volume > 1.5x avg (low volume)."""
    closes = [100.0]
    for i in range(n_bars - 1):
        if i % 4 == 0:
            closes.append(round(closes[-1] * 0.995, 2))
        else:
            closes.append(round(closes[-1] * 1.003, 2))
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    volumes = [500000] * n_bars  # Low volume throughout
    return closes, highs, lows, volumes


def _make_insufficient_data(n_bars: int = 15) -> tuple:
    """Generate OHLCV data with insufficient bars."""
    closes = [100 + i * 0.5 for i in range(n_bars)]
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    volumes = [1000000] * n_bars
    return closes, highs, lows, volumes


def test_screen_passes_all_criteria():
    """Symbol passes all three v1.0 criteria."""
    closes, highs, lows, volumes = _make_passing_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    assert "VNM" in results
    result = results["VNM"]
    assert result.passed is True
    assert result.excluded is False
    assert result.version == SCREEN_VERSION
    
    evals = result.evaluations
    assert evals["price_gt_sma20"].pass_ is True
    assert evals["rsi_lt_70"].pass_ is True
    assert evals["volume_gt_1_5x_avg"].pass_ is True


def test_screen_fails_price_criterion():
    """Symbol fails Price > SMA20 (downtrend)."""
    closes, highs, lows, volumes = _make_failing_price_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    result = results["VNM"]
    assert result.passed is False
    assert result.evaluations["price_gt_sma20"].pass_ is False
    assert result.evaluations["rsi_lt_70"].pass_ is True  # RSI should be low in downtrend
    assert result.evaluations["volume_gt_1_5x_avg"].pass_ is True


def test_screen_fails_rsi_criterion():
    """Symbol fails RSI < 70 (overbought)."""
    closes, highs, lows, volumes = _make_failing_rsi_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    result = results["VNM"]
    assert result.passed is False
    assert result.evaluations["price_gt_sma20"].pass_ is True
    assert result.evaluations["rsi_lt_70"].pass_ is False
    assert result.evaluations["rsi_lt_70"].rsi is not None
    assert result.evaluations["rsi_lt_70"].rsi >= 70


def test_screen_fails_volume_criterion():
    """Symbol fails Volume > 1.5x avg (low volume)."""
    closes, highs, lows, volumes = _make_failing_volume_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    result = results["VNM"]
    assert result.passed is False
    assert result.evaluations["price_gt_sma20"].pass_ is True
    assert result.evaluations["rsi_lt_70"].pass_ is True
    assert result.evaluations["volume_gt_1_5x_avg"].pass_ is False


def test_screen_insufficient_data():
    """Symbol with < 20 bars is excluded."""
    closes, highs, lows, volumes = _make_insufficient_data(15)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    result = results["VNM"]
    assert result.passed is False
    assert result.excluded is True
    assert result.exclusion_reason == "insufficient_data"
    assert len(result.evaluations) == 0


def test_screen_multiple_symbols_mixed():
    """Test screening multiple symbols with mixed pass/fail/excluded."""
    # VNM: passes all
    closes_vnm, highs_vnm, lows_vnm, volumes_vnm = _make_passing_data(25)
    
    # VIC: fails price (downtrend)
    closes_vic, highs_vic, lows_vic, volumes_vic = _make_failing_price_data(25)
    
    # FPT: insufficient data (15 bars)
    closes_fpt, highs_fpt, lows_fpt, volumes_fpt = _make_insufficient_data(15)
    
    ind_vnm = create_test_indicators_result("VNM", closes_vnm, highs_vnm, lows_vnm, volumes_vnm)
    ind_vic = create_test_indicators_result("VIC", closes_vic, highs_vic, lows_vic, volumes_vic)
    ind_fpt = create_test_indicators_result("FPT", closes_fpt, highs_fpt, lows_fpt, volumes_fpt)
    
    results = screen_symbols({"VNM": ind_vnm, "VIC": ind_vic, "FPT": ind_fpt})
    
    assert results["VNM"].passed is True
    assert results["VNM"].excluded is False
    
    assert results["VIC"].passed is False
    assert results["VIC"].excluded is False
    assert results["VIC"].evaluations["price_gt_sma20"].pass_ is False
    
    assert results["FPT"].passed is False
    assert results["FPT"].excluded is True
    assert results["FPT"].exclusion_reason == "insufficient_data"


def test_screen_deterministic():
    """Same input + same version = identical output."""
    closes, highs, lows, volumes = _make_passing_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    
    results1 = screen_symbols_to_dict({"VNM": ind})
    results2 = screen_symbols_to_dict({"VNM": ind})
    
    assert results1 == results2  # Bit-identical


def test_screen_version_rejection():
    """Unsupported version raises ValueError."""
    closes, highs, lows, volumes = _make_failing_rsi_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    
    with pytest.raises(ValueError, match="Unsupported screening version"):
        screen_symbols({"VNM": ind}, version="v2.0")


def test_screen_evaluation_details():
    """Check evaluation output contains expected metrics."""
    closes, highs, lows, volumes = _make_passing_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols({"VNM": ind})
    
    result = results["VNM"]
    evals = result.evaluations
    
    # price_gt_sma20
    assert evals["price_gt_sma20"].price is not None
    assert evals["price_gt_sma20"].sma20 is not None
    assert evals["price_gt_sma20"].diff_pct is not None
    
    # rsi_lt_70
    assert evals["rsi_lt_70"].rsi is not None
    assert evals["rsi_lt_70"].threshold == 70
    
    # volume_gt_1_5x_avg
    assert evals["volume_gt_1_5x_avg"].volume is not None
    assert evals["volume_gt_1_5x_avg"].avg_volume is not None
    assert evals["volume_gt_1_5x_avg"].ratio is not None


def test_screen_to_dict_format():
    """Test JSON-serializable dict output format."""
    closes, highs, lows, volumes = _make_passing_data(25)
    ind = create_test_indicators_result("VNM", closes, highs, lows, volumes)
    results = screen_symbols_to_dict({"VNM": ind})
    
    result = results["VNM"]
    assert result["symbol"] == "VNM"
    assert result["passed"] is True
    assert result["version"] == SCREEN_VERSION
    assert "evaluations" in result
    assert "price_gt_sma20" in result["evaluations"]
    assert "rsi_lt_70" in result["evaluations"]
    assert "volume_gt_1_5x_avg" in result["evaluations"]
    
    # Check excluded format
    closes_short, highs_short, lows_short, volumes_short = _make_insufficient_data(15)
    ind_short = create_test_indicators_result("ABC", closes_short, highs_short, lows_short, volumes_short)
    results_short = screen_symbols_to_dict({"ABC": ind_short})
    
    result_short = results_short["ABC"]
    assert result_short["symbol"] == "ABC"
    assert result_short["passed"] is False
    assert result_short["excluded"] is True
    assert result_short["exclusion_reason"] == "insufficient_data"
    assert "evaluations" not in result_short or result_short["evaluations"] == {}


def test_all_pass_universe():
    """All symbols pass screening."""
    symbols = ["VNM", "VIC", "FPT", "HPG", "MWG"]
    indicators = {}
    
    for sym in symbols:
        closes, highs, lows, volumes = _make_passing_data(25)
        indicators[sym] = create_test_indicators_result(sym, closes, highs, lows, volumes)
    
    results = screen_symbols(indicators)
    
    for sym in symbols:
        assert results[sym].passed is True
        assert results[sym].excluded is False


def test_all_fail_universe():
    """All symbols fail screening."""
    symbols = ["VNM", "VIC", "FPT"]
    indicators = {}
    
    for sym in symbols:
        # Downtrend, overbought, low volume
        closes, highs, lows, volumes = _make_failing_volume_data(25)
        indicators[sym] = create_test_indicators_result(sym, closes, highs, lows, volumes)
    
    results = screen_symbols(indicators)
    
    for sym in symbols:
        assert results[sym].passed is False
        assert results[sym].excluded is False