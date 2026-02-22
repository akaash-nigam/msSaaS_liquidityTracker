"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { AssetPriceData, AssetCorrelationData } from "@/lib/types";

const ASSET_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  equity: { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/20" },
  commodity: { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/20" },
  crypto: { bg: "bg-violet-500/10", text: "text-violet-400", border: "border-violet-500/20" },
};

function corrColor(v: number): string {
  if (v >= 0.7) return "text-emerald-400";
  if (v >= 0.4) return "text-yellow-400";
  return "text-slate-400";
}

function formatPrice(price: number): string {
  if (price >= 10000) return price.toLocaleString("en-US", { maximumFractionDigits: 0 });
  if (price >= 100) return price.toLocaleString("en-US", { maximumFractionDigits: 0 });
  return price.toFixed(2);
}

export default function AssetCorrelationsCard() {
  const { data: prices } = useSWR<AssetPriceData[]>(
    `${API_BASE}/assets/prices`,
    fetcher
  );
  const { data: correlations } = useSWR<AssetCorrelationData[]>(
    `${API_BASE}/assets/correlations`,
    fetcher
  );

  if (!prices || !correlations) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-48 bg-slate-700 rounded mb-6" />
        <div className="grid grid-cols-3 gap-4 mb-6">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-24 bg-slate-800 rounded-xl" />
          ))}
        </div>
        <div className="h-32 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-6">
        Asset Prices & Correlations
      </h2>

      {/* Asset Price Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        {prices.map((asset) => {
          const colors = ASSET_COLORS[asset.asset_class] || ASSET_COLORS.equity;
          return (
            <div
              key={asset.ticker}
              className="rounded-xl border border-white/5 bg-slate-800/50 p-4"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-slate-400">{asset.asset}</span>
                <span
                  className={`text-[10px] font-medium px-1.5 py-0.5 rounded border ${colors.bg} ${colors.text} ${colors.border}`}
                >
                  {asset.asset_class}
                </span>
              </div>
              <p className="text-2xl font-bold text-white tabular-nums">
                ${formatPrice(asset.price)}
              </p>
              <p
                className={`text-xs font-medium mt-1 tabular-nums ${
                  asset.change_pct >= 0 ? "text-emerald-400" : "text-red-400"
                }`}
              >
                {asset.change_pct >= 0 ? "+" : ""}
                {asset.change_pct.toFixed(2)}%
              </p>
            </div>
          );
        })}
      </div>

      {/* Correlation Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left text-xs text-slate-500 font-medium pb-2 pr-4">
                Asset
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                30d
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                90d
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 px-3">
                365d
              </th>
              <th className="text-right text-xs text-slate-500 font-medium pb-2 pl-3">
                Beta
              </th>
            </tr>
          </thead>
          <tbody>
            {correlations.map((row) => (
              <tr
                key={row.asset}
                className="border-b border-white/5 last:border-0 hover:bg-slate-800/50"
              >
                <td className="py-2.5 pr-4 text-white font-medium">
                  {row.asset}
                </td>
                <td
                  className={`py-2.5 px-3 text-right tabular-nums font-medium ${corrColor(
                    row.correlation_30d
                  )}`}
                >
                  {row.correlation_30d.toFixed(2)}
                </td>
                <td
                  className={`py-2.5 px-3 text-right tabular-nums font-medium ${corrColor(
                    row.correlation_90d
                  )}`}
                >
                  {row.correlation_90d.toFixed(2)}
                </td>
                <td
                  className={`py-2.5 px-3 text-right tabular-nums font-medium ${corrColor(
                    row.correlation_365d
                  )}`}
                >
                  {row.correlation_365d.toFixed(2)}
                </td>
                <td className="py-2.5 pl-3 text-right tabular-nums font-medium text-white">
                  {row.beta_to_gli.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
