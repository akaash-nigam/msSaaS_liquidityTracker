"use client";

import { useState } from "react";
import useSWR, { useSWRConfig } from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type {
  GliCurrent,
  GliComponent,
  PrivateSectorCurrent,
  PrivateSectorComponent,
} from "@/lib/types";
import GliHeroCard from "@/components/GliHeroCard";
import CycleGauge from "@/components/CycleGauge";
import GliChart from "@/components/GliChart";
import StackedLiquidityChart from "@/components/StackedLiquidityChart";
import ComponentsTable from "@/components/ComponentsTable";
import TpslHeroCard from "@/components/TpslHeroCard";
import TpslChart from "@/components/TpslChart";
import PrivateSectorTable from "@/components/PrivateSectorTable";
import ExchangeRatesTable from "@/components/ExchangeRatesTable";
import CapitalFlowsCard from "@/components/CapitalFlowsCard";
import MarketIndicatorsCard from "@/components/MarketIndicatorsCard";
import AssetCorrelationsCard from "@/components/AssetCorrelationsCard";

function SectionHeader({ title }: { title: string }) {
  return (
    <div className="flex items-center gap-3 pt-4">
      <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">
        {title}
      </h2>
      <div className="flex-1 h-px bg-white/5" />
    </div>
  );
}

export default function Home() {
  const { mutate } = useSWRConfig();
  const [refreshing, setRefreshing] = useState(false);
  const [refreshStatus, setRefreshStatus] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);

  const { data: current } = useSWR<GliCurrent>(
    `${API_BASE}/gli/current`,
    fetcher,
    { refreshInterval: 60_000 }
  );
  const { data: components } = useSWR<GliComponent[]>(
    `${API_BASE}/gli/components`,
    fetcher
  );
  const { data: psCurrent } = useSWR<PrivateSectorCurrent>(
    `${API_BASE}/private-sector/current`,
    fetcher
  );
  const { data: psComponents } = useSWR<PrivateSectorComponent[]>(
    `${API_BASE}/private-sector/components`,
    fetcher
  );

  async function handleRefresh() {
    setRefreshing(true);
    setRefreshStatus(null);
    try {
      const res = await fetch(`${API_BASE}/data/refresh`, { method: "POST" });
      const json = await res.json();
      if (json.status === "success") {
        setRefreshStatus({ type: "success", message: "Refreshed!" });
        mutate(() => true, undefined, { revalidate: true });
      } else {
        setRefreshStatus({ type: "error", message: "Failed" });
      }
    } catch {
      setRefreshStatus({ type: "error", message: "Failed" });
    } finally {
      setRefreshing(false);
      setTimeout(() => setRefreshStatus(null), 2000);
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0a1a]">
      {/* Header */}
      <header className="border-b border-white/5 px-6 py-4">
        <div className="mx-auto max-w-7xl flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">
              Global Liquidity Tracker
            </h1>
            <p className="text-xs text-slate-500">
              Powered by FRED &middot; Michael Howell Framework
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Refresh Button */}
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-white/10 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
            >
              <svg
                className={`w-3.5 h-3.5 ${refreshing ? "animate-spin" : ""}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              {refreshing ? "Refreshing..." : "Refresh"}
            </button>
            {refreshStatus && (
              <span
                className={`text-xs font-medium ${
                  refreshStatus.type === "success"
                    ? "text-emerald-400"
                    : "text-red-400"
                }`}
              >
                {refreshStatus.message}
              </span>
            )}
            {/* Live indicator */}
            <span className="inline-block h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-slate-500">Live</span>
          </div>
        </div>
      </header>

      {/* Dashboard */}
      <main className="mx-auto max-w-7xl px-6 py-8 space-y-6">
        {/* GLI Hero + Cycle Gauge */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <GliHeroCard data={current} />
          </div>
          <CycleGauge />
        </div>

        {/* GLI Chart + Stacked Chart + Central Bank Table */}
        <GliChart />
        <StackedLiquidityChart />
        <ComponentsTable data={components} />

        {/* Private Sector Liquidity */}
        <SectionHeader title="Private Sector Liquidity" />
        <TpslHeroCard data={psCurrent} />
        <TpslChart />
        <PrivateSectorTable data={psComponents} />

        {/* Exchange Rates */}
        <SectionHeader title="Exchange Rates" />
        <ExchangeRatesTable />

        {/* Capital Flows */}
        <SectionHeader title="Capital Flows" />
        <CapitalFlowsCard />

        {/* Market Indicators */}
        <SectionHeader title="Market Indicators" />
        <MarketIndicatorsCard />

        {/* Asset Correlations */}
        <SectionHeader title="Asset Correlations" />
        <AssetCorrelationsCard />
      </main>
    </div>
  );
}
