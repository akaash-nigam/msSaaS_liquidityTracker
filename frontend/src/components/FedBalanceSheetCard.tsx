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
  Legend,
} from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type { FedBalanceSheetData } from "@/lib/types";

const TIMEFRAMES = ["1M", "3M", "6M", "1Y", "2Y"] as const;

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", year: "2-digit" });
}

export default function FedBalanceSheetCard() {
  const [tf, setTf] = useState<string>("1Y");
  const { data } = useSWR<FedBalanceSheetData>(
    `${API_BASE}/fed-balance-sheet/composition?timeframe=${tf}`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-56 bg-slate-700 rounded mb-6" />
        <div className="h-64 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  const latest = data.latest;

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Fed Balance Sheet Composition
        </h3>
        {/* Timeframe selector */}
        <div className="flex gap-1">
          {TIMEFRAMES.map((t) => (
            <button
              key={t}
              onClick={() => setTf(t)}
              className={`px-2 py-0.5 text-[10px] font-medium rounded ${
                tf === t
                  ? "bg-blue-500/20 text-blue-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>
      <p className="text-[10px] text-slate-600 mb-4">
        Treasuries vs MBS vs Other — QT pace visible in declining totals
      </p>

      {/* Summary metrics */}
      {latest && (
        <div className="grid grid-cols-4 gap-3 mb-5">
          <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
            <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
              Total
            </p>
            <p className="text-lg font-bold tabular-nums text-white">
              ${latest.total?.toFixed(0)}B
            </p>
          </div>
          <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
            <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
              Treasuries
            </p>
            <p className="text-lg font-bold tabular-nums text-blue-400">
              ${latest.treasuries?.toFixed(0)}B
            </p>
          </div>
          <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
            <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
              MBS
            </p>
            <p className="text-lg font-bold tabular-nums text-violet-400">
              ${latest.mbs?.toFixed(0)}B
            </p>
          </div>
          <div className="rounded-xl border border-white/5 bg-slate-800/50 p-3">
            <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">
              Other
            </p>
            <p className="text-lg font-bold tabular-nums text-slate-400">
              ${latest.other?.toFixed(0)}B
            </p>
          </div>
        </div>
      )}

      {/* Stacked area chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data.data}>
            <defs>
              <linearGradient id="treasGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.4} />
                <stop offset="100%" stopColor="#3b82f6" stopOpacity={0.05} />
              </linearGradient>
              <linearGradient id="mbsGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.4} />
                <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.05} />
              </linearGradient>
              <linearGradient id="otherGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#64748b" stopOpacity={0.3} />
                <stop offset="100%" stopColor="#64748b" stopOpacity={0.05} />
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
              tickFormatter={(v) => `$${(Number(v) / 1000).toFixed(1)}T`}
              stroke="#475569"
              tick={{ fontSize: 10 }}
              width={55}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "0.5rem",
                fontSize: 12,
              }}
              formatter={(value, name) => [
                `$${Number(value).toFixed(0)}B`,
                name === "treasuries"
                  ? "Treasuries"
                  : name === "mbs"
                  ? "MBS"
                  : "Other",
              ]}
            />
            <Legend
              wrapperStyle={{ fontSize: 11, color: "#94a3b8" }}
              formatter={(value) =>
                value === "treasuries"
                  ? "Treasuries"
                  : value === "mbs"
                  ? "MBS"
                  : "Other"
              }
            />
            <Area
              type="monotone"
              dataKey="other"
              stackId="1"
              stroke="#64748b"
              fill="url(#otherGradient)"
              strokeWidth={1}
            />
            <Area
              type="monotone"
              dataKey="mbs"
              stackId="1"
              stroke="#8b5cf6"
              fill="url(#mbsGradient)"
              strokeWidth={1}
            />
            <Area
              type="monotone"
              dataKey="treasuries"
              stackId="1"
              stroke="#3b82f6"
              fill="url(#treasGradient)"
              strokeWidth={1}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
