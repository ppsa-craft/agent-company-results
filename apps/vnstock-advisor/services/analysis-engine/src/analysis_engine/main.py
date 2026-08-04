from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from vnstock_shared.config import get_settings
from vnstock_shared.models import MarketDataCreate
import structlog

from .indicators import IndicatorsResult, compute_all_indicators, OHLCV
from .screening import (
    screen_symbols,
    screen_symbols_to_dict,
    ScreenResult,
    SCREEN_VERSION,
    SCREEN_PRICE_GT_SMA20,
    SCREEN_RSI_MAX,
    SCREEN_VOLUME_RATIO_MIN,
)

settings = get_settings()
logger = structlog.get_logger()

app = FastAPI(
    title="vnstock Analysis Engine",
    description="Technical analysis and signal generation service",
    version="0.1.0",
)


# --------------------------------------------------------------------------- #
# Request/Response Models
# --------------------------------------------------------------------------- #
class IndicatorRequest(BaseModel):
    symbols: List[str] = Field(..., min_length=1, max_length=100)
    start_date: str = Field(..., description="ISO date (YYYY-MM-DD)")
    end_date: str = Field(..., description="ISO date (YYYY-MM-DD)")


class IndicatorResponse(BaseModel):
    symbol: str
    sma20: Optional[float] = None
    sma50: Optional[float] = None
    sma200: Optional[float] = None
    ema12: Optional[float] = None
    ema26: Optional[float] = None
    ema9: Optional[float] = None
    rsi14: Optional[float] = None
    macd: Optional[Dict] = None
    vwap: Optional[float] = None
    volume_sma: Optional[float] = None
    volume_ratio: Optional[float] = None
    roc10: Optional[float] = None
    atr14: Optional[float] = None
    obv: Optional[int] = None
    warnings: List[str] = []


class ScreenRequest(BaseModel):
    symbols: List[str] = Field(..., min_length=1, max_length=500)
    as_of_date: Optional[str] = Field(None, description="ISO date (YYYY-MM-DD), defaults to latest")
    version: str = Field(default=SCREEN_VERSION, pattern="^v1\\.0$")


class CriterionEval(BaseModel):
    pass_: bool = Field(alias="pass")
    price: Optional[float] = None
    sma20: Optional[float] = None
    diff_pct: Optional[float] = None
    rsi: Optional[float] = None
    threshold: Optional[float] = None
    volume: Optional[float] = None
    avg_volume: Optional[float] = None
    ratio: Optional[float] = None


class ScreenEvaluations(BaseModel):
    price_gt_sma20: CriterionEval
    rsi_lt_70: CriterionEval
    volume_gt_1_5x_avg: CriterionEval


class ScreenResponse(BaseModel):
    symbol: str
    passed: bool
    evaluations: Optional[ScreenEvaluations] = None
    excluded: bool = False
    exclusion_reason: Optional[str] = None
    version: str


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: Optional[str] = None


# --------------------------------------------------------------------------- #
# Health & Root
# --------------------------------------------------------------------------- #
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "analysis-engine",
        "version": "0.1.0",
    }


@app.get("/")
async def root():
    return {"message": "vnstock Analysis Engine Service"}


# --------------------------------------------------------------------------- #
# Indicators Endpoint (5a)
# --------------------------------------------------------------------------- #
@app.post("/indicators/compute", response_model=Dict[str, IndicatorResponse])
async def compute_indicators(request: IndicatorRequest):
    """Compute all indicators for given symbols and date range.
    
    Returns the latest indicator values per symbol.
    """
    # TODO: In real implementation, fetch OHLCV from data-ingest service
    # For now, return error indicating data source not wired
    raise HTTPException(
        status_code=501,
        detail="Data source not yet wired. Indicators computation requires market data from data-ingest service.",
    )


# --------------------------------------------------------------------------- #
# Screening Endpoint (5b)
# --------------------------------------------------------------------------- #
@app.post("/screen", response_model=Dict[str, ScreenResponse])
async def screen(request: ScreenRequest):
    """Screen symbols against v1.0 criteria.
    
    Criteria (AND logic):
    1. Price > SMA20
    2. RSI14 < 70
    3. Volume > 1.5 * Volume_SMA20
    
    Returns per-symbol pass/fail with detailed evaluations.
    """
    logger.info("Screen request", symbols=request.symbols, version=request.version)
    
    # TODO: In real implementation, fetch indicators from indicators service/computation
    # For now, return error indicating data source not wired
    raise HTTPException(
        status_code=501,
        detail="Indicator data source not yet wired. Screening requires indicator computation from indicators service.",
    )


# --------------------------------------------------------------------------- #
# Legacy /analyze (placeholder)
# --------------------------------------------------------------------------- #
@app.post("/analyze")
async def analyze_data(data: MarketDataCreate):
    logger.info("Analysis request received", symbol=data.symbol, time=data.time)
    return {
        "symbol": data.symbol,
        "time": data.time.isoformat(),
        "analysis": {
            "ma_20": 100.0,
            "ma_50": 95.0,
            "rsi": 50.0,
            "volume": 1000000,
            "signal": "neutral",
        },
        "note": "This is a placeholder response. Technical analysis implementation is pending M2 work.",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.analysis_engine_port)