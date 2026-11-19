#!/usr/bin/env python3
"""Independent stepper for OEIS A357953 (pure Python, no shared code with totF.c / main.go).
Definition: connected graph on n nodes; rule R subset of {0..n-1}; node v is ON at t+1 iff the number of ON
neighbours of v (v itself not counted) at t is in R.
Usage: stepper.py <graph6> <rule as comma list, e.g. 0,2,4> <start_state_int>   (bit v of the state = node v ON;
nodes in graph6 order). Prints pre-period and minimal cycle length. Also: permax(g6) = max over ALL 2^n rules
(no degree pruning) and all 2^n starts."""
import sys
def g6(s):
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        x = ord(ch) - 63
        bits += [(x >> (5 - b)) & 1 for b in range(6)]
    adj = [[] for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i].append(j); adj[j].append(i)
            k += 1
    return n, adj
def step(n, adj, R, st):
    out = 0
    for v in range(n):
        c = 0
        for u in adj[v]: c += (st >> u) & 1
        if c in R: out |= 1 << v
    return out
def cycle(n, adj, R, st):
    seen = {}; t = 0; x = st
    while x not in seen:
        seen[x] = t; x = step(n, adj, R, x); t += 1
    return seen[x], t - seen[x]
def counts_table(n, adj):
    return [[sum((s >> u) & 1 for u in adj[v]) for v in range(n)] for s in range(1 << n)]
def permax(n, adj):
    """max over all 2^n rules R subset {0..n-1} and all 2^n starts; returns (max, rule_mask, start)."""
    C = counts_table(n, adj); best = (0, 0, 0); N = 1 << n
    for rm in range(1 << n):
        nxt = [0] * N
        for s in range(N):
            o = 0; cs = C[s]
            for v in range(n):
                if (rm >> cs[v]) & 1: o |= 1 << v
            nxt[s] = o
        mark = [0] * N  # 0 new, else id of walk
        for s0 in range(N):
            if mark[s0]: continue
            path = []; x = s0; wid = s0 + 1
            while not mark[x]:
                mark[x] = wid; path.append(x); x = nxt[x]
            if mark[x] == wid:
                L = len(path) - path.index(x)
                if L > best[0]: best = (L, rm, x)
    return best
if __name__ == "__main__":
    s = sys.argv[1]; R = set(int(x) for x in sys.argv[2].split(',') if x != ''); st = int(sys.argv[3])
    n, adj = g6(s)
    pre, L = cycle(n, adj, R, st)
    print(f"graph6={s} n={n} edges={sum(map(len, adj))//2} rule={sorted(R)} start={st} preperiod={pre} cycle_length={L}")
