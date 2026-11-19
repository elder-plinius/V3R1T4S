"""settled-already checks on sweep survivors. usage: survivors.py candidates.json [mode main|p1]
1. Live NCEI events re-query for the candidate's year: every event (any validity, any cause) within +/-2 days, with distance.
2. p1 mode: live runups for the NCEI event, nearest runup row to each claimed gauge.
3. Weather: Open-Meteo ERA5 archive (open, no key) hourly surface pressure and 10 m wind at each claimed gauge,
   t0-1 d .. t0+1 d: max wind, max |dP/dt| (hPa/h); a storm (wind > 15 m/s or |dP/dt| > 2 hPa/h) is flagged."""
import datetime as dt
import json
import sys

import numpy as np

import tsu

cands = json.load(open(sys.argv[1]))
mode = sys.argv[2] if len(sys.argv) > 2 else "main"
for ev in cands:
    t0 = ev["t0"]
    day = dt.datetime.fromtimestamp(t0, dt.timezone.utc)
    print("\n=== CANDIDATE", ev["id"], ev["time"], ev.get("mag"), ev.get("place"), "claimed", ev["claimed"])
    items, page = [], 1
    while True:
        b = tsu.fetch("https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events?minYear=%d&maxYear=%d&page=%d"
                      % (day.year - (1 if day.month == 1 else 0), day.year + (1 if day.month == 12 else 0), page), "ncei_live", cache=False)
        d = json.loads(b); items += d["items"]
        if page >= d.get("totalPages", 1):
            break
        page += 1
    near = []
    for e in items:
        if not (e.get("year") and e.get("month") and e.get("day")):
            continue
        te = dt.datetime(e["year"], e["month"], e["day"], tzinfo=dt.timezone.utc).timestamp() + 43200
        if abs(te - t0) <= 2.5 * 86400:
            km = None if e.get("latitude") is None else float(tsu.gc_dist(ev["lat"], ev["lon"], e["latitude"], e["longitude"])) / 1000
            near.append((e["id"], e["year"], e["month"], e["day"], e.get("hour"), e.get("eventValidity"), e.get("causeCode"),
                         e.get("country"), e.get("locationName"), None if km is None else round(km)))
    print("NCEI live events within +/-2 d (id, y, m, d, h, validity, cause, country, location, km):", near or "none")
    if mode == "p1" and ev.get("ncei_id"):
        items, page = [], 1
        while True:
            b = tsu.fetch("https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId=%d&page=%d"
                          % (ev["ncei_id"], page), "ncei_runups_live", cache=False)
            d = json.loads(b); items += d["items"]
            if page >= d.get("totalPages", 1):
                break
            page += 1
        print("NCEI live runup rows for event", ev["ncei_id"], ":", len(items))
    for g in ev["gauges"]:
        if g["code"] not in ev["claimed"]:
            continue
        line = "  gauge %s %.1f km lat %.3f lon %.3f eta %.1f min onset %.1f min dt_arr %+.1f R %.2f peak %.3f m rms24 %.4f" % (
            g["code"], g["km"], g["lat"], g["lon"], g["eta_min"], g["full"]["onset"] / 60, g["full"]["dt_arr"],
            g["full"]["R"], g["full"]["peak"], g["full"]["rms24"])
        if mode == "p1" and ev.get("ncei_id"):
            rr = [r for r in items if r.get("latitude") is not None]
            if rr:
                dd = tsu.gc_dist(g["lat"], g["lon"], np.array([r["latitude"] for r in rr]), np.array([r["longitude"] for r in rr]))
                k = int(np.argmin(dd))
                line += " | nearest NCEI row %s %.1f km" % (rr[k].get("locationName"), dd[k] / 1000)
        print(line)
        print("    controls:", [(c["d"], c.get("R"), c.get("detect")) for c in g.get("controls", [])])
        a = (day - dt.timedelta(days=1)).strftime("%Y-%m-%d"); z = (day + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            w = json.loads(tsu.fetch("https://archive-api.open-meteo.com/v1/archive?latitude=%.3f&longitude=%.3f&start_date=%s&end_date=%s"
                                     "&hourly=surface_pressure,wind_speed_10m&wind_speed_unit=ms&timezone=GMT" % (g["lat"], g["lon"], a, z), "meteo"))
            p = np.array([x if x is not None else np.nan for x in w["hourly"]["surface_pressure"]], float)
            ws = np.array([x if x is not None else np.nan for x in w["hourly"]["wind_speed_10m"]], float)
            dp = np.nanmax(np.abs(np.diff(p)))
            print("    weather (ERA5, t0 +/- 1 d): max wind %.1f m/s, max |dP/dt| %.2f hPa/h, storm flag %s" % (
                np.nanmax(ws), dp, bool(np.nanmax(ws) > 15 or dp > 2)))
        except Exception as e:
            print("    weather: fetch failed", repr(e))
