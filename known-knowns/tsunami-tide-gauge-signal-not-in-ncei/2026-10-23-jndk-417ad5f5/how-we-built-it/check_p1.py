"""Standalone re-check of the p1 observations for NCEI event 5942 (run on a server with numpy+scipy and internet).
usage: python3 check_p1.py RAW_DIR
Re-scores luga/lifo/lifo2 from the saved raw IOC series with the frozen tsu.py rules, recomputes travel times from
ETOPO1 (re-downloaded), re-downloads the 12 control days, and re-queries NCEI runup rows for event 5942."""
import datetime as dt, gzip, json, os, sys
import numpy as np
os.environ.setdefault("RAW_DIR", os.path.join(os.environ.get("JOB_OUT", "."), "refetch"))
import tsu
raw = sys.argv[1]
t0 = dt.datetime(2024, 12, 17, 1, 47, 26, tzinfo=dt.timezone.utc).timestamp()
lat, lon = -17.686, 168.034
G = {"luga": (-15.516, 167.189, "ioc_luga_8654b733704b737be615c9be.gz"),
     "lifo": (-20.918, 167.279, "ioc_lifo_bb8e0d555fffdce969188d09.gz"),
     "lifo2": (-20.918, 167.279, "ioc_lifo2_fef6bb5363ddadcdc1d0dc27.gz")}
lats, lons, z = tsu.etopo_box(-24, -12, 165, 171)
T = tsu.travel_time_grid(lats, lons, z, tsu.snap(lats, lons, z, lat, lon, 20, 50))
for code, (gl, go, fn) in G.items():
    eta = float(T[tsu.snap(lats, lons, z, gl, go, 20, 30)])
    info = tsu.prepare_gauge(json.loads(gzip.open(os.path.join(raw, fn)).read()), t0)
    sc = tsu.score(info["tg"], info["bp"], t0, eta)
    ctrl = []
    for d in [-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7]:
        tc = t0 + d * 86400
        i2 = tsu.prepare_gauge(tsu.ioc_data(code, dt.datetime.fromtimestamp(tc - 36 * 3600, dt.timezone.utc),
                                            dt.datetime.fromtimestamp(tc + 12 * 3600, dt.timezone.utc)), tc)
        ctrl.append(None if not i2.get("ok") else tsu.detect(tsu.score(i2["tg"], i2["bp"], tc, eta)))
    print(code, "sensor", info["sensor"], "ETA %.2f min" % (eta / 60), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in sc.items()},
          "DETECT", tsu.detect(sc), "control-day detects", ctrl)
items = json.loads(tsu.fetch("https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId=5942", "live", cache=False))["items"]
for r in items:
    d = min(float(tsu.gc_dist(r["latitude"], r["longitude"], gl, go)) / 1000 for gl, go, _ in G.values())
    print("NCEI runup row:", r.get("locationName"), r.get("typeMeasurementId"), r.get("latitude"), r.get("longitude"), "km to nearest claimed gauge %.1f" % d)
print("NCEI runup rows for 5942:", len(items))
