from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    auth_subject: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), unique=True)
    display_name: Mapped[str | None] = mapped_column(String(255))
    access_mode: Mapped[str] = mapped_column(String(32), default="public")
    entitlements: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class Watchlist(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "watchlists"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(128))
    symbols: Mapped[list[str]] = mapped_column(JSONB, default=list)


class PaperAccount(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "paper_accounts"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(128))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    starting_cash: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    risk_config: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class PaperOrder(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "paper_orders"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("paper_accounts.id"), index=True)
    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    side: Mapped[str] = mapped_column(String(8))
    order_type: Mapped[str] = mapped_column(String(16))
    quantity: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    status: Mapped[str] = mapped_column(String(32), index=True)
    assumptions: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)


class PaperFill(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "paper_fills"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("paper_orders.id"), index=True)
    filled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    fee: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    slippage: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)


class PaperPosition(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "paper_positions"
    __table_args__ = (
        UniqueConstraint("account_id", "instrument_id", name="uq_paper_position_instrument"),
    )

    account_id: Mapped[UUID] = mapped_column(ForeignKey("paper_accounts.id"), index=True)
    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    average_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(24, 8), default=0)


class PaperTrade(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "paper_trades"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("paper_accounts.id"), index=True)
    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(24, 8))
    entry_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    exit_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    realized_pnl: Mapped[Decimal | None] = mapped_column(Numeric(24, 8))
    strategy_version: Mapped[str] = mapped_column(String(64))
