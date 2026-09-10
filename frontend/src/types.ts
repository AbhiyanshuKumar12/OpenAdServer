export type Role = "admin" | "advertiser" | "publisher";
export interface User { id: string; name: string; email: string; role: Role; }
export interface Session { user: User; token: string; }
export const BID_TYPES: Record<number, string> = { 1: "CPM", 2: "CPC", 3: "CPA" };
export const CREATIVE_TYPES: Record<number, string> = { 1: "banner", 2: "native", 3: "video", 4: "interstitial" };
export const STATUS: Record<number, string> = { 0: "paused", 1: "active" };
export interface DeviceInfo { os: string; os_version?: string; model?: string; brand?: string; screen_width?: number; screen_height?: number; language?: string; }
export interface GeoInfo { ip?: string; country?: string; region?: string; city?: string; latitude?: number; longitude?: number; }
export interface AdRequestPayload { slot_id: string; user_id?: string; device: DeviceInfo; geo?: GeoInfo; num_ads: number; }
export interface CreativeResponse { title?: string; description?: string; image_url?: string; video_url?: string; landing_url: string; width?: number; height?: number; creative_type: string; }
export interface TrackingUrls { impression_url: string; click_url: string; conversion_url?: string; }
export interface AdResponse { ad_id: string; campaign_id: number; creative_id: number; creative: CreativeResponse; tracking: TrackingUrls; metadata?: { ecpm?: number; pctr?: number } | null; }
export interface AdListResponse { request_id: string; ads: AdResponse[]; count: number; }
export interface HealthResponse { status: string; version: string; database: boolean; redis: boolean; }
export interface Advertiser { id: number; name: string; company?: string; contact_email?: string; balance: number; daily_budget: number; status: number; }
export interface Campaign { id: number; advertiser_id: number; name: string; description?: string; budget_daily: number; budget_total: number; spent_today: number; spent_total: number; bid_type: number; bid_amount: number; freq_cap_daily: number; freq_cap_hourly: number; start_time?: string; end_time?: string; status: number; impressions: number; clicks: number; conversions: number; }
export interface Creative { id: number; campaign_id: number; title: string; description?: string; image_url?: string; video_url?: string; landing_url: string; creative_type: number; width: number; height: number; status: number; quality_score: number; }
export interface Publisher { id: number; name: string; email?: string; site_url?: string; status: number; }
export interface AdSlot { id: number; publisher_id: number; slot_id: string; name: string; format: number; width: number; height: number; status: number; ecpm_today?: number; }
export interface PublisherReporting { publisher_id: number; start_date: string; end_date: string; impressions: number; clicks: number; conversions: number; earnings: number; ecpm: number; }
