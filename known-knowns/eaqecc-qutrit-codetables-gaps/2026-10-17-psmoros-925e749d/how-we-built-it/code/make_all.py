#!/usr/bin/env python3
"""For every row (n,1,c) of the table with T = n-1-c in {1,2,3,4}, n >= 2T and d_lower < n-1 <= d_upper,
build the X-type-radical code with T classes (build_family.build) and write result/S_<n>_1_<n-1>_<c>.txt.
Class sizes: T-1 classes of size 2 (|Y|=2) and one class taking the remaining positions (|Y|=2, rest off Y)."""
import sys, subprocess
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
pass  # eacheck.py sits in this folder
import numpy as np
from build_family import build
from eacheck import nullspace, rank, symp
RUN = __import__('os').environ.get('RUN', '.')  # folder holding data/qutrit_table.tsv
rows = [l.rstrip('\n').split('\t') for l in open(RUN + '/data/qutrit_table.tsv')][1:]
cells = sorted({(int(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4])) for r in rows})
out = []
for (n, k, c, lo, hi) in cells:
    if k != 1: continue
    T = n - 1 - c
    if T not in (1, 2, 3, 4) or n < 2 * T: continue
    if not (lo < n - 1 <= hi): continue
    sizes = [(n - 2 * (T - 1), 2)] + [(2, 2)] * (T - 1)
    nn, TT, C = build(sizes, seed=n * 100 + c)
    S = nullspace((C @ symp(nn)) % 3)
    fn = RUN + '/attempts/small-cases/result/S_%d_1_%d_%d.txt' % (n, n - 1, c)
    with open(fn, 'w') as f:
        f.write('# [[%d,1,%d;%d]]_3 X-type radical construction, class sizes %s ; table row %d-%d\n' % (n, n - 1, c, sizes, lo, hi))
        for row in S:
            f.write(' '.join(map(str, row)) + '\n')
    with open(fn.replace('/S_', '/C_'), 'w') as f:
        f.write('# generators of C = span(S)^perp: first %d rows span R (X-type), last 2 rows u, v\n' % T)
        for row in C:
            f.write(' '.join(map(str, row)) + '\n')
    out.append((n, c, lo, hi, fn))
    print(n, 1, n - 1, c, 'table', lo, hi, fn.split('/')[-1])
