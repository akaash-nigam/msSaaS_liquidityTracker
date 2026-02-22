"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSWRConfig } from "swr";
import { API_BASE } from "@/lib/api";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard" },
  { href: "/markets", label: "Markets" },
  { href: "/analytics", label: "Analytics" },
] as const;

export default function NavigationBar() {
  const pathname = usePathname();
  const { mutate } = useSWRConfig();
  const [refreshing, setRefreshing] = useState(false);
  const [refreshStatus, setRefreshStatus] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);

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
    <header className="border-b border-white/5 bg-[#0a0a1a] sticky top-0 z-50">
      <div className="mx-auto max-w-7xl px-6 py-3">
        <div className="flex items-center justify-between">
          {/* Left: title + nav */}
          <div className="flex items-center gap-6">
            <div>
              <h1 className="text-lg font-bold text-white tracking-tight">
                Global Liquidity Tracker
              </h1>
              <p className="text-[10px] text-slate-500">
                Powered by FRED &middot; Michael Howell Framework
              </p>
            </div>

            {/* Desktop nav */}
            <nav className="hidden md:flex items-center gap-1">
              {NAV_ITEMS.map((item) => {
                const isActive =
                  item.href === "/"
                    ? pathname === "/"
                    : pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                      isActive
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        : "text-slate-400 hover:text-white hover:bg-slate-800"
                    }`}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Right: actions */}
          <div className="flex items-center gap-3">
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
            <span className="inline-block h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-slate-500">Live</span>

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-1.5 text-slate-400 hover:text-white"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                {mobileOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile nav */}
        {mobileOpen && (
          <nav className="md:hidden flex gap-1 pt-3 border-t border-white/5 mt-3">
            {NAV_ITEMS.map((item) => {
              const isActive =
                item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                    isActive
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        )}
      </div>
    </header>
  );
}
