import type { AdListResponse, AdRequestPayload, HealthResponse } from "../types";
const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "";
export class ApiError extends Error { constructor(message: string, public status: number) { super(message); this.name = "ApiError"; } }
async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { headers: { "Content-Type": "application/json", ...(options.headers ?? {}) }, ...options });
  if (!res.ok) { let message = `Request failed (${res.status})`; try { const body = await res.json() as { message?: string }; if (body.message) message = body.message; } catch { /* non-json error */ } throw new ApiError(message, res.status); }
  return await res.json() as T;
}
export const getHealth = () => apiFetch<HealthResponse>("/health");
export const ping = () => apiFetch<{ pong: boolean }>("/ping");
export const requestAds = (payload: AdRequestPayload) => apiFetch<AdListResponse>("/api/v1/ad/request", { method: "POST", body: JSON.stringify(payload) });
export const trackEvent = (payload: { request_id: string; ad_id: string; event_type: string }) => apiFetch<{ success: boolean }>("/api/v1/event/track", { method: "POST", body: JSON.stringify(payload) });
