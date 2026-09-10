"""CRUD and publisher reporting endpoints."""

from datetime import date, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from liteads.common.database import get_session
from liteads.models import AdSlot, Advertiser, Campaign, Creative, Publisher, PublisherDailyStat
from liteads.schemas.management import (
    AdvertiserCreate,
    AdvertiserResponse,
    AdvertiserUpdate,
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate,
    CreativeCreate,
    CreativeResponse,
    CreativeUpdate,
    PublisherCreate,
    PublisherReportingResponse,
    PublisherResponse,
    PublisherUpdate,
    SlotCreate,
    SlotResponse,
    SlotUpdate,
)

router = APIRouter()


def _not_found(entity: str, entity_id: int) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} {entity_id} not found")


@router.get("/advertiser", response_model=list[AdvertiserResponse])
async def list_advertisers(session: AsyncSession = Depends(get_session)) -> list[Advertiser]:
    result = await session.execute(select(Advertiser).order_by(Advertiser.id))
    return list(result.scalars().all())


@router.post("/advertiser", response_model=AdvertiserResponse, status_code=status.HTTP_201_CREATED)
async def create_advertiser(
    payload: AdvertiserCreate, session: AsyncSession = Depends(get_session)
) -> Advertiser:
    advertiser = Advertiser(**payload.model_dump())
    session.add(advertiser)
    await session.flush()
    return advertiser


@router.get("/advertiser/{advertiser_id}", response_model=AdvertiserResponse)
async def get_advertiser(advertiser_id: int, session: AsyncSession = Depends(get_session)) -> Advertiser:
    advertiser = await session.get(Advertiser, advertiser_id)
    if advertiser is None:
        raise _not_found("Advertiser", advertiser_id)
    return advertiser


@router.patch("/advertiser/{advertiser_id}", response_model=AdvertiserResponse)
async def update_advertiser(
    advertiser_id: int,
    payload: AdvertiserUpdate,
    session: AsyncSession = Depends(get_session),
) -> Advertiser:
    advertiser = await session.get(Advertiser, advertiser_id)
    if advertiser is None:
        raise _not_found("Advertiser", advertiser_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(advertiser, key, value)
    await session.flush()
    return advertiser


@router.get("/campaign", response_model=list[CampaignResponse])
async def list_campaigns(
    advertiser_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[Campaign]:
    query = select(Campaign).order_by(Campaign.id)
    if advertiser_id is not None:
        query = query.where(Campaign.advertiser_id == advertiser_id)
    result = await session.execute(query)
    return list(result.scalars().all())


@router.post("/campaign", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    payload: CampaignCreate, session: AsyncSession = Depends(get_session)
) -> Campaign:
    if await session.get(Advertiser, payload.advertiser_id) is None:
        raise _not_found("Advertiser", payload.advertiser_id)
    campaign = Campaign(**payload.model_dump())
    session.add(campaign)
    await session.flush()
    return campaign


@router.get("/campaign/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int, session: AsyncSession = Depends(get_session)) -> Campaign:
    campaign = await session.get(Campaign, campaign_id)
    if campaign is None:
        raise _not_found("Campaign", campaign_id)
    return campaign


@router.patch("/campaign/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    payload: CampaignUpdate,
    session: AsyncSession = Depends(get_session),
) -> Campaign:
    campaign = await session.get(Campaign, campaign_id)
    if campaign is None:
        raise _not_found("Campaign", campaign_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(campaign, key, value)
    await session.flush()
    return campaign


@router.get("/creative", response_model=list[CreativeResponse])
async def list_creatives(
    campaign_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[Creative]:
    query = select(Creative).order_by(Creative.id)
    if campaign_id is not None:
        query = query.where(Creative.campaign_id == campaign_id)
    result = await session.execute(query)
    return list(result.scalars().all())


@router.post("/creative", response_model=CreativeResponse, status_code=status.HTTP_201_CREATED)
async def create_creative(
    payload: CreativeCreate, session: AsyncSession = Depends(get_session)
) -> Creative:
    if await session.get(Campaign, payload.campaign_id) is None:
        raise _not_found("Campaign", payload.campaign_id)
    creative = Creative(**payload.model_dump())
    session.add(creative)
    await session.flush()
    return creative


@router.get("/creative/{creative_id}", response_model=CreativeResponse)
async def get_creative(creative_id: int, session: AsyncSession = Depends(get_session)) -> Creative:
    creative = await session.get(Creative, creative_id)
    if creative is None:
        raise _not_found("Creative", creative_id)
    return creative


@router.patch("/creative/{creative_id}", response_model=CreativeResponse)
async def update_creative(
    creative_id: int,
    payload: CreativeUpdate,
    session: AsyncSession = Depends(get_session),
) -> Creative:
    creative = await session.get(Creative, creative_id)
    if creative is None:
        raise _not_found("Creative", creative_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(creative, key, value)
    await session.flush()
    return creative


@router.get("/publisher", response_model=list[PublisherResponse])
async def list_publishers(session: AsyncSession = Depends(get_session)) -> list[Publisher]:
    result = await session.execute(select(Publisher).order_by(Publisher.id))
    return list(result.scalars().all())


@router.post("/publisher", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def create_publisher(
    payload: PublisherCreate, session: AsyncSession = Depends(get_session)
) -> Publisher:
    publisher = Publisher(**payload.model_dump())
    session.add(publisher)
    await session.flush()
    return publisher


@router.get("/publisher/{publisher_id}", response_model=PublisherResponse)
async def get_publisher(publisher_id: int, session: AsyncSession = Depends(get_session)) -> Publisher:
    publisher = await session.get(Publisher, publisher_id)
    if publisher is None:
        raise _not_found("Publisher", publisher_id)
    return publisher


@router.patch("/publisher/{publisher_id}", response_model=PublisherResponse)
async def update_publisher(
    publisher_id: int,
    payload: PublisherUpdate,
    session: AsyncSession = Depends(get_session),
) -> Publisher:
    publisher = await session.get(Publisher, publisher_id)
    if publisher is None:
        raise _not_found("Publisher", publisher_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(publisher, key, value)
    await session.flush()
    return publisher


@router.get("/slot", response_model=list[SlotResponse])
async def list_slots(
    publisher_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AdSlot]:
    query = select(AdSlot).order_by(AdSlot.id)
    if publisher_id is not None:
        query = query.where(AdSlot.publisher_id == publisher_id)
    result = await session.execute(query)
    return list(result.scalars().all())


@router.post("/slot", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
async def create_slot(payload: SlotCreate, session: AsyncSession = Depends(get_session)) -> AdSlot:
    if await session.get(Publisher, payload.publisher_id) is None:
        raise _not_found("Publisher", payload.publisher_id)
    slot = AdSlot(**payload.model_dump())
    session.add(slot)
    await session.flush()
    return slot


@router.get("/slot/{slot_id}", response_model=SlotResponse)
async def get_slot(slot_id: int, session: AsyncSession = Depends(get_session)) -> AdSlot:
    slot = await session.get(AdSlot, slot_id)
    if slot is None:
        raise _not_found("Slot", slot_id)
    return slot


@router.patch("/slot/{slot_id}", response_model=SlotResponse)
async def update_slot(
    slot_id: int, payload: SlotUpdate, session: AsyncSession = Depends(get_session)
) -> AdSlot:
    slot = await session.get(AdSlot, slot_id)
    if slot is None:
        raise _not_found("Slot", slot_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(slot, key, value)
    await session.flush()
    return slot


@router.get("/publisher/{publisher_id}/reporting", response_model=PublisherReportingResponse)
async def publisher_reporting(
    publisher_id: int,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> PublisherReportingResponse:
    if await session.get(Publisher, publisher_id) is None:
        raise _not_found("Publisher", publisher_id)
    today = date.today()
    start = start_date or today
    end = end_date or today
    if end < start:
        raise HTTPException(status_code=422, detail="end_date must be on or after start_date")
    result = await session.execute(
        select(
            func.coalesce(func.sum(PublisherDailyStat.impressions), 0),
            func.coalesce(func.sum(PublisherDailyStat.clicks), 0),
            func.coalesce(func.sum(PublisherDailyStat.conversions), 0),
            func.coalesce(func.sum(PublisherDailyStat.earnings), Decimal("0")),
        ).where(
            PublisherDailyStat.publisher_id == publisher_id,
            PublisherDailyStat.stat_date >= start,
            PublisherDailyStat.stat_date <= end,
        )
    )
    impressions, clicks, conversions, earnings = result.one()
    earnings = Decimal(earnings or 0)
    ecpm = (earnings / Decimal(impressions) * Decimal(1000)) if impressions else Decimal("0")
    return PublisherReportingResponse(
        publisher_id=publisher_id,
        start_date=start,
        end_date=end,
        impressions=int(impressions),
        clicks=int(clicks),
        conversions=int(conversions),
        earnings=earnings,
        ecpm=ecpm,
    )
