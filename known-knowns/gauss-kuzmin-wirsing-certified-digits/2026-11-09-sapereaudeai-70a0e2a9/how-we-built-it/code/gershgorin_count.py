#!/usr/bin/env python3
"""Independent eigenvalue count for A_K (no use of acb_mat.eig's isolation guarantee).
usage: gershgorin_count.py K PREC MU_FILE R0 RHO
Builds A_K exactly as gkw_cert.py does (balls), takes an approximate eigenvector matrix X (midpoints of a
floating eigen-decomposition), computes B = X^-1 A_K X in ball arithmetic (X^-1 a rigorous enclosure), and applies
Gershgorin's theorem: if the K discs are pairwise disjoint, each contains exactly one eigenvalue of A_K.
Counts discs inside |z - mu| < r0 and outside |z| > rho; fails loudly if any disc straddles a circle."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gkw_cert as G
from flint import arb, acb, ctx, arb_mat, acb_mat

K, prec = int(sys.argv[1]), int(sys.argv[2])
mu_str, r0s, rhos = open(sys.argv[3]).read().split()[0], sys.argv[4], sys.argv[5]
ctx.prec = prec
mu, r0, rho = arb(mu_str).mid(), arb(r0s), arb(rhos)
Z = G.zeta_list(2 * K + 4)
F = G.fact_list(2 * K + 4)
h = G.hankel_h(2 * K + 1, Z, F)
PK = G.P_matrix(K)
Rr = arb(4) / 5
rows = []
Rj = arb(1)
for j in range(K):
    fac = Rj / F[j] * (-1 if j % 2 else 1)
    rows.append([h[j + m] / F[m + 1] * fac for m in range(K)])
    Rj = Rj * Rr
AK = arb_mat(rows) * PK
Ac = acb_mat(AK)
# approximate eigenvectors: use the eigen-solver only as a source of approximations (midpoints)
E, Rv = Ac.eig(right=True, nonstop=True)
X = Rv.mid()
Xi = X.inv()                       # rigorous enclosure of the inverse of the exact midpoint matrix X
B = Xi * Ac * X                    # similar to A_K: same eigenvalues
discs = []
for i in range(K):
    rad = arb(0)
    for j in range(K):
        if j != i:
            rad += arb(B[i, j].abs_upper())
    discs.append((B[i, i], arb((rad + arb(B[i, i].rad())).upper())))
# pairwise disjointness
ok = True
for i in range(K):
    for j in range(i + 1, K):
        if not (abs(discs[i][0].mid() - discs[j][0].mid()) > discs[i][1] + discs[j][1] + arb(discs[i][0].rad()) + arb(discs[j][0].rad())):
            ok = False
inside2 = outside = 0
for c, r in discs:
    cm = c.mid()
    d2 = abs(cm - acb(mu))
    if d2 + r < r0:
        inside2 += 1
    elif not (d2 - r > r0):
        print('disc straddles Gamma_2', c, r); ok = False
    dz = abs(cm)
    if dz - r > rho:
        outside += 1
    elif not (dz + r < rho):
        print('disc straddles |z|=rho', c, r); ok = False
maxr = discs[0][1]
for c, r in discs:
    if r > maxr:
        maxr = r
print('K=%d prec=%d  discs pairwise disjoint and no straddle: %s  max disc radius %s' % (K, prec, ok, arb(maxr.upper()).str(3)))
print('discs inside |z-mu|<r0: %d   discs with |z|>rho: %d' % (inside2, outside))
print('GERSHGORIN_COUNT', 'PASS' if (ok and inside2 == 1 and outside == 2) else 'FAIL')
