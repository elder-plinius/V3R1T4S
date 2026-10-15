#!/usr/bin/env python3
"""independent_recheck.py: a second, independently written evaluation of LB(D) for a mixture JSON, by a different
route than ../../code/lb_check.py: the normalised-posterior (Lemma 3.3) form. For each environment, p_i(s) =
Pr[high state | s_i] computed from the likelihoods, report x_i = theta_1 + Delta p_i, joint posterior
p12 = (p1 p2/lam2) / ((1-p1)(1-p2)/lam1 + p1 p2/lam2), pair probability P(s1)P(s2)((1-p1)(1-p2)/lam1 + p1 p2/lam2),
fBayes = theta_1 + Delta p12; then LB = sum over distinct report pairs of the D-weighted variance of fBayes.
Exact rationals. Prints the value and compares with 31/1326."""
import sys, json
from fractions import Fraction as F
d = json.load(open(sys.argv[1]))
acc = {}
tw = F(0)
for e in d["environments"]:
    w = F(e["weight"]); tw += w
    th1, th2 = F(e["theta"][0]), F(e["theta"][1]); lam1, lam2 = F(e["prior"][0]), F(e["prior"][1])
    assert 0 <= th1 <= th2 <= 1 and lam1 + lam2 == 1 and lam1 >= 0 and lam2 >= 0
    D = th2 - th1
    exps = []
    for ex in e["experts"]:
        L = [[F(v) for v in row] for row in ex["likelihoods"]]
        assert sum(L[0]) == 1 and sum(L[1]) == 1 and all(0 <= v <= 1 for row in L for v in row)
        sig = []
        for s in range(len(L[0])):
            Ps = lam1 * L[0][s] + lam2 * L[1][s]
            if Ps == 0: continue
            p = lam2 * L[1][s] / Ps
            sig.append((Ps, p, th1 + D * p))
        exps.append(sig)
    for (P1, p1, x1) in exps[0]:
        for (P2, p2, x2) in exps[1]:
            z = (1 - p1) * (1 - p2) / lam1 + p1 * p2 / lam2 if D > 0 else F(1)
            prob = P1 * P2 * z
            if prob == 0: continue
            p12 = (p1 * p2 / lam2) / z if D > 0 else F(0)
            fb = th1 + D * p12
            a = acc.setdefault((x1, x2), [F(0), F(0), F(0)])
            a[0] += w * prob; a[1] += w * prob * fb; a[2] += w * prob * fb * fb
assert tw == 1
lb = sum(m2 - m1 * m1 / m0 for (m0, m1, m2) in acc.values())
bar = F(31, 1326)
print("independent LB:", lb); print("float: %.15f" % float(lb)); print("bar 31/1326 = %.15f" % float(bar))
print("strictly greater than bar:", "yes" if lb > bar else "no"); print("margin: %.6e" % float(lb - bar))
