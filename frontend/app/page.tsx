'use client';

import { useEffect, useState } from 'react';
import GLIHeroCard from '@/components/GLIHeroCard';
import GLIChart from '@/components/GLIChart';
import ComponentBreakdown from '@/components/ComponentBreakdown';

export default function Home() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate initial load
    setTimeout(() => setLoading(false), 1000);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Global Liquidity Data...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm bg-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Global Liquidity Tracker</h1>
              <p className="text-sm text-gray-400 mt-1">Real-time monitoring of the $176T liquidity cycle</p>
            </div>
            <div className="flex gap-4">
              <button className="px-4 py-2 text-sm text-white hover:bg-white/10 rounded-lg transition">
                Learn More
              </button>
              <button className="px-4 py-2 text-sm bg-primary text-white rounded-lg hover:bg-blue-600 transition">
                Sign In
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* GLI Hero Card */}
        <div className="mb-8">
          <GLIHeroCard />
        </div>

        {/* GLI Chart */}
        <div className="mb-8">
          <GLIChart />
        </div>

        {/* Component Breakdown */}
        <div className="mb-8">
          <ComponentBreakdown />
        </div>

        {/* Footer Info */}
        <div className="text-center text-gray-400 text-sm py-8">
          <p>Data sources: Federal Reserve, ECB, BOJ, PBoC, and other major central banks</p>
          <p className="mt-2">Based on research by Michael J. Howell - "Capital Wars: The Rise of Global Liquidity"</p>
        </div>
      </div>
    </main>
  );
}
