from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from decimal import Decimal

from app.models.central_bank_data import CentralBankData
from app.models.global_liquidity_index import GlobalLiquidityIndex
from app.services.fred_service import FREDService


class DataIngestionService:
    """Service for ingesting data from external sources and calculating GLI"""

    def __init__(self, db: Session):
        self.db = db
        self.fred_service = FREDService()

    async def refresh_all_data(self) -> Dict[str, Any]:
        """Refresh all data sources"""
        results = {
            "fed_data": await self.ingest_fed_data(),
            "gli_calculated": await self.calculate_and_store_gli()
        }

        return results

    async def ingest_fed_data(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Ingest Federal Reserve data from FRED

        Args:
            days_back: Number of days of historical data to fetch
        """
        start_date = date.today() - timedelta(days=days_back)
        end_date = date.today()

        print(f"📥 Fetching Fed data from {start_date} to {end_date}...")

        # Fetch all Fed data
        fed_data = await self.fred_service.fetch_all_fed_data(start_date, end_date)

        records_added = 0

        # Store Fed Balance Sheet
        for obs in fed_data.get("fed_balance_sheet", []):
            self._store_central_bank_data(
                source="FED",
                indicator="balance_sheet",
                date=obs["date"],
                value=self.fred_service.convert_to_trillions(obs["value"]),
                currency="USD",
                unit="trillions"
            )
            records_added += 1

        # Store TGA
        for obs in fed_data.get("treasury_general_account", []):
            self._store_central_bank_data(
                source="FED",
                indicator="tga",
                date=obs["date"],
                value=self.fred_service.convert_to_trillions(obs["value"]),
                currency="USD",
                unit="trillions"
            )
            records_added += 1

        # Store Reverse Repo
        for obs in fed_data.get("reverse_repo", []):
            self._store_central_bank_data(
                source="FED",
                indicator="rrp",
                date=obs["date"],
                value=self.fred_service.convert_to_trillions(obs["value"]),
                currency="USD",
                unit="trillions"
            )
            records_added += 1

        self.db.commit()

        return {
            "status": "success",
            "records_added": records_added,
            "date_range": f"{start_date} to {end_date}"
        }

    def _store_central_bank_data(
        self,
        source: str,
        indicator: str,
        date: date,
        value: float,
        currency: str,
        unit: str
    ):
        """Store or update central bank data record"""
        existing = self.db.query(CentralBankData).filter(
            CentralBankData.source == source,
            CentralBankData.indicator == indicator,
            CentralBankData.date == date
        ).first()

        if existing:
            existing.value = Decimal(str(value))
            existing.currency = currency
            existing.unit = unit
        else:
            record = CentralBankData(
                source=source,
                indicator=indicator,
                date=date,
                value=Decimal(str(value)),
                currency=currency,
                unit=unit
            )
            self.db.add(record)

    async def calculate_and_store_gli(self) -> Dict[str, Any]:
        """
        Calculate Global Liquidity Index and store it

        Formula: GLI = FED - TGA - RRP + ECB + PBoC + BOJ + ... (other central banks)
        """
        print("🧮 Calculating Global Liquidity Index...")

        # Get unique dates from central bank data
        dates = self.db.query(CentralBankData.date).distinct().all()

        gli_records_added = 0

        for (date_val,) in dates:
            # Get Fed components for this date
            fed_balance = self._get_cb_value("FED", "balance_sheet", date_val)
            tga = self._get_cb_value("FED", "tga", date_val)
            rrp = self._get_cb_value("FED", "rrp", date_val)

            if fed_balance is None:
                continue

            # Calculate Fed Net (FED - TGA - RRP)
            fed_net = fed_balance - (tga or 0) - (rrp or 0)

            # For MVP, we'll start with just Fed data
            # Later: add ECB, PBoC, BOJ, etc.
            gli_value = fed_net

            # Store GLI
            existing_gli = self.db.query(GlobalLiquidityIndex).filter(
                GlobalLiquidityIndex.date == date_val
            ).first()

            if existing_gli:
                existing_gli.value = Decimal(str(gli_value))
            else:
                gli_record = GlobalLiquidityIndex(
                    date=date_val,
                    value=Decimal(str(gli_value)),
                    cycle_position="expansion"  # Simplified for now
                )
                self.db.add(gli_record)
                gli_records_added += 1

        self.db.commit()

        # Calculate percentage changes
        await self._calculate_gli_changes()

        return {
            "status": "success",
            "gli_records_added": gli_records_added
        }

    def _get_cb_value(self, source: str, indicator: str, date: date) -> float:
        """Get central bank data value for specific date"""
        record = self.db.query(CentralBankData).filter(
            CentralBankData.source == source,
            CentralBankData.indicator == indicator,
            CentralBankData.date == date
        ).first()

        return float(record.value) if record else None

    async def _calculate_gli_changes(self):
        """Calculate percentage changes for GLI"""
        # Get all GLI records ordered by date
        gli_records = self.db.query(GlobalLiquidityIndex).order_by(
            GlobalLiquidityIndex.date
        ).all()

        for i, record in enumerate(gli_records):
            # Calculate 1-day change
            if i > 0:
                prev_value = float(gli_records[i - 1].value)
                current_value = float(record.value)
                change = ((current_value - prev_value) / prev_value) * 100
                record.change_pct = Decimal(str(round(change, 4)))

            # Calculate 1-month change
            month_ago = record.date - timedelta(days=30)
            month_ago_record = self.db.query(GlobalLiquidityIndex).filter(
                GlobalLiquidityIndex.date <= month_ago
            ).order_by(GlobalLiquidityIndex.date.desc()).first()

            if month_ago_record:
                prev_value = float(month_ago_record.value)
                current_value = float(record.value)
                change = ((current_value - prev_value) / prev_value) * 100
                record.change_1m_pct = Decimal(str(round(change, 4)))

        self.db.commit()
