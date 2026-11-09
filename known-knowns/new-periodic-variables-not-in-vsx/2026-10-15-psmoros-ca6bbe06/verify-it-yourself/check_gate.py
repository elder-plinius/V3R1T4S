"""Standalone checker (Python standard library only) for the vsx-reproduce-known calibration gate.
Run from the package folder:  python3 -I -B verify-it-yourself/check_gate.py
Checks, from the definition: 'Pipeline recovers, blind, the VSX period for at least 50 randomly drawn VSX
EW/EA/RRAB/DSCT stars with ZTF coverage (within 0.1% or 2x alias) and reports its own false-alarm rate on 50 VSX
constant / non-variable comparison stars; saved as a table.'
1. every file listed in SHA256SUMS is intact (catches any edit to object/ or the evidence);
2. the variable table: 80 scored stars of types EW/EA/RRAB/DSCT, processed in the seeded draw order, P_vsx equal to
   the saved B/vsx pool; recovery recomputed with an independent agree() (0.1% at 1x, 2x or 1/2x);
3. the control table: 400 scored controls, >= 50 of them VSX CST; false-alarm counts at T = 54.0 recomputed;
   recovered AND detected (S above every control) recounted;
4. optional (--lc-dir DIR, after verify-it-yourself/fetch_lightcurves.py DIR): each recovered period folds the star's
   ZTF light curve (phase dispersion, 25 bins) far better than 100 seeded random periods (ratio to the random median
   < 0.8); files whose sha256 differs from how-we-built-it/data/lc_manifest.csv are reported.
Prints PASS on the last line, or FAIL with reasons."""
import csv, hashlib, json, math, os, random, sys

fails = []
def fail(msg):
    fails.append(msg); print("FAIL:", msg)

# 1. integrity
listed = {}
for line in open("SHA256SUMS", encoding="utf-8"):
    parts = line.strip().split(None, 1)
    if len(parts) == 2:
        listed[parts[1].lstrip("*").lstrip("./")] = parts[0]
bad = 0
for rel, h in listed.items():
    if not os.path.isfile(rel) or hashlib.sha256(open(rel, "rb").read()).hexdigest() != h:
        bad += 1; fail("sha256 mismatch or missing: " + rel)
print("integrity: %d files listed, %d bad" % (len(listed), bad))

def rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))
def agree(p, q, tol=1e-3):
    return any(abs(p / (r * q) - 1.0) <= tol for r in (1.0, 2.0, 0.5))

V = rows("object/vsx_reproduce_known_table.csv")
Cc = rows("object/controls_table.csv")
pool = {r["OID"].strip(): r for r in rows("how-we-built-it/data/vsx_var_pool.csv")}
order = rows("how-we-built-it/data/var_draw_order.csv")

# 2. variables
scored = [r for r in V if r["scored"] == "True"]
if len(scored) != 80: fail("scored variables %d != 80" % len(scored))
if any(r["type"].strip() not in ("EW", "EA", "RRAB", "DSCT") for r in V): fail("type outside EW/EA/RRAB/DSCT")
for i, r in enumerate(V):
    if str(order[i]["OID"]).strip() != r["vsx_oid"].strip():
        fail("draw %s is not the seeded draw-order star" % r["draw"])
    pr = pool.get(r["vsx_oid"].strip())
    if pr is None or abs(float(pr["Period"]) - float(r["P_vsx"])) > 1e-12:
        fail("P_vsx of draw %s differs from the saved B/vsx pool" % r["draw"])
rec = [r for r in scored if agree(float(r["P_rec"]), float(r["P_vsx"]))]
mine = {r["draw"] for r in rec}
if any((r["draw"] in mine) != (r["recovered"] == "True") for r in scored): fail("recovered column disagrees with agree()")
print("variables: scored %d, recovered (independent agree) %d" % (len(scored), len(rec)))

# 3. controls
cs = [r for r in Cc if r["scored"] == "True"]
n_cst = sum(1 for r in cs if r["set"] == "cst")
bar = max(float(r["S"]) for r in cs)
far_all = sum(1 for r in cs if float(r["S"]) > 54.0)
far_cst = sum(1 for r in cs if r["set"] == "cst" and float(r["S"]) > 54.0)
rd = sum(1 for r in rec if float(r["S"]) > bar)
print("controls: scored %d (VSX CST %d), max control S %.6f, S > 54.0: %d/%d overall, %d/%d CST"
      % (len(cs), n_cst, bar, far_all, len(cs), far_cst, n_cst))
print("recovered AND S above every control: %d (rule: >= 50)" % rd)
if len(cs) < 400: fail("fewer than 400 scored controls")
if n_cst < 50: fail("fewer than 50 VSX CST controls")
if rd < 50: fail("fewer than 50 recovered and detected")

# 4. light curves: phase dispersion at P_rec vs random periods
def theta(t, m, P, nb=25):
    bins = [[] for _ in range(nb)]
    for ti, mi in zip(t, m):
        bins[int(((ti / P) % 1.0) * nb) % nb].append(mi)
    mu = sum(m) / len(m); tot = sum((x - mu) ** 2 for x in m) / (len(m) - 1)
    num = 0.0; dof = 0
    for b in bins:
        if len(b) > 1:
            bm = sum(b) / len(b); num += sum((x - bm) ** 2 for x in b); dof += len(b) - 1
    return (num / dof) / tot if dof > 0 and tot > 0 else 1.0
lcdir = sys.argv[sys.argv.index("--lc-dir") + 1] if "--lc-dir" in sys.argv else None
man = {(r["set"], int(r["draw"])): r["sha256"] for r in rows("how-we-built-it/data/lc_manifest.csv")}
rng = random.Random(20261015)
worst = 0.0
for r in (rec if lcdir else []):
    fn = os.path.join(lcdir, "var_%04d.json" % int(r["draw"]))
    raw = open(fn, "rb").read()
    if hashlib.sha256(raw).hexdigest() != man[("var", int(r["draw"]))]:
        print("note: draw %s light curve differs from the scored file (SNAD 'latest' changed)" % r["draw"])
    d = json.loads(raw)
    best = max(((len(v["lc"]), k) for k, v in d.items() if v["meta"]["filter"] in ("zg", "zr")), default=(0, None))
    lc = d[best[1]]["lc"]
    t = [e["mjd"] for e in lc]; m = [e["mag"] for e in lc]
    th = theta(t, m, float(r["P_rec"]))
    rnd = sorted(theta(t, m, math.exp(rng.uniform(math.log(0.05), math.log(20.0)))) for _ in range(100))
    ratio = th / rnd[50]
    worst = max(worst, ratio)
    if ratio >= 0.8: fail("draw %s: P_rec does not fold its light curve (PDM ratio %.3f)" % (r["draw"], ratio))
if lcdir:
    print("light curves: %d recovered periods folded; worst PDM ratio to random median %.3f (limit 0.8)" % (len(rec), worst))
else:
    print("light curves: not checked offline (run fetch_lightcurves.py DIR, then this script with --lc-dir DIR)")

print("FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
