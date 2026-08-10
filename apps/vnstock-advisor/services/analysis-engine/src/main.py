from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from vnstock_shared.config import get_settings
from vnstock_shared.models import MarketDataCreate
import structlog
from indicators import compute_all_indicators, OHLCV
from ranking import rank_symbols

# Analysis Engine - placeholder for technical analysis implementation
# TODO: M2 milestone - implement MA/RSI/volume indicators, screening, ranking logic

settings = get_settings()
logger = structlog.get_logger()

app = FastAPI(
    title="vnstock Analysis Engine",
    description="Technical analysis and signal generation service - PLANNING",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    # Service is initialized but functional implementation needed (M2 work)
    return {
        "status": "healthy",
        "service": "analysis-engine",
        "version": "0.1.0",
        "note": "Functional analysis implementation pending",
    }


@app.get("/")
async def root():
    return {"message": "vnstock Analysis Engine Service - PLANNING"}


# Service contract for data-ingest to interact with
@app.post("/analyze")
async def analyze_data(data: MarketDataCreate):
    # Convert MarketDataCreate to OHLCV for indicator computation
    ohlcv = OHLCV(
        time=data.time,
        open=float(data.open),
        high=float(data.high),
        low=float(data.low),
        close=float(data.close),
        volume=data.volume,
    )
    
    # Compute all indicators using the real implementation
    result = compute_all_indicators([ohlcv])
    
    logger.info("Analysis request received", symbol=data.symbol, timeframe=data.timeframe)
    return {
        "symbol": data.symbol,
        "timeframe": data.timeframe,
        "indicators": {
            "sma20": result.sma20[-1] if result.sma20 else None,
            "sma50": result.sma50[-1] if result.sma50 else None,
            "sma200": result.sma200[-1] if result.sma200 else None,
            "ema12": result.ema12[-1] if result.ema12 else None,
            "ema26": result.ema26[-1] if result.ema26 else None,
            "ema9": result.ema9[-1] if result.ema9 else None,
            "rsi14": result.rsi14[-1] if result.rsi14 else None,
            "macd": result.macd[-1] if result.macd else None,
            "vwap": result.vwap[-1] if result.vwap else None,
            "volume_sma": result.volume_sma[-1] if result.volume_sma else None,
            "volume_ratio": result.volume_ratio[-1] if result.volume_ratio else None,
            "roc10": result.roc10[-1] if result.roc10 else None,
            "atr14": result.atr14[-1] if result.atr14 else None,
            "obv": result.obv[-1] if result.obv else None,
        },
        "warnings": result.warnings,
    }


class RankRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of symbols to rank")
    date: str = Field(..., description="Analysis date in ISO format")
    version: str = Field("1.0", description="Ranking version for deterministic results")


class RankResponse(BaseModel):
    ranked_symbols: List[Dict[str, Any]]
    version: str
    total_analyzed: int


@app.post("/rank")
async def rank_symbols_endpoint(request: RankRequest):
    """Rank symbols based on composite scores from indicators.

    Computes weighted composite scores (momentum 40% / trend 30% / volume 20% /
    volatility 10%) for each symbol from the indicator results and returns a
    ranked list with per-symbol reasoning.
    """
    if not request.symbols:
        raise HTTPException(status_code=400, detail="symbols must not be empty")

    try:
        logger.info("Rank symbols request received",
                    symbols=request.symbols,
                    date=request.date,
                    version=request.version)

        # Prepare indicators data from previous analysis
        # In a real implementation, this would fetch from database or previous analysis
        indicators_by_symbol: Dict[str, Dict[str, Any]] = {}

        for symbol in request.symbols:
            # For now, create sample indicators data
            # In production, this would be fetched from the database
            indicators_by_symbol[symbol] = {
                "roc10": 5.2 if symbol == "VNM" else 3.8,
                "rsi": 65.2 if symbol == "VNM" else 58.5,
                "trend_conditions": [True, True, True, True, False, False, False],
                "total_trend_conditions": 7,
                "volume_ratio": 2.5 if symbol == "VNM" else 1.8,
                "obv_trend": 0.3 if symbol == "VNM" else 0.2,
                "atr_percentile": 30.0 if symbol == "VNM" else 45.0,
                "atr": 1.5 if symbol == "VNM" else 2.0,
                "valid_bars": 250,
            }

        # Define weights according to specification
        weights = {
            "momentum": 0.4,
            "trend": 0.3,
            "volume": 0.2,
            "volatility": 0.1,
        }

        # Perform ranking
        ranked_results = rank_symbols(
            indicators_by_symbol=indicators_by_symbol,
            screened_symbols=request.symbols,
            weights=weights,
            version=request.version,
        )

        return RankResponse(
            ranked_symbols=ranked_results,
            version=request.version,
            total_analyzed=len(request.symbols),
        )

    except Exception as e:
        logger.error("Error in rank symbols endpoint", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.analysis_engine_port)