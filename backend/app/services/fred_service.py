import httpx
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from app.config import settings


class FREDService:
    """Service for fetching data from FRED API"""

    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    # FRED Series IDs
    SERIES_IDS = {
        "fed_balance_sheet": "WALCL",  # Federal Reserve Total Assets
        "treasury_general_account": "WDTGAL",  # Treasury General Account
        "reverse_repo": "RRPONTSYD",  # Overnight Reverse Repurchase Agreements
    }

    def __init__(self):
        self.api_key = settings.FRED_API_KEY

    async def fetch_series(
        self,
        series_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch data for a specific FRED series

        Args:
            series_id: FRED series identifier
            start_date: Start date for data
            end_date: End date for data

        Returns:
            List of observations with date and value
        """
        if not self.api_key:
            print("⚠️  FRED API key not configured. Using mock data.")
            return self._get_mock_data(series_id)

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }

        if start_date:
            params["observation_start"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["observation_end"] = end_date.strftime("%Y-%m-%d")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL, params=params, timeout=30.0)
                response.raise_for_status()

                data = response.json()

                if "observations" not in data:
                    print(f"⚠️  No observations found for series {series_id}")
                    return []

                observations = []
                for obs in data["observations"]:
                    if obs["value"] != ".":  # FRED uses "." for missing values
                        observations.append({
                            "date": datetime.strptime(obs["date"], "%Y-%m-%d").date(),
                            "value": float(obs["value"])
                        })

                return observations

        except httpx.HTTPError as e:
            print(f"❌ Error fetching FRED data: {e}")
            return self._get_mock_data(series_id)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return self._get_mock_data(series_id)

    async def fetch_fed_balance_sheet(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Fetch Federal Reserve balance sheet data"""
        return await self.fetch_series(
            self.SERIES_IDS["fed_balance_sheet"],
            start_date,
            end_date
        )

    async def fetch_treasury_general_account(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Fetch Treasury General Account data"""
        return await self.fetch_series(
            self.SERIES_IDS["treasury_general_account"],
            start_date,
            end_date
        )

    async def fetch_reverse_repo(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Fetch Reverse Repo data"""
        return await self.fetch_series(
            self.SERIES_IDS["reverse_repo"],
            start_date,
            end_date
        )

    async def fetch_all_fed_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all Fed-related data series"""
        results = {}

        for key, series_id in self.SERIES_IDS.items():
            results[key] = await self.fetch_series(series_id, start_date, end_date)

        return results

    def _get_mock_data(self, series_id: str) -> List[Dict[str, Any]]:
        """Generate mock data for testing without API key"""
        from datetime import timedelta
        import random

        mock_data = []
        current_date = date.today() - timedelta(days=365)
        end_date = date.today()

        # Base values for different series
        base_values = {
            self.SERIES_IDS["fed_balance_sheet"]: 7000000,  # $7T in millions
            self.SERIES_IDS["treasury_general_account"]: 500000,  # $500B in millions
            self.SERIES_IDS["reverse_repo"]: 300000,  # $300B in millions
        }

        base_value = base_values.get(series_id, 1000000)

        while current_date <= end_date:
            variation = random.uniform(-0.02, 0.02)
            value = base_value * (1 + variation)

            mock_data.append({
                "date": current_date,
                "value": round(value, 2)
            })

            current_date += timedelta(days=7)  # Weekly data

        return mock_data

    def convert_to_trillions(self, value_in_millions: float) -> float:
        """Convert value from millions to trillions"""
        return value_in_millions / 1_000_000
