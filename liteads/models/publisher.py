"""Publisher inventory and reporting models."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from liteads.models.base import Base, Status, TimestampMixin


class Publisher(Base, TimestampMixin):
    """Publisher account that owns ad inventory."""

    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=Status.ACTIVE, nullable=False)

    slots: Mapped[list["AdSlot"]] = relationship(
        "AdSlot", back_populates="publisher", cascade="all, delete-orphan", lazy="selectin"
    )
    daily_stats: Mapped[list["PublisherDailyStat"]] = relationship(
        "PublisherDailyStat", back_populates="publisher", cascade="all, delete-orphan"
    )


class AdSlot(Base, TimestampMixin):
    """A publisher placement addressable by the ad request API."""

    __tablename__ = "ad_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    publisher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("publishers.id", ondelete="CASCADE"), nullable=False
    )
    slot_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    format: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    width: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    height: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=Status.ACTIVE, nullable=False)

    publisher: Mapped[Publisher] = relationship("Publisher", back_populates="slots")


class PublisherDailyStat(Base, TimestampMixin):
    """Persisted publisher delivery and earnings aggregate for one day."""

    __tablename__ = "publisher_daily_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    publisher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("publishers.id", ondelete="CASCADE"), nullable=False
    )
    stat_date: Mapped[date] = mapped_column(Date, nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    earnings: Mapped[Decimal] = mapped_column(Numeric(12, 6), default=Decimal("0"), nullable=False)

    publisher: Mapped[Publisher] = relationship("Publisher", back_populates="daily_stats")
