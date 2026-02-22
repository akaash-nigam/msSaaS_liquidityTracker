"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { TicData, BopData } from "@/lib/types";

function ValRow({ label, value, unit = "B" }: { label: string; value: number; unit?: string }) {
  const color = value > 0 ? "text-emerald-400" : value < 0 ? "text-red-400" : "text-slate-300";
  const sign = value > 0 ? "+" : "";
  return (
    <div className="flex justify-between items-center py-1.5">
      <span className="text-xs text-slate-400">{label}</span>
      <span className={`text-sm font-semibold tabular-nums ${color}`}>
        {sign}${Math.abs(value).toFixed(1)}{unit}
      </span>
    </div>
  );
}

function TicPanel({ data }: { data: TicData | undefined }) {
  if (!data) {
    return (
      <div className="space-y-3 animate-pulse">
        {[1, 2, 3, 4].map((i) => <div key={i} className="h-6 bg-slate-800 rounded" />)}
      </div>
    );
  }

  const items = [
    { label: "Treasuries", value: data.treasuries },
    { label: "Equities", value: data.equities },
    { label: "Corporate Bonds", value: data.corporate_bonds },
    { label: "Agency Bonds", value: data.agency_bonds },
  ];
  const max = Math.max(...items.map((i) => Math.abs(i.value)));

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Foreign Holdings (TIC)
        </h3>
        <span className="text-lg font-bold tabular-nums text-white">
          ${data.total_holdings.toFixed(1)}T
        </span>
      </div>
      <div className="space-y-2">
        {items.map((item) => (
          <div key={item.label}>
            <div className="flex justify-between text-xs mb-0.5">
              <span className="text-slate-400">{item.label}</span>
              <span className="tabular-nums text-slate-300 font-medium">${item.value.toFixed(1)}T</span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-violet-500 rounded-full transition-all duration-500"
                style={{ width: `${max > 0 ? (Math.abs(item.value) / max) * 100 : 0}%` }}
              />
            </div>
          </div>
        ))}
      </div>
      <p className="mt-2 text-xs text-slate-600">As of {data.date}</p>
    </div>
  );
}

function BopPanel({ data }: { data: BopData | undefined }) {
  if (!data) {
    return (
      <div className="space-y-3 animate-pulse">
        {[1, 2, 3, 4, 5].map((i) => <div key={i} className="h-6 bg-slate-800 rounded" />)}
      </div>
    );
  }

  return (
    <div>
      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300 mb-3">
        Balance of Payments
      </h3>
      <div className="divide-y divide-white/5">
        <ValRow label="Current Account" value={data.current_account_balance} />
        <ValRow label="Trade Balance" value={data.trade_balance} />
        <ValRow label="Financial Account" value={data.financial_account_balance} />
        <ValRow label="Net FDI" value={data.net_direct_investment} />
        <ValRow label="Net Portfolio" value={data.net_portfolio_investment} />
      </div>
      <p className="mt-2 text-xs text-slate-600">As of {data.date}</p>
    </div>
  );
}

export default function CapitalFlowsCard() {
  const { data: tic } = useSWR<TicData>(`${API_BASE}/capital-flows/tic/latest`, fetcher);
  const { data: bop } = useSWR<BopData>(`${API_BASE}/capital-flows/bop/latest`, fetcher);

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400 mb-5">
        Capital Flows
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TicPanel data={tic} />
        <BopPanel data={bop} />
      </div>
    </div>
  );
}
