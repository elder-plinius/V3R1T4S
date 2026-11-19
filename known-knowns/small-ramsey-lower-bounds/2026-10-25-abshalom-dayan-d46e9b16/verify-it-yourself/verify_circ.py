#!/usr/bin/env python3
"""Standalone checker for a circulant (cyclic) r-colouring of K_N (Python standard library only).

usage: python3 verify_circ.py <colouring file> k_1 k_2 ... k_r
File: lines starting with '#' are ignored; first line "circulant N r"; then r lines "c: d d d ...": the distances of
colour c. Vertices are 0..N-1 and edge {i, j} gets the colour of the distance (j - i) mod N; d and N - d name the same
distance. Every distance 1..N-1 must get exactly one colour.

Claim checked: for every colour c, the graph of colour c has no clique on k_c vertices. Then the colouring proves
R(k_1, ..., k_r) >= N + 1.

Why it is enough to look at cliques through vertex 0: the graph of colour c is the Cayley graph of Z_N with the
symmetric connection set S_c, so x -> x + t is an automorphism for every t, and any clique can be shifted to one that
contains 0. A clique on k vertices containing 0 is 0 plus a (k-1)-clique inside S_c (the neighbours of 0). The search
inside S_c is an exhaustive branch and bound (greedy colouring bound); it prints a witness if it finds a clique, and
the witness is re-checked edge by edge.
Last line: PASS or FAIL.
"""
import sys


def load(path):
    lines = [l.strip() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    head = lines[0].split()
    if head[0] != 'circulant':
        raise SystemExit("FAIL: first line must be 'circulant N r'")
    N, r = int(head[1]), int(head[2])
    colour = [0] * N
    for l in lines[1:1 + r]:
        c, ds = l.split(':', 1)
        c = int(c)
        if not 1 <= c <= r:
            raise SystemExit("FAIL: colour %d out of range" % c)
        for d in (int(x) for x in ds.split()):
            if d % N == 0:
                raise SystemExit("FAIL: distance 0 listed")
            for e in (d % N, (N - d) % N):
                if colour[e] not in (0, c):
                    raise SystemExit("FAIL: distance %d has colours %d and %d" % (e, colour[e], c))
                colour[e] = c
    bad = [d for d in range(1, N) if colour[d] == 0]
    if bad:
        raise SystemExit("FAIL: distances without a colour, e.g. %s" % bad[:5])
    return N, r, colour


def clique_in(N, S, k):
    """Return a list of k vertices of S forming a clique in the Cayley graph Cay(Z_N, S), or None (exhaustive)."""
    verts = sorted(S)
    idx = {v: i for i, v in enumerate(verts)}
    n = len(verts)
    adj = [0] * n
    for i, a in enumerate(verts):
        m = 0
        for j, b in enumerate(verts):
            if i != j and ((b - a) % N) in S:
                m |= 1 << j
        adj[i] = m
    found = []

    def colour_order(P):
        out, col, U = [], 0, P
        while U:
            col += 1
            Q = U
            while Q:
                low = Q & -Q
                v = low.bit_length() - 1
                Q &= ~low
                Q &= ~adj[v]
                U &= ~low
                out.append((v, col))
        return out

    def expand(chosen, P):
        if len(chosen) >= k:
            found.extend(chosen)
            return True
        for v, c in reversed(colour_order(P)):
            if len(chosen) + c < k:
                return False
            if expand(chosen + [v], P & adj[v]):
                return True
            P &= ~(1 << v)
        return False

    if k <= 0:
        return []
    if expand([], (1 << n) - 1):
        return [verts[i] for i in found[:k]]
    return None


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: verify_circ.py <file> k_1 ... k_r")
    path, ks = sys.argv[1], [int(x) for x in sys.argv[2:]]
    N, r, colour = load(path)
    if len(ks) != r:
        raise SystemExit("FAIL: %d colours in the file but %d clique sizes given" % (r, len(ks)))
    ok = True
    for c in range(1, r + 1):
        S = {d for d in range(1, N) if colour[d] == c}
        k = ks[c - 1]
        w = clique_in(N, S, k - 1)
        if w is None:
            print("colour %d: degree %d, no K_%d (no K_%d among the neighbours of 0, exhaustive)" % (c, len(S), k, k - 1))
        else:
            cl = [0] + w
            assert all(colour[(b - a) % N] == c for a in cl for b in cl if a != b)
            print("colour %d: degree %d, K_%d found: %s" % (c, len(S), k, cl))
            ok = False
    print("N %d colours %d forbidden %s" % (N, r, ",".join(map(str, ks))))
    if ok:
        print("proves R(%s) >= %d" % (",".join(map(str, ks)), N + 1))
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)


if __name__ == '__main__':
    main()
