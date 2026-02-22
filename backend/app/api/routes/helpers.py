"""Shared helpers used by multiple route modules."""

from datetime import date, timedelta

TIMEFRAME_DAYS = {
    "1M": 30, "3M": 90, "6M": 180, "1Y": 365,
    "2Y": 730, "5Y": 1825, "ALL": 3650,
}


def _cycle_position(change_1m: float) -> str:
    if change_1m > 1:
        return "expansion"
    if change_1m > 0:
        return "recovery"
    if change_1m > -1:
        return "slowdown"
    return "contraction"
