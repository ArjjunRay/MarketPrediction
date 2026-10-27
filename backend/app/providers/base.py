from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.schemas.capabilities import ProviderCapabilities
from app.schemas.events import QuoteEvent, TradeEvent

MarketEvent = QuoteEvent | TradeEvent


class MarketDataProvider(ABC):
    """Boundary for live provider integrations.

    Implementations own authentication, wire protocols, and vendor symbology.
    Consumers receive only normalized internal events.
    """

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        raise NotImplementedError

    @abstractmethod
    def stream(self, symbols: set[str]) -> AsyncIterator[MarketEvent]:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


class HistoricalDataProvider(ABC):
    @abstractmethod
    async def backfill(self, symbols: set[str], start_iso: str, end_iso: str) -> str:
        """Return a manifest identifier for a completed immutable backfill."""
        raise NotImplementedError


class NewsProvider(ABC):
    @abstractmethod
    def stream_news(self, symbols: set[str]) -> AsyncIterator[dict[str, object]]:
        raise NotImplementedError


class ReferenceDataProvider(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[dict[str, object]]:
        raise NotImplementedError


class FundamentalDataProvider(ABC):
    """Boundary for official company facts and filing-event sources."""

    @abstractmethod
    async def company_facts(self, cik: str) -> dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    async def company_submissions(self, cik: str) -> dict[str, object]:
        raise NotImplementedError


class MacroDataProvider(ABC):
    """Boundary for public economic and rates data."""

    @abstractmethod
    async def series(
        self, series_ids: tuple[str, ...], start_year: int | None, end_year: int | None
    ) -> dict[str, object]:
        raise NotImplementedError
