from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.events import EventEnvelope, QuoteEvent


def envelope() -> EventEnvelope:
    now = datetime.now(UTC)
    return EventEnvelope(
        event_id=uuid4(),
        correlation_id=uuid4(),
        provider="test",
        dataset="test",
        instrument_id=uuid4(),
        provider_timestamp=now,
        received_timestamp=now,
        processed_timestamp=now,
        is_simulated=True,
    )


def test_quote_rejects_negative_price() -> None:
    with pytest.raises(ValidationError):
        QuoteEvent(
            envelope=envelope(),
            symbol="TEST",
            bid_price=Decimal("-1"),
            bid_size=Decimal("1"),
            ask_price=Decimal("2"),
            ask_size=Decimal("1"),
        )
