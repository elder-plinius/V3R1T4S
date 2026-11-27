"""Controls K3 (exact rationals, Python Fractions, independent of flint) and K4 (vs the lead's long-double rho.c) for lamfx.sigma_upper.
Usage: controls.py <rhofx exe> <old rho exe> <rho_exact_p128.json with rho_levels>"""
import sys, os, json
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lamfx, subprocess
from flint import fmpq
def exact_sigma(n):
    def fac(m):
        f = []; p = 3
        while p * p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0: return None
                f.append(p)
            p += 2
        if m > 1: f.append(m)
        return f
    Fs = {d: fac(d) for d in range(1, n + 1, 2)}; ds = [d for d in Fs if Fs[d] is not None]
    h = {}
    for d in ds:
        v = F(1)
        for p in Fs[d]: v /= (p - 2)
        h[d] = v
    V = sum(h.values()); lam = {}
    for d in ds:
        k = F(1)
        for p in Fs[d]: k *= F(p - 1, p - 2)
        lam[d] = (-1) ** len(Fs[d]) * k * sum(h[t] for t in ds if t <= n // d and gcd(t, d) == 1) / V
    rho = {}
    for a in ds:
        for b in ds:
            q = a // gcd(a, b) * b; rho[q] = rho.get(q, 0) + lam[a] * lam[b]
    return sum(abs(v) for v in rho.values())
ok = True
print("K3: exact Fraction Sigma(n) vs lamfx upper bound")
for n in [3, 7, 15, 31, 51, 100, 151, 200, 255, 300]:
    e = exact_sigma(n); u = lamfx.sigma_upper(n, sys.argv[1])["sigma_up"]; uF = F(int(u.p), int(u.q))
    good = uF >= e and (uF - e) / e < F(1, 10**6); ok &= good
    print(" n=%d exact=%.15g upper=%.15g rel_gap=%.2e %s" % (n, float(e), float(uF), float((uF - e) / e), "ok" if good else "BAD"))
print("K4: vs long-double rho.c (lead) at every level used")
lv = json.load(open(sys.argv[3]))["rho_levels"]
ns = [r[0] for r in lv]
out = subprocess.run([sys.argv[2]] + [str(n) for n in ns], capture_output=True, text=True, check=True).stdout.split("\n")
old = {int(l.split()[0]): float(l.split()[3]) for l in out if l.strip()}
for r in lv:
    n = r[0]; u = float(fmpq(int(r[4]), int(r[5]))); rel = abs(u - old[n]) / old[n]; good = rel < 1e-8; ok &= good
    print(" n=%d exact_upper=%.15g longdouble=%.15g rel=%.2e %s" % (n, u, old[n], rel, "ok" if good else "BAD"))
print("PASS" if ok else "FAIL")
