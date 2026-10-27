# Streaming

Provider adapters normalize typed events, then quality validation precedes publication
to Redpanda. Processors derive bars, book state, rolling features, inference requests,
predictions, and delayed outcomes. Redis exposes only latest ephemeral state to the API;
TimescaleDB and object storage retain authoritative history and replay inputs.

Subscriptions are demand-driven. Opening an instrument touches its lease and adds only
required context symbols; inactive leases expire. SPY, QQQ, and sector context are
included only when required by an active workspace/model. Reconnect logic must detect
sequence gaps, mark stale state, and backfill or explicitly disclose unrecoverable gaps.

Latency spans provider event time through browser receipt. Each boundary preserves the
timestamps required to measure normalization, processing, inference, publish, and
transport delay independently.
