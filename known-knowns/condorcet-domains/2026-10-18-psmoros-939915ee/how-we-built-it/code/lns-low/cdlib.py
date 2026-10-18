"""cdlib.py -- never-condition assignments, gluing constructions and the exact counter (glue-constructor lens).

Assignment = numpy uint8 array over triples a<b<c (0-based) in colex order idx = C(c,3)+C(b,2)+a, value 3*s+p:
s = subject (0: a, 1: b, 2: c), p = forbidden position of the subject in the triple (0 top, 1 middle, 2 bottom).
Paper notation iNj <=> s=i-1, p=j-1. Labels are 0-based here, 1-based in order files.
"""
import ctypes
import os
from itertools import combinations
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_lib = ctypes.CDLL(os.path.join(HERE, "libcdcount.so"))
_lib.cd_count.restype = ctypes.c_longlong
_lib.cd_count.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_longlong)]
_lib.cd_enum.restype = ctypes.c_longlong
_lib.cd_enum.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]


def tidx(a, b, c):
    a, b, c = sorted((a, b, c))
    return comb(c, 3) + comb(b, 2) + a


def ntrip(n):
    return comb(n, 3)


def count(n, cond, states=False):
    buf = np.ascontiguousarray(cond[:ntrip(n)], dtype=np.uint8).tobytes()
    ns = ctypes.c_longlong(0)
    r = _lib.cd_count(n, buf, ctypes.byref(ns))
    return (r, ns.value) if states else r


def enum(n, cond, path):
    buf = np.ascontiguousarray(cond[:ntrip(n)], dtype=np.uint8).tobytes()
    return _lib.cd_enum(n, buf, path.encode())


def set_cond(cond, subj, others, p):
    """Set never condition: alternative subj never at position p (0 top,1 mid,2 bottom) in triple {subj}+others."""
    t = sorted((subj,) + tuple(others))
    cond[tidx(*t)] = 3 * t.index(subj) + p


def get_cond(cond, a, b, c):
    t = sorted((a, b, c))
    code = int(cond[tidx(*t)])
    return t[code // 3], code % 3


def fishburn(n, flip=False):
    """Paper (2601.07336) convention: middle element b (1-based label b+1) even -> 2N1 (b never top), else 2N3."""
    cond = np.zeros(ntrip(n), dtype=np.uint8)
    for a, b, c in combinations(range(n), 3):
        even = (b + 1) % 2 == 0
        if flip:
            even = not even
        cond[tidx(a, b, c)] = 3 * 1 + (0 if even else 2)
    return cond


def relabel(n, cond, perm):
    """New assignment on n alternatives where old alternative x becomes perm[x]."""
    out = np.zeros(ntrip(n), dtype=np.uint8)
    for a, b, c in combinations(range(n), 3):
        code = int(cond[tidx(a, b, c)])
        subj = (a, b, c)[code // 3]
        set_cond(out, perm[subj], (perm[x] for x in (a, b, c) if x != subj), code % 3)
    return out


def dual(n, cond):
    """Reverse every order: never top <-> never bottom, middle stays."""
    out = cond.copy()
    for i in range(ntrip(n)):
        s, p = divmod(int(cond[i]), 3)
        out[i] = 3 * s + (2 - p)
    return out


def embed(n_total, cond_small, n_small, labels):
    """Return dict triple-index -> code for the small assignment placed on the given labels (list, len n_small)."""
    res = {}
    for a, b, c in combinations(range(n_small), 3):
        code = int(cond_small[tidx(a, b, c)])
        subj = (a, b, c)[code // 3]
        t = sorted((labels[a], labels[b], labels[c]))
        res[tidx(*t)] = 3 * t.index(labels[subj]) + code % 3
    return res


def ks_glue(m, cond1, n2, cond2, u, v):
    """Karpov-Slinko concatenation+shuffle (D1 (x)2 D2)(u,v) as a full assignment on m+n2 alternatives.
    D1 on 0..m-1, D2 on m..m+n2-1 (D2 labels shifted). u: order (list, best first) of 0..m-1; v: order of 0..n2-1.
    Mixed {a,b,x}: the u-higher of a,b never last. Mixed {a,x,y}: the v-lower of x,y never first."""
    N = m + n2
    cond = np.zeros(ntrip(N), dtype=np.uint8)
    for k, code in embed(N, cond1, m, list(range(m))).items():
        cond[k] = code
    for k, code in embed(N, cond2, n2, list(range(m, N))).items():
        cond[k] = code
    ru = {x: i for i, x in enumerate(u)}
    rv = {x + m: i for i, x in enumerate(v)}
    for a, b in combinations(range(m), 2):
        hi = a if ru[a] < ru[b] else b
        lo = b if hi == a else a
        for x in range(m, N):
            set_cond(cond, hi, (lo, x), 2)
    for x, y in combinations(range(m, N), 2):
        lo = y if rv[x] < rv[y] else x
        hi = x if lo == y else y
        for a in range(m):
            set_cond(cond, lo, (a, hi), 0)
    return cond


def s1_glue(m, cond1, n2, cond2, A1, B1):
    """Paper (2601.07336) Section 7 construction 1 with A = 0..m-1 before B = m..N-1 on the axis.
    {a1,a2,b}: 1N3 if a1,a2 in A1 else 3N1.  {a,b1,b2}: 3N1 if b1,b2 in B1 else 1N3. (B1 given 0-based in D2)."""
    N = m + n2
    cond = np.zeros(ntrip(N), dtype=np.uint8)
    for k, code in embed(N, cond1, m, list(range(m))).items():
        cond[k] = code
    for k, code in embed(N, cond2, n2, list(range(m, N))).items():
        cond[k] = code
    A1 = set(A1)
    B1 = set(x + m for x in B1)
    for a1, a2 in combinations(range(m), 2):
        for b in range(m, N):
            cond[tidx(a1, a2, b)] = (0 * 3 + 2) if (a1 in A1 and a2 in A1) else (2 * 3 + 0)
    for b1, b2 in combinations(range(m, N), 2):
        for a in range(m):
            cond[tidx(a, b1, b2)] = (2 * 3 + 0) if (b1 in B1 and b2 in B1) else (0 * 3 + 2)
    return cond


def s2_glue(m, cond1, n2, cond2):
    """Paper construction 2: 2N3 on every mixed triple (axis A before B)."""
    N = m + n2
    cond = np.zeros(ntrip(N), dtype=np.uint8)
    for k, code in embed(N, cond1, m, list(range(m))).items():
        cond[k] = code
    for k, code in embed(N, cond2, n2, list(range(m, N))).items():
        cond[k] = code
    for a, b, c in combinations(range(N), 3):
        if (c < m) or (a >= m):
            continue
        cond[tidx(a, b, c)] = 1 * 3 + 2
    return cond


def replace_glue(m, cond1, z, n2, cond2):
    """Fishburn replacement: alternative z of D1 (on m alts) is replaced by the block D2 (n2 alts).
    Result on m+n2-1 alternatives: D1's others keep labels order-preserved around the block.
    Triples with 2 or 3 block members: block-internal from D2 / outsider never middle; one block member: as z."""
    N = m + n2 - 1
    # labels: D1 alternative x<z -> x, x>z -> x+n2-1 ; block member j -> z+j
    lab1 = [x if x < z else x + n2 - 1 for x in range(m)]
    blk = [z + j for j in range(n2)]
    cond = np.zeros(ntrip(N), dtype=np.uint8)
    for k, code in embed(N, cond2, n2, blk).items():
        cond[k] = code
    others = [x for x in range(m) if x != z]
    for a, b, c in combinations(range(m), 3):
        code = int(cond1[tidx(a, b, c)])
        subj = (a, b, c)[code // 3]
        tri = (a, b, c)
        if z not in tri:
            set_cond(cond, lab1[subj], tuple(lab1[x] for x in tri if x != subj), code % 3)
        else:
            for bm in blk:
                mp = {x: (bm if x == z else lab1[x]) for x in tri}
                set_cond(cond, mp[subj], tuple(mp[x] for x in tri if x != subj), code % 3)
    for x in others:
        for b1, b2 in combinations(blk, 2):
            set_cond(cond, lab1[x], (b1, b2), 1)
    return cond


def from_orders(orders):
    """Assignment satisfied by a copious domain given as list of 0-based tuples (first unused never condition)."""
    n = len(orders[0])
    pos = np.array([[0] * n for _ in orders])
    for r, o in enumerate(orders):
        for i, x in enumerate(o):
            pos[r, x] = i
    cond = np.zeros(ntrip(n), dtype=np.uint8)
    for a, b, c in combinations(range(n), 3):
        pa, pb, pc = pos[:, a], pos[:, b], pos[:, c]
        ra = (pb < pa).astype(int) + (pc < pa)
        rb = (pa < pb).astype(int) + (pc < pb)
        rc = (pa < pc).astype(int) + (pb < pc)
        found = None
        for s, r in enumerate((ra, rb, rc)):
            for p in range(3):
                if not np.any(r == p):
                    found = 3 * s + p
                    break
            if found is not None:
                break
        if found is None:
            raise ValueError("not a CD at triple %s" % ((a, b, c),))
        cond[tidx(a, b, c)] = found
    return cond


def read_orders(path):
    out = []
    for ln in open(path):
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.append(tuple(int(x) - 1 for x in ln.replace(",", " ").split()))
    return out
