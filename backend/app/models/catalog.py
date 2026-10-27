from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Sector(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sectors"

    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    classification_system: Mapped[str] = mapped_column(String(32), default="GICS")


class Industry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "industries"
    __table_args__ = (UniqueConstraint("sector_id", "code", name="uq_industries_sector_code"),)

    sector_id: Mapped[UUID] = mapped_column(ForeignKey("sectors.id"), index=True)
    code: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    classification_system: Mapped[str] = mapped_column(String(32), default="GICS")


class Company(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "companies"

    instrument_id: Mapped[UUID] = mapped_column(
        ForeignKey("instruments.id"), unique=True, index=True
    )
    legal_name: Mapped[str] = mapped_column(String(255))
    sector_id: Mapped[UUID | None] = mapped_column(ForeignKey("sectors.id"), index=True)
    industry_id: Mapped[UUID | None] = mapped_column(ForeignKey("industries.id"), index=True)
    metadata_: Mapped[dict[str, object]] = mapped_column("metadata", JSONB, default=dict)


class InstrumentClassificationMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Point-in-time sector, industry, and ETF membership."""

    __tablename__ = "instrument_classification_memberships"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id",
            "membership_type",
            "classification_id",
            "valid_from",
            name="uq_membership_period_start",
        ),
    )

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    membership_type: Mapped[str] = mapped_column(String(32), index=True)
    classification_id: Mapped[UUID] = mapped_column(index=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(64))


class CorporateAction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "corporate_actions"
    __table_args__ = (
        UniqueConstraint(
            "provider", "provider_action_id", name="uq_corporate_actions_provider_action"
        ),
    )

    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    action_type: Mapped[str] = mapped_column(String(32), index=True)
    ex_date: Mapped[date] = mapped_column(Date, index=True)
    effective_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ratio: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    cash_amount: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    provider: Mapped[str] = mapped_column(String(64))
    provider_action_id: Mapped[str] = mapped_column(String(128))
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
