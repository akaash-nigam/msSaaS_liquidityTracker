"use client";

function isStale(dateStr: string, thresholdHours: number): boolean {
  const dataDate = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - dataDate.getTime();
  return diffMs > thresholdHours * 60 * 60 * 1000;
}

function formatFreshnessDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function FreshnessBadge({
  lastUpdated,
  thresholdHours = 48,
}: {
  lastUpdated: string | null | undefined;
  thresholdHours?: number;
}) {
  if (!lastUpdated) return null;

  const stale = isStale(lastUpdated, thresholdHours);

  return (
    <span
      className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${
        stale
          ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
          : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
      }`}
    >
      {stale ? "Stale" : "Fresh"} &middot; {formatFreshnessDate(lastUpdated)}
    </span>
  );
}
