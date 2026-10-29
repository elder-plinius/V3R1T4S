#!/usr/bin/env python3
"""Standalone checker (Python standard library only) for a 3-colouring of K_N given as a matrix file
('matrix N 3', then N rows of N digits; entry j of row i = colour of edge {i,j}, 0 on the diagonal).

usage: python3 verify_join.py <matrix file> <n_circ>
Claim checked: colour 1 and colour 2 have no triangle, colour 3 has no K_15, so R(3,3,15) >= N + 1.
Method:
  1. The matrix is symmetric, every off-diagonal entry is 1, 2 or 3.
  2. Colours 1 and 2: for every edge {i,j} of colour c, no common colour-c neighbour (exhaustive over all edges).
  3. Colour 3: vertices 0..n_circ-1 must form a circulant (entry (i,j) depends only on (j - i) mod n_circ; checked
     for every pair). Its colour-3 clique number w is found by an exhaustive branch and bound through vertex 0
     (rotations are automorphisms, so every clique moves to one containing 0). The other vertices must have no
     colour-3 edge among themselves (checked), so a colour-3 clique holds at most one of them, and every colour-3
     clique has at most w + 1 vertices. The claim needs w + 1 <= 14. As a tightness witness the checker also
     reports a colour-3 clique of size w + 1 if one exists (an extra vertex adjacent in colour 3 to a w-clique).
Last line: PASS or FAIL."""
import sys


def fail(msg):
    print('FAIL:', msg)
    print('FAIL')
    sys.exit(1)


def max_clique(nb, P):
    best = []

    def order(P):
        out, col, U = [], 0, P
        while U:
            col += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~(1 << v) & ~nb[v]
                U &= ~(1 << v)
                out.append((v, col))
        return out

    def expand(cl, P):
        nonlocal best
        for v, c in reversed(order(P)):
            if len(cl) + c <= len(best):
                return
            cl.append(v)
            Pn = P & nb[v]
            if Pn:
                expand(cl, Pn)
            elif len(cl) > len(best):
                best = list(cl)
            cl.pop()
            P &= ~(1 << v)
    expand([], P)
    return best


def main():
    path, n = sys.argv[1], int(sys.argv[2])
    rows = [l.strip() for l in open(path) if l.strip() and not l.startswith('#')]
    h = rows[0].split()
    if h[0] != 'matrix' or h[2] != '3':
        fail("first line must be 'matrix N 3'")
    N = int(h[1]); M = rows[1:]
    if len(M) != N or any(len(r) != N for r in M):
        fail('matrix is not N x N')
    for i in range(N):
        if M[i][i] != '0':
            fail('diagonal entry %d is not 0' % i)
        for j in range(N):
            if i != j and (M[i][j] not in '123' or M[i][j] != M[j][i]):
                fail('entry (%d,%d) invalid or not symmetric' % (i, j))
    nb = {c: [0] * N for c in '123'}
    for i in range(N):
        for j in range(N):
            if i != j:
                nb[M[i][j]][i] |= 1 << j
    for c in '12':
        for i in range(N):
            x = nb[c][i] >> (i + 1)
            j = i + 1
            while x:
                if x & 1 and nb[c][i] & nb[c][j]:
                    fail('colour %s has a triangle on edge {%d,%d}' % (c, i, j))
                x >>= 1
                j += 1
        print('colour %s: %d edges, no triangle (every edge checked)' % (c, sum(bin(b).count('1') for b in nb[c]) // 2))
    for i in range(n):
        for j in range(n):
            if i != j and M[i][j] != M[0][(j - i) % n]:
                fail('vertices 0..%d are not a circulant at (%d,%d)' % (n - 1, i, j))
    for i in range(n, N):
        for j in range(n, N):
            if i != j and M[i][j] == '3':
                fail('vertices %d and %d (outside the circulant) are joined in colour 3' % (i, j))
    nbc = [b & ((1 << n) - 1) for b in nb['3'][:n]]
    cl = max_clique(nbc, nbc[0])
    w = len(cl) + 1
    clique = [0] + cl
    assert all((nbc[a] >> b) & 1 for a in clique for b in clique if a != b)
    print('colour 3 on vertices 0..%d (circulant, verified): clique number %d (exhaustive through vertex 0)' % (n - 1, w))
    print('vertices %d..%d: no colour-3 edge among them, so a colour-3 clique holds at most one of them' % (n, N - 1))
    ext = [x for x in range(n, N) if all((nb['3'][x] >> v) & 1 for v in clique)]
    print('colour 3 clique number %s %d; witness of size %d: %s' % ('=' if ext else '<=', w + 1, w + 1 if ext else w,
                                                                    clique + ext[:1] if ext else clique))
    if w + 1 > 14:
        fail('colour 3 may contain K_15')
    print('N %d: no K_3 in colour 1, no K_3 in colour 2, no K_15 in colour 3' % N)
    print('proves R(3,3,15) >= %d' % (N + 1))
    print('PASS')


if __name__ == '__main__':
    main()
