"use client";

import WorldMapCard from "@/components/WorldMapCard";
import CorrelationMatrixCard from "@/components/CorrelationMatrixCard";
import SankeyDiagramCard from "@/components/SankeyDiagramCard";
import MultiTimeframeCard from "@/components/MultiTimeframeCard";
import CycleAllocationCard from "@/components/CycleAllocationCard";

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

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-[#0a0a1a]">
      <main className="mx-auto max-w-7xl px-6 py-8 space-y-6">
        {/* Multi-Timeframe */}
        <SectionHeader title="Multi-Timeframe GLI" />
        <MultiTimeframeCard />

        {/* Cycle Allocation */}
        <SectionHeader title="Cycle-Based Asset Allocation" />
        <CycleAllocationCard />

        {/* Global Liquidity Map */}
        <SectionHeader title="Global Liquidity Map" />
        <WorldMapCard />

        {/* Correlation Matrix */}
        <SectionHeader title="Correlation Matrix" />
        <CorrelationMatrixCard />

        {/* Liquidity Flow Sankey */}
        <SectionHeader title="Liquidity Flow Sankey" />
        <SankeyDiagramCard />
      </main>
    </div>
  );
}
