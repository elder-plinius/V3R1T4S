#!/usr/bin/env python3
"""Checker for super edge-magic labelings of trees, written from the definition
(Figueroa-Centeno, Ichishima and Muntaner-Batle reformulation, as quoted in the V3R1T4S bank entry
super-edge-magic-trees-beyond-17): a graph with p vertices and q edges is super edge-magic iff there is a
bijection f: V -> {1..p} whose q edge sums f(u)+f(v) form q consecutive integers.
Certificate line format: n;u-v,u-v,...;l0,...,l(n-1)[;anything]  (vertices 0..n-1, li = label of vertex i).
Standard library only. Usage: python3 check_sem.py FILE  (prints a summary; last line PASS or FAIL)."""
import sys

def check(n, edges, labels):
    q = len(edges)
    if len(labels) != n: return False, "label count"
    if sorted(labels) != list(range(1, n+1)): return False, "labels are not a bijection onto 1..n"
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n): return False, "vertex id out of range 0..n-1"
    if q == 0: return True, "ok"
    s = sorted(labels[u]+labels[v] for u, v in edges)
    if s != list(range(s[0], s[0]+q)): return False, "edge sums not q consecutive integers"
    return True, "ok"

def parse(line):
    """Return (n, edges, labels) or raise ValueError on a malformed line."""
    parts = line.strip().split(";")
    if len(parts) < 3: raise ValueError("fewer than 3 fields")
    n = int(parts[0])
    edges = []
    for x in parts[1].split(","):
        if not x: continue
        a, b = x.split("-")
        edges.append((int(a), int(b)))
    labels = [int(x) for x in parts[2].split(",")] if parts[2] else []
    return n, edges, labels

if __name__ == "__main__":
    bad = tot = 0
    for line in open(sys.argv[1]):
        if not line.strip() or line.startswith("#"): continue
        tot += 1
        try:
            ok, why = check(*parse(line))
        except ValueError as e:
            ok, why = False, "malformed line (%s)" % e
        if not ok: bad += 1; print("FAIL", why, line.strip()[:80])
    print("checked %d labelings, %d failures" % (tot, bad))
    print("PASS" if tot and not bad else "FAIL")
