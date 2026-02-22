"use client";

import type { PrivateSectorComponent } from "@/lib/types";

export default function PrivateSectorTable({
  data,
}: {
  data: PrivateSectorComponent[] | undefined;
}) {
  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-6 w-48 bg-slate-700 rounded mb-4" />
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-8 bg-slate-800 rounded" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-4">
        Private Sector Components
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left py-2 pr-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Metric
              </th>
              <th className="text-right py-2 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Value
              </th>
              <th className="text-right py-2 pl-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Share
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((c) => (
              <tr
                key={c.key}
                className="border-b border-white/5 last:border-0 hover:bg-slate-800/50 transition-colors"
              >
                <td className="py-3 pr-4 font-medium text-white">
                  {c.name}
                </td>
                <td className="py-3 px-4 text-right tabular-nums font-medium text-white">
                  ${c.value.toFixed(2)}T
                </td>
                <td className="py-3 pl-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-emerald-500 rounded-full"
                        style={{ width: `${Math.min(c.pct_of_total, 100)}%` }}
                      />
                    </div>
                    <span className="tabular-nums text-slate-400 text-xs w-12 text-right">
                      {c.pct_of_total.toFixed(1)}%
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
