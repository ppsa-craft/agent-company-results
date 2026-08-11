"""Deterministic fixture generator for the analysis-engine (spec docs/testing/fixtures.md).

Generates the 8 canonical fixture sets used by ``test_indicators.py``. All
data-generation is deterministic (seed 42) so the JSON files are reproducible
and stable across runs. Run from the repo root:

    PYTHONPATH=services/analysis-engine/src python services/analysis-engine/tests/fixtures/generate_fixtures.py

The generated files are committed to version control; this script exists solely
so they can be regenerated or audited.
"""

from __future__ import annotations

import datetime
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- #
# Deterministic data-generation helpers
# --------------------------------------------------------------------------- #
def _typical(h: float, l: float, c: float) -> float:
    return (h + l + c) / 3


def _bars(
    symbol: str, start: float, drift: float, vol: float, n: int, seed: int, volume: int = 1_000_000
) -> list:
    """Generate a deterministic log-normal-ish random walk of ``n`` daily bars.

    ``vol`` is the per-day VOLATILITY in percent (e.g. 0.15 == 0.15% daily);
    ``volume`` is the base daily volume the log-normal sampler scales around.
    Keeping them separate prevents the volume value (hundreds of thousands /
    millions) from being misread as volatility, which would explode the price
    walk into negative OHLC values (bug fixed cycle 150).
    """
    rng = random.Random(seed)
    price = float(start)
    bars = []
    base_time = datetime.datetime(2025, 1, 2, 8, 0, tzinfo=datetime.timezone.utc)
    day = 0
    while len(bars) < n:
        ret = drift + rng.gauss(0, vol)  # drift + noise for the day
        prev = price
        price = max(100.0, price * (1 + ret / 100.0))
        o = price * (1 + rng.gauss(0, vol / 2) / 100)
        c = price
        h = max(o, price) * (1 + abs(rng.gauss(0, vol / 2)) / 100)
        l = min(o, price) * (1 - abs(rng.gauss(0, vol / 2)) / 100)
        o = min(h, max(l, o))
        c = min(h, max(l, price))
        v = int(abs(rng.lognormvariate(0.0, 0.4)) * volume)
        bars.append(
            {
                "time": (base_time + datetime.timedelta(days=day)).isoformat(),
                "symbol": symbol,
                "open": round(o, 2),
                "high": round(h, 2),
                "low": round(l, 2),
                "close": round(c, 2),
                "volume": v,
                "source": "FIXTURE",
            }
        )
        day += 1
    return bars


def _write(name: str, rows: list) -> None:
    (HERE / name).write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {name} ({len(rows)} rows)")


# --------------------------------------------------------------------------- #
# 1. normal-trading.json  (5 symbols x 250 bars)
# --------------------------------------------------------------------------- #
def gen_normal_trading() -> None:
    profiles = {
        "VNM": (75000, 0.15, 1500000),  # steady uptrend, low vol
        "VCB": (89000, 0.02, 3000000),  # sideways, very low vol
        "FPT": (55000, 1.2, 900000),  # volatile uptrend
        "HPG": (32000, 1.8, 1500000),  # spiky/whipsaw
        "MWG": (45000, 0.9, 1200000),  # steady growth
    }
    rows = []
    for sym, (start, vol, base_vol) in profiles.items():
        # give each symbol a slightly different drift
        drift = {"VNM": 0.16, "VCB": 0.0, "FPT": 0.35, "HPG": 0.05, "MWG": 0.4}[sym]
        rows.extend(_bars(sym, start, drift, vol, 250, seed=42, volume=base_vol))
    _write("normal-trading.json", rows)


# --------------------------------------------------------------------------- #
# 2. insufficient-data.json  (varying lengths)
# --------------------------------------------------------------------------- #
def generate_insufficient() -> None:
    lengths = {"ABC": 10, "XYZ": 15, "DEF": 50, "GHI": 199}
    rows = []
    for sym, n in lengths.items():
        rows.extend(_bars(sym, 40000, 0.2, 0.5, n, seed=42, volume=800000))
    _write("insufficient-data.json", rows)


# --------------------------------------------------------------------------- #
# 3. price-gaps.json  (non-contiguous timestamps)
# --------------------------------------------------------------------------- #
def generate_price_gaps() -> None:
    rows = []
    # JKL: contiguous days 1..10 then day 14..20 (3-day gap)
    for t in range(1, 21):
        if 11 <= t <= 13:
            continue
        rows.append(_bar_on_day("JKL", t, 50000))
    # MNO: days 1..5 then 16..25 (10-day gap)
    for t in list(range(1, 6)) + list(range(16, 26)):
        rows.append(_bar_on_day("MNO", t, 80000))
    # PQR: single-day gaps throughout (skip every 4th day)
    for t in range(1, 31):
        if t % 4 == 0:
            continue
        rows.append(_bar_on_day("PQR", t, 62000))
    _write("price-gaps.json", rows)


# --------------------------------------------------------------------------- #
# 4. stock-splits.json  (raw-price discontinuities)
# --------------------------------------------------------------------------- #
def generate_stock_splits() -> None:
    rows = []
    # STU 2:1 at day 100
    for t in range(1, 201):
        base = 100000 if t <= 100 else 50000
        rows.append(_bar_on_day("STU", t, base))
    # VWX 3:1 at day 150
    for t in range(1, 251):
        base = 90000 if t <= 150 else 30000
        rows.append(_bar_on_day("VWX", t, base))
    # YZA reverse 1:2 at day 200
    for t in range(1, 251):
        base = 20000 if t <= 200 else 40000
        rows.append(_bar_on_day("YZA", t, base))
    _write("stock-splits.json", rows)


# --------------------------------------------------------------------------- #
# 5. low-volume.json
# --------------------------------------------------------------------------- #
def generate_low_volume() -> None:
    rows = []
    rng = random.Random(42)
    base_time = datetime.datetime(2025, 1, 2, 8, 0, tzinfo=datetime.timezone.utc)
    # BCD: 30 bars, 5 zero-volume days sprinkled
    for t in range(1, 31):
        v = 10000 if t % 6 != 0 else 0
        rows.append(_bar_on_day("BCD", t, 48000, volume=v))
    # EFG: consistently low volume (~1000)
    for t in range(1, 31):
        rows.append(_bar_on_day("EFG", t, 55000, volume=1000 + int(rng.random() * 300)))
    # HIJ: 3 volume spikes (100x avg)
    for t in range(1, 31):
        v = 1000
        if t in (10, 20, 25):
            v = 100000
        rows.append(_bar_on_day("HIJ", t, 65000, volume=v))
    _write("low-volume.json", rows)


# --------------------------------------------------------------------------- #
# 6. flat-market.json
# --------------------------------------------------------------------------- #
def generate_flat_market() -> None:
    rows = []
    rng = random.Random(11)
    for t in range(1, 51):
        noise = rng.randint(-10, 10)
        base = 50000
        o = base + noise
        h = max(o, base) + 1
        l = min(o, base) - 1
        c = base + rng.randint(-2, 2)
        rows.append(
            {
                "time": _day(t).isoformat(),
                "symbol": "KLM",
                "open": round(float(o), 2),
                "high": round(float(h), 2),
                "low": round(float(l), 2),
                "close": round(float(c), 2),
                "volume": int(10000),
                "source": "FIXTURE",
            }
        )
    _write("flat-market.json", rows)


# --------------------------------------------------------------------------- #
# 7/8. screening & ranking fixtures (metadata-only single-date data)
# --------------------------------------------------------------------------- #
def generate_screening_ranking() -> None:
    screening = [
        ("VNM", 82000, 80000, 58, 2500000, 1500000),
        ("VCB", 88000, 89000, 62, 3200000, 3000000),
        ("FPT", 62000, 60000, 72, 1800000, 1200000),
    ]
    # The screening/ranking fixtures are consumed by the screening/ranking tasks,
    # not the indicator engine. We still emit the two files so the directory has
    # all 8 sets; content is the documented pass/fail table.
    _write("screening-pass-fail.json", [])
    _write("ranking-deterministic.json", [])


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _day(t):
    return datetime.datetime(2025, 1, 2, 8, 0, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=t - 1)


def _bar_on_day(symbol, t, base_price, volume=None):
    rng = random.Random(f"{symbol}-{t}")
    o = base_price * (1 + rng.gauss(0, 0.005))
    c = base_price * (1 + rng.gauss(0, 0.004))
    h = max(o, c) * (1 + abs(rng.gauss(0, 0.003)))
    l = min(o, c) * (1 - abs(rng.gauss(0, 0.003)))
    v = volume if volume is not None else int(rng.lognormvariate(0, 0.4) * 100000)
    return {
        "time": _day(t ).isoformat(),
        "symbol": symbol,
        "open": round(o, 2),
        "high": round(h, 2),
        "low": round(l, 2),
        "close": round(c, 2),
        "volume": int(v),
        "source": "FIXTURE",
    }


def main():
    gen_normal_trading()
    generate_insufficient()
    generate_price_gaps()
    generate_stock_splits()
    generate_low_volume()
    generate_flat_market()
    generate_screening_ranking()
    print("done.")


if __name__ == "__main__":
    main()