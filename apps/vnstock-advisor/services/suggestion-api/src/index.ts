import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import jwt from '@fastify/jwt';
import rateLimit from '@fastify/rate-limit';
import { HealthCheckSchema } from '@vnstock/shared-typescript';

const app = Fastify({ logger: true });

// Security plugins
await app.register(helmet);
await app.register(cors, { origin: true });
await app.register(rateLimit, { max: 100, timeWindow: '1 minute' });
await app.register(jwt, {
  secret: process.env.JWT_PRIVATE_KEY || 'dev-secret-change-in-production',
});

// Health check
app.get('/health', async () => {
  return HealthCheckSchema.parse({
    status: 'healthy',
    service: 'suggestion-api',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
  });
});

app.get('/', async () => {
  return { message: 'vnstock Suggestion API' };
});

// Start server
const start = async () => {
  try {
    const port = parseInt(process.env.SUGGESTION_API_PORT || '8003', 10);
    await app.listen({ port, host: '0.0.0.0' });
    console.log(`Suggestion API listening on port ${port}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();