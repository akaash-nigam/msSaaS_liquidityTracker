# Extended Liquidity Metrics Implementation Plan

## Overview
This document outlines the plan to expand from the basic GLI (Fed - TGA - RRP) to Michael Howell's comprehensive liquidity framework tracking 60+ metrics across 80+ economies.

## Current Implementation Status
- ✅ Federal Reserve Balance Sheet (WALCL)
- ✅ Treasury General Account (WDTGAL)
- ✅ Reverse Repo Program (RRPONTSYD)
- ✅ Basic GLI calculation (Fed - TGA - RRP)

## Phase 1: Core Central Bank Liquidity Expansion

### Priority 1A: Major Central Banks (Week 1-2)
**European Central Bank (ECB)**
- Total Assets (ECB balance sheet)
- Deposit Facility
- Main Refinancing Operations
- Data Source: ECB Statistical Data Warehouse (SDW)
- API: https://sdw-wsrest.ecb.europa.eu/

**Bank of Japan (BOJ)**
- Total Assets
- Japanese Government Bonds held
- ETF/REIT holdings
- Data Source: BOJ Time-Series Data Search
- API: https://www.stat-search.boj.or.jp/

**People's Bank of China (PBoC)**
- Total Assets
- Foreign Exchange Reserves
- Required Reserve Ratio effects
- Data Source: PBoC statistics, SAFE
- Note: May need web scraping or manual updates

**Bank of England (BOE)**
- Total Assets
- Asset Purchase Facility
- Reserve Balances
- Data Source: BOE Statistics
- API: https://www.bankofengland.co.uk/boeapps/database/

### Priority 1B: Other Major Central Banks (Week 3)
- Swiss National Bank (SNB)
- Bank of Canada (BOC)
- Reserve Bank of Australia (RBA)
- Reserve Bank of India (RBI)

### Data Structure Addition
```python
# Extend central_bank_data table
class CentralBankData(Base):
    source = Column(String(10))  # 'FED', 'ECB', 'BOJ', 'PBOC', 'BOE', etc.
    indicator = Column(String(50))  # 'balance_sheet', 'tga', 'rrp', 'etf_holdings', etc.
    region = Column(String(20))  # 'Americas', 'Europe', 'Asia', 'Emerging'
    category = Column(String(30))  # 'central_bank', 'private_sector', 'cross_border'
```

## Phase 2: Private Sector Liquidity Metrics

### Priority 2A: Shadow Banking (Week 4)
**Money Market Funds**
- Total Assets in MMFs
- FRED Series: MMMFFAQ027S
- Prime vs Government MMF breakdown

**Repo Market Activity**
- Tri-party repo volume
- FRED Series: REPO (various)
- SOFR rates and volumes

**Commercial Paper**
- Total CP outstanding
- FRED Series: COMPOUT
- Asset-backed vs unsecured breakdown

**Margin Debt**
- NYSE margin debt
- FINRA margin statistics

### Priority 2B: Traditional Banking (Week 5)
**Bank Credit**
- Total bank credit (FRED: TOTBKCR)
- Commercial & Industrial loans (FRED: BUSLOANS)
- Real estate loans (FRED: REALLN)
- Consumer credit (FRED: TOTALSL)

**Deposits & Funding**
- M2 Money Supply (FRED: M2SL)
- Savings deposits (FRED: SAVINGS)
- Time deposits (FRED: TDSL)

## Phase 3: Credit & Risk Metrics

### Priority 3A: Credit Spreads (Week 6)
**Investment Grade Spreads**
- ICE BofA US Corporate Index OAS (FRED: BAMLC0A0CM)
- AAA Corporate Bond Yield Spread (FRED: AAA10Y)

**High Yield Spreads**
- ICE BofA US High Yield OAS (FRED: BAMLH0A0HYM2)

**Other Spreads**
- TED Spread (3M LIBOR - 3M T-Bill)
- SOFR-OIS Spread
- Mortgage spreads

### Priority 3B: Volatility & Risk (Week 6)
**Bond Market Volatility**
- MOVE Index (Merrill Option Volatility Estimate)
- 10Y Treasury Volatility

**Equity Volatility**
- VIX Index (CBOE)
- Credit default swap indices

## Phase 4: Cross-Border Flows

### Priority 4A: International Flows (Week 7)
**FX Reserves**
- Global FX reserves (IMF COFER data)
- Country-specific reserves

**Capital Flows**
- TIC (Treasury International Capital) flows
- FRED: BOGZ1FL263064105Q (Net US portfolio flows)
- Portfolio equity vs debt flows

**Offshore Dollar Liquidity**
- Eurodollar deposits
- Non-US bank dollar holdings
- BIS cross-border banking statistics

### Priority 4B: FX Swaps (Week 7)
- FX swap market volumes
- Basis swap spreads
- Central bank swap lines usage

## Phase 5: Regional & Country-Specific Indices

### Priority 5A: Regional Aggregates (Week 8)
**Americas Liquidity Index**
- US (70% weight)
- Canada, Mexico, Brazil (30% combined)

**Europe Liquidity Index**
- Eurozone (60%)
- UK (25%)
- Switzerland, Norway, Sweden (15%)

**Asia Liquidity Index**
- China (40%)
- Japan (35%)
- India, Korea, Australia (25%)

**Emerging Markets Index**
- Major EM central banks
- EM cross-border flows

### Priority 5B: Top 20 Countries (Week 9-10)
Individual country tracking for:
1. United States
2. Eurozone
3. China
4. Japan
5. United Kingdom
6. India
7. Canada
8. Australia
9. South Korea
10. Brazil
11. Mexico
12. Switzerland
13. Saudi Arabia
14. Russia (if data available)
15. Indonesia
16. Turkey
17. Taiwan
18. Thailand
19. Singapore
20. Hong Kong

## Phase 6: Advanced Analytics

### Priority 6A: Liquidity Quality Metrics (Week 11)
**Public vs Private Mix**
- Ratio of central bank liquidity to private sector liquidity
- Quality index for FX implications

**Multiplier Analysis**
- Shadow monetary base calculation
- Liquidity multiplier (currently ~1.7x)

**Diffusion Indexes**
- Z-score standardization of metrics
- Breadth of liquidity expansion/contraction

### Priority 6B: Cycle Position Indicators (Week 12)
**Four Investment Zones**
1. Rebound (liquidity rising, spreads tight)
2. Calm (liquidity high, stable)
3. Speculation (liquidity peaking, spreads widening)
4. Turbulence (liquidity falling, spreads wide)

**Leading Indicators**
- 3-6 month forward projections
- Momentum oscillators
- Rate of change metrics

**Cycle Timer**
- 65-month cycle tracking
- Current position in cycle
- Historical cycle comparisons

## Database Schema Extensions

### New Tables

```sql
-- Private sector liquidity data
CREATE TABLE private_sector_liquidity (
    id SERIAL PRIMARY KEY,
    indicator VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),  -- 'shadow_banking', 'traditional_banking', 'corporate'
    date DATE NOT NULL,
    value NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(indicator, date)
);

-- Credit and risk metrics
CREATE TABLE credit_risk_metrics (
    id SERIAL PRIMARY KEY,
    metric_type VARCHAR(50) NOT NULL,  -- 'spread', 'volatility', 'cds'
    instrument VARCHAR(100),  -- 'IG_Corporate', 'HY', 'TED', 'MOVE'
    date DATE NOT NULL,
    value NUMERIC(10, 4) NOT NULL,
    unit VARCHAR(20) DEFAULT 'bps',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(metric_type, instrument, date)
);

-- Cross-border flows
CREATE TABLE cross_border_flows (
    id SERIAL PRIMARY KEY,
    flow_type VARCHAR(50) NOT NULL,  -- 'portfolio_equity', 'portfolio_debt', 'banking', 'fx_reserves'
    from_region VARCHAR(50),
    to_region VARCHAR(50),
    date DATE NOT NULL,
    value NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Regional liquidity indices
CREATE TABLE regional_liquidity_index (
    id SERIAL PRIMARY KEY,
    region VARCHAR(50) NOT NULL,  -- 'Americas', 'Europe', 'Asia', 'EM'
    index_type VARCHAR(50) NOT NULL,  -- 'total', 'central_bank', 'private', 'cross_border'
    date DATE NOT NULL,
    value NUMERIC(15, 2) NOT NULL,
    change_1m NUMERIC(10, 4),
    change_3m NUMERIC(10, 4),
    change_1y NUMERIC(10, 4),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(region, index_type, date)
);

-- Country-specific indices
CREATE TABLE country_liquidity_index (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) NOT NULL,  -- ISO 3166-1 alpha-3
    country_name VARCHAR(100),
    index_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    value NUMERIC(15, 2) NOT NULL,
    weight_in_global NUMERIC(5, 4),  -- % weight in global index
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(country_code, index_type, date)
);

-- Cycle position tracking
CREATE TABLE liquidity_cycle_position (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    zone VARCHAR(20) NOT NULL,  -- 'Rebound', 'Calm', 'Speculation', 'Turbulence'
    momentum NUMERIC(10, 4),
    cycle_day INTEGER,  -- Day number in 65-month (1975-day) cycle
    quality_index NUMERIC(10, 4),  -- Public vs private mix
    multiplier NUMERIC(5, 2),  -- Current liquidity multiplier
    leading_indicator NUMERIC(10, 4),  -- 3-6 month forward signal
    created_at TIMESTAMP DEFAULT NOW()
);

-- TimescaleDB hypertables
SELECT create_hypertable('private_sector_liquidity', 'date');
SELECT create_hypertable('credit_risk_metrics', 'date');
SELECT create_hypertable('cross_border_flows', 'date');
SELECT create_hypertable('regional_liquidity_index', 'date');
SELECT create_hypertable('country_liquidity_index', 'date');
SELECT create_hypertable('liquidity_cycle_position', 'date');
```

## API Endpoints to Add

### Regional Endpoints
```
GET /api/v1/liquidity/regional
  ?region=Americas|Europe|Asia|EM
  &timeframe=1M|3M|6M|1Y|3Y|5Y

GET /api/v1/liquidity/regional/breakdown
  ?region=Americas
```

### Country-Specific Endpoints
```
GET /api/v1/liquidity/country/{country_code}
  ?timeframe=1M|3M|6M|1Y|3Y|5Y

GET /api/v1/liquidity/countries/compare
  ?countries=USA,CHN,JPN,EUR
```

### Private Sector Endpoints
```
GET /api/v1/liquidity/private-sector
  ?category=shadow_banking|traditional_banking|corporate

GET /api/v1/liquidity/private-sector/breakdown
```

### Credit & Risk Endpoints
```
GET /api/v1/liquidity/credit-spreads
  ?type=IG|HY|all

GET /api/v1/liquidity/risk-metrics
  ?metrics=spreads,volatility,cds
```

### Cross-Border Endpoints
```
GET /api/v1/liquidity/cross-border
  ?flow_type=portfolio|banking|fx_reserves

GET /api/v1/liquidity/cross-border/flows
  ?from=US&to=EM
```

### Cycle Analytics Endpoints
```
GET /api/v1/liquidity/cycle/current
  # Returns current zone, momentum, cycle position

GET /api/v1/liquidity/cycle/history
  # Historical cycle positions

GET /api/v1/liquidity/cycle/forecast
  # 3-6 month forward indicators
```

### Advanced Analytics Endpoints
```
GET /api/v1/liquidity/quality-index
  # Public vs private liquidity mix

GET /api/v1/liquidity/multiplier
  # Current liquidity multiplier

GET /api/v1/liquidity/diffusion
  # Breadth indicators
```

## Data Sources & APIs

### Free/Public Sources
1. **FRED API** (Federal Reserve Economic Data)
   - 500+ relevant series
   - Already integrated

2. **ECB Statistical Data Warehouse**
   - Free API access
   - Comprehensive European data

3. **Bank of Japan**
   - Free API
   - English data available

4. **Bank of England**
   - Free API
   - Historical data back to 1694

5. **BIS (Bank for International Settlements)**
   - Global banking statistics
   - Cross-border flow data
   - Free download (no API)

6. **IMF Data**
   - COFER (FX reserves)
   - IFS (International Financial Statistics)
   - Free API access

7. **World Bank Data**
   - Country economic indicators
   - Free API

### Paid/Premium Sources (Future)
1. **Bloomberg Terminal**
   - Real-time credit spreads
   - Advanced derivatives data
   - $24,000/year per terminal

2. **Refinitiv Eikon**
   - Alternative to Bloomberg
   - $22,000/year

3. **CrossBorder Capital GLI™**
   - The actual proprietary indices
   - Pricing on request
   - Could license for premium tier

4. **Quandl/Nasdaq Data Link**
   - Alternative data sources
   - Some free, some paid

## Frontend UI Extensions

### New Dashboard Components

1. **Regional Liquidity Map**
   - Interactive world map
   - Color-coded by liquidity growth
   - Click for country detail

2. **Liquidity Cycle Clock**
   - Visual 65-month cycle representation
   - Current position indicator
   - Historical cycle overlays

3. **Three Pillars Chart**
   - Stacked area chart
   - Central Bank (blue)
   - Private Sector (green)
   - Cross-Border (purple)

4. **Quality Index Gauge**
   - Public vs Private liquidity mix
   - FX market implications

5. **Credit Spreads Dashboard**
   - Multiple spread charts
   - TED, SOFR, IG, HY
   - Historical percentiles

6. **Investment Zone Indicator**
   - Large visual indicator
   - Current zone: Rebound/Calm/Speculation/Turbulence
   - Recommended asset positioning

7. **Country Comparison Table**
   - Sortable by liquidity growth
   - Filters by region
   - Export functionality

8. **Advanced Analytics Page**
   - Multiplier trends
   - Diffusion indices
   - Leading indicators
   - Forecasting models

## Implementation Timeline

### Weeks 1-2: Core Central Bank Expansion
- Integrate ECB, BOJ, PBoC, BOE data
- Update database schema
- Create new API endpoints
- Update GLI calculation to include all central banks

### Weeks 3-4: Private Sector Liquidity
- Add shadow banking metrics
- Add traditional banking metrics
- Create private sector endpoints
- Build private sector UI components

### Weeks 5-6: Credit & Risk Metrics
- Integrate credit spread data
- Add volatility metrics
- Create risk dashboard
- Build credit spreads charts

### Weeks 7-8: Cross-Border & Regional
- Add cross-border flow data
- Create regional indices
- Build regional map UI
- Add country comparison tools

### Weeks 9-10: Country-Specific Tracking
- Add top 20 countries
- Country detail pages
- Comparison tools
- Export functionality

### Weeks 11-12: Advanced Analytics
- Cycle position tracking
- Quality index
- Multiplier calculations
- Leading indicators
- Forecasting models

## Success Metrics

1. **Data Coverage**
   - ✅ Target: 60+ distinct liquidity metrics
   - ✅ Target: 80+ countries tracked
   - ✅ Target: 10+ years of historical data

2. **Update Frequency**
   - Daily updates for available metrics
   - Weekly for less frequent data
   - Monthly for country-specific indices

3. **Accuracy**
   - Match CrossBorder Capital methodology where published
   - Validate against known academic research
   - Document any methodology differences

4. **User Engagement**
   - Track which metrics are most viewed
   - Monitor dashboard interaction patterns
   - Collect user feedback on additional desired metrics

## Next Steps

1. **Immediate (This Week)**
   - Begin ECB API integration
   - Set up BOJ data fetching
   - Create extended database schema
   - Document ECB/BOJ data series IDs

2. **Short-term (Next 2 Weeks)**
   - Complete Phase 1 central bank expansion
   - Build regional aggregation logic
   - Update frontend to show new data
   - Create regional breakdown UI

3. **Medium-term (Next Month)**
   - Add private sector metrics
   - Build credit spreads tracking
   - Create cycle position calculator
   - Launch beta of extended metrics

## Resources & References

1. **Michael Howell's Work**
   - "Capital Wars: The Rise of Global Liquidity" (2020)
   - Capital Wars Substack: https://capitalwars.substack.com
   - CrossBorder Capital: https://www.crossbordercapital.com

2. **Academic Papers**
   - BIS Papers on Global Liquidity
   - IMF Working Papers on Cross-Border Flows
   - Federal Reserve research on shadow banking

3. **Data Provider Documentation**
   - FRED API docs: https://fred.stlouisfed.org/docs/api/
   - ECB API docs: https://sdw-wsrest.ecb.europa.eu/help/
   - BOJ API docs: https://www.stat-search.boj.or.jp/

4. **Technical References**
   - TimescaleDB best practices
   - FastAPI async patterns
   - Recharts advanced charting

## Notes

- This plan is ambitious and will significantly expand the application's capabilities
- We should implement in phases to maintain working application throughout
- Some data sources may require manual updates or web scraping
- Consider adding data quality indicators for each metric
- Document data update frequencies and any gaps in coverage
- Build robust error handling for API failures
- Consider caching strategies for expensive calculations
- Plan for data storage costs as database grows
