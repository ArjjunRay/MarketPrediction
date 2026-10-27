from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class FeatureVector(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "features"
    __table_args__ = (Index("ix_features_instrument_event_time", "instrument_id", "event_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, index=True
    )
    feature_version: Mapped[str] = mapped_column(String(64), index=True)
    values: Mapped[dict[str, object]] = mapped_column(JSONB)


class Prediction(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "predictions"
    __table_args__ = (Index("ix_predictions_instrument_time", "instrument_id", "prediction_time"),)

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    prediction_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    horizon_seconds: Mapped[int]
    feature_version: Mapped[str] = mapped_column(String(64))
    model_version: Mapped[str] = mapped_column(String(64), index=True)
    raw_probabilities: Mapped[dict[str, float]] = mapped_column(JSONB)
    calibrated_probabilities: Mapped[dict[str, float]] = mapped_column(JSONB)
    expected_return: Mapped[Decimal | None] = mapped_column(Numeric(20, 12))
    predicted_volatility: Mapped[Decimal | None] = mapped_column(Numeric(20, 12))
    uncertainty: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
    regime: Mapped[str | None] = mapped_column(String(64))


class PredictionResult(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "prediction_results"

    prediction_id: Mapped[UUID] = mapped_column(
        ForeignKey("predictions.id"), unique=True, index=True
    )
    matured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    actual_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    realized_return: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    realized_class: Mapped[str] = mapped_column(String(16))
    metrics: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class ModelVersion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "model_versions"

    name: Mapped[str] = mapped_column(String(128), index=True)
    version: Mapped[str] = mapped_column(String(64))
    state: Mapped[str] = mapped_column(String(32), index=True)
    feature_version: Mapped[str] = mapped_column(String(64))
    dataset_hash: Mapped[str] = mapped_column(String(128))
    training_manifest: Mapped[dict[str, object]] = mapped_column(JSONB)
    metrics: Mapped[dict[str, object]] = mapped_column(JSONB)
