"use client";

import useSWR from "swr";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { API_BASE, fetcher } from "@/lib/api";
import type { CycleAllocationData } from "@/lib/types";

const PHASE_COLORS: Record<string, string> = {
  expansion: "text-emerald-400",
  recovery: "text-blue-400",
  slowdown: "text-amber-400",
  contraction: "text-red-400",
};

export default function CycleAllocationCard() {
  const { data } = useSWR<CycleAllocationData>(
    `${API_BASE}/analytics/cycle-allocation`,
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

  const chartData = data.allocations.map((a) => ({
    name: a.asset_class,
    value: a.weight,
    color: a.color,
  }));

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Howell Cycle Allocation
        </h2>
        <div className="flex items-center gap-2">
          <span
            className={`text-xs font-semibold capitalize ${
              PHASE_COLORS[data.cycle_position] || "text-slate-400"
            }`}
          >
            {data.cycle_position}
          </span>
          <span className="text-[10px] text-slate-600">
            Momentum: {data.momentum > 0 ? "+" : ""}
            {data.momentum.toFixed(2)}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
                label={({ name, value }) => `${name} ${value}%`}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: "0.5rem",
                  fontSize: 13,
                }}
                formatter={(value) => [`${Number(value)}%`, "Weight"]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Allocation cards */}
        <div className="space-y-3">
          {data.allocations.map((alloc) => (
            <div
              key={alloc.asset_class}
              className="rounded-xl border border-white/5 bg-slate-800/50 px-4 py-3"
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <div
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: alloc.color }}
                  />
                  <span className="text-sm font-medium text-white">
                    {alloc.asset_class}
                  </span>
                </div>
                <span className="text-sm font-bold tabular-nums text-white">
                  {alloc.weight}%
                </span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                {alloc.rationale}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
