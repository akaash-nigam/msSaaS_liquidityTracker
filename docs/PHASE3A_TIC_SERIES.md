# Phase 3A: US Treasury TIC Data - FRED Series

## Overview
US Treasury International Capital (TIC) data tracks foreign holdings of US securities. This is the **easiest and most impactful** starting point for capital flows tracking.

## 🎯 Priority Series (Free via FRED)

### 1. **Rest of World Holdings of US Assets**

#### Total US Financial Assets
- **BOGZ1FL263061005Q** - Rest of World; Total Financial Assets
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current Value**: ~$50 trillion
  - **Description**: Total foreign holdings of all US financial assets

#### US Treasury Securities
- **BOGZ1FL263064105Q** - Rest of World; Treasury Securities
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current Value**: ~$7-8 trillion
  - **Description**: Foreign holdings of US Treasury bonds and bills
  - **Importance**: ⭐⭐⭐ Critical for "dollar recycling" indicator

#### US Corporate Equities
- **BOGZ1FL263063005Q** - Rest of World; Corporate Equities
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current Value**: ~$12-15 trillion
  - **Description**: Foreign holdings of US stocks
  - **Importance**: ⭐⭐⭐ Risk-on/risk-off indicator

#### US Corporate and Foreign Bonds
- **BOGZ1FL263063043Q** - Rest of World; Corporate and Foreign Bonds
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current Value**: ~$4-5 trillion
  - **Description**: Foreign holdings of US corporate bonds

#### US Agency Securities
- **BOGZ1FL263061703Q** - Rest of World; Agency and GSE-Backed Securities
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current Value**: ~$2 trillion
  - **Description**: Foreign holdings of Fannie Mae, Freddie Mac securities

---

### 2. **US Holdings of Foreign Assets (Reverse Flow)**

#### Total Foreign Assets
- **BOGZ1FL153061005Q** - Households and Nonprofit Orgs; Total Foreign Assets
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Description**: US holdings of foreign securities

---

### 3. **Country-Specific TIC Data (Top Foreign Holders)**

#### China Holdings of US Treasuries
- **BOGZ1FL263064145Q** - Foreign Official Institutions; US Government Securities
  - **Frequency**: Quarterly
  - **Unit**: Billions of Dollars
  - **Current**: China holds ~$800-900 billion
  - **Importance**: ⭐⭐⭐ Geopolitical indicator

#### Japan Holdings
- Similar data available through TIC monthly reports
- Japan is typically the #1 or #2 holder (~$1.1 trillion)

---

### 4. **Balance of Payments Series (US)**

#### US Current Account
- **BOPGSTB** - Trade Balance: Goods and Services, Balance of Payments Basis
  - **Frequency**: Quarterly
  - **Unit**: Millions of Dollars
  - **Current**: Deficit of ~$200-250 billion per quarter

- **NETFI** - Net Financial Inflows
  - **Frequency**: Quarterly
  - **Unit**: Millions of Dollars
  - **Description**: Net foreign purchases of US assets

#### US Financial Account
- **BOPGFAA** - Financial Account, Balance of Payments Basis
  - **Frequency**: Quarterly
  - **Unit**: Millions of Dollars
  - **Description**: Net financial flows

#### Direct Investment
- **BOPGFDI** - Direct Investment, Net
  - **Frequency**: Quarterly
  - **Unit**: Millions of Dollars
  - **Description**: FDI inflows minus outflows

#### Portfolio Investment
- **BOPGPNI** - Portfolio Investment, Net
  - **Frequency**: Quarterly
  - **Unit**: Millions of Dollars
  - **Description**: Portfolio flows (stocks, bonds)

---

## 📊 Derived Metrics to Calculate

### 1. **Dollar Recycling Indicator**
```
Dollar Recycling = US Current Account Deficit
                 - Foreign Official Purchases of US Treasuries
```
- **Meaning**: How much of the US trade deficit is being recycled back into US assets
- **Signal**:
  - High recycling = Strong dollar demand, stable system
  - Low recycling = Dollar weakness risk

### 2. **Foreign Demand Index**
```
Foreign Demand = (Foreign Holdings of US Assets YoY Change) / US GDP
```
- **Meaning**: Foreign appetite for US assets relative to economy size
- **Signal**:
  - Rising = Capital inflows, risk-on
  - Falling = Capital outflows, risk-off

### 3. **Risk Appetite Score**
```
Risk Score = (Foreign Equity Holdings / Foreign Treasury Holdings) × 100
```
- **Meaning**: Foreign preference for risky vs safe assets
- **Signal**:
  - >100 = Risk-on (prefer stocks)
  - <100 = Risk-off (prefer bonds)

### 4. **Treasury Demand Stress**
```
Stress = (Quarterly Change in Foreign Treasury Holdings) / (US Treasury Issuance)
```
- **Meaning**: Foreign absorption of new Treasury supply
- **Signal**:
  - <50% = Low foreign demand (potential yield spike)
  - >100% = Strong foreign demand (yield suppression)

---

## 🔧 Implementation Priority

### Week 1: Foundation
1. ✅ Create database models (`capital_flows.py`)
2. ⬜ Fetch TIC series from FRED:
   - BOGZ1FL263061005Q (Total foreign holdings)
   - BOGZ1FL263064105Q (Treasury holdings)
   - BOGZ1FL263063005Q (Equity holdings)
3. ⬜ Store in `us_treasury_tic` table
4. ⬜ Create basic API endpoint to view data

### Week 2: Analysis
1. ⬜ Fetch Balance of Payments series:
   - BOPGSTB (Trade balance)
   - NETFI (Net financial inflows)
   - BOPGFAA (Financial account)
2. ⬜ Calculate derived metrics:
   - Dollar Recycling Indicator
   - Foreign Demand Index
   - Risk Appetite Score
3. ⬜ Store in `capital_flow_index` table

### Week 3: Visualization
1. ⬜ Create frontend dashboard showing:
   - Foreign holdings breakdown (pie chart)
   - Trend over time (line chart)
   - Dollar recycling gauge
   - Risk appetite indicator
2. ⬜ Add comparison view (US vs China vs Japan holdings)

---

## 📈 Expected Data

### Sample Query Results
```sql
SELECT
    report_date,
    country_name,
    total_treasuries,
    equities,
    total_holdings
FROM us_treasury_tic
WHERE country_code = 'CHN'
ORDER BY report_date DESC
LIMIT 4;
```

**Expected Output**:
```
report_date | country_name | total_treasuries | equities | total_holdings
------------|--------------|------------------|----------|----------------
2024-09-30  | China        | 775,200         | 125,300  | 985,400
2024-06-30  | China        | 768,300         | 118,900  | 972,100
2024-03-31  | China        | 781,900         | 110,200  | 988,500
2023-12-31  | China        | 816,300         | 105,700  | 1,015,800
```

**Analysis**:
- China reduced Treasury holdings by $41B (-5%) in 2024
- Increased equity holdings by $20B (+19%)
- **Signal**: Shift from safe to risky assets = moderate risk-on

---

## 🎯 Success Metrics

After Phase 3A implementation, you should have:

1. ✅ **5-10 years of historical data** for key TIC series
2. ✅ **Quarterly updates** tracking $50T+ in cross-border flows
3. ✅ **4 calculated indicators** (Dollar Recycling, Foreign Demand, Risk Appetite, Treasury Stress)
4. ✅ **Dashboard visualization** showing trends
5. ✅ **Country breakdown** for top 10 foreign holders

**Total Data Points**: ~200-400 records (5 series × 40-80 quarters)

---

## 💡 Next Steps After Phase 3A

Once TIC data is working:
1. **Phase 3B**: Add BIS cross-border banking data
2. **Phase 3C**: Add OECD FDI statistics
3. **Phase 3D**: Build Sankey diagram for flow visualization
4. **Phase 3E**: Add real-time indicators (currency flows, fund flows)

---

## 📚 Data Sources

- **FRED API**: https://fred.stlouisfed.org/
- **US Treasury TIC Reports**: https://home.treasury.gov/data/treasury-international-capital-tic-system
- **IMF Balance of Payments**: https://data.imf.org/
- **OECD Data**: https://data.oecd.org/

All Phase 3A data is **100% free** and does not require paid subscriptions.
