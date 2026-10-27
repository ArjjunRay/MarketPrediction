import asyncio
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from decimal import Decimal
from uuid import NAMESPACE_URL, uuid4, uuid5

from app.providers.base import MarketDataProvider, MarketEvent
from app.schemas.capabilities import Capability, ProviderCapabilities
from app.schemas.events import EventEnvelope, QuoteEvent


class SimulatedMarketDataProvider(MarketDataProvider):
    """Deterministic transport test feed, never a market-data substitute."""

    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled
        self._closed = False

    @property
    def capabilities(self) -> ProviderCapabilities:
        enabled_caps = frozenset({Capability.NBBO}) if self._enabled else frozenset()
        return ProviderCapabilities(
            provider="simulated",
            configured=self._enabled,
            simulated=True,
            capabilities=enabled_caps,
            public_display=frozenset(),
            notes=(
                "Development transport test source only.",
                "Values are simulated and are not valid for research or public display.",
            ),
        )

    async def stream(self, symbols: set[str]) -> AsyncIterator[MarketEvent]:
        if not self._enabled:
            raise RuntimeError("Simulated provider is disabled")

        step = 0
        while not self._closed:
            for symbol in sorted(symbols):
                now = datetime.now(UTC)
                instrument_id = uuid5(NAMESPACE_URL, f"qstream:instrument:{symbol}")
                midpoint = Decimal("100.00") + Decimal(step % 20) / Decimal("100")
                yield QuoteEvent(
                    envelope=EventEnvelope(
                        event_id=uuid4(),
                        correlation_id=uuid4(),
                        provider="simulated",
                        dataset="development-transport-test",
                        instrument_id=instrument_id,
                        sequence_number=step,
                        provider_timestamp=now,
                        received_timestamp=now,
                        processed_timestamp=now,
                        is_simulated=True,
                    ),
                    symbol=symbol,
                    bid_price=midpoint - Decimal("0.01"),
                    bid_size=Decimal("10"),
                    ask_price=midpoint + Decimal("0.01"),
                    ask_size=Decimal("12"),
                )
                step += 1
            await asyncio.sleep(1)

    async def close(self) -> None:
        self._closed = True
