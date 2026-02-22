"use client";

import useSWR from "swr";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type { ValuationData } from "@/lib/types";

const SIGNAL_COLORS: Record<string, string> = {
  extreme: "#ef4444",
  elevated: "#f59e0b",
  fair: "#10b981",
  undervalued: "#3b82f6",
};

const SIGNAL_BG: Record<string, string> = {
  extreme: "bg-red-500/10 text-red-400 border-red-500/20",
  elevated: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  fair: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  undervalued: "bg-blue-500/10 text-blue-400 border-blue-500/20",
};

function SignalBadge({ signal }: { signal: string }) {
  return (
    <span
      className={`text-[10px] font-medium px-1.5 py-0.5 rounded border ${
        SIGNAL_BG[signal] || SIGNAL_BG.fair
      }`}
    >
      {signal}
    </span>
  );
}

export default function ValuationHeatmapCard() {
  const { data } = useSWR<ValuationData[]>(
    `${API_BASE}/liquidity-flows/valuations`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-56 bg-slate-700 rounded mb-6" />
        <div className="h-80 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  const sorted = [...data].sort((a, b) => b.ratio - a.ratio);

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Global Valuation Heatmap
        </h2>
        <span className="text-[10px] text-slate-600">
          Buffett Indicator (Market Cap / GDP)
        </span>
      </div>

      {/* Warning callout */}
      <div className="mb-5 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3">
        <p className="text-xs text-red-400">
          <span className="font-semibold">Japan 1989 parallel:</span>{" "}
          Japan was 18% of global GDP but 48% of market cap at its peak.
          The US is now 22% of GDP but ~49% of market cap.
        </p>
      </div>

      {/* Horizontal bar chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              horizontal={false}
            />
            <XAxis
              type="number"
              tickFormatter={(v) => `${Number(v)}%`}
              stroke="#475569"
              tick={{ fontSize: 11 }}
            />
            <YAxis
              type="category"
              dataKey="country"
              stroke="#475569"
              tick={{ fontSize: 11, fill: "#94a3b8" }}
              width={75}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "0.5rem",
                fontSize: 13,
              }}
              formatter={(value) => [
                `${Number(value).toFixed(1)}%`,
                "Market Cap / GDP",
              ]}
              labelFormatter={(label) => String(label)}
            />
            <ReferenceLine
              x={100}
              stroke="#475569"
              strokeDasharray="3 3"
              label={{
                value: "Fair Value",
                position: "top",
                fill: "#64748b",
                fontSize: 10,
              }}
            />
            <Bar dataKey="ratio" radius={[0, 4, 4, 0]}>
              {sorted.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={SIGNAL_COLORS[entry.signal] || SIGNAL_COLORS.fair}
                  fillOpacity={0.8}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Data table */}
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left text-xs text-slate-500 font-medium pb-2 pr-4">
                Country
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                Ratio
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                GDP Share
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                MCap Share
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 pl-3">
                Signal
              </th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((row) => (
              <tr
                key={row.country_code}
                className="border-b border-white/5 last:border-0 hover:bg-slate-800/50"
              >
                <td className="py-2 pr-4 text-white font-medium">
                  {row.country}
                </td>
                <td className="py-2 px-3 text-right tabular-nums font-medium text-white">
                  {row.ratio.toFixed(1)}%
                </td>
                <td className="py-2 px-3 text-right tabular-nums text-slate-300">
                  {row.gdp_share?.toFixed(1) ?? "\u2014"}%
                </td>
                <td className="py-2 px-3 text-right tabular-nums text-slate-300">
                  {row.mcap_share?.toFixed(1) ?? "\u2014"}%
                </td>
                <td className="py-2 pl-3 text-right">
                  <SignalBadge signal={row.signal} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
