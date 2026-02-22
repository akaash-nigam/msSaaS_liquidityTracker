"use client";

import type { PrivateSectorCurrent } from "@/lib/types";

const COMPONENT_LABELS: Record<string, string> = {
  m2: "M2",
  bank_credit: "Bank Credit",
  mmf: "MMF",
  commercial_paper: "Comm. Paper",
  repos_net: "Net Repos",
};

const COMPONENT_COLORS: Record<string, string> = {
  m2: "bg-emerald-500",
  bank_credit: "bg-teal-500",
  mmf: "bg-cyan-500",
  commercial_paper: "bg-sky-500",
  repos_net: "bg-blue-500",
};

export default function TpslHeroCard({ data }: { data: PrivateSectorCurrent | undefined }) {
  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-8 animate-pulse">
        <div className="h-8 w-48 bg-slate-700 rounded mb-4" />
        <div className="h-14 w-64 bg-slate-700 rounded" />
      </div>
    );
  }

  const changePctColor = data.change_pct >= 0 ? "text-emerald-400" : "text-red-400";
  const change1mColor = data.change_1m_pct >= 0 ? "text-emerald-400" : "text-red-400";

  const total = data.total_value;
  const compEntries = Object.entries(data.components).filter(([, v]) => v > 0);

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-8">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Private Sector Liquidity (TPSL)
        </h2>
        <span className={`text-xs font-medium px-3 py-1 rounded-full border border-emerald-500/20 text-emerald-400`}>
          {data.data_quality === "full" ? "Full Data" : "Partial Data"}
        </span>
      </div>

      <div className="mt-4">
        <span className="text-5xl font-bold tabular-nums tracking-tight text-white">
          ${data.total_value.toFixed(1)}T
        </span>
        <span className="ml-2 text-lg text-slate-400">USD</span>
      </div>

      <div className="mt-6 flex gap-8">
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Daily</p>
          <p className={`text-lg font-semibold tabular-nums ${changePctColor}`}>
            {data.change_pct >= 0 ? "+" : ""}{data.change_pct.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Monthly</p>
          <p className={`text-lg font-semibold tabular-nums ${change1mColor}`}>
            {data.change_1m_pct >= 0 ? "+" : ""}{data.change_1m_pct.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Components</p>
          <p className="text-lg font-semibold tabular-nums text-slate-300">
            {data.num_components} metrics
          </p>
        </div>
      </div>

      {compEntries.length > 0 && (
        <div className="mt-6 pt-5 border-t border-white/5">
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">
            Component Breakdown
          </p>
          <div className="h-3 rounded-full overflow-hidden flex bg-slate-800">
            {compEntries.map(([key, val]) => (
              <div
                key={key}
                className={`${COMPONENT_COLORS[key] ?? "bg-slate-500"} transition-all duration-500`}
                style={{ width: `${(val / total) * 100}%` }}
              />
            ))}
          </div>
          <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
            {compEntries.map(([key, val]) => (
              <span key={key} className="flex items-center gap-1 text-xs">
                <span className={`inline-block w-2 h-2 rounded-full ${COMPONENT_COLORS[key] ?? "bg-slate-500"}`} />
                <span className="text-slate-400">{COMPONENT_LABELS[key] ?? key}</span>
                <span className="font-semibold tabular-nums text-slate-300">${val.toFixed(1)}T</span>
              </span>
            ))}
          </div>
        </div>
      )}

      <p className="mt-4 text-xs text-slate-600">
        As of {data.date}
      </p>
    </div>
  );
}
