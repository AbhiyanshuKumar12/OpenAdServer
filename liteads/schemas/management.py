"""Management API request and response schemas."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AdvertiserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    company: str | None = None
    contact_email: str | None = None
    balance: Decimal = Field(default=Decimal("0"), ge=0)
    daily_budget: Decimal = Field(default=Decimal("0"), ge=0)


class AdvertiserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    company: str | None = None
    contact_email: str | None = None
    balance: Decimal | None = Field(default=None, ge=0)
    daily_budget: Decimal | None = Field(default=None, ge=0)
    status: int | None = Field(default=None, ge=0, le=4)


class AdvertiserResponse(ORMModel):
    id: int
    name: str
    company: str | None
    contact_email: str | None
    balance: Decimal
    daily_budget: Decimal
    status: int
    created_at: datetime
    updated_at: datetime


class CampaignCreate(BaseModel):
    advertiser_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    budget_daily: Decimal = Field(default=Decimal("0"), ge=0)
    budget_total: Decimal = Field(default=Decimal("0"), ge=0)
    bid_type: int = Field(default=1, ge=1, le=4)
    bid_amount: Decimal = Field(default=Decimal("0"), ge=0)
    freq_cap_daily: int = Field(default=10, ge=0)
    freq_cap_hourly: int = Field(default=3, ge=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: int = Field(default=1, ge=0, le=4)


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    budget_daily: Decimal | None = Field(default=None, ge=0)
    budget_total: Decimal | None = Field(default=None, ge=0)
    bid_type: int | None = Field(default=None, ge=1, le=4)
    bid_amount: Decimal | None = Field(default=None, ge=0)
    freq_cap_daily: int | None = Field(default=None, ge=0)
    freq_cap_hourly: int | None = Field(default=None, ge=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: int | None = Field(default=None, ge=0, le=4)


class CampaignResponse(ORMModel):
    id: int
    advertiser_id: int
    name: str
    description: str | None
    budget_daily: Decimal
    budget_total: Decimal
    spent_today: Decimal
    spent_total: Decimal
    bid_type: int
    bid_amount: Decimal
    freq_cap_daily: int
    freq_cap_hourly: int
    start_time: datetime | None
    end_time: datetime | None
    status: int
    impressions: int
    clicks: int
    conversions: int
    created_at: datetime
    updated_at: datetime


class CreativeCreate(BaseModel):
    campaign_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    landing_url: str
    creative_type: int = Field(default=1, ge=1, le=4)
    width: int = Field(default=0, ge=0)
    height: int = Field(default=0, ge=0)
    status: int = Field(default=1, ge=0, le=4)
    quality_score: int = Field(default=80, ge=0, le=100)


class CreativeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    landing_url: str | None = None
    creative_type: int | None = Field(default=None, ge=1, le=4)
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    status: int | None = Field(default=None, ge=0, le=4)
    quality_score: int | None = Field(default=None, ge=0, le=100)


class CreativeResponse(ORMModel):
    id: int
    campaign_id: int
    title: str
    description: str | None
    image_url: str | None
    video_url: str | None
    landing_url: str
    creative_type: int
    width: int
    height: int
    status: int
    quality_score: int
    created_at: datetime
    updated_at: datetime


class PublisherCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: str | None = None
    site_url: str | None = None


class PublisherUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = None
    site_url: str | None = None
    status: int | None = Field(default=None, ge=0, le=4)


class PublisherResponse(ORMModel):
    id: int
    name: str
    email: str | None
    site_url: str | None
    status: int
    created_at: datetime
    updated_at: datetime


class SlotCreate(BaseModel):
    publisher_id: int = Field(gt=0)
    slot_id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    format: int = Field(default=1, ge=1, le=4)
    width: int = Field(default=0, ge=0)
    height: int = Field(default=0, ge=0)
    status: int = Field(default=1, ge=0, le=4)


class SlotUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    format: int | None = Field(default=None, ge=1, le=4)
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    status: int | None = Field(default=None, ge=0, le=4)


class SlotResponse(ORMModel):
    id: int
    publisher_id: int
    slot_id: str
    name: str
    format: int
    width: int
    height: int
    status: int
    created_at: datetime
    updated_at: datetime


class PublisherReportingResponse(BaseModel):
    publisher_id: int
    start_date: date
    end_date: date
    impressions: int
    clicks: int
    conversions: int
    earnings: Decimal
    ecpm: Decimal
