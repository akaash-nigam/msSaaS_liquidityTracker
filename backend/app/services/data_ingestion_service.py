from datetime import date, timedelta
from decimal import Decimal
from typing import Dict

from sqlalchemy.orm import Session

from app.models.base_models import CentralBankData, GlobalLiquidityIndex, ExchangeRate
from app.models.private_sector_liquidity import (
    PrivateSectorLiquidity,
    PrivateSectorLiquidityIndex,
    EnhancedGlobalLiquidityIndex,
)
from app.services.fred_service import FREDService


class DataIngestionService:
    """Orchestrates data fetching from FRED and storage into TimescaleDB."""

    PRIORITY_PRIVATE_SECTOR = {
        "M2SL": {"name": "M2 Money Stock", "category": "shadow_banking", "frequency": "monthly"},
        "MMMFAQ027S": {"name": "Money Market Funds", "category": "shadow_banking", "frequency": "quarterly"},
        "COMPOUT": {"name": "Commercial Paper", "category": "shadow_banking", "frequency": "weekly"},
        "PDREPO": {"name": "Primary Dealer Repos", "category": "shadow_banking", "frequency": "weekly"},
        "PDREVREPO": {"name": "Primary Dealer Reverse Repos", "category": "shadow_banking", "frequency": "weekly"},
        "TOTBKCR": {"name": "Total Bank Credit", "category": "traditional_banking", "frequency": "weekly"},
    }

    def __init__(self, db: Session):
        self.db = db
        self.fred = FREDService()

    # ------------------------------------------------------------------
    # Phase 1: Central bank + GLI
    # ------------------------------------------------------------------

    async def ingest_fed_data(self, days_back: int = 365) -> Dict:
        """Fetch Federal Reserve balance sheet data and store it."""
        end = date.today()
        start = end - timedelta(days=days_back)

        all_banks = ["FED", "ECB", "BOJ", "BOE", "SNB", "BOC", "RBA", "PBOC"]
        records_added = 0
        min_date = None
        max_date = None

        # FRED exchange rate conventions:
        #   DEXUSEU (EUR), DEXUSUK (GBP), DEXUSAL (AUD) → "USD per local" → store as-is
        #   DEXJPUS (JPY), DEXSZUS (CHF), DEXCAUS (CAD) → "local per USD" → invert
        invert_currencies = {"JPY", "CHF", "CAD", "CNY"}

        # Fetch exchange rates first
        for currency in ["EUR", "JPY", "GBP", "CHF", "CAD", "AUD", "CNY"]:
            data = await self.fred.fetch_exchange_rates(currency, start, end)
            for obs in data["observations"]:
                existing = self.db.query(ExchangeRate).filter(
                    ExchangeRate.from_currency == currency,
                    ExchangeRate.date == obs["date"],
                ).first()
                if not existing:
                    raw_rate = Decimal(str(obs["value"]))
                    # Normalize to "USD per unit of foreign currency"
                    rate = (1 / raw_rate) if currency in invert_currencies else raw_rate
                    self.db.add(ExchangeRate(
                        from_currency=currency,
                        to_currency="USD",
                        date=obs["date"],
                        rate=rate,
                        series_id=data["series_id"],
                        data_source="FRED",
                    ))

        # Fetch central bank data
        for bank in all_banks:
            data = await self.fred.fetch_central_bank_data(bank, start, end)
            config = self.fred.CENTRAL_BANK_SERIES[bank]
            for obs in data["observations"]:
                obs_date = obs["date"]
                value_trillions = Decimal(str(obs["value"])) / Decimal(str(config["unit_scale"]))

                existing = self.db.query(CentralBankData).filter(
                    CentralBankData.source == bank,
                    CentralBankData.indicator == "balance_sheet",
                    CentralBankData.date == obs_date,
                ).first()
                if not existing:
                    self.db.add(CentralBankData(
                        source=bank,
                        indicator="balance_sheet",
                        value=value_trillions,
                        currency=config["currency"],
                        date=obs_date,
                        series_id=data["series_id"],
                        data_source="FRED",
                    ))
                    records_added += 1
                    if min_date is None or obs_date < min_date:
                        min_date = obs_date
                    if max_date is None or obs_date > max_date:
                        max_date = obs_date

        self.db.commit()
        return {
            "status": "success",
            "records_added": records_added,
            "date_range": f"{min_date} to {max_date}" if min_date else "no data",
        }

    async def calculate_and_store_gli(self) -> Dict:
        """Calculate Global Liquidity Index from central bank data."""
        from sqlalchemy import distinct, func

        dates = (
            self.db.query(distinct(CentralBankData.date))
            .order_by(CentralBankData.date)
            .all()
        )
        gli_added = 0

        for (d,) in dates:
            existing = self.db.query(GlobalLiquidityIndex).filter(
                GlobalLiquidityIndex.date == d
            ).first()
            if existing:
                continue

            total_usd = Decimal("0")
            banks = self.db.query(CentralBankData).filter(
                CentralBankData.date == d,
                CentralBankData.indicator == "balance_sheet",
            ).all()

            for bank in banks:
                value_usd = bank.value
                if bank.currency != "USD":
                    fx = self.db.query(ExchangeRate).filter(
                        ExchangeRate.from_currency == bank.currency,
                        ExchangeRate.date == d,
                    ).first()
                    if fx:
                        value_usd = bank.value * fx.rate
                total_usd += value_usd

            if total_usd > 0:
                # Calculate changes
                prev = self.db.query(GlobalLiquidityIndex).filter(
                    GlobalLiquidityIndex.date < d
                ).order_by(GlobalLiquidityIndex.date.desc()).first()
                change_pct = None
                if prev and prev.value:
                    change_pct = ((total_usd - prev.value) / prev.value) * 100

                prev_1m = self.db.query(GlobalLiquidityIndex).filter(
                    GlobalLiquidityIndex.date <= d - timedelta(days=30)
                ).order_by(GlobalLiquidityIndex.date.desc()).first()
                change_1m = None
                if prev_1m and prev_1m.value:
                    change_1m = ((total_usd - prev_1m.value) / prev_1m.value) * 100

                self.db.add(GlobalLiquidityIndex(
                    date=d,
                    value=total_usd,
                    change_pct=change_pct,
                    change_1m_pct=change_1m,
                    num_sources=len(banks),
                ))
                gli_added += 1

        self.db.commit()
        return {"status": "success", "gli_records_added": gli_added}

    async def refresh_all_data(self, days_back: int = 365) -> Dict:
        """Refresh all data: exchange rates, central banks, GLI."""
        results = {}
        fed = await self.ingest_fed_data(days_back)
        results["exchange_rates"] = {
            "status": "success",
            "records_added": 0,
            "currencies": list(self.fred.EXCHANGE_RATE_SERIES.keys()),
            "date_range": fed["date_range"],
        }
        results["central_banks"] = fed
        gli = await self.calculate_and_store_gli()
        results["gli_calculated"] = gli
        return results

    # ------------------------------------------------------------------
    # Phase 2: Private sector liquidity
    # ------------------------------------------------------------------

    async def ingest_priority_private_sector_data(self, days_back: int = 365) -> Dict:
        """Fetch priority private sector metrics from FRED."""
        end = date.today()
        start = end - timedelta(days=days_back)
        records_added = 0
        metrics = {}
        min_date = None
        max_date = None

        for series_id, config in self.PRIORITY_PRIVATE_SECTOR.items():
            data = await self.fred.fetch_private_sector_metric(series_id, start, end)
            count = 0
            for obs in data["observations"]:
                existing = self.db.query(PrivateSectorLiquidity).filter(
                    PrivateSectorLiquidity.series_id == series_id,
                    PrivateSectorLiquidity.date == obs["date"],
                ).first()
                if not existing:
                    self.db.add(PrivateSectorLiquidity(
                        date=obs["date"],
                        metric_name=config["name"],
                        series_id=series_id,
                        value=Decimal(str(obs["value"])),
                        unit="billions_usd",
                        frequency=config["frequency"],
                        category=config["category"],
                        data_source="FRED",
                    ))
                    count += 1
                    if min_date is None or obs["date"] < min_date:
                        min_date = obs["date"]
                    if max_date is None or obs["date"] > max_date:
                        max_date = obs["date"]
            metrics[config["name"]] = count
            records_added += count

        self.db.commit()
        return {
            "status": "success",
            "records_added": records_added,
            "metrics": metrics,
            "date_range": f"{min_date} to {max_date}" if min_date else "no data",
        }

    async def calculate_and_store_private_sector_index(self) -> Dict:
        """Calculate TPSL (Total Private Sector Liquidity) index."""
        from sqlalchemy import distinct

        dates = (
            self.db.query(distinct(PrivateSectorLiquidity.date))
            .order_by(PrivateSectorLiquidity.date)
            .all()
        )
        added = 0

        for (d,) in dates:
            existing = self.db.query(PrivateSectorLiquidityIndex).filter(
                PrivateSectorLiquidityIndex.date == d
            ).first()
            if existing:
                continue

            def get_val(sid):
                rec = self.db.query(PrivateSectorLiquidity).filter(
                    PrivateSectorLiquidity.series_id == sid,
                    PrivateSectorLiquidity.date == d,
                ).first()
                return Decimal(str(rec.value)) / 1000 if rec else None  # billions→trillions

            m2 = get_val("M2SL")
            mmf = get_val("MMMFAQ027S")
            cp = get_val("COMPOUT")
            repos = get_val("PDREPO")
            rev_repos = get_val("PDREVREPO")
            bank_credit = get_val("TOTBKCR")

            repos_net = None
            if repos is not None and rev_repos is not None:
                repos_net = repos - rev_repos

            components = [v for v in [m2, mmf, cp, repos_net, bank_credit] if v is not None]
            if not components:
                continue

            total = sum(components)
            self.db.add(PrivateSectorLiquidityIndex(
                date=d,
                total_value=total,
                m2_value=m2,
                mmf_value=mmf,
                commercial_paper_value=cp,
                repos_net_value=repos_net,
                bank_credit_value=bank_credit,
                num_components=len(components),
                data_quality="full" if len(components) == 5 else "partial",
            ))
            added += 1

        self.db.commit()
        return {"status": "success", "psli_records_added": added}

    async def calculate_and_store_enhanced_gli(self) -> Dict:
        """Calculate Enhanced GLI = Central Bank Liquidity + Private Sector Liquidity."""
        from sqlalchemy import distinct

        dates = (
            self.db.query(distinct(GlobalLiquidityIndex.date))
            .order_by(GlobalLiquidityIndex.date)
            .all()
        )
        added = 0

        for (d,) in dates:
            existing = self.db.query(EnhancedGlobalLiquidityIndex).filter(
                EnhancedGlobalLiquidityIndex.date == d
            ).first()
            if existing:
                continue

            gli = self.db.query(GlobalLiquidityIndex).filter(
                GlobalLiquidityIndex.date == d
            ).first()
            psli = self.db.query(PrivateSectorLiquidityIndex).filter(
                PrivateSectorLiquidityIndex.date == d
            ).first()

            if not gli:
                continue
            cb_val = gli.value
            ps_val = psli.total_value if psli else Decimal("0")
            total = cb_val + ps_val

            cb_pct = (cb_val / total * 100) if total else Decimal("0")
            ps_pct = (ps_val / total * 100) if total else Decimal("0")

            self.db.add(EnhancedGlobalLiquidityIndex(
                date=d,
                total_value=total,
                central_bank_liquidity=cb_val,
                private_sector_liquidity=ps_val,
                cb_percentage=cb_pct,
                ps_percentage=ps_pct,
            ))
            added += 1

        self.db.commit()
        return {"status": "success", "egli_records_added": added}
