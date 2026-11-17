#!/usr/bin/env python3
"""Lengthened family codes: for every table row (n,1,c), c >= 1, with n >= c+6 (outside the direct family, T = n-1-c >= 5),
take the family code [[n0,1,n0-1;c]] with n0 = c+5 (T = 4 classes, needs n0 >= 8) and lengthen n-n0 times
(new qutrit in state |0>: S' = (S | 0) + Z_new).  Lengthening keeps k, c and d >= n0-1 = c+4.
Writes result/S_<n>_1_<c+4>_<c>.txt when c+4 > d_lower (and c+4 <= d_upper)."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
pass  # eacheck.py sits in this folder
import numpy as np
from build_family import build
from eacheck import nullspace, symp
RUN = __import__('os').environ.get('RUN', '.')  # folder holding data/qutrit_table.tsv
rows = [l.rstrip('\n').split('\t') for l in open(RUN + '/data/qutrit_table.tsv')][1:]
cells = sorted({(int(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4])) for r in rows})
for (n, k, c, lo, hi) in cells:
    if k != 1 or c < 1 or n < c + 6: continue
    n0 = c + 5
    if n0 < 8: continue
    d = n0 - 1
    if not (lo < d <= hi): continue
    sizes = [(n0 - 6, 2), (2, 2), (2, 2), (2, 2)]
    nn, T, C = build(sizes, seed=n0 * 100 + c)
    S0 = nullspace((C @ symp(nn)) % 3)            # 2*n0 columns
    ext = n - n0
    S = np.zeros((S0.shape[0] + ext, 2 * n), dtype=np.int64)
    S[:S0.shape[0], :n0] = S0[:, :n0]             # X part of old positions
    S[:S0.shape[0], n:n + n0] = S0[:, n0:]         # Z part of old positions
    for e in range(ext):
        S[S0.shape[0] + e, n + n0 + e] = 1          # Z on new qutrit n0+e
    fn = RUN + '/attempts/small-cases/result/S_%d_1_%d_%d.txt' % (n, d, c)
    with open(fn, 'w') as f:
        f.write('# [[%d,1,%d;%d]]_3 = family code [[%d,1,%d;%d]] (classes %s) lengthened by %d qutrits in state |0>; table %d-%d\n' % (n, d, c, n0, d, c, sizes, ext, lo, hi))
        for row in S:
            f.write(' '.join(map(str, row)) + '\n')
    print(n, 1, d, c, 'table', lo, hi, fn.split('/')[-1])
