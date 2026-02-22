"""Liquidity Flows / Destination endpoints."""

from datetime import date
import random

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

def _mock_valuations() -> list:
    countries = [
        {"country": "United States", "country_code": "USA", "ratio": 209.0, "gdp_share": 22.0, "mcap_share": 48.5, "gdp_usd": 28.3},
        {"country": "Japan", "country_code": "JPA", "ratio": 148.0, "gdp_share": 4.0, "mcap_share": 6.2, "gdp_usd": 4.2},
        {"country": "Canada", "country_code": "CAA", "ratio": 140.0, "gdp_share": 1.9, "mcap_share": 2.8, "gdp_usd": 2.1},
        {"country": "India", "country_code": "INA", "ratio": 112.0, "gdp_share": 3.5, "mcap_share": 4.1, "gdp_usd": 3.7},
        {"country": "United Kingdom", "country_code": "GBA", "ratio": 105.0, "gdp_share": 3.2, "mcap_share": 3.5, "gdp_usd": 3.3},
        {"country": "South Korea", "country_code": "KRA", "ratio": 95.0, "gdp_share": 1.6, "mcap_share": 1.6, "gdp_usd": 1.7},
        {"country": "France", "country_code": "FRA", "ratio": 85.0, "gdp_share": 2.9, "mcap_share": 2.6, "gdp_usd": 3.0},
        {"country": "China", "country_code": "CNA", "ratio": 65.0, "gdp_share": 17.0, "mcap_share": 11.6, "gdp_usd": 17.9},
        {"country": "Germany", "country_code": "DEA", "ratio": 52.0, "gdp_share": 4.3, "mcap_share": 2.4, "gdp_usd": 4.5},
        {"country": "Brazil", "country_code": "BRA", "ratio": 45.0, "gdp_share": 1.9, "mcap_share": 0.9, "gdp_usd": 2.0},
    ]
    for c in countries:
        if c["ratio"] > 150:
            c["signal"] = "extreme"
        elif c["ratio"] > 100:
            c["signal"] = "elevated"
        elif c["ratio"] > 50:
            c["signal"] = "fair"
        else:
            c["signal"] = "undervalued"
        c["mcap_usd"] = round(c["gdp_usd"] * c["ratio"] / 100, 2)
        c["date"] = date.today().isoformat()
    return countries


def _mock_liquidity_flows_direction() -> dict:
    return {
        "date": date.today().isoformat(),
        "total_global_flows": 1250.0,
        "flows": [
            {"region": "United States", "flow_type": "inflow", "amount": 750.0, "share_pct": 60.0, "change_pct": 2.3, "direction": "increasing"},
            {"region": "Europe (DM)", "flow_type": "inflow", "amount": 250.0, "share_pct": 20.0, "change_pct": -1.1, "direction": "decreasing"},
            {"region": "EM Asia", "flow_type": "inflow", "amount": 112.5, "share_pct": 9.0, "change_pct": 3.8, "direction": "increasing"},
            {"region": "Japan", "flow_type": "inflow", "amount": 62.5, "share_pct": 5.0, "change_pct": -0.5, "direction": "flat"},
            {"region": "EM LatAm", "flow_type": "inflow", "amount": 50.0, "share_pct": 4.0, "change_pct": 1.2, "direction": "increasing"},
            {"region": "Other", "flow_type": "inflow", "amount": 25.0, "share_pct": 2.0, "change_pct": -0.3, "direction": "flat"},
        ],
        "dm_vs_em": {
            "dm_share": 85.0,
            "em_share": 15.0,
            "dm_to_em_trend": "decreasing",
        },
    }


def _mock_historical_comparison() -> dict:
    random.seed(1989)
    japan_data = []
    jp_val = 30.0
    for year in range(1975, 2011):
        if year <= 1989:
            jp_val += random.uniform(3, 12)
        elif year <= 1992:
            jp_val -= random.uniform(10, 20)
        else:
            jp_val += random.uniform(-3, 2)
        jp_val = max(jp_val, 40)
        japan_data.append({"year": year, "ratio": round(jp_val, 1)})

    random.seed(2024)
    us_data = []
    us_val = 55.0
    for year in range(1990, 2026):
        if year <= 2000:
            us_val += random.uniform(5, 15)
        elif year <= 2002:
            us_val -= random.uniform(10, 20)
        elif year <= 2007:
            us_val += random.uniform(3, 10)
        elif year <= 2009:
            us_val -= random.uniform(15, 25)
        elif year <= 2020:
            us_val += random.uniform(5, 12)
        elif year <= 2022:
            us_val += random.uniform(-5, 15)
        else:
            us_val += random.uniform(8, 18)
        us_val = max(us_val, 60)
        us_data.append({"year": year, "ratio": round(us_val, 1)})

    for d in japan_data:
        if d["year"] == 1989:
            d["ratio"] = 140.0
    for d in us_data:
        if d["year"] == 2024:
            d["ratio"] = 209.0
        if d["year"] == 2025:
            d["ratio"] = 205.0

    return {
        "japan": japan_data,
        "us": us_data,
        "peak_comparison": {
            "japan_peak_year": 1989,
            "japan_peak_ratio": 140.0,
            "japan_gdp_share_at_peak": 18.0,
            "japan_mcap_share_at_peak": 48.0,
            "us_current_year": 2024,
            "us_current_ratio": 209.0,
            "us_gdp_share": 22.0,
            "us_mcap_share": 48.5,
            "warning": "US currently exceeds Japan's 1989 peak by 49 percentage points",
        },
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/liquidity-flows/valuations")
def get_valuations(db: Session = Depends(get_db)):
    """Global valuation heatmap - Buffett Indicator by country."""
    try:
        from app.models.liquidity_valuation import LiquidityValuation
        from sqlalchemy import func

        latest_subq = (
            db.query(
                LiquidityValuation.country_code,
                func.max(LiquidityValuation.date).label("max_date"),
            )
            .group_by(LiquidityValuation.country_code)
            .subquery()
        )

        rows = (
            db.query(LiquidityValuation)
            .join(
                latest_subq,
                (LiquidityValuation.country_code == latest_subq.c.country_code)
                & (LiquidityValuation.date == latest_subq.c.max_date),
            )
            .all()
        )

        if rows:
            gdp_shares = {
                "USA": 22.0, "JPA": 4.0, "CNA": 17.0, "GBA": 3.2, "DEA": 4.3,
                "FRA": 2.9, "CAA": 1.9, "INA": 3.5, "KRA": 1.6, "BRA": 1.9,
            }
            total_mcap = 0
            entries = []
            for r in rows:
                ratio = float(r.market_cap_to_gdp) if r.market_cap_to_gdp else 0
                gdp = float(r.gdp_usd) if r.gdp_usd else 0
                mcap = float(r.market_cap_usd) if r.market_cap_usd else round(gdp * ratio / 100, 2)
                total_mcap += mcap
                entries.append((r, ratio, gdp, mcap))

            result = []
            for r, ratio, gdp, mcap in entries:
                if ratio > 150:
                    signal = "extreme"
                elif ratio > 100:
                    signal = "elevated"
                elif ratio > 50:
                    signal = "fair"
                else:
                    signal = "undervalued"

                result.append({
                    "country": r.country_name,
                    "country_code": r.country_code,
                    "ratio": round(ratio, 1),
                    "gdp_usd": round(gdp, 2),
                    "mcap_usd": round(mcap, 2),
                    "gdp_share": gdp_shares.get(r.country_code, 0),
                    "mcap_share": round(mcap / total_mcap * 100, 1) if total_mcap else 0,
                    "signal": signal,
                    "date": r.date.isoformat(),
                })
            result.sort(key=lambda x: x["ratio"], reverse=True)
            return result
    except Exception:
        pass
    return _mock_valuations()


@router.get("/liquidity-flows/direction")
def get_liquidity_flow_direction(db: Session = Depends(get_db)):
    """Where is global liquidity flowing? Regional breakdown."""
    try:
        from app.models.capital_flows import CapitalFlowIndex
        latest = db.query(CapitalFlowIndex).order_by(CapitalFlowIndex.index_date.desc()).first()
        if latest:
            total = float(latest.total_global_flows) if latest.total_global_flows else 0
            us_net = float(latest.us_net_flows) if latest.us_net_flows else 0
            dm_em = float(latest.dm_to_em_flows) if latest.dm_to_em_flows else 0

            us_share = round((us_net / total * 100), 1) if total else 60.0
            return {
                "date": latest.index_date.isoformat(),
                "total_global_flows": round(total, 1),
                "flows": [
                    {"region": "United States", "flow_type": "inflow", "amount": round(us_net, 1), "share_pct": us_share, "change_pct": 0, "direction": "increasing"},
                    {"region": "Emerging Markets", "flow_type": "inflow", "amount": round(dm_em, 1), "share_pct": round(dm_em / total * 100, 1) if total else 15.0, "change_pct": 0, "direction": "flat"},
                ],
                "dm_vs_em": {
                    "dm_share": round(100 - (dm_em / total * 100), 1) if total else 85.0,
                    "em_share": round(dm_em / total * 100, 1) if total else 15.0,
                    "dm_to_em_trend": "decreasing",
                },
            }
    except Exception:
        pass
    return _mock_liquidity_flows_direction()


@router.get("/liquidity-flows/historical-comparison")
def get_historical_comparison(db: Session = Depends(get_db)):
    """Japan 1989 vs US today - Buffett Indicator historical comparison."""
    try:
        from app.models.liquidity_valuation import LiquidityValuation

        us_rows = (
            db.query(LiquidityValuation)
            .filter(LiquidityValuation.country_code == "USA")
            .order_by(LiquidityValuation.date)
            .all()
        )
        jp_rows = (
            db.query(LiquidityValuation)
            .filter(LiquidityValuation.country_code == "JPA")
            .order_by(LiquidityValuation.date)
            .all()
        )

        if us_rows and jp_rows:
            us_by_year = {}
            for r in us_rows:
                us_by_year[r.date.year] = {"year": r.date.year, "ratio": round(float(r.market_cap_to_gdp), 1)}
            jp_by_year = {}
            for r in jp_rows:
                jp_by_year[r.date.year] = {"year": r.date.year, "ratio": round(float(r.market_cap_to_gdp), 1)}

            jp_peak = max(jp_by_year.values(), key=lambda x: x["ratio"])
            us_latest = max(us_by_year.values(), key=lambda x: x["year"])

            return {
                "japan": sorted(jp_by_year.values(), key=lambda x: x["year"]),
                "us": sorted(us_by_year.values(), key=lambda x: x["year"]),
                "peak_comparison": {
                    "japan_peak_year": jp_peak["year"],
                    "japan_peak_ratio": jp_peak["ratio"],
                    "japan_gdp_share_at_peak": 18.0,
                    "japan_mcap_share_at_peak": 48.0,
                    "us_current_year": us_latest["year"],
                    "us_current_ratio": us_latest["ratio"],
                    "us_gdp_share": 22.0,
                    "us_mcap_share": 48.5,
                    "warning": f"US currently at {us_latest['ratio']}% vs Japan's peak of {jp_peak['ratio']}%",
                },
            }
    except Exception:
        pass
    return _mock_historical_comparison()
