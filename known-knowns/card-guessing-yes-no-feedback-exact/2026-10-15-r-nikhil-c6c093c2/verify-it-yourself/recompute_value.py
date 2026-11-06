#!/usr/bin/env python3
"""Recompute P+_{m,n} (card guessing, yes/no feedback) from scratch with Python integers only: an independent
implementation of the backward recursion of Luo (arXiv:2609.25062, Appendix A) on the canonical state
(g, sorted (r_i, f_i) pairs of labels with r_i >= 1), using the integer form W = C * V+:
  W(s) = max over labels [ C(yes) + W(yes) + W(no) ],  W = 0 when L = 0,  C from (A.1).
Prints the reduced fraction and compares it with --expect. Standard library only. n = 11 takes a few minutes.
"""
import sys, argparse
from fractions import Fraction
from math import comb, factorial

_fact = {}
def label_factor(r, f):
    a = []; fall = 1
    for k in range(min(r, f) + 1):
        if k: fall *= (r - k + 1)
        a.append((-1) ** k * comb(f, k) * fall)
    return a
_C = {}
def C(pairs):
    c = _C.get(pairs)
    if c is not None: return c
    M = sum(r for r, f in pairs); poly = [1]; den = 1
    for r, f in pairs:
        a = label_factor(r, f); new = [0] * (len(poly) + len(a) - 1)
        for i, pc in enumerate(poly):
            if pc:
                for j, ac in enumerate(a): new[i + j] += pc * ac
        poly = new; den *= factorial(r)
    t = sum(cf * factorial(M - K) for K, cf in enumerate(poly) if cf)
    assert t % den == 0
    c = t // den; _C[pairs] = c; return c

def successors(g, pairs, idx):
    r, f = pairs[idx]; rest = pairs[:idx] + pairs[idx + 1:]
    yes = (g, tuple(sorted(rest + ((r - 1, f),)))) if r > 1 else (g + f, tuple(sorted(rest)))
    no = (g, tuple(sorted(rest + ((r, f + 1),))))
    return yes, no

def solve(n, m):
    init = (0, tuple((m, 0) for _ in range(n)))
    Lmax = n * m
    # forward enumeration layer by layer (states with C > 0 only)
    layers = [None] * (Lmax + 1); layers[Lmax] = {init}
    for L in range(Lmax, 0, -1):
        nxt = set()
        for (g, pairs) in layers[L]:
            k = len(pairs)
            for idx in range(k):
                if idx and pairs[idx] == pairs[idx - 1]: continue
                yes, no = successors(g, pairs, idx)
                if C(yes[1]) > 0: nxt.add(yes)
                if C(no[1]) > 0: nxt.add(no)
            if k < n: nxt.add((g + 1, pairs))
        layers[L - 1] = nxt
    # backward evaluation
    prev = {}
    for L in range(0, Lmax + 1):
        cur = {}
        for s in layers[L]:
            g, pairs = s
            if L == 0: cur[s] = 0; continue
            Cs = C(pairs); best = -1; k = len(pairs)
            for idx in range(k):
                if idx and pairs[idx] == pairs[idx - 1]: continue
                yes, no = successors(g, pairs, idx)
                Cy = C(yes[1]); Wy = prev.get(yes, 0); Wn = prev.get(no, 0)
                assert Cy + C(no[1]) == Cs
                cand = Cy + Wy + Wn
                if cand > best: best = cand
            if k < n:
                cand = prev.get((g + 1, pairs), 0)
                if cand > best: best = cand
            cur[s] = best
        prev = cur; layers[L] = None
    W = prev[init]; Cinit = C(init[1])
    return Fraction(W, Cinit), sum(1 for _ in [])

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('n', type=int); ap.add_argument('m', type=int, nargs='?', default=2)
    ap.add_argument('--expect', help='expected reduced fraction NUM/DEN')
    a = ap.parse_args()
    import time; t0 = time.time()
    v, _ = solve(a.n, a.m)
    print(f"n={a.n} m={a.m} P+={v} = {float(v):.12f} seconds={time.time()-t0:.1f}")
    if a.expect:
        ok = (v == Fraction(a.expect))
        print("expected:", a.expect, "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
