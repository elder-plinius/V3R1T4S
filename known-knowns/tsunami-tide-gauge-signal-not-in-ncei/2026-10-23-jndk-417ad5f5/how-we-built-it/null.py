"""Stage 4 (PREREG null test). usage: null.py candidates.json [event_id ...]
For each candidate: 400 control origin times uniform in [t0-60 d, t0+60 d], |t-t0| >= 2 d (seed 20261023),
QC failures redrawn; S = min over claimed gauges of R_g (R_g = R if |dt_arr| <= 10 min else 0).
Prints controls run, best control S, real S, and whether the real S beats every control."""
import bisect
import datetime as dt
import json
import os
import random
import sys

import numpy as np

import tsu

OUT = os.environ.get("JOB_OUT", ".")
cands = json.load(open(sys.argv[1]))
want = set(sys.argv[2:])


def utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


def rows_ts(rows):
    out = []
    for r in rows:
        try:
            t = dt.datetime.strptime(r["stime"].strip()[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp()
        except Exception:
            continue
        out.append((t, r))
    out.sort(key=lambda x: x[0])
    return [x[0] for x in out], [x[1] for x in out]


def s_at(series, gauges, tc):
    rs = []
    for g in gauges:
        ts, rows = series[g["code"]]
        a = bisect.bisect_left(ts, tc - 36 * 3600); b = bisect.bisect_right(ts, tc + 12 * 3600)
        info = tsu.prepare_gauge(rows[a:b], tc)
        if not info["ok"]:
            return None, None
        sc = tsu.score(info["tg"], info["bp"], tc, g["eta_min"] * 60)
        r = sc["R"] if sc["dt_arr"] is not None and abs(sc["dt_arr"]) <= 10 else 0.0
        rs.append(r)
    return min(rs), rs


results = []
for ev in cands:
    if want and ev["id"] not in want:
        continue
    t0 = ev["t0"]
    gauges = [g for g in ev["gauges"] if g["code"] in ev["claimed"]]
    series = {}
    for g in gauges:
        rows = tsu.ioc_data_long(g["code"], utc(t0 - 61 * 86400), utc(t0 + 61 * 86400))
        series[g["code"]] = rows_ts(rows)
    real, real_rs = s_at(series, gauges, t0)
    rng = random.Random(20261023)
    ctrl, tried = [], 0
    while len(ctrl) < 400 and tried < 4000:
        tried += 1
        off = rng.uniform(-60 * 86400, 60 * 86400)
        if abs(off) < 2 * 86400:
            continue
        s, rs = s_at(series, gauges, t0 + off)
        if s is None:
            continue
        ctrl.append({"off_days": off / 86400, "S": s, "R": rs})
    best = max(c["S"] for c in ctrl) if ctrl else None
    r = {"id": ev["id"], "time": ev["time"], "claimed": ev["claimed"], "real_S": real, "real_R": real_rs,
         "controls": len(ctrl), "draws": tried, "best_control": best,
         "n_ge_real": sum(1 for c in ctrl if real is not None and c["S"] >= real),
         "real_beats_all_controls": bool(ctrl) and real is not None and len(ctrl) >= 400 and real > best}
    results.append(r)
    json.dump(ctrl, open(os.path.join(OUT, "null_controls_%s.json" % ev["id"]), "w"))
    print("NULL", json.dumps(r), flush=True)
json.dump(results, open(os.path.join(OUT, "null_summary.json"), "w"), indent=1)
