'use client';

import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

export default function GLIChart() {
  const [timeframe, setTimeframe] = useState('1Y');

  // Mock data - will be replaced with real API data
  const generateMockData = () => {
    const data = [];
    const baseValue = 150;
    const now = new Date();

    for (let i = 365; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      const randomVariation = Math.sin(i / 30) * 15 + Math.random() * 5;
      data.push({
        date: date.toISOString().split('T')[0],
        value: baseValue + randomVariation + (365 - i) * 0.05,
      });
    }
    return data;
  };

  const data = generateMockData();

  const timeframes = ['1M', '3M', '6M', '1Y', '3Y', '5Y', '10Y', 'ALL'];

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white">Global Liquidity Trend</h3>

        {/* Timeframe Selector */}
        <div className="flex gap-2 bg-white/5 p-1 rounded-lg">
          {timeframes.map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3 py-1 rounded text-sm font-medium transition ${
                timeframe === tf
                  ? 'bg-primary text-white'
                  : 'text-gray-400 hover:text-white hover:bg-white/10'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorGLI" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0066FF" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#0066FF" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
            <XAxis
              dataKey="date"
              stroke="#9CA3AF"
              tick={{ fill: '#9CA3AF' }}
              tickFormatter={(value) => {
                const date = new Date(value);
                return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
              }}
            />
            <YAxis
              stroke="#9CA3AF"
              tick={{ fill: '#9CA3AF' }}
              tickFormatter={(value) => `$${value}T`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: '#fff'
              }}
              labelStyle={{ color: '#9CA3AF' }}
              formatter={(value: any) => [`$${value.toFixed(2)}T`, 'GLI']}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#0066FF"
              strokeWidth={2}
              fill="url(#colorGLI)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Info */}
      <div className="mt-4 flex items-center justify-between text-sm">
        <p className="text-gray-400">
          Showing data from {data[0]?.date} to {data[data.length - 1]?.date}
        </p>
        <button className="text-primary hover:text-blue-400 transition">
          Download Chart ↓
        </button>
      </div>
    </div>
  );
}
