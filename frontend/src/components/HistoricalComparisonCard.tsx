"use client";

import useSWR from "swr";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
} from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type {
  HistoricalComparisonData,
  HistoricalComparisonPoint,
} from "@/lib/types";

function mergeData(
  japan: HistoricalComparisonPoint[],
  us: HistoricalComparisonPoint[]
): Array<{ year: number; japan?: number; us?: number }> {
  const map = new Map<
    number,
    { year: number; japan?: number; us?: number }
  >();
  for (const d of japan) {
    map.set(d.year, { year: d.year, japan: d.ratio });
  }
  for (const d of us) {
    const existing = map.get(d.year) || { year: d.year };
    existing.us = d.ratio;
    map.set(d.year, existing);
  }
  return Array.from(map.values()).sort((a, b) => a.year - b.year);
}

export default function HistoricalComparisonCard() {
  const { data } = useSWR<HistoricalComparisonData>(
    `${API_BASE}/liquidity-flows/historical-comparison`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-52 bg-slate-700 rounded mb-6" />
        <div className="h-64 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  const merged = mergeData(data.japan, data.us);
  const peak = data.peak_comparison;

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Japan 1989 vs US Today
        </h3>
      </div>
      <p className="text-[10px] text-slate-600 mb-4">
        Buffett Indicator historical comparison
      </p>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={merged}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="year"
              stroke="#475569"
              tick={{ fontSize: 11 }}
              minTickGap={20}
            />
            <YAxis
              tickFormatter={(v) => `${Number(v)}%`}
              stroke="#475569"
              tick={{ fontSize: 11 }}
              width={50}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "0.5rem",
                fontSize: 13,
              }}
              formatter={(value, name) => [
                `${Number(value).toFixed(1)}%`,
                name === "japan" ? "Japan" : "United States",
              ]}
            />
            <Legend
              wrapperStyle={{ fontSize: 11, color: "#94a3b8" }}
              formatter={(value) =>
                value === "japan" ? "Japan" : "United States"
              }
            />
            <ReferenceLine
              x={peak.japan_peak_year}
              stroke="#f43f5e"
              strokeDasharray="4 4"
              label={{
                value: `Peak ${peak.japan_peak_ratio}%`,
                position: "top",
                fill: "#f43f5e",
                fontSize: 10,
              }}
            />
            <Line
              type="monotone"
              dataKey="japan"
              stroke="#f43f5e"
              strokeWidth={2}
              dot={false}
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="us"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Peak comparison */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
          <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
            Japan Peak ({peak.japan_peak_year})
          </p>
          <p className="text-xl font-bold tabular-nums text-rose-400">
            {peak.japan_peak_ratio}%
          </p>
          {peak.japan_gdp_share_at_peak && (
            <p className="text-[10px] text-slate-500 mt-1">
              {peak.japan_gdp_share_at_peak}% GDP,{" "}
              {peak.japan_mcap_share_at_peak}% MCap
            </p>
          )}
        </div>
        <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
          <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
            US Current ({peak.us_current_year})
          </p>
          <p className="text-xl font-bold tabular-nums text-blue-400">
            {peak.us_current_ratio}%
          </p>
          {peak.us_gdp_share && (
            <p className="text-[10px] text-slate-500 mt-1">
              {peak.us_gdp_share}% GDP, {peak.us_mcap_share}% MCap
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
