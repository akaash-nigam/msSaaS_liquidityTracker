"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { ExchangeRateData } from "@/lib/types";

const CURRENCY_LABELS: Record<string, string> = {
  EUR: "Euro",
  JPY: "Japanese Yen",
  GBP: "British Pound",
  CHF: "Swiss Franc",
  CAD: "Canadian Dollar",
  AUD: "Australian Dollar",
};

export default function ExchangeRatesTable() {
  const { data } = useSWR<ExchangeRateData[]>(
    `${API_BASE}/exchange-rates/latest`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-6 w-48 bg-slate-700 rounded mb-4" />
        <div className="space-y-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-8 bg-slate-800 rounded" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Exchange Rates
        </h2>
        {data.length > 0 && (
          <span className="text-xs text-slate-600">
            As of {data[0].date}
          </span>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left py-2 pr-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Currency
              </th>
              <th className="text-right py-2 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Rate (USD)
              </th>
              <th className="text-right py-2 pl-4 text-xs font-medium text-slate-500 uppercase tracking-wider">
                Daily Change
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((r) => {
              const changeColor = r.change_pct > 0
                ? "text-emerald-400"
                : r.change_pct < 0
                  ? "text-red-400"
                  : "text-slate-400";
              return (
                <tr
                  key={r.currency}
                  className="border-b border-white/5 last:border-0 hover:bg-slate-800/50 transition-colors"
                >
                  <td className="py-3 pr-4">
                    <span className="font-semibold text-white">{r.currency}</span>
                    <span className="ml-2 text-xs text-slate-500">
                      {CURRENCY_LABELS[r.currency] ?? ""}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right tabular-nums font-medium text-white">
                    {r.rate < 0.01 ? r.rate.toFixed(6) : r.rate.toFixed(4)}
                  </td>
                  <td className={`py-3 pl-4 text-right tabular-nums font-semibold ${changeColor}`}>
                    {r.change_pct > 0 ? "+" : ""}{r.change_pct.toFixed(2)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
