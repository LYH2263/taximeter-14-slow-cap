import sqlite3

SLOW_FEE_CAP_KEY = "slow_fee_cap"


def get_map(conn):
    return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}


def get_float(conn, key, default):
    """读取数值设置；缺失、非法或非正数一律回退 default。"""
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    if row is None:
        return default
    try:
        v = float(row["value"])
    except (TypeError, ValueError):
        return default
    return v if v > 0 else default


def upsert(conn, key, value):
    conn.execute(
        "INSERT INTO settings(key,value) VALUES(?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, str(value)),
    )
    conn.commit()
