from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from decimal import Decimal

from pydantic import BaseModel, Field


class OHLCV(BaseModel):
    time: datetime
    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    source: str = Field(default="CAFEF")
    raw_data: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_cafef(cls, cafef_data: Dict[str, Any]) -> "OHLCV":
        return cls(
            time=cls._parse_cafef_time(cafef_data.get("time", "")),
            symbol=cafef_data.get("symbol", ""),
            open=Decimal(str(cafef_data.get("open", 0))),
            high=Decimal(str(cafef_data.get("high", 0))),
            low=Decimal(str(cafef_data.get("low", 0))),
            close=Decimal(str(cafef_data.get("close", 0))),
            volume=int(cafef_data.get("volume", 0)),
            source="CAFEF",
            raw_data=cafef_data
        )

    @classmethod
    def from_vndirect(cls, vndirect_data: Dict[str, Any]) -> "OHLCV":
        return cls(
            time=cls._parse_vndirect_time(vndirect_data.get("time", "")),
            symbol=vndirect_data.get("symbol", ""),
            open=Decimal(str(vndirect_data.get("open", 0))),
            high=Decimal(str(vndirect_data.get("high", 0))),
            low=Decimal(str(vndirect_data.get("low", 0))),
            close=Decimal(str(vndirect_data.get("close", 0))),
            volume=int(vndirect_data.get("volume", 0)),
            source="VNDIRECT",
            raw_data=vndirect_data
        )

    @classmethod
    def _parse_cafef_time(cls, time_str: str) -> datetime:
        try:
            from dateutil.parser import parse
            return parse(time_str).replace(tzinfo=timezone.utc)
        except Exception:
            from datetime import datetime
            return datetime(2024, 1, 1, tzinfo=timezone.utc)

    @classmethod
    def _parse_vndirect_time(cls, time_str: str) -> datetime:
        try:
            from dateutil.parser import parse
            return parse(time_str).replace(tzinfo=timezone.utc)
        except Exception:
            from datetime import datetime
            return datetime(2024, 1, 1, tzinfo=timezone.utc)

    def normalize(self) -> "MarketDataCreate":
        from vnstock_shared.models import MarketDataCreate
        return MarketDataCreate(
            time=self.time,
            symbol=self.symbol,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            volume=self.volume,
            source=self.source
        )


class IngestResult(BaseModel):
    symbol: str
    status: str
    source: str
    rows_upserted: int
    error: Optional[str] = None
    duplicate_skipped: bool = False
