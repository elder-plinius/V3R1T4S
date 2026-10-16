#!/usr/bin/env python3
"""brute-scale lens: independent exact checker for a spherical code file.

c* = max_{i<j} <x_i/|x_i|, x_j/|x_j|> computed in mpmath at 50 digits from the decimal strings in the file.
Screen: float64 Gram of the normalised vectors; every pair with float value >= gmax - 1e-7 is recomputed in mpmath
(float64 error of a normalised inner product for d <= 64 is < 1e-13, so the screen cannot drop the true maximum).
To be extra safe the screen is widened to 1e-6 if fewer than 2 pairs are inside it.

Usage: python3 -I bs_check.py FILE D N [--plain plain.csv] [--bar bar_table.tsv]
Prints one JSON line. Needs numpy + mpmath only.
"""
import csv
import json
import re
import sys

import mpmath
import numpy as np

mpmath.mp.dps = 50
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def read(path):
    pts = []
    for line in open(path):
        t = NUM.findall(line)
        if t:
            pts.append(t)
    return pts


def sig(tok):
    m = tok.lower().split("e")[0].lstrip("+-").replace(".", "")
    s = m.lstrip("0")
    return len(s) if s else len(m)


def cstar(pts, screen=1e-7):
    X = np.array([[float(t) for t in p] for p in pts])
    n = np.linalg.norm(X, axis=1)
    if np.any(n == 0):
        raise ValueError("zero vector")
    Y = X / n[:, None]
    G = Y @ Y.T
    np.fill_diagonal(G, -3.0)
    gmax = G.max()
    I, J = np.nonzero(np.triu(G >= gmax - screen, 1))
    if len(I) < 2:
        I, J = np.nonzero(np.triu(G >= gmax - 1e-6, 1))
    M = [[mpmath.mpf(t) for t in p] for p in pts]
    inv = {}
    def iv(i):
        if i not in inv:
            inv[i] = 1 / mpmath.sqrt(mpmath.fsum([a * a for a in M[i]]))
        return inv[i]
    best = mpmath.mpf(-3)
    for i, j in zip(I.tolist(), J.tolist()):
        v = mpmath.fsum([a * b for a, b in zip(M[i], M[j])]) * iv(i) * iv(j)
        if v > best:
            best = v
    return best, len(I), float(gmax)


def main(a):
    opts = {}
    for k in ("--plain", "--bar"):
        if k in a:
            i = a.index(k); opts[k] = a[i + 1]; del a[i:i + 2]
    path, d, N = a[1], int(a[2]), int(a[3])
    pts = read(path)
    out = {"file": path, "d": d, "N": N, "npts": len(pts)}
    ok = len(pts) == N and all(len(p) == d for p in pts)
    out["shape_ok"] = ok
    if not ok:
        print(json.dumps(out)); return 1
    out["min_sig_digits"] = min(sig(t) for p in pts for t in p)
    c, nscr, gf = cstar(pts)
    out["c_star"] = mpmath.nstr(c, 25)
    out["n_screened_pairs"] = nscr
    out["float_max"] = repr(gf)
    out["min_angle_deg"] = mpmath.nstr(mpmath.degrees(mpmath.acos(c)), 15)
    if "--plain" in opts:
        ct = None
        for row in csv.reader(open(opts["--plain"])):
            if len(row) >= 3 and row[0].strip() == str(d) and row[1].strip() == str(N):
                ct = row[2].strip()
        out["c_table_plain"] = ct
        if ct is not None:
            g = mpmath.mpf(ct) - c
            out["gain_vs_plain"] = mpmath.nstr(g, 12)
            out["gain_ge_1e-10"] = bool(g >= mpmath.mpf("1e-10"))
    if "--bar" in opts:
        for r in csv.DictReader(open(opts["--bar"]), delimiter="\t"):
            if int(r["d"]) == d and int(r["N"]) == N:
                out["star"] = r["star"]; out["nmo"] = r["nmo"]; out["cos_index"] = r["cos_index"]
                vc = r["cos_vahteristo"]
                out["cos_vahteristo"] = vc
                if vc not in ("", "None"):
                    gv = mpmath.mpf(vc) - c
                    out["gain_vs_vahteristo"] = mpmath.nstr(gv, 12)
                    out["below_vahteristo_by_1e-10"] = bool(gv >= mpmath.mpf("1e-10"))
                out["kissing_excluded"] = bool(9 <= d <= 23 and c <= mpmath.mpf("0.5"))
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(list(sys.argv)))
