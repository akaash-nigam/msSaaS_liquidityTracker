"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { DataFreshness } from "@/lib/types";
import ExchangeRatesTable from "@/components/ExchangeRatesTable";
import CapitalFlowsCard from "@/components/CapitalFlowsCard";
import StablecoinSupplyCard from "@/components/StablecoinSupplyCard";
import ValuationHeatmapCard from "@/components/ValuationHeatmapCard";
import LiquidityFlowCard from "@/components/LiquidityFlowCard";
import HistoricalComparisonCard from "@/components/HistoricalComparisonCard";
import MarketIndicatorsCard from "@/components/MarketIndicatorsCard";
import AssetCorrelationsCard from "@/components/AssetCorrelationsCard";
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

export default function MarketsPage() {
  const { data: freshness } = useSWR<DataFreshness>(
    `${API_BASE}/data/freshness`,
    fetcher
  );

  return (
    <div className="min-h-screen bg-[#0a0a1a]">
      <main className="mx-auto max-w-7xl px-6 py-8 space-y-6">
        {/* Exchange Rates */}
        <SectionHeader
          title="Exchange Rates"
          lastUpdated={freshness?.exchange_rates}
        />
        <ExchangeRatesTable />

        {/* Capital Flows */}
        <SectionHeader
          title="Capital Flows"
          lastUpdated={freshness?.capital_flows}
        />
        <CapitalFlowsCard />

        {/* Stablecoin Supply */}
        <SectionHeader title="Stablecoin Supply" />
        <StablecoinSupplyCard />

        {/* Liquidity Destination */}
        <SectionHeader
          title="Liquidity Destination"
          lastUpdated={freshness?.valuations}
        />
        <ValuationHeatmapCard />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <LiquidityFlowCard />
          <HistoricalComparisonCard />
        </div>

        {/* Market Indicators */}
        <SectionHeader
          title="Market Indicators"
          lastUpdated={freshness?.market_indicators}
        />
        <MarketIndicatorsCard />

        {/* Asset Correlations */}
        <SectionHeader
          title="Asset Correlations"
          lastUpdated={freshness?.asset_prices}
        />
        <AssetCorrelationsCard />
      </main>
    </div>
  );
}
