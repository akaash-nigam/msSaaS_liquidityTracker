"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { MarketIndicatorData } from "@/lib/types";

const CATEGORY_LABELS: Record<string, string> = {
  volatility: "Volatility",
  yield_curve: "Yield Curve",
  credit_spread: "Credit Spreads",
  real_rates: "Real Rates",
};

const CATEGORY_ORDER = ["volatility", "yield_curve", "credit_spread", "real_rates"];

function SignalBadge({ signal }: { signal: string }) {
  const colors: Record<string, string> = {
    bullish: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    bearish: "bg-red-500/10 text-red-400 border-red-500/20",
    neutral: "bg-slate-500/10 text-slate-400 border-slate-500/20",
  };
  return (
    <span
      className={`text-[10px] font-medium px-1.5 py-0.5 rounded border ${
        colors[signal] || colors.neutral
      }`}
    >
      {signal}
    </span>
  );
}

export default function MarketIndicatorsCard() {
  const { data } = useSWR<MarketIndicatorData[]>(
    `${API_BASE}/market-indicators/current`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-40 bg-slate-700 rounded mb-6" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="h-24 bg-slate-800 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  // Group by category
  const grouped: Record<string, MarketIndicatorData[]> = {};
  for (const item of data) {
    const cat = item.category || "other";
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(item);
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-6">
        Market Indicators
      </h2>

      <div className="space-y-5">
        {CATEGORY_ORDER.filter((cat) => grouped[cat]).map((cat) => (
          <div key={cat}>
            <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-600 mb-2">
              {CATEGORY_LABELS[cat] || cat}
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {grouped[cat].map((ind) => (
                <div
                  key={ind.series_id}
                  className="rounded-xl border border-white/5 bg-slate-800/50 p-3"
                >
                  <p className="text-xs text-slate-400 mb-1 truncate">
                    {ind.name}
                  </p>
                  <p className="text-2xl font-bold text-white tabular-nums">
                    {ind.unit === "percent"
                      ? `${ind.value.toFixed(2)}%`
                      : ind.value.toFixed(2)}
                  </p>
                  <div className="flex items-center justify-between mt-1.5">
                    <span
                      className={`text-xs font-medium tabular-nums ${
                        ind.change > 0
                          ? "text-red-400"
                          : ind.change < 0
                          ? "text-emerald-400"
                          : "text-slate-500"
                      }`}
                    >
                      {ind.change > 0 ? "+" : ""}
                      {ind.change.toFixed(2)}
                    </span>
                    <SignalBadge signal={ind.signal} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
