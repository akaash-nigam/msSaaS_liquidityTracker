"use client";

import useSWR from "swr";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type { MultiTimeframeData } from "@/lib/types";

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function MultiTimeframeCard() {
  const { data } = useSWR<MultiTimeframeData>(
    `${API_BASE}/analytics/multi-timeframe`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-48 bg-slate-700 rounded mb-6" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 bg-slate-800 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-4">
        Multi-Timeframe GLI
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {data.panels.map((panel) => (
          <div
            key={panel.timeframe}
            className="rounded-xl border border-white/5 bg-slate-800/50 p-4"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-white">
                {panel.timeframe}
              </span>
              <span
                className={`text-xs font-medium tabular-nums ${
                  panel.change_pct >= 0 ? "text-emerald-400" : "text-red-400"
                }`}
              >
                {panel.change_pct >= 0 ? "+" : ""}
                {panel.change_pct.toFixed(2)}%
              </span>
            </div>

            {/* Sparkline */}
            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={panel.gli_data}>
                  <defs>
                    <linearGradient
                      id={`mtGrad-${panel.timeframe}`}
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop
                        offset="5%"
                        stopColor={panel.change_pct >= 0 ? "#10b981" : "#ef4444"}
                        stopOpacity={0.3}
                      />
                      <stop
                        offset="95%"
                        stopColor={panel.change_pct >= 0 ? "#10b981" : "#ef4444"}
                        stopOpacity={0}
                      />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" hide />
                  <YAxis domain={["auto", "auto"]} hide />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "0.5rem",
                      fontSize: 11,
                    }}
                    labelFormatter={(label) => formatDate(String(label))}
                    formatter={(value) => [
                      `$${Number(value).toFixed(2)}T`,
                      "GLI",
                    ]}
                  />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke={panel.change_pct >= 0 ? "#10b981" : "#ef4444"}
                    strokeWidth={1.5}
                    fill={`url(#mtGrad-${panel.timeframe})`}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-2 mt-3 text-center">
              <div>
                <p className="text-[10px] text-slate-500">Current</p>
                <p className="text-xs font-medium tabular-nums text-white">
                  ${panel.current.toFixed(1)}T
                </p>
              </div>
              <div>
                <p className="text-[10px] text-slate-500">High</p>
                <p className="text-xs font-medium tabular-nums text-emerald-400">
                  ${panel.high.toFixed(1)}T
                </p>
              </div>
              <div>
                <p className="text-[10px] text-slate-500">Low</p>
                <p className="text-xs font-medium tabular-nums text-red-400">
                  ${panel.low.toFixed(1)}T
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
