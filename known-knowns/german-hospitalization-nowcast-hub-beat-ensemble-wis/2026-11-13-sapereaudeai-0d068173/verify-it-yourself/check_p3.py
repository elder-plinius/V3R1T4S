"""Standalone checker for the p3 reproduction package (Python 3 standard library only). Run from the package folder.

Definition (Wolffram et al. 2023, PLoS Comput Biol 19:e1011394, eq. 2): WIS = 1/(2N+1) (|y - m| + sum_k alpha_k IS_alpha_k),
N = 3, alpha = 0.5, 0.2, 0.05 = the mean over the 7 quantile levels of 2 x pinball loss; a published cell is the mean
over all scored quantile rows of a model at one level.

Checks:
1. object/p3_reproduction_table.csv has the sha256 recorded below (a corrupted copy fails).
2. The 31 published values (the-record-we-beat/record.md; copied below as PUB) equal the table's pub_wis column.
3. Stage S2 (the published evaluation's exclusion and repair rules): every one of the 31 cells is within 1% of the
   published value; 28 agree to < 1e-9 relative; the three Epiforecasts cells differ by less than 2e-4.
4. Stages S0 and S1 (without the rules): 6 of 31 cells are outside 1% or undefined at each stage (documented need of
   the rules); every S2 relative difference is recomputed from the table's wis and pub_wis columns.
5. The WIS identity (pinball form = interval form) on deterministic pseudo-random cases, a known positive (a point
   forecast scores |y - m|) and a known negative (a wrong normalisation differs).
The full recomputation from the public inputs is described in RUN_IT_YOURSELF.md (needs pandas).
Last line: PASS or FAIL.
"""
import csv
import sys
import hashlib
import math
import random

OBJ = "object/p3_reproduction_table.csv"
EXPECT_SHA = "0d068173581343468b7a4ef6f28861c18a8fbf83a5e2aa2b8808272fe7283ee4"
PUB = {
    ('national', 'Epiforecasts'): 423.0877824833674,
    ('national', 'ILM'): 142.62904907116408,
    ('national', 'KIT'): 256.1101674082833,
    ('national', 'KIT-frozen_baseline'): 1572.7172729252886,
    ('national', 'LMU'): 465.84566278744126,
    ('national', 'MeanEnsemble'): 259.5944503220587,
    ('national', 'MedianEnsemble'): 319.91481625540655,
    ('national', 'RIVM'): 289.0506436117248,
    ('national', 'RKI'): 382.9351292902262,
    ('national', 'SU'): 382.44957486697575,
    ('national', 'SZ'): 521.6907173040053,
    ('states', 'Epiforecasts'): 26.436121062098028,
    ('states', 'KIT'): 21.966840315976192,
    ('states', 'KIT-frozen_baseline'): 98.41240851040631,
    ('states', 'LMU'): 29.401141255139766,
    ('states', 'MeanEnsemble'): 22.18647102805194,
    ('states', 'MedianEnsemble'): 23.76213942050262,
    ('states', 'RIVM'): 24.33678445596914,
    ('states', 'RKI'): 30.70784615144972,
    ('states', 'SU'): 25.438784619525958,
    ('states', 'SZ'): 36.50541792773564,
    ('age', 'Epiforecasts'): 64.84597839446195,
    ('age', 'ILM'): 29.299157253840328,
    ('age', 'KIT'): 44.00253446183527,
    ('age', 'KIT-frozen_baseline'): 262.3706527263486,
    ('age', 'LMU'): 76.780345188827,
    ('age', 'MeanEnsemble'): 41.484004418582934,
    ('age', 'MedianEnsemble'): 50.372454387984774,
    ('age', 'RIVM'): 46.283498252274114,
    ('age', 'SU'): 59.50958479841513,
    ('age', 'SZ'): 87.42562635858035,
}
fails = []


def ok(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


raw = open(OBJ, "rb").read()
ok(hashlib.sha256(raw).hexdigest() == EXPECT_SHA, "object sha256 " + hashlib.sha256(raw).hexdigest())
rows = list(csv.DictReader(open(OBJ, encoding="utf-8")))
by = {(r["stage"], r["level"], r["model"]): r for r in rows}
ok(len(rows) == 93, "93 stage cells (3 stages x 31) in the table: %d" % len(rows))
for (lv, mo), v in PUB.items():
    r = by.get(("S2", lv, mo))
    ok(r is not None and abs(float(r["pub_wis"]) - v) <= 1e-9 * v, "published value recorded for %s %s" % (lv, mo))


def rel(r):
    w = r["wis"]
    if w in ("", "nan", "NaN"):
        return float("nan")
    return float(w) / float(r["pub_wis"]) - 1.0


s2 = [(k, rel(by[("S2",) + k])) for k in PUB]
ok(all(abs(d) <= 0.01 for _, d in s2), "S2: all 31 cells within 1%% (max |rel| %.3e)" % max(abs(d) for _, d in s2))
exact = [k for k, d in s2 if abs(d) < 1e-9]
ok(len(exact) == 28, "S2: 28 cells agree to < 1e-9 relative: %d" % len(exact))
nonexact = sorted(k for k, d in s2 if abs(d) >= 1e-9)
ok(nonexact == sorted([("national", "Epiforecasts"), ("states", "Epiforecasts"), ("age", "Epiforecasts")]),
   "S2: the only non-exact cells are the three Epiforecasts cells")
ok(all(abs(d) < 2e-4 for k, d in s2 if k in nonexact), "S2: Epiforecasts residuals below 2e-4")
for st in ("S0", "S1"):
    bad = [k for k in PUB if not (abs(rel(by[(st,) + k])) <= 0.01)]
    ok(len(bad) == 6, "%s: 6 cells outside 1%% or undefined without the full rules: %d" % (st, len(bad)))

TAU = [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975]


def wis_pinball(q, y):
    return sum(2 * ((1.0 if y < qi else 0.0) - t) * (qi - y) for qi, t in zip(q, TAU)) / 7.0


def wis_interval(q, y):
    tot = abs(y - q[3])
    for k, a in enumerate([0.05, 0.2, 0.5]):
        lo, up = q[k], q[6 - k]
        tot += a * ((up - lo) + 2 / a * (lo - y) * (y < lo) + 2 / a * (y - up) * (y > up))
    return tot / 7.0


rnd = random.Random(20261113)
md = 0.0
for _ in range(20000):
    q = sorted(rnd.gauss(100, 20) for _ in range(7))
    y = rnd.gauss(100, 35)
    md = max(md, abs(wis_pinball(q, y) - wis_interval(q, y)))
ok(md < 1e-9, "WIS pinball form = interval form (max diff %.2e)" % md)
ok(all(abs(wis_pinball([50.0] * 7, y) - abs(y - 50.0)) < 1e-12 for y in (40.0, 50.0, 80.0)),
   "known positive: a point forecast scores |y - m|")
q = sorted(rnd.gauss(100, 20) for _ in range(7))
ok(abs(wis_pinball(q, 130.0) * 7 / 4 - wis_interval(q, 130.0)) > 1e-6, "known negative: a wrong normalisation differs")
print("PASS" if not fails else "FAIL")
sys.exit(0 if not fails else 1)
