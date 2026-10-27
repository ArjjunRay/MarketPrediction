# Data and event contracts

## Event envelope

All streaming records include provider event time, receive time, processing time, provider/feed identifiers, instrument ID, optional sequence number, schema version, quality flags, correlation ID, and an explicit simulation flag.

Protobuf definitions live in `contracts/protobuf`. Pydantic transport models mirror the same semantics for JSON-facing APIs.

## Topic naming

- `market.trades.v1`
- `market.quotes.v1`
- `market.book.v1`
- `market.bars.v1`
- `market.quality.v1`
- `features.live.v1`
- `predictions.live.v1`
- `predictions.realized.v1`
- `news.events.v1`
- `models.health.v1`
- `paper.orders.v1`
- `paper.fills.v1`

## Time semantics

Provider timestamps are never replaced by ingest time. Processing stages append timestamps so end-to-end latency can be measured. Out-of-order and duplicate handling occurs before state mutation.

## Simulation policy

Development simulation is disabled by default. Simulated records must set `is_simulated=true`, use provider `simulated`, and must not be persisted into production research datasets.

## Approved external data

SEC filing/fact, BLS/BEA series and Treasury-yield responses retain source and retrieval
metadata. They are fundamentals/macro inputs, not market-price observations. No real
price history is currently approved, so the historical price dataset builder must not
run on simulated or unlabeled substitute data.
