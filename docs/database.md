# Database

PostgreSQL 16 with TimescaleDB is the authoritative structured store. Alembic owns
schema changes and runs as the Compose `migrate` gate before the API. Redis is only
ephemeral live state; MinIO holds immutable raw captures, dataset manifests, research
artifacts, and model artifacts.

Time-series entities use composite primary keys containing their partition timestamp.
Hypertables cover quotes, trades, market ticks, bars, book snapshots/events, features,
provider/system health, and related high-volume series. Entity, provider, symbol,
event-time, model-version, and evaluation dimensions are indexed. Application-level
deduplication uses event IDs and provider sequences; a time-only unique constraint is
not used because Timescale unique indexes must contain the partition key.

Retention and compression policies are intentionally not hard-coded yet. They depend
on the selected feed rate, replay requirements, approved historical depth, and local/cloud
storage budget. Raw captures must be partitioned by provider/dataset/symbol/date and
accompanied by an immutable manifest and checksum.
