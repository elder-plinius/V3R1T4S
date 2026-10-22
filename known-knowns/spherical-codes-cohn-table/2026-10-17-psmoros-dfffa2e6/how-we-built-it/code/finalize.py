#!/usr/bin/env python3
"""Certify a candidate code and (if it passes) write result/d<d>_N<N>.txt and a claims.csv row.

usage: finalize.py CANDIDATE_FILE D N
Checks (all from the run's snapshots; the main session re-fetches the live table at the gate):
  shape, >= 20 significant digits per coordinate, c* (mpmath 50 digits, via bs_check.cstar),
  gain vs plain.csv >= 1e-10, c* below Vahteristo's cosine by >= 1e-10, row unstarred and not NMO in
  index_parsed.tsv, not taken, not kissing (9 <= d <= 23 and c* <= 0.5).
"""
import csv, hashlib, json, os, shutil, sys
import mpmath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bs_check as K

RUN = "WORKDIR/runs/2026-10-16-0024"
LENS = RUN + "/attempts/brute-scale"
TAKEN = {(29, 114), (30, 74), (29, 72), (28, 70), (30, 117), (29, 145), (26, 232), (27, 68)}


def main(a):
    path, d, N = a[1], int(a[2]), int(a[3])
    pts = K.read(path)
    rep = {"d": d, "N": N, "file": path}
    rep["shape_ok"] = len(pts) == N and all(len(p) == d for p in pts)
    rep["min_sig_digits"] = min(K.sig(t) for p in pts for t in p)
    c, nscr, gf = K.cstar(pts)
    rep["c_star"] = mpmath.nstr(c, 25)
    ct = None
    for row in csv.reader(open(RUN + "/data/sc/plain.csv")):
        if len(row) >= 3 and row[0].strip() == str(d) and row[1].strip() == str(N):
            ct = row[2].strip()
    rep["c_table"] = ct
    bar = None
    for r in csv.DictReader(open(RUN + "/data/sc/bar_table.tsv"), delimiter="\t"):
        if int(r["d"]) == d and int(r["N"]) == N:
            bar = r
    rep["star"] = bar["star"]; rep["nmo"] = bar["nmo"]; rep["cos_vahteristo"] = bar["cos_vahteristo"]
    gain = mpmath.mpf(ct) - c if ct else None
    rep["gain"] = mpmath.nstr(gain, 15) if gain is not None else None
    gv = mpmath.mpf(bar["cos_vahteristo"]) - c if bar["cos_vahteristo"] not in ("", "None") else None
    rep["gain_vs_vahteristo"] = mpmath.nstr(gv, 15) if gv is not None else None
    ok = (rep["shape_ok"] and rep["min_sig_digits"] >= 20 and ct is not None and gain >= mpmath.mpf("1e-10")
          and (gv is None or gv >= mpmath.mpf("1e-10")) and bar["star"] == "0" and bar["nmo"] == "0"
          and (d, N) not in TAKEN and not (9 <= d <= 23 and c <= mpmath.mpf("0.5")))
    rep["passes_lens_checks"] = bool(ok)
    print(json.dumps(rep))
    if ok:
        os.makedirs(LENS + "/result", exist_ok=True)
        dst = LENS + "/result/d%d_N%d.txt" % (d, N)
        shutil.copyfile(path, dst)
        sha = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        cp = LENS + "/result/claims.csv"
        new = not os.path.exists(cp)
        rows = []
        if not new:
            rows = [r for r in csv.reader(open(cp))][1:]
            rows = [r for r in rows if not (r[0] == str(d) and r[1] == str(N))]
        rows.append([str(d), str(N), mpmath.nstr(c, 25), ct, mpmath.nstr(gain, 12), sha])
        with open(cp, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["d", "N", "c_star", "c_table", "gain", "sha256"])
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
