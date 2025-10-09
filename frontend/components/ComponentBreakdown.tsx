'use client';

import { TrendingUp, TrendingDown } from 'lucide-react';

interface CentralBankData {
  name: string;
  flag: string;
  value: number;
  change: number;
  percentOfTotal: number;
  trend: 'up' | 'down';
}

export default function ComponentBreakdown() {
  // Mock data - will be replaced with real API data
  const centralBanks: CentralBankData[] = [
    { name: 'Federal Reserve (Net)', flag: '🇺🇸', value: 6.8, change: 0.12, percentOfTotal: 38.6, trend: 'up' },
    { name: 'People\'s Bank of China', flag: '🇨🇳', value: 5.2, change: 0.085, percentOfTotal: 29.5, trend: 'up' },
    { name: 'European Central Bank', flag: '🇪🇺', value: 3.1, change: -0.02, percentOfTotal: 17.6, trend: 'down' },
    { name: 'Bank of Japan', flag: '🇯🇵', value: 1.9, change: 0.015, percentOfTotal: 10.8, trend: 'up' },
    { name: 'Bank of England', flag: '🇬🇧', value: 0.8, change: 0.005, percentOfTotal: 4.5, trend: 'up' },
    { name: 'Bank of Canada', flag: '🇨🇦', value: 0.5, change: -0.01, percentOfTotal: 2.8, trend: 'down' },
    { name: 'Reserve Bank of Australia', flag: '🇦🇺', value: 0.4, change: 0.008, percentOfTotal: 2.3, trend: 'up' },
    { name: 'Swiss National Bank', flag: '🇨🇭', value: 0.3, change: 0.002, percentOfTotal: 1.7, trend: 'up' },
  ];

  const totalGLI = centralBanks.reduce((sum, bank) => sum + bank.value, 0);

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-white mb-2">Component Breakdown</h3>
        <p className="text-gray-400 text-sm">Individual central bank contributions to global liquidity</p>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th className="text-left py-3 px-4 text-gray-400 font-medium text-sm">Central Bank</th>
              <th className="text-right py-3 px-4 text-gray-400 font-medium text-sm">Value (T)</th>
              <th className="text-right py-3 px-4 text-gray-400 font-medium text-sm">Change (1M)</th>
              <th className="text-right py-3 px-4 text-gray-400 font-medium text-sm">% of Total</th>
              <th className="text-center py-3 px-4 text-gray-400 font-medium text-sm">Trend</th>
            </tr>
          </thead>
          <tbody>
            {centralBanks.map((bank, index) => (
              <tr
                key={index}
                className="border-b border-white/5 hover:bg-white/5 transition"
              >
                <td className="py-4 px-4">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{bank.flag}</span>
                    <span className="text-white font-medium">{bank.name}</span>
                  </div>
                </td>
                <td className="text-right py-4 px-4">
                  <span className="text-white font-mono">${bank.value.toFixed(1)}T</span>
                </td>
                <td className="text-right py-4 px-4">
                  <span className={`font-mono ${bank.change >= 0 ? 'text-expansion' : 'text-contraction'}`}>
                    {bank.change >= 0 ? '+' : ''}${bank.change.toFixed(3)}T
                  </span>
                </td>
                <td className="text-right py-4 px-4">
                  <div className="flex items-center justify-end gap-2">
                    <span className="text-white font-mono">{bank.percentOfTotal.toFixed(1)}%</span>
                    <div className="w-20 h-2 bg-white/10 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary"
                        style={{ width: `${bank.percentOfTotal}%` }}
                      ></div>
                    </div>
                  </div>
                </td>
                <td className="text-center py-4 px-4">
                  {bank.trend === 'up' ? (
                    <div className="inline-flex items-center gap-1 text-expansion">
                      <TrendingUp className="w-4 h-4" />
                      <span className="text-xs font-semibold">Expanding</span>
                    </div>
                  ) : (
                    <div className="inline-flex items-center gap-1 text-contraction">
                      <TrendingDown className="w-4 h-4" />
                      <span className="text-xs font-semibold">Shrinking</span>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t-2 border-white/20">
              <td className="py-4 px-4 text-white font-bold">Total GLI</td>
              <td className="text-right py-4 px-4">
                <span className="text-white font-bold font-mono">${totalGLI.toFixed(1)}T</span>
              </td>
              <td colSpan={3}></td>
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Legend */}
      <div className="mt-6 flex items-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-expansion"></div>
          <span className="text-gray-400">Expanding</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-contraction"></div>
          <span className="text-gray-400">Contracting</span>
        </div>
        <div className="ml-auto text-gray-400">
          Last updated: {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
        </div>
      </div>
    </div>
  );
}
