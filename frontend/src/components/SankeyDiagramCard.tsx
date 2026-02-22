"use client";

import useSWR from "swr";
import { API_BASE, fetcher } from "@/lib/api";
import type { SankeyData, SankeyNode, SankeyLink } from "@/lib/types";

const CATEGORY_COLORS: Record<string, string> = {
  source: "#3b82f6",
  channel: "#8b5cf6",
  destination: "#10b981",
};

interface LayoutNode extends SankeyNode {
  x: number;
  y: number;
  height: number;
  totalValue: number;
}

function layoutSankey(
  nodes: SankeyNode[],
  links: SankeyLink[],
  width: number,
  height: number
) {
  const categories = ["source", "channel", "destination"];
  const colX = [40, width / 2 - 40, width - 120];
  const nodeWidth = 20;

  // Group by category
  const grouped: Record<string, SankeyNode[]> = {};
  for (const cat of categories) {
    grouped[cat] = nodes.filter((n) => n.category === cat);
  }

  // Compute total outflow/inflow for each node
  const nodeValues: Record<string, number> = {};
  for (const node of nodes) {
    const outflow = links
      .filter((l) => l.source === node.id)
      .reduce((s, l) => s + l.value, 0);
    const inflow = links
      .filter((l) => l.target === node.id)
      .reduce((s, l) => s + l.value, 0);
    nodeValues[node.id] = Math.max(outflow, inflow);
  }

  // Layout each column
  const layoutNodes: Record<string, LayoutNode> = {};
  for (let col = 0; col < categories.length; col++) {
    const cat = categories[col];
    const group = grouped[cat];
    const totalVal = group.reduce((s, n) => s + (nodeValues[n.id] || 1), 0);
    const usableHeight = height - 40;
    const gap = 8;
    const totalGaps = (group.length - 1) * gap;
    const scale = (usableHeight - totalGaps) / totalVal;

    let y = 20;
    for (const node of group) {
      const h = Math.max(4, (nodeValues[node.id] || 1) * scale);
      layoutNodes[node.id] = {
        ...node,
        x: colX[col],
        y,
        height: h,
        totalValue: nodeValues[node.id] || 1,
      };
      y += h + gap;
    }
  }

  // Build link paths with offsets
  const sourceOffsets: Record<string, number> = {};
  const targetOffsets: Record<string, number> = {};
  for (const id in layoutNodes) {
    sourceOffsets[id] = 0;
    targetOffsets[id] = 0;
  }

  const layoutLinks = links.map((link) => {
    const src = layoutNodes[link.source];
    const tgt = layoutNodes[link.target];
    if (!src || !tgt) return null;

    const srcProportion = link.value / src.totalValue;
    const tgtProportion = link.value / tgt.totalValue;
    const srcH = src.height * srcProportion;
    const tgtH = tgt.height * tgtProportion;

    const y1 = src.y + sourceOffsets[link.source];
    const y2 = tgt.y + targetOffsets[link.target];

    sourceOffsets[link.source] += srcH;
    targetOffsets[link.target] += tgtH;

    const x1 = src.x + nodeWidth;
    const x2 = tgt.x;
    const midX = (x1 + x2) / 2;

    return {
      ...link,
      path: `M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2} L ${x2} ${y2 + tgtH} C ${midX} ${y2 + tgtH}, ${midX} ${y1 + srcH}, ${x1} ${y1 + srcH} Z`,
      color: CATEGORY_COLORS[src.category] || "#3b82f6",
    };
  });

  return { layoutNodes, layoutLinks: layoutLinks.filter(Boolean) };
}

export default function SankeyDiagramCard() {
  const { data } = useSWR<SankeyData>(
    `${API_BASE}/analytics/sankey-flows`,
    fetcher
  );

  if (!data) {
    return (
      <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 animate-pulse">
        <div className="h-4 w-48 bg-slate-700 rounded mb-6" />
        <div className="h-80 bg-slate-800 rounded-xl" />
      </div>
    );
  }

  const svgWidth = 700;
  const svgHeight = 400;
  const { layoutNodes, layoutLinks } = layoutSankey(
    data.nodes,
    data.links,
    svgWidth,
    svgHeight
  );
  const nodeWidth = 20;

  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Liquidity Flow Sankey
        </h2>
        <div className="flex items-center gap-3">
          {Object.entries(CATEGORY_COLORS).map(([cat, color]) => (
            <div key={cat} className="flex items-center gap-1">
              <div
                className="w-2.5 h-2.5 rounded-full"
                style={{ backgroundColor: color }}
              />
              <span className="text-[10px] text-slate-500 capitalize">
                {cat === "source" ? "CB Sources" : cat === "channel" ? "Channels" : "Destinations"}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto">
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          className="w-full"
          style={{ minWidth: 500 }}
        >
          {/* Links */}
          {layoutLinks.map((link, i) => (
            <path
              key={i}
              d={link!.path}
              fill={link!.color}
              fillOpacity={0.15}
              stroke={link!.color}
              strokeOpacity={0.4}
              strokeWidth={0.5}
            />
          ))}

          {/* Nodes */}
          {Object.values(layoutNodes).map((node) => (
            <g key={node.id}>
              <rect
                x={node.x}
                y={node.y}
                width={nodeWidth}
                height={node.height}
                rx={4}
                fill={CATEGORY_COLORS[node.category] || "#3b82f6"}
                fillOpacity={0.8}
              />
              <text
                x={
                  node.category === "destination"
                    ? node.x + nodeWidth + 6
                    : node.category === "source"
                    ? node.x - 6
                    : node.x + nodeWidth / 2
                }
                y={node.y + node.height / 2}
                textAnchor={
                  node.category === "destination"
                    ? "start"
                    : node.category === "source"
                    ? "end"
                    : "middle"
                }
                dominantBaseline="central"
                className="fill-slate-300"
                fontSize={10}
                fontWeight={500}
              >
                {node.name}
              </text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
}
