# Event contracts

Internal events are vendor-neutral and versioned. Protobuf definitions live in
`contracts/protobuf/market_events.proto`; Pydantic runtime contracts live in
`backend/app/schemas/events.py`. Every event carries provider, dataset, instrument,
provider/receive/process timestamps, schema version, trace correlation, sequence when
available, quality flags, and a simulation marker.

Topic names are centralized in `backend/app/streaming/topics.py`. Breaking payload
changes require a new topic/schema version. Consumers must ignore unknown additive
fields and reject unsupported major versions. Replay must preserve original provider
time and assign new processing metadata without rewriting the source event.

Data-quality findings publish separately to `market.quality.v1`; they do not silently
mutate authoritative source facts. A crossed quote is a quality event, not an order
book. Top-of-book messages never imply L2/L3 availability.
