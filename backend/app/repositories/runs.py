import json
from datetime import datetime, timezone


def _parse(row):
    d = dict(row)
    d["input"] = json.loads(d.pop("input_json"))
    d["result"] = json.loads(d.pop("result_json"))
    return d


def insert(conn, kind, payload, result, trip_id=None):
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "INSERT INTO calc_runs(kind,trip_id,input_json,result_json,created_at) VALUES (?,?,?,?,?)",
        (kind, trip_id, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False), now),
    )
    conn.commit()
    return int(cur.lastrowid)


def list_recent(conn, limit=50):
    return [dict(r) for r in conn.execute("SELECT * FROM calc_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def get(conn, run_id):
    row = conn.execute("SELECT * FROM calc_runs WHERE id=?", (run_id,)).fetchone()
    return _parse(row) if row else None


def latest_by_trip(conn, trip_id, kind="fare"):
    row = conn.execute(
        "SELECT * FROM calc_runs WHERE trip_id=? AND kind=? ORDER BY id DESC LIMIT 1",
        (trip_id, kind),
    ).fetchone()
    return _parse(row) if row else None
