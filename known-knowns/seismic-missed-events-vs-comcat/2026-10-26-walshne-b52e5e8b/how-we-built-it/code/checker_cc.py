"""Checker for the detector's per-station correlation (run 2026-10-26-1727 PREREG.md L1.3), written from the definition:
CC_s(j) = Pearson correlation of the template's 120-sample window w (20 Hz, 2-8 Hz) with the station's preprocessed
20 Hz trace x[j : j + 120], computed directly in float64 (no FFT). The detector aligns it as A_s(k) = CC_s(k + m_s),
where k is the template-origin sample and m_s the station moveout.

Usage: NULLWORK=<folder with wf20/> python -I checker_cc.py <claim folder> <f32 module path> <f64 module path>
Compares both detector versions against the direct value at: REPRODUCE's artefact point (YER, nn00888600, 23:09:29 on
2024-12-09), the event's template nn00890362 at 23:20:12.75, and 200 random points (50 inside the mainshock chunk)."""
import sys, os, json, importlib.util, datetime as dt
import numpy as np

CL, F32, F64 = sys.argv[1:4]
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
m32, m64 = load(F32, "nf32"), load(F64, "nf64")
m32.CL = m64.CL = CL
T = {t["id"]: t for t in json.load(open(os.path.join(CL, "data", "templates.json")))["templates"]}
FS, L, U = 20.0, 120, dt.timezone.utc

def direct(x, w, j):
    a = np.asarray(x[j:j + L], np.float64); b = np.asarray(w, np.float64)
    a = a - a.mean(); b = b - b.mean(); d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else 0.0

cache = {}
def station_cc(mod, day, s, tid):
    key = (mod.__name__, day, s, tid)
    if key not in cache:
        D = mod.load_day(day); P = mod.prep_station(*D[s]); cache[key] = mod.xcorr(P, T[tid]["st"][s]["w"])
    return cache[key]

def k_of(day, hms):
    t0 = dt.datetime.fromisoformat(day).replace(tzinfo=U)
    return int(round((dt.datetime.fromisoformat(day + "T" + hms).replace(tzinfo=U) - t0).total_seconds() * FS))

D9 = m64.load_day("2024-12-09")
out = []
# 1. Artefact point: search +/-1 s around 23:09:29 (aligned k), report where the float32 value peaks.
tid, s = "nn00888600", "NN.YER..HHZ"; m = T[tid]["st"][s]["m"]; k0 = k_of("2024-12-09", "23:09:29")
c32, c64 = station_cc(m32, "2024-12-09", s, tid), station_cc(m64, "2024-12-09", s, tid)
ks = range(k0 - 20, k0 + 21); kb = max(ks, key=lambda k: c32[k + m])
out.append("artefact point %s %s k=%d (%.2f s): f32 %.4f, f64 %.6f, direct %.6f" % (tid, s, kb, kb / FS, c32[kb + m], c64[kb + m], direct(D9[s][0], T[tid]["st"][s]["w"], kb + m)))
a_ok = abs(c64[kb + m] - direct(D9[s][0], T[tid]["st"][s]["w"], kb + m)) <= 1e-5
# 2. Event template at the exact aligned lag.
tid = "nn00890362"; k = k_of("2024-12-09", "23:20:12.750000"); e_ok = True; vals = []
for s in T[tid]["st"]:
    if s not in D9: continue
    m = T[tid]["st"][s]["m"]; v64 = station_cc(m64, "2024-12-09", s, tid)[k + m]; v32 = station_cc(m32, "2024-12-09", s, tid)[k + m]; vd = direct(D9[s][0], T[tid]["st"][s]["w"], k + m)
    e_ok &= abs(v64 - vd) <= 1e-5; vals.append(v64)
    out.append("event %s %s: f32 %.6f, f64 %.6f, direct %.6f" % (tid, s.split(".")[1], v32, v64, vd))
out.append("event NCC (mean of %d station CCs, f64): %.6f" % (len(vals), float(np.mean(vals))))
# 3. Random points: 150 anywhere on the 4 days, 50 inside the 12-09 chunk holding the mainshock.
rng = np.random.default_rng(20261026); ids = sorted(T); days = ["2024-12-09", "2024-12-10", "2024-12-11", "2024-12-12"]
kmain = int((m64.T_MAIN - dt.datetime(2024, 12, 9, tzinfo=U).timestamp()) * FS); c = kmain // m64.STEP
d32 = []; d64 = []; n = 0; tries = 0
while n < 200 and tries < 5000:
    tries += 1; tid = ids[rng.integers(len(ids))]; s = sorted(T[tid]["st"])[rng.integers(len(T[tid]["st"]))]
    if n < 50: day, j = "2024-12-09", int(rng.integers(c * m64.STEP, min((c + 1) * m64.STEP, m64.N - L)))
    else: day, j = days[rng.integers(4)], int(rng.integers(0, m64.N - L))
    Dd = m64.load_day(day) if day != "2024-12-09" else D9
    if s not in Dd: continue
    P = m64.prep_station(*Dd[s])
    if P[1][j] <= 0: continue  # gap or near-zero window: the detector sets CC to 0 by rule
    vd = direct(Dd[s][0], T[tid]["st"][s]["w"], j)
    d64.append(abs(m64.xcorr(P, T[tid]["st"][s]["w"])[j] - vd)); d32.append(abs(m32.xcorr(m32.prep_station(*Dd[s]), T[tid]["st"][s]["w"])[j] - vd)); n += 1
out.append("random points: %d (first 50 in the mainshock chunk %d); max |f64 - direct| %.2e; max |f32 - direct| %.2e (in-chunk max %.2e)" % (n, c, max(d64), max(d32), max(d32[:50])))
r_ok = max(d64) <= 1e-5
out.append("CHECKER: %s (artefact %s, event %s, random %s)" % ("PASS" if a_ok and e_ok and r_ok else "FAIL", a_ok, e_ok, r_ok))
print("\n".join(out))
