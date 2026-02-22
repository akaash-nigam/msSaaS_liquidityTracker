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
import type { StablecoinData } from "@/lib/types";

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", year: "2-digit" });
}

export default function StablecoinSupplyCard() {
  const { data } = useSWR<StablecoinData>(
    `${API_BASE}/stablecoins/current`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-48 bg-slate-700 rounded mb-6" />
        <div className="h-64 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Stablecoin Supply
        </h2>
        <span className="text-[10px] text-slate-600">
          Total: ${data.total_supply.toFixed(1)}B
        </span>
      </div>

      {/* Hero numbers */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="rounded-xl border border-white/5 bg-slate-800/50 px-4 py-3">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />
            <span className="text-xs text-slate-400">USDT</span>
            <span className="text-[10px] text-slate-600">
              {data.usdt.dominance.toFixed(1)}%
            </span>
          </div>
          <p className="text-xl font-bold tabular-nums text-white">
            ${data.usdt.supply.toFixed(1)}B
          </p>
          <span
            className={`text-[11px] font-medium ${
              data.usdt.change_7d >= 0 ? "text-emerald-400" : "text-red-400"
            }`}
          >
            {data.usdt.change_7d >= 0 ? "+" : ""}
            {data.usdt.change_7d.toFixed(1)}% 7d
          </span>
        </div>
        <div className="rounded-xl border border-white/5 bg-slate-800/50 px-4 py-3">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <span className="text-xs text-slate-400">USDC</span>
            <span className="text-[10px] text-slate-600">
              {data.usdc.dominance.toFixed(1)}%
            </span>
          </div>
          <p className="text-xl font-bold tabular-nums text-white">
            ${data.usdc.supply.toFixed(1)}B
          </p>
          <span
            className={`text-[11px] font-medium ${
              data.usdc.change_7d >= 0 ? "text-emerald-400" : "text-red-400"
            }`}
          >
            {data.usdc.change_7d >= 0 ? "+" : ""}
            {data.usdc.change_7d.toFixed(1)}% 7d
          </span>
        </div>
      </div>

      {/* Area Chart */}
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data.historical}>
            <defs>
              <linearGradient id="usdtGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="usdcGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
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
              tickFormatter={(v) => `$${Number(v).toFixed(0)}B`}
              stroke="#475569"
              tick={{ fontSize: 11 }}
              width={60}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "0.5rem",
                fontSize: 13,
              }}
              labelFormatter={(label) => String(label)}
              formatter={(value, name) => [
                `$${Number(value).toFixed(1)}B`,
                String(name).toUpperCase(),
              ]}
            />
            <Area
              type="monotone"
              dataKey="usdt"
              stackId="1"
              stroke="#10b981"
              fill="url(#usdtGrad)"
              strokeWidth={2}
            />
            <Area
              type="monotone"
              dataKey="usdc"
              stackId="1"
              stroke="#3b82f6"
              fill="url(#usdcGrad)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
