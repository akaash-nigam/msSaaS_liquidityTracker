# Global Capital Flows Tracking Framework

## Overview
Global capital flows represent the movement of money for investment, trade, or business operations across international borders. This is the "third pillar" of Michael Howell's liquidity framework.

## 🎯 What Are Capital Flows?

### Definition
Capital flows are cross-border transactions involving financial assets, including:
- **Portfolio Flows**: Stocks, bonds, derivatives
- **Direct Investment**: FDI, M&A
- **Banking Flows**: Loans, deposits, credit
- **Official Flows**: Central bank reserves, government transactions

---

## 📊 Key Metrics to Track

### 1. **Balance of Payments (BOP) Data**

#### Components:
- **Current Account**
  - Trade balance (exports - imports)
  - Primary income (investment income)
  - Secondary income (remittances)

- **Capital Account**
  - Capital transfers
  - Acquisition/disposal of non-financial assets

- **Financial Account** ⭐ (Most Important for Capital Flows)
  - Direct Investment (FDI)
  - Portfolio Investment
  - Financial Derivatives
  - Other Investment (loans, deposits)
  - Reserve Assets

#### Data Sources:
- **IMF Balance of Payments Statistics**
- **World Bank Data**
- **National Central Banks** (Fed, ECB, BoJ, etc.)
- **BIS (Bank for International Settlements)**

### 2. **Cross-Border Banking Flows**

#### Metrics:
- **BIS Locational Banking Statistics**
  - Cross-border bank claims
  - Cross-border bank liabilities
  - By currency, counterparty sector, and country

- **BIS Consolidated Banking Statistics**
  - International claims of banks
  - By nationality of reporting banks

#### Key Indicators:
- US Dollar funding stress
- Euro-dollar market activity
- Offshore banking flows
- Shadow banking cross-border activity

### 3. **Foreign Direct Investment (FDI)**

#### Inflows vs Outflows:
- **FDI Inflows**: Foreign investment into domestic economy
- **FDI Outflows**: Domestic investment abroad
- **Net FDI**: Inflows - Outflows

#### Data Sources:
- UNCTAD World Investment Report
- OECD FDI Statistics
- National investment promotion agencies

### 4. **Portfolio Flows**

#### Equity Flows:
- Foreign purchases of domestic stocks
- Domestic purchases of foreign stocks
- ETF flows (especially emerging markets)

#### Debt Flows:
- Foreign holdings of government bonds
- Corporate bond flows
- Emerging market debt flows

#### Data Sources:
- **EPFR Global** (Fund flow data)
- **ICI (Investment Company Institute)**
- **National securities regulators**
- **Bloomberg, Refinitiv**

### 5. **Currency Flows & FX Markets**

#### Metrics:
- **FX Turnover** (BIS Triennial Survey)
- **Currency Composition of Official Reserves** (IMF COFER)
- **Real Effective Exchange Rates**
- **FX Forward Markets** (future expectations)

#### Key Indicators:
- Dollar dominance (60% of global reserves)
- Currency wars / competitive devaluations
- Capital flight indicators

### 6. **Reserve Assets & Official Flows**

#### Central Bank Reserves:
- Foreign exchange reserves
- Gold reserves
- SDR (Special Drawing Rights)
- IMF reserve position

#### Sovereign Wealth Funds:
- Norway Government Pension Fund
- China Investment Corporation
- Saudi Arabia PIF
- UAE ADIA

### 7. **Derivative Flows**

#### Metrics:
- Cross-border derivative positions
- Currency swaps
- Interest rate swaps
- CDS (Credit Default Swaps)

#### Data Source:
- BIS OTC Derivatives Statistics

---

## 🔍 Analytical Dimensions

### Geographic Flows
Track flows BETWEEN regions:

1. **Developed Markets → Emerging Markets**
   - "Risk-on" indicator
   - Carry trade activity

2. **Emerging Markets → Developed Markets**
   - "Risk-off" / capital flight
   - Flight to safety

3. **US ⟷ Rest of World**
   - Dollar recycling
   - US Treasury flows

4. **China ⟷ Rest of World**
   - Belt & Road Initiative
   - Chinese overseas investment

5. **Europe ⟷ Rest of World**
   - Euro-area cross-border banking

### Sectoral Flows

1. **Banking Sector**
   - Interbank lending
   - Trade finance
   - Correspondent banking

2. **Non-Bank Financial**
   - Asset managers
   - Pension funds
   - Insurance companies

3. **Corporate Sector**
   - M&A flows
   - Repatriation of earnings
   - Supply chain finance

4. **Household Sector**
   - Remittances
   - Personal investment abroad

### Asset Class Flows

1. **Equity**
   - Net equity flows by region
   - Sector rotation

2. **Fixed Income**
   - Government bonds
   - Corporate bonds
   - EM debt

3. **Real Estate**
   - Cross-border property investment
   - REITs

4. **Commodities**
   - Oil money recycling
   - Gold flows

---

## 🎯 Priority Implementation Approach

### Phase 3A: Foundation (Easiest to Implement)

#### 1. US Treasury International Capital (TIC) Data
**Source**: US Treasury Department
**Update**: Monthly
**Free**: Yes

**Key Metrics**:
- Foreign holdings of US securities
- US holdings of foreign securities
- Net foreign purchases of US assets

**FRED Series IDs**:
```
BOGZ1FL263061005Q  - Rest of World Holdings of US Financial Assets
BOGZ1FL263064105Q  - RoW Holdings of US Treasury Securities
BOGZ1FL263063005Q  - RoW Holdings of US Corporate Equities
```

#### 2. IMF Balance of Payments (via FRED)
**Update**: Quarterly
**Free**: Yes

**Example Series**:
```
BOPGSTB  - US Trade Balance
BOPCUBA  - US Current Account Balance
BOPGFAA  - US Financial Account
```

#### 3. BIS Cross-Border Banking Claims
**Source**: BIS.org
**Update**: Quarterly
**Free**: Yes (CSV downloads)

**Key Metrics**:
- Total cross-border claims
- By currency (USD, EUR, JPY, etc.)
- By counterparty country

### Phase 3B: Intermediate (Moderate Complexity)

#### 1. OECD International Investment Position
**Metrics**:
- Net international investment position
- External debt
- FDI positions

#### 2. World Bank Capital Flows Database
**Metrics**:
- Portfolio equity flows
- Portfolio debt flows
- Bank lending flows

#### 3. IIF (Institute of International Finance) Data
**Note**: Paid subscription required
**Coverage**: Emerging market flows

### Phase 3C: Advanced (Most Complex)

#### 1. Real-Time Fund Flow Data
**Sources**:
- EPFR Global (expensive)
- Morningstar
- Bloomberg Terminal

#### 2. High-Frequency Indicators
**Metrics**:
- Daily FX flows estimates
- Crypto cross-border flows
- Real-time payment systems (SWIFT gpi)

#### 3. Alternative Data
**Sources**:
- Shipping data (trade flows proxy)
- Satellite imagery (construction FDI)
- Web scraping (M&A announcements)

---

## 🏗️ Technical Implementation

### Database Schema

```sql
-- Capital Flows Table
CREATE TABLE capital_flows (
    id SERIAL PRIMARY KEY,
    flow_date DATE NOT NULL,
    source_country VARCHAR(3),  -- ISO code
    destination_country VARCHAR(3),
    flow_type VARCHAR(50),  -- 'portfolio_equity', 'fdi', 'banking', etc.
    asset_class VARCHAR(50),  -- 'equity', 'debt', 'derivatives'
    direction VARCHAR(10),  -- 'inflow', 'outflow', 'net'
    amount_usd NUMERIC(18, 2),
    currency VARCHAR(3),
    data_source VARCHAR(100),
    frequency VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_date (flow_date),
    INDEX idx_countries (source_country, destination_country),
    INDEX idx_flow_type (flow_type)
);

-- Aggregated Capital Flow Index
CREATE TABLE capital_flow_index (
    id SERIAL PRIMARY KEY,
    index_date DATE NOT NULL UNIQUE,
    total_global_flows NUMERIC(18, 4),  -- Trillions USD
    dm_to_em_flows NUMERIC(18, 4),
    em_to_dm_flows NUMERIC(18, 4),
    us_net_flows NUMERIC(18, 4),
    china_net_flows NUMERIC(18, 4),
    risk_appetite_score NUMERIC(5, 2),  -- 0-100 score
    change_1m NUMERIC(18, 4),
    change_1m_pct NUMERIC(10, 4),
    data_quality VARCHAR(20)
);
```

### API Endpoints

```python
# Get capital flows by region
@router.get("/capital-flows/regional")
async def get_regional_flows(
    from_region: str,
    to_region: str,
    timeframe: str = "1Y"
)

# Get flows by asset class
@router.get("/capital-flows/asset-class/{asset_class}")
async def get_flows_by_asset(asset_class: str)

# Get capital flow index
@router.get("/capital-flows/index")
async def get_capital_flow_index()

# Get flows for specific country
@router.get("/capital-flows/country/{country_code}")
async def get_country_flows(country_code: str)
```

### Visualization Components

1. **Sankey Diagram**: Show flows between regions
2. **Chord Diagram**: Bilateral flows matrix
3. **World Map**: Heatmap of net flows
4. **Time Series**: Flow trends over time
5. **Risk-On/Risk-Off Indicator**: Flow-based sentiment

---

## 📈 Key Calculated Indicators

### 1. **Global Risk Appetite Index**
```
Risk Score = (EM Inflows / Total Flows) × Weight1
           + (Equity Flows / Debt Flows) × Weight2
           + (HY Flows / IG Flows) × Weight3
```

### 2. **Dollar Recycling Indicator**
```
Dollar Recycling = US Current Account Deficit
                 - Foreign Official Purchases of US Treasuries
```

### 3. **Capital Flight Index**
```
Flight Index = (EM Outflows - EM Inflows) / EM GDP
```

### 4. **Cross-Border Leverage**
```
Leverage = Cross-Border Bank Claims / Global GDP
```

---

## 🚧 Challenges & Dependencies

### Data Challenges

1. **Lagged Reporting**: Most data is 1-3 months delayed
2. **Inconsistent Definitions**: Countries report differently
3. **Data Gaps**: Many flows are unrecorded (dark pools, crypto)
4. **Valuation Effects**: FX moves distort flow measurements
5. **Errors & Omissions**: BOP residual category can be large

### Technical Dependencies

1. **Multiple Data Sources**: Need to integrate 5+ different APIs
2. **Currency Conversion**: Real-time FX rates for normalization
3. **Geographic Mapping**: Country codes, regional aggregations
4. **Data Quality**: Missing data, outliers, revisions
5. **Computation**: Heavy aggregations across dimensions

### API/Data Costs

**Free Sources**:
- FRED (US data)
- BIS (banking flows)
- IMF (BOP data)
- World Bank

**Paid Sources** (if needed for completeness):
- Bloomberg Terminal: $2,000+/month
- EPFR: $20,000+/year
- IIF: $10,000+/year
- Refinitiv: $1,000+/month

---

## 🎯 Recommended Starting Point

### Phase 3A: Minimal Viable Product (Free Data Only)

**Focus on US-centric flows first**:

1. **US Treasury TIC Data** (Monthly)
   - Foreign holdings of US securities
   - Tracks "dollar recycling"
   - Good proxy for global risk appetite

2. **US Balance of Payments** (Quarterly)
   - Current account deficit
   - Financial account flows
   - Direct investment

3. **BIS Cross-Border Banking** (Quarterly)
   - Dollar banking flows
   - European banking flows
   - Emerging market exposure

**Deliverables**:
- Dashboard showing US net capital flows
- Trend charts (risk-on vs risk-off)
- Geographic breakdown (where money is coming from)
- Simple risk appetite indicator

**Estimated Effort**: 2-3 weeks

---

## 📚 Additional Resources

### Academic Research
- Michael Howell: "Capital Wars" (2020)
- Hélène Rey: "Dilemma not Trilemma" (2013)
- Hyun Song Shin (BIS): Dollar funding research

### Data Documentation
- BIS Statistics Explorer: https://stats.bis.org/
- IMF BOP Manual: https://www.imf.org/external/pubs/ft/bop/2007/bopman6.htm
- FRED: https://fred.stlouisfed.org/categories/125

### Tools
- Python: `pandas`, `fredapi`, `wbdata` (World Bank)
- APIs: `requests`, `xmltodict` (for BIS XML data)
- Viz: D3.js (Sankey), `plotly` (maps)

---

## 💡 Next Steps

Would you like me to:

1. **Start with Phase 3A** - Implement US TIC data first?
2. **Create visualizations** - Sankey diagram for capital flows?
3. **Build the database schema** - Set up capital flows tables?
4. **Research specific regions** - Focus on a particular flow (e.g., China-US)?

Let me know which direction you'd like to pursue!
