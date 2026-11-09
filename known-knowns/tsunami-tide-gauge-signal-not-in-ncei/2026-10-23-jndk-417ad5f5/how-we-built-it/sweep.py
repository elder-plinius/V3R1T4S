"""Stages 1-3 of PREREG.md.  usage: sweep.py main|p1 [limit]
main: ComCat M>=6.0 depth<=70 km 2015-01-01..2026-10-22 not matched to NCEI (+/-1 d, 3000 km, any validity).
p1:   NCEI earthquake events since 2024-01-01; IOC stations within 1500 km without a runup row within 20 km.
Writes $JOB_OUT/results.jsonl (one line per event) and candidates.json."""
import datetime as dt
import json
import os
import sys
import traceback

import numpy as np

import tsu

MODE = sys.argv[1]
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
SHARD = int(sys.argv[3]) if len(sys.argv) > 3 else 0
NSHARD = int(sys.argv[4]) if len(sys.argv) > 4 else 1
OUT = os.environ.get("JOB_OUT", ".")
CTRL_DAYS = [-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7]

st = tsu.ioc_stationlist()
seen, stations = set(), []
for s in st:
    if s["Code"] in seen or s.get("Lat") is None or s.get("Lon") is None:
        continue
    seen.add(s["Code"])
    stations.append(s)
SLAT = np.array([s["Lat"] for s in stations]); SLON = np.array([s["Lon"] for s in stations])
print("stations", len(stations), flush=True)

ncei = tsu.ncei_events(2014)
print("ncei events since 2014", len(ncei), flush=True)


def utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


def gauge_prep(code, t0):
    rows = tsu.ioc_data(code, utc(t0 - 36 * 3600), utc(t0 + 12 * 3600))
    return tsu.prepare_gauge(rows, t0)


def process(ev, maxkm, nmax, exclude_fn=None):
    t0, lat, lon = ev["t0"], ev["lat"], ev["lon"]
    d = tsu.gc_dist(lat, lon, SLAT, SLON)
    order = [i for i in np.argsort(d) if d[i] <= maxkm * 1000]
    cand = []
    for i in order:
        s = stations[i]
        if exclude_fn and exclude_fn(s):
            continue
        cand.append((float(d[i]) / 1000, s))
        if len(cand) >= nmax:
            break
    ev["n_stations"] = len(cand)
    gauges = []
    for km, s in cand:
        try:
            info = gauge_prep(s["Code"], t0)
        except Exception as e:  # network error: record, never retry
            gauges.append({"code": s["Code"], "km": km, "ok": False, "why": "fetch error %r" % e})
            continue
        g = {"code": s["Code"], "km": round(km, 1), "lat": s["Lat"], "lon": s["Lon"], "ok": info["ok"],
             "why": info.get("why")}
        if info["ok"]:
            s1 = tsu.score(info["tg"], info["bp"], t0)
            g.update(sensor=info["sensor"], screenR=round(s1["R"], 3), rms24=s1["rms24"], tpeak_min=s1["t_peak"] / 60)
        gauges.append(g)
    ev["gauges"] = gauges
    flagged = [g for g in gauges if g.get("ok") and g["screenR"] > 5]
    ev["n_usable"] = sum(1 for g in gauges if g.get("ok"))
    ev["n_flagged"] = len(flagged)
    if len(flagged) < 2:
        ev["stage"] = 1
        return ev
    # stage 2: travel times on a box around source + flagged gauges
    la = [lat] + [g["lat"] for g in flagged]; lo = [lon] + [g["lon"] for g in flagged]
    if max(lo) - min(lo) > 180:  # dateline: shift to 0..360 frame not supported by the ascii slab; skip honestly
        ev["stage"] = 2; ev["why"] = "dateline box not supported"
        return ev
    lats, lons, z = tsu.etopo_box(max(-89, min(la) - 2), min(89, max(la) + 2), max(-180, min(lo) - 2), min(180, max(lo) + 2))
    src = tsu.snap(lats, lons, z, lat, lon, 20, 50)
    if src is None:
        ev["stage"] = 2; ev["why"] = "source not offshore (no >=20 m cell within 50 km)"
        return ev
    T = tsu.travel_time_grid(lats, lons, z, src)
    det = []
    for g in flagged:
        cell = tsu.snap(lats, lons, z, g["lat"], g["lon"], 20, 30)
        if cell is None or not np.isfinite(T[cell]):
            g["eta_min"] = None
            continue
        eta = float(T[cell])
        g["eta_min"] = round(eta / 60, 2)
        info = gauge_prep(g["code"], t0)
        sc = tsu.score(info["tg"], info["bp"], t0, eta)
        g["full"] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in sc.items()}
        g["detect"] = tsu.detect(sc)
        if g["detect"]:
            det.append(g)
    ev["n_detect"] = len(det)
    if len(det) < 2:
        ev["stage"] = 2
        return ev
    # stage 3: control days
    for g in det:
        ctrl = []
        for dd in CTRL_DAYS:
            tc = t0 + dd * 86400
            try:
                info = gauge_prep(g["code"], tc)
            except Exception as e:
                ctrl.append({"d": dd, "ok": False, "why": "fetch error"})
                continue
            if not info["ok"]:
                ctrl.append({"d": dd, "ok": False, "why": info.get("why")})
                continue
            sc = tsu.score(info["tg"], info["bp"], tc, g["eta_min"] * 60)
            ctrl.append({"d": dd, "ok": True, "R": round(sc["R"], 3), "dt_arr": sc["dt_arr"], "detect": tsu.detect(sc)})
        avail = [c for c in ctrl if c["ok"]]
        g["controls"] = ctrl
        g["ctrl_pass"] = len(avail) >= 8 and not any(c["detect"] for c in avail)
    claimed = [g for g in det if g["ctrl_pass"]]
    ev["claimed"] = [g["code"] for g in claimed]
    ev["stage"] = 3
    ev["candidate"] = len(claimed) >= 2
    return ev


events = []
if MODE == "main":
    feats = tsu.comcat("2015-01-01", "2026-10-22", 6.0, 70)
    print("comcat", len(feats), flush=True)
    for f in sorted(feats, key=lambda f: -f["properties"]["time"]):
        p = f["properties"]; c = f["geometry"]["coordinates"]
        t0 = p["time"] / 1000.0
        hits = tsu.ncei_conflict(ncei, t0, c[1], c[0])
        ev = {"id": f["id"], "t0": t0, "time": utc(t0).isoformat(), "lat": c[1], "lon": c[0], "depth": c[2],
              "mag": p["mag"], "place": p["place"], "ncei_conflict": [h["id"] for h in hits]}
        events.append(ev)
    todo = [e for e in events if not e["ncei_conflict"]]
    print("not matched to NCEI", len(todo), "of", len(events), flush=True)
    maxkm, nmax, excl = 800, 8, None
elif MODE == "p1":
    for e in ncei:
        if e.get("causeCode") != 1 or e.get("latitude") is None or not (
                int(os.environ.get("P1_MINYEAR", "2024")) <= e.get("year", 0) <= int(os.environ.get("P1_MAXYEAR", "9999"))):
            continue
        t0 = tsu.ncei_event_time(e)
        if t0 is None or e.get("hour") is None:
            continue
        sec = e.get("second") or 0
        t0 = t0 + sec
        events.append({"id": "ncei%d" % e["id"], "ncei_id": e["id"], "t0": t0, "time": utc(t0).isoformat(),
                       "lat": e["latitude"], "lon": e["longitude"], "mag": e.get("eqMagnitude"),
                       "place": "%s / %s" % (e.get("country"), e.get("locationName")), "validity": e.get("eventValidity")})
    todo = sorted(events, key=lambda e: -e["t0"])
    print("ncei earthquake events since 2024", len(todo), flush=True)
    maxkm, nmax = 1500, 40
else:
    raise SystemExit("mode?")

n = 0
with open(os.path.join(OUT, "results.jsonl"), "w") as fo:
    for ev in todo[:LIMIT][SHARD::NSHARD]:
        excl = None
        if MODE == "p1":
            items, page = [], 1
            while True:
                b = tsu.fetch("https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId=%d&page=%d"
                              % (ev["ncei_id"], page), "ncei_runups", cache=False)
                dd = json.loads(b)
                items += dd["items"]
                if page >= dd.get("totalPages", 1):
                    break
                page += 1
            rr = [r for r in items if r.get("latitude") is not None]
            ev["ncei_runup_rows"] = len(items)
            RL = np.array([r["latitude"] for r in rr]); RO = np.array([r["longitude"] for r in rr])

            def excl(s, RL=RL, RO=RO):
                return len(RL) > 0 and bool(np.any(tsu.gc_dist(s["Lat"], s["Lon"], RL, RO) <= 20e3))
        try:
            process(ev, maxkm, nmax, excl)
        except Exception:
            ev["error"] = traceback.format_exc()[-600:]
        fo.write(json.dumps(ev, default=str) + "\n"); fo.flush()
        n += 1
        print(n, ev["time"][:16], ev.get("mag"), ev.get("place"), "stations", ev.get("n_stations"), "usable",
              ev.get("n_usable"), "flag", ev.get("n_flagged"), "det", ev.get("n_detect"), "claimed", ev.get("claimed"),
              ev.get("why", ""), "ERR" if "error" in ev else "", flush=True)

res = [json.loads(l) for l in open(os.path.join(OUT, "results.jsonl"))]
cands = [e for e in res if e.get("candidate")]
json.dump(cands, open(os.path.join(OUT, "candidates.json"), "w"), indent=1, default=str)
print("SUMMARY mode", MODE, "events", len(res), "with>=2 usable", sum(1 for e in res if (e.get("n_usable") or 0) >= 2),
      "stage1 pass", sum(1 for e in res if (e.get("n_flagged") or 0) >= 2),
      "stage2 pass", sum(1 for e in res if (e.get("n_detect") or 0) >= 2), "candidates", len(cands),
      "errors", sum(1 for e in res if "error" in e))
for e in cands:
    print("CANDIDATE", e["id"], e["time"], e.get("mag"), e.get("place"), e["claimed"])
