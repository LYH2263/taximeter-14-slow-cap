from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare

T = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}

def test_day_short():
    r = calc_fare(5, 2, False, T)
    assert r["total"] == 17.6
    assert r["mileage"] == 5.0

def test_night_long():
    r = calc_fare(18, 12, True, T)
    assert r["total"] == 69.72

def test_compare_delta():
    c = compare_day_night(18, 12, T)
    assert c["night_total"] > c["day_total"]

def test_uncapped_fields():
    r = calc_fare(5, 2, False, T, slow_cap=50)
    assert r["slow_fee"] == 1.6
    assert r["slow_fee_before"] == 1.6
    assert r["slow_fee_capped"] is False
    assert r["slow_fee_cap"] == 50.0
    assert r["total"] == 17.6

def test_day_capped_total_uses_cap():
    r = calc_fare(5, 20, False, T, slow_cap=10)
    assert r["slow_fee_before"] == 16.0
    assert r["slow_fee"] == 10.0
    assert r["slow_fee_capped"] is True
    assert r["slow_fee_cap"] == 10.0
    assert r["total"] == 26.0

def test_night_scales_before_cap():
    # 日间低速费 9.0 未触顶；夜间 9.0*1.2=10.8 先乘系数后被 10 封顶
    c = compare_day_night(5, 11.25, T, slow_cap=10)
    d, n = c["day"], c["night"]
    assert d["slow_fee_before"] == 9.0
    assert d["slow_fee"] == 9.0
    assert d["slow_fee_capped"] is False
    assert n["slow_fee_before"] == 10.8
    assert n["slow_fee"] == 10.0
    assert n["slow_fee_capped"] is True
    assert d["slow_fee_cap"] == n["slow_fee_cap"] == 10.0
    # 夜间应付按截断后的 10 元低速费计
    assert n["total"] == round(11 * 1.2 + 5 * 1.2 + 10, 2)

def test_zero_slow_fee_not_capped():
    r = calc_fare(5, 0, False, T, slow_cap=10)
    assert r["slow_fee_before"] == 0
    assert r["slow_fee"] == 0
    assert r["slow_fee_capped"] is False

def test_slow_fee_equal_cap_not_capped():
    r = calc_fare(5, 12, False, T, slow_cap=9.6)
    assert r["slow_fee"] == 9.6
    assert r["slow_fee_capped"] is False
