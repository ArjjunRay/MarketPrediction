from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from app.schemas.events import EventEnvelope, QualityFlag, QuoteEvent
from app.streaming.quality import MarketEventValidator


def quote(*, event_id=None, sequence=1, seconds_ago=0, bid="10", ask="11") -> QuoteEvent:
    now = datetime.now(UTC)
    observed = now - timedelta(seconds=seconds_ago)
    return QuoteEvent(
        envelope=EventEnvelope(
            event_id=event_id or uuid4(),
            correlation_id=uuid4(),
            provider="test",
            dataset="quotes",
            instrument_id=INSTRUMENT_ID,
            sequence_number=sequence,
            provider_timestamp=observed,
            received_timestamp=now,
            processed_timestamp=now,
            is_simulated=True,
        ),
        symbol="TEST",
        bid_price=Decimal(bid),
        bid_size=Decimal("1"),
        ask_price=Decimal(ask),
        ask_size=Decimal("1"),
    )


INSTRUMENT_ID = uuid4()


def test_detects_duplicate_sequence_gap_and_crossed_market() -> None:
    validator = MarketEventValidator()
    first_id = uuid4()
    validator.validate(quote(event_id=first_id, sequence=1))

    flags = validator.validate(quote(event_id=first_id, sequence=3, bid="12", ask="11"))

    assert set(flags) == {
        QualityFlag.DUPLICATE,
        QualityFlag.SEQUENCE_GAP,
        QualityFlag.CROSSED_MARKET,
    }


def test_detects_stale_event() -> None:
    event = quote(seconds_ago=10)
    flags = MarketEventValidator(stale_after=timedelta(seconds=5)).validate(
        event, now=datetime.now(UTC)
    )
    assert QualityFlag.STALE in flags
