import numpy as np
import mpmath as mp
import os, sys, json

mp.mp.dps = 50


def to_mp(U):
    m, n, N = U.shape
    out = []
    for k in range(N):
        B = [[mp.mpf(repr(float(U[c, v, k]))) for c in range(m)] for v in range(n)]
        out.append(B)
    return out


def orth_mp(B, m, n):
    """Modified Gram-Schmidt on list B of n vectors (each m mpf)."""
    Q = []
    for v in B:
        w = [mp.mpf(x) for x in v]
        for q in Q:
            s = sum(wi * qi for wi, qi in zip(w, q))
            w = [wi - s * qi for wi, qi in zip(w, q)]
        nrm = mp.sqrt(sum(wi * wi for wi in w))
        Q.append([wi / nrm for wi in w])
    return Q


def mindist_mp(subspaces, m, n):
    """Exact min squared chordal distance n - ||Ui^T Uj||_F^2."""
    N = len(subspaces)
    dmin = mp.mpf(n)
    for i in range(N):
        for j in range(i + 1, N):
            s = mp.mpf(0)
            for vi in subspaces[i]:
                for vj in subspaces[j]:
                    t = sum(a * b for a, b in zip(vi, vj))
                    s += t * t
            d = n - s
            if d < dmin:
                dmin = d
    return dmin


def write_cell(path, U, m, n, N, tag=''):
    """Re-orthonormalize in high precision, write cell file."""
    subs = to_mp(U)
    Qs = [orth_mp(B, m, n) for B in subs]
    with open(path, 'w') as f:
        f.write(f'# packing {m}-{n}-{N} {tag}\n')
        for B in Qs:
            for v in B:
                f.write(','.join(mp.nstr(x, 30) for x in v) + '\n')
    return Qs


def verify_cell(path, m, n, N):
    """Parse cell file, compute min chordal distance squared (high precision)."""
    vecs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            vecs.append([mp.mpf(x) for x in line.split(',')])
    assert len(vecs) == n * N, (len(vecs), n * N)
    subs = [vecs[k * n:(k + 1) * n] for k in range(N)]
    # orthonormality check
    err = mp.mpf(0)
    for B in subs:
        for i in range(n):
            for j in range(n):
                s = sum(a * b for a, b in zip(B[i], B[j]))
                tgt = 1 if i == j else 0
                err = max(err, abs(s - tgt))
    d = mindist_mp(subs, m, n)
    return d, err


TABLE = None


def table():
    global TABLE
    if TABLE is None:
        TABLE = {}
        with open('/inputs/grassmannian_2026-11-04.tsv') as fh:
            for line in fh:
                if line.startswith('#') or line.startswith('m\t'):
                    continue
                p = line.rstrip('\n').split('\t')
                if len(p) < 8:
                    p += [''] * (8 - len(p))
                TABLE[(int(p[0]), int(p[1]), int(p[2]))] = dict(
                    val=float(p[3]) if p[3] else None,
                    bnd=float(p[4]) if p[4] else None)
    return TABLE
