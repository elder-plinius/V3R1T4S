#!/usr/bin/env python3
"""Exact checker for Erdos 677 counterexample candidates (standard library only).

  python3 -I check677.py N M K [--allow-different-length L2]

M(n, k) = lcm(n+1, ..., n+k). A counterexample to Erdos 677 is (m, n, k) with k > 0, m >= n + k and
M(m, k) == M(n, k). With --allow-different-length L2 it instead tests M(n, K) == M(m, L2) (Erdos's known
different-length coincidences; used only as the checker's positive test).
Last line: PASS (a counterexample / the tested equality holds) or FAIL.
"""
import sys
from math import gcd

def M(n, k):
    v = 1
    for x in range(n + 1, n + k + 1):
        v = v // gcd(v, x) * x
    return v

def main():
    a = sys.argv[1:]
    l2 = None
    if "--allow-different-length" in a:
        i = a.index("--allow-different-length"); l2 = int(a[i + 1]); del a[i:i + 2]
    n, m, k = (int(x) for x in a)
    problems = []
    if l2 is None:
        if not k > 0: problems.append("k must be > 0")
        if not m >= n + k: problems.append("blocks overlap: m < n + k")
        x, y = M(n, k), M(m, k)
        print("M(n,k) = %s\nM(m,k) = %s" % (x if x < 10**60 else "%d digits" % len(str(x)), y if y < 10**60 else "%d digits" % len(str(y))))
    else:
        x, y = M(n, k), M(m, l2)
        print("M(%d,%d) = %d, M(%d,%d) = %d" % (n, k, x, m, l2, y))
    if x != y: problems.append("lcms differ")
    for p in problems: print("problem: " + p)
    print("FAIL" if problems else "PASS")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
