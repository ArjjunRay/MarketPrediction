from datetime import UTC, datetime, timedelta

from app.services.subscriptions import SubscriptionRegistry


def test_subscription_normalizes_and_expires() -> None:
    now = datetime.now(UTC)
    registry = SubscriptionRegistry(idle_ttl=timedelta(seconds=30))

    registry.touch(" nvda ", now=now)

    assert registry.active(now=now + timedelta(seconds=29)) == {"NVDA"}
    assert registry.active(now=now + timedelta(seconds=30)) == set()
