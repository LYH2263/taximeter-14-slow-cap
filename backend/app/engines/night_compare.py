from app.config import DEFAULT_SLOW_FEE_CAP
from app.engines.tariff_breakdown import calc_fare


def compare_day_night(
    distance_km: float,
    slow_min: float,
    tariff: dict,
    slow_cap: float = DEFAULT_SLOW_FEE_CAP,
) -> dict:
    day = calc_fare(distance_km, slow_min, False, tariff, slow_cap)
    night = calc_fare(distance_km, slow_min, True, tariff, slow_cap)
    return {
        "distance_km": day["distance_km"],
        "slow_min": day["slow_min"],
        "day_total": day["total"],
        "night_total": night["total"],
        "delta": round(night["total"] - day["total"], 2),
        "day": day,
        "night": night,
    }
