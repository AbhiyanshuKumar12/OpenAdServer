import { Navigate, Outlet, useLocation } from "react-router-dom";
import { roleHome, useAuth } from "../auth/AuthContext";
import type { Role } from "../types";
export default function RequireRole({ roles }: { roles?: Role[] }) { const { session } = useAuth(); const location = useLocation(); if (!session) return <Navigate to="/login" replace state={{ from: location.pathname }} />; if (roles && !roles.includes(session.user.role)) return <Navigate to={roleHome(session.user.role)} replace />; return <Outlet />; }
