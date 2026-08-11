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
    def from_cafef(cls, cafef_data: Dict[str, Any], symbol: str) -> "OHLCV":
        def _get_value(key):
            value = cafef_data.get(key, cafef_data.get(key.upper(), 0))
            if isinstance(value, list) and len(value) > 0:
                return value[0]
            return value
        
        return cls(
            time=cls._parse_cafef_time(_get_value("t")),
            symbol=symbol,
            open=Decimal(str(_get_value("o"))),
            high=Decimal(str(_get_value("h"))),
            low=Decimal(str(_get_value("l"))),
            close=Decimal(str(_get_value("c"))),
            volume=int(_get_value("v")),
            source="CAFEF",
            raw_data=cafef_data
        )

    @classmethod
    def from_vndirect(cls, vndirect_data: Dict[str, Any], symbol: str = "") -> "OHLCV":
        # VNDIRECT returns arrays of data, extract the first element
        time_val = vndirect_data.get("t", [])
        if isinstance(time_val, list) and len(time_val) > 0:
            time_str = time_val[0]
        else:
            time_str = time_val
            
        open_val = vndirect_data.get("o", [])
        if isinstance(open_val, list) and len(open_val) > 0:
            open_val = open_val[0]
            
        high_val = vndirect_data.get("h", [])
        if isinstance(high_val, list) and len(high_val) > 0:
            high_val = high_val[0]
            
        low_val = vndirect_data.get("l", [])
        if isinstance(low_val, list) and len(low_val) > 0:
            low_val = low_val[0]
            
        close_val = vndirect_data.get("c", [])
        if isinstance(close_val, list) and len(close_val) > 0:
            close_val = close_val[0]
            
        volume_val = vndirect_data.get("v", [])
        if isinstance(volume_val, list) and len(volume_val) > 0:
            volume_val = volume_val[0]
        
        return cls(
            time=cls._parse_vndirect_time(time_str),
            symbol=symbol or vndirect_data.get("symbol", ""),
            open=Decimal(str(open_val)),
            high=Decimal(str(high_val)),
            low=Decimal(str(low_val)),
            close=Decimal(str(close_val)),
            volume=int(volume_val),
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

    def normalize(self, timeframe: str = "1D") -> "MarketDataCreate":
        from vnstock_shared.models import MarketDataCreate
        return MarketDataCreate(
            time=self.time,
            symbol=self.symbol,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            volume=self.volume,
            source=self.source,
            timeframe=timeframe
        )


class IngestResult(BaseModel):
    symbol: str
    status: str
    source: str
    rows_upserted: int
    error: Optional[str] = None
    duplicate_skipped: bool = False
