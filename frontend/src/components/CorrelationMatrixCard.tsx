"use client";

import { useState } from "react";
import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { CorrelationMatrix } from "@/lib/types";

function getCellColor(value: number): string {
  if (value >= 0.8) return "rgba(16, 185, 129, 0.9)";
  if (value >= 0.5) return "rgba(16, 185, 129, 0.6)";
  if (value >= 0.2) return "rgba(16, 185, 129, 0.3)";
  if (value > -0.2) return "rgba(100, 116, 139, 0.2)";
  if (value > -0.5) return "rgba(239, 68, 68, 0.3)";
  if (value > -0.8) return "rgba(239, 68, 68, 0.6)";
  return "rgba(239, 68, 68, 0.9)";
}

function getTextColor(value: number): string {
  if (Math.abs(value) >= 0.5) return "#ffffff";
  return "#94a3b8";
}

export default function CorrelationMatrixCard() {
  const { data } = useSWR<CorrelationMatrix>(
    `${API_BASE}/analytics/correlation-matrix`,
    fetcher
  );
  const [hover, setHover] = useState<{ row: number; col: number } | null>(null);

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-48 bg-slate-700 rounded mb-6" />
        <div className="h-80 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  const { labels, matrix } = data;
  const n = labels.length;

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Asset Correlation Matrix
        </h2>
        {hover !== null && (
          <span className="text-xs text-slate-400">
            {labels[hover.row]} vs {labels[hover.col]}:{" "}
            <span className="font-semibold text-white">
              {matrix[hover.row][hover.col].toFixed(2)}
            </span>
          </span>
        )}
      </div>

      <div className="overflow-x-auto">
        <div
          className="grid gap-1 mx-auto"
          style={{
            gridTemplateColumns: `56px repeat(${n}, 1fr)`,
            maxWidth: `${56 + n * 56}px`,
          }}
        >
          {/* Top-left empty cell */}
          <div />
          {/* Column headers */}
          {labels.map((label) => (
            <div
              key={`col-${label}`}
              className="text-[10px] font-medium text-slate-400 text-center py-1"
            >
              {label}
            </div>
          ))}

          {/* Rows */}
          {matrix.map((row, i) => (
            <>
              {/* Row label */}
              <div
                key={`row-label-${i}`}
                className="text-[10px] font-medium text-slate-400 flex items-center justify-end pr-2"
              >
                {labels[i]}
              </div>
              {/* Cells */}
              {row.map((value, j) => (
                <div
                  key={`cell-${i}-${j}`}
                  className="aspect-square rounded-md flex items-center justify-center cursor-default transition-transform hover:scale-110"
                  style={{
                    backgroundColor: getCellColor(value),
                    color: getTextColor(value),
                  }}
                  onMouseEnter={() => setHover({ row: i, col: j })}
                  onMouseLeave={() => setHover(null)}
                >
                  <span className="text-[10px] font-mono font-medium tabular-nums">
                    {value.toFixed(2)}
                  </span>
                </div>
              ))}
            </>
          ))}
        </div>
      </div>

      {/* Color scale legend */}
      <div className="flex items-center justify-center gap-2 mt-4">
        <span className="text-[10px] text-slate-500">-1.0</span>
        <div className="flex h-2 rounded-full overflow-hidden w-40">
          <div className="flex-1" style={{ backgroundColor: "rgba(239, 68, 68, 0.9)" }} />
          <div className="flex-1" style={{ backgroundColor: "rgba(239, 68, 68, 0.5)" }} />
          <div className="flex-1" style={{ backgroundColor: "rgba(100, 116, 139, 0.2)" }} />
          <div className="flex-1" style={{ backgroundColor: "rgba(16, 185, 129, 0.5)" }} />
          <div className="flex-1" style={{ backgroundColor: "rgba(16, 185, 129, 0.9)" }} />
        </div>
        <span className="text-[10px] text-slate-500">+1.0</span>
      </div>
    </div>
  );
}
