from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Instrument(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "instruments"

    symbol: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    exchange: Mapped[str | None] = mapped_column(String(64))
    sector: Mapped[str | None] = mapped_column(String(128), index=True)
    industry: Mapped[str | None] = mapped_column(String(128), index=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    asset_class: Mapped[str] = mapped_column(String(32), index=True)
    provider_identifiers: Mapped[dict[str, str]] = mapped_column(JSONB, default=dict)


class Quote(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "quotes"
    __table_args__ = (Index("ix_quotes_instrument_event_time", "instrument_id", "event_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    received_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    bid_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    bid_size: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    ask_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    ask_size: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    sequence_number: Mapped[int | None] = mapped_column(BigInteger)
    provider: Mapped[str] = mapped_column(String(64), index=True)
    dataset: Mapped[str] = mapped_column(String(128))
    quality_flags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    is_simulated: Mapped[bool] = mapped_column(default=False)


class Trade(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "trades"
    __table_args__ = (Index("ix_trades_instrument_event_time", "instrument_id", "event_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    received_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    size: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    exchange: Mapped[str | None] = mapped_column(String(32))
    sequence_number: Mapped[int | None] = mapped_column(BigInteger)
    provider: Mapped[str] = mapped_column(String(64), index=True)
    dataset: Mapped[str] = mapped_column(String(128))
    conditions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    quality_flags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    is_simulated: Mapped[bool] = mapped_column(default=False)


class MarketTick(UUIDPrimaryKeyMixin, Base):
    """Normalized event index; full typed payloads remain in their dedicated tables."""

    __tablename__ = "market_ticks"
    __table_args__ = (
        Index("ix_market_ticks_instrument_event_time", "instrument_id", "event_time"),
    )

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    event_id: Mapped[UUID] = mapped_column(index=True)
    event_type: Mapped[str] = mapped_column(String(32), index=True)
    provider: Mapped[str] = mapped_column(String(64), index=True)
    dataset: Mapped[str] = mapped_column(String(128))
    sequence_number: Mapped[int | None] = mapped_column(BigInteger)
    quality_flags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    is_simulated: Mapped[bool] = mapped_column(default=False)
