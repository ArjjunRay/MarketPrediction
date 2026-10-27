from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssetClass(StrEnum):
    EQUITY = "equity"
    ETF = "etf"
    SECTOR = "sector"


class Instrument(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    symbol: str
    name: str
    exchange: str | None
    sector: str | None
    industry: str | None
    currency: str
    asset_class: AssetClass


class InstrumentSearchResponse(BaseModel):
    query: str
    results: list[Instrument]
    source: str = "development_reference_catalog"
