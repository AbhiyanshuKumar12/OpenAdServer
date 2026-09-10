import { useState, type FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { roleHome, useAuth } from "../auth/AuthContext";
import { Layers, ArrowRight, ShieldCheck, UserCheck, GlobeCheck } from "lucide-react";

const DEMO_ACCOUNTS = [
  { label: "Platform Admin", email: "admin@openadserver.dev", password: "admin123", icon: ShieldCheck },
  { label: "Advertiser", email: "advertiser@openadserver.dev", password: "ad1234", icon: UserCheck },
  { label: "Publisher", email: "publisher@openadserver.dev", password: "pub1234", icon: GlobeCheck },
];

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(DEMO_ACCOUNTS[0].email);
  const [password, setPassword] = useState(DEMO_ACCOUNTS[0].password);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const session = await login(email, password);
      const from = (location.state as { from?: string } | null)?.from;
      navigate(from && from !== "/login" ? from : roleHome(session.user.role), { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 16 }}>
          <div className="brand-icon" style={{ width: 44, height: 44, borderRadius: 14 }}>
            <Layers size={26} />
          </div>
        </div>
        <h1>OpenAdServer</h1>
        <p className="login-subtitle">Sign in to manage campaigns, creatives and placements.</p>

        <div style={{ marginBottom: 20 }}>
          <label style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "0.06em", color: "#64748b", fontWeight: 700 }}>
            Select Demo Account
          </label>
          <div className="demo-accounts">
            {DEMO_ACCOUNTS.map((account) => {
              const Icon = account.icon;
              return (
                <button
                  key={account.email}
                  type="button"
                  onClick={() => {
                    setEmail(account.email);
                    setPassword(account.password);
                  }}
                  style={{
                    borderColor: email === account.email ? "#3b82f6" : undefined,
                    backgroundColor: email === account.email ? "#eff6ff" : undefined,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <Icon size={18} color={email === account.email ? "#2563eb" : "#64748b"} />
                    <div>
                      <b style={{ color: email === account.email ? "#1d4ed8" : "inherit" }}>{account.label}</b>
                      <br />
                      <span className="muted" style={{ fontSize: 12 }}>{account.email}</span>
                    </div>
                  </div>
                  <ArrowRight size={14} color={email === account.email ? "#2563eb" : "#cbd5e1"} />
                </button>
              );
            })}
          </div>
        </div>

        <form onSubmit={submit}>
          <div className="field">
            <label>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button className="btn" style={{ width: "100%", marginTop: 8 }} disabled={busy}>
            {busy ? "Signing in..." : "Sign in to Dashboard"}
          </button>
        </form>
      </div>
    </div>
  );
}
