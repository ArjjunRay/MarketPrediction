from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from app.providers.replay import ReplayMarketDataProvider
from app.schemas.events import EventEnvelope, QuoteEvent


@pytest.mark.asyncio
async def test_replay_is_deterministic_and_never_public() -> None:
    now = datetime.now(UTC)
    event = QuoteEvent(
        envelope=EventEnvelope(
            event_id=uuid4(),
            correlation_id=uuid4(),
            provider="fixture",
            dataset="test-replay",
            instrument_id=uuid4(),
            sequence_number=1,
            provider_timestamp=now,
            received_timestamp=now,
            processed_timestamp=now,
            is_simulated=True,
        ),
        symbol="NVDA",
        bid_price=Decimal("100"),
        bid_size=Decimal("10"),
        ask_price=Decimal("100.02"),
        ask_size=Decimal("12"),
    )
    provider = ReplayMarketDataProvider([event])

    replayed = [item async for item in provider.stream({"NVDA"})]

    assert replayed == [event]
    assert provider.capabilities.public_display == frozenset()
