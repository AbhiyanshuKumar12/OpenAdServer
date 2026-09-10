import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import type { Role } from "../types";
import {
  LayoutDashboard,
  Users,
  Target,
  Globe,
  Wrench,
  Activity,
  LogOut,
  Layers,
  PlusCircle,
  Code,
  ShieldAlert
} from "lucide-react";

interface NavItem {
  to: string;
  label: string;
  icon: React.ElementType;
}

const NAV: Record<Role, NavItem[]> = {
  admin: [
    { to: "/admin", label: "Overview", icon: LayoutDashboard },
    { to: "/admin/advertisers", label: "Advertisers", icon: Users },
    { to: "/admin/campaigns", label: "Campaigns", icon: Target },
    { to: "/admin/publishers", label: "Publishers", icon: Globe },
  ],
  advertiser: [
    { to: "/advertiser", label: "Dashboard", icon: LayoutDashboard },
    { to: "/advertiser/campaigns/new", label: "New Campaign", icon: PlusCircle },
  ],
  publisher: [
    { to: "/publisher", label: "Dashboard", icon: LayoutDashboard },
    { to: "/publisher/integration", label: "Integration", icon: Code },
  ],
};

const SHARED: NavItem[] = [
  { to: "/tools", label: "Ad Tester", icon: Wrench },
  { to: "/health", label: "System Health", icon: Activity },
];

const ROLE_LABEL: Record<Role, string> = {
  admin: "Platform Admin",
  advertiser: "Advertiser Console",
  publisher: "Publisher Portal",
};

export default function Layout() {
  const { session, logout } = useAuth();
  const navigate = useNavigate();

  if (!session) return null;
  const { user } = session;

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Layers size={20} />
          </div>
          <span>OpenAdServer</span>
        </div>
        <nav>
          {NAV[user.role].map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/admin" || item.to === "/advertiser" || item.to === "/publisher"}
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <Icon />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
          <div className="nav-section">Tools & System</div>
          {SHARED.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <Icon />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <div className="main">
        <header className="topbar">
          <div className="muted">
            <span className="role-pill">{ROLE_LABEL[user.role]}</span>
          </div>
          <div className="actions">
            <div className="user-profile">
              <div className="user-avatar">{user.name.charAt(0).toUpperCase()}</div>
              <span>{user.name}</span>
            </div>
            <button
              className="btn secondary small"
              onClick={() => {
                logout();
                navigate("/login");
              }}
            >
              <LogOut size={14} />
              <span>Log out</span>
            </button>
          </div>
        </header>

        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
