"""Indicator unit tests using fixture data."""

import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from indicators import (
    OHLCV,
    compute_all_indicators,
    rsi,
    macd,
    volume_profile,
    roc,
    atr,
    obv,
    sma,
    ema,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@dataclass
class OHLCVWithSymbol:
    """OHLCV with symbol attribute for testing."""
    time: Optional[str]
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str = ""


def load_fixture(name: str) -> list[OHLCVWithSymbol]:
    """Load a fixture file and convert to OHLCVWithSymbol objects."""
    path = FIXTURE_DIR / f"{name}.json"
    with open(path) as f:
        data = json.load(f)
    return [
        OHLCVWithSymbol(
            time=row["time"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
            symbol=row.get("symbol", ""),
        )
        for row in data
    ]


class TestNormalTrading:
    """Tests using the normal-trading.json fixture (realistic data)."""

    def test_compute_all_indicators_returns_result(self):
        ohlcv = load_fixture("normal-trading")
        result = compute_all_indicators(ohlcv)

        assert result.symbol == "VNM"
        assert len(result.closes) == len(ohlcv)
        # With 125+ bars, most indicators should have values
        assert result.sma20[-1] is not None
        assert result.sma50[-1] is not None
        assert result.rsi14[-1] is not None
        assert result.macd[-1] is not None
        assert result.vwap[-1] is not None
        assert result.roc10[-1] is not None
        assert result.atr14[-1] is not None
        assert result.obv[-1] is not None

    def test_rsi_in_range(self):
        ohlcv = load_fixture("normal-trading")
        closes = [float(row.close) for row in ohlcv]
        rsi_values = rsi(closes, 14)
        # RSI should be between 0 and 100
        valid_rsi = [v for v in rsi_values if v is not None]
        assert all(0 <= v <= 100 for v in valid_rsi)

    def test_macd_structure(self):
        ohlcv = load_fixture("normal-trading")
        closes = [float(row.close) for row in ohlcv]
        macd_values = macd(closes, 12, 26, 9)
        valid_macd = [v for v in macd_values if v is not None]
        assert len(valid_macd) > 0
        for m in valid_macd:
            assert "macd" in m
            assert "signal" in m
            assert "histogram" in m


class TestInsufficientData:
    """Tests using the insufficient-data.json fixture (short series)."""

    def test_insufficient_data_has_none_indicators(self):
        ohlcv = load_fixture("insufficient-data")
        result = compute_all_indicators(ohlcv)

        # With short series, early indicators should be None
        # The fixture has ~5 bars, so SMA20 should be None
        assert result.sma20[0] is None
        # RSI needs 14+1 bars, so should be None
        assert result.rsi14[0] is None


class TestFlatMarket:
    """Tests using the flat-market.json fixture (flat prices)."""

    def test_flat_market_rsi_near_50(self):
        ohlcv = load_fixture("flat-market")
        closes = [float(row.close) for row in ohlcv]
        rsi_values = rsi(closes, 14)

        # After the initial period, RSI should be near 50 for flat market
        valid_rsi = [v for v in rsi_values if v is not None]
        assert len(valid_rsi) > 0
        # Prices vary slightly (49989-50011), so RSI will be around 40-60
        for v in valid_rsi:
            assert 30 <= v <= 70, f"RSI {v} out of expected range for flat market"

    def test_flat_market_macd_near_zero(self):
        ohlcv = load_fixture("flat-market")
        closes = [float(row.close) for row in ohlcv]
        macd_values = macd(closes, 12, 26, 9)

        valid_macd = [v for v in macd_values if v is not None]
        assert len(valid_macd) > 0
        for m in valid_macd:
            # MACD line, signal, and histogram should be small for flat market
            assert abs(m["macd"]) < 1.0
            assert abs(m["signal"]) < 1.0
            assert abs(m["histogram"]) < 1.0


class TestLowVolume:
    """Tests using the low-volume.json fixture."""

    def test_low_volume_computes_without_error(self):
        ohlcv = load_fixture("low-volume")
        result = compute_all_indicators(ohlcv)

        # Should compute without crashing
        assert result.symbol is not None
        assert len(result.closes) == len(ohlcv)

    def test_volume_ratio_structure(self):
        ohlcv = load_fixture("low-volume")
        result = compute_all_indicators(ohlcv)

        # Volume ratio should be present (may be None or have values)
        assert hasattr(result, "volume_ratio")
        assert len(result.volume_ratio) == len(ohlcv)


class TestPriceGaps:
    """Tests using the price-gaps.json fixture."""

    def test_gaps_propagate_none(self):
        ohlcv = load_fixture("price-gaps")
        result = compute_all_indicators(ohlcv)

        # Gaps should propagate None values
        # The result should have some None values in the indicator series
        assert any(v is None for v in result.rsi14)
        assert any(v is None for v in result.sma20)


class TestStockSplits:
    """Tests using the stock-splits.json fixture."""

    def test_stock_splits_handled(self):
        ohlcv = load_fixture("stock-splits")
        result = compute_all_indicators(ohlcv)

        # Should compute without crashing
        assert result.symbol is not None
        assert len(result.closes) == len(ohlcv)


class TestEdgeCases:
    """Additional edge case tests."""

    def test_single_bar_returns_none(self):
        ohlcv = [
            OHLCV(time="2025-01-01T08:00:00+00:00", open=100, high=105, low=99, close=102, volume=1000)
        ]
        result = compute_all_indicators(ohlcv)

        # All indicators should be None with 1 bar
        assert result.sma20[0] is None
        assert result.rsi14[0] is None
        assert result.macd[0] is None

    def test_sma_rounding(self):
        closes = [100.0] * 20
        result = sma(closes, 20)
        assert result[-1] == 100.0  # Exactly 100.0, not 100.0001

    def test_ema_seed_is_sma(self):
        closes = [100.0, 101.0, 102.0, 103.0, 104.0]
        result = ema(closes, 3)
        # Seed at index 2 should be SMA of first 3: (100+101+102)/3 = 101
        assert result[2] == 101.0

    def test_obv_first_bar(self):
        closes = [100.0]
        volumes = [1000]
        result = obv(closes, volumes)
        assert result[0] == 1000

    def test_obv_up_day(self):
        closes = [100.0, 102.0]
        volumes = [1000, 500]
        result = obv(closes, volumes)
        assert result[1] == 1500  # 1000 + 500

    def test_obv_down_day(self):
        closes = [100.0, 98.0]
        volumes = [1000, 500]
        result = obv(closes, volumes)
        assert result[1] == 500  # 1000 - 500

    def test_obv_flat_day(self):
        closes = [100.0, 100.0]
        volumes = [1000, 500]
        result = obv(closes, volumes)
        assert result[1] == 1000  # unchanged


if __name__ == "__main__":
    pytest.main([__file__, "-v"])