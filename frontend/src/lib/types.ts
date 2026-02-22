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
