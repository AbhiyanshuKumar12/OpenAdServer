import type { AdListResponse, AdRequestPayload, AdSlot, Advertiser, Campaign, Creative, HealthResponse, Publisher, PublisherReporting, Session } from "../types";
const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "";
export class ApiError extends Error { constructor(message: string, public status: number) { super(message); this.name = "ApiError"; } }
export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { headers: { "Content-Type": "application/json", ...(options.headers ?? {}) }, ...options });
  if (!res.ok) { let message = `Request failed (${res.status})`; try { const body = await res.json() as { message?: string }; if (body.message) message = body.message; } catch { /* non-json error */ } throw new ApiError(message, res.status); }
  return await res.json() as T;
}
export const getHealth = () => apiFetch<HealthResponse>("/health");
export const ping = () => apiFetch<{ pong: boolean }>("/ping");
export const requestAds = (payload: AdRequestPayload) => apiFetch<AdListResponse>("/api/v1/ad/request", { method: "POST", body: JSON.stringify(payload) });
export const trackEvent = (payload: { request_id: string; ad_id: string; event_type: string }) => apiFetch<{ success: boolean }>("/api/v1/event/track", { method: "POST", body: JSON.stringify(payload) });

export const login = (email: string, password: string) => apiFetch<Session>("/api/v1/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
export const listAdvertisers = () => apiFetch<Advertiser[]>("/api/v1/advertiser");
export const createAdvertiser = (input: Omit<Advertiser, "id" | "status" | "created_at" | "updated_at">) => apiFetch<Advertiser>("/api/v1/advertiser", { method: "POST", body: JSON.stringify(input) });
export const setAdvertiserStatus = (id: number, status: number) => apiFetch<Advertiser>(`/api/v1/advertiser/${id}`, { method: "PATCH", body: JSON.stringify({ status }) }).then(() => undefined);
export const listCampaigns = (advertiserId?: number) => apiFetch<Campaign[]>(`/api/v1/campaign${advertiserId ? `?advertiser_id=${advertiserId}` : ""}`);
export interface CampaignInput { name: string; description: string; budget_daily: number; budget_total: number; bid_type: number; bid_amount: number; freq_cap_daily: number; freq_cap_hourly: number; start_time?: string; end_time?: string; }
export const getCampaign = (id: number) => apiFetch<Campaign>(`/api/v1/campaign/${id}`);
export const createCampaign = (advertiserId: number, input: CampaignInput) => apiFetch<Campaign>("/api/v1/campaign", { method: "POST", body: JSON.stringify({ ...input, advertiser_id: advertiserId }) });
export const setCampaignStatus = (id: number, status: number) => apiFetch<Campaign>(`/api/v1/campaign/${id}`, { method: "PATCH", body: JSON.stringify({ status }) }).then(() => undefined);
export const listCreatives = (campaignId: number) => apiFetch<Creative[]>(`/api/v1/creative?campaign_id=${campaignId}`);
export interface CreativeInput { title: string; description: string; image_url: string; landing_url: string; creative_type: number; width: number; height: number; }
export const createCreative = (campaignId: number, input: CreativeInput) => apiFetch<Creative>("/api/v1/creative", { method: "POST", body: JSON.stringify({ ...input, campaign_id: campaignId }) });
export const listPublishers = () => apiFetch<Publisher[]>("/api/v1/publisher");
export const createPublisher = (input: Omit<Publisher, "id" | "status" | "created_at" | "updated_at">) => apiFetch<Publisher>("/api/v1/publisher", { method: "POST", body: JSON.stringify(input) });
export const listSlots = (publisherId?: number) => apiFetch<AdSlot[]>(`/api/v1/slot${publisherId ? `?publisher_id=${publisherId}` : ""}`);
export const createSlot = (publisherId: number, input: { slot_id: string; name: string; format: number; width: number; height: number }) => apiFetch<AdSlot>("/api/v1/slot", { method: "POST", body: JSON.stringify({ ...input, publisher_id: publisherId }) });
export const getPublisherReporting = (publisherId: number, startDate?: string, endDate?: string) => { const params = new URLSearchParams(); if (startDate) params.set("start_date", startDate); if (endDate) params.set("end_date", endDate); return apiFetch<PublisherReporting>(`/api/v1/publisher/${publisherId}/reporting${params.size ? `?${params}` : ""}`); };
