# vnstock Analysis Engine

Technical analysis engine for vnstock-advisor. Computes indicators, screens symbols, and ranks opportunities.

## Quick Start

```bash
# Install dependencies (from workspace root)
cd /data/worktrees/dev/apps/vnstock-advisor
pip install -e services/analysis-engine

# Run tests
pytest services/analysis-engine/tests/ -v

# Run service
cd services/analysis-engine
python -m analysis_engine.main
```

## API Endpoints

### Health Check
```
GET /health
```

### Indicators Computation (5a)
```
POST /indicators/compute
{
  "symbols": ["VNM", "VIC"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

### Screening (5b)
```
POST /screen
{
  "symbols": ["VNM", "VIC", "FPT"],
  "as_of_date": "2024-12-31",
  "version": "v1.0"
}
```

#### Screening Criteria v1.0 (AND logic)
1. **Price > SMA20** - Price above 20-day simple moving average
2. **RSI14 < 70** - Not overbought
3. **Volume > 1.5 × Volume_SMA20** - Above-average volume

#### Response Format
```json
{
  "VNM": {
    "symbol": "VNM",
    "passed": true,
    "evaluations": {
      "price_gt_sma20": {"pass": true, "price": 78500.0, "sma20": 77200.0, "diff_pct": 1.68},
      "rsi_lt_70": {"pass": true, "rsi": 58.3, "threshold": 70},
      "volume_gt_1_5x_avg": {"pass": true, "volume": 2500000, "avg_volume": 1400000, "ratio": 1.79}
    },
    "version": "v1.0"
  },
  "ABC": {
    "symbol": "ABC",
    "passed": false,
    "excluded": true,
    "exclusion_reason": "insufficient_data",
    "version": "v1.0"
  }
}
```

### Legacy Analyze (placeholder)
```
POST /analyze
{
  "symbol": "VNM",
  "time": "2024-01-01T00:00:00Z",
  "open": 100.0,
  "high": 105.0,
  "low": 99.0,
  "close": 102.0,
  "volume": 1000000,
  "source": "manual"
}
```

## Configuration

Environment variables (v1.0 defaults are immutable):

| Variable | Default | Description |
|----------|---------|-------------|
| `SCREEN_PRICE_GT_SMA20` | `true` | Enable price > SMA20 criterion |
| `SCREEN_RSI_MAX` | `70` | RSI upper bound |
| `SCREEN_VOLUME_RATIO_MIN` | `1.5` | Minimum volume ratio |

> **Warning:** Overriding these creates a de facto new version. Audited runs must record effective thresholds.

## Determinism

- Same input + same version = bit-identical output
- No randomness in screening pipeline
- Percentile calculation uses stable algorithm (linear interpolation)

## Testing

```bash
# Run all tests
pytest services/analysis-engine/tests/ -v

# Run specific test file
pytest services/analysis-engine/tests/test_screening.py -v
pytest services/analysis-engine/tests/test_main.py -v
```

## Project Structure

```
services/analysis-engine/
├── pyproject.toml
├── src/
│   └── analysis_engine/
│       ├── __init__.py
│       ├── indicators.py      # 5a: Indicator computations
│       ├── screening.py       # 5b: Screening logic
│       └── main.py            # FastAPI app with endpoints
└── tests/
    ├── test_main.py
    ├── test_screening.py
    └── fixtures/
        ├── normal-trading.json
        ├── insufficient-data.json
        ├── screening-pass-fail.json
        └── ...
```

## Dependencies

- `vnstock-shared-python` - Shared models and config
- `fastapi` / `uvicorn` - Web framework
- `pandas` / `numpy` - Data processing
- `ta-lib` - Technical analysis (optional, not used in pure-Python impl)