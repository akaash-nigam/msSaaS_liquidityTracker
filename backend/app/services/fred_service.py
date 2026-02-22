import httpx
import random
import asyncio
import time
import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class FREDService:
    """Service for fetching data from FRED (Federal Reserve Economic Data) API."""

    BASE_URL = "https://api.stlouisfed.org/fred"

    # Rate limiting: FRED allows 120 req/min
    _last_request_time: float = 0
    _min_interval: float = 0.6  # ~100 req/min, staying under limit

    # Central bank balance sheet series
    CENTRAL_BANK_SERIES = {
        "FED": {
            "series_id": "WALCL",
            "name": "Federal Reserve Total Assets",
            "currency": "USD",
            "unit_scale": 1_000_000,  # FRED reports in millions
        },
        "ECB": {
            "series_id": "ECBASSETSW",
            "name": "ECB Total Assets",
            "currency": "EUR",
            "unit_scale": 1_000_000,
        },
        "BOJ": {
            "series_id": "JPNASSETS",
            "name": "Bank of Japan Total Assets",
            "currency": "JPY",
            "unit_scale": 100_000_000,  # FRED reports in 100 million JPY
        },
        "BOE": {
            "series_id": "UKASSETS",
            "name": "Bank of England Total Assets",
            "currency": "GBP",
            "unit_scale": 1_000_000,
            "fallback_to_mock": True,  # Series may be discontinued
        },
        "SNB": {
            "series_id": "SNBASSETS",
            "name": "Swiss National Bank Total Assets",
            "currency": "CHF",
            "unit_scale": 1_000_000,
            "fallback_to_mock": True,  # Not available on FRED
        },
        "BOC": {
            "series_id": "BCASSETS",
            "name": "Bank of Canada Total Assets",
            "currency": "CAD",
            "unit_scale": 1_000_000,
            "fallback_to_mock": True,  # Not available on FRED
        },
        "RBA": {
            "series_id": "RBASSETS",
            "name": "Reserve Bank of Australia Total Assets",
            "currency": "AUD",
            "unit_scale": 1_000_000,
            "fallback_to_mock": True,  # Not available on FRED
        },
        "PBOC": {
            "series_id": "CHNASSETS",
            "name": "People's Bank of China Total Assets",
            "currency": "CNY",
            "unit_scale": 100_000_000,  # 100 million CNY
            "fallback_to_mock": True,  # Not available on FRED
        },
    }

    # Exchange rate series (to USD)
    EXCHANGE_RATE_SERIES = {
        "EUR": "DEXUSEU",
        "JPY": "DEXJPUS",
        "GBP": "DEXUSUK",
        "CHF": "DEXSZUS",
        "CAD": "DEXCAUS",
        "AUD": "DEXUSAL",
        "CNY": "DEXCHUS",
    }

    # Fed Balance Sheet Decomposition series
    FED_BALANCE_SHEET_SERIES = {
        "treasuries": {
            "series_id": "TREAST",
            "name": "U.S. Treasury Securities Held",
            "unit": "millions_usd",
        },
        "mbs": {
            "series_id": "WSHOMCB",
            "name": "Mortgage-Backed Securities Held",
            "unit": "millions_usd",
        },
        "total": {
            "series_id": "WALCL",
            "name": "Total Assets",
            "unit": "millions_usd",
        },
    }

    # Private sector liquidity series (Phase 2)
    PRIVATE_SECTOR_SERIES = {
        "shadow_banking": {
            "m2": {"series_id": "M2SL", "name": "M2 Money Stock", "frequency": "monthly", "unit": "billions_usd"},
            "mmf_total": {"series_id": "MMMFAQ027S", "name": "Money Market Funds Total Assets", "frequency": "quarterly", "unit": "billions_usd"},
            "commercial_paper": {"series_id": "COMPOUT", "name": "Commercial Paper Outstanding", "frequency": "weekly", "unit": "billions_usd"},
            "repos": {"series_id": "PDREPO", "name": "Primary Dealer Repo", "frequency": "weekly", "unit": "billions_usd"},
            "reverse_repos": {"series_id": "PDREVREPO", "name": "Primary Dealer Reverse Repo", "frequency": "weekly", "unit": "billions_usd"},
            "abs_outstanding": {"series_id": "ABSOUT", "name": "Asset-Backed Securities Outstanding", "frequency": "quarterly", "unit": "billions_usd"},
            "gse_mortgage": {"series_id": "GSEMORT", "name": "GSE Mortgage Pools", "frequency": "quarterly", "unit": "billions_usd"},
            "fed_funds_volume": {"series_id": "EFFRVOL", "name": "Fed Funds Volume", "frequency": "daily", "unit": "billions_usd"},
            "tri_party_repo": {"series_id": "TPRVOL", "name": "Tri-Party Repo Volume", "frequency": "daily", "unit": "billions_usd"},
        },
        "traditional_banking": {
            "bank_credit": {"series_id": "TOTBKCR", "name": "Total Bank Credit", "frequency": "weekly", "unit": "billions_usd"},
            "ci_loans": {"series_id": "BUSLOANS", "name": "C&I Loans", "frequency": "weekly", "unit": "billions_usd"},
            "consumer_credit": {"series_id": "TOTALSL", "name": "Consumer Credit Outstanding", "frequency": "monthly", "unit": "billions_usd"},
            "real_estate_loans": {"series_id": "RELOAN", "name": "Real Estate Loans", "frequency": "weekly", "unit": "billions_usd"},
            "bank_deposits": {"series_id": "DPSACBW027SBOG", "name": "Deposits at Commercial Banks", "frequency": "weekly", "unit": "billions_usd"},
            "excess_reserves": {"series_id": "EXCSRESNS", "name": "Excess Reserves", "frequency": "monthly", "unit": "billions_usd"},
            "required_reserves": {"series_id": "REQRESNS", "name": "Required Reserves", "frequency": "monthly", "unit": "billions_usd"},
            "money_multiplier": {"series_id": "MULT", "name": "M1 Money Multiplier", "frequency": "weekly", "unit": "ratio"},
            "velocity_m2": {"series_id": "M2V", "name": "Velocity of M2", "frequency": "quarterly", "unit": "ratio"},
            "tga_balance": {"series_id": "WTREGEN", "name": "Treasury General Account", "frequency": "weekly", "unit": "billions_usd"},
        },
        "corporate_debt": {
            "corporate_bonds": {"series_id": "CBTOT", "name": "Corporate Bonds Outstanding", "frequency": "quarterly", "unit": "billions_usd"},
            "high_yield_spread": {"series_id": "BAMLH0A0HYM2", "name": "High Yield Spread", "frequency": "daily", "unit": "percent"},
            "ig_spread": {"series_id": "BAMLC0A4CBBB", "name": "Investment Grade Spread", "frequency": "daily", "unit": "percent"},
        },
    }

    # Capital flows series (Phase 3A)
    CAPITAL_FLOWS_SERIES = {
        "rest_of_world": {
            "total_financial_assets": {"series_id": "BOGZ1FL263090005Q", "name": "ROW Total Financial Assets"},
            "treasury_securities": {"series_id": "BOGZ1FL263061105Q", "name": "ROW Treasury Securities"},
            "corporate_equities": {"series_id": "BOGZ1FL263064105Q", "name": "ROW Corporate Equities"},
            "corporate_bonds": {"series_id": "BOGZ1FL263063005Q", "name": "ROW Corporate Bonds"},
            "agency_securities": {"series_id": "BOGZ1FL263061705Q", "name": "ROW Agency Securities"},
        },
        "balance_of_payments": {
            "trade_balance": {"series_id": "BOPGSTB", "name": "Trade Balance"},
            "current_account": {"series_id": "BOPBCA", "name": "Current Account Balance"},
            "financial_account": {"series_id": "BOPFINA", "name": "Financial Account Balance"},
            "net_financial_inflows": {"series_id": "BOPFINB", "name": "Net Financial Inflows"},
            "fdi_net": {"series_id": "BOPFDI", "name": "Net FDI"},
            "portfolio_investment_net": {"series_id": "BOPPORT", "name": "Net Portfolio Investment"},
        },
    }

    # Market indicator series (Phase 4)
    MARKET_INDICATOR_SERIES = {
        "VIXCLS": {"name": "VIX", "category": "volatility", "unit": "index"},
        "T10Y2Y": {"name": "10Y-2Y Spread", "category": "yield_curve", "unit": "percent"},
        "DGS10": {"name": "10Y Treasury", "category": "yield_curve", "unit": "percent"},
        "DGS2": {"name": "2Y Treasury", "category": "yield_curve", "unit": "percent"},
        "BAMLH0A0HYM2": {"name": "HY Spread", "category": "credit_spread", "unit": "percent"},
        "BAMLC0A4CBBB": {"name": "IG Spread", "category": "credit_spread", "unit": "percent"},
        "T10YIE": {"name": "Breakeven Inflation", "category": "real_rates", "unit": "percent"},
        "RRPONTSYD": {"name": "ON RRP", "category": "fed_facility", "unit": "millions_usd"},
        "TREAST": {"name": "Fed Treasury Holdings", "category": "fed_balance_sheet", "unit": "millions_usd"},
        "WSHOMCB": {"name": "Fed MBS Holdings", "category": "fed_balance_sheet", "unit": "millions_usd"},
    }

    # Asset price series (Phase 4)
    ASSET_PRICE_SERIES = {
        "SP500": {"series_id": "SP500", "name": "S&P 500", "asset_class": "equity", "ticker": "SPX"},
        "GOLDAMGBD228NLBM": {"series_id": "GOLDAMGBD228NLBM", "name": "Gold", "asset_class": "commodity", "ticker": "GOLD"},
        "CBBTCUSD": {"series_id": "CBBTCUSD", "name": "Bitcoin", "asset_class": "crypto", "ticker": "BTC"},
    }

    # Buffett Indicator (Market Cap to GDP) series - World Bank via FRED (Phase 5)
    BUFFETT_INDICATOR_SERIES = {
        "USA": {"series_id": "DDDM01USA156NWDB", "name": "United States"},
        "JPA": {"series_id": "DDDM01JPA156NWDB", "name": "Japan"},
        "CNA": {"series_id": "DDDM01CNA156NWDB", "name": "China"},
        "GBA": {"series_id": "DDDM01GBA156NWDB", "name": "United Kingdom"},
        "DEA": {"series_id": "DDDM01DEA156NWDB", "name": "Germany"},
        "FRA": {"series_id": "DDDM01FRA156NWDB", "name": "France"},
        "CAA": {"series_id": "DDDM01CAA156NWDB", "name": "Canada"},
        "INA": {"series_id": "DDDM01INA156NWDB", "name": "India"},
        "KRA": {"series_id": "DDDM01KRA156NWDB", "name": "South Korea"},
        "BRA": {"series_id": "DDDM01BRA156NWDB", "name": "Brazil"},
    }

    # GDP series for reference
    GDP_SERIES = {
        "USA": {"series_id": "GDP", "name": "US Nominal GDP"},
        "WORLD": {"series_id": "NYGDPMKTPCDWLD", "name": "World GDP"},
        "JPA": {"series_id": "JPNNGDP", "name": "Japan GDP"},
    }

    # Series IDs that should fall back to mock if FRED returns an error
    _FALLBACK_SERIES: set = set()

    def __init__(self):
        self.api_key = settings.FRED_API_KEY
        self.use_mock = settings.USE_MOCK_DATA or self.api_key == "demo"
        # Build fallback set from central bank configs
        for config in self.CENTRAL_BANK_SERIES.values():
            if config.get("fallback_to_mock"):
                self._FALLBACK_SERIES.add(config["series_id"])

    def _should_fallback(self, series_id: str) -> bool:
        """Check if a series should fall back to mock data on error."""
        return series_id in self._FALLBACK_SERIES

    async def fetch_series(
        self,
        series_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Dict:
        """Fetch a FRED series. Returns mock data if USE_MOCK_DATA is True."""
        if self.use_mock:
            return self._generate_mock_series(series_id, start_date, end_date)

        # Rate limiting
        now = time.time()
        elapsed = now - FREDService._last_request_time
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        FREDService._last_request_time = time.time()

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }
        if start_date:
            params["observation_start"] = start_date.isoformat()
        if end_date:
            params["observation_end"] = end_date.isoformat()

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"{self.BASE_URL}/series/observations", params=params)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status in (400, 404) and self._should_fallback(series_id):
                logger.warning(f"FRED series {series_id} returned {status} — using mock data")
                return self._generate_mock_series(series_id, start_date, end_date)
            logger.error(f"FRED API error for {series_id}: {status}")
            raise
        except httpx.TimeoutException:
            if self._should_fallback(series_id):
                logger.warning(f"FRED series {series_id} timed out — using mock data")
                return self._generate_mock_series(series_id, start_date, end_date)
            raise

        observations = []
        for obs in data.get("observations", []):
            if obs["value"] != ".":
                observations.append({
                    "date": date.fromisoformat(obs["date"]),
                    "value": float(obs["value"]),
                })

        if not observations and self._should_fallback(series_id):
            logger.warning(f"FRED series {series_id} returned no data — using mock data")
            return self._generate_mock_series(series_id, start_date, end_date)

        logger.info(f"FRED series {series_id}: fetched {len(observations)} observations")
        return {"series_id": series_id, "observations": observations}

    async def fetch_central_bank_data(
        self, bank_code: str, start_date: date, end_date: date
    ) -> Dict:
        """Fetch central bank balance sheet data."""
        config = self.CENTRAL_BANK_SERIES.get(bank_code)
        if not config:
            raise ValueError(f"Unknown central bank: {bank_code}")
        result = await self.fetch_series(config["series_id"], start_date, end_date)
        result["bank_code"] = bank_code
        result["currency"] = config["currency"]
        result["unit_scale"] = config["unit_scale"]
        return result

    async def fetch_exchange_rates(
        self, currency: str, start_date: date, end_date: date
    ) -> Dict:
        """Fetch exchange rate series."""
        series_id = self.EXCHANGE_RATE_SERIES.get(currency)
        if not series_id:
            raise ValueError(f"No exchange rate series for: {currency}")
        return await self.fetch_series(series_id, start_date, end_date)

    async def fetch_capital_flows_metric(
        self, category: str, subcategory: str, start_date: date, end_date: date
    ) -> Dict:
        """Fetch a capital flows metric."""
        cat_data = self.CAPITAL_FLOWS_SERIES.get(category, {})
        config = cat_data.get(subcategory)
        if not config:
            raise ValueError(f"Unknown capital flows metric: {category}/{subcategory}")
        return await self.fetch_series(config["series_id"], start_date, end_date)

    async def fetch_priority_capital_flows_data(
        self, start_date: date, end_date: date
    ) -> Dict:
        """Fetch all priority capital flows series."""
        results = {}
        for category, subcategories in self.CAPITAL_FLOWS_SERIES.items():
            for subcat_key, config in subcategories.items():
                key = f"{category}_{subcat_key}"
                try:
                    data = await self.fetch_series(config["series_id"], start_date, end_date)
                    data["data_category"] = category
                    results[key] = data
                except Exception as e:
                    results[key] = {"error": str(e), "series_id": config["series_id"]}
        return results

    async def fetch_private_sector_metric(
        self, series_id: str, start_date: date, end_date: date
    ) -> Dict:
        """Fetch a private sector liquidity metric."""
        return await self.fetch_series(series_id, start_date, end_date)

    # -------------------------------------------------------------------------
    # Mock data generators
    # -------------------------------------------------------------------------

    def _generate_mock_series(
        self, series_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict:
        """Generate mock time series data."""
        if not start_date:
            start_date = date.today() - timedelta(days=365)
        if not end_date:
            end_date = date.today()

        base_values = {
            # Central bank balance sheets (in FRED native units)
            "WALCL": 7_500_000,   # Fed ~7.5T (millions USD)
            "ECBASSETSW": 6_800_000,  # ECB ~6.8T EUR (millions EUR)
            "JPNASSETS": 7_500_000,  # BOJ ~750T JPY (100 million JPY)
            "UKASSETS": 850_000,   # BOE ~850B GBP (millions GBP)
            "SNBASSETS": 800_000,  # SNB ~800B CHF (millions CHF)
            "BCASSETS": 400_000,   # BOC ~400B CAD (millions CAD)
            "RBASSETS": 550_000,   # RBA ~550B AUD (millions AUD)
            "CHNASSETS": 4_930_000_000,  # PBOC ~49.3T CNY (value/unit_scale=trillions)
            # Exchange rates
            "DEXUSEU": 1.08,
            "DEXJPUS": 150.0,
            "DEXUSUK": 1.27,
            "DEXSZUS": 0.88,
            "DEXCAUS": 1.36,
            "DEXUSAL": 0.65,
            "DEXCHUS": 7.25,  # CNY per USD
            # Private sector (billions)
            "M2SL": 21_000,
            "MMMFAQ027S": 6_200,
            "COMPOUT": 1_200,
            "PDREPO": 3_500,
            "PDREVREPO": 2_800,
            "TOTBKCR": 17_500,
            # Capital flows (millions)
            "BOGZ1FL263090005Q": 35_000_000,
            "BOGZ1FL263061105Q": 8_000_000,
            "BOGZ1FL263064105Q": 12_000_000,
            "BOGZ1FL263063005Q": 5_000_000,
            "BOGZ1FL263061705Q": 2_000_000,
            "BOPGSTB": -70_000,
            "BOPBCA": -200_000,
            "BOPFINA": -180_000,
            "BOPFINB": 180_000,
            "BOPFDI": -50_000,
            "BOPPORT": 100_000,
            # Market indicators & Fed facilities
            "RRPONTSYD": 200_000,  # ON RRP ~$200B (millions USD)
            "TREAST": 4_200_000,   # Fed Treasury holdings ~$4.2T (millions USD)
            "WSHOMCB": 2_200_000,  # Fed MBS holdings ~$2.2T (millions USD)
            "VIXCLS": 18.5,
            "T10Y2Y": 0.42,
            "DGS10": 4.25,
            "DGS2": 3.83,
            "BAMLH0A0HYM2": 3.45,
            "BAMLC0A4CBBB": 1.28,
            "T10YIE": 2.35,
            # Asset prices
            "SP500": 5820,
            "GOLDAMGBD228NLBM": 2950,
            "CBBTCUSD": 95000,
            # Buffett Indicator (Market Cap / GDP as percentage)
            "DDDM01USA156NWDB": 209.0,
            "DDDM01JPA156NWDB": 148.0,
            "DDDM01CNA156NWDB": 65.0,
            "DDDM01GBA156NWDB": 105.0,
            "DDDM01DEA156NWDB": 52.0,
            "DDDM01FRA156NWDB": 85.0,
            "DDDM01CAA156NWDB": 140.0,
            "DDDM01INA156NWDB": 112.0,
            "DDDM01KRA156NWDB": 95.0,
            "DDDM01BRA156NWDB": 45.0,
            # GDP (billions)
            "GDP": 28_300,
            "NYGDPMKTPCDWLD": 105_000,
            "JPNNGDP": 4_200,
        }
        base = base_values.get(series_id, 1000)

        observations = []
        current = start_date
        value = float(base)
        while current <= end_date:
            # Skip weekends for daily series
            if current.weekday() < 5:
                drift = value * random.uniform(-0.002, 0.003)
                value += drift
                observations.append({"date": current, "value": round(value, 2)})
            current += timedelta(days=1)

        return {"series_id": series_id, "observations": observations}
