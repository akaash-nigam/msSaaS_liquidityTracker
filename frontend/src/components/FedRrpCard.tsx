"use client";

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
import type { FedRrpData } from "@/lib/types";

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function FedRrpCard() {
  const { data } = useSWR<FedRrpData>(
    `${API_BASE}/fed-rrp/current`,
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

  const isBullish = data.signal === "bullish";

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Fed Overnight Reverse Repo (ON RRP)
        </h3>
        <span
          className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full ${
            isBullish
              ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
              : "bg-slate-500/10 text-slate-400 border border-slate-500/20"
          }`}
        >
          {data.signal}
        </span>
      </div>
      <p className="text-[10px] text-slate-600 mb-4">
        When RRP drains, liquidity enters risk assets
      </p>

      {/* Key metrics */}
      <div className="grid grid-cols-3 gap-4 mb-5">
        <div>
          <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
            Current Level
          </p>
          <p className="text-2xl font-bold tabular-nums text-white">
            ${data.current_level_billions.toFixed(0)}B
          </p>
        </div>
        <div>
          <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
            Peak Level
          </p>
          <p className="text-lg font-bold tabular-nums text-slate-400">
            ${data.peak_level_billions.toFixed(0)}B
          </p>
        </div>
        <div>
          <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
            Drawdown from Peak
          </p>
          <p
            className={`text-lg font-bold tabular-nums ${
              data.drawdown_pct < -50 ? "text-emerald-400" : "text-amber-400"
            }`}
          >
            {data.drawdown_pct.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Chart */}
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data.historical}>
            <defs>
              <linearGradient id="rrpGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              stroke="#475569"
              tick={{ fontSize: 10 }}
              minTickGap={40}
            />
            <YAxis
              tickFormatter={(v) => `$${Number(v).toFixed(0)}B`}
              stroke="#475569"
              tick={{ fontSize: 10 }}
              width={60}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "0.5rem",
                fontSize: 12,
              }}
              formatter={(value) => [
                `$${Number(value).toFixed(1)}B`,
                "ON RRP",
              ]}
              labelFormatter={(label) => formatDate(String(label))}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#rrpGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
