'use client';

import { X } from 'lucide-react';

interface LearnMoreModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function LearnMoreModal({ isOpen, onClose }: LearnMoreModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 rounded-2xl border border-white/20 max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-slate-900 border-b border-white/10 p-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white">About Global Liquidity</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition"
          >
            <X className="w-6 h-6 text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 text-gray-300">
          {/* What is Global Liquidity */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">What is Global Liquidity?</h3>
            <p className="leading-relaxed">
              Global liquidity is a measure of the total funding available in the global financial system,
              currently valued at over <span className="text-primary font-semibold">$176 trillion</span>.
              It represents the balance sheet capacity of central banks and financial institutions worldwide.
            </p>
          </section>

          {/* Why It Matters */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">Why Does It Matter?</h3>
            <p className="leading-relaxed mb-3">
              Global liquidity is the primary driver of asset prices - more important than interest rates alone.
              According to Michael Howell's research in "Capital Wars: The Rise of Global Liquidity":
            </p>
            <div className="bg-white/5 border border-white/10 rounded-lg p-4 mb-3">
              <p className="font-mono text-primary text-lg text-center">
                Price = Liquidity × Risk Positioning
              </p>
            </div>
            <p className="leading-relaxed">
              When liquidity expands, asset prices (stocks, crypto, real estate) tend to rise.
              When it contracts, markets typically fall - regardless of fundamentals.
            </p>
          </section>

          {/* The Liquidity Cycle */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">The 65-Month Cycle</h3>
            <p className="leading-relaxed mb-3">
              Global liquidity follows a predictable 5-6 year cycle (approximately 65 months):
            </p>
            <ul className="space-y-2 ml-6">
              <li className="flex items-start gap-2">
                <span className="text-expansion mt-1">▲</span>
                <span><strong className="text-white">Expansion Phase:</strong> Central banks add liquidity through QE and balance sheet expansion</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-1">●</span>
                <span><strong className="text-white">Peak:</strong> Maximum liquidity, markets at highs</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-contraction mt-1">▼</span>
                <span><strong className="text-white">Contraction Phase:</strong> QT and balance sheet reduction</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-gray-400 mt-1">●</span>
                <span><strong className="text-white">Trough:</strong> Minimum liquidity, often market bottoms</span>
              </li>
            </ul>
          </section>

          {/* How We Calculate It */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">How We Calculate GLI</h3>
            <p className="leading-relaxed mb-3">
              The Global Liquidity Index aggregates data from major central banks:
            </p>
            <div className="bg-white/5 border border-white/10 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <p className="text-primary mb-2">GLI Formula:</p>
              <p className="text-white">
                GLI = FED - TGA - RRP + ECB + PBoC + BOJ + BOE + ...
              </p>
              <div className="mt-3 text-xs text-gray-400 space-y-1">
                <p>• FED = Federal Reserve Balance Sheet</p>
                <p>• TGA = Treasury General Account (reduces liquidity)</p>
                <p>• RRP = Reverse Repo (reduces liquidity)</p>
                <p>• ECB, PBoC, BOJ, BOE = Other central bank balance sheets</p>
              </div>
            </div>
          </section>

          {/* Data Sources */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">Data Sources</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white/5 border border-white/10 rounded-lg p-3">
                <p className="font-semibold text-white mb-1">🇺🇸 FRED API</p>
                <p className="text-sm">Federal Reserve Economic Data</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-lg p-3">
                <p className="font-semibold text-white mb-1">🇪🇺 ECB</p>
                <p className="text-sm">European Central Bank</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-lg p-3">
                <p className="font-semibold text-white mb-1">🇨🇳 PBoC</p>
                <p className="text-sm">People's Bank of China</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-lg p-3">
                <p className="font-semibold text-white mb-1">🇯🇵 BOJ</p>
                <p className="text-sm">Bank of Japan</p>
              </div>
            </div>
          </section>

          {/* Credits */}
          <section>
            <h3 className="text-xl font-semibold text-white mb-3">Research Credits</h3>
            <p className="leading-relaxed">
              This tracker is based on groundbreaking research by{' '}
              <span className="text-primary font-semibold">Michael J. Howell</span>, founder of
              CrossBorder Capital and author of{' '}
              <em className="text-white">"Capital Wars: The Rise of Global Liquidity"</em>.
            </p>
            <div className="mt-4 flex gap-3">
              <a
                href="https://www.amazon.com/Capital-Wars-Rise-Global-Liquidity/dp/3030392872"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-primary/20 border border-primary text-primary rounded-lg hover:bg-primary/30 transition text-sm"
              >
                Get the Book
              </a>
              <a
                href="https://capitalwars.substack.com"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-white/5 border border-white/20 text-white rounded-lg hover:bg-white/10 transition text-sm"
              >
                Read Research
              </a>
            </div>
          </section>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-slate-900 border-t border-white/10 p-6">
          <button
            onClick={onClose}
            className="w-full px-6 py-3 bg-primary text-white rounded-lg hover:bg-blue-600 transition font-semibold"
          >
            Got It!
          </button>
        </div>
      </div>
    </div>
  );
}
