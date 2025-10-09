'use client';

import { ArrowUp, ArrowDown, TrendingUp } from 'lucide-react';

export default function GLIHeroCard() {
  // Mock data - will be replaced with real API data
  const gliData = {
    current: 176.2,
    change1M: 2.4,
    change3M: 5.1,
    changeYoY: 7.8,
    status: 'expanding',
    cycleDay: 1842,
  };

  const isExpanding = gliData.status === 'expanding';

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-lg text-gray-300 mb-2">Global Liquidity Index</h2>
          <div className="flex items-baseline gap-2">
            <span className="text-5xl font-bold text-white">${gliData.current}T</span>
            <span className="text-gray-400 text-lg">USD</span>
          </div>
        </div>
        <div className={`px-4 py-2 rounded-lg ${isExpanding ? 'bg-expansion/20 border border-expansion' : 'bg-contraction/20 border border-contraction'}`}>
          <div className="flex items-center gap-2">
            {isExpanding ? (
              <TrendingUp className="w-5 h-5 text-expansion" />
            ) : (
              <ArrowDown className="w-5 h-5 text-contraction" />
            )}
            <span className={`text-sm font-semibold ${isExpanding ? 'text-expansion' : 'text-contraction'}`}>
              {isExpanding ? 'EXPANDING' : 'CONTRACTING'}
            </span>
          </div>
        </div>
      </div>

      {/* Change Indicators */}
      <div className="grid grid-cols-3 gap-6 mb-6">
        <div>
          <p className="text-gray-400 text-sm mb-1">1 Month Change</p>
          <div className="flex items-center gap-2">
            <ArrowUp className="w-4 h-4 text-expansion" />
            <span className="text-2xl font-semibold text-white">+{gliData.change1M}%</span>
          </div>
        </div>
        <div>
          <p className="text-gray-400 text-sm mb-1">3 Month Change</p>
          <div className="flex items-center gap-2">
            <ArrowUp className="w-4 h-4 text-expansion" />
            <span className="text-2xl font-semibold text-white">+{gliData.change3M}%</span>
          </div>
        </div>
        <div>
          <p className="text-gray-400 text-sm mb-1">Year over Year</p>
          <div className="flex items-center gap-2">
            <ArrowUp className="w-4 h-4 text-expansion" />
            <span className="text-2xl font-semibold text-white">+{gliData.changeYoY}%</span>
          </div>
        </div>
      </div>

      {/* Cycle Position */}
      <div className="border-t border-white/10 pt-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm mb-1">Cycle Position</p>
            <p className="text-white font-semibold">Late Expansion Phase</p>
          </div>
          <div className="text-right">
            <p className="text-gray-400 text-sm mb-1">Days in Cycle</p>
            <p className="text-white font-semibold">Day {gliData.cycleDay} / 1,950</p>
          </div>
        </div>
        {/* Progress bar */}
        <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-expansion to-primary transition-all duration-500"
            style={{ width: `${(gliData.cycleDay / 1950) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}
