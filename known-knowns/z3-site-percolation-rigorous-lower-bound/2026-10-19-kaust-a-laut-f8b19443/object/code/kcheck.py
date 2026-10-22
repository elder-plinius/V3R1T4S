"""Finite criterion for canonical geodesics. With ext[f] = sum over N-step candidate walks with |F| = f of the
number of valid extensions, K_N(p) = sum_f ext[f] p^(N+1) (1-p)^f, and theta(p) <= K_N(p) theta(p).
So K_N(p) < 1 proves theta(p) = 0, i.e. p_c^site(Z^3) >= p. Prints the largest p = j/10^6 with K_N(p) < 1
(exact rational arithmetic), and K_N at a few values. usage: python kcheck.py <canon output>"""
import sys
from fractions import Fraction

for line in open(sys.argv[1]):
    w = line.split()
    if w and w[0] == "EXT":
        N = int(w[1])
        ext = {int(a): int(b) for a, b in (t.split(":") for t in w[2:])}


def K(p):
    return sum(c * p ** (N + 1) * (1 - p) ** f for f, c in ext.items())


den = 10 ** 6
lo, hi = 0, den
while hi - lo > 1:
    mid = (lo + hi) // 2
    if K(Fraction(mid, den)) < 1:
        lo = mid
    else:
        hi = mid
print("N=%d: certified p_c^site(Z^3) >= %d/%d = %.6f   (K_N there = %.6f)" % (N, lo, den, lo / den, float(K(Fraction(lo, den)))))
for p in (0.24, 0.25, 0.26, 0.263, 0.27):
    print("   K_%d(%.3f) = %.4f" % (N, p, float(K(Fraction(p).limit_denominator(10 ** 6)))))
