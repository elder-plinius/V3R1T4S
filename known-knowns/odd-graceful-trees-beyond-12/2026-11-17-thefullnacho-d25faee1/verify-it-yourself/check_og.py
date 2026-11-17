#!/usr/bin/env python3
"""Odd-graceful tree certificate checker (Python 3, standard library only).

Line format: n;u-v,u-v,...;l0,l1,...[;ignored]
Blank lines and lines starting with # are skipped.

Definition: a graph with q edges is odd-graceful if there is an injection
f: V -> {0,...,2q-1} whose edge differences |f(u)-f(v)| are exactly
{1,3,...,2q-1}. This program also checks that each line is a tree on
vertices {0,...,n-1}, that the trees are pairwise non-isomorphic under
the AHU canonical form of an unrooted tree, and that the count equals
A000055(n) when --expect is given or n is in the built-in table.

Usage:
  python3 check_og.py --selftest
  python3 check_og.py [--n N] [--expect K] [--regen] FILE
Last line: PASS or FAIL
"""
import argparse, sys

A000055 = {
    0:1,1:1,2:1,3:1,4:2,5:3,6:6,7:11,8:23,9:47,10:106,11:235,12:551,
    13:1301,14:3159,15:7741,16:19320,17:48629,18:123867,19:317955,
    20:823065,21:2144505,22:5623756,23:14828074,24:39299897,
}

def ahu_rooted(adj, v, p):
    kids = []
    for w in adj[v]:
        if w != p:
            kids.append(ahu_rooted(adj, w, v))
    kids.sort()
    return "(" + "".join(kids) + ")"

def centres(adj):
    n = len(adj)
    if n <= 2:
        return list(range(n))
    deg = [len(adj[v]) for v in range(n)]
    leaves = [v for v in range(n) if deg[v] <= 1]
    remain = n
    while remain > 2:
        remain -= len(leaves)
        nxt = []
        for v in leaves:
            for u in adj[v]:
                deg[u] -= 1
                if deg[u] == 1:
                    nxt.append(u)
        leaves = nxt
    return leaves

def ahu_unrooted(adj):
    c = centres(adj)
    if len(c) == 1:
        return ahu_rooted(adj, c[0], -1)
    a = ahu_rooted(adj, c[0], c[1])
    b = ahu_rooted(adj, c[1], c[0])
    return a + "|" + b if a <= b else b + "|" + a

def parse_and_check(line, expect_n=0):
    line = line.strip()
    if not line or line.startswith("#"):
        return None  # skip
    parts = line.split(";")
    if len(parts) < 3:
        raise ValueError("need at least three fields")
    n = int(parts[0])
    if expect_n and n != expect_n:
        raise ValueError("n is %d, expected %d" % (n, expect_n))
    if n < 1:
        raise ValueError("n < 1")
    q = n - 1
    adj = [[] for _ in range(n)]
    edges = []
    if q == 0:
        if parts[1] != "":
            raise ValueError("n=1 should have no edges")
    else:
        for tok in parts[1].split(","):
            a, b = tok.split("-")
            a, b = int(a), int(b)
            if a < 0 or b < 0 or a >= n or b >= n or a == b:
                raise ValueError("bad edge %s" % tok)
            if (a, b) in edges or (b, a) in edges:
                raise ValueError("repeated edge %s" % tok)
            edges.append((a, b))
            adj[a].append(b)
            adj[b].append(a)
        if len(edges) != q:
            raise ValueError("expected %d edges, got %d" % (q, len(edges)))
    # connected?
    seen = set()
    stack = [0]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj[v])
    if len(seen) != n:
        raise ValueError("not connected")
    labels = [int(x) for x in parts[2].split(",")]
    if len(labels) != n:
        raise ValueError("expected %d labels" % n)
    if len(set(labels)) != n:
        raise ValueError("labels are not injective")
    if any(l < 0 or l > 2 * q - 1 for l in labels):
        raise ValueError("label out of range")
    diffs = []
    for a, b in edges:
        d = abs(labels[a] - labels[b])
        diffs.append(d)
    if sorted(diffs) != list(range(1, 2 * q, 2)):
        raise ValueError("edge differences are not {1,3,...,2q-1}")
    return n, ahu_unrooted(adj)

def check_file(path, expect_n=0, expect=None, do_regen=False):
    forms = {}
    n_seen = expect_n
    nlines = 0
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            try:
                r = parse_and_check(line, expect_n)
            except ValueError as e:
                print("line %d: %s" % (lineno, e))
                print("FAIL")
                return 1
            if r is None:
                continue
            n, form = r
            n_seen = n
            nlines += 1
            if form in forms:
                print("line %d: isomorphic to line %d" % (lineno, forms[form]))
                print("FAIL")
                return 1
            forms[form] = lineno
    if expect is None and n_seen in A000055:
        expect = A000055[n_seen]
    print("n=%s lines=%d unique=%d expected=%s" % (n_seen, nlines, len(forms), expect))
    if expect is not None and (nlines != expect or len(forms) != expect):
        print("FAIL")
        return 1
    if do_regen:
        if n_seen is None:
            print("nothing to regenerate")
            print("FAIL")
            return 1
        gen = generate_trees(n_seen)
        print("regenerated=%d" % len(gen))
        if gen != set(forms):
            missing = gen - set(forms)
            extra = set(forms) - gen
            print("regen mismatch: only_generated=%d only_certificate=%d" % (len(missing), len(extra)))
            print("FAIL")
            return 1
        print("regen_match=1")
    print("PASS")
    return 0

def generate_trees(n):
    """All unrooted unlabeled trees on n vertices, as AHU forms, by leaf extension."""
    if n < 1:
        return set()
    if n == 1:
        return {ahu_unrooted([[]])}
    # start from K2
    adj = {2: [[1], [0]]}
    forms = {2: {ahu_unrooted(adj[2])}}
    trees = {2: [adj[2]]}
    for k in range(3, n + 1):
        seen = set()
        out = []
        for t in trees[k - 1]:
            for v in range(k - 1):
                nt = [list(x) for x in t] + [[]]
                nt[v].append(k - 1)
                nt[k - 1].append(v)
                form = ahu_unrooted(nt)
                if form not in seen:
                    seen.add(form)
                    out.append(nt)
        trees[k] = out
        forms[k] = seen
        if k in A000055 and len(seen) != A000055[k]:
            raise SystemExit("internal regen count %d != A000055(%d)=%d" % (len(seen), k, A000055[k]))
    return forms[n]

def selftest():
    fails = 0
    def acc(s):
        nonlocal fails
        try:
            parse_and_check(s)
        except ValueError:
            print("should accept:", s)
            fails += 1
    def rej(s):
        nonlocal fails
        try:
            parse_and_check(s)
            print("should reject:", s)
            fails += 1
        except ValueError:
            pass
    acc("2;0-1;0,1")
    acc("3;0-1,1-2;0,3,2")
    acc("4;0-1,1-2,2-3;0,5,2,3")
    acc("4;0-1,0-2,0-3;0,1,3,5")
    a = parse_and_check("4;0-1,1-2,2-3;0,5,2,3")[1]
    b = parse_and_check("4;0-1,1-2,2-3;3,2,5,0")[1]
    if a != b:
        print("P4 numberings should match")
        fails += 1
    c = parse_and_check("4;0-1,0-2,0-3;0,1,3,5")[1]
    if a == c:
        print("path and star should differ")
        fails += 1
    rej("4;0-1,1-2,2-3;0,1,2,3")
    rej("4;0-1,1-2,2-3;0,5,2,5")
    rej("4;0-1,1-2,2-3;0,5,2,7")
    rej("3;0-1,1-2,2-0;0,3,2")
    rej("4;0-1,1-2,2-3,0-3;0,5,2,3")
    rej("4;0-1,1-2;0,5,2,3")
    rej("4;0-1,1-2,2-2;0,5,2,3")
    for k in range(1, 11):
        g = generate_trees(k)
        if len(g) != A000055[k]:
            print("regen n=%d got %d want %d" % (k, len(g), A000055[k]))
            fails += 1
    if fails:
        print("selftest_failures=%d" % fails)
        print("FAIL")
        return 1
    print("selftest_failures=0")
    print("PASS")
    return 0

def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--expect", type=int, default=None)
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.file:
        print("usage: check_og.py [--n N] [--expect K] [--regen] FILE")
        return 2
    return check_file(a.file, a.n, a.expect, a.regen)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
