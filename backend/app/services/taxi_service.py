from app.config import DEFAULT_SLOW_FEE_CAP
from app.db import connect
from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare
from app.repositories import runs, settings, tariff, trips

SLOW_FEE_CAP_KEY = settings.SLOW_FEE_CAP_KEY


class TaxiService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_trips(self): return trips.list_all(self._c)
    def trip(self, tid): return trips.get(self._c, tid)
    def tariff(self): return tariff.get_active(self._c)
    def settings(self): return settings.get_map(self._c)

    def settings_normalized(self):
        m = settings.get_map(self._c)
        return {
            "currency": m.get("currency", "CNY"),
            SLOW_FEE_CAP_KEY: settings.get_float(self._c, SLOW_FEE_CAP_KEY, DEFAULT_SLOW_FEE_CAP),
        }

    # 每次计价实时读取上限：改上限当场生效；保存失败（未提交）时仍读到旧值
    def _slow_cap(self):
        return settings.get_float(self._c, SLOW_FEE_CAP_KEY, DEFAULT_SLOW_FEE_CAP)

    def save_settings_slow_cap(self, value):
        settings.upsert(self._c, SLOW_FEE_CAP_KEY, float(value))
        return self.settings_normalized()

    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def history_run(self, rid): return runs.get(self._c, rid)

    def trip_with_fare(self, tid):
        row = trips.get(self._c, tid)
        if row is None:
            return None
        snap = runs.latest_by_trip(self._c, tid, "fare")
        row["fare"] = snap["result"] if snap else None
        row["fare_run_id"] = snap["id"] if snap else None
        return row

    def fare(self, distance_km, slow_min, night, trip_id, persist):
        t = tariff.get_active(self._c)
        cap = self._slow_cap()
        r = calc_fare(distance_km, slow_min, night, t, cap)
        rid = runs.insert(self._c, "fare", {"distance_km": distance_km, "slow_min": slow_min, "night": night}, r, trip_id) if persist else None
        return {"run_id": rid, **r}

    def compare(self, distance_km, slow_min, persist):
        t = tariff.get_active(self._c)
        cap = self._slow_cap()
        r = compare_day_night(distance_km, slow_min, t, cap)
        rid = runs.insert(self._c, "compare", {"distance_km": distance_km, "slow_min": slow_min}, r, None) if persist else None
        return {"run_id": rid, **r}

    def dashboard(self):
        items = trips.list_all(self._c)
        clean = [x for x in items if "种子" not in x["label"]]
        dirty = [x for x in items if "种子" in x["label"]]
        return {"trip_count": len(items), "clean": len(clean), "dirty": len(dirty)}
