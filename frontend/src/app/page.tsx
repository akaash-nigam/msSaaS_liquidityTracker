"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type {
  GliCurrent,
  GliComponent,
  PrivateSectorCurrent,
  PrivateSectorComponent,
  DataFreshness,
} from "@/lib/types";
import GliHeroCard from "@/components/GliHeroCard";
import CycleGauge from "@/components/CycleGauge";
import GliChart from "@/components/GliChart";
import StackedLiquidityChart from "@/components/StackedLiquidityChart";
import FedBalanceSheetCard from "@/components/FedBalanceSheetCard";
import ComponentsTable from "@/components/ComponentsTable";
import FedRrpCard from "@/components/FedRrpCard";
import TpslHeroCard from "@/components/TpslHeroCard";
import TpslChart from "@/components/TpslChart";
import PrivateSectorTable from "@/components/PrivateSectorTable";
import FreshnessBadge from "@/components/FreshnessBadge";

function SectionHeader({
  title,
  lastUpdated,
}: {
  title: string;
  lastUpdated?: string | null;
}) {
  return (
    <div className="flex items-center gap-3 pt-4">
      <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">
        {title}
      </h2>
      {lastUpdated && <FreshnessBadge lastUpdated={lastUpdated} />}
      <div className="flex-1 h-px bg-white/5" />
    </div>
  );
}

export default function Home() {
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
  const { data: freshness } = useSWR<DataFreshness>(
    `${API_BASE}/data/freshness`,
    fetcher
  );

  return (
    <div className="min-h-screen bg-[#0a0a1a]">
      <main className="mx-auto max-w-7xl px-6 py-8 space-y-6">
        {/* GLI Hero + Cycle Gauge */}
        <SectionHeader
          title="Global Liquidity Index"
          lastUpdated={freshness?.gli}
        />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <GliHeroCard data={current} />
          </div>
          <CycleGauge />
        </div>

        {/* GLI Chart + Stacked Chart + Fed Balance Sheet + Central Bank Table */}
        <GliChart />
        <StackedLiquidityChart />
        <FedBalanceSheetCard />
        <ComponentsTable data={components} />

        {/* Fed RRP Facility */}
        <SectionHeader title="Fed Reverse Repo (RRP) Facility" />
        <FedRrpCard />

        {/* Private Sector Liquidity */}
        <SectionHeader
          title="Private Sector Liquidity"
          lastUpdated={freshness?.private_sector}
        />
        <TpslHeroCard data={psCurrent} />
        <TpslChart />
        <PrivateSectorTable data={psComponents} />
      </main>
    </div>
  );
}
