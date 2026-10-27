from enum import StrEnum


class Topic(StrEnum):
    """Versioned event-bus topic names; payload versions evolve independently."""

    TRADES = "market.trades.v1"
    QUOTES = "market.quotes.v1"
    BOOK = "market.book.v1"
    BARS = "market.bars.v1"
    QUALITY = "market.quality.v1"
    LIVE_FEATURES = "features.live.v1"
    LIVE_PREDICTIONS = "predictions.live.v1"
    REALIZED_PREDICTIONS = "predictions.realized.v1"
    NEWS = "news.events.v1"
    MODEL_HEALTH = "models.health.v1"
    PAPER_ORDERS = "paper.orders.v1"
    PAPER_FILLS = "paper.fills.v1"
