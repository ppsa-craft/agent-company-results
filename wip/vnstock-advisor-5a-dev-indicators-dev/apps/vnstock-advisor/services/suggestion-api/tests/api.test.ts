import { describe, it, expect, vi } from 'vitest';
import Fastify from 'fastify';

describe('Suggestion API', () => {
  it('should return health check', async () => {
    const app = Fastify();
    
    app.get('/health', async () => ({
      status: 'healthy',
      service: 'suggestion-api',
      version: '0.1.0',
      timestamp: new Date().toISOString(),
    }));

    await app.ready();
    const response = await app.inject({ method: 'GET', url: '/health' });
    
    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.status).toBe('healthy');
    expect(body.service).toBe('suggestion-api');
    
    await app.close();
  });
});