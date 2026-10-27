from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AggregatedBar(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "aggregated_bars"
    __table_args__ = (
        Index(
            "ix_bars_instrument_interval_start",
            "instrument_id",
            "interval",
            "start_time",
            unique=True,
        ),
    )

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    interval: Mapped[str] = mapped_column(String(16))
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    open: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    high: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    low: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    close: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    volume: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    vwap: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    trade_count: Mapped[int | None] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(64))
    is_simulated: Mapped[bool] = mapped_column(default=False)


class OrderBookSnapshot(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "order_book_snapshots"
    __table_args__ = (Index("ix_book_instrument_event_time", "instrument_id", "event_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    depth: Mapped[int] = mapped_column(Integer)
    book_type: Mapped[str] = mapped_column(String(16))
    bids: Mapped[list[dict[str, object]]] = mapped_column(JSONB)
    asks: Mapped[list[dict[str, object]]] = mapped_column(JSONB)
    provider: Mapped[str] = mapped_column(String(64))
    dataset: Mapped[str] = mapped_column(String(128))
    is_simulated: Mapped[bool] = mapped_column(default=False)


class OrderBookEvent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "order_book_events"
    __table_args__ = (Index("ix_book_events_instrument_event_time", "instrument_id", "event_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    side: Mapped[str] = mapped_column(String(4))
    action: Mapped[str] = mapped_column(String(16))
    price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    size: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    order_id: Mapped[str | None] = mapped_column(String(128), index=True)
    sequence_number: Mapped[int | None] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(64), index=True)
    dataset: Mapped[str] = mapped_column(String(128))
    quality_flags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    is_simulated: Mapped[bool] = mapped_column(default=False)


class NewsEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "news_events"
    __table_args__ = (Index("ix_news_provider_published", "provider", "published_at"),)

    provider: Mapped[str] = mapped_column(String(64))
    provider_event_id: Mapped[str] = mapped_column(String(128))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    headline: Mapped[str] = mapped_column(String(1024))
    summary: Mapped[str | None] = mapped_column(String(4096))
    source: Mapped[str | None] = mapped_column(String(255))
    symbols: Mapped[list[str]] = mapped_column(JSONB, default=list)
    entities: Mapped[list[dict[str, object]]] = mapped_column(JSONB, default=list)
    classifications: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
    redistribution_allowed: Mapped[bool] = mapped_column(default=False)


class ModelMetric(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "model_metrics"

    model_version_id: Mapped[UUID] = mapped_column(ForeignKey("model_versions.id"), index=True)
    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    metric_name: Mapped[str] = mapped_column(String(64), index=True)
    metric_value: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    dimensions: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class RegimeState(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "regime_states"

    instrument_id: Mapped[UUID | None] = mapped_column(ForeignKey("instruments.id"), index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    regime: Mapped[str] = mapped_column(String(64), index=True)
    model_version: Mapped[str] = mapped_column(String(64))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(10, 8))
    evidence: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class DriftEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "drift_events"

    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    feature_name: Mapped[str | None] = mapped_column(String(128), index=True)
    drift_type: Mapped[str] = mapped_column(String(32), index=True)
    severity: Mapped[str] = mapped_column(String(16), index=True)
    method: Mapped[str] = mapped_column(String(32))
    magnitude: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    baseline_window: Mapped[dict[str, object]] = mapped_column(JSONB)
    comparison_window: Mapped[dict[str, object]] = mapped_column(JSONB)


class SystemHealth(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "system_health"

    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    component: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(16), index=True)
    latency_ms: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    details: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class ProviderStatus(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "provider_status"

    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    provider: Mapped[str] = mapped_column(String(64), index=True)
    dataset: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(16), index=True)
    last_event_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    latency_ms: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    reconnect_count: Mapped[int] = mapped_column(Integer, default=0)
    details: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
