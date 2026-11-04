#!/usr/bin/env python3
"""check_graceful_cubic.py: standard-library checker for graceful-labeling certificates of connected cubic graphs.

Usage: python3 check_graceful_cubic.py n CERT      (CERT may be plain text or .gz)

Written from the definitions, without nauty. A certificate for order n (n even) has one line per graph:
    <graph6> f(0) f(1) ... f(n-1)
For every line it checks:
  1. graph6 decodes strictly: first byte 63+n, exact length, bytes in 63..126, zero padding bits;
  2. simple graph on n vertices, every degree exactly 3 (so q = 3n/2 edges), connected;
  3. exactly n labels, decimal integers, pairwise distinct, all in [0, q];
  4. the q edge differences |f(u)-f(v)| are exactly {1, 2, ..., q}, each once (a graceful labeling).
Completeness: every line gets an exact canonical form, computed here by colour refinement (seeded with per-vertex
distance profiles) plus individualisation over the whole search tree, keeping the lexicographically least relabelled
edge list. Two graphs get the same form if and only if they are isomorphic. The checker requires
  number of lines = number of distinct canonical forms = A002851(n/2) (connected cubic graphs on n vertices, OEIS).
Since every line is a connected cubic graph on n vertices and no two are isomorphic, A002851 distinct lines means
every isomorphism class occurs exactly once. Prints one summary line ending in PASS or FAIL; exit status 0 or 1.
"""
import gzip, sys
from multiprocessing import Pool

# OEIS A002851: number of connected cubic (trivalent) graphs with 2k vertices, k = 2..11.
A002851 = {4: 1, 6: 2, 8: 5, 10: 19, 12: 85, 14: 509, 16: 4060, 18: 41301, 20: 510489, 22: 7319447}


def decode_graph6(s, n):
    if len(s) < 1 or ord(s[0]) - 63 != n:
        raise ValueError("graph6 vertex count is not %d" % n)
    m = n * (n - 1) // 2
    nch = (m + 5) // 6
    if len(s) != 1 + nch:
        raise ValueError("graph6 length")
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        if v < 0 or v > 63:
            raise ValueError("graph6 byte out of range")
        for b in range(5, -1, -1):
            bits.append((v >> b) & 1)
    if any(bits[m:]):
        raise ValueError("graph6 padding bits not zero")
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return edges


def refine(nb, col):
    """Equitable refinement of colouring col (list of ints). Returns canonical ranks."""
    n = len(nb)
    k = len(set(col))
    while True:
        sig = [(col[v],) + tuple(sorted(col[w] for w in nb[v])) for v in range(n)]
        r = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [r[s] for s in sig]
        if len(r) == k:
            return new
        col, k = new, len(r)


def canon(n, edges, nb):
    # isomorphism-invariant seed colours: distance profile of each vertex (bitset BFS)
    adj = [0] * n
    for v in range(n):
        for w in nb[v]:
            adj[v] |= 1 << w
    reach = [1 << v for v in range(n)]
    prof = [[] for _ in range(n)]
    while True:
        new = [reach[v] | reach[nb[v][0]] | reach[nb[v][1]] | reach[nb[v][2]] for v in range(n)]
        if new == reach:
            break
        for v in range(n):
            prof[v].append(bin(new[v]).count("1"))
        reach = new
    full = (1 << n) - 1
    connected = reach[0] == full
    seed = [tuple(p) for p in prof]
    r = {s: i for i, s in enumerate(sorted(set(seed)))}
    col = refine(nb, [r[s] for s in seed])
    best = [None]

    def search(col):
        cells = {}
        for v, c in enumerate(col):
            cells.setdefault(c, []).append(v)
        if len(cells) == n:
            code = bytes(x for e in sorted((col[a], col[b]) if col[a] < col[b] else (col[b], col[a])
                                           for a, b in edges) for x in e)
            if best[0] is None or code < best[0]:
                best[0] = code
            return
        # target cell: smallest non-singleton cell, ties broken by colour (both invariant)
        c0 = min((len(vs), c) for c, vs in cells.items() if len(vs) > 1)[1]
        for v in cells[c0]:
            ind = [2 * c for c in col]
            ind[v] += 1
            search(refine(nb, ind))

    search(col)
    return connected, best[0]


def check_lines(args):
    n, start, lines = args
    q = 3 * n // 2
    want = set(range(1, q + 1))
    errs = []
    forms = []
    for i, line in enumerate(lines):
        ln = start + i
        p = line.split()
        try:
            if len(p) != n + 1:
                raise ValueError("expected graph6 plus %d labels, got %d tokens" % (n, len(p)))
            edges = decode_graph6(p[0], n)
            nb = [[] for _ in range(n)]
            for a, b in edges:
                nb[a].append(b)
                nb[b].append(a)
            if any(len(x) != 3 for x in nb):
                raise ValueError("not cubic")
            if not all(t.isdigit() and t.isascii() for t in p[1:]):
                raise ValueError("labels are not plain non-negative integers")
            f = [int(t) for t in p[1:]]
            if len(set(f)) != n:
                raise ValueError("labels not distinct")
            if min(f) < 0 or max(f) > q:
                raise ValueError("label outside [0, %d]" % q)
            d = [abs(f[a] - f[b]) for a, b in edges]
            if len(d) != q or set(d) != want:
                raise ValueError("edge differences are not exactly {1, ..., %d}" % q)
            connected, form = canon(n, edges, nb)
            if not connected:
                raise ValueError("graph not connected")
            forms.append((form, ln))
        except ValueError as e:
            errs.append("line %d: %s" % (ln, e))
    return errs, forms


def chunks(fh, n, size=2000):
    block, start, ln = [], 1, 0
    for raw in fh:
        ln += 1
        block.append(raw.rstrip("\r\n"))
        if len(block) == size:
            yield (n, start, block)
            block, start = [], ln + 1
    if block:
        yield (n, start, block)


def main():
    n = int(sys.argv[1])
    path = sys.argv[2]
    if n not in A002851:
        print("order %d: no A002851 value in this checker FAIL" % n)
        sys.exit(1)
    opener = gzip.open if path.endswith(".gz") else open
    errs, bad, total, dups = [], 0, 0, 0
    seen = {}
    with opener(path, "rt", encoding="ascii", newline="") as fh, Pool() as pool:
        for e, forms in pool.imap(check_lines, chunks(fh, n)):
            bad += len(e)
            errs.extend(e[:10])
            total += len(e) + len(forms)
            for form, ln in forms:
                if form in seen:
                    dups += 1
                    if dups <= 5:
                        errs.append("line %d: graph isomorphic to line %d (duplicate)" % (ln, seen[form]))
                else:
                    seen[form] = ln
    want = A002851[n]
    for e in errs[:10]:
        print("order %d: %s" % (n, e))
    ok = bad == 0 and dups == 0 and total == len(seen) == want
    print("order %d: %d lines, %d bad lines, %d duplicates, %d pairwise non-isomorphic gracefully labelled connected "
          "cubic graphs, A002851 = %d %s" % (n, total, bad, dups, len(seen), want, "PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
