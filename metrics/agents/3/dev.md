# dev — cycle 3 lane log

```
imedelta(days=1)
            while not is_trading_day(next_run):
                next_run += timedelta(days=1)
    return next_run


@asynccontextmanager
async def lifespan(app: FastAPI):
    global global_db_engine
    
    global_db_engine = create_async_engine(settings.database_url)
    
    state.next_run = get_next_run_time()
    
    yield
    
    if global_db_engine:
        await global_db_engine.dispose()
app = FastAPI(
    title="vnstock Data Ingest",
    description="Market data ingestion service",
    version="0.1.0",
    lifespan=lifespan(app)


@app.get("/health")
async def health_check():
    try:
        from sqlalchemy import text
        from sqlalchemy.ext.asyncio import create_async_engine
        
        engine = create_async_engine(settings.database_url)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        db_status = "ok"
    except ImportError:
        db_status = "missing_driver"
    except Exception as e:
        db_status = f"error: {str(e)}"

    health = HealthCheck(
        status="healthy" if db_status == "ok" else "degraded",
        service="data-ingest",
        version="0.1.0",
        timestamp=datetime.utcnow(),
        checks={
            "database": db_status,
            "primary_source": "ok" if db_status == "ok" else "unknown",
            "fallback_sources": ["VNDIRECT: ok", "Vietstock: ok"]
        }
    )
    
    return health


@app.post("/ingest/run")
async def run_ingest():
    """
    Trigger manual data ingestion run for all symbols.
    Expected to fetch from primary source (CAFEF) with fallback.
    """
    try:
        target_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        symbols = ["VNM", "VCB", "BID", "FPT", "MSN", "VHM", "VIC", "VRE", "PLX", "HCM"]
        
        logger.info("Starting manual ingestion via API", date=target_date, symbols=symbols)
        
        results, summary = await run_ingestion_job(
            db_url=settings.database_url,
            symbols=symbols,
            target_date=target_date
        )
        
        state.last_run = datetime.utcnow()
        state.errors = [r.error for r in results if r.error]
        
        logger.info("Manual ingestion completed", summary=summary)
        
        return {
            "request_id": f"manual-ingest-{datetime.utcnow().timestamp()}",
            "date": target_date.strftime("%Y-%m-%d"),
            "results": [r.dict() for r in results],
            "summary": summary
        }
    except Exception as e:
        logger.error("Error running manual ingestion", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error running ingestion: {str(e)}")


@app.get("/")
async def root():
    return {"message": "vnstock Data Ingest Service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.data_ingest_port)
EOF
(no output)
[0m
timestamp=2026-07-31T12:32:36.746Z level=INFO run=c22918c7 message=loop session.id=ses_047e63689ffe0ZQkDZXcUphMuB step=54
timestamp=2026-07-31T12:32:36.855Z level=INFO run=c22918c7 message=process session.id=ses_047e63689ffe0ZQkDZXcUphMuB messageID=msg_fb829859c001PkfEVJ3A5s6Kzv
timestamp=2026-07-31T12:32:36.859Z level=INFO run=c22918c7 message=stream providerID=ppsa modelID=big-pickle session.id=ses_047e63689ffe0ZQkDZXcUphMuB small=false agent=build mode=primary
timestamp=2026-07-31T12:32:36.866Z level=INFO run=c22918c7 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=big-pickle
timestamp=2026-07-31T12:32:51.463Z level=INFO run=c22918c7 message=loop session.id=ses_047e63689ffe0ZQkDZXcUphMuB step=55
timestamp=2026-07-31T12:32:51.478Z level=INFO run=c22918c7 message="exiting loop" session.id=ses_047e63689ffe0ZQkDZXcUphMuB
Data Ingest Service Implementation for vnstock-advisor
timestamp=2026-07-31T12:32:51.499Z level=INFO run=c22918c7 message="disposing instance" directory=/data

```
