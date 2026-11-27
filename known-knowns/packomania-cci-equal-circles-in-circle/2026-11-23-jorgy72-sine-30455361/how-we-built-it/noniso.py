#!/usr/bin/env python3
"""Non-isometry check: compare sorted pairwise-distance multisets of the
candidate vs the posted seed, at double precision with a 1e-9 tolerance,
plus a coarse structural check (max |c| and nearest-pair stats)."""
import numpy as np, sys

def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) >= 3 and p[0].isdigit():
                pts.append((float(p[1]), float(p[2])))
    return np.array(pts)

def multiset(P):
    n = len(P)
    ds = []
    bs = 700
    for i0 in range(0, n, bs):
        A = P[i0:i0+bs]
        D = np.linalg.norm(A[:, None, :] - P[None, :, :], axis=2)
        for k, i in enumerate(range(i0, min(i0+bs, n))):
            row = D[k, i+1:]
            ds.append(row)
    d = np.concatenate(ds)
    d.sort()
    return d

cand = load(sys.argv[1])
seed = load(sys.argv[2])
print('cand N=%d seed N=%d' % (len(cand), len(seed)))
dc = multiset(cand)
ds = multiset(seed)
print('pairs:', len(dc), len(ds))
diff = np.abs(dc - ds)
print('max |diff| over sorted multisets: %.3e' % diff.max())
print('fraction differing by >1e-9: %.4f' % float((diff > 1e-9).mean()))
print('fraction differing by >1e-6: %.4f' % float((diff > 1e-6).mean()))
print('cand max|c|=%.15f seed max|c|=%.15f' % (np.linalg.norm(cand, axis=1).max(), np.linalg.norm(seed, axis=1).max()))
# binding terms at double precision
def binding(P):
    n = len(P)
    dmin = np.inf; arg = None
    bs = 700
    for i0 in range(0, n, bs):
        A = P[i0:i0+bs]
        D = np.linalg.norm(A[:, None, :] - P[None, :, :], axis=2)
        for k, i in enumerate(range(i0, min(i0+bs, n))):
            D[k, i] = np.inf
        j = np.unravel_index(np.argmin(D), D.shape)
        if D[j] < dmin:
            dmin = D[j]; arg = (i0 + j[0], j[1])
    rad = np.linalg.norm(P, axis=1)
    imax = int(np.argmax(rad))
    return dmin/2, arg, 1-rad[imax], imax
pc, argc, wc, argw = binding(cand)
print('cand: min pair/2=%.15f at %s ; wall 1-max|c|=%.15f at %d' % (pc, argc, wc, argw))
print('binding term:', 'PAIR' if pc < wc else 'WALL')
