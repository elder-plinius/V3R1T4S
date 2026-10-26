"""Standalone certificate verifier (Python standard library only).

Input: a line "EXT N f1:c1 f2:c2 ..." where c_f = sum over all N-step canonical-candidate walks gamma from the
origin with |F(gamma)| = f of |E(gamma)| (the number of valid extensions). Then
    K_N(p) = sum_f c_f * p^(N+1) * (1-p)^f,
and K_N(p) < 1 proves theta(p) = 0, i.e. p_c^site(Z^3) >= p.

The script checks K_N(p*) < 1 exactly at a given rational p* = j/10^6, prints K_N(p*) to 12 digits, and reports
whether p* + 1/10^6 fails (so p* is the largest such value on the 10^-6 grid). It also checks the sanity values
p = 1/5 (must pass) and p = 3116/10000 (numerical p_c; must fail).
usage: python verify_cert.py <file containing the EXT line> <j>        (p* = j / 10^6)
"""
import sys
from fractions import Fraction

ext = None
for line in open(sys.argv[1]):
    w = line.split()
    if w and w[0] == "EXT":
        N = int(w[1])
        ext = {int(a): int(b) for a, b in (t.split(":") for t in w[2:])}
if ext is None:
    sys.exit("no EXT line found")


def K(p):
    return sum(c * p ** (N + 1) * (1 - p) ** f for f, c in ext.items())


j = int(sys.argv[2])
p = Fraction(j, 10 ** 6)
k = K(p)
print("N = %d, sum of c_f = %d" % (N, sum(ext.values())))
# Monotonicity certificate: p^(N+1) (1-p)^f increases on [0, (N+1)/(N+1+f)], so K_N is increasing on
# [0, (N+1)/(N+1+f_max)]. If (j+1)/10^6 lies inside, the passing grid points form an initial segment up to j there,
# so binary search is exact and p* is the largest passing grid value on that interval.
fmax = max(f for f, c in ext.items() if c)
pmono = Fraction(N + 1, N + 1 + fmax)
print("f_max = %d: K_N is increasing on [0, %s] = [0, %.6f]; (j+1)/10^6 inside: %s"
      % (fmax, pmono, float(pmono), Fraction(j + 1, 10 ** 6) <= pmono))
print("K_N(%d/10^6) = %.12f  ->  %s" % (j, float(k), "PASS: p_c >= %d/10^6" % j if k < 1 else "FAIL"))
k2 = K(Fraction(j + 1, 10 ** 6))
print("K_N(%d/10^6) = %.12f  ->  %s" % (j + 1, float(k2), "fails (p* is maximal on the grid)" if k2 >= 1 else "also passes"))
for q, name in ((Fraction(1, 5), "1/5 (proven bound; must pass)"), (Fraction(3116, 10000), "0.3116 (numerical p_c; must fail)")):
    print("sanity %s: K = %.6f" % (name, float(K(q))))
