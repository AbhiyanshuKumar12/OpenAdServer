interface StatCardProps {
  title: string;
  value: string | number;
  hint?: string;
}

export default function StatCard({ title, value, hint }: StatCardProps) {
  return (
    <div className="stat">
      <div>
        <div className="eyebrow">{title}</div>
        <div className="stat-value">{value}</div>
      </div>
      {hint && <div className="hint">{hint}</div>}
    </div>
  );
}
