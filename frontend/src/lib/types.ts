export interface GliCurrent {
  date: string;
  value: number;
  change_pct: number;
  change_1m_pct: number;
  cycle_position: string;
  num_sources: number;
  cb_value?: number;
  ps_value?: number;
}

export interface GliHistoricalPoint {
  date: string;
  value: number;
}

export interface GliComponent {
  source: string;
  value: number;
  currency: string;
  value_usd: number;
  pct_of_total: number;
}

export interface CycleData {
  current_position: string;
  momentum: number;
  cycle_day: number;
  total_cycle_days: number;
  phase_pct: number;
}

export interface PrivateSectorCurrent {
  date: string;
  total_value: number;
  change_pct: number;
  change_1m_pct: number;
  data_quality: string;
  num_components: number;
  components: {
    m2: number;
    mmf: number;
    commercial_paper: number;
    repos_net: number;
    bank_credit: number;
  };
}

export interface PrivateSectorComponent {
  name: string;
  key: string;
  value: number;
  pct_of_total: number;
}

export interface ExchangeRateData {
  currency: string;
  rate: number;
  change_pct: number;
  date: string;
}

export interface TicData {
  date: string;
  country: string;
  total_holdings: number;
  treasuries: number;
  equities: number;
  corporate_bonds: number;
  agency_bonds: number;
}

export interface BopData {
  date: string;
  country: string;
  current_account_balance: number;
  trade_balance: number;
  financial_account_balance: number;
  net_direct_investment: number;
  net_portfolio_investment: number;
}

export interface StackedLiquidityPoint {
  date: string;
  cb_value: number;
  ps_value: number;
}

export interface MarketIndicatorData {
  name: string;
  series_id: string;
  value: number;
  change: number;
  signal: string;
  category: string;
  unit: string;
}

export interface AssetPriceData {
  asset: string;
  ticker: string;
  price: number;
  change_pct: number;
  asset_class: string;
}

export interface AssetCorrelationData {
  asset: string;
  correlation_30d: number;
  correlation_90d: number;
  correlation_365d: number;
  beta_to_gli: number;
}

export interface ValuationData {
  country: string;
  country_code: string;
  ratio: number;
  gdp_usd: number;
  mcap_usd: number;
  gdp_share?: number;
  mcap_share?: number;
  signal: string;
  date: string;
}

export interface LiquidityFlowRegion {
  region: string;
  flow_type: string;
  amount: number;
  share_pct: number;
  change_pct: number;
  direction: string;
}

export interface LiquidityFlowData {
  date: string;
  total_global_flows: number;
  flows: LiquidityFlowRegion[];
  dm_vs_em: {
    dm_share: number;
    em_share: number;
    dm_to_em_trend: string;
  };
}

export interface HistoricalComparisonPoint {
  year: number;
  ratio: number;
}

export interface HistoricalComparisonData {
  japan: HistoricalComparisonPoint[];
  us: HistoricalComparisonPoint[];
  peak_comparison: {
    japan_peak_year: number;
    japan_peak_ratio: number;
    japan_gdp_share_at_peak?: number;
    japan_mcap_share_at_peak?: number;
    us_current_year: number;
    us_current_ratio: number;
    us_gdp_share?: number;
    us_mcap_share?: number;
    warning: string;
  };
}

export interface FedRrpData {
  date: string;
  current_level_billions: number;
  peak_level_billions: number;
  drawdown_pct: number;
  signal: string;
  historical: { date: string; value: number }[];
  last_updated?: string;
}

export interface FedBalanceSheetPoint {
  date: string;
  treasuries: number;
  mbs: number;
  other: number;
  total: number;
}

export interface FedBalanceSheetData {
  data: FedBalanceSheetPoint[];
  latest: FedBalanceSheetPoint;
  last_updated?: string;
}

export interface DataFreshness {
  gli: string | null;
  private_sector: string | null;
  exchange_rates: string | null;
  market_indicators: string | null;
  asset_prices: string | null;
  capital_flows: string | null;
  valuations: string | null;
}

// Phase C: Cycle-Based Asset Allocation
export interface CycleAllocation {
  asset_class: string;
  weight: number;
  rationale: string;
  color: string;
}

export interface CycleAllocationData {
  cycle_position: string;
  momentum: number;
  allocations: CycleAllocation[];
}

// Phase D: Stablecoin Supply
export interface StablecoinData {
  total_supply: number;
  usdt: { supply: number; change_7d: number; dominance: number };
  usdc: { supply: number; change_7d: number; dominance: number };
  historical: { date: string; usdt: number; usdc: number; total: number }[];
}

// Phase E: World Map
export interface WorldMapCountry {
  country_code: string;
  country: string;
  cb_assets_usd: number;
  buffett_ratio: number | null;
  signal: string;
  liquidity_contribution_pct: number;
}

// Phase F: Correlation Matrix
export interface CorrelationMatrix {
  labels: string[];
  matrix: number[][];
}

// Phase G: Sankey Diagram
export interface SankeyNode {
  id: string;
  name: string;
  category: string;
}

export interface SankeyLink {
  source: string;
  target: string;
  value: number;
}

export interface SankeyData {
  nodes: SankeyNode[];
  links: SankeyLink[];
}

// Phase H: Multi-Timeframe
export interface TimeframePanel {
  timeframe: string;
  gli_data: { date: string; value: number }[];
  change_pct: number;
  high: number;
  low: number;
  current: number;
}

export interface MultiTimeframeData {
  panels: TimeframePanel[];
}
