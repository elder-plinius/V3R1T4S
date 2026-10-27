"""Mc table (maximum curvature + 0.2, 0.1-magnitude bins) from the live ComCat queries saved in data/mc_*.csv (run from
claim/: python -I code/mc_table.py). Query URLs: REPRODUCE.md section 4. Bins by floor (floor(10 m) / 10) and by
numpy-style round half to even (round(10 m) / 10); the maximum-curvature bin is the most populated (ties: the lower)."""
import csv, glob, os, math
CL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
for f in sorted(glob.glob(os.path.join(CL, "data", "mc_*km.csv"))):
    M = [float(e["mag"]) for e in csv.DictReader(open(f)) if e["mag"]]; out = []
    for how in ("floor", "round"):
        H = {}
        for m in M:
            x = (math.floor(m * 10 + 1e-9) if how == "floor" else round(m * 10)) / 10; H[x] = H.get(x, 0) + 1
        pk = max(H, key=lambda k: (H[k], -k)); out.append("%s maxc %.1f Mc %.1f" % (how, pk, round(pk + 0.2, 1)))
    print("%-28s n=%5d  %s" % (os.path.basename(f), len(M), "; ".join(out)))
