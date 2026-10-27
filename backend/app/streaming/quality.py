from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from app.providers.base import MarketEvent
from app.schemas.events import QualityFlag, QuoteEvent


@dataclass
class _StreamState:
    event_ids: set[UUID] = field(default_factory=set)
    last_provider_timestamp: datetime | None = None
    last_sequence: int | None = None


class MarketEventValidator:
    """Stateful integrity checks applied after normalization and before publishing.

    Transport adapters remain responsible for malformed wire messages. This layer
    catches cross-message ordering and market-integrity failures in typed events.
    """

    def __init__(self, stale_after: timedelta = timedelta(seconds=5)) -> None:
        self._stale_after = stale_after
        self._state: dict[tuple[str, str, UUID], _StreamState] = {}

    def validate(
        self, event: MarketEvent, *, now: datetime | None = None
    ) -> tuple[QualityFlag, ...]:
        envelope = event.envelope
        key = (envelope.provider, envelope.dataset, envelope.instrument_id)
        state = self._state.setdefault(key, _StreamState())
        flags: list[QualityFlag] = []

        if envelope.event_id in state.event_ids:
            flags.append(QualityFlag.DUPLICATE)
        else:
            state.event_ids.add(envelope.event_id)

        if (
            state.last_provider_timestamp is not None
            and envelope.provider_timestamp < state.last_provider_timestamp
        ):
            flags.append(QualityFlag.OUT_OF_ORDER)

        sequence = envelope.sequence_number
        if sequence is not None and state.last_sequence is not None:
            if sequence > state.last_sequence + 1:
                flags.append(QualityFlag.SEQUENCE_GAP)
            elif sequence <= state.last_sequence:
                flags.append(QualityFlag.OUT_OF_ORDER)

        observed_at = now or datetime.now(UTC)
        if observed_at - envelope.provider_timestamp > self._stale_after:
            flags.append(QualityFlag.STALE)

        if isinstance(event, QuoteEvent) and event.bid_price > event.ask_price:
            flags.append(QualityFlag.CROSSED_MARKET)

        state.last_provider_timestamp = max(
            filter(None, (state.last_provider_timestamp, envelope.provider_timestamp))
        )
        if sequence is not None:
            state.last_sequence = max(sequence, state.last_sequence or sequence)

        return tuple(dict.fromkeys(flags))

    @staticmethod
    def is_valid_price(value: Decimal) -> bool:
        return value.is_finite() and value > 0
