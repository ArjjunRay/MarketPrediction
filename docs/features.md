# Feature framework

Feature records are versioned by feature set, event time, instrument, and provenance.
Planned groups are microstructure, price/return, volume, volatility, market context,
related assets, session/time, and licensed point-in-time news.

Every online feature must have a replay-equivalent offline implementation or a tested
shared kernel. Window boundaries use event time, late-data behavior is explicit, and
normalizers/imputers/selectors fit only on the training interval. Full-depth features
such as cancellation or replenishment rate remain unavailable without an entitled
L2/L3 or MBO feed. NBBO can support spread and midpoint but is not an order book.

Feature tests must cover ordering, exact window edges, session boundaries, corporate
actions, missing context instruments, replay/online parity, and deliberate future-data
leakage probes.
