# Phase 2: Private Sector Liquidity - FRED Series IDs

## Overview
Private sector liquidity complements central bank liquidity and represents the "real economy" money creation through banking systems, shadow banking, and credit markets.

## 1. Shadow Banking Metrics

### Money Market Funds (MMF)
- **Total Assets**: `MMMFAQ027S` - Money Market Mutual Fund Assets (Quarterly, Billions USD)
- **Institutional MMF**: `WIMMMFAQ027S` - Institutional Money Market Funds (Quarterly, Billions USD)
- **Retail MMF**: `WRMMMFAQ027S` - Retail Money Market Funds (Quarterly, Billions USD)

### Repurchase Agreements (Repos)
- **Primary Dealer Repos**: `PDREPO` - Primary Dealer Repo Positions (Weekly, Billions USD)
- **Reverse Repos**: `PDREVREPO` - Primary Dealer Reverse Repo Positions (Weekly, Billions USD)

### Commercial Paper
- **Total Commercial Paper**: `COMPOUT` - Commercial Paper Outstanding (Weekly, Billions USD)
- **Financial CP**: `COMPAPFF` - Financial Commercial Paper Outstanding (Weekly, Billions USD)
- **Nonfinancial CP**: `COMPAAPNF` - Nonfinancial Commercial Paper Outstanding (Weekly, Billions USD)
- **Asset-Backed CP**: `ABCOMP` - Asset-Backed Commercial Paper Outstanding (Weekly, Billions USD)

### Securities Lending
- **Treasury Securities Lending**: Not directly available in FRED (requires DTCC/TriParty data)
- **Corporate Bond Lending**: Not directly available in FRED

## 2. Traditional Banking Metrics

### Monetary Aggregates
- **M2 Money Stock**: `M2SL` - M2 Money Stock (Monthly, Billions USD)
- **M2 Velocity**: `M2V` - Velocity of M2 Money Stock (Quarterly, Ratio)
- **M3 (Discontinued)**: Use M2 + Institutional MMF as proxy

### Bank Credit
- **Total Bank Credit**: `TOTBKCR` - Bank Credit, All Commercial Banks (Weekly, Billions USD)
- **Consumer Credit**: `TOTALSL` - Total Consumer Credit Outstanding (Monthly, Billions USD)
- **Commercial & Industrial Loans**: `BUSLOANS` - Commercial and Industrial Loans (Weekly, Billions USD)
- **Real Estate Loans**: `REALLN` - Real Estate Loans, All Commercial Banks (Weekly, Billions USD)

### Deposits
- **Total Deposits**: `DPSACBW027SBOG` - Deposits, All Commercial Banks (Weekly, Billions USD)
- **Small Time Deposits**: `STDSL` - Small Time Deposits (Monthly, Billions USD)
- **Savings Deposits**: `SAVINGSL` - Savings Deposits (Monthly, Billions USD)

### Reserve Balances
- **Reserve Balances**: `WRESBAL` - Reserve Balances with Federal Reserve Banks (Weekly, Billions USD)
- **Required Reserves**: `REQRESNS` - Required Reserves of Depository Institutions (Monthly, Billions USD)

## 3. Corporate Debt & Securities

### Corporate Debt Issuance
- **Nonfinancial Corporate Debt**: `BCNSDODNS` - Nonfinancial Corporate Business; Debt Securities (Quarterly, Billions USD)
- **Financial Corporate Debt**: `FBCELLQ027S` - Financial Business; Corporate Equities; Liability (Quarterly, Billions USD)

### Credit Market Instruments
- **Total Credit Market Debt**: `TCMDO` - Total Credit Market Debt Outstanding (Quarterly, Billions USD)
- **Household Debt**: `CMDEBT` - Household Credit Market Debt Outstanding (Quarterly, Billions USD)

## 4. International Money Markets (US-focused)

### Eurodollar Deposits
- **Eurodollar Deposits**: `EURODOL` - Eurodollar Deposits (Monthly, Billions USD) - Note: Series discontinued 2020

### Foreign Exchange Swaps
- Not directly available in FRED (requires BIS data)

## Data Update Frequencies

| Metric | Frequency | Typical Lag |
|--------|-----------|-------------|
| Money Market Funds | Quarterly | 2 months |
| Repos/Reverse Repos | Weekly | 1 week |
| Commercial Paper | Weekly | 1 week |
| M2 Money Stock | Monthly | 2 weeks |
| Bank Credit | Weekly | 1 week |
| Deposits | Weekly/Monthly | 1-2 weeks |
| Corporate Debt | Quarterly | 2-3 months |

## Implementation Priority

### High Priority (Week 1-2)
1. **M2 Money Stock** - Core traditional banking metric
2. **Total Bank Credit** - Credit creation indicator
3. **Money Market Funds** - Shadow banking core
4. **Commercial Paper** - Short-term funding market

### Medium Priority (Week 3)
5. **Repos/Reverse Repos** - Collateral velocity
6. **Consumer Credit** - Household liquidity
7. **C&I Loans** - Business credit
8. **Deposits** - Funding base

### Lower Priority (Week 4-5)
9. **Corporate Debt** - Long-term funding
10. **Reserve Balances** - Banking system reserves
11. **M2 Velocity** - Money circulation

## Data Source Notes

- **FRED Coverage**: Good for US traditional banking, shadow banking basics
- **Missing Data**: Securities lending, FX swaps, detailed MMF composition
- **Alternative Sources**:
  - SEC Form N-MFP for detailed MMF holdings
  - DTCC for securities lending
  - BIS for international swaps
  - SIFMA for corporate issuance details

## Calculation: Total Private Sector Liquidity (TPSL)

```
TPSL = M2 + MMF + Commercial_Paper + Repos_Net + Bank_Credit_Growth

Where:
- M2 = Broad money supply
- MMF = Total Money Market Fund assets
- Commercial_Paper = Total CP outstanding
- Repos_Net = Primary Dealer Repos - Reverse Repos
- Bank_Credit_Growth = Change in total bank credit (6-month moving sum)
```

## Integration with Global Liquidity Index

```
Enhanced GLI = Central_Bank_Liquidity + Private_Sector_Liquidity

Where:
- Central_Bank_Liquidity = FED + ECB + BOJ + BOE + SNB + BOC + RBA (already implemented)
- Private_Sector_Liquidity = TPSL (to be implemented)
```

---

**Next Steps**:
1. Create database models for private sector data
2. Extend FRED service to fetch these series
3. Build aggregation logic for TPSL
4. Update dashboard to show private vs public liquidity breakdown
