#!/usr/bin/env python3
"""Independent checker for odd-graceful labelings (Gnanajothi 1991, as quoted in Gallian DS6 3.6 / bank entry):
a graph with q edges is odd-graceful if vertices get DISTINCT labels from {0,...,2q-1} so that the edge
differences |f(u)-f(v)| are EXACTLY the odd numbers 1,3,...,2q-1.
Input line format: n;u-v,u-v,...;l0,l1,...,l(n-1)   (vertices 0..n-1)"""
import sys
def check(n, edges, labels):
    q = len(edges)
    if len(labels) != n: return False, "label count %d != n %d" % (len(labels), n)
    if len(set(labels)) != n: return False, "labels not distinct"
    if any(l < 0 or l > 2*q-1 for l in labels): return False, "label out of range [0,%d]" % (2*q-1)
    diffs = sorted(abs(labels[u]-labels[v]) for u, v in edges)
    if diffs != list(range(1, 2*q, 2)): return False, "edge differences are not exactly {1,3,...,%d}" % (2*q-1)
    return True, "ok"
def parse(line):
    n, e, l = line.strip().split(";")[:3]
    edges = [tuple(map(int, x.split("-"))) for x in e.split(",") if x]
    return int(n), edges, list(map(int, l.split(",")))
if __name__ == "__main__":
    bad = 0; tot = 0
    for line in open(sys.argv[1]):
        if not line.strip() or line.startswith("#"): continue
        tot += 1; ok, why = check(*parse(line))
        if not ok: bad += 1; print("FAIL", why, line.strip()[:80])
    print("checked %d labelings, %d failures" % (tot, bad))
