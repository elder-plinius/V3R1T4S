"""Own exact checker for binary constant-weight codes. Usage: python check_cw.py FILE n d w M"""
import sys, numpy as np
f, n, d, w, M = sys.argv[1], *map(int, sys.argv[2:6])
rows = [l.strip() for l in open(f) if l.strip()]
assert all(len(r) == n and set(r) <= {'0', '1'} for r in rows), 'bad row'
assert len(rows) == M, ('count', len(rows))
assert len(set(rows)) == M, 'duplicates'
assert all(r.count('1') == w for r in rows), 'weight'
x = np.array([int(r, 2) for r in rows], dtype=np.uint64)
mind = n
for i in range(M - 1):
    z = x[i] ^ x[i + 1:]
    pc = np.zeros(z.shape, dtype=np.int64)
    for s in range(0, 64, 8):
        pc += np.array([bin(k).count('1') for k in range(256)], dtype=np.int64)[((z >> np.uint64(s)) & np.uint64(255)).astype(np.int64)]
    m = int(pc.min()); mind = min(mind, m)
    if m < d:
        print('FAIL distance', i, m); sys.exit(1)
print(f'{f.split("/")[-1]}: M={M} n={n} w={w} min distance {mind} >= {d} PASS')
