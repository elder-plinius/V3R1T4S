"""Standalone checker for the p1 claim of seismic-missed-events-vs-comcat (Python 3 standard library only).
Run from the package folder: python3 verify-it-yourself/verify.py   (add --live to refetch the absence queries once).

Checks, written from the criterion, against the files in object/ and the-record-we-beat/:
 0. object/ files match SHA256SUMS.
 1. picks.csv: >= 8 P/S picks on >= 4 stations; station coordinates equal event.json.
 2. Relocation from the picks alone: grid search, homogeneous Vp 6.0 / Vs 3.46 km/s, station elevations, lat/lon
    +/- 0.5 deg in 0.01 deg around 39.1535 N 119.0559 W, depth 0-20 km in 0.5 km, origin = mean residual. The best node,
    origin, RMS, residuals and horizontal error (largest distance to a node with RMS <= best + 0.1 s) must equal
    event.json, and meet RMS <= 0.3 s and horizontal error <= 5 km.
 3. Magnitudes from event.json's per-station and per-event values: medians and minimum as stated.
 4. Mc (maximum curvature + 0.2) from the binned live ComCat queries (object/mc_histograms.csv); every magnitude estimate
    must be >= the largest Mc - 0.3 (p1), and the main win (>= largest Mc) is reported, not required.
 5. Null: 600 whole-day controls (object/null_per_control_max.csv), stations shifted by distinct whole minutes in
    [10, 1430] and >= 10 min apart; none reaches the event's NCC; expected false count = count x 3.0 / 600 < 0.05.
 6. Early-hours sensitivity (object/early_per_control_max.csv): 3000 controls, the stated shift design, the stated count
    and expected false count.
 7. Region NN authoritative; absence: ComCat 0 rows and ISC 204 in the-record-we-beat/record.json (or live with --live).
Last line: PASS or FAIL."""
import csv, hashlib, json, math, os, statistics, sys, datetime as dt

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OBJ = os.path.join(ROOT, "object")
fails = []


def check(ok, what):
    print(("ok    " if ok else "FAIL  ") + what)
    if not ok:
        fails.append(what)


def near(a, b, tol):
    return abs(a - b) <= tol


# 0. integrity
sums = {}
for line in open(os.path.join(ROOT, "SHA256SUMS")):
    h, p = line.strip().split(None, 1)
    sums[p.lstrip("*").lstrip("./")] = h
for f in sorted(os.listdir(OBJ)):
    h = hashlib.sha256(open(os.path.join(OBJ, f), "rb").read()).hexdigest()
    check(sums.get("object/" + f) == h, "object/%s matches SHA256SUMS" % f)

E = json.load(open(os.path.join(OBJ, "event.json")))

# 1. picks
picks = list(csv.DictReader(open(os.path.join(OBJ, "picks.csv"))))
stations = sorted({p["station"] for p in picks})
check(len(picks) >= 8 and all(p["phase"] in ("P", "S") for p in picks), "%d P/S picks (>= 8)" % len(picks))
check(len(stations) >= 4, "%d stations (>= 4)" % len(stations))
check(len(picks) == E["n_picks"] and len(stations) == E["n_stations"], "pick and station counts equal event.json")
for p in picks:
    c = E["station_coordinates"][p["station"]]
    check([float(p["sta_lat"]), float(p["sta_lon"]), float(p["sta_elev_m"])] == c, "coordinates of %s %s equal event.json" % (p["station"], p["phase"]))


# 2. relocation
def km(a, b, c, d):
    r = math.radians
    h = math.sin(r(c - a) / 2) ** 2 + math.cos(r(a)) * math.cos(r(c)) * math.sin(r(d - b) / 2) ** 2
    return 12742 * math.asin(math.sqrt(min(1.0, h)))


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=dt.timezone.utc).timestamp()


obs = [(ts(p["time_utc"]), 6.0 if p["phase"] == "P" else 3.46, float(p["sta_lat"]), float(p["sta_lon"]), float(p["sta_elev_m"]) / 1000) for p in picks]
LA = [round(39.1535 + i * 0.01, 4) for i in range(-50, 51)]
LO = [round(-119.0559 + i * 0.01, 4) for i in range(-50, 51)]
Z = [k * 0.5 for k in range(41)]
grid = []
for la in LA:
    for lo in LO:
        hd = [km(la, lo, o[2], o[3]) for o in obs]
        for z in Z:
            res = [o[0] - math.sqrt(h * h + (z + o[4]) ** 2) / o[1] for o, h in zip(obs, hd)]
            m = sum(res) / len(res)
            grid.append((math.sqrt(sum((x - m) ** 2 for x in res) / len(res)), la, lo, z, m, res))
best = min(grid, key=lambda g: g[0])
rms, la, lo, z, ot, res = best
herr = max(km(la, lo, g[1], g[2]) for g in grid if g[0] <= rms + 0.1)
nn = sum(1 for g in grid if g[0] <= rms + 0.1)
otime = dt.datetime.fromtimestamp(ot, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]
print("      relocation: %.4f N %.4f W %.1f km, origin %s, RMS %.4f s, horizontal error %.3f km (%d nodes)" % (la, -lo, z, otime, rms, herr, nn))
check(near(la, E["latitude"], 1e-6) and near(lo, E["longitude"], 1e-6) and near(z, E["depth_km"], 1e-6), "best node equals event.json")
check(otime == E["origin_time_utc"], "origin time equals event.json")
check(near(rms, E["rms_s"], 5e-5), "RMS equals event.json (%.4f)" % E["rms_s"])
check(near(herr, E["horizontal_error_km"], 5e-4), "horizontal error equals event.json (%.3f)" % E["horizontal_error_km"])
for p, r in zip(picks, res):
    key = "%s_%s" % (p["station"], p["phase"])
    check(near(r - ot, E["residuals_s"][key], 5e-4), "residual %s equals event.json" % key)
check(rms <= 0.3 and herr <= 5.0, "location bars: RMS <= 0.3 s and horizontal error <= 5 km")

# 3. magnitudes
M = E["magnitude"]
st = M["wa_station_ml_and_noise_sensitivity"]
wa = statistics.median(v["ML"] for v in st.values())
off = statistics.median(c["comcat_ml"] - c["wa_ml"] for c in M["calibration_events"])
snr2 = statistics.median(v["ML"] for v in st.values() if v["amp_ratio"] >= 2)
coloc = statistics.median(c["M"] for c in M["coloc_events"])
check(len(st) == 8 and near(wa, M["wa_ml_uncalibrated"], 5e-4), "WA ML median of 8 stations %.3f" % wa)
check(len(M["calibration_events"]) == 6 and near(off, M["calibration_offset"], 5e-4), "calibration offset %.4f over 6 events" % off)
check(near(wa + off, M["wa_ml_calibrated"], 1e-3), "calibrated WA ML %.4f (stored values rounded to 3 decimals)" % (wa + off))
check(near(snr2, M["wa_snr2_station_median"], 5e-4), "median ML over event/noise >= 2 stations %.4f" % snr2)
check(len(M["coloc_events"]) == 10 and near(coloc, M["M_coloc"], 5e-4), "M_coloc %.3f over 10 events" % coloc)
check(near(min(M["M_rel"], wa + off, coloc), M["M_cons"], 1e-3), "M_cons = min(M_rel, calibrated, M_coloc) = %.3f" % M["M_cons"])
low = min(wa, wa + off, snr2, coloc, M["M_cons"])

# 4. Mc
H = {}
for r in csv.DictReader(open(os.path.join(OBJ, "mc_histograms.csv"))):
    H.setdefault((r["query"], r["binning"]), {})[float(r["bin"])] = int(r["count"])
mcs = {}
for (q, how), h in sorted(H.items()):
    pk = max(h, key=lambda k: (h[k], -k))
    mcs[(q, how)] = round(pk + 0.2, 1)
mc_max = max(mcs.values())
print("      Mc over %d query/binning cells: %.1f-%.1f; largest %.1f" % (len(mcs), min(mcs.values()), mc_max, mc_max))
check(len(mcs) == 24, "24 Mc cells (12 live ComCat queries x floor/round binning)")
check(low >= round(mc_max - 0.3, 1) - 1e-9, "p1: smallest magnitude estimate %.3f >= largest Mc - 0.3 = %.1f" % (low, mc_max - 0.3))
print("      main win (M >= Mc %.1f): %s (not claimed)" % (mc_max, "met" if low >= mc_max else "not met"))

# 5. null
ncc = E["detection"]["ncc"]
rows = list(csv.DictReader(open(os.path.join(OBJ, "null_per_control_max.csv"))))
check(len(rows) == 600 and sum(r["set"] == "null" for r in rows) == 400 and sum(r["set"] == "null_d9" for r in rows) == 200, "600 controls (400 on 12-10..12, 200 on 12-09)")
good = True
for r in rows:
    sh = [int(x.split(":")[1]) for x in r["shifts_samples_20Hz"].split(";")]
    pts = [0] + sh
    good &= len(sh) == 7 and all(s % 1200 == 0 and 12000 <= s <= 1716000 for s in sh)
    good &= all(min(abs(a - b), 1728000 - abs(a - b)) >= 12000 for i, a in enumerate(pts) for b in pts[i + 1:])
check(good, "every control: 7 stations shifted by whole minutes in [10, 1430], all >= 10 min apart")
n = sum(float(r["max_ncc"]) >= ncc for r in rows)
efc = n * 3.0 / 600
check(n == E["null"]["count_ge_event"] == 0, "controls >= event NCC %.4f: %d" % (ncc, n))
check(near(max(float(r["max_ncc"]) for r in rows), E["null"]["best_control"], 5e-5), "best control %.4f" % E["null"]["best_control"])
check(efc < 0.05 and near(efc, E["null"]["expected_false_count_3day_span"], 1e-9), "expected false count %.4f < 0.05" % efc)

# 6. early-hours sensitivity
X = E["null"]["early_hours_sensitivity"]
rows = list(csv.DictReader(open(os.path.join(OBJ, "early_per_control_max.csv"))))
good = len({r["control"] for r in rows}) == 3000
for r in rows:
    sh = [int(x.split(":")[1]) for x in r["shifts_samples_20Hz"].split(";")]
    pts = [0] + sh
    good &= len(sh) == 7 and all(12000 <= s <= 132000 for s in sh)
    good &= all(min(abs(a - b), 144000 - abs(a - b)) >= 12000 for i, a in enumerate(pts) for b in pts[i + 1:])
check(good, "3000 early-hours controls with the stated shift design")
n = sum(float(r["max_ncc"]) >= X["event_E2"] for r in rows)
check(n == X["count_ge_event"] and near(n / 3000 * 36, X["efc_early"], 1e-9), "early-hours: %d control(s) >= %.4f, EFC %.4f" % (n, X["event_E2"], n / 3000 * 36))

# 7. region and absence
check(E["checks"]["geoserve_authoritative"] == ["NN"], "authoritative region NN")
R = {r["name"]: r for r in json.load(open(os.path.join(ROOT, "the-record-we-beat", "record.json")))}
if "--live" in sys.argv:
    import urllib.request, urllib.error
    for k in ("absence_comcat", "absence_isc"):
        try:
            q = urllib.request.urlopen(urllib.request.Request(R[k]["url"], headers={"User-Agent": "V3R1T4S-verify"}), timeout=60)
            b, s = q.read(), q.status
        except urllib.error.HTTPError as e:
            b, s = e.read(), e.code
        R[k] = dict(R[k], http_status=s, rows=(b.decode(errors="replace").count("\n") - 1) if k == "absence_comcat" else None)
        print("      live %s: HTTP %d, %d bytes" % (k, s, len(b)))
check(R["absence_comcat"]["http_status"] == 200 and R["absence_comcat"]["rows"] == 0, "ComCat +/-30 s, 50 km: 0 events")
check(R["absence_isc"]["http_status"] == 204, "ISC +/-30 s, 0.45 deg: no event (HTTP 204)")

print("VERIFIED p1: event %s, RMS %.4f s, herr %.3f km, M >= %.3f vs Mc - 0.3 = %.1f, EFC %.4f" % (E["origin_time_utc"], rms, herr, low, mc_max - 0.3, efc) if not fails else "%d check(s) failed" % len(fails))
print("PASS" if not fails else "FAIL")
sys.exit(0 if not fails else 1)
