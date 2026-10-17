"""Derived design of a (v,k,t) covering at its minimum-degree point p: the blocks containing p, with p removed,
relabelled to 1..v-1 (points above p shift down by one). Writes the block file and prints the point, degree and
degree spread.
usage: python -I derive_at_point.py design.txt v out.txt"""
import sys
from collections import Counter
design, v, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
B = [list(map(int, l.split())) for l in open(design, encoding='utf-8') if l.strip()]
lo = min(min(b) for b in B)
deg = Counter(p for b in B for p in b)
pts = list(range(lo, lo + v))
p = min(pts, key=lambda x: (deg.get(x, 0), x))
print('blocks', len(B), 'points', lo, '..', lo + v - 1, 'min-degree point', p, 'degree', deg[p],
      'degree range', min(deg[x] for x in pts), max(deg[x] for x in pts))
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    for b in B:
        if p in b:
            q = sorted((x if x < p else x - 1) - lo + 1 for x in b if x != p)
            f.write(' '.join(map(str, q)) + '\n')
