#!/usr/bin/env python3
"""Independent checker for OEIS A214570 (Python 3 standard library only).

a(n) = max over rooted trees t with n vertices of c(t), the number of ordered (plane) trees that are
isomorphic, as rooted trees, to t.

Part 1 (pure definition, n <= 10): build every ordered tree on n vertices as nested tuples, map each to its
rooted-tree class (children sorted recursively), count ordered trees per class, take the largest count.
Part 2 (n <= 17): build every rooted tree once as a multiset of smaller rooted trees; the number of distinct
orderings of its children is deg!/prod(mult!) for identical child subtrees, so c(t) = deg!/prod(mult!) * prod c(child).
Self-checks: number of trees = A000081(n), sum of c(t) over all trees = Catalan(n-1) (every ordered tree counted once).

usage: verify_a214570.py VALUE_FILE [NMAX]     (checks a(1..16) = OEIS DATA and a(17) = VALUE_FILE)
       verify_a214570.py --control             (negative control: c(t) = deg! per vertex, no multiplicity division)
"""
import sys
from itertools import combinations_with_replacement, product
from math import factorial, comb
from collections import Counter

DATA = [1, 1, 1, 2, 3, 4, 6, 12, 24, 40, 60, 120, 240, 420, 840, 1680]   # OEIS A214570 a(1..16)
A000081 = [1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973, 87811, 235381, 634847]


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def ordered_trees(n):
    """All ordered trees with n vertices, as nested tuples (a vertex = tuple of its children)."""
    if n == 1:
        return [()]
    return [tuple(f) for f in ordered_forests(n - 1)]


_ff = {}
def ordered_forests(m):
    if m in _ff:
        return _ff[m]
    if m == 0:
        res = [()]
    else:
        res = []
        for s in range(1, m + 1):
            for t in ordered_trees(s):
                for rest in ordered_forests(m - s):
                    res.append((t,) + rest)
    _ff[m] = res
    return res


def canon(t):
    return tuple(sorted(canon(c) for c in t))


def part1(nmax):
    out = []
    for n in range(1, nmax + 1):
        cnt = Counter(canon(t) for t in ordered_trees(n))
        out.append(max(cnt.values()))
    return out


def partitions(m, maxpart):
    """Partitions of m into parts <= maxpart, as lists of (size, multiplicity), sizes decreasing."""
    if m == 0:
        yield []
        return
    for s in range(min(m, maxpart), 0, -1):
        for k in range(m // s, 0, -1):
            for rest in partitions(m - s * k, s - 1):
                yield [(s, k)] + rest


def part2(nmax, control=False):
    """Returns list of (a(n), #trees, sum c, #maximizers) for n = 1..nmax."""
    trees = {1: [1]}           # trees[s] = list of c(t), one entry per rooted tree with s vertices
    res = [(1, 1, 1, 1)]
    for n in range(2, nmax + 1):
        cs = []
        for parts in partitions(n - 1, n - 1):
            deg = sum(k for _, k in parts)
            groups = [list(combinations_with_replacement(range(len(trees[s])), k)) for s, k in parts]
            for choice in product(*groups):
                # c = deg!/prod(mult!) * prod c(child), exact integers
                prodc, den = 1, 1
                for combo, (s, k) in zip(choice, parts):
                    for i in combo:
                        prodc *= trees[s][i]
                    if not control:
                        for mult in Counter(combo).values():
                            den *= factorial(mult)
                cs.append(factorial(deg) * prodc // den)
        trees[n] = cs
        m = max(cs)
        res.append((m, len(cs), sum(cs), cs.count(m)))
    return res


def main():
    args = sys.argv[1:]
    if args and args[0] == "--control":
        r = [x[0] for x in part2(12, control=True)]
        print("control a(1..12):", ",".join(map(str, r)))
        return 0 if r == DATA[:12] else 1          # exit 1 = differs from DATA (expected)
    want = int(open(args[0]).read().strip())
    nmax = int(args[1]) if len(args) > 1 else 17
    ok = True
    p1 = part1(10)
    print("part 1 (nested-tuple definition) a(1..10):", ",".join(map(str, p1)))
    if p1 != DATA[:10]:
        print("part 1 differs from DATA"); ok = False
    r = part2(nmax)
    for n, (m, nt, sc, am) in enumerate(r, 1):
        good = nt == A000081[n - 1] and sc == catalan(n - 1)
        print("%2d %5d trees=%d sum=%d argmax=%d %s" % (n, m, nt, sc, am, "ok" if good else "SELF-CHECK FAILED"))
        ok &= good
    got = [x[0] for x in r]
    if got[:16] != DATA[:min(16, nmax)]:
        print("a(1..16) differs from OEIS DATA"); ok = False
    else:
        print("a(1..%d) equal OEIS DATA" % min(16, nmax))
    if nmax >= 17:
        if got[16] == want:
            print("a(17) = %d equals the object (%d)" % (got[16], want))
        else:
            print("a(17) = %d differs from the object (%d)" % (got[16], want)); ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
