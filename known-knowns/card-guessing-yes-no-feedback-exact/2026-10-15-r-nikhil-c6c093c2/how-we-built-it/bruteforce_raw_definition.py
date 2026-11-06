#!/usr/bin/env python3
"""Brute-force optimal expected score for card guessing with yes/no feedback, from the raw game definition.

Deck: n labels, m copies each, N = n*m cards; uniformly random arrangement (every distinct word with the
multiset counts is equally likely, which is the same as a uniform shuffle of the physical cards).
Guesser knows n and m. At each position t = 0..N-1 the guesser names any label in [n] (including labels
whose copies are all found), then is told only whether the card at position t has that label.
Score = number of correct guesses. P+ = max over adaptive strategies of E[score].

Method: the guesser's information is the set S of arrangements consistent with the history; the posterior is
uniform on S. Let Wsum(S, t) = sum over words w in S of the score the optimal continuation earns on w.
  Wsum(S, t) = max over labels g of [ |S_g| + Wsum(S_g, t+1) + Wsum(S \ S_g, t+1) ],  S_g = {w in S : w[t] = g},
  Wsum(S, N) = 0.   Then P+ = Wsum(S0, 0) / |S0|.
Sets are bitmasks over the enumerated words; memoised on (t, S). No sufficient statistic is assumed.
"""
import sys, time
from fractions import Fraction
from itertools import permutations

def words(n, m):
    deck = []
    for i in range(n): deck += [i]*m
    return sorted(set(permutations(deck)))

def solve(n, m, time_cap=None):
    W = words(n, m)
    N = n*m
    # mask[t][g] = bitmask of words with w[t]==g
    mask = [[0]*n for _ in range(N)]
    for idx, w in enumerate(W):
        for t in range(N):
            mask[t][w[t]] |= (1 << idx)
    full = (1 << len(W)) - 1
    memo = {}
    t0 = time.time()
    sys.setrecursionlimit(10000)
    def pc(x): return bin(x).count('1')
    def rec(S, t):
        if t == N or S == 0:
            return 0
        key = (t, S)
        v = memo.get(key)
        if v is not None: return v
        if time_cap and time.time()-t0 > time_cap: raise TimeoutError
        best = -1
        for g in range(n):
            Sg = S & mask[t][g]
            cand = pc(Sg) + rec(Sg, t+1) + rec(S & ~Sg, t+1)
            if cand > best: best = cand
        memo[key] = best
        return best
    tot = rec(full, 0)
    return Fraction(tot, len(W)), len(W), len(memo), time.time()-t0

if __name__ == '__main__':
    n = int(sys.argv[1]); m = int(sys.argv[2]); cap = float(sys.argv[3]) if len(sys.argv) > 3 else None
    try:
        v, nw, ns, dt = solve(n, m, cap)
        print(f"n={n} m={m} words={nw} memo_states={ns} P+={v} = {float(v):.10f} time={dt:.1f}s")
    except TimeoutError:
        print(f"n={n} m={m} TIMEOUT after {cap}s")
