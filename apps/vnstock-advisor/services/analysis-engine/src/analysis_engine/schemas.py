"""Frozen-contract Pydantic schemas for the vnstock-advisor analysis-engine.

Implements the exact request/response shapes from
``docs/specs/analysis-engine-api.md`` v1.0 (frozen, PM sign-off cycle 42):

  * ``POST /indicators/compute``  -> ``IndicatorComputeRequest/Response``
  * ``POST /analyze``             -> ``AnalyzeRequest/Response``
  * ``POST /rank``                -> ``RankRequest/RankResponse``

Contract rules honoured here:
  * algorithm version pinned via ``algorithm_version`` (``^v\\d+\\.\\d+$``), only
    ``v1.0`` is supported (anything else is ``400 UNSUPPORTED_VERSION``).
  * ``/rank`` splits ``ranked[]`` / ``excluded[]`` (no interleaving), carries
    ``weights_used``, and validates every input with explicit Pydantic guards.
  * Errors use RFC 7807 Problem Details (raised as ``HTTPException`` in the
    endpoint layer; the helper here builds the body).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# --------------------------------------------------------------------------- #
# Shared pieces
# --------------------------------------------------------------------------- #

SUPPORTED_ALGORITHM_VERSIONS = ("v1.0",)

SYMBOL_PATTERN = r"^[A-Z][A-Z0-9]{0,9}$"  # VN tickers: uppercase letters, optional digits
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def problem_detail(
    status: int,
    code: str,
    title: str,
    detail: str,
    instance: str,
    errors: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """RFC 7807 Problem Details body (``application/problem+json``)."""
    body: Dict[str, Any] = {
        "type": f"https://vnstock-advisor.com/errors/{code}",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance,
    }
    if errors:
        body["errors"] = errors
    return body


# --------------------------------------------------------------------------- #
# OHLCV bar (contract §1.1)
# --------------------------------------------------------------------------- #
class OHLCVBar(BaseModel):
    """A single OHLCV bar as defined by the frozen /indicators/compute contract."""

    time: str = Field(..., description="ISO 8601 UTC timestamp of the bar")
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: int = Field(..., ge=0)
    source: str = Field(..., min_length=1, max_length=50, description="Data source identifier")


# --------------------------------------------------------------------------- #
# POST /indicators/compute
# --------------------------------------------------------------------------- #
class IndicatorComputeRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, pattern=SYMBOL_PATTERN)
    ohlcv: List[OHLCVBar] = Field(..., min_length=1, max_length=10000)
    algorithm_version: str = Field(..., pattern=r"^v\d+\.\d+$")
    volume_sma_period: int = Field(20, ge=2, le=200)


class IndicatorComputeResponse(BaseModel):
    symbol: str
    algorithm_version: str
    computed_at: str
    bars_processed: int
    indicators: Dict[str, Any]
    warnings: List[str]
    last: Dict[str, Any]


# --------------------------------------------------------------------------- #
# POST /analyze (data-ingest consumer contract, §2)
# --------------------------------------------------------------------------- #
class AnalyzeRequest(BaseModel):
    """Higher-level analysis endpoint.

    Accepts a single ``MarketDataCreate``-shaped payload (data-ingest consumer
    contract) OR an explicit ascending ``bars`` series so real indicator values
    can be produced (C2 fix — a lone bar yields all-None indicators).

    ``timeframe`` is fixed to ``1D`` in v1.0 (contract §2, defer resampling to
    v1.1).
    """

    time: str = Field(..., description="ISO 8601 UTC timestamp (of the single-bar form)")
    symbol: str = Field(..., min_length=1, max_length=20, pattern=SYMBOL_PATTERN)
    open: Optional[float] = Field(None, gt=0)
    high: Optional[float] = Field(None, gt=0)
    low: Optional[float] = Field(None, gt=0)
    close: Optional[float] = Field(None, gt=0)
    volume: Optional[int] = Field(None, ge=0)
    source: Optional[str] = Field(None, min_length=1, max_length=50)
    timeframe: str = Field("1D", pattern="^(1D|1W|1M|3M)$")
    bars: Optional[List[OHLCVBar]] = Field(
        None,
        max_length=10000,
        description="Explicit ascending OHLCV series (preferred — produces real indicators)",
    )

    @field_validator("bars")
    @classmethod
    def _bars_nonempty(cls, v: Optional[List[OHLCVBar]]) -> Optional[List[OHLCVBar]]:
        if v is not None and len(v) < 1:
            raise ValueError("bars must have at least 1 item")
        return v


class AnalyzeResponse(BaseModel):
    symbol: str
    timeframe: str
    analysis: Dict[str, Any]
    timestamp: str


# --------------------------------------------------------------------------- #
# POST /rank (frozen UC-AE-3 contract, §4)
# --------------------------------------------------------------------------- #
class RankRequest(BaseModel):
    """Ranking request with explicit input guards (C6).

    ``series`` maps each requested symbol to its ascending OHLCV bars; the
    endpoint computes real indicators from it (C2 fix — no fabricated literals).
    Symbols present in ``symbols`` but missing from ``series`` are unresolvable
    and produce a ``400 INVALID_INPUT`` listing them (no silent drops).
    """

    symbols: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Symbols to rank (VN tickers)",
    )
    as_of_date: str = Field(..., pattern=DATE_PATTERN, description="Analysis date (YYYY-MM-DD)")
    algorithm_version: str = Field("v1.0", pattern=r"^v\d+\.\d+$")
    weights: Optional[Dict[str, float]] = Field(
        None,
        description="Optional weights for momentum/trend/volume/volatility (must sum to 1.0)",
    )
    series: Dict[str, List[OHLCVBar]] = Field(
        ...,
        min_length=1,
        description="Symbol -> ascending OHLCV bars for real indicator computation",
    )

    @field_validator("symbols")
    @classmethod
    def _symbols_pattern(cls, v: List[str]) -> List[str]:
        import re

        pat = re.compile(SYMBOL_PATTERN)
        bad = [s for s in v if not pat.match(s)]
        if bad:
            raise ValueError(f"invalid ticker(s): {', '.join(bad)} (pattern {SYMBOL_PATTERN})")
        return v


class RankResponse(BaseModel):
    algorithm_version: str
    as_of_date: str
    ranked_at: str
    weights_used: Dict[str, float]
    ranked: List[Dict[str, Any]]
    excluded: List[Dict[str, Any]]
