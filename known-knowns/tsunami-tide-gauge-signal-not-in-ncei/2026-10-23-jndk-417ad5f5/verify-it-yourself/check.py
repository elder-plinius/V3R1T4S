"""Standalone check of object/observations.csv (Python standard library only; needs internet).

Definition checked (bank target tsunami-tide-gauge-signal-not-in-ncei, per-gauge evidence standard):
  "on each gauge, a band-passed (2-120 min) signal with peak amplitude > 5x the RMS of the preceding 24 h in the
  same band; arrival times ... consistent within +/- 10 min with shallow-water travel times computed from the source".

What this script does, independently of the code that found the object:
 1. Downloads the three IOC SLSMF API v1 series (2024-12-15T13:47 .. 2024-12-17T13:47 UTC) and checks that their
    sha256 equals the hash recorded when the object was made (the data are not redistributed here).
 2. For each gauge: picks the sensor named in the object, bins it to 1-min means on a grid starting at the origin
    second minus 36 h, interpolates gaps, removes a linear trend and applies a zero-phase 4th-order Butterworth
    high-pass at 120 min (1-min sampling: the 2-120 min band), written out below without numpy/scipy.
 3. RMS24 = rms over the 24 h before the origin; onset = first minute in [ETA-30, ETA+60] min with
    |bp| >= 3 RMS24; peak = max |bp| over [onset, onset+180 min]; R = peak / RMS24.
 4. Requires, for both stations (Luganville; Lifou), R > 5 and |onset - ETA| <= 10 min for the ETA in the object,
    and agreement with the object: R within 3%, peak within 0.003 m, onset minute within 1 min.
Prints PASS or FAIL as the last line."""
import cmath
import csv
import datetime as dt
import hashlib
import json
import math
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "..", "object", "observations.csv")
BASE = "https://www.ioc-sealevelmonitoring.org/service.php?query=data&code=%s&timestart=2024-12-15T13%%3A47&timestop=2024-12-17T13%%3A47&format=json"
SHA = {"luga": "fe684f751d3224631da7880e8f1dc8cae75a83e650368edc87583d04c07bdbb9",
       "lifo": "2b4cb928fea203283f38e4707e856ee94f289606637e6c3b373a59f079f6aa57",
       "lifo2": "8a76d34530e5559a641a5e14d661d96b77f01a5fc253d14c7569f8009997009e"}
T0 = dt.datetime(2024, 12, 17, 1, 47, 26, tzinfo=dt.timezone.utc).timestamp()
SRC = (-17.686, 168.034)  # NCEI event 5942 epicentre
HDR_SHA = "ee61f6c2967ce561ebb73e2915c3e773668ce0add9a8078db9933c4d4b4bc73e"  # sha256 of the object's comment lines (provenance text)


def gc_km(a, b, c, d):
    p1, p2, dl = math.radians(a), math.radians(c), math.radians(d - b)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def station(code):
    url = "https://www.ioc-sealevelmonitoring.org/service.php?query=station&code=%s&format=json" % code
    b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "V3R1T4S verify-it-yourself"}), timeout=120).read()
    d = json.loads(b)
    d = d[0] if isinstance(d, list) else d
    return float(d["Lat"]), float(d["Lon"])


def butter_hp_sos(fc, fs=1.0, order=4):
    """Digital Butterworth high-pass as second-order sections (bilinear transform, prewarped)."""
    wc = 2 * fs * math.tan(math.pi * fc / fs)
    poles = [cmath.exp(1j * math.pi * (2 * k + order + 1) / (2 * order)) for k in range(order)]
    hp_poles = [wc / p for p in poles]  # analog high-pass poles; zeros at s = 0
    zp = [(2 * fs + p) / (2 * fs - p) for p in hp_poles]
    # gain: unity at Nyquist (z = -1)
    sos = []
    used = set()
    for i, p in enumerate(zp):
        if i in used or p.imag < 0:
            continue
        j = min((k for k in range(len(zp)) if k != i and k not in used), key=lambda k: abs(zp[k] - p.conjugate()))
        used |= {i, j}
        a1 = -(p + zp[j]).real
        a2 = (p * zp[j]).real
        sos.append([1.0, -2.0, 1.0, 1.0, a1, a2])
    for s in sos:  # normalise each section to gain 1 at z = -1
        g = (s[3] - s[4] + s[5]) / (s[0] - s[1] + s[2])
        s[0] *= g; s[1] *= g; s[2] *= g
    return sos


def sosfilt(sos, x):
    y = list(x)
    for b0, b1, b2, _, a1, a2 in sos:
        z1 = z2 = 0.0
        out = []
        for v in y:
            o = b0 * v + z1
            z1 = b1 * v - a1 * o + z2
            z2 = b2 * v - a2 * o
            out.append(o)
        y = out
    return y


def filtfilt(sos, x, pad=1500):
    pad = min(pad, len(x) - 1)
    ext = [2 * x[0] - x[i] for i in range(pad, 0, -1)] + list(x) + [2 * x[-1] - x[-1 - i] for i in range(1, pad + 1)]
    y = sosfilt(sos, ext)
    y = sosfilt(sos, y[::-1])[::-1]
    return y[pad:pad + len(x)]


def series(code, sensor):
    url = BASE % code
    body = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "V3R1T4S verify-it-yourself"}), timeout=120).read()
    ok_hash = hashlib.sha256(body).hexdigest() == SHA[code]
    pts = {}
    for r in json.loads(body):
        if r.get("sensor") != sensor:
            continue
        try:
            v = float(r["slevel"])
        except (TypeError, ValueError):
            continue
        if v <= -999:
            continue
        t = dt.datetime.strptime(r["stime"].strip()[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp()
        pts[t] = v
    return ok_hash, sorted(pts.items())


def analyse(pts, eta_min):
    lo = T0 - 36 * 3600
    n = 48 * 60
    s = [0.0] * n; c = [0] * n
    for t, v in pts:
        k = int((t - lo) // 60)
        if 0 <= k < n:
            s[k] += v; c[k] += 1
    x = [s[k] / c[k] if c[k] else None for k in range(n)]
    idx = [k for k in range(n) if x[k] is not None]
    for k in range(n):  # linear interpolation over gaps
        if x[k] is None:
            a = max([i for i in idx if i < k], default=None); b = min([i for i in idx if i > k], default=None)
            x[k] = x[b] if a is None else x[a] if b is None else x[a] + (x[b] - x[a]) * (k - a) / (b - a)
    m = sum(x) / n; kt = sum(range(n)) / n
    slope = sum((k - kt) * (x[k] - m) for k in range(n)) / sum((k - kt) ** 2 for k in range(n))
    x = [x[k] - m - slope * (k - kt) for k in range(n)]
    bp = filtfilt(butter_hp_sos(1 / 120.0), x)
    t = [lo + 60 * k for k in range(n)]
    pre = [bp[k] for k in range(n) if T0 - 86400 <= t[k] < T0]
    rms = math.sqrt(sum(v * v for v in pre) / len(pre))
    eta = T0 + eta_min * 60
    on = next((k for k in range(n) if max(T0, eta - 1800) <= t[k] <= eta + 3600 and abs(bp[k]) >= 3 * rms), None)
    if on is None:
        return None
    win = [k for k in range(n) if t[on] <= t[k] <= t[on] + 180 * 60]
    pk = max(abs(bp[k]) for k in win)
    kp = max(win, key=lambda k: abs(bp[k]))
    seg = [bp[k] for k in win]
    ext = [i for i in range(1, len(seg) - 1) if (seg[i] - seg[i - 1]) * (seg[i + 1] - seg[i]) < 0]
    p2t = max([abs(seg[ext[i + 1]] - seg[ext[i]]) for i in range(len(ext) - 1)] or [0])
    lab = lambda tt: dt.datetime.fromtimestamp(tt, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"rms24": rms, "onset_min": (t[on] - T0) / 60, "peak": pk, "R": pk / rms, "dt_arr": (t[on] - eta) / 60,
            "p2t": p2t, "onset_utc": lab(t[on]), "peak_utc": lab(t[kp])}


rows = [r for r in csv.reader(l for l in open(OBJ) if not l.startswith("#"))]
hdr, data = rows[0], rows[1:]
ok = hashlib.sha256("".join(l for l in open(OBJ) if l.startswith("#")).encode()).hexdigest() == HDR_SHA
print("object comment lines unchanged:", ok)
# Columns this script cannot recompute offline (control days, null counts, model ETA, names) are pinned to the values
# the panel reviewed; the model ETA is also tied to onset and dt_arr below.
FIXED = ("gauge", "ioc_code", "sensor", "eta_model_min", "control_days_detect", "null_controls_R_ge_real")
fixed_ok = hashlib.sha256("\n".join("|".join(dict(zip(hdr, r))[c] for c in FIXED) for r in data).encode()).hexdigest() == "a003316acbfc7af7797ffbd79e3c56b4a241c96ced3e3e51330ab85eaed1cb6b"
print("pinned columns unchanged:", fixed_ok)
ok = ok and fixed_ok
stations_ok = set()
for r in data:
    d = dict(zip(hdr, r))
    code, sensor = d["ioc_code"], d["sensor"]
    good_hash, pts = series(code, sensor)
    res = analyse(pts, float(d["eta_model_min"]))
    if res is None:
        print(code, "no onset found"); ok = False; continue
    checks = {
        "sha256 of re-downloaded series matches record": good_hash,
        "R > 5": res["R"] > 5,
        "|onset - ETA| <= 10 min": abs(res["dt_arr"]) <= 10,
        "R matches object (3%)": abs(res["R"] - float(d["R"])) <= 0.03 * float(d["R"]),
        "peak matches object (0.003 m)": abs(res["peak"] - float(d["peak_m"])) <= 0.003,
        "onset matches object (1 min)": abs(res["onset_min"] - float(d["onset_min_after_origin"])) <= 1.0,
        "dt_arr matches object (1 min)": abs(res["dt_arr"] - float(d["dt_arr_min"])) <= 1.0,
        "onset - ETA = dt_arr in object (0.06 min)": abs(float(d["onset_min_after_origin"]) - float(d["eta_model_min"]) - float(d["dt_arr_min"])) <= 0.06,
        "p2t matches object (0.002 m)": abs(res["p2t"] - float(d["p2t_m"])) <= 0.002,
        "rms24 matches object (0.0002 m)": abs(res["rms24"] - float(d["rms24_m"])) <= 0.0002,
        "onset/peak UTC labels match": res["onset_utc"] == d["onset_utc"] and res["peak_utc"] == d["peak_utc"],
        "lat/lon match IOC metadata (0.002 deg)": max(abs(a - float(d[k])) for a, k in zip(station(code), ("lat", "lon"))) <= 0.002,
        "dist_km matches source (0.2 km)": abs(gc_km(SRC[0], SRC[1], float(d["lat"]), float(d["lon"])) - float(d["dist_km"])) <= 0.2,
    }
    print("%s/%s: R %.3f peak %.4f m rms24 %.4f m onset %.1f min dt_arr %+.2f min | %s" % (
        code, sensor, res["R"], res["peak"], res["rms24"], res["onset_min"], res["dt_arr"],
        ", ".join("%s=%s" % (k, v) for k, v in checks.items())))
    if all(checks.values()):
        stations_ok.add("Lifou" if code.startswith("lifo") else "Luganville" if code == "luga" else code)
    else:
        ok = False
ok = ok and {"Luganville", "Lifou"} <= stations_ok
print("stations passing:", sorted(stations_ok))
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
