from app.engines.tariff_breakdown import calc_fare


def compare_day_night(distance_km: float, slow_min: float, tariff: dict, slow_fee_cap: float | None = None) -> dict:
    day = calc_fare(distance_km, slow_min, False, tariff, slow_fee_cap)
    night = calc_fare(distance_km, slow_min, True, tariff, slow_fee_cap)
    return {
        "distance_km": day["distance_km"],
        "slow_min": day["slow_min"],
        "slow_fee_cap": day["slow_fee_cap"],
        "day_total": day["total"],
        "night_total": night["total"],
        "delta": round(night["total"] - day["total"], 2),
        "day_slow_fee_truncated": day["slow_fee_truncated"],
        "night_slow_fee_truncated": night["slow_fee_truncated"],
        "day": day,
        "night": night,
    }
