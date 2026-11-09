"""calibrator-v2 pipeline (run 2026-10-15-1643). Blind: never sees a catalogue period.

analyze(d): d = SNAD API v3 circle json (dict oid -> {meta, lc}).
  Bands: for zg and zr separately, the ZTF object with the most good epochs in that band (SNAD lc = good epochs).
  A band is used if it has >= NBAND epochs. USABLE LC := at least one band with >= NUSE epochs.
  Multi-band periodogram on one common grid f in [FMIN, FMAX], df = 0.2/T (T = full span; astropy 'fast' LS, trig_sum oversampling 2):
      Z_b(f) = -(N_b - 3)/2 * log10(1 - p_b(f))   (p_b = 1-term floating-mean LS power, astropy standard norm;
                                                   Z = -log10 single-frequency false-alarm probability)
      Z(f)   = sum over used bands of Z_b(f)
  Candidate peaks: the NPK highest local maxima of Z, each refined with exact LS on a +-3 df local grid.
  For each candidate f: split-half replicates. Times split at the median epoch of the union of bands (H1 = before,
  H2 = after); Zh1(f), Zh2(f) = the same summed Z computed on each half only, evaluated exactly AT f.
  Alias distance a(f) = distance to the nearest m*FS/k +- b (k = 1..4, b in {0, j/29.530589, j/365.25, j=1..4}).
select(rec, params): period pick + S, applied to the stored candidates:
  eligible := a(f) > DELTA and f >= FLOW; f* := eligible candidate with the largest Z; P_rec = 1/f*;
  S := min(Zh1(f*), Zh2(f*))   (replication: the period must be significant in both halves independently).
  No eligible candidate -> S = 0, P_rec = NaN.
"""
import numpy as np
from astropy.timeseries import LombScargle

FS = 1.0027379093
LUNAR, YEAR = 29.530589, 365.25
FMIN, FMAX = 0.01, 20.0
NBAND, NUSE, NPK = 20, 50, 60


def bands(d):
    out = {}
    for filt in ("zg", "zr"):
        c = [(len(v["lc"]), oid) for oid, v in d.items() if v["meta"]["filter"] == filt]
        if c:
            n, oid = max(c)
            if n >= NBAND:
                lc = d[oid]["lc"]
                t = np.array([p["mjd"] for p in lc], float); y = np.array([p["mag"] for p in lc], float)
                e = np.array([p["magerr"] for p in lc], float)
                o = np.argsort(t); out[filt] = (oid, t[o], y[o], e[o])
    return out


def alias_dist(f, mode="full"):
    """distance (c/d) to the nearest alias-family member m*day/k + s*b (m >= 0 integer, s = +-1), day in
    {1 (solar), FS (sidereal)}.  mode 'full': k = 1..4, b in {0, j/LUNAR, j/YEAR, j = 1..4}.
    mode 'lunar': k = 1, b in {j/LUNAR, j = 1..4} only (the lunar family and its daily sidelobes).
    mode 'lunyear': k = 1, b in {j/LUNAR, j/YEAR, j = 1..4}.  mode 'pure': k = 1..4, b = 0 only."""
    f = np.atleast_1d(np.asarray(f, float))
    lun = [j / LUNAR for j in range(1, 5)]; yr = [j / YEAR for j in range(1, 5)]
    if mode == "full": ks, bases = (1, 2, 3, 4), [0.0] + lun + yr
    elif mode == "lunar": ks, bases = (1,), lun
    elif mode == "lunyear": ks, bases = (1,), lun + yr
    elif mode == "pure": ks, bases = (1, 2, 3, 4), [0.0]
    else: raise ValueError(mode)
    dmin = np.full(f.shape, np.inf)
    for day in (1.0, FS):
        for k in ks:
            step = day / k
            for b in bases:
                for sgn in (1, -1):
                    x = f - sgn * b
                    dmin = np.minimum(dmin, np.abs(x - np.round(x / step) * step))
    return dmin


def zpow(p, n):
    p = np.clip(p, 0, 1 - 1e-15)
    return -(n - 3) / 2.0 * np.log10(1 - p)


def zsum(B, f, method, sel=None):
    tot = np.zeros(len(f))
    for filt, (oid, t, y, e) in B.items():
        m = slice(None) if sel is None else sel[filt]
        tt, yy, ee = t[m], y[m], e[m]
        if len(tt) < 10: continue
        p = LombScargle(tt, yy, ee).power(f, method=method, **({"assume_regular_frequency": True, "method_kwds": {"trig_sum_kwds": {"oversampling": 2}}} if method == "fast" else {}))
        tot += zpow(p, len(tt))
    return tot


def analyze(d):
    B = bands(d)
    rec = {"bands": {k: [str(v[0]), len(v[1])] for k, v in B.items()}}
    nmax = max([len(v[1]) for v in B.values()] or [0])
    rec["usable"] = bool(nmax >= NUSE)
    if not rec["usable"]:
        return rec
    tall = np.concatenate([v[1] for v in B.values()])
    T = tall.max() - tall.min(); tmed = np.median(tall)
    df = 0.2 / T
    f = np.arange(FMIN, FMAX, df)
    Z = zsum(B, f, "fast")
    lm = np.where((Z[1:-1] > Z[:-2]) & (Z[1:-1] >= Z[2:]))[0] + 1
    top = lm[np.argsort(Z[lm])[::-1][:NPK]]
    h1 = {k: v[1] < tmed for k, v in B.items()}; h2 = {k: v[1] >= tmed for k, v in B.items()}
    cands = []
    for j in top:
        fl = np.linspace(f[j] - 3 * df, f[j] + 3 * df, 61)
        zl = zsum(B, fl, "cython"); i = int(np.argmax(zl)); fb = float(fl[i])
        zh1 = float(zsum(B, np.array([fb]), "cython", h1)[0]); zh2 = float(zsum(B, np.array([fb]), "cython", h2)[0])
        cands.append([fb, float(zl[i]), zh1, zh2, float(alias_dist(fb)[0])])
    rec.update(T=float(T), nfreq=len(f), n_epochs=int(sum(len(v[1]) for v in B.values())), cands=cands)
    ys = [v[2] for v in B.values()]
    rec["amp_5_95"] = float(max(np.percentile(y, 95) - np.percentile(y, 5) for y in ys))
    return rec


def select(rec, DELTA, FLOW, MODE="full"):
    if not rec.get("usable") or not rec.get("cands"):
        return float("nan"), 0.0, None
    C = np.array(rec["cands"], float)
    a = alias_dist(C[:, 0], MODE) if DELTA > 0 else np.full(len(C), np.inf)
    ok = (a > DELTA) & (C[:, 0] >= FLOW)
    if not ok.any():
        return float("nan"), 0.0, None
    j = int(np.argmax(np.where(ok, C[:, 1], -np.inf)))
    best = list(C[j]); best[4] = float(a[j])
    return 1.0 / best[0], float(min(best[2], best[3])), best
