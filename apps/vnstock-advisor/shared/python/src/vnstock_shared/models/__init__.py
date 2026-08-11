from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Numeric,
    BigInteger,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    pass


class MarketData(Base):
    __tablename__ = "market_data"
    __table_args__ = (
        Index("idx_market_data_symbol_time", "symbol", "time"),
        Index("idx_market_data_source", "source"),
        {"timescaledb_hypertable": {"time_column": "time"}},
    )

    time = Column(
        TIMESTAMP(timezone=True),
        primary_key=True,
        nullable=False,
        comment="Timestamp of the market data point",
    )
    symbol = Column(String(20), primary_key=True, nullable=False, comment="Stock symbol")
    open = Column(Numeric(12, 4), nullable=False, comment="Opening price")
    high = Column(Numeric(12, 4), nullable=False, comment="Highest price")
    low = Column(Numeric(12, 4), nullable=False, comment="Lowest price")
    close = Column(Numeric(12, 4), nullable=False, comment="Closing price")
    volume = Column(BigInteger, nullable=False, comment="Trading volume")
    source = Column(String(50), nullable=False, comment="Data source identifier")


class MarketDataCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time: datetime = Field(..., description="Timestamp of the market data point")
    symbol: str = Field(..., min_length=1, max_length=20, description="Stock symbol")
    open: Decimal = Field(..., gt=0, description="Opening price")
    high: Decimal = Field(..., gt=0, description="Highest price")
    low: Decimal = Field(..., gt=0, description="Lowest price")
    close: Decimal = Field(..., gt=0, description="Closing price")
    volume: int = Field(..., ge=0, description="Trading volume")
    source: str = Field(..., min_length=1, max_length=50, description="Data source identifier")
    timeframe: str = Field(..., pattern="^(1D|1W|1M|3M)$", description="Timeframe for the data")


class MarketDataRead(MarketDataCreate):
    pass


class MarketDataBatch(BaseModel):
    items: list[MarketDataCreate] = Field(..., min_length=1, max_length=10000)


class SuggestionBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    action: str = Field(..., pattern="^(BUY|SELL|HOLD)$")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str = Field(..., min_length=1, max_length=500)
    target_price: Optional[Decimal] = Field(None, gt=0, description="Target price")
    stop_loss: Optional[Decimal] = Field(None, gt=0, description="Stop loss price")
    timeframe: str = Field(..., pattern="^(1D|1W|1M|3M)$")


class SuggestionCreate(SuggestionBase):
    pass


class SuggestionRead(SuggestionBase):
    id: str = Field(..., description="UUID")
    created_at: datetime


class AnalysisResultBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    indicators: dict[str, float] = Field(default_factory=dict)
    signals: list[str] = Field(default_factory=list)
    trend: str = Field(..., pattern="^(BULLISH|BEARISH|SIDEWAYS)$")
    strength: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultRead(AnalysisResultBase):
    pass


class HealthCheck(BaseModel):
    status: str = Field(..., pattern="^(healthy|degraded|unhealthy)$")
    service: str
    version: str
    timestamp: datetime
    checks: Optional[list[dict]] = None