#!/usr/bin/env python3
"""Builder-side generator (needs numpy and scipy; NOT part of the shipped standard-library check).
Produces the rational dual certificates read by e8_check.py. Every certificate is verified again,
in exact integers, by e8_check.py; nothing here is trusted.
usage: e8_gen_dual.py MATFILE OUTFILE
"""
import sys, math, time
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import e8_check as E

mat, out = sys.argv[1], sys.argv[2]
A, _ = E.load_matrix(mat)
P, S, G, C, Ci, base = E.identify(A)
Pn = np.array(P, dtype=float)
cs = E.enumerate_dominant(Ci, 620)
QS = list(range(1, 65)) + [96, 120, 128, 192, 240, 256, 384, 512, 768, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 1 << 17, 1 << 18, 1 << 19, 1 << 20, 1 << 22, 1 << 24]
lines = []
tight = []
stats = {'fail': 0, 'q1': 0}
t0 = time.time()
B = 3000.0
for idx, c in enumerate(cs):
    nv = [sum(Ci[a][b] * c[b] for b in range(8)) for a in range(8)]
    nw = [2 * x for x in nv]
    xs = [2 * sum(p[k] * c[k] for k in range(8)) for p in P]
    xa = np.array(xs, dtype=float)
    fp = np.abs(3 * xa - 13)    # s = +1
    fm = np.abs(3 * xa + 13)    # s = -1
    # variables: m (8), t (120). minimize sum t - nw.m
    cost = np.concatenate([-np.array(nw, dtype=float), np.ones(120)])
    # t_i >= fp_i + n_i.m  ->  n_i.m - t_i <= -fp_i
    A1 = np.hstack([Pn, -np.eye(120)])
    b1 = -fp
    # t_i >= fm_i - n_i.m  ->  -n_i.m - t_i <= -fm_i
    A2 = np.hstack([-Pn, -np.eye(120)])
    b2 = -fm
    r = linprog(cost, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([b1, b2]), bounds=[(-B, B)] * 8 + [(0, None)] * 120, method='highs')
    assert r.status == 0, r.message
    m = r.x[:8]
    found = None
    for q in QS:
        Mv = [int(round(v * q)) for v in m]
        d = E.dual_times_q(P, xs, nw, Mv, q)
        if d <= 6104 * q:
            found = (Mv, q)
            break
    if found is None:
        # try exact vertex by limit_denominator
        for den in (10, 100, 1000, 10000, 100000):
            fr = [Fraction(float(v)).limit_denominator(den) for v in m]
            q = 1
            for f in fr:
                q = q * f.denominator // math.gcd(q, f.denominator)
            Mv = [int(f * q) for f in fr]
            d = E.dual_times_q(P, xs, nw, Mv, q)
            if d <= 6104 * q:
                found = (Mv, q)
                break
    if found is None:
        stats['fail'] += 1
        print("NO certificate for c =", c, "LP value", r.fun, flush=True)
        continue
    Mv, q = found
    if q == 1:
        stats['q1'] += 1
    if abs(r.fun - 6104) < 1e-6:
        tight.append(c)
    lines.append(" ".join(str(x) for x in c) + " " + " ".join(str(x) for x in Mv) + " " + str(q))
    if idx % 2000 == 0:
        print(idx, len(cs), "%.0fs" % (time.time() - t0), flush=True)
open(out, 'w').write("\n".join(lines) + "\n")
print("done", len(lines), "certificates; failures", stats['fail'], "; integer-only", stats['q1'], "; LP-tight dominant vectors:", tight)
