"""Stage-3 gate probe (floats, a guide only): coarse-Z^3 box tiling with blocks a x b x c.

Block state eps in {0,1}^B, designated set G(eps) = the largest open component (ties: the one containing the smallest
site index). eta(v, w) = 1 iff the traces of G(v), G(w) on their shared face meet in a mirrored pair (sites facing
each other across the face are Z^3-adjacent). Coarse growth process as in the square-site proof.

Worst case over the parent's posterior: the entry trace T_in of G(b2) must meet U (the mirrored trace of the parent's
G) for some nonempty U; the posterior of eps(b2) is pi conditioned on that, so every nonempty U is checked (depth 0,
valid for every history; mixtures over U are covered by convexity of the dominating set). Root: pi conditioned on
G nonempty, 6 children. Children's eta given eps(b2) are independent with P = r(trace of G(b2) on that face).

usage: python gate.py a b c p q        -> worst max-flow (feasible iff 1) over all entry faces and U, and the root
       python gate.py a b c bisect q   -> smallest p (to 1e-4) where every check passes
"""
import sys
from itertools import product

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack


def setup(a, b, c):
    sites = [(x, y, z) for x in range(a) for y in range(b) for z in range(c)]
    idx = {s: i for i, s in enumerate(sites)}
    nbr = [[idx[(x + dx, y + dy, z + dz)] for dx, dy, dz in
            ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
            if (x + dx, y + dy, z + dz) in idx] for (x, y, z) in sites]
    # faces: (axis, side). face-local index = position of the other two coordinates
    faces = []
    for axis, L in ((0, a), (1, b), (2, c)):
        for side in (0, L - 1):
            loc = {}
            for i, s in enumerate(sites):
                if s[axis] == side:
                    o = tuple(s[k] for k in range(3) if k != axis)
                    loc[i] = o
            keys = sorted(set(loc.values()))
            faces.append({i: keys.index(o) for i, o in loc.items()})
    return sites, nbr, faces


def enumerate_block(a, b, c):
    sites, nbr, faces = setup(a, b, c)
    n = len(sites)
    N = 1 << n
    k = np.zeros(N, np.int8)
    tr = np.zeros((N, 6), np.int32)
    for e in range(N):
        k[e] = bin(e).count("1")
        seen = 0
        best, bestsize = 0, 0
        for s in range(n):
            if (e >> s) & 1 and not (seen >> s) & 1:
                comp, stack = 1 << s, [s]
                seen |= 1 << s
                size = 1
                while stack:
                    v = stack.pop()
                    for u in nbr[v]:
                        if (e >> u) & 1 and not (seen >> u) & 1:
                            seen |= 1 << u
                            comp |= 1 << u
                            size += 1
                            stack.append(u)
                if size > bestsize:
                    best, bestsize = comp, size
        for f, loc in enumerate(faces):
            t = 0
            for i, j in loc.items():
                if (best >> i) & 1:
                    t |= 1 << j
            tr[e, f] = t
    return n, k, tr, faces


OPP = [1, 0, 3, 2, 5, 4]   # the child across face f touches its own face OPP[f]


def dominated(law, q, m):
    """max-flow of a monotone coupling Bernoulli(q)^m <= law (law indexed by bit patterns)."""
    zs = range(1 << m)
    pz = np.array([q ** bin(z).count("1") * (1 - q) ** (m - bin(z).count("1")) for z in zs])
    pairs = [(z, x) for z in zs for x in zs if z & ~x == 0]
    M = len(pairs)
    A1 = coo_matrix((np.ones(M), ([z for z, x in pairs], range(M))), shape=(1 << m, M))
    A2 = coo_matrix((np.ones(M), ([x for z, x in pairs], range(M))), shape=(1 << m, M))
    res = linprog(-np.ones(M), A_ub=vstack([A1, A2]).tocsr(), b_ub=np.concatenate([pz, law]), bounds=(0, None),
                  method="highs")
    return -res.fun


def check(data, p, q, verbose=False):
    n, k, tr, faces = data
    pi = p ** k.astype(float) * (1 - p) ** (n - k.astype(float))
    fsize = [len(set(f.values())) for f in faces]
    # trace laws and r tables (mirror = same face-local index on the opposite face)
    r = []
    for f in range(6):
        g = OPP[f]
        dist = np.bincount(tr[:, g], weights=pi, minlength=1 << fsize[g])
        rf = np.array([dist[[S for S in range(1 << fsize[g]) if S & T]].sum() for T in range(1 << fsize[f])])
        r.append(rf)
    rr = np.stack([r[f][tr[:, f]] for f in range(6)], axis=1)   # N x 6 child success prob per face
    worst = (2.0, None)
    # root
    w = pi * (tr.any(axis=1) | (k > 0) & False)
    gnon = np.array([True] * len(pi))
    gmask = (tr.sum(axis=1) > 0) | np.zeros(len(pi), bool)
    # G nonempty iff the block has an open site (G = largest component)
    gmask = k > 0
    proot = pi[gmask].sum()
    if proot < q:
        worst = (0.0, "root P(G nonempty) %.5f" % proot)
    law = np.zeros(64)
    for x in range(64):
        f = np.ones(len(pi))
        for i in range(6):
            f = f * (rr[:, i] if (x >> i) & 1 else 1 - rr[:, i])
        law[x] = (pi * gmask * f).sum()
    law /= law.sum()
    v = dominated(law, q, 6)
    if v < worst[0]:
        worst = (v, "root")
    for fin in range(6):
        kids = [f for f in range(6) if f != fin]
        laws_T = {}
        Tin = tr[:, fin]
        L = np.zeros((1 << fsize[fin], 32))
        for x in range(32):
            f = np.ones(len(pi))
            for i, face in enumerate(kids):
                f = f * (rr[:, face] if (x >> i) & 1 else 1 - rr[:, face])
            L[:, x] = np.bincount(Tin, weights=pi * f, minlength=1 << fsize[fin])
        for U in range(1, 1 << fsize[fin]):
            sel = [T for T in range(1 << fsize[fin]) if T & U]
            law = L[sel].sum(axis=0)
            if law.sum() <= 0:
                continue
            law = law / law.sum()
            v = dominated(law, q, 5)
            if v < worst[0]:
                worst = (v, "entry face %d U=%s" % (fin, bin(U)))
    return worst


def main():
    a, b, c = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    q = float(sys.argv[5])
    data = enumerate_block(a, b, c)
    if sys.argv[4] == "bisect":
        lo, hi = 0.2, 0.7
        if check(data, hi, q)[0] < 1 - 1e-9:
            print("%dx%dx%d q=%s: fails even at p=%s" % (a, b, c, q, hi))
            return
        while hi - lo > 1e-4:
            mid = (lo + hi) / 2
            if check(data, mid, q)[0] >= 1 - 1e-9:
                hi = mid
            else:
                lo = mid
        print("%dx%dx%d q=%s: all checks pass for p >= %.4f (fails at %.4f: %s)" % (a, b, c, q, hi, lo, check(data, lo, q)[1]))
    else:
        p = float(sys.argv[4])
        v, where = check(data, p, q)
        print("%dx%dx%d p=%s q=%s: worst max-flow %.6f (deficit %.2e) at %s" % (a, b, c, p, q, v, 1 - v, where))


if __name__ == "__main__":
    main()
