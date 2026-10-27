from app.services.instruments import InstrumentSearchService


def test_exact_symbol_ranks_first() -> None:
    results = InstrumentSearchService().search("nvda")
    assert results[0].symbol == "NVDA"


def test_search_by_industry() -> None:
    results = InstrumentSearchService().search("semiconductor")
    assert {item.symbol for item in results} >= {"NVDA", "AMD", "SOXX"}


def test_empty_search_is_bounded() -> None:
    results = InstrumentSearchService().search("", limit=3)
    assert len(results) == 3
