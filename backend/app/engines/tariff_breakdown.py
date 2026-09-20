def calc_fare(distance_km: float, slow_min: float, night: bool, tariff: dict, slow_fee_cap: float | None = None) -> dict:
    base = float(tariff["start_price"])
    include = float(tariff["start_include_km"])
    per_km = float(tariff["per_km"])
    per_slow = float(tariff["per_slow_min"])
    night_f = float(tariff.get("night_factor", 1.0)) if night else 1.0
    dist = max(0.0, float(distance_km) - include)
    mile = dist * per_km
    slow = float(slow_min) * per_slow
    # 低速费先乘（夜间）系数，再与上限取小
    slow_before_cap = round(slow * night_f, 2)
    cap = float(slow_fee_cap) if slow_fee_cap is not None else None
    truncated = bool(cap is not None and slow_before_cap > cap)
    slow_fee = round(min(slow_before_cap, cap), 2) if cap is not None else slow_before_cap
    sub = base + mile
    # 应付按截断后的低速费计算
    total = round(sub * night_f + slow_fee, 2)
    return {
        "distance_km": round(float(distance_km), 2),
        "slow_min": round(float(slow_min), 1),
        "night": night,
        "night_factor": night_f,
        "start": round(base * night_f, 2),
        "mileage": round(mile * night_f, 2),
        "slow_fee": slow_fee,
        "slow_fee_before_cap": slow_before_cap,
        "slow_fee_truncated": truncated,
        "slow_fee_cap": cap,
        "total": total,
    }
