#!/usr/bin/env python3
"""d = n-2 class construction for table rows (n,1,c) with r = n-1-c in {5,6,7,8}, c >= 1, d_lower < n-2 <= d_upper,
skipping rows where result/ already holds a code with d >= n-2. Classes: e=2 -> size 3, Y = {sum 0}; e=1 -> size 2, y=(1,2);
extra positions (n - (r+4)) appended to class 1 (off the support of Y)."""
import sys, glob, re, os
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
pass  # eacheck.py sits in this folder
import numpy as np
from build_family2 import build
from eacheck import nullspace, symp
RUN = __import__('os').environ.get('RUN', '.')  # folder holding data/qutrit_table.tsv
have = {}
for f in glob.glob(RUN + '/attempts/small-cases/result/S_*.txt'):
    n, k, d, c = map(int, re.findall(r'S_(\d+)_(\d+)_(\d+)_(\d+)', f)[0]); have[(n, k, c)] = (d, f)
rows = [l.rstrip('\n').split('\t') for l in open(RUN + '/data/qutrit_table.tsv')][1:]
cells = sorted({(int(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4])) for r in rows})
E = {5: (2, 1, 1, 1), 6: (2, 2, 1, 1), 7: (2, 2, 2, 1), 8: (2, 2, 2, 2)}
for (n, k, c, lo, hi) in cells:
    if k != 1 or c < 1: continue
    r = n - 1 - c
    if r not in E or n < r + 4: continue
    d = n - 2
    if not (lo < d <= hi): continue
    if (n, k, c) in have and have[(n, k, c)][0] >= d: continue
    spec = []
    for t, e in enumerate(E[r]):
        if e == 2: s, ys = 3, [(1, 2, 0), (0, 1, 2)]
        else: s, ys = 2, [(1, 2)]
        if t == 0:
            extra = n - (r + 4); s += extra; ys = [tuple(list(y) + [0] * extra) for y in ys]
        spec.append((s, ys))
    nn, rr, Crows = build(spec, 2, seed=n * 1000 + c)
    C = np.array(Crows, dtype=np.int64) % 3
    S = nullspace((C @ symp(nn)) % 3)
    old = have.get((n, k, c))
    if old: os.remove(old[1])
    fn = RUN + '/attempts/small-cases/result/S_%d_1_%d_%d.txt' % (n, d, c)
    with open(fn, 'w') as f:
        f.write('# [[%d,1,%d;%d]]_3 class construction with <=2 zeros per word, e_t=%s, extra=%d; table %d-%d%s\n' % (n, d, c, E[r], n - r - 4, lo, hi, (' (replaces d=%d file)' % old[0]) if old else ''))
        for row in S: f.write(' '.join(map(str, row)) + '\n')
    with open(fn.replace('/S_', '/C_'), 'w') as f:
        f.write('# generators of C: first %d rows span R (X-type), last 2 rows u, v\n' % rr)
        for row in C: f.write(' '.join(map(str, row)) + '\n')
    print(n, 1, d, c, 'table', lo, hi, 'replaces d=%d' % old[0] if old else 'new cell', flush=True)
