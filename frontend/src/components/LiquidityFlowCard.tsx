"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { LiquidityFlowData } from "@/lib/types";

const REGION_COLORS: Record<string, string> = {
  "United States": "bg-blue-500",
  "Europe (DM)": "bg-violet-500",
  Japan: "bg-rose-500",
  "EM Asia": "bg-emerald-500",
  "EM LatAm": "bg-amber-500",
  "Emerging Markets": "bg-emerald-500",
  Other: "bg-slate-500",
};

const DIRECTION_COLORS: Record<string, string> = {
  increasing: "text-emerald-400",
  decreasing: "text-red-400",
  flat: "text-slate-400",
};

export default function LiquidityFlowCard() {
  const { data } = useSWR<LiquidityFlowData>(
    `${API_BASE}/liquidity-flows/direction`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-44 bg-slate-700 rounded mb-6" />
        <div className="h-40 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Liquidity Flow Direction
        </h3>
        <span className="text-lg font-bold tabular-nums text-white">
          ${data.total_global_flows.toFixed(0)}B
        </span>
      </div>
      <p className="text-[10px] text-slate-600 mb-4">
        Where is global capital flowing?
      </p>

      {/* Stacked horizontal bar */}
      <div className="h-6 rounded-full overflow-hidden flex bg-slate-800 mb-4">
        {data.flows.map((flow) => (
          <div
            key={flow.region}
            className={`${
              REGION_COLORS[flow.region] || "bg-slate-600"
            } transition-all duration-500`}
            style={{ width: `${flow.share_pct}%` }}
            title={`${flow.region}: ${flow.share_pct}%`}
          />
        ))}
      </div>

      {/* Flow breakdown */}
      <div className="space-y-2">
        {data.flows.map((flow) => (
          <div key={flow.region} className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span
                className={`inline-block w-2.5 h-2.5 rounded-sm ${
                  REGION_COLORS[flow.region] || "bg-slate-600"
                }`}
              />
              <span className="text-xs text-slate-400">{flow.region}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs tabular-nums text-slate-300 font-medium">
                ${flow.amount.toFixed(0)}B
              </span>
              <span className="text-xs tabular-nums text-slate-400 w-10 text-right">
                {flow.share_pct.toFixed(0)}%
              </span>
              <span
                className={`text-xs tabular-nums font-medium w-12 text-right ${
                  DIRECTION_COLORS[flow.direction] || "text-slate-400"
                }`}
              >
                {flow.change_pct > 0 ? "+" : ""}
                {flow.change_pct.toFixed(1)}%
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* DM vs EM mini bar */}
      <div className="mt-5 pt-4 border-t border-white/5">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-600 mb-2">
          Developed vs Emerging
        </p>
        <div className="h-3 rounded-full overflow-hidden flex bg-slate-800">
          <div
            className="bg-blue-500 transition-all duration-500"
            style={{ width: `${data.dm_vs_em.dm_share}%` }}
          />
          <div
            className="bg-emerald-500 transition-all duration-500"
            style={{ width: `${data.dm_vs_em.em_share}%` }}
          />
        </div>
        <div className="mt-1.5 flex justify-between text-xs">
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-2 h-2 rounded-full bg-blue-500" />
            <span className="text-slate-400">DM</span>
            <span className="font-semibold tabular-nums text-slate-300">
              {data.dm_vs_em.dm_share.toFixed(0)}%
            </span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-slate-400">EM</span>
            <span className="font-semibold tabular-nums text-slate-300">
              {data.dm_vs_em.em_share.toFixed(0)}%
            </span>
          </span>
        </div>
      </div>
    </div>
  );
}
