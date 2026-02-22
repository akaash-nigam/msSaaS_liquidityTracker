# Global Liquidity Tracker — Feature Workplan

## Current State (Complete)

| Section | Components | Endpoints | Status |
|---------|-----------|-----------|--------|
| GLI (7 Central Banks) | HeroCard, Chart, StackedChart, ComponentsTable, CycleGauge | 5 | Done |
| Private Sector (TPSL) | HeroCard, Chart, Table | 3 | Done |
| Exchange Rates | Table (6 currencies) | 1 | Done |
| Capital Flows | TIC + BOP Card | 2 | Done |
| Liquidity Destination | Valuation Heatmap, Flow Direction, Japan Parallel | 3 | Done |
| Market Indicators | 7-indicator grid (VIX, spreads, inflation) | 1 | Done |
| Asset Correlations | Prices + correlation table (SPX, Gold, BTC) | 2 | Done |
| Data Refresh | Header button with SWR revalidation | 1 | Done |
| **Totals** | **16 components** | **18 data endpoints** | **All mock + real FRED ready** |

---

## Phase 6: Missing Liquidity Sources

**Priority: HIGH — These are critical data gaps for a complete liquidity picture.**

### 6A. Fed Reverse Repo (RRP) Facility
- **Why**: The ON RRP facility is the single best daily indicator of excess liquidity in the system. When RRP drains, liquidity enters risk assets.
- **FRED Series**: `RRPONTSYD` (Overnight RRP), `WLRRAL` (RRP awards)
- **Scope**: 1 new endpoint (`GET /fed-rrp/current`), 1 component showing current level + historical drawdown chart
- **Effort**: Small — follows existing chart pattern exactly

### 6B. PBOC (People's Bank of China)
- **Why**: China is 17% of world GDP. Without PBOC, the "global" liquidity index is really a G7 index.
- **Data**: FRED has limited PBOC data. May need mock with manual updates or alternative API.
- **Scope**: Add to `CENTRAL_BANK_SERIES`, update GLI calculation to include 8th bank
- **Effort**: Medium — need to handle CNY exchange rate and data availability

### 6C. Stablecoin Supply (USDT + USDC)
- **Why**: Stablecoin market cap ($150B+) is a direct measure of crypto-native liquidity. When stablecoins grow, crypto rallies.
- **Data**: CoinGecko or DeFiLlama API (free tier)
- **Scope**: New service, 1 endpoint, 1 component
- **Effort**: Medium — new API integration, not FRED

### 6D. Fed Balance Sheet Decomposition
- **Why**: Not just total assets — break out Treasuries vs MBS vs loans. QT pace matters.
- **FRED Series**: `TREAST` (Treasuries held), `MBST` (MBS held), `H41RESPPALDKNWW` (total assets weekly)
- **Scope**: Expand existing FED data, add stacked chart showing composition
- **Effort**: Small

---

## Phase 7: Real FRED Data Activation

**Priority: HIGH — The entire FRED pipeline is built, just needs a key.**

### 7A. Switch from Mock to Real Data
- Set `USE_MOCK_DATA=False` and add `FRED_API_KEY` to `.env`
- Run all ingestion scripts with real data
- Verify data quality and fix any unit conversion issues
- **Effort**: Small — infrastructure is already built

### 7B. Scheduled Data Ingestion
- Add cron job or APScheduler to auto-refresh data daily
- Backend: Add `BackgroundScheduler` to main.py startup
- Schedule: Central banks weekly, exchange rates daily, market indicators daily
- **Effort**: Small

### 7C. Data Freshness Indicators
- Show "last updated" timestamp on each section
- Warn if data is stale (>24h for daily series, >7d for weekly)
- **Effort**: Small — add `last_updated` to each endpoint response

---

## Phase 8: Portfolio & Allocation Tools

**Priority: MEDIUM — Transforms the dashboard from informational to actionable.**

### 8A. Cycle-Based Asset Allocation
- **Why**: Michael Howell's framework maps liquidity cycle phases to optimal asset allocations (expansion → equities, contraction → bonds/gold)
- **UI**: Recommended allocation pie chart based on current cycle position
- **Logic**: Map `cycle_position` → allocation weights (hardcoded Howell rules)
- **Effort**: Medium

### 8B. Liquidity Regime Alerts
- **Why**: Notify when GLI crosses key thresholds or cycle phases change
- **Scope**: In-browser notifications (toast), optional email via SendGrid
- **Triggers**: GLI crosses ±2% monthly, cycle phase changes, VIX > 30, yield curve inverts
- **Effort**: Medium

### 8C. Custom Watchlist
- **Why**: Users want to track specific indicators they care about
- **Scope**: LocalStorage-based watchlist, pinned indicators on top of dashboard
- **Effort**: Small — frontend only

---

## Phase 9: Advanced Visualizations

**Priority: MEDIUM — Improve insight density.**

### 9A. Global Liquidity Heatmap (World Map)
- **Why**: Geographic visualization of where liquidity is concentrated
- **Library**: react-simple-maps or d3-geo
- **Data**: Already have 10 countries with Buffett Indicator + 7 central banks
- **Effort**: Medium — new dependency, but data already exists

### 9B. Correlation Matrix Heatmap
- **Why**: See how all assets/indicators correlate with each other, not just vs GLI
- **UI**: NxN heatmap with color intensity (like a quant correlation matrix)
- **Data**: Expand `asset_correlations` to cross-asset (SPX-Gold, SPX-BTC, Gold-BTC)
- **Effort**: Medium

### 9C. Liquidity Flow Sankey Diagram
- **Why**: Show flows from central banks → private sector → asset classes → regions
- **Library**: d3-sankey or recharts-sankey
- **Effort**: Large — complex visualization, new dependency

### 9D. Multi-Timeframe Dashboard
- **Why**: See 1M, 1Y, 5Y views simultaneously instead of toggling
- **UI**: 3-panel layout with sparklines for quick comparison
- **Effort**: Small — reuse existing chart components with fixed timeframes

---

## Phase 10: Infrastructure & Production

**Priority: LOW for demo, HIGH for production.**

### 10A. Docker Containers
- Dockerfile for backend (Python + uvicorn)
- Dockerfile for frontend (Node build → nginx)
- Update docker-compose to run full stack
- **Effort**: Small

### 10B. Testing
- Backend: pytest for endpoints (mock DB session)
- Frontend: Jest + React Testing Library for components
- E2E: Playwright for critical paths
- **Effort**: Large

### 10C. CI/CD Pipeline
- GitHub Actions: lint → test → build → deploy
- Auto-deploy to Cloud Run on push to main
- **Effort**: Medium

### 10D. Monitoring & Logging
- Structured logging (structlog or loguru)
- Error tracking (Sentry)
- `/metrics` endpoint for Prometheus
- **Effort**: Medium

### 10E. Authentication
- Simple API key auth or OAuth2 (Google) for premium features
- Rate limiting per API key
- **Effort**: Medium

---

## Recommended Implementation Order

```
NOW (Quick Wins):
  Phase 6A — Fed RRP Facility (small, high value)
  Phase 7A — Switch to real FRED data
  Phase 7C — Data freshness indicators

NEXT (Core Value):
  Phase 6D — Fed balance sheet decomposition
  Phase 6B — PBOC integration
  Phase 8A — Cycle-based asset allocation
  Phase 7B — Scheduled ingestion

LATER (Enhancement):
  Phase 8B — Liquidity regime alerts
  Phase 8C — Custom watchlist
  Phase 9A — World map heatmap
  Phase 9D — Multi-timeframe dashboard
  Phase 6C — Stablecoin supply

PRODUCTION:
  Phase 10A — Docker containers
  Phase 10B — Testing
  Phase 10C — CI/CD
  Phase 10D — Monitoring
```

---

## Quick Reference: FRED Series Not Yet Used

| Series | Name | Phase |
|--------|------|-------|
| `RRPONTSYD` | Overnight RRP | 6A |
| `TREAST` | Fed Treasury Holdings | 6D |
| `MBST` | Fed MBS Holdings | 6D |
| `BOGZ1FL263090005Q` | ROW Total Financial Assets | Already ingested |
| `BUSLOANS` | C&I Loans | Mapped, not displayed |
| `TOTALSL` | Consumer Credit | Mapped, not displayed |
| `DPSACBW027SBOG` | Bank Deposits | Mapped, not displayed |
| `WTREGEN` | Treasury General Account (TGA) | Mapped, not displayed |
| `M2V` | Velocity of M2 | Mapped, not displayed |
