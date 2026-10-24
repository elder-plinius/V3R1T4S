#!/usr/bin/env python3
"""Build a torus graph for the extender lens codes (brute.c, fdp.c).

Usage:
  mkgraph.py word WORD W NCELLS        row-word lattice (BRIEF construction) on W columns x (len(WORD)*NCELLS) rows
  mkgraph.py kagome N                  triangular lattice minus sites (x even, y even) on 2N x 2N (kagome, 3N^2 sites)
  mkgraph.py wordR WORD W R            row-word lattice with an explicit number of rows R (R % len(WORD) == 0)
  mkgraph.py kagomeWR W R              kagome (triangular minus (even,even) sites) on W x R, W and R even
  mkgraph.py transpose wordR WORD W R  the same torus with x and y exchanged (rows = old columns)

Row-word construction (BRIEF.md, checker/q9_check.py): vertices (x,y), x = 0..W-1 periodic, y = 0..R-1 periodic.
Every row has edges (x,y)-(x+1,y). Gap y (rows y, y+1) of type S adds (x,y)-(x,y+1); type T adds (x,y)-(x,y+1) and
(x+1,y)-(x,y+1). Gap type of gap y is WORD[y % len(WORD)].

Output (stdout), whitespace separated:
  N E
  then N lines "x y" (vertex coordinates, vertex index = processing order = row-major)
  then E lines "u v dx dy" with u <= v (indices), meaning lift(v) = lift(u) + (dx*W, dy*R) in the covering plane,
  i.e. (dx, dy) counts the signed crossings of the x seam and the y seam.
Multi-edges (small W or R) and self-loops (W = 1 or R = 1) are kept: they are distinct edges of the torus graph.
"""
import sys


def rowword(word, W, R):
    assert R % len(word) == 0
    verts = [(x, y) for y in range(R) for x in range(W)]
    idx = {v: i for i, v in enumerate(verts)}
    edges = []

    def add(x1, y1, x2, y2):
        # endpoints in the covering plane; reduce to torus with seam crossing counts
        a = idx[(x1 % W, y1 % R)]
        b = idx[(x2 % W, y2 % R)]
        # lift(b) - lift(a) in units of periods:
        da = (x1 // W, y1 // R)
        db = (x2 // W, y2 // R)
        dx, dy = db[0] - da[0], db[1] - da[1]
        if a > b:
            a, b, dx, dy = b, a, -dx, -dy
        edges.append((a, b, dx, dy))

    for y in range(R):
        g = word[y % len(word)]
        for x in range(W):
            add(x, y, x + 1, y)
            add(x, y, x, y + 1)
            if g == 'T':
                add(x + 1, y, x, y + 1)
            elif g != 'S':
                raise SystemExit('bad gap letter ' + g)
    return verts, edges


def kagome(n, W=None, R=None):
    """Triangular lattice (word T) on 2n x 2n (or W x R, both even), delete sites with x, y both even."""
    if W is None:
        W = R = 2 * n
    tv, te = rowword('T', W, R)
    keep = [i for i, (x, y) in enumerate(tv) if not (x % 2 == 0 and y % 2 == 0)]
    new = {old: k for k, old in enumerate(keep)}
    verts = [tv[i] for i in keep]
    edges = [(new[a], new[b], dx, dy) for (a, b, dx, dy) in te if a in new and b in new]
    return verts, edges


def dump(verts, edges):
    out = ["%d %d" % (len(verts), len(edges))]
    out += ["%d %d" % v for v in verts]
    out += ["%d %d %d %d" % e for e in edges]
    print("\n".join(out))


def transpose(verts, edges):
    """Swap the roles of x and y (new rows = old columns), re-order vertices row-major in the new coordinates."""
    order = sorted(range(len(verts)), key=lambda i: (verts[i][0], verts[i][1]))
    new = {old: k for k, old in enumerate(order)}
    nv = [(verts[i][1], verts[i][0]) for i in order]
    ne = []
    for (a, b, dx, dy) in edges:
        u, v, ex, ey = new[a], new[b], dy, dx
        if u > v:
            u, v, ex, ey = v, u, -ex, -ey
        ne.append((u, v, ex, ey))
    return nv, ne


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'transpose':
        a = a[1:]
        if a[0] == 'wordR':
            dump(*transpose(*rowword(a[1], int(a[2]), int(a[3]))))
        else:
            raise SystemExit('transpose supports wordR only')
        sys.exit()
    if a[0] == 'word':
        word, W, nc = a[1], int(a[2]), int(a[3])
        dump(*rowword(word, W, len(word) * nc))
    elif a[0] == 'wordR':
        dump(*rowword(a[1], int(a[2]), int(a[3])))
    elif a[0] == 'kagome':
        dump(*kagome(int(a[1])))
    elif a[0] == 'kagomeWR':
        dump(*kagome(0, int(a[1]), int(a[2])))
    else:
        raise SystemExit(__doc__)
