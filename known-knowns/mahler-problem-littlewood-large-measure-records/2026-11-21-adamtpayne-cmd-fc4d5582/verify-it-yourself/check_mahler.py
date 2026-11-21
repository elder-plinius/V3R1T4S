#!/usr/bin/env python3
"""Standalone, rigorous checker (Python standard library only, exact integers).

Claim checked: the polynomial f in the object file (coefficients +-1, x^0 first) has degree d and
Mahler measure M(f) > T + 1e-9, where T is the table value given on the command line.

Method (Graeffe root squaring, no root finding): if f_0 = f and f_{m+1}(x^2) = (-1)^d f_m(x) f_m(-x),
then the roots of f_m are the 2^m-th powers of the roots of f, so M(f_m) = M(f)^(2^m) exactly.
For any integer polynomial g of degree d with coefficients c_k, |c_k| <= C(d,k) M(g) (Vieta), so
    M(g) >= max_k |c_k| / C(d,k),
and by Landau's inequality M(g) <= ||g||_2. Hence
    (max_k |c_k^(m)| / C(d,k))^(1/2^m)  <=  M(f)  <=  ||f_m||_2^(1/2^m),
rigorous for every m; the bracket tightens as m grows. All arithmetic on the coefficients is exact;
the final 2^m-th root is bounded with exact integer comparisons (no floating point in the decision).

usage: check_mahler.py object_file table_value [m]
Last line: PASS or FAIL.
"""
import sys
from math import comb


def graeffe(c):
    d = len(c) - 1
    even = c[0::2]
    odd = c[1::2]

    def mul(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    r[i + j] += x * y
        return r

    e2 = mul(even, even)
    o2 = mul(odd, odd) if odd else [0]
    h = [0] * (d + 1)
    for i, v in enumerate(e2):
        h[i] += v
    for i, v in enumerate(o2):
        h[i + 1] -= v  # f(x) f(-x) = E(x^2)^2 - x^2 O(x^2)^2, so h(y) = E(y)^2 - y O(y)^2
    if d % 2:
        h = [-v for v in h]
    return h


def lower_bound_exceeds(c_m, d, m, P, Q):
    """True iff (max_k |c_k| / C(d,k))^(1/2^m) > P/Q, decided with exact integers:
    some k has |c_k| * Q^(2^m) > C(d,k) * P^(2^m)."""
    e = 1 << m
    Pe, Qe = pow(P, e), pow(Q, e)
    return any(abs(v) * Qe > comb(d, k) * Pe for k, v in enumerate(c_m) if v)


def main():
    obj, table = sys.argv[1], sys.argv[2]
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 18
    s = open(obj).read().strip()
    if not s or any(ch not in '+-' for ch in s):
        print("object is not a +/- string"); print("FAIL"); return 1
    c = [1 if ch == '+' else -1 for ch in s]
    d = len(c) - 1
    print(f"degree {d}, {d + 1} coefficients, all +-1")
    # target = table + 1e-9 as an exact fraction P/Q (table given in decimal)
    ip, _, fp = table.partition('.')
    Q = 10 ** max(len(fp), 9)
    P = int(ip) * Q + int((fp or '0').ljust(len(str(Q)) - 1, '0')) + Q // 10 ** 9
    g = c
    for i in range(1, m + 1):
        g = graeffe(g)
    ok = lower_bound_exceeds(g, d, m, P, Q)
    # report the bracket numerically (informational only)
    import math
    lo_log = max((abs(v).bit_length() - 1) * math.log(2) - math.log(comb(d, k)) for k, v in enumerate(g) if v)
    print(f"Graeffe iterations m = {m}; certified lower bound on M(f) about {math.exp(lo_log / 2 ** m):.6f} (display only, rounded down by up to a factor 2^(1/2^m))")
    print(f"table value + 1e-9 = {P / Q:.12f}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
