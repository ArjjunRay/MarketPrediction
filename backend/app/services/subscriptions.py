from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True)
class Subscription:
    symbol: str
    expires_at: datetime


class SubscriptionRegistry:
    """Tracks demand-driven symbols without streaming the full market universe."""

    def __init__(self, idle_ttl: timedelta = timedelta(minutes=15)) -> None:
        self._idle_ttl = idle_ttl
        self._subscriptions: dict[str, Subscription] = {}

    def touch(self, symbol: str, *, now: datetime | None = None) -> Subscription:
        observed_at = now or datetime.now(UTC)
        normalized = symbol.strip().upper()
        if not normalized:
            raise ValueError("symbol must not be empty")
        subscription = Subscription(normalized, observed_at + self._idle_ttl)
        self._subscriptions[normalized] = subscription
        return subscription

    def active(self, *, now: datetime | None = None) -> set[str]:
        observed_at = now or datetime.now(UTC)
        self.expire(now=observed_at)
        return set(self._subscriptions)

    def expire(self, *, now: datetime | None = None) -> set[str]:
        observed_at = now or datetime.now(UTC)
        expired = {
            symbol
            for symbol, subscription in self._subscriptions.items()
            if subscription.expires_at <= observed_at
        }
        for symbol in expired:
            del self._subscriptions[symbol]
        return expired
