"""Standalone magnitudes for the claim (run 2026-10-24-0604 PREREG.md L1.3). Run from the claim/ folder:

    python -I code/mag_check.py fetch      # event windows [origin - 30 s, + 60 s] for the 6 calibration and 10 co-located
                                           # ComCat events (honest EarthScope GETs, logged, cached in data/evwin/)
    python -I code/mag_check.py compute    # WA ML of the event, calibration offset, M_coloc, M_cons, per-station table

Rules (run 12 PREREG.md L2.5 with PREREG.v5): response removed to displacement (pre-filter 0.5/1/25/40 Hz),
Wood-Anderson simulated (poles -6.283+/-4.7124i, zeros 0,0, gain 2080); A = mean over the live (non-constant) horizontals
of the peak |amplitude| (mm) in [P - 0.5 s, S + 4 s]; station ML = log10 A + 1.11 log10(r/100) + 0.00189 (r - 100) + 3.0
(Hutton and Boore 1987); event ML = median over stations. P and S times: the event's picks (picks.csv) where present,
else predicted (Vp 6.0, Vs 3.46 km/s from the hypocentre); ComCat events use predicted times from their ComCat
hypocentre. Calibration offset = median (ComCat ml - WA ML) over the 6 validation events (data/mc_gate.json).
M_coloc = median over the 10 nearest same-UTC-day ComCat ml events within 5 km of the epicentre of
(M_i + median over common stations of log10(A_event / A_i)). M_rel from event.json. M_cons = min(M_rel, WA ML calibrated,
M_coloc). Noise comparison: the same WA measurement on an equal-length window ending 1 s before P."""
import os, sys, csv, json, math, glob, time, hashlib, urllib.request, urllib.error, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, "..")); DD = os.path.join(CL, "data"); EW = os.path.join(DD, "evwin")
U = dt.timezone.utc; VP, VS = 6.0, 3.46; UA = "V3R1T4S-research (+https://github.com/elder-plinius/V3R1T4S)"
WA = {"poles": [-6.283 + 4.7124j, -6.283 - 4.7124j], "zeros": [0j, 0j], "gain": 2080.0, "sensitivity": 1.0}
STA = ["NN.YER", "NN.PNT", "NN.BFC", "NN.WASH", "NN.REDF", "NN.BMHS", "NN.CMK6", "NN.KVN"]
EV = json.load(open(os.path.join(CL, "event.json"))); SX = {k: tuple(v) for k, v in EV["station_coordinates"].items()}
def km(a, b, c, d):
    p = math.radians; h = math.sin(p(c - a) / 2) ** 2 + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2; return 12742 * math.asin(math.sqrt(min(1.0, h)))
def ts(s): return dt.datetime.strptime(s[:23].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=U).timestamp()
CAT = {r["id"]: r for r in csv.DictReader(open(os.path.join(DD, "window_50km_alltypes.csv")))}
O = ts(EV["origin_time_utc"]); LA, LO, DE = EV["latitude"], EV["longitude"], EV["depth_km"]
CALIB = [v["id"] for v in json.load(open(os.path.join(DD, "mc_gate.json")))["validation"]]
day = dt.datetime.fromtimestamp(O, U).date()
COLOC = [r["id"] for r in sorted([r for r in CAT.values() if dt.datetime.fromtimestamp(ts(r["time"]), U).date() == day and r["magType"] == "ml" and km(LA, LO, float(r["latitude"]), float(r["longitude"])) <= 5],
                                  key=lambda r: km(LA, LO, float(r["latitude"]), float(r["longitude"])))[:10]]
def url(sta, t0):
    net, s = sta.split("."); a = dt.datetime.fromtimestamp(math.floor(t0 - 30), U).strftime("%Y-%m-%dT%H:%M:%S"); b = dt.datetime.fromtimestamp(math.floor(t0 - 30) + 90, U).strftime("%Y-%m-%dT%H:%M:%S")
    return "https://service.earthscope.org/fdsnws/dataselect/1/query?net=%s&sta=%s&loc=--&cha=HH?&starttime=%s&endtime=%s&nodata=404" % (net, s, a, b)
def fetch():
    os.makedirs(EW, exist_ok=True); log = os.path.join(EW, "_fetchlog.jsonl")
    for eid in CALIB + COLOC:
        t = ts(CAT[eid]["time"])
        for s in STA:
            fn = os.path.join(EW, "%s_%s.mseed" % (eid, s))
            if os.path.exists(fn) or os.path.exists(fn + ".nodata"): continue
            u = url(s, t)
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=300) as q: st, b = q.status, q.read()
            except urllib.error.HTTPError as x: st, b = x.code, b""
            except Exception as x: st, b = "ERR " + type(x).__name__, b""
            open(log, "a").write(json.dumps({"url": u, "fetch_time": dt.datetime.now(U).strftime("%Y-%m-%dT%H:%M:%SZ"), "http_status": st, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest() if b else None}) + "\n")
            if st in (401, 403, 429, 503): sys.exit("STOP: HTTP %s on %s (do not retry)" % (st, u))
            if st == 200 and b: open(fn, "wb").write(b)
            else: open(fn + ".nodata", "w").write(str(st))
            time.sleep(0.25)
    print("fetched windows for", len(CALIB), "calibration and", len(COLOC), "co-located events")
INV = {}
def inv(s):
    from obspy import read_inventory
    if s not in INV: INV[s] = read_inventory(os.path.join(DD, "resp_%s.xml" % s))
    return INV[s]
def window_file(eid, s):
    if eid == "EVENT": return glob.glob(os.path.join(DD, "cand_*_%s.mseed" % s))[0]
    fn = os.path.join(EW, "%s_%s.mseed" % (eid, s)); return fn if os.path.exists(fn) else None
def wa_amp(eid, s, a, b):
    import obspy
    fn = window_file(eid, s)
    if not fn: return None
    st = obspy.read(fn); st.merge(fill_value=0); h = [tr for tr in st if tr.stats.channel[-1] in "NE" and float(np.std(tr.data.astype(float))) > 0]
    if not h: return None
    amps = []
    for tr in h:
        tr = tr.copy(); tr.detrend("demean"); tr.taper(0.05); tr.remove_response(inventory=inv(s), output="DISP", pre_filt=(0.5, 1, 25, 40))
        tr.simulate(paz_simulate=WA, simulate_sensitivity=False); w = tr.slice(obspy.UTCDateTime(a), obspy.UTCDateTime(b)).data
        if not len(w): return None
        amps.append(float(np.max(np.abs(w))) * 1000.0)
    return float(np.mean(amps))
def hb(A, r): return math.log10(A) + 1.11 * math.log10(r / 100) + 0.00189 * (r - 100) + 3.0
def amps(eid, t, la, lo, de, picks=None):
    out = {}
    for s in STA:
        r = math.hypot(km(la, lo, SX[s][0], SX[s][1]), de + SX[s][2] / 1000); tp = (picks or {}).get((s, "P"), t + r / VP); tsx = (picks or {}).get((s, "S"), t + r / VS)
        A = wa_amp(eid, s, tp - 0.5, tsx + 4)
        if A and A > 0: out[s] = (A, r, tp, tsx)
    return out
def compute():
    pk = {(r["station"], r["phase"]): ts(r["time_utc"]) for r in csv.DictReader(open(os.path.join(CL, "picks.csv")))}
    ae = amps("EVENT", O, LA, LO, DE, pk); ml = {s: hb(A, r) for s, (A, r, _, _) in ae.items()}; wa = float(np.median(list(ml.values())))
    cal = []
    for eid in CALIB:
        r = CAT[eid]; a = amps(eid, ts(r["time"]), float(r["latitude"]), float(r["longitude"]), float(r["depth"]))
        m = float(np.median([hb(A, rr) for A, rr, _, _ in a.values()])) if a else None; cal.append({"id": eid, "comcat_ml": float(r["mag"]), "wa_ml": round(m, 3) if m is not None else None, "n_sta": len(a)})
    off = float(np.median([c["comcat_ml"] - c["wa_ml"] for c in cal if c["wa_ml"] is not None]))
    co = []
    for eid in COLOC:
        r = CAT[eid]; a = amps(eid, ts(r["time"]), float(r["latitude"]), float(r["longitude"]), float(r["depth"])); com = [s for s in ae if s in a]
        if com: co.append({"id": eid, "comcat_ml": float(r["mag"]), "n_common": len(com), "M": round(float(r["mag"]) + float(np.median([math.log10(ae[s][0] / a[s][0]) for s in com])), 3)})
    mco = float(np.median([c["M"] for c in co])); mrel = EV["magnitude"]["M_rel"]; mcons = min(mrel, wa + off, mco)
    noise = {}
    for s, (A, r, tp, tsx) in ae.items():
        Ln = tsx + 4 - (tp - 0.5); An = wa_amp("EVENT", s, tp - 1 - Ln, tp - 1)
        if An: noise[s] = {"ML": round(ml[s], 3), "noise_ML": round(hb(An, r), 3), "amp_ratio": round(A / An, 2), "r_km": round(r, 2)}
    sel2 = [noise[s]["ML"] for s in noise if noise[s]["amp_ratio"] >= 2]
    print("EVENT WA ML (median of %d stations): %.3f; calibrated %.3f (offset %.3f over %d events)" % (len(ml), wa, wa + off, off, len(cal)))
    for c in cal: print("  calibration", c)
    print("M_coloc %.3f over %d events:" % (mco, len(co)), [(c["id"], c["comcat_ml"], c["M"]) for c in co])
    print("M_rel %.2f | M_cons = min(M_rel, WA cal, M_coloc) = %.3f" % (mrel, mcons))
    for s in sorted(noise, key=lambda s: noise[s]["r_km"]): print("  %-8s r %6.2f km  ML %.3f  noise ML %.3f  event/noise amplitude %.2f" % (s, noise[s]["r_km"], noise[s]["ML"], noise[s]["noise_ML"], noise[s]["amp_ratio"]))
    print("stations with event/noise >= 2: %d, median ML %.3f, calibrated %.3f" % (len(sel2), float(np.median(sel2)), float(np.median(sel2)) + off))
    json.dump({"wa_ml": wa, "offset": off, "wa_ml_cal": wa + off, "calibration": cal, "coloc": co, "M_coloc": mco, "M_rel": mrel, "M_cons": mcons, "per_station": noise,
               "snr2_median": float(np.median(sel2)), "coloc_ids": COLOC, "calib_ids": CALIB}, open(os.environ.get("MAGOUT", "mag_check_out.json"), "w"), indent=1)
if __name__ == "__main__":
    {"fetch": fetch, "compute": compute}[sys.argv[1]]()
