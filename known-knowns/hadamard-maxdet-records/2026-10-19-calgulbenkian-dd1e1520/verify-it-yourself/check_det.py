#!/usr/bin/env python3
"""Exact determinant checker for a +-1 matrix (standard library only).

Usage: python3 check_det.py MATRIX_FILE EXPECT_D RECORDS_JSON [--neg]
  MATRIX_FILE: n lines of n integers (+1 or -1).
  EXPECT_D: the claimed normalised determinant |det| / 2**(n-1) as an exact integer.
Three independent exact computations of det: fraction-free Bareiss elimination on Python
integers, Gaussian elimination over the rationals (Fraction), and elimination modulo 14
primes near 2**61 combined by the Chinese remainder theorem. Then: entries are +-1; |det|
is divisible by 2**(n-1); D = |det| / 2**(n-1) equals EXPECT_D; the residue-class upper
bound for n = 1 mod 4 (Barba: |det| <= sqrt(2n-1) * (n-1)**((n-1)/2)) is not exceeded; D
is compared with each record in RECORDS_JSON (decimal strings, compared exactly as
Decimal values). --neg flips the sign of entry (0,1) (negative control: D must not match).
The last output line is a JSON object.
"""
import sys, json, decimal
from fractions import Fraction


def bareiss(A):
    n = len(A); M = [r[:] for r in A]; sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    M[k], M[i] = M[i], M[k]; sign = -sign; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def is_prime(m):
    if m < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if m % p == 0: return m == p
    d = m - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, m)
        if x in (1, m - 1): continue
        for _ in range(s - 1):
            x = x * x % m
            if x == m - 1: break
        else:
            return False
    return True


def det_mod(A, p):
    n = len(A); M = [[x % p for x in r] for r in A]; d = 1
    for k in range(n):
        piv = None
        for i in range(k, n):
            if M[i][k]: piv = i; break
        if piv is None: return 0
        if piv != k: M[k], M[piv] = M[piv], M[k]; d = -d
        d = d * M[k][k] % p; inv = pow(M[k][k], p - 2, p)
        for i in range(k + 1, n):
            f = M[i][k] * inv % p
            if f:
                Mi, Mk = M[i], M[k]
                for j in range(k, n): Mi[j] = (Mi[j] - f * Mk[j]) % p
    return d % p


def det_crt(A, count=14):
    ps = []; m = 1 << 61
    while len(ps) < count:
        m -= 1
        if is_prime(m): ps.append(m)
    r = 0; mod = 1
    for p in ps:
        d = det_mod(A, p)
        t = ((d - r) * pow(mod, -1, p)) % p
        r += mod * t; mod *= p
    return r if r <= mod // 2 else r - mod


def det_fraction(A):
    n = len(A); M = [[Fraction(x) for x in r] for r in A]; d = Fraction(1)
    for k in range(n):
        piv = None
        for i in range(k, n):
            if M[i][k] != 0: piv = i; break
        if piv is None: return Fraction(0)
        if piv != k: M[k], M[piv] = M[piv], M[k]; d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            if f != 0:
                for j in range(k, n): M[i][j] -= f * M[k][j]
    return d


def main():
    path, expect, rec = sys.argv[1], int(sys.argv[2]), json.load(open(sys.argv[3]))
    A = [[int(x) for x in l.split()] for l in open(path) if l.strip()]
    n = len(A)
    res = {"file": path.split("/")[-1], "n": n}
    if "--neg" in sys.argv:
        A[0][1] = -A[0][1]; res["negative_control"] = "entry (0,1) negated"
    res["square"] = all(len(r) == n for r in A)
    res["entries_plus_minus_one"] = all(x in (1, -1) for r in A for x in r)
    d1 = bareiss(A); d2 = det_crt(A); d3 = det_fraction(A)
    res["three_methods_agree_on_abs_det"] = (abs(d1) == abs(d2) == abs(d3))
    ad = abs(d1); p = 1 << (n - 1)
    res["abs_det_divisible_by_2^(n-1)"] = (ad % p == 0)
    D = ad // p
    res["D_normalised"] = str(D)
    res["D_equals_claimed"] = (D == expect)
    bar2 = (2 * n - 1) * (n - 1) ** (n - 1)
    res["n_mod_4"] = n % 4
    res["abs_det_le_Barba_bound"] = (ad * ad <= bar2)
    decimal.getcontext().prec = 60
    res["ratio_to_Barba_bound"] = str((decimal.Decimal(ad * ad) / decimal.Decimal(bar2)).sqrt())[:8]
    cmp = []
    for r in rec["records"]:
        rv = decimal.Decimal(r["value"])
        cmp.append({"source": r["source"], "value": r["value"], "D_greater": decimal.Decimal(D) > rv})
    res["comparison_with_records"] = cmp
    k = (n - 1) // 4
    e = 2 * k - 1
    q, rem = divmod(D, k ** e)
    res["D_as_m_times_k^e"] = "%d * %d^%d" % (q, k, e) if rem == 0 else "not of that form"
    print(json.dumps(res))
    return 0


sys.exit(main())
