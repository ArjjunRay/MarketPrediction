from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QualityFlag(StrEnum):
    DUPLICATE = "duplicate"
    OUT_OF_ORDER = "out_of_order"
    STALE = "stale"
    INVALID_PRICE = "invalid_price"
    INVALID_SIZE = "invalid_size"
    CROSSED_MARKET = "crossed_market"
    SEQUENCE_GAP = "sequence_gap"


class EventEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: UUID
    correlation_id: UUID
    provider: str
    dataset: str
    instrument_id: UUID
    sequence_number: int | None = Field(default=None, ge=0)
    provider_timestamp: datetime
    received_timestamp: datetime
    processed_timestamp: datetime
    schema_version: int = Field(default=1, ge=1)
    quality_flags: tuple[QualityFlag, ...] = ()
    is_simulated: bool = False


class TradeEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    envelope: EventEnvelope
    symbol: str
    price: Decimal = Field(gt=0)
    size: Decimal = Field(gt=0)
    exchange: str | None = None
    conditions: tuple[str, ...] = ()


class QuoteEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    envelope: EventEnvelope
    symbol: str
    bid_price: Decimal = Field(gt=0)
    bid_size: Decimal = Field(ge=0)
    ask_price: Decimal = Field(gt=0)
    ask_size: Decimal = Field(ge=0)
    bid_exchange: str | None = None
    ask_exchange: str | None = None
