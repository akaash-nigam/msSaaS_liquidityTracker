"use client";

import { useState } from "react";
import useSWR from "swr";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type { GliHistoricalPoint } from "@/lib/types";

const TIMEFRAMES = ["1M", "3M", "6M", "1Y"] as const;

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function TpslChart() {
  const [timeframe, setTimeframe] = useState<string>("1Y");
  const { data } = useSWR<GliHistoricalPoint[]>(
    `${API_BASE}/private-sector/historical?timeframe=${timeframe}`,
    fetcher
  );

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Historical TPSL
        </h2>
        <div className="flex gap-1">
          {TIMEFRAMES.map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                timeframe === tf
                  ? "bg-emerald-600 text-white"
                  : "text-slate-400 hover:text-white hover:bg-slate-800"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      <div className="h-72">
        {data ? (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="tpslGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey="date"
                tickFormatter={(v) => formatDate(String(v))}
                stroke="#475569"
                tick={{ fontSize: 11 }}
                minTickGap={40}
              />
              <YAxis
                domain={["auto", "auto"]}
                tickFormatter={(v) => `$${Number(v).toFixed(0)}T`}
                stroke="#475569"
                tick={{ fontSize: 11 }}
                width={70}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: "0.5rem",
                  fontSize: 13,
                }}
                labelFormatter={(label) => String(label)}
                formatter={(value) => [`$${Number(value).toFixed(2)}T`, "TPSL"]}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#10b981"
                strokeWidth={2}
                fill="url(#tpslGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-600">
            Loading chart...
          </div>
        )}
      </div>
    </div>
  );
}
