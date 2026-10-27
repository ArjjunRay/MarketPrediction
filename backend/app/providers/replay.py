from collections.abc import AsyncIterator, Iterable

from app.providers.base import MarketDataProvider, MarketEvent
from app.schemas.capabilities import Capability, ProviderCapabilities
from app.schemas.events import QuoteEvent, TradeEvent


class ReplayMarketDataProvider(MarketDataProvider):
    """Deterministically replay normalized fixtures without claiming live data."""

    def __init__(self, events: Iterable[MarketEvent]) -> None:
        self._events = tuple(events)
        self._closed = False

    @property
    def capabilities(self) -> ProviderCapabilities:
        capabilities: set[Capability] = set()
        if any(isinstance(event, QuoteEvent) for event in self._events):
            capabilities.add(Capability.NBBO)
        if any(isinstance(event, TradeEvent) for event in self._events):
            capabilities.add(Capability.TRADES)
        return ProviderCapabilities(
            provider="replay",
            configured=bool(self._events),
            simulated=True,
            capabilities=frozenset(capabilities),
            public_display=frozenset(),
            notes=(
                "Deterministic development and test replay only.",
                "Replay events are never a public-display market source.",
            ),
        )

    async def stream(self, symbols: set[str]) -> AsyncIterator[MarketEvent]:
        if not self._events:
            raise RuntimeError("Replay provider has no events")
        allowed = {symbol.upper() for symbol in symbols}
        for event in self._events:
            if self._closed:
                return
            if event.symbol.upper() in allowed:
                yield event

    async def close(self) -> None:
        self._closed = True
