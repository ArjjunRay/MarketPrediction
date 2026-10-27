from uuid import NAMESPACE_URL, uuid5

from app.schemas.instruments import AssetClass, Instrument


def _instrument(
    symbol: str,
    name: str,
    exchange: str,
    sector: str,
    industry: str,
    asset_class: AssetClass = AssetClass.EQUITY,
) -> Instrument:
    return Instrument(
        id=uuid5(NAMESPACE_URL, f"qstream:instrument:{symbol}"),
        symbol=symbol,
        name=name,
        exchange=exchange,
        sector=sector,
        industry=industry,
        currency="USD",
        asset_class=asset_class,
    )


# Valid reference metadata for transport/search development. This is not live market data.
DEVELOPMENT_CATALOG = (
    _instrument("NVDA", "NVIDIA Corporation", "NASDAQ", "Technology", "Semiconductors"),
    _instrument("AMD", "Advanced Micro Devices, Inc.", "NASDAQ", "Technology", "Semiconductors"),
    _instrument("AAPL", "Apple Inc.", "NASDAQ", "Technology", "Consumer Electronics"),
    _instrument("MSFT", "Microsoft Corporation", "NASDAQ", "Technology", "Software"),
    _instrument("JPM", "JPMorgan Chase & Co.", "NYSE", "Financials", "Banks"),
    _instrument("XOM", "Exxon Mobil Corporation", "NYSE", "Energy", "Oil & Gas"),
    _instrument(
        "SPY",
        "SPDR S&P 500 ETF Trust",
        "NYSE Arca",
        "Broad Market",
        "Index ETF",
        AssetClass.ETF,
    ),
    _instrument("QQQ", "Invesco QQQ Trust", "NASDAQ", "Technology", "Index ETF", AssetClass.ETF),
    _instrument(
        "SOXX",
        "iShares Semiconductor ETF",
        "NASDAQ",
        "Technology",
        "Semiconductor ETF",
        AssetClass.ETF,
    ),
)


class InstrumentSearchService:
    def search(self, query: str, limit: int = 10) -> list[Instrument]:
        normalized = query.strip().casefold()
        if not normalized:
            return list(DEVELOPMENT_CATALOG[:limit])

        scored: list[tuple[int, Instrument]] = []
        for instrument in DEVELOPMENT_CATALOG:
            symbol = instrument.symbol.casefold()
            fields = " ".join(
                filter(None, (instrument.name, instrument.sector, instrument.industry))
            ).casefold()
            if symbol == normalized:
                score = 0
            elif symbol.startswith(normalized):
                score = 1
            elif normalized in fields:
                score = 2
            else:
                continue
            scored.append((score, instrument))
        scored.sort(key=lambda item: (item[0], item[1].symbol))
        return [instrument for _, instrument in scored[:limit]]
