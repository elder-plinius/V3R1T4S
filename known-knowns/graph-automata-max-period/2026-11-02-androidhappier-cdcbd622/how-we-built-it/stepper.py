#!/usr/bin/env python3
"""Direct stepper (third implementation, pure Python, no shared code).
Definition (OEIS A357952): node is ON next generation iff (#ON neighbours + own state) is in rule set.
usage: stepper.py GRAPH6 RULE(comma list) START(int bitmask, bit v = node v)   -> cycle length reached from START
       stepper.py GRAPH6 RULE all                                               -> max cycle length over all starts
       stepper.py GRAPH6 allrules                                               -> max over all rules subset {0..n} and starts
"""
import sys
def g6(s):
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        x = ord(ch) - 63
        bits += [(x >> (5 - b)) & 1 for b in range(6)]
    E = []; k = 0
    nb = [set() for _ in range(n)]
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i].add(j); nb[j].add(i)
            k += 1
    return n, nb
def step(n, nb, rule, st):
    on = [(st >> v) & 1 for v in range(n)]
    out = 0
    for v in range(n):
        c = on[v] + sum(on[u] for u in nb[v])
        if c in rule: out |= 1 << v
    return out
def cyc(n, nb, rule, st):
    seen = {}
    t = 0
    while st not in seen:
        seen[st] = t; st = step(n, nb, rule, st); t += 1
    return t - seen[st], st
def connected(n, nb):
    s = {0}; f = [0]
    while f:
        v = f.pop()
        for u in nb[v]:
            if u not in s: s.add(u); f.append(u)
    return len(s) == n
if __name__ == "__main__":
    g = sys.argv[1]; n, nb = g6(g)
    print("graph6", g, "n", n, "connected", connected(n, nb), "degrees", sorted(len(x) for x in nb))
    if sys.argv[2] == "allrules":
        best = (0,)
        for R in range(1 << (n + 1)):
            rule = {k for k in range(n + 1) if R >> k & 1}
            nxt = [step(n, nb, rule, s) for s in range(1 << n)]
            done = [0] * (1 << n)
            for s in range(1 << n):
                x = s; path = {}
                while x not in path and not done[x]:
                    path[x] = len(path); x = nxt[x]
                if x in path:
                    L = len(path) - path[x]
                    if L > best[0]: best = (L, sorted(rule), x)
                for y in path: done[y] = 1
        print("max_over_all_rules_and_starts", best[0], "rule", "{" + ",".join(map(str, best[1])) + "}", "state_on_cycle", best[2])
    else:
        rule = {int(x) for x in sys.argv[2].split(",") if x != ""}
        if sys.argv[3] == "all":
            print("max_over_starts", max(cyc(n, nb, rule, s)[0] for s in range(1 << n)), "rule", sorted(rule))
        else:
            L, x = cyc(n, nb, rule, int(sys.argv[3]))
            print("start", sys.argv[3], "rule", sorted(rule), "cycle_length", L)
