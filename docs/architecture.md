# Architecture

## Principles

QStream uses explicit service contracts and provider adapters while remaining deployable as a small number of processes. The initial system avoids premature microservices but preserves boundaries needed to split ingestion, processing, inference, evaluation, and browser fanout later.

The current system has one product mode: anonymous public access. Only fields with
verified public-display rights may be exposed. Private/authenticated research is not a
current milestone; the provider boundaries remain capable of supporting it later.

Top-of-book/NBBO is never represented as a full order book.

## Runtime flow

```text
provider -> adapter -> validation -> Redpanda -> feature processors
         -> TimescaleDB/raw object storage
feature processors -> Redis -> inference -> prediction events
Redis + TimescaleDB -> FastAPI/WebSocket gateway -> Next.js terminal
prediction events -> delayed evaluator -> realized outcomes
```

## Components

| Component | Responsibility |
|---|---|
| Frontend | Accessible terminal, search, capability-aware states, live transport |
| API | Query/control plane, capability policy, health, WebSocket gateway |
| Provider adapters | Convert vendor events to internal contracts |
| Stream processors | Quality checks, book/bar/feature state, event-time ordering |
| Inference | Versioned model loading and prediction publication |
| Evaluation | Append realized outcomes after forecast horizons mature |
| PostgreSQL/TimescaleDB | Authoritative structured and time-series state |
| Redis | Ephemeral latest values and fanout state |
| Redpanda | Replayable, versioned event backbone |
| MinIO | Raw captures, datasets, model and research artifacts |

## Deployment boundaries

The API, ingestion, stream processing, inference, evaluation, and paper-trading modules are separate packages. They may share a deployment during development but must communicate through typed interfaces or event contracts when separated.

## Capability policy

Provider capabilities and licensing flags are data, not scattered conditionals. Each provider reports availability for trades, bars, NBBO, L2, L3/MBO, news, and public redistribution. API responses and UI states derive from that policy.

## Deferred decisions

- A zero-cost market-data source with explicit public redistribution rights
- News provider and text redistribution rights
- Cloud and managed-service selection
