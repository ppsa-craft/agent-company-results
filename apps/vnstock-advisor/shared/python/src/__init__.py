"""
vnstock-shared-python: Shared Python models and utilities for vnstock-advisor.
"""

from .models import (
    MarketData,
    MarketDataCreate,
    MarketDataRead,
    MarketDataBatch,
    SuggestionBase,
    SuggestionCreate,
    SuggestionRead,
    AnalysisResultBase,
    AnalysisResultCreate,
    AnalysisResultRead,
    HealthCheck,
)
from .config import Settings, get_settings

__all__ = [
    "MarketData",
    "MarketDataCreate",
    "MarketDataRead",
    "MarketDataBatch",
    "SuggestionBase",
    "SuggestionCreate",
    "SuggestionRead",
    "AnalysisResultBase",
    "AnalysisResultCreate",
    "AnalysisResultRead",
    "HealthCheck",
    "Settings",
    "get_settings",
]

__version__ = "0.1.0"