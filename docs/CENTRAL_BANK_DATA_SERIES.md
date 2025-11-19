# Central Bank Data Series Reference

## Overview
This document contains the specific data series IDs for tracking global central bank liquidity across major economies.

## ✅ Federal Reserve (USA) - Already Implemented

**Source**: FRED API (Federal Reserve Economic Data)
**API Key**: Required (already configured)
**Update Frequency**: Weekly

| Indicator | FRED Series ID | Description | Units |
|-----------|----------------|-------------|-------|
| Balance Sheet | WALCL | Total Assets | Billions of USD |
| Treasury General Account | WDTGAL | TGA at Federal Reserve | Millions of USD |
| Reverse Repo | RRPONTSYD | Overnight Reverse Repo | Billions of USD |

**Current Implementation**: ✅ Fully integrated

---

## 🇪🇺 European Central Bank (ECB)

**Source**: ECB Data Portal API
**API Endpoint**: https://data-api.ecb.europa.eu
**API Key**: Not required (public API)
**Update Frequency**: Weekly
**Documentation**: https://data.ecb.europa.eu/help/api/overview

### Key Series (via ECB Data Portal)

| Indicator | Series Key | Description | Units |
|-----------|------------|-------------|-------|
| Total Assets | BSI.M.U2.Y.V.A.A.T.A.FA.A.T.EUR | ECB Balance Sheet Total Assets | Millions of EUR |
| Main Refinancing Operations | ILM.M.U2.C.A010000.U2.EUR | Main refinancing operations | Millions of EUR |
| Deposit Facility | FM.M.U2.EUR.4F.KR.DFR.LEV | Deposit facility rate | Percent |
| Securities Holdings | BSI.M.U2.N.A.L41.A.1.Z5.0000.Z01.E | Securities held | Millions of EUR |

### Alternative: Use FRED for ECB Data

FRED also tracks ECB data, which is easier to integrate:

| Indicator | FRED Series ID | Description |
|-----------|----------------|-------------|
| ECB Total Assets | ECBASSETSW | ECB Assets (Weekly) |
| ECB Balance Sheet | ECBASSETS | ECB Total Assets |

**Recommendation**: Use FRED series for ECB data to keep consistent API

---

## 🇯🇵 Bank of Japan (BOJ)

**Source**: FRED API (easier) or BOJ Time-Series Database
**API Key**: Not required for FRED (already have key)
**Update Frequency**: Monthly
**BOJ Official Site**: https://www.stat-search.boj.or.jp/index_en.html

### FRED Series (Recommended)

| Indicator | FRED Series ID | Description | Units |
|-----------|----------------|-------------|-------|
| Total Assets | JPNASSETS | Bank of Japan Total Assets | Billions of Yen |

### BOJ Direct Series (Alternative)

If we need more granular data:
- **JGB Holdings**: Available through BOJ API
- **ETF Holdings**: Available through BOJ API
- **REIT Holdings**: Available through BOJ API

**Recommendation**: Start with FRED JPNASSETS, add BOJ direct API later if needed

---

## 🇬🇧 Bank of England (BOE)

**Source**: FRED API or BOE Database
**API Key**: Not required
**Update Frequency**: Weekly
**BOE Database**: https://www.bankofengland.co.uk/boeapps/database/

### FRED Series (Recommended)

| Indicator | FRED Series ID | Description | Units |
|-----------|----------------|-------------|-------|
| Total Assets | BOEBSTAUKA | Bank of England Balance Sheet - Total Assets | Millions of GBP |

### BOE Direct Series (Alternative)

Available through BOE Database:
- Weekly Report balance sheet data
- Asset Purchase Facility holdings
- Reserve balances

**Recommendation**: Use FRED BOEBSTAUKA for consistency

---

## 🇨🇳 People's Bank of China (PBoC)

**Source**: Multiple sources (no easy API)
**API Key**: Not required but data access is challenging
**Update Frequency**: Monthly
**Official Site**: http://www.pbc.gov.cn/en/

### Data Sources

**Option 1: FRED (Limited)**
| Indicator | FRED Series ID | Description |
|-----------|----------------|-------------|
| Foreign Exchange Reserves | TRESEGCNM052N | China Foreign Exchange Reserves |

**Option 2: CEIC Data (Paid)**
- Comprehensive China economic data
- Subscription required ($$$)

**Option 3: Trading Economics**
- Free tier available
- Central Bank Balance Sheet data
- May require web scraping

**Option 4: Manual Updates**
- PBoC publishes monthly balance sheet
- Could manually update from official reports
- JSON file with historical data

**Recommendation**: Start with FRED FX reserves, add manual updates for balance sheet data

---

## 🇨🇭 Swiss National Bank (SNB)

**Source**: SNB or FRED
**API Key**: Not required
**Update Frequency**: Weekly

### FRED Series

| Indicator | FRED Series ID | Description |
|-----------|----------------|-------------|
| Total Assets | SNBASSETSW | SNB Assets (Weekly) |

---

## 🇨🇦 Bank of Canada (BOC)

**Source**: FRED or BOC Statistics
**API Key**: Not required
**Update Frequency**: Weekly

### FRED Series

| Indicator | FRED Series ID | Description |
|-----------|----------------|-------------|
| Total Assets | BOCBSTAA | Bank of Canada Balance Sheet - Total Assets |

---

## 🇦🇺 Reserve Bank of Australia (RBA)

**Source**: FRED or RBA Statistics
**API Key**: Not required
**Update Frequency**: Weekly

### FRED Series

| Indicator | FRED Series ID | Description |
|-----------|----------------|-------------|
| Total Assets | RBATCAUM | Reserve Bank of Australia Total Assets |

---

## Implementation Priority

### Phase 1A: Major Central Banks (Week 1) - Use FRED

All available through FRED API (which we already have configured):

```python
CENTRAL_BANK_SERIES = {
    # Already implemented
    "FED": {
        "balance_sheet": "WALCL",
        "tga": "WDTGAL",
        "rrp": "RRPONTSYD",
        "currency": "USD",
        "region": "Americas"
    },

    # Add these next
    "ECB": {
        "balance_sheet": "ECBASSETSW",
        "currency": "EUR",
        "region": "Europe"
    },

    "BOJ": {
        "balance_sheet": "JPNASSETS",
        "currency": "JPY",
        "region": "Asia"
    },

    "BOE": {
        "balance_sheet": "BOEBSTAUKA",
        "currency": "GBP",
        "region": "Europe"
    },

    "SNB": {
        "balance_sheet": "SNBASSETSW",
        "currency": "CHF",
        "region": "Europe"
    },

    "BOC": {
        "balance_sheet": "BOCBSTAA",
        "currency": "CAD",
        "region": "Americas"
    },

    "RBA": {
        "balance_sheet": "RBATCAUM",
        "currency": "AUD",
        "region": "Asia"
    }
}
```

### Phase 1B: China (Special Handling)

PBoC requires special handling:
1. Start with FRED foreign exchange reserves (TRESEGCNM052N)
2. Add manual balance sheet data from official reports
3. Consider paid data providers for automation later

---

## Currency Conversion

All central bank data will need to be converted to USD for aggregation.

**Options**:

1. **FRED Exchange Rates** (Recommended)
   - EUR/USD: DEXUSEU
   - JPY/USD: DEXJPUS
   - GBP/USD: DEXUSUK
   - CHF/USD: DEXSZUS
   - CAD/USD: DEXCAUS
   - AUD/USD: DEXUSAL
   - CNY/USD: DEXCHUS

2. **ECB Exchange Rate API**
   - Free, daily updates
   - Good backup source

3. **External Forex API**
   - exchangerate-api.com (free tier: 1,500 requests/month)
   - Good for real-time rates

**Recommendation**: Use FRED for historical rates, cache daily rates in database

---

## Global Liquidity Index Calculation

### Current (US-only):
```
GLI_US = FED - TGA - RRP
```

### Target (Global):
```
GLI_Global = (FED - TGA - RRP) +       # United States
             ECB +                      # Eurozone
             BOJ +                      # Japan
             BOE +                      # United Kingdom
             PBOC +                     # China
             SNB +                      # Switzerland
             BOC +                      # Canada
             RBA +                      # Australia
             ... (other central banks)
```

All converted to USD.

### Weighting
Based on Michael Howell's research, approximate weights:
- United States: ~30%
- Eurozone: ~25%
- China: ~20%
- Japan: ~15%
- Others: ~10%

---

## Data Update Schedule

| Central Bank | Update Frequency | Update Day | Lag |
|--------------|------------------|------------|-----|
| Federal Reserve | Weekly | Thursday | 1 day |
| ECB | Weekly | Tuesday | 1 day |
| BOJ | Monthly | Beginning of month | ~1 week |
| BOE | Weekly | Thursday | 1 day |
| PBoC | Monthly | Mid-month | ~2 weeks |
| SNB | Weekly | Monday | 1 day |
| BOC | Weekly | Thursday | 1 day |
| RBA | Weekly | Friday | 1 day |

**Recommendation**: Run daily data ingestion job, fetch all available updates

---

## Next Steps

1. **Extend FRED Service** (fred_service.py)
   - Add all new series IDs
   - Add currency conversion
   - Fetch exchange rates

2. **Update Data Models** (models/)
   - Add currency field
   - Add region field
   - Support multiple central banks

3. **Update GLI Calculation** (gli_service.py)
   - Aggregate all central banks
   - Apply currency conversion
   - Calculate weighted global index

4. **Add Exchange Rate Service** (exchange_rate_service.py)
   - Fetch USD conversion rates
   - Cache rates in database
   - Provide conversion utility

5. **Update UI Components**
   - Show breakdown by central bank
   - Show breakdown by region
   - Update total from $5.77T to actual global total

---

## Expected Global Liquidity Total

Based on Michael Howell's research:
- **Shadow Monetary Base**: ~$100 trillion (central banks + collateral)
- **Global Liquidity Pool**: ~$176 trillion (including multiplier effects)

Our Phase 1 implementation will capture the **central bank component** (~$22-30 trillion), which is the foundation of the Global Liquidity Index.

---

## Resources

- FRED API Docs: https://fred.stlouisfed.org/docs/api/
- ECB Data Portal: https://data.ecb.europa.eu/
- BOJ Statistics: https://www.stat-search.boj.or.jp/index_en.html
- BOE Database: https://www.bankofengland.co.uk/boeapps/database/
- Michael Howell's Capital Wars: https://capitalwars.substack.com
