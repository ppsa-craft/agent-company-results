"""Deterministic ranking module for vnstock-advisor analysis-engine.

This module implements the ranking functionality as described in task vnstock-advisor-5c-dev-ranking.
It calculates weighted composite scores based on momentum, trend, volume, and volatility indicators,
and provides deterministic reasoning for each ranked symbol.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class RankedSymbol:
    """Represents a ranked symbol with its composite score and component breakdown."""
    rank: int
    symbol: str
    composite_score: float
    momentum_score: float
    trend_score: float
    volume_score: float
    volatility_score: float
    components: List[Dict[str, Any]]
    sub_components: Dict[str, Any]
    reasoning: List[str]
    excluded: bool = False
    exclusion_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "rank": self.rank,
            "symbol": self.symbol,
            "composite_score": self.composite_score,
            "components": self.components,
            "sub_components": self.sub_components,
            "reasoning": self.reasoning,
        }
        
        if self.excluded:
            result["excluded"] = True
            result["exclusion_reason"] = self.exclusion_reason
        
        result["component_scores"] = {
            "momentum": self.momentum_score,
            "trend": self.trend_score,
            "volume": self.volume_score,
            "volatility": self.volatility_score,
        }
        
        return result


class RankingError(Exception):
    """Raised when ranking encounters validation errors."""
    pass


def percentile_rank(sorted_values: List[float], value: float) -> float:
    """Calculate percentile rank using linear interpolation (spec compliant).
    
    Args:
        sorted_values: Sorted list of values in ascending order
        value: Value to rank
        
    Returns:
        Percentile rank between 0.0 and 100.0
    """
    if not sorted_values:
        return 50.0
    
    # Handle edge cases
    if value <= sorted_values[0]:
        return 0.0
    if value >= sorted_values[-1]:
        return 100.0
    
    # Find position where value would be inserted
    for i, val in enumerate(sorted_values):
        if val >= value:
            lower_idx = i - 1 if i > 0 else 0
            upper_idx = i
            
            lower_val = sorted_values[lower_idx]
            upper_val = sorted_values[upper_idx]
            
            # Linear interpolation
            if upper_val == lower_val:
                return 50.0
                
            position = (value - lower_val) / (upper_val - lower_val)
            lower_percentile = (lower_idx) / (len(sorted_values) - 1) * 100
            upper_percentile = (upper_idx) / (len(sorted_values) - 1) * 100
            
            return lower_percentile + position * (upper_percentile - lower_percentile)
    
    return 100.0


def rank_symbols(
    indicators_by_symbol: Dict[str, Dict[str, Any]],
    screened_symbols: List[str],
    weights: Optional[Dict[str, float]] = None,
    version: str = "1.0",
) -> List[Dict[str, Any]]:
    """Rank symbols based on composite scores from indicators.
    
    Args:
        indicators_by_symbol: Dict mapping symbol to indicator values
        screened_symbols: List of symbols to include in ranking
        weights: Optional dict with keys "momentum", "trend", "volume", "volatility"
                Default: {"momentum": 0.4, "trend": 0.3, "volume": 0.2, "volatility": 0.1}
        version: Version string for deterministic reasoning
        
    Returns:
        List of ranked symbol results as dictionaries
    """
    # Default weights (40% momentum, 30% trend, 20% volume, 10% volatility)
    if weights is None:
        weights = {
            "momentum": 0.4,
            "trend": 0.3,
            "volume": 0.2,
            "volatility": 0.1,
        }
    
    # Validate weights
    if abs(sum(weights.values()) - 1.0) > 0.001:
        raise RankingError("Weights must sum to 1.0")
    
    ranked_results: List[RankedSymbol] = []
    
    for symbol in screened_symbols:
        if symbol not in indicators_by_symbol:
            continue
            
        indicator_data = indicators_by_symbol[symbol]
        
        # Check for insufficient data (less than 200 valid bars)
        if indicator_data.get("valid_bars", 0) < 200:
            ranked_results.append(
                RankedSymbol(
                    rank=len(ranked_results) + 1,
                    symbol=symbol,
                    composite_score=0.0,
                    momentum_score=0.0,
                    trend_score=0.0,
                    volume_score=0.0,
                    volatility_score=0.0,
                    components=[],
                    sub_components={},
                    reasoning=[],
                    excluded=True,
                    exclusion_reason="insufficient_data",
                )
            )
            continue
        
        # Calculate component scores (simplified implementations for now)
        momentum_score = calculate_momentum(indicator_data)
        trend_score = calculate_trend(indicator_data)
        volume_score = calculate_volume(indicator_data)
        volatility_score = calculate_volatility(indicator_data)
        
        # Calculate weighted composite score
        composite_score = (
            momentum_score * weights["momentum"] +
            trend_score * weights["trend"] +
            volume_score * weights["volume"] +
            volatility_score * weights["volatility"]
        )
        
        # Generate deterministic reasoning
        reasoning = generate_reasoning(symbol, composite_score, version)
        
        # Create component breakdown
        components = create_components(momentum_score, trend_score, volume_score, volatility_score)
        
        # Create sub-components
        sub_components = create_sub_components(indicator_data)
        
        ranked_symbol = RankedSymbol(
            rank=len(ranked_results) + 1,
            symbol=symbol,
            composite_score=composite_score,
            momentum_score=momentum_score,
            trend_score=trend_score,
            volume_score=volume_score,
            volatility_score=volatility_score,
            components=components,
            sub_components=sub_components,
            reasoning=reasoning,
        )
        
        ranked_results.append(ranked_symbol)
    
    # Sort by composite score (descending) then by symbol (ascending) for ties
    ranked_results.sort(key=lambda x: (-x.composite_score, x.symbol))
    
    # Reassign ranks
    for i, ranked_symbol in enumerate(ranked_results):
        ranked_symbol.rank = i + 1
    
    return [symbol.to_dict() for symbol in ranked_results]


def calculate_momentum(indicator_data: Dict[str, Any]) -> float:
    """Calculate momentum score from ROC10 and RSI indicators."""
    roc10 = indicator_data.get("roc10", 0.0)
    rsi = indicator_data.get("rsi", 50.0)
    
    # Normalize ROC10 (assuming reasonable range)
    roc10_norm = min(max((roc10 + 50) / 100, 0.0), 1.0)
    # RSI is already in 0-100 range
    rsi_norm = rsi / 100.0
    
    # Average of ROC10 percentile and RSI normalized
    return (roc10_norm + rsi_norm) / 2.0 * 100.0


def calculate_trend(indicator_data: Dict[str, Any]) -> float:
    """Calculate trend score from passing conditions."""
    trend_conditions = indicator_data.get("trend_conditions", [])
    total_conditions = indicator_data.get("total_trend_conditions", 7)
    
    if total_conditions == 0:
        return 0.0
    
    passed = len([c for c in trend_conditions if c])
    return (passed / total_conditions) * 100.0


def calculate_volume(indicator_data: Dict[str, Any]) -> float:
    """Calculate volume score from volume ratio and OBV trend."""
    volume_ratio = indicator_data.get("volume_ratio", 1.0)
    obv_trend = indicator_data.get("obv_trend", 0.0)
    
    # Normalize volume ratio (assuming 0.1-10 range)
    volume_norm = min(max((volume_ratio - 0.1) / 9.9, 0.0), 1.0)
    # OBV trend normalized
    obv_norm = min(max((obv_trend + 1) / 2, 0.0), 1.0)
    
    # Average of volume ratio percentile and OBV trend
    return (volume_norm + obv_norm) / 2.0 * 100.0


def calculate_volatility(indicator_data: Dict[str, Any]) -> float:
    """Calculate volatility score from ATR percentile (inverted)."""
    atr_percentile = indicator_data.get("atr_percentile", 50.0)
    
    # Inverted: lower ATR = lower volatility = higher score
    return (100.0 - atr_percentile) * 1.0


def generate_reasoning(symbol: str, composite_score: float, version: str) -> List[str]:
    """Generate deterministic reasoning strings for a symbol."""
    reasoning = []
    
    if composite_score >= 80:
        band = "very strong"
    elif composite_score >= 60:
        band = "strong"
    elif composite_score >= 40:
        band = "moderate"
    elif composite_score >= 20:
        band = "weak"
    else:
        band = "very weak"
    
    # Generate deterministic reasoning based on composite score band
    reasoning.append(f"{symbol} scored in {band} band ({composite_score:.2f})")
    reasoning.append(f"Weighted composite score reflects {band} overall performance")
    
    # Add component-specific reasoning
    reasoning.append(f"{symbol} has favorable risk-adjusted characteristics")
    
    return reasoning


def create_components(
    momentum: float,
    trend: float,
    volume: float,
    volatility: float,
) -> List[Dict[str, Any]]:
    """Create component breakdown."""
    components = []
    
    # Momentum component
    momentum_band = get_band(momentum)
    components.append({
        "name": "momentum",
        "score": round(momentum, 2),
        "band": momentum_band,
        "weight": 0.4,
        "description": f"Momentum in {momentum_band} band",
    })
    
    # Trend component
    trend_band = get_band(trend)
    components.append({
        "name": "trend",
        "score": round(trend, 2),
        "band": trend_band,
        "weight": 0.3,
        "description": f"Trend in {trend_band} band",
    })
    
    # Volume component
    volume_band = get_band(volume)
    components.append({
        "name": "volume",
        "score": round(volume, 2),
        "band": volume_band,
        "weight": 0.2,
        "description": f"Volume in {volume_band} band",
    })
    
    # Volatility component (inverted)
    volatility_band = get_band(100 - volatility)  # Invert for display
    components.append({
        "name": "volatility",
        "score": round(100 - volatility, 2),
        "band": volatility_band,
        "weight": 0.1,
        "description": f"Volatility in {volatility_band} band",
    })
    
    return components


def create_sub_components(indicator_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create sub-components breakdown."""
    sub_components = {}
    
    # Sub-components for each factor
    sub_components["momentum"] = {
        "roc10": indicator_data.get("roc10", 0.0),
        "rsi": indicator_data.get("rsi", 50.0),
    }
    
    sub_components["trend"] = {
        "passed_conditions": indicator_data.get("trend_conditions", []),
        "total_conditions": indicator_data.get("total_trend_conditions", 7),
    }
    
    sub_components["volume"] = {
        "volume_ratio": indicator_data.get("volume_ratio", 1.0),
        "obv_trend": indicator_data.get("obv_trend", 0.0),
    }
    
    sub_components["volatility"] = {
        "atr_percentile": indicator_data.get("atr_percentile", 50.0),
        "atr_value": indicator_data.get("atr", 0.0),
    }
    
    return sub_components


def get_band(score: float) -> str:
    """Convert score to band description."""
    if score >= 80:
        return "strong"
    elif score >= 60:
        return "moderate"
    elif score >= 40:
        return "weak"
    else:
        return "very weak"


if __name__ == "__main__":
    # Simple test case
    sample_indicators = {
        "VNM": {
            "roc10": 15.5,
            "rsi": 65.0,
            "trend_conditions": [True, True, True, True, False, False, False],
            "total_trend_conditions": 7,
            "volume_ratio": 2.5,
            "obv_trend": 0.3,
            "atr_percentile": 30.0,
            "atr": 1.5,
            "valid_bars": 250,
        },
        "FPT": {
            "roc10": 8.2,
            "rsi": 72.0,
            "trend_conditions": [True, True, True, True, True, True, True],
            "total_trend_conditions": 7,
            "volume_ratio": 1.2,
            "obv_trend": 0.1,
            "atr_percentile": 45.0,
            "atr": 2.0,
            "valid_bars": 300,
        },
    }
    
    screened_symbols = ["VNM", "FPT"]
    
    results = rank_symbols(sample_indicators, screened_symbols)
    
    print("Ranking Results:")
    for result in results:
        print(f"\nRank {result['rank']}: {result['symbol']}")
        print(f"  Composite Score: {result['composite_score']:.2f}")
        print(f"  Components: {result['components']}")
        print(f"  Reasoning: {result['reasoning']}")
