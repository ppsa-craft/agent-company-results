import { z } from 'zod';

// Market data schemas
export const MarketDataSchema = z.object({
  time: z.string().datetime(),
  symbol: z.string().min(1).max(20),
  open: z.number().positive(),
  high: z.number().positive(),
  low: z.number().positive(),
  close: z.number().positive(),
  volume: z.number().int().nonnegative(),
  source: z.string().min(1).max(50),
});

export const MarketDataBatchSchema = z.array(MarketDataSchema);

export type MarketData = z.infer<typeof MarketDataSchema>;

// Suggestion schemas
export const SuggestionSchema = z.object({
  id: z.string().uuid(),
  symbol: z.string().min(1).max(20),
  action: z.enum(['BUY', 'SELL', 'HOLD']),
  confidence: z.number().min(0).max(1),
  reasoning: z.string().min(1).max(500),
  targetPrice: z.number().positive().optional(),
  stopLoss: z.number().positive().optional(),
  timeframe: z.enum(['1D', '1W', '1M', '3M']),
  createdAt: z.string().datetime(),
});

export type Suggestion = z.infer<typeof SuggestionSchema>;

// Analysis schemas
export const AnalysisResultSchema = z.object({
  symbol: z.string().min(1).max(20),
  indicators: z.record(z.string(), z.number()),
  signals: z.array(z.enum(['BUY', 'SELL', 'NEUTRAL'])),
  trend: z.enum(['BULLISH', 'BEARISH', 'SIDEWAYS']),
  strength: z.number().min(0).max(1),
  timestamp: z.string().datetime(),
});

export type AnalysisResult = z.infer<typeof AnalysisResultSchema>;

// API response schemas
export const ApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema.optional(),
    error: z.string().optional(),
    meta: z.object({
      timestamp: z.string().datetime(),
      requestId: z.string().uuid(),
    }).optional(),
  });

export const PaginatedResponseSchema = <T extends z.ZodTypeAny>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    total: z.number().int().nonnegative(),
    page: z.number().int().positive(),
    pageSize: z.number().int().positive(),
    totalPages: z.number().int().nonnegative(),
  });

// Health check schema
export const HealthCheckSchema = z.object({
  status: z.enum(['healthy', 'degraded', 'unhealthy']),
  service: z.string(),
  version: z.string(),
  timestamp: z.string().datetime(),
  checks: z.array(
    z.object({
      name: z.string(),
      status: z.enum(['pass', 'warn', 'fail']),
      message: z.string().optional(),
    })
  ).optional(),
});

export type HealthCheck = z.infer<typeof HealthCheckSchema>;

// Export all schemas
export const schemas = {
  MarketData: MarketDataSchema,
  MarketDataBatch: MarketDataBatchSchema,
  Suggestion: SuggestionSchema,
  AnalysisResult: AnalysisResultSchema,
  HealthCheck: HealthCheckSchema,
} as const;

export type Schemas = typeof schemas;