#!/usr/bin/env python3
"""Check a list of anomaly-free U(1) charge assignments against the six ACCs (all-left-handed basis).
Usage: check_list.py QMAX NU(0|1) FILE   (one solution per line, whitespace-separated integers)
Checks: each line satisfies all six ACCs; max |F| <= QMAX; not all zero; canonical form (each species' three
charges sorted ascending; the lexicographically larger of F and -F after sorting); gcd 1; lines in strictly
increasing lexicographic order (as integer tuples), which rules out duplicates without holding the list in memory.
FILE may be gzip-compressed (.gz). The U(1)_Y^2 U(1)_F condition is checked multiplied by 6 (integer form).
Prints the number of valid lines and PASS, or the first failure and FAIL."""
import sys
import gzip
from math import gcd

def accs(F, nu):
    Q, u, d, L, e = F[0:3], F[3:6], F[6:9], F[9:12], F[12:15]
    n = F[15:18] if nu else [0, 0, 0]
    s = sum
    return (
        s(2*q for q in Q) + s(u) + s(d),
        s(3*q for q in Q) + s(L),
        s(Q) + 8*s(u) + 2*s(d) + 3*s(L) + 6*s(e),   # 6 x (sum F_Q/6 + 4F_u/3 + F_d/3 + F_L/2 + F_e)
        s(6*q for q in Q) + s(3*x for x in u) + s(3*x for x in d) + s(2*x for x in L) + s(e) + s(n),
        s(q*q for q in Q) - 2*s(x*x for x in u) + s(x*x for x in d) - s(x*x for x in L) + s(x*x for x in e),
        s(6*q**3 for q in Q) + s(3*x**3 for x in u) + s(3*x**3 for x in d) + s(2*x**3 for x in L) + s(x**3 for x in e) + s(x**3 for x in n),
    )

def canon(F, nu):
    k = 6 if nu else 5
    a = [x for i in range(k) for x in sorted(F[3*i:3*i+3])]
    b = [x for i in range(k) for x in sorted([-y for y in F[3*i:3*i+3]])]
    return tuple(max(a, b))

def main():
    qmax, nu, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    n = 18 if nu else 15
    prev = None
    count = 0
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        for ln, line in enumerate(f, 1):
            if not line.strip():
                continue
            F = [int(x) for x in line.split()]
            why = None
            if len(F) != n: why = "wrong length"
            elif any(a != 0 for a in accs(F, nu)): why = "ACC violated %s" % (accs(F, nu),)
            elif max(abs(x) for x in F) > qmax: why = "charge above QMAX"
            elif all(x == 0 for x in F): why = "zero solution"
            elif tuple(F) != canon(F, nu): why = "not canonical"
            else:
                g = 0
                for x in F: g = gcd(g, x)
                if g != 1: why = "gcd %d" % g
                elif prev is not None and tuple(F) <= prev: why = "not strictly increasing (duplicate or unsorted)"
            if why:
                print("line %d: %s: %s" % (ln, why, line.strip()))
                print("FAIL")
                sys.exit(1)
            prev = tuple(F)
            count += 1
    print("valid solutions: %d" % count)
    print("PASS")

if __name__ == "__main__":
    main()
