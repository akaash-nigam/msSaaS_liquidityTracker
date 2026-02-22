"use client";

import { useState } from "react";
import useSWR from "swr";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
} from "react-simple-maps";
import { API_BASE, fetcher } from "@/lib/api";
import type { WorldMapCountry } from "@/lib/types";

const GEO_URL =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

// Map ISO Alpha-3 to country IDs in Natural Earth data
const CODE_TO_NAME: Record<string, string> = {
  USA: "United States of America",
  DEU: "Germany",
  JPN: "Japan",
  GBR: "United Kingdom",
  CHE: "Switzerland",
  AUS: "Australia",
  CAN: "Canada",
  CHN: "China",
};

function getColor(pct: number): string {
  if (pct >= 20) return "#059669";
  if (pct >= 10) return "#10b981";
  if (pct >= 5) return "#34d399";
  if (pct >= 1) return "#6ee7b7";
  return "#1e293b";
}

export default function WorldMapCard() {
  const { data } = useSWR<WorldMapCountry[]>(
    `${API_BASE}/analytics/world-map`,
    fetcher
  );
  const [tooltip, setTooltip] = useState<WorldMapCountry | null>(null);

  const countryMap: Record<string, WorldMapCountry> = {};
  if (data) {
    for (const c of data) {
      countryMap[c.country_code] = c;
      const name = CODE_TO_NAME[c.country_code];
      if (name) countryMap[name] = c;
    }
  }

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Global Liquidity Map
        </h2>
        <span className="text-[10px] text-slate-600">
          CB Balance Sheet Contribution (%)
        </span>
      </div>

      <div className="relative h-[400px]">
        <ComposableMap
          projectionConfig={{ scale: 147 }}
          style={{ width: "100%", height: "100%" }}
        >
          <ZoomableGroup>
            <Geographies geography={GEO_URL}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  const geoName = geo.properties.name;
                  const match = countryMap[geoName];
                  const fillColor = match
                    ? getColor(match.liquidity_contribution_pct)
                    : "#1e293b";

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill={fillColor}
                      stroke="#0a0a1a"
                      strokeWidth={0.5}
                      onMouseEnter={() => {
                        if (match) setTooltip(match);
                      }}
                      onMouseLeave={() => setTooltip(null)}
                      style={{
                        default: { outline: "none" },
                        hover: { fill: match ? "#a7f3d0" : "#334155", outline: "none" },
                        pressed: { outline: "none" },
                      }}
                    />
                  );
                })
              }
            </Geographies>
          </ZoomableGroup>
        </ComposableMap>

        {/* Tooltip */}
        {tooltip && (
          <div className="absolute top-4 right-4 rounded-xl border border-white/10 bg-slate-800/95 backdrop-blur-sm px-4 py-3 pointer-events-none">
            <p className="text-sm font-medium text-white">{tooltip.country}</p>
            <p className="text-xs text-slate-400 mt-1">
              CB Assets: ${tooltip.cb_assets_usd.toFixed(2)}T
            </p>
            {tooltip.buffett_ratio !== null && (
              <p className="text-xs text-slate-400">
                Buffett Ratio: {tooltip.buffett_ratio.toFixed(1)}%
              </p>
            )}
            <p className="text-xs text-emerald-400 mt-1">
              {tooltip.liquidity_contribution_pct.toFixed(1)}% of global
              liquidity
            </p>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 mt-4 justify-center">
        {[
          { label: ">20%", color: "#059669" },
          { label: "10-20%", color: "#10b981" },
          { label: "5-10%", color: "#34d399" },
          { label: "1-5%", color: "#6ee7b7" },
          { label: "<1%", color: "#1e293b" },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-1.5">
            <div
              className="w-3 h-3 rounded-sm"
              style={{ backgroundColor: color }}
            />
            <span className="text-[10px] text-slate-500">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
