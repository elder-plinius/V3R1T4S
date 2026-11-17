"""Standalone checker for a spherical code against a table cosine (Python standard library only).

Definition checked (spherical-codes-cohn-table success rule): N vectors in R^d, coordinates given to >= 20
digits; after normalising each vector to unit length, the maximum pairwise inner product c* must be lower than
the table's 12-decimal cosine by at least 1e-10.

1. The file is the claimed object (sha256), N lines of d decimals, every coordinate with >= 20 significant digits,
   no zero vector.
2. Exact test (integer arithmetic): with t = c_table - 1e-10, every pair has <u,v> <= 0 or
   <u,v>^2 <= t^2 |u|^2 |v|^2.
3. c* itself at 60 digits (decimal module), and the gap c_table - c*.
Usage: verify_code.py <file> <d> <N> <c_table> <sha256>. Last output line: PASS or FAIL (exit 0 or 1)."""
import sys, hashlib, re
from fractions import Fraction
from decimal import Decimal, getcontext

def main():
    path, d, N, ctab, sha = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), Fraction(sys.argv[4]), sys.argv[5]
    raw = open(path, "rb").read()
    ok = True
    h = hashlib.sha256(raw).hexdigest()
    print("sha256", h, "expected" if h == sha else "MISMATCH (expected %s)" % sha)
    ok &= h == sha
    lines = [l for l in raw.decode("ascii").splitlines() if l.strip()]
    toks = [l.replace(",", " ").split() for l in lines]
    shape = len(toks) == N and all(len(t) == d for t in toks)
    print("points %d, coordinates per point %s" % (len(toks), sorted(set(len(t) for t in toks))))
    ok &= shape
    if not shape:
        return ok
    def sig(s):
        m = re.fullmatch(r"[+-]?(\d*)\.?(\d*)(?:[eE][+-]?\d+)?", s)
        digits = (m.group(1) + m.group(2)).lstrip("0")
        return len(digits)
    mind = min(sig(s) for t in toks for s in t)
    print("fewest significant digits in a coordinate:", mind)
    ok &= mind >= 20
    # exact integers: scale every coordinate by a common power of ten
    fr = [[Fraction(s) for s in t] for t in toks]
    den = 1
    for p in fr:
        for x in p:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
    P = [[int(x * den) for x in p] for p in fr]
    nrm = [sum(x * x for x in p) for p in P]
    zero = sum(1 for n in nrm if n == 0)
    print("zero vectors:", zero)
    ok &= zero == 0
    t = ctab - Fraction(1, 10 ** 10)
    t2n, t2d = (t * t).numerator, (t * t).denominator
    worst, wpair, viol = Fraction(-2), None, 0
    for i in range(N):
        for j in range(i + 1, N):
            s = sum(a * b for a, b in zip(P[i], P[j]))
            if s > 0 and s * s * t2d > t2n * nrm[i] * nrm[j]:
                viol += 1
            if s > 0:
                q = Fraction(s * s, nrm[i] * nrm[j])
                if q > worst:
                    worst, wpair = q, (i, j)
    print("pairs with cosine above c_table - 1e-10 (exact):", viol)
    ok &= viol == 0
    getcontext().prec = 60
    cstar = (Decimal(worst.numerator) / Decimal(worst.denominator)).sqrt()
    print("c* = %s at pair %s (0-based lines)" % (str(cstar)[:42], wpair))
    print("c_table - c* = %.6e" % float(Decimal(ctab.numerator) / Decimal(ctab.denominator) - cstar))
    return ok

if __name__ == "__main__":
    good = main()
    print("PASS" if good else "FAIL")
    sys.exit(0 if good else 1)
