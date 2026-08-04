# vnstock-advisor

Vietnam Stock Advisor - A monorepo for stock analysis and suggestion platform.

## Architecture

```
vnstock-advisor/
├── services/
│   ├── data-ingest/      # Python: Fetches and normalizes market data
│   ├── analysis-engine/  # Python: Technical analysis and signals
│   ├── suggestion-api/   # Node.js: REST API for suggestions
│   └── web-ui/           # React/TypeScript: Frontend dashboard
├── shared/
│   ├── typescript/       # Shared Zod schemas & TypeScript config
│   └── python/           # Shared Pydantic models & config
├── docker-compose.yml    # PostgreSQL + Redis
└── scripts/
    └── init-db.sql       # TimescaleDB schema initialization
```

## Prerequisites

- Docker & Docker Compose v2
- Node.js 20+
- Python 3.11+
- npm 10+

## Quick Start

```bash
# 1. Clone and navigate
cd workspace/apps/vnstock-advisor

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys and JWT keys

# 3. Start infrastructure
docker compose up -d

# 4. Initialize database (creates TimescaleDB hypertable)
docker compose exec -T postgres psql -U vnstock -d vnstock_advisor < scripts/init-db.sql

# 5. Install dependencies
npm install
pip install -e ./shared/python[dev]
```

## Development

### Start all services (in separate terminals)

```bash
# Terminal 1: Data Ingest (Python/FastAPI)
cd services/data-ingest
pip install -e .[dev]
uvicorn main:app --reload --port 8001

# Terminal 2: Analysis Engine (Python/FastAPI)
cd services/analysis-engine
pip install -e .[dev]
uvicorn main:app --reload --port 8002

# Terminal 3: Suggestion API (Node.js/Fastify)
cd services/suggestion-api
npm install
npm run dev

# Terminal 4: Web UI (React/Vite)
cd services/web-ui
npm install
npm run dev
```

### Run tests

```bash
# All tests
npm test                    # TypeScript services
pytest services/*/tests     # Python services

# Single service
npm run test --workspace=@vnstock/shared-typescript
pytest services/data-ingest/tests -v
```

### Lint & Type Check

```bash
# TypeScript
npm run lint
npm run typecheck

# Python
ruff check .
ruff format --check .
mypy shared/python/src services/*/src
```

### Test Commands

```bash
# All tests
npm test                    # TypeScript services
pytest services/*/tests     # Python services

# Single service
npm run test --workspace=@vnstock/shared-typescript
pytest services/data-ingest/tests -v
pytest services/analysis-engine/tests -v
```

## Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL 15 + TimescaleDB |
| redis | 6379 | Redis 7 with persistence |

### Useful Commands

```bash
# View logs
docker compose logs -f postgres
docker compose logs -f redis

# Stop all
docker compose down

# Stop and remove volumes (WARNING: destroys data)
docker compose down -v

# Restart single service
docker compose restart postgres
```

## Environment Variables

See `.env.example` for all required variables.

### Required for Production

- `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` - RSA keys for JWT signing
- At least one data source API key (`VNSTOCK_API_KEY`, `ALPHA_VANTAGE_API_KEY`, or `TWELVE_DATA_API_KEY`)

### Generate JWT Keys

```bash
# Generate private key
openssl genrsa -out private.pem 2048

# Extract public key
openssl rsa -in private.pem -pubout -out public.pem

# Copy contents to .env (escape newlines for docker-compose)
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push/PR:

- TypeScript: ESLint, TypeScript type-check, Vitest
- Python: Ruff lint/format, MyPy type-check, Pytest
- Shared packages: Independent validation
- Docker Compose: Config validation
- Security: Gitleaks secret scanning
- Dependencies: Snyk vulnerability scanning

## Project Structure Details

### Shared Packages

**`@vnstock/shared-typescript`** (npm)
- Zod schemas for all API contracts
- MarketData, Suggestion, AnalysisResult types
- HealthCheck, PaginatedResponse utilities

**`vnstock-shared-python`** (pip)
- SQLAlchemy models with TimescaleDB hypertable
- Pydantic models for validation
- Settings management with pydantic-settings

### Service Contracts

All services communicate via shared schemas:

```
data-ingest → PostgreSQL (market_data hypertable)
analysis-engine → reads market_data, writes signals
suggestion-api → reads signals, serves REST API
web-ui → consumes suggestion-api
```

## License

MIT