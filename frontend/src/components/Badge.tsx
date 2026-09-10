import { STATUS } from "../types";
export default function Badge({ status }: { status: number }) { const label = STATUS[status] ?? "unknown"; return <span className={`badge ${label}`}>{label}</span>; }
