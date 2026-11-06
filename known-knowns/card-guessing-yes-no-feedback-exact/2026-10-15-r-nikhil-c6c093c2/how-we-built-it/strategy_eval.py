#!/usr/bin/env python3
"""Exact expected score of fixed strategies (greedy, linear card counting) and of optimal play, on the
(g, {(r_i,f_i)}) state space, with exact fractions. Independent Python implementation (no C++ code reused).
greedy: guess a most likely label (max p_i), ties broken uniformly at random among tied labels.
linear:B: guess a label maximising r_i + B f_i (DGS: c_i + beta g_i), ties uniform at random among tied labels.
optimal: max over labels (exhausted labels included).
"""
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial
sys.setrecursionlimit(10000)

@lru_cache(maxsize=None)
def C(pairs):
    M = sum(r for r, f in pairs); poly = [1]; denom = 1
    for r, f in pairs:
        a = []; fall = 1
        for k in range(min(r, f) + 1):
            if k: fall *= (r - k + 1)
            a.append((-1) ** k * comb(f, k) * fall)
        new = [0] * (len(poly) + len(a) - 1)
        for i, pc in enumerate(poly):
            for j, ac in enumerate(a): new[i + j] += pc * ac
        poly = new; denom *= factorial(r)
    tot = sum(c * factorial(M - K) for K, c in enumerate(poly))
    assert tot % denom == 0
    return tot // denom

def succ(g, pairs, idx):
    r, f = pairs[idx]; rest = pairs[:idx] + pairs[idx+1:]
    yes = (g, tuple(sorted(rest + ((r-1, f),)))) if r > 1 else (g + f, tuple(sorted(rest)))
    no = (g, tuple(sorted(rest + ((r, f+1),))))
    return yes, no

def make(n, m, strategy):
    @lru_cache(maxsize=None)
    def V(g, pairs):
        L = sum(r for r, f in pairs) - sum(f for r, f in pairs) - g
        if L == 0: return Fraction(0)
        Cs = C(pairs)
        opts = []  # (score key, multiplicity, value)
        seen = set()
        for idx, (r, f) in enumerate(pairs):
            if (r, f) in seen: continue
            seen.add((r, f)); mult = pairs.count((r, f))
            yes, no = succ(g, pairs, idx)
            Cy = C(yes[1]); Cn = Cs - Cy
            val = Fraction(0)
            if Cy: val += Fraction(Cy, Cs) * (1 + V(*yes))
            if Cn: val += Fraction(Cn, Cs) * V(*no)
            if strategy == 'greedy': key = Fraction(Cy, Cs)
            elif strategy.startswith('linear:'): key = Fraction(r) + Fraction(strategy[7:]) * f
            else: key = val
            opts.append((key, mult, val))
        if len(pairs) < n:  # exhausted label guess
            mult = n - len(pairs); val = V(g + 1, pairs)
            if strategy == 'greedy': key = Fraction(0)
            elif strategy.startswith('linear:'): key = Fraction(0)  # c_i = 0, and g_i for exhausted labels is not tracked: treated as 0
            else: key = val
            opts.append((key, mult, val))
        best = max(k for k, _, _ in opts)
        tied = [(mu, v) for k, mu, v in opts if k == best]
        tot = sum(mu for mu, _ in tied)
        return sum(Fraction(mu, tot) * v for mu, v in tied)
    return V(0, tuple((m, 0) for _ in range(n)))

if __name__ == '__main__':
    n, m, strat = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    v = make(n, m, strat)
    print(f"n={n} m={m} strategy={strat} value={v} = {float(v):.6f}")
