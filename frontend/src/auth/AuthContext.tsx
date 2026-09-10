import { createContext, useContext, useState, type ReactNode } from "react";
import { login as apiLogin } from "../api/client";
import type { Role, Session } from "../types";
interface AuthValue { session: Session | null; login: (email: string, password: string) => Promise<Session>; logout: () => void; }
const STORAGE_KEY = "oas_session";
const AuthContext = createContext<AuthValue | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) { const [session, setSession] = useState<Session | null>(() => { try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) as Session : null; } catch { return null; } }); const login = async (email: string, password: string) => { const next = await apiLogin(email, password); localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); setSession(next); return next; }; const logout = () => { localStorage.removeItem(STORAGE_KEY); setSession(null); }; return <AuthContext.Provider value={{ session, login, logout }}>{children}</AuthContext.Provider>; }
export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error("useAuth must be used inside AuthProvider"); return value; }
export function roleHome(role: Role) { return role === "admin" ? "/admin" : role === "advertiser" ? "/advertiser" : "/publisher"; }
