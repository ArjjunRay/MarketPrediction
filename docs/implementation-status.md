# Implementation status

Last updated: 2026-10-13

## Completed

- Public, anonymous product policy; no login, subscription, paid tier or user key
- Zero-paid-data and provider-redistribution decision record
- Provider-neutral market, historical, fundamentals, macro, news and replay boundaries
- SEC EDGAR company-facts/submissions adapter with required operator User-Agent gating
- BLS public-series, U.S. Treasury daily-yield and operator-keyed BEA NIPA adapters
- Public source-status API with source, status, cadence, delay and resolution metadata
- Honest market-price state: no eligible source, no L2/L3, no live news and no model claims
- UI removal of profile/authentication cues and unsupported 5/30-second horizons
- Next.js terminal, FastAPI API/WebSocket gateway and instrument search
- TimescaleDB, Redis, Redpanda and S3-compatible local object storage
- Versioned event contracts, quality checks, demand-driven subscriptions and migrations
- Docker Compose health gates, metrics, structured logging and local operational checks

## Intentionally unavailable

- Equity/ETF prices, bars, trades, quotes and historical-price ingestion: no reviewed
  zero-cost source grants anonymous public redistribution
- L2/L3/MBO and depth-derived microstructure
- Licensed market news
- Price-derived features, training datasets, baseline forecasts and walk-forward results
- Persistent personal portfolios or private dashboards

Building models without a lawful real-price target would create fake output. These stages
stay blocked rather than being filled with simulated data.

## Next executable work

- Configure `QSTREAM_SEC_USER_AGENT` and validate live SEC company facts/filing events
- Configure the free operator `QSTREAM_BEA_API_KEY` for NIPA/GDP macro series
- Persist/cache approved SEC, BLS, Treasury and BEA observations with provenance
- Add SEC filing-event timeline and fundamentals panels to the company experience
- Add macro features only at frequencies valid for their publication cadence
- Add SEC MIDAS aggregate research ingestion if its metrics support a defined experiment
- Implement price ingestion, features, datasets, baselines and walk-forward evaluation
  only after written public-display permission or a new clearly permissive free source exists

## Current decisions—not open requirements

- Authentication is not a milestone.
- GitHub integration is not planned.
- Paid market-data providers are out of scope.
- FRED is excluded initially because its current key guidance conflicts with one
  operator-owned backend key and individual series require licensing review.
- Hosting cost is separate from data cost; no production host has been selected.

## Known engineering debt

- Upstream government calls need shared caching and application-level rate limiting
  before high-traffic public deployment.
- The full npm audit, including development tooling, reports five high-severity
  transitive advisories under the ESLint/Next.js lint chain; production dependencies
  report zero vulnerabilities.
- Community MinIO is pinned and source-built for local development; production storage
  must use an approved maintained S3-compatible service.
