import { useEffect, useState, type FormEvent } from "react";
import { createSlot, listSlots } from "../../api/mock";
import Badge from "../../components/Badge";
import StatCard from "../../components/StatCard";
import { money } from "../../lib/format";
import { CREATIVE_TYPES, type AdSlot } from "../../types";
import { LayoutGrid, PlusCircle, Layers } from "lucide-react";

const PUBLISHER_ID = 1;

export default function PublisherDashboard() {
  const [slots, setSlots] = useState<AdSlot[]>([]);
  const [form, setForm] = useState({ slot_id: "", name: "", format: "1" });

  const reload = () => listSlots(PUBLISHER_ID).then(setSlots);

  useEffect(() => {
    void reload();
  }, []);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    await createSlot(PUBLISHER_ID, {
      slot_id: form.slot_id,
      name: form.name,
      format: Number(form.format),
      width: 300,
      height: 250,
    });
    setForm({ slot_id: "", name: "", format: "1" });
    await reload();
  };

  const avg = slots.length
    ? slots.reduce((s, x) => s + (x.ecpm_today ?? 0), 0) / slots.length
    : 0;

  return (
    <div>
      <h1>
        <LayoutGrid size={24} color="#3b82f6" />
        <span>My Ad Slots</span>
      </h1>

      <div className="grid cards">
        <StatCard
          title="Active slots"
          value={`${slots.filter((s) => s.status === 1).length} / ${slots.length}`}
        />
        <StatCard title="Avg eCPM today" value={money(avg)} />
        <StatCard
          title="Est. earnings today"
          value={money(slots.reduce((s, x) => s + (x.ecpm_today ?? 0) * 12, 0))}
        />
      </div>

      <div className="card">
        <h2>Register a New Ad Slot</h2>
        <form onSubmit={submit}>
          <div className="form-grid">
            <div className="field">
              <label>Slot ID *</label>
              <input
                placeholder="e.g. sidebar-banner-01"
                value={form.slot_id}
                onChange={(e) => setForm({ ...form, slot_id: e.target.value })}
                required
              />
            </div>
            <div className="field">
              <label>Friendly Name *</label>
              <input
                placeholder="e.g. Main Sidebar Ad"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </div>
            <div className="field">
              <label>Ad Format</label>
              <select
                value={form.format}
                onChange={(e) => setForm({ ...form, format: e.target.value })}
              >
                {Object.entries(CREATIVE_TYPES).map(([v, l]) => (
                  <option key={v} value={v}>
                    {l}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button className="btn">
            <PlusCircle size={16} />
            <span>Create Slot</span>
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Registered Slots ({slots.length})</h2>
        <div className="table-wrapper">
          <table className="table">
            <thead>
              <tr>
                <th>Slot ID</th>
                <th>Name</th>
                <th>Format</th>
                <th>Size</th>
                <th>eCPM Today</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {slots.map((s) => (
                <tr key={s.id}>
                  <td>
                    <code>{s.slot_id}</code>
                  </td>
                  <td>
                    <b>{s.name}</b>
                  </td>
                  <td>{CREATIVE_TYPES[s.format]}</td>
                  <td>
                    {s.width}×{s.height}
                  </td>
                  <td>
                    <b>{money(s.ecpm_today ?? 0)}</b>
                  </td>
                  <td>
                    <Badge status={s.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
