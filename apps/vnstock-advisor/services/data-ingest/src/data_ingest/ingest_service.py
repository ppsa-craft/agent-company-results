from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from vnstock_shared.config import get_settings
from vnstock_shared.models import MarketDataCreate
from .models import OHLCV, IngestResult
import structlog
from .disclaimer import build_meta_disclaimer

logger = structlog.get_logger()


settings = get_settings()


class DatabaseUnavailableError(Exception):
    """Raised when PostgreSQL cannot be reached at connection time.

    Surfaced to the API layer as a clean RFC-7807 problem+json 503 response so a
    DB-unreachable failure never leaks a raw driver exception / stack trace to the
    client (TESTER defect 4: uncaught asyncpg ConnectionRefusedError at engine.begin()).
    """


def calculate_technical_indicators(datas: List[Dict]) -> Dict:
    return {}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_from_cafef(session: httpx.AsyncClient, date: datetime, symbol: str) -> Optional[OHLCV]:
    """Fetch data from CAFEF primary source with retry logic."""
    try:
        url = "https://www.cafef.vn/giaodich.jsp"
        params = {
            "symbol": symbol,
            "date": date.strftime("%Y-%m-%d"),
            "type": "1"
        }
        response = await session.get(url, params=params, timeout=30.0)
        
        if response.status_code == 200:
            raw_data = response.json()
            # Validate CAFEF response format - expect at least some known keys
            if not raw_data or not isinstance(raw_data, dict):
                logger.warning("CAFEF returned invalid data format", symbol=symbol)
                return None
            # Check for expected CAFEF response structure
            expected_keys = {"t", "o", "h", "l", "c", "v", "s"}
            if not any(k in raw_data for k in expected_keys) and not any(k.upper() in raw_data for k in expected_keys):
                logger.warning("CAFEF returned unexpected data format", symbol=symbol, keys=list(raw_data.keys())[:10])
                return None
            return OHLCV.from_cafef(raw_data, symbol)
        else:
            logger.warning("CAFEF fetch failed", status_code=response.status_code, symbol=symbol)
            return None
    except Exception as e:
        logger.error("Error fetching from CAFEF", error=str(e), symbol=symbol)
        return None


async def fetch_from_vndirect(session: httpx.AsyncClient, date: datetime, symbol: str) -> Optional[OHLCV]:
    """Fetch data from VNDIRECT fallback source."""
    try:
        url = "https://services.vndirect.com.vn/price-history"
        params = {
            "symbol": symbol,
            "date": date.strftime("%Y-%m-%d"),
            "resolution": "day"
        }
        response = await session.get(url, params=params, timeout=30.0)
        
        if response.status_code == 200:
            raw_data = response.json()
            return OHLCV.from_vndirect(raw_data)
        else:
            logger.warning("VNDIRECT fetch failed", status_code=response.status_code, symbol=symbol)
            return None
    except Exception as e:
        logger.error("Error fetching from VNDIRECT", error=str(e), symbol=symbol)
        return None


async def ingest_data_for_date(
    session: httpx.AsyncClient, 
    db_session: AsyncSession, 
    date: datetime,
    symbol: str
) -> IngestResult:
    """Ingest data for a single symbol and date with fallback logic."""
    logger.info("Starting ingestion", date=date.strftime("%Y-%m-%d"), symbol=symbol)
    
    result = IngestResult(symbol=symbol, status="failed", source="", rows_upserted=0)
    
    try:
        cafef_data = await fetch_from_cafef(session, date, symbol)
        if cafef_data:
            result.source = "CAFEF"
            db_record = cafef_data.normalize("1D")
        else:
            logger.info("Primary source CAFEF failed, trying VNDIRECT", symbol=symbol)
            vndirect_data = await fetch_from_vndirect(session, date, symbol)
            if vndirect_data:
                result.source = "VNDIRECT"
                db_record = vndirect_data.normalize("1D")
            else:
                result.status = "failed"
                result.error = "Both primary and fallback sources failed"
                logger.error("All sources failed", symbol=symbol, date=date)
                return result
        
        try:
            db_session.add(db_record)
            await db_session.commit()
            result.status = "success"
            result.rows_upserted = 1
            logger.info("Successfully ingested data", symbol=symbol, source=result.source)
            return result
        except SQLAlchemyError as e:
            await db_session.rollback()
            error_msg = str(e)
            if "unique violation" in error_msg.lower():
                result.status = "success"
                result.duplicate_skipped = True
                result.error = "Duplicate entry skipped"
                logger.info("Duplicate entry skipped", symbol=symbol, date=date)
            else:
                result.status = "error"
                result.error = f"Database error: {error_msg}"
                logger.error("Database error during upsert", symbol=symbol, error=error_msg)
            return result
            
    except Exception as e:
        result.status = "error"
        result.error = str(e)
        logger.error("Unexpected error during ingestion", symbol=symbol, error=str(e))
        return result


def is_trading_day(date: datetime) -> bool:
    """Check if a date is a trading day in Vietnam."""
    if date.weekday() >= 5:
        return False
    
    from datetime import date as d
    year, month, day = date.year, date.month, date.day
    vietnam_holidays = [
        d(2024, 1, 1),
        d(2024, 2, 12),
        d(2024, 4, 18),
        d(2024, 4, 30),
        d(2024, 5, 1),
        d(2024, 9, 2),
        d(2024, 9, 20),
        d(2024, 10, 10),
        d(2024, 12, 25),
        d(2024, 12, 31),
    ]
    return d(year, month, day) not in vietnam_holidays


async def run_ingestion_job(
    db_url: str,
    symbols: List[str],
    target_date: Optional[datetime] = None
) -> Tuple[List[IngestResult], Dict[str, Any]]:
    """Main ingestion job that processes data for given symbols and date."""
    logger.info("Starting ingestion job", symbols=symbols, target_date=target_date)
    
    results: List[IngestResult] = []
    summary: Dict[str, Any] = {
        "total": len(symbols),
        "success": 0,
        "failed": 0,
        "duplicates_skipped": 0
    }
    
    if target_date is None:
        target_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not is_trading_day(target_date):
        logger.warning("Skipping non-trading day", date=target_date.strftime("%Y-%m-%d"))
        return results, summary

    async with httpx.AsyncClient() as http_client:
        try:
            engine = create_async_engine(db_url)
            async with engine.begin() as conn:
                async_session = sessionmaker(
                    bind=conn,
                    class_=AsyncSession,
                    expire_on_commit=False
                )()
                
                for symbol in symbols:
                    result = await ingest_data_for_date(http_client, async_session, target_date, symbol)
                    results.append(result)
                    
                    if result.status == "success":
                        if result.duplicate_skipped:
                            summary["duplicates_skipped"] += 1
                        else:
                            summary["success"] += 1
                    else:
                        summary["failed"] += 1
        except DatabaseUnavailableError:
            # Already sanitized — re-raise so the API layer returns the RFC-7807 503.
            raise
        except Exception as e:
            # DB unreachable at connection time (engine creation / begin / connect):
            # asyncpg raises OSError subclasses (e.g. ConnectionRefusedError), and
            # SQLAlchemy raises SQLAlchemyError subclasses for bad URLs/dialects.
            # Do NOT leak the raw driver exception to the client — log it server-side
            # and raise a sanitized domain error. The per-symbol try/except inside
            # ingest_data_for_date is unaffected (it catches its own DB errors).
            logger.error("Database unreachable during ingestion job", error=str(e))
            raise DatabaseUnavailableError("Database unavailable; ingestion could not run. Check DATABASE_URL and PostgreSQL availability.") from e
    
    logger.info("Ingestion job completed", summary=summary)
    # Add disclaimer to summary for API responses
    summary["meta"] = {
        "generated_at": datetime.now(timezone.utc).isoformat() + "Z",
        "source": "data-ingest-v0.1.0",
        "disclaimer": build_meta_disclaimer("full")
    }
    return results, summary