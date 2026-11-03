#!/usr/bin/env python3
"""Independent checker for super edge-magic labelings of trees, from the bank definition
(Figueroa-Centeno, Ichishima, Muntaner-Batle reformulation): a graph with p vertices and q edges is super edge-magic
iff there is a bijection f: V -> {1..p} whose q edge sums f(u)+f(v) form q consecutive integers.
Line format: n;u-v,u-v,...;l0,...,l(n-1)  (vertices 0..n-1)."""
import sys
def check(n, edges, labels):
    q = len(edges)
    if len(labels) != n: return False, "label count"
    if sorted(labels) != list(range(1, n+1)): return False, "labels are not a bijection onto 1..n"
    s = sorted(labels[u]+labels[v] for u, v in edges)
    if s != list(range(s[0], s[0]+q)): return False, "edge sums not q consecutive integers"
    return True, "ok"
def parse(line):
    n, e, l = line.strip().split(";")[:3]
    return int(n), [tuple(map(int, x.split("-"))) for x in e.split(",") if x], list(map(int, l.split(",")))
if __name__ == "__main__":
    bad = tot = 0
    for line in open(sys.argv[1]):
        if not line.strip() or line.startswith("#"): continue
        tot += 1; ok, why = check(*parse(line))
        if not ok: bad += 1; print("FAIL", why, line.strip()[:80])
    print("checked %d labelings, %d failures" % (tot, bad))
