# Backtesting

The planned engine is event-driven and shares order/execution semantics with paper
trading. It must support market and limit orders, multiple symbols, position sizing,
risk rules, exits, spread, fees, slippage, and configurable latency.

Replays use the information set available at each event time. Signals cannot see later
bars, revised news, future constituents, or resolved outcomes. Fill assumptions must
match available data granularity: top-of-book cannot justify queue-position or L3 fill
claims. Results must identify data source, feed type, adjustment policy, costs, and
execution model.
