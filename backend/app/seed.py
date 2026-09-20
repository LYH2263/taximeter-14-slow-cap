from app.config import DEFAULT_SLOW_FEE_CAP
from app.db import connect
from app.engines.tariff_breakdown import calc_fare
from app.repositories import runs
from app.repositories.settings import SLOW_FEE_CAP_KEY

TARIFF = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}

def init_db():
    conn = connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS tariff(id INTEGER PRIMARY KEY, start_price REAL, start_include_km REAL, per_km REAL, per_slow_min REAL, night_factor REAL);
    CREATE TABLE IF NOT EXISTS trips(id INTEGER PRIMARY KEY, label TEXT, distance_km REAL, slow_min REAL, night INTEGER);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE IF NOT EXISTS calc_runs(id INTEGER PRIMARY KEY, kind TEXT, trip_id INTEGER, input_json TEXT, result_json TEXT, created_at TEXT);
    """)
    # 每次启动幂等补设置缺项（老库兼容）；OR IGNORE 不覆盖用户已保存的值
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES ('currency','CNY')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES (?,?)", (SLOW_FEE_CAP_KEY, str(DEFAULT_SLOW_FEE_CAP)))
    conn.commit()
    if conn.execute("SELECT COUNT(*) c FROM tariff").fetchone()["c"] == 0:
        conn.execute("INSERT INTO tariff(start_price,start_include_km,per_km,per_slow_min,night_factor) VALUES (11,3,2.5,0.8,1.2)")
        conn.execute("INSERT INTO trips(label,distance_km,slow_min,night) VALUES ('白天短途',5.0,2,0)")
        conn.execute("INSERT INTO trips(label,distance_km,slow_min,night) VALUES ('夜间长途(种子)',18.0,12,1)")
        conn.commit()
        # 每条种子行程各写一条含当时上限与截断标记的结算快照
        runs.insert(conn, "fare", {"distance_km": 5, "slow_min": 2, "night": False},
                    calc_fare(5, 2, False, TARIFF, DEFAULT_SLOW_FEE_CAP), 1)
        runs.insert(conn, "fare", {"distance_km": 18, "slow_min": 12, "night": True},
                    calc_fare(18, 12, True, TARIFF, DEFAULT_SLOW_FEE_CAP), 2)
    conn.close()
