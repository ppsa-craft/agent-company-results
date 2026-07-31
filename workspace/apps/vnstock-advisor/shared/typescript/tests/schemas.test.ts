import { describe, it, expect } from 'vitest';
import {
  MarketDataSchema,
  SuggestionSchema,
  AnalysisResultSchema,
  HealthCheckSchema,
} from '../src/index';

describe('Shared TypeScript Schemas', () => {
  describe('MarketDataSchema', () => {
    it('validates correct market data', () => {
      const validData = {
        time: '2024-01-15T10:00:00Z',
        symbol: 'VCB',
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: 1000000,
        source: 'vnstock',
      };
      const result = MarketDataSchema.safeParse(validData);
      expect(result.success).toBe(true);
    });

    it('rejects invalid symbol', () => {
      const invalidData = {
        time: '2024-01-15T10:00:00Z',
        symbol: '',
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: 1000000,
        source: 'vnstock',
      };
      const result = MarketDataSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
    });

    it('rejects negative volume', () => {
      const invalidData = {
        time: '2024-01-15T10:00:00Z',
        symbol: 'VCB',
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: -100,
        source: 'vnstock',
      };
      const result = MarketDataSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
    });
  });

  describe('SuggestionSchema', () => {
    it('validates correct suggestion', () => {
      const validData = {
        id: '123e4567-e89b-12d3-a456-426614174000',
        symbol: 'VCB',
        action: 'BUY' as const,
        confidence: 0.85,
        reasoning: 'Strong uptrend',
        targetPrice: 110.0,
        stopLoss: 98.0,
        timeframe: '1W' as const,
        createdAt: '2024-01-15T10:00:00Z',
      };
      const result = SuggestionSchema.safeParse(validData);
      expect(result.success).toBe(true);
    });

    it('rejects invalid action', () => {
      const invalidData = {
        id: '123e4567-e89b-12d3-a456-426614174000',
        symbol: 'VCB',
        action: 'INVALID',
        confidence: 0.85,
        reasoning: 'Test',
        timeframe: '1W' as const,
        createdAt: '2024-01-15T10:00:00Z',
      };
      const result = SuggestionSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
    });
  });

  describe('HealthCheckSchema', () => {
    it('validates healthy status', () => {
      const validData = {
        status: 'healthy' as const,
        service: 'test-service',
        version: '1.0.0',
        timestamp: '2024-01-15T10:00:00Z',
      };
      const result = HealthCheckSchema.safeParse(validData);
      expect(result.success).toBe(true);
    });
  });
});