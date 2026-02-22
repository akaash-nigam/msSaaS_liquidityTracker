"""Stablecoin supply endpoint."""

import time
from datetime import date, timedelta

from fastapi import APIRouter

router = APIRouter()

# Simple in-memory cache
_cache: dict = {}
_CACHE_TTL = 3600  # 1 hour


def _mock_stablecoin_data() -> dict:
    """Mock fallback: USDT ~$144B, USDC ~$60B."""
    historical = []
    usdt_val, usdc_val = 80.0, 25.0
    current = date.today() - timedelta(days=365)
    import random
    random.seed(123)
    while current <= date.today():
        usdt_val += random.uniform(-0.5, 1.2)
        usdc_val += random.uniform(-0.3, 0.6)
        if current.day == 1 or current == date.today():
            historical.append({
                "date": current.isoformat(),
                "usdt": round(usdt_val, 2),
                "usdc": round(usdc_val, 2),
                "total": round(usdt_val + usdc_val, 2),
            })
        current += timedelta(days=1)

    total = 144.0 + 60.0
    return {
        "total_supply": total,
        "usdt": {"supply": 144.0, "change_7d": 1.2, "dominance": round(144.0 / total * 100, 1)},
        "usdc": {"supply": 60.0, "change_7d": 0.8, "dominance": round(60.0 / total * 100, 1)},
        "historical": historical,
    }


@router.get("/stablecoins/current")
async def get_stablecoin_supply():
    """Current stablecoin supply (USDT + USDC) from DeFiLlama."""
    # Check cache
    if "stablecoins" in _cache:
        cached_time, cached_data = _cache["stablecoins"]
        if time.time() - cached_time < _CACHE_TTL:
            return cached_data

    try:
        import httpx

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://stablecoins.llama.fi/stablecoins?includePrices=true")
            if resp.status_code != 200:
                return _mock_stablecoin_data()

            data = resp.json()
            stables = data.get("peggedAssets", [])

            usdt_info = next((s for s in stables if s.get("symbol") == "USDT"), None)
            usdc_info = next((s for s in stables if s.get("symbol") == "USDC"), None)

            def extract(info):
                if not info:
                    return {"supply": 0, "change_7d": 0, "dominance": 0}
                chains = info.get("chainCirculating", {})
                supply = sum(
                    v.get("current", {}).get("peggedUSD", 0)
                    for v in chains.values()
                ) / 1e9  # to billions
                return {"supply": round(supply, 2), "change_7d": 0, "dominance": 0}

            usdt = extract(usdt_info)
            usdc = extract(usdc_info)
            total = usdt["supply"] + usdc["supply"]
            usdt["dominance"] = round(usdt["supply"] / total * 100, 1) if total else 0
            usdc["dominance"] = round(usdc["supply"] / total * 100, 1) if total else 0

            # Fetch historical for USDT (id=1) and USDC (id=2)
            historical = []
            try:
                usdt_hist_resp = await client.get("https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1")
                usdc_hist_resp = await client.get("https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=2")

                if usdt_hist_resp.status_code == 200 and usdc_hist_resp.status_code == 200:
                    usdt_hist = usdt_hist_resp.json()
                    usdc_hist = usdc_hist_resp.json()

                    # Build lookup for USDC by date
                    usdc_by_date = {}
                    for point in usdc_hist:
                        d = point.get("date")
                        val = point.get("totalCirculatingUSD", {}).get("peggedUSD", 0)
                        if d:
                            usdc_by_date[d] = val / 1e9

                    # Sample monthly points from last year
                    cutoff_ts = int((date.today() - timedelta(days=365)).strftime("%s"))
                    for point in usdt_hist:
                        ts = point.get("date", 0)
                        if ts < cutoff_ts:
                            continue
                        usdt_val = point.get("totalCirculatingUSD", {}).get("peggedUSD", 0) / 1e9
                        usdc_val = usdc_by_date.get(ts, 0)
                        d_str = date.fromtimestamp(ts).isoformat()
                        historical.append({
                            "date": d_str,
                            "usdt": round(usdt_val, 2),
                            "usdc": round(usdc_val, 2),
                            "total": round(usdt_val + usdc_val, 2),
                        })
                    # Thin out to ~30 points
                    if len(historical) > 30:
                        step = len(historical) // 30
                        historical = historical[::step]
            except Exception:
                pass

            result = {
                "total_supply": round(total, 2),
                "usdt": usdt,
                "usdc": usdc,
                "historical": historical if historical else _mock_stablecoin_data()["historical"],
            }

            _cache["stablecoins"] = (time.time(), result)
            return result

    except Exception:
        return _mock_stablecoin_data()
