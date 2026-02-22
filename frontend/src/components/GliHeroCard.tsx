"use client";

import type { GliCurrent } from "@/lib/types";

const CYCLE_COLORS: Record<string, string> = {
  expansion: "text-emerald-400",
  recovery: "text-blue-400",
  slowdown: "text-amber-400",
  contraction: "text-red-400",
};

export default function GliHeroCard({ data }: { data: GliCurrent | undefined }) {
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
  const cycleColor = CYCLE_COLORS[data.cycle_position] ?? "text-slate-400";

  const hasCbPs = data.cb_value != null && data.ps_value != null;
  const total = hasCbPs ? data.cb_value! + data.ps_value! : 0;
  const cbPct = total > 0 ? (data.cb_value! / total) * 100 : 0;
  const psPct = total > 0 ? (data.ps_value! / total) * 100 : 0;

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-8">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Global Liquidity Index
        </h2>
        <span className={`text-xs font-semibold uppercase tracking-wider px-3 py-1 rounded-full border ${cycleColor} border-current/20`}>
          {data.cycle_position}
        </span>
      </div>

      <div className="mt-4">
        <span className="text-5xl font-bold tabular-nums tracking-tight text-white">
          ${data.value.toFixed(1)}T
        </span>
        <span className="ml-2 text-lg text-slate-400">USD</span>
      </div>

      <div className="mt-6 flex gap-8">
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Daily</p>
          <p className={`text-lg font-semibold tabular-nums ${changePctColor}`}>
            {data.change_pct >= 0 ? "+" : ""}
            {data.change_pct.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Monthly</p>
          <p className={`text-lg font-semibold tabular-nums ${change1mColor}`}>
            {data.change_1m_pct >= 0 ? "+" : ""}
            {data.change_1m_pct.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider">Sources</p>
          <p className="text-lg font-semibold tabular-nums text-slate-300">
            {data.num_sources} central banks
          </p>
        </div>
      </div>

      {hasCbPs && (
        <div className="mt-6 pt-5 border-t border-white/5">
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">
            Liquidity Composition
          </p>
          <div className="h-3 rounded-full overflow-hidden flex bg-slate-800">
            <div
              className="bg-blue-500 transition-all duration-500"
              style={{ width: `${cbPct}%` }}
            />
            <div
              className="bg-emerald-500 transition-all duration-500"
              style={{ width: `${psPct}%` }}
            />
          </div>
          <div className="mt-2 flex justify-between text-xs">
            <span className="flex items-center gap-1.5">
              <span className="inline-block w-2 h-2 rounded-full bg-blue-500" />
              <span className="text-slate-400">Central Banks</span>
              <span className="font-semibold tabular-nums text-slate-300">
                ${data.cb_value!.toFixed(1)}T
              </span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-slate-400">Private Sector</span>
              <span className="font-semibold tabular-nums text-slate-300">
                ${data.ps_value!.toFixed(1)}T
              </span>
            </span>
          </div>
        </div>
      )}

      <p className="mt-4 text-xs text-slate-600">
        As of {data.date}
      </p>
    </div>
  );
}
