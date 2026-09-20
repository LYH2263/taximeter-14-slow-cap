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

def test_slow_fee_capped():
    r = calc_fare(5, 2, False, T, 1.0)
    assert r["slow_fee_before_cap"] == 1.6
    assert r["slow_fee"] == 1.0
    assert r["slow_fee_truncated"] is True
    assert r["slow_fee_cap"] == 1.0
    assert r["total"] == 17.0

def test_slow_fee_under_cap():
    r = calc_fare(5, 2, False, T, 20.0)
    assert r["slow_fee"] == 1.6
    assert r["slow_fee_truncated"] is False
    assert r["total"] == 17.6

def test_slow_fee_equal_to_cap_not_truncated():
    r = calc_fare(5, 2, False, T, 1.6)
    assert r["slow_fee"] == 1.6
    assert r["slow_fee_truncated"] is False

def test_zero_slow_fee_not_truncated():
    r = calc_fare(5, 0, False, T, 0.5)
    assert r["slow_fee_before_cap"] == 0.0
    assert r["slow_fee"] == 0.0
    assert r["slow_fee_truncated"] is False
    assert r["total"] == 16.0

def test_night_slow_fee_factored_then_capped():
    r = calc_fare(18, 12, True, T, 10.0)
    assert r["slow_fee_before_cap"] == 11.52
    assert r["slow_fee"] == 10.0
    assert r["slow_fee_truncated"] is True
    assert r["total"] == 68.2

def test_compare_exposes_truncation_on_both_sides():
    c = compare_day_night(18, 12, T, 10.0)
    assert c["slow_fee_cap"] == 10.0
    assert c["day_slow_fee_truncated"] is False
    assert c["night_slow_fee_truncated"] is True
    assert c["day"]["slow_fee"] == 9.6
    assert c["night"]["slow_fee_before_cap"] == 11.52
    assert c["night"]["slow_fee"] == 10.0
    assert c["day_total"] == 58.1
    assert c["night_total"] == 68.2
    assert c["delta"] == 10.1
