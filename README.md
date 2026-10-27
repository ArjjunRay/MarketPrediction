# QStream

QStream is a provider-neutral foundation for an anonymous public quantitative research
terminal. It never presents simulated development events as real market data. The
architecture can grow into live ingestion, point-in-time research, forecasting,
backtesting, and browser-local paper simulation without coupling the system to one vendor.

## Current status

The repository contains a verified runnable foundation: a Next.js terminal shell, FastAPI API and WebSocket gateway, typed provider contracts, TimescaleDB, Redis, Redpanda, S3-compatible local object storage, migrations, health checks, metrics, and a disabled-by-default simulated development feed.

No legally eligible zero-cost public-display price or news provider is configured. SEC,
BLS, Treasury and BEA adapters provide official fundamentals, filings and macro data;
they do not masquerade as price feeds. See
[implementation status](docs/implementation-status.md).

## Local start

1. Copy `.env.example` to `.env` and replace the local-only passwords.
2. Run `docker compose up --build`.
3. Open `http://localhost:33000`.
4. API documentation is at `http://localhost:38000/docs`.

The first build compiles the pinned community MinIO source and can take several minutes. Later starts reuse the local image and volumes.

QStream uses a dedicated host-port range to avoid colliding with common local
services. All host ports are configurable in `.env.example`; containers use their
standard internal ports.

The default configuration does not emit simulated prices. To exercise transport locally, explicitly set `QSTREAM_ENABLE_SIMULATED_PROVIDER=true`; every resulting event carries `is_simulated=true` and the UI must label it.

Database migrations run automatically before the API starts. The optional
observability profile is started with
`docker compose --profile observability up --build`.

## Data flow

The intended live path is provider adapter → validation and normalization → versioned
Redpanda events → stream processors and feature engine → Redis live state and durable
Timescale history → inference events → FastAPI WebSocket gateway → browser. Raw capture,
replay data, datasets, and model artifacts use the S3-compatible object-store boundary.
Redis is never the sole authoritative copy.

## Architecture and methodology

See [architecture](docs/architecture.md), [events](docs/events.md),
[database](docs/database.md), [modeling](docs/modeling.md), and
[security](docs/security.md). Provider and licensing boundaries are described in
[providers](docs/providers.md); point-in-time feature rules and validation are in
[features](docs/features.md) and [evaluation](docs/evaluation.md).

## Development

- Backend: Python 3.12+, FastAPI, Pydantic, SQLAlchemy, pytest, Ruff, mypy
- Frontend: Next.js App Router, strict TypeScript, Tailwind CSS
- Infrastructure: TimescaleDB, Redis, Redpanda, MinIO
- Optional observability: Prometheus and Grafana through the `observability` profile

Environment variables are documented in [environment](docs/environment.md).

## Verification

Backend checks:

```bash
cd backend
.venv/bin/ruff check app tests migrations
.venv/bin/mypy app
.venv/bin/python -m pytest -q
```

Frontend checks:

```bash
cd frontend
npm run typecheck
npm run format:check
npm run lint
npm test -- --run
npm run build
npm run test:e2e
npm audit --omit=dev
```

Runtime checks:

```bash
docker compose config --quiet
docker compose ps -a
```

## Data and modeling limits

No live price provider, licensed news, or trained production model is configured. The
main application intentionally has no user-account system. The checked-in catalog is
reference metadata for
search, not a live price source. Full-depth views stay disabled unless a provider
explicitly reports L2/L3 capability and the current user has the required entitlement.

Research pipelines must use point-in-time data, chronological or walk-forward
evaluation, train-only preprocessing, and purging/embargo where labels overlap.
No profitability or predictive-quality claim exists yet.

The current object store is for local development. Production requires an approved,
maintained S3-compatible service, retention policy, encryption, backup/restore testing,
and credentials supplied through a secrets manager. Cloud provisioning, live providers,
trained models, production rate limiting, and public-data caching are
not implemented and are not implied by the runnable local foundation.

See [deployment](docs/deployment.md), [testing/status](docs/implementation-status.md),
and [UI rules](docs/ui.md) for the remaining decision boundaries.

GitHub automation is intentionally absent by project requirement.
