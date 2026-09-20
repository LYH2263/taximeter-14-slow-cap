from app.config import DEFAULT_SLOW_FEE_CAP

# 浮点"严格大于上限"判定容差，避免二进制误差把恰好等于上限误判为截断
_CAP_EPS = 1e-9


def calc_fare(
    distance_km: float,
    slow_min: float,
    night: bool,
    tariff: dict,
    slow_cap: float = DEFAULT_SLOW_FEE_CAP,
) -> dict:
    base = float(tariff["start_price"])
    include = float(tariff["start_include_km"])
    per_km = float(tariff["per_km"])
    per_slow = float(tariff["per_slow_min"])
    night_f = float(tariff.get("night_factor", 1.0)) if night else 1.0
    cap = float(slow_cap)
    dist = max(0.0, float(distance_km) - include)
    mile = dist * per_km
    # 夜间低速费：先乘夜间系数，再与上限取小
    slow_before = float(slow_min) * per_slow * night_f
    capped = slow_before > cap + _CAP_EPS
    slow_final = min(slow_before, cap)
    total = round(base * night_f + mile * night_f + slow_final, 2)
    return {
        "distance_km": round(float(distance_km), 2),
        "slow_min": round(float(slow_min), 1),
        "night": night,
        "night_factor": night_f,
        "start": round(base * night_f, 2),
        "mileage": round(mile * night_f, 2),
        "slow_fee_before": round(slow_before, 2),
        "slow_fee": round(slow_final, 2),
        "slow_fee_capped": capped,
        "slow_fee_cap": cap,
        "total": total,
    }
