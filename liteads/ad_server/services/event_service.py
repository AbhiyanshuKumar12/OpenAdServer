"""
Event tracking service.

Handles recording ad events (impressions, clicks, conversions).
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from liteads.common.cache import CacheKeys, redis_client
from liteads.common.logger import get_logger
from liteads.common.utils import current_date, current_hour
from liteads.models import AdEvent, AdSlot, Campaign, Creative, EventType, PublisherDailyStat

logger = get_logger(__name__)


class EventService:
    """Event tracking service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def track_event(
        self,
        request_id: str,
        ad_id: str,
        event_type: str,
        user_id: str | None = None,
        timestamp: int | None = None,
        extra: dict[str, Any] | None = None,
    ) -> bool:
        """
        Track an ad event.

        Events are:
        1. Persisted to database for billing/reporting
        2. Cached in Redis for real-time stats
        3. Used for frequency control updates
        """
        try:
            # Parse ad ID to get campaign/creative IDs
            campaign_id, creative_id = self._parse_ad_id(ad_id)

            # Convert event type
            event_type_enum = self._get_event_type(event_type)
            if event_type_enum is None:
                logger.warning(f"Unknown event type: {event_type}")
                return False

            # Create event record
            campaign = await self.session.get(Campaign, campaign_id) if campaign_id else None
            cost = self._calculate_cost(event_type_enum, campaign)
            event = AdEvent(
                request_id=request_id,
                campaign_id=campaign_id,
                creative_id=creative_id,
                event_type=event_type_enum,
                event_time=datetime.fromtimestamp(timestamp, tz=timezone.utc)
                if timestamp
                else datetime.now(timezone.utc),
                user_id=user_id,
                cost=cost,
            )

            self.session.add(event)
            await self.session.flush()

            await self._update_campaign_stats(campaign, creative_id, event_type_enum)
            await self._update_publisher_stats(event_type_enum, cost, extra)

            # Update real-time stats in Redis
            await self._update_stats(campaign_id, event_type_enum)

            # Update frequency counter for impressions
            if event_type_enum == EventType.IMPRESSION and user_id:
                await self._update_frequency(user_id, campaign_id)

            logger.info(
                "Event tracked",
                event_id=event.id,
                campaign_id=campaign_id,
            )

            return True

        except Exception as e:
            logger.error(f"Failed to track event: {e}")
            return False

    def _parse_ad_id(self, ad_id: str) -> tuple[int | None, int | None]:
        """Parse ad ID to extract campaign and creative IDs."""
        # Expected format: ad_{campaign_id}_{creative_id}
        try:
            parts = ad_id.split("_")
            if len(parts) >= 3:
                return int(parts[1]), int(parts[2])
            elif len(parts) >= 2:
                return int(parts[1]), None
            else:
                return int(ad_id), None
        except (ValueError, IndexError):
            logger.warning(f"Invalid ad_id format: {ad_id}")
            return None, None

    def _get_event_type(self, event_type: str) -> int | None:
        """Convert event type string to enum."""
        mapping = {
            "impression": EventType.IMPRESSION,
            "imp": EventType.IMPRESSION,
            "click": EventType.CLICK,
            "clk": EventType.CLICK,
            "conversion": EventType.CONVERSION,
            "conv": EventType.CONVERSION,
        }
        return mapping.get(event_type.lower())

    def _calculate_cost(self, event_type: int, campaign: Campaign | None) -> Decimal:
        """Calculate cost for the event."""
        if campaign is None:
            return Decimal("0.000000")
        if campaign.bid_type == 1 and event_type == EventType.IMPRESSION:
            return Decimal(campaign.bid_amount) / Decimal("1000")
        if campaign.bid_type == 2 and event_type == EventType.CLICK:
            return Decimal(campaign.bid_amount)
        if campaign.bid_type == 3 and event_type == EventType.CONVERSION:
            return Decimal(campaign.bid_amount)
        return Decimal("0.000000")

    async def _update_campaign_stats(
        self,
        campaign: Campaign | None,
        creative_id: int | None,
        event_type: int,
    ) -> None:
        """Update cached campaign and creative counters."""
        if campaign is None:
            return
        if event_type == EventType.IMPRESSION:
            campaign.impressions += 1
        elif event_type == EventType.CLICK:
            campaign.clicks += 1
        elif event_type == EventType.CONVERSION:
            campaign.conversions += 1
        if creative_id:
            creative = await self.session.get(Creative, creative_id)
            if creative:
                if event_type == EventType.IMPRESSION:
                    creative.impressions += 1
                elif event_type == EventType.CLICK:
                    creative.clicks += 1
                elif event_type == EventType.CONVERSION:
                    creative.conversions += 1

    async def _update_publisher_stats(
        self,
        event_type: int,
        cost: Decimal,
        extra: dict[str, Any] | None,
    ) -> None:
        """Attribute tracked delivery to a slot and persist publisher earnings."""
        slot_id = extra.get("slot_id") if extra else None
        if not slot_id:
            return
        result = await self.session.execute(select(AdSlot).where(AdSlot.slot_id == slot_id))
        slot = result.scalar_one_or_none()
        if slot is None:
            return
        stat_date = datetime.now(timezone.utc).date()
        result = await self.session.execute(
            select(PublisherDailyStat).where(
                PublisherDailyStat.publisher_id == slot.publisher_id,
                PublisherDailyStat.stat_date == stat_date,
            )
        )
        stat = result.scalar_one_or_none()
        if stat is None:
            stat = PublisherDailyStat(publisher_id=slot.publisher_id, stat_date=stat_date)
            self.session.add(stat)
        if event_type == EventType.IMPRESSION:
            stat.impressions += 1
        elif event_type == EventType.CLICK:
            stat.clicks += 1
        elif event_type == EventType.CONVERSION:
            stat.conversions += 1
        stat.earnings += cost * Decimal("0.70")

    async def _update_stats(self, campaign_id: int | None, event_type: int) -> None:
        """Update real-time statistics in Redis."""
        if campaign_id is None:
            return

        hour = current_hour()
        key = CacheKeys.stat_hourly(campaign_id, hour)

        # Increment appropriate counter
        if event_type == EventType.IMPRESSION:
            await redis_client.hincrby(key, "impressions", 1)
        elif event_type == EventType.CLICK:
            await redis_client.hincrby(key, "clicks", 1)
        elif event_type == EventType.CONVERSION:
            await redis_client.hincrby(key, "conversions", 1)

        # Set TTL (48 hours)
        await redis_client.expire(key, 48 * 3600)

    async def _update_frequency(self, user_id: str, campaign_id: int | None) -> None:
        """Update frequency counter."""
        if campaign_id is None:
            return

        today = current_date()
        hour = current_hour()

        # Update daily counter
        daily_key = CacheKeys.freq_daily(user_id, campaign_id, today)
        await redis_client.incr(daily_key)
        await redis_client.expire(daily_key, 24 * 3600)

        # Update hourly counter
        hourly_key = CacheKeys.freq_hourly(user_id, campaign_id, hour)
        await redis_client.incr(hourly_key)
        await redis_client.expire(hourly_key, 3600)
