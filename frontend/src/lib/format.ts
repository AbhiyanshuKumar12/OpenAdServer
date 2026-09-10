export const money = (n: number) => `$${n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
export const num = (n: number) => n.toLocaleString("en-US");
export const ctr = (clicks: number, impressions: number) => impressions > 0 ? `${((clicks / impressions) * 100).toFixed(2)}%` : "0.00%";
