import { useEffect, useState } from "react";
import { getHealth } from "../../api/client";
import { listAdvertisers, listCampaigns, listPublishers } from "../../api/mock";
import StatCard from "../../components/StatCard";
import { money, num } from "../../lib/format";
import type { HealthResponse } from "../../types";
import { LayoutDashboard, Activity, CheckCircle2, XCircle } from "lucide-react";

export default function AdminDashboard() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    advertisers: 0,
    campaigns: 0,
    active: 0,
    impressions: 0,
    spend: 0,
    publishers: 0,
  });

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch((e) => setHealthError(e instanceof Error ? e.message : "unreachable"));

    Promise.all([listAdvertisers(), listCampaigns(), listPublishers()]).then(
      ([advertisers, campaigns, publishers]) =>
        setStats({
          advertisers: advertisers.length,
          campaigns: campaigns.length,
          active: campaigns.filter((c) => c.status === 1).length,
          impressions: campaigns.reduce((s, c) => s + c.impressions, 0),
          spend: campaigns.reduce((s, c) => s + c.spent_total, 0),
          publishers: publishers.length,
        })
    );
  }, []);

  return (
    <div>
      <h1>
        <LayoutDashboard size={24} color="#3b82f6" />
        <span>Platform Overview</span>
      </h1>

      <div className="grid cards">
        <StatCard title="Advertisers" value={num(stats.advertisers)} />
        <StatCard
          title="Campaigns"
          value={`${num(stats.active)} / ${num(stats.campaigns)}`}
          hint="active / total"
        />
        <StatCard title="Impressions" value={num(stats.impressions)} />
        <StatCard title="Total Spend" value={money(stats.spend)} />
        <StatCard title="Publishers" value={num(stats.publishers)} />
      </div>

      <div className="card">
        <h2 style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Activity size={18} color="#3b82f6" />
          <span>Backend Health</span>
        </h2>
        {healthError && (
          <div className="error">
            Could not reach the ad server: {healthError}. Is it running on port 8000?
          </div>
        )}
        {health && (
          <div className="table-wrapper">
            <table className="table">
              <tbody>
                <tr>
                  <td style={{ fontWeight: 600, color: "#64748b" }}>Status</td>
                  <td>
                    <span className="badge active">{health.status}</span>
                  </td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: "#64748b" }}>Version</td>
                  <td>
                    <code>{health.version}</code>
                  </td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: "#64748b" }}>PostgreSQL Database</td>
                  <td>
                    {health.database ? (
                      <span style={{ color: "#16a34a", display: "inline-flex", alignItems: "center", gap: 6, fontWeight: 600 }}>
                        <CheckCircle2 size={16} /> Connected
                      </span>
                    ) : (
                      <span style={{ color: "#dc2626", display: "inline-flex", alignItems: "center", gap: 6, fontWeight: 600 }}>
                        <XCircle size={16} /> Down
                      </span>
                    )}
                  </td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: "#64748b" }}>Redis Cache</td>
                  <td>
                    {health.redis ? (
                      <span style={{ color: "#16a34a", display: "inline-flex", alignItems: "center", gap: 6, fontWeight: 600 }}>
                        <CheckCircle2 size={16} /> Connected
                      </span>
                    ) : (
                      <span style={{ color: "#dc2626", display: "inline-flex", alignItems: "center", gap: 6, fontWeight: 600 }}>
                        <XCircle size={16} /> Down
                      </span>
                    )}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
        {!health && !healthError && <p className="muted">Checking health status...</p>}
      </div>
    </div>
  );
}
