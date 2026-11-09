"""Independent pure-Python stepper for totalistic CA on a graph (neighbours only, A357953 convention).
Usage: tstepper.py <graph6> <rule like 0,2 or empty string> <start state int>   (bit v = node v ON)
       tstepper.py <graph6> <rule> maxsingle   -> max cycle over all starts (exhaustive, small n)"""
import sys
def g6(s):
    n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: bits += [((ord(ch) - 63) >> (5 - b)) & 1 for b in range(6)]
    nb = [set() for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i].add(j); nb[j].add(i)
            k += 1
    return n, nb
def step(n, nb, R, x):
    return sum(1 << v for v in range(n) if sum((x >> u) & 1 for u in nb[v]) in R)
def cyc(n, nb, R, x):
    seen = {}; t = 0
    while x not in seen: seen[x] = t; x = step(n, nb, R, x); t += 1
    return seen[x], t - seen[x]
g, rs, st = sys.argv[1], sys.argv[2], sys.argv[3]
R = set(int(c) for c in rs.split(",") if c != "")
n, nb = g6(g)
if st == "maxall":
    best = max((cyc(n, nb, R, x)[1], x) for x in range(1 << n))
    print(f"graph6={g} n={n} rule={sorted(R)} max_cycle_over_all_starts={best[0]} at_start={best[1]}")
else:
    pre, L = cyc(n, nb, R, int(st))
    print(f"graph6={g} n={n} degrees={[len(a) for a in nb]} rule={sorted(R)} start={st} preperiod={pre} cycle_length={L}")
