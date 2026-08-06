from fastapi import FastAPI
from vnstock_shared.config import get_settings
from vnstock_shared.models import MarketDataCreate
import structlog
from indicators import compute_all_indicators, OHLCV

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.analysis_engine_port)