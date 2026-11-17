"""Standalone checker for the p3 reproduction package (Python 3 standard library only). Run from the package folder.

Definition (Bracher, Ray, Gneiting, Reich 2021): for K central prediction intervals with levels alpha_k and the median
m, WIS = (0.5 |y - m| + sum_k alpha_k/2 * IS_alpha_k) / (K + 1/2), with IS_alpha = (u - l) + 2/alpha (l - y) 1(y < l)
+ 2/alpha (y - u) 1(y > u). It equals the mean over the 2K+1 quantile levels of 2 x pinball loss. Sharpness is the
(u - l) part, underprediction and overprediction the two penalty parts. The hub uses K = 11 (23 quantiles).

Checks:
1. object/p3_reproduction_table.csv has the sha256 recorded below (a corrupted copy fails).
2. Its published columns equal the per-model means of the published scores.csv (PUB, copied below; the table itself
   is not included; see the-record-we-beat/record.md).
3. Truth mode owidhosp (hospitalisation truth from the hub's OWID file): all 15 models within 1% on wis, sharpness,
   underprediction and overprediction; relative differences recomputed from the table's columns.
4. Truth mode primary (ECDC hospitalisation file): exactly the 7 named models are over 1%.
5. object/rows_not_exact_owid_hosp_truth.csv: 3 rows, each differing only where the recomputed value is within 1e-6
   of a half integer (rounding ties). object/rows_not_exact_primary_truth.csv: 534 rows, 531 of them inc hosp CZ and
   the other 3 the same rounding ties.
6. The WIS identity (interval form = pinball form) on deterministic pseudo-random cases, a known positive (a point
   mass scores mean_tau 2|1(y<m) - tau||y - m|) and a known negative (a 1/(K+1) normalisation differs).
The full recomputation from the public inputs is in RUN_IT_YOURSELF.md (needs numpy and pandas).
Last line: PASS or FAIL.
"""
import csv
import hashlib
import math
import random
import sys

OBJ = "object/p3_reproduction_table.csv"
EXPECT_SHA = "f6fc71163c4247914cb1f832649ed956887aabef08de4bc353e1904e2662f8e0"
# model: (rows, mean wis, mean sharpness, mean underprediction, mean overprediction) from scores.csv
PUB = {
    'ECDC-norrsken_blue': (2310, 525.278354978355, 227.96709956709958, 3.675324675324675, 293.61038961038963),
    'ECDC-norrsken_green': (2390, 610.3615062761506, 114.56820083682008, 15.041004184100418, 480.7334728033473),
    'ECDC-soca_simplex': (1315, 173.63878326996198, 34.53231939163498, 66.19847908745247, 72.89353612167301),
    'EuroCOVIDhub-baseline': (3988, 705.4686559679037, 525.6100802407221, 60.889167502507526, 118.95661985957874),
    'EuroCOVIDhub-ensemble': (3379, 350.3998224326724, 157.79017460787216, 54.85084344480615, 137.7496300680675),
    'ICM-agentModel': (152, 922.3947368421053, 180.48684210526315, 677.2565789473684, 64.6842105263158),
    'ISI-BLModel': (690, 6.673913043478261, 1.0420289855072464, 3.428985507246377, 2.1449275362318843),
    'ISI-SMtrend': (862, 4.930394431554524, 0.4431554524361949, 3.534802784222738, 0.8132250580046404),
    'Lydia-SARIMA': (3369, 1550.9504303947758, 1439.439893143366, 22.215494211932324, 89.27960819234194),
    'Lydia-simpleARIMA': (2066, 1604.2357212003872, 1456.0716360116166, 32.836882865440465, 115.30154888673766),
    'PL_GRedlarski-DistrictsSum': (96, 1493.75, 478.2604166666667, 489.6354166666667, 525.8645833333334),
    'epiforecasts-EpiNow2': (2949, 391.8674126822652, 106.0, 151.4852492370295, 134.35537470328924),
    'epiforecasts-tsensemble': (4913, 307.03785874211275, 66.3942601261958, 128.47506615102787, 112.14858538571137),
    'epiforecasts-weeklygrowth': (543, 3496.5801104972375, 3011.476979742173, 190.74953959484347, 294.36648250460405),
    'fjordhest-ensemble': (2234, 363.71530886302594, 100.4816472694718, 138.9785138764548, 124.2506714413608),
}
OVER_PRIMARY = {"EuroCOVIDhub-baseline", "EuroCOVIDhub-ensemble", "Lydia-SARIMA", "Lydia-simpleARIMA",
                "epiforecasts-tsensemble", "epiforecasts-weeklygrowth", "fjordhest-ensemble"}
C = ["wis", "sharpness", "underprediction", "overprediction"]
fails = []


def ok(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


raw = open(OBJ, "rb").read()
ok(hashlib.sha256(raw).hexdigest() == EXPECT_SHA, "object sha256 " + hashlib.sha256(raw).hexdigest())
rows = list(csv.DictReader(open(OBJ, encoding="utf-8")))
ok(len(rows) == 30, "30 rows (15 models x 2 truth modes): %d" % len(rows))
by = {(r["truth_mode"], r["model"]): r for r in rows}
for m, v in PUB.items():
    for mode in ("owidhosp", "primary"):
        r = by.get((mode, m))
        good = r is not None and int(r["rows"]) == v[0] and all(
            abs(float(r[c + "_published"]) - v[i + 1]) <= 1e-6 * max(1.0, abs(v[i + 1])) for i, c in enumerate(C))
        ok(good, "published means recorded for %s (%s)" % (m, mode))


def reldiffs(r):
    out = []
    for c in C:
        p, q = float(r[c + "_published"]), float(r[c + "_recomputed"])
        out.append((q - p) / p if p != 0 else (0.0 if q == p else float("inf")))
    return out


mx = max(max(abs(x) for x in reldiffs(by[("owidhosp", m)])) for m in PUB)
ok(mx <= 0.01, "owidhosp: all 15 models within 1%% on all four components (max |rel| %.3e)" % mx)
over = {m for m in PUB if max(abs(x) for x in reldiffs(by[("primary", m)])) > 0.01}
ok(over == OVER_PRIMARY, "primary: models over 1%% = %s" % sorted(over))
mxp = max(max(abs(x) for x in reldiffs(by[("primary", m)])) for m in PUB)
ok(abs(mxp - 0.02136) < 5e-5, "primary: max |rel| %.5f (Lydia-simpleARIMA underprediction)" % mxp)


def ties(path):
    rs = list(csv.DictReader(open(path, encoding="utf-8")))
    res = []
    for r in rs:
        tie = True
        for c in C:
            p, q = float(r[c + "_pub"]), float(r[c + "_rec"])
            if round(q) != p and abs(q - p) > 0.5 + 1e-6:
                tie = False
            if abs(q - p) > 1e-6 and abs((q - math.floor(q)) - 0.5) > 1e-6 and round(q) != p:
                tie = False
        res.append((r, tie))
    return res


t3 = ties("object/rows_not_exact_owid_hosp_truth.csv")
ok(len(t3) == 3 and all(t for _, t in t3), "owidhosp: 3 non-exact rows, all half-integer rounding ties")
tp = ties("object/rows_not_exact_primary_truth.csv")
hosp = [r for r, _ in tp if r["target_variable"] == "inc hosp" and r["location"] == "CZ"]
other = [(r, t) for r, t in tp if not (r["target_variable"] == "inc hosp" and r["location"] == "CZ")]
ok(len(tp) == 534 and len(hosp) == 531 and len(other) == 3 and all(t for _, t in other),
   "primary: 534 non-exact rows = 531 inc hosp CZ + 3 rounding ties")

# WIS identity, known positive, known negative
TAU = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
       0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99]


def wis_interval(q, y, k1=False):
    m = q[11]
    tot = (1.0 if k1 else 0.5) * abs(y - m)
    for k in range(11):
        a = 2 * TAU[k]
        lo, hi = q[k], q[22 - k]
        IS = (hi - lo) + 2 / a * (lo - y) * (y < lo) + 2 / a * (y - hi) * (y > hi)
        tot += a / 2 * IS
    return tot / (12 if k1 else 11.5)


def wis_pinball(q, y):
    return sum(2 * ((y < qq) - t) * (qq - y) for qq, t in zip(q, TAU)) / 23


rng = random.Random(20261113)
dmax, dneg = 0.0, 0.0
for _ in range(5000):
    q = sorted(rng.lognormvariate(5, 1) for _ in range(23))
    y = rng.lognormvariate(5, 1.3)
    dmax = max(dmax, abs(wis_interval(q, y) - wis_pinball(q, y)))
    dneg = max(dneg, abs(wis_interval(q, y, k1=True) - wis_pinball(q, y)))
ok(dmax < 1e-9, "WIS interval form = pinball form (max diff %.2e)" % dmax)
pos = all(abs(wis_interval([50.0] * 23, y) - sum(2 * abs((y < 50) - t) * abs(50 - y) for t in TAU) / 23) < 1e-12
          for y in (40.0, 50.0, 80.0))
ok(pos, "known positive: point mass")
ok(dneg > 1e-6, "known negative: 1/(K+1) normalisation differs (max diff %.2e)" % dneg)
print("PASS" if not fails else "FAIL")
sys.exit(0 if not fails else 1)
