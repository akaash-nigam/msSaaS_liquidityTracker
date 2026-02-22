"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { CycleData } from "@/lib/types";

const PHASES = [
  { key: "expansion", label: "Expansion", color: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-500/30" },
  { key: "slowdown", label: "Slowdown", color: "bg-amber-500", text: "text-amber-400", border: "border-amber-500/30" },
  { key: "contraction", label: "Contraction", color: "bg-red-500", text: "text-red-400", border: "border-red-500/30" },
  { key: "recovery", label: "Recovery", color: "bg-blue-500", text: "text-blue-400", border: "border-blue-500/30" },
] as const;

export default function CycleGauge() {
  const { data } = useSWR<CycleData>(`${API_BASE}/gli/cycle`, fetcher);

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse h-full">
        <div className="h-6 w-32 bg-slate-700 rounded mb-4" />
        <div className="grid grid-cols-2 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-20 bg-slate-800 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  const momentumColor = data.momentum >= 0 ? "text-emerald-400" : "text-red-400";

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 h-full flex flex-col">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-4">
        Liquidity Cycle
      </h2>

      <div className="grid grid-cols-2 gap-3 flex-1">
        {PHASES.map((phase) => {
          const isActive = data.current_position === phase.key;
          return (
            <div
              key={phase.key}
              className={`rounded-xl border p-3 flex flex-col items-center justify-center transition-all ${
                isActive
                  ? `${phase.border} bg-slate-800/80 scale-105 ring-1 ring-current/10`
                  : "border-white/5 bg-slate-800/30 opacity-40"
              }`}
            >
              <div className={`w-3 h-3 rounded-full ${phase.color} ${isActive ? "animate-pulse" : ""} mb-1.5`} />
              <span className={`text-xs font-semibold uppercase tracking-wider ${isActive ? phase.text : "text-slate-500"}`}>
                {phase.label}
              </span>
            </div>
          );
        })}
      </div>

      <div className="mt-4 pt-4 border-t border-white/5 space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-xs text-slate-500">Momentum</span>
          <span className={`text-sm font-semibold tabular-nums ${momentumColor}`}>
            {data.momentum >= 0 ? "+" : ""}{data.momentum.toFixed(2)}%
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-xs text-slate-500">Cycle Progress</span>
          <span className="text-sm font-semibold tabular-nums text-slate-300">
            Day {data.cycle_day.toLocaleString()} / {data.total_cycle_days.toLocaleString()}
          </span>
        </div>
        <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full transition-all duration-500"
            style={{ width: `${data.phase_pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}
