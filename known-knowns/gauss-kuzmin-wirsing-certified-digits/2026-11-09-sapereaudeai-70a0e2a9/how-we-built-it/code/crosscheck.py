#!/usr/bin/env python3
"""Contrarian lens: try to break the ingredients of gkw_cert.py with independent computations.
usage: crosscheck.py VFILE PREC
(a) L v evaluated directly at points z0 of D: explicit sum over n <= NN of (z0+n)^-2 v(1/(z0+n)) with v by Horner in
    w (no monomial conversion), plus Euler-Maclaurin-free tail sum_{n>NN} via sum_m p_m zeta(m+2, z0+NN+1);
    compared with the Taylor series sum_j (Lv)_j w0^j from the certifier's Hankel formula (J terms).
(b) analytic truncation bound for ||L e_k|| (k >= K) versus the actual column norms from the matrix.
(c) Hurwitz-zeta tail constant kappa versus arb's zeta(s, 8/5) * (8/5)^s."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gkw_cert as G
from flint import arb, acb, ctx, arb_mat

vfile, prec = sys.argv[1], int(sys.argv[2])
ctx.prec = prec
v = G.load_vec(vfile)
N = len(v)
J = 4 * N
Z = G.zeta_list(N + J + 2)
F = G.fact_list(N + J + 3)
h = G.hankel_h(N + J, Z, F)
p = G.w_to_monomial(v)
Lv = G.Lcoeffs_from_monomial(p, J, h, F)
c, R = arb(3) / 5, arb(4) / 5


def v_eval(u):
    w = (u - c) / R
    s = acb(0)
    for x in reversed(v):
        s = s * w + x
    return s


NN = 40
worst = 0
for z0 in [acb(arb(1) / 3), acb(arb(-1) / 10, arb(1) / 5), acb(arb(6) / 5, arb(-1) / 4), acb(arb(1) / 2, arb(7) / 10)]:
    direct = acb(0)
    for n in range(1, NN + 1):
        u = 1 / (z0 + n)
        direct += u * u * v_eval(u)
    tail = acb(0)
    for m in range(N):
        tail += p[m] * acb(m + 2).zeta(z0 + NN + 1)
    direct += tail
    w0 = (z0 - c) / R
    ser = acb(0)
    for j in reversed(range(J)):
        ser = ser * w0 + Lv[j]
    d = abs(direct - ser)
    print('z0=%s |w0|=%s  direct-vs-series diff %s  (|Lv(z0)| %s)' % (z0.str(4), abs(w0).str(4), d.str(3),
                                                                      abs(direct).str(5)))
# (b) column norms ||L e_k|| from the matrix vs analytic bound (25/16)(13/16)^k/sqrt(1-(13/16)^2) + ...
K = 80
J0 = 600
PK = G.P_matrix(K + 20)
Brows = []
Rj = arb(1)
for j in range(J0):
    fac = Rj / F[j] * (-1 if j % 2 else 1)
    Brows.append([h[j + m] / F[m + 1] * fac for m in range(K + 20)])
    Rj = Rj * R
AJ = arb_mat(Brows) * PK
r1, ri = arb(13) / 16, arb(3) / 4
for k in [K, K + 5, K + 10, K + 19]:
    col = sum((AJ[j, k] ** 2 for j in range(J0)), arb(0)).sqrt()
    bnd = (arb(25) / 16) * r1 ** k / (1 - r1 ** 2).sqrt() + (arb(10) / 13) * ri ** k / (1 - ri ** 2).sqrt()
    # ||L e_k|| <= ||L(I-P_k)|| bound, since e_k has unit norm and lies in the complement of P_k
    print('k=%d  ||L e_k|| (first %d coeffs) %s   analytic bound %s   ok %s' % (k, J0, col.str(4), bnd.str(4),
                                                                              col < bnd))
# (c) kappa
a = arb(8) / 5
# Compare the excesses over 1, which are tiny for large s (comparing ratio and kappa themselves is undecidable at
# working precision once (8/13)^s < 2^-prec; that was the 'ok False' at s = 4000 in run 2026-11-08-2057):
#   zeta(s,a) a^s - 1 = zeta(s, a+1) a^s   versus   kappa(s) - 1 = (a/(1+a))^s (1 + (1+a)/(s-1)).
for s in [12, 100, 1000, 4000, 4 * N, 4 * N + 2]:
    excess = arb(s).zeta(a + 1) * a ** s
    kex = (a / (1 + a)) ** s * (1 + (1 + a) / (s - 1))
    # kex is the expression that G.zeta_tail_kappa(s) adds to 1 (Lemma 5(a))
    print('s=%d  zeta(s,8/5)(8/5)^s - 1 = %s  kappa(s) - 1 = %s  ok %s' % (s, excess.str(8), kex.str(8), excess < kex))
