"""Standalone LJ checker, Python standard library only. Definition: E = sum_{i<j} 4 (r^-12 - r^-6), sigma = epsilon = 1.
Computes E and the gradient 2-norm in decimal arithmetic (40 digits) and compares with a table value."""
import sys
from decimal import Decimal as D, getcontext
getcontext().prec = 40
path, table = sys.argv[1], D(sys.argv[2])
P = [[D(t) for t in l.split()] for l in open(path) if l.strip()]
n = len(P); assert all(len(p) == 3 for p in P)
E = D(0); G = [[D(0)] * 3 for _ in range(n)]
for i in range(n):
    a = P[i]
    for j in range(i + 1, n):
        b = P[j]; d = [a[k] - b[k] for k in range(3)]; r2 = d[0]*d[0] + d[1]*d[1] + d[2]*d[2]
        i6 = 1 / (r2 * r2 * r2); E += 4 * (i6 * i6 - i6); f = (-48 * i6 * i6 + 24 * i6) / r2
        for k in range(3): G[i][k] += f * d[k]; G[j][k] -= f * d[k]
gn = sum(c * c for g in G for c in g).sqrt()
print("N=%d" % n); print("E=%s" % +E); print("grad_norm=%.3e" % gn)
print("table=%s margin=%s" % (table, table - E))
ok = n == 662 and gn < D("1e-15") and E < table - D("1e-5")
print("PASS" if ok else "FAIL")
