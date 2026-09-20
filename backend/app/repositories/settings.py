import sqlite3

DEFAULT_SLOW_FEE_CAP = 20.0

def get_map(conn): return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}

def get_slow_fee_cap(conn: sqlite3.Connection) -> float:
    row = conn.execute("SELECT value FROM settings WHERE key='slow_fee_cap'").fetchone()
    if not row:
        return DEFAULT_SLOW_FEE_CAP
    try:
        value = float(row["value"])
    except (TypeError, ValueError):
        return DEFAULT_SLOW_FEE_CAP
    return value if value > 0 else DEFAULT_SLOW_FEE_CAP

def set_slow_fee_cap(conn: sqlite3.Connection, value: float) -> None:
    conn.execute(
        "INSERT INTO settings(key,value) VALUES('slow_fee_cap',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (repr(float(value)),),
    )
    conn.commit()
