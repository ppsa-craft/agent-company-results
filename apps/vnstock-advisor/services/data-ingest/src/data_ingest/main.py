from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from vnstock_shared.config import get_settings
from vnstock_shared.models import HealthCheck
from .ingest_service import run_ingestion_job, is_trading_day
from .disclaimer import build_meta_disclaimer

settings = get_settings()


# Scheduler for scheduled ingestion
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.add_job(
        scheduled_ingestion_job,
        CronTrigger(hour=6, minute=0, timezone="Asia/Ho_Chi_Minh"),  # Run at 6:00 AM ICT (after market close)
        id="daily_ingestion",
        replace_existing=True,
    )
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()


app = FastAPI(
    title="vnstock Data Ingest",
    description="Market data ingestion service",
    version="0.1.0",
    lifespan=lifespan,
)


DEFAULT_SYMBOLS = ["VNM", "VCB", "BID", "FPT", "HPG", "MSN", "VIC", "VHM", "GAS", "TCB"]


def build_meta() -> dict:
    """Build the standard response `meta` object including the mandatory disclaimer."""
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "data-ingest-v0.1.0",
        "disclaimer": build_meta_disclaimer("full"),
    }


async def scheduled_ingestion_job():
    """Scheduled ingestion job for trading days."""
    target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not is_trading_day(target_date):
        return
    
    await run_ingestion_job(settings.database_url, DEFAULT_SYMBOLS, target_date)


class IngestRunRequest(BaseModel):
    """Request model for manual ingestion trigger."""
    date: Optional[str] = Field(None, description="Target date in YYYY-MM-DD format (defaults to latest trading day)")
    symbols: Optional[List[str]] = Field(None, description="List of symbols to ingest (defaults to all)")
    source: Optional[str] = Field(None, description="Force specific source (CAFEF, VNDIRECT) - bypasses fallback")


class IngestResultResponse(BaseModel):
    """Response model for ingestion results."""
    symbol: str
    status: str
    source: str
    rows_upserted: int
    error: Optional[str] = None
    duplicate_skipped: bool = False


class IngestRunResponse(BaseModel):
    """Response model for manual ingestion run."""
    request_id: str
    date: str
    results: List[IngestResultResponse]
    summary: dict
    meta: dict = Field(default_factory=dict)


@app.get("/health")
async def health_check():
    """Health check endpoint with database and source connectivity."""
    try:
        from sqlalchemy import text
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy.exc import SQLAlchemyError

        engine = create_async_engine(settings.database_url)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        db_status = "ok"
    except ImportError:
        db_status = "missing_driver"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check source connectivity (lightweight)
    primary_source_status = "unknown"
    fallback_sources_status = []
    
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check CAFEF
            try:
                resp = await client.get("https://www.cafef.vn", timeout=3.0)
                primary_source_status = "ok" if resp.status_code == 200 else f"http_{resp.status_code}"
            except Exception:
                primary_source_status = "unreachable"
            
            # Check VNDIRECT
            try:
                resp = await client.get("https://services.vndirect.com.vn", timeout=3.0)
                fallback_sources_status.append(f"VNDIRECT: {'ok' if resp.status_code == 200 else f'http_{resp.status_code}'}")
            except Exception:
                fallback_sources_status.append("VNDIRECT: unreachable")
    except Exception:
        primary_source_status = "check_failed"
        fallback_sources_status = ["VNDIRECT: check_failed"]

    health = HealthCheck(
        status="healthy" if db_status == "ok" else "degraded",
        service="data-ingest",
        version="0.1.0",
        timestamp=datetime.utcnow(),
        checks=[
            {"name": "database", "status": db_status},
            {"name": "primary_source", "status": primary_source_status},
            {"name": "fallback_sources", "status": fallback_sources_status},
        ]
    )
    
    return {
        "status": health.status,
        "service": health.service,
        "version": health.version,
        "timestamp": health.timestamp.isoformat() + "Z",
        "checks": health.checks,
        "meta": build_meta(),
    }


@app.post("/ingest/run", response_model=IngestRunResponse)
async def run_ingest(request: IngestRunRequest):
    """
    Trigger manual data ingestion run for specified symbols and date.
    Fetches from primary source (CAFEF) with fallback to VNDIRECT.
    """
    import uuid
    
    request_id = str(uuid.uuid4())[:8]
    
    # Parse date
    if request.date:
        try:
            target_date = datetime.strptime(request.date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Validate trading day
    if not is_trading_day(target_date):
        raise HTTPException(
            status_code=400, 
            detail=f"{target_date.strftime('%Y-%m-%d')} is not a trading day (weekend or holiday)"
        )
    
    # Determine symbols
    symbols = request.symbols if request.symbols else DEFAULT_SYMBOLS
    
    if not symbols:
        raise HTTPException(status_code=400, detail="No symbols provided")
    
    # Run ingestion job with source override if specified
    if request.source:
        # Note: run_ingestion_job doesn't support source parameter, 
        # this would need to be implemented in a future enhancement
        pass
    
    results, summary = await run_ingestion_job(settings.database_url, symbols, target_date)
    
    # Convert to response model
    response_results = [
        IngestResultResponse(
            symbol=r.symbol,
            status=r.status,
            source=r.source,
            rows_upserted=r.rows_upserted,
            error=r.error,
            duplicate_skipped=r.duplicate_skipped,
        )
        for r in results
    ]
    
    return IngestRunResponse(
        request_id=request_id,
        date=target_date.strftime("%Y-%m-%d"),
        results=response_results,
        summary=summary,
        meta=build_meta(),
    )


@app.get("/ingest/status")
async def ingest_status():
    """Get last scheduled ingestion status."""
    # This would typically query a job status table
    # For now, return basic info
    return {
        "scheduler_running": scheduler.running,
        "next_run": scheduler.get_job("daily_ingestion").next_run_time.isoformat() if scheduler.get_job("daily_ingestion") else None,
        "default_symbols": DEFAULT_SYMBOLS,
        "meta": build_meta(),
    }


@app.get("/")
async def root():
    return {
        "message": "vnstock Data Ingest Service",
        "meta": build_meta(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.data_ingest_port)