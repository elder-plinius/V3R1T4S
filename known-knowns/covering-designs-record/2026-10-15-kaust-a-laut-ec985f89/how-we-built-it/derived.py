"""R7 derived designs: in a (v,k,t) covering, the blocks through a point p, with p removed, form a (v-1,k-1,t-1)
covering. So C(v-1,k-1,t-1) <= min over p of deg(p). Also R8: the blocks through a fixed pair {p,q}, minus p and q,
form a (v-2,k-2,t-2) covering when t >= 4 (t-2 >= 2), so C(v-2,k-2,t-2) <= min pair degree.
Runs over every published design in the LJCR Zenodo v1.2 covers.json (via the byte index) and compares with live.
usage: python -I derived.py covers.json index.tsv merged_table.csv out.csv"""
import csv, re, sys
from collections import Counter
from itertools import combinations
covers, index, table, out = sys.argv[1:5]
live = {}
for r in csv.DictReader(open(table, encoding='utf-8')):
    live[(int(r['v']), int(r['k']), int(r['t']))] = int(r['cr'])
rows = []; n = 0
with open(covers, 'rb') as f:
    for line in open(index, encoding='utf-8'):
        name, off, ln, nb = line.rstrip('\n').split('\t')
        v, k, t = map(int, re.findall(r'\d+', name))
        f.seek(int(off)); raw = f.read(int(ln)).decode()
        B = [list(map(int, x.split(','))) for x in re.findall(r'\[([\d,\s]+)\]', raw)]
        n += 1
        deg = Counter(p for b in B for p in b)
        md = min(deg.get(p, 0) for p in range(min(min(b) for b in B), min(min(b) for b in B) + v))
        cell = (v - 1, k - 1, t - 1)
        if t - 1 >= 2 and cell in live:
            rows.append((cell, md, live[cell], 'R7 derived of %s (%d blocks)' % (name, len(B))))
        if t >= 4 and len(B) <= 3000 and k <= 25:
            pc = Counter(pq for b in B for pq in combinations(sorted(b), 2))
            npairs = v * (v - 1) // 2
            mp = 0 if len(pc) < npairs else min(pc.values())
            cell2 = (v - 2, k - 2, t - 2)
            if cell2 in live:
                rows.append((cell2, mp, live[cell2], 'R8 pair-derived of %s' % name))
beats = [r for r in rows if r[1] < r[2]]
ties = [r for r in rows if r[1] == r[2]]
with open(out, 'w', encoding='utf-8', newline='') as g:
    w = csv.writer(g, lineterminator='\n'); w.writerow(['v', 'k', 't', 'bound', 'live', 'via'])
    for c, b, L, how in sorted(beats): w.writerow([*c, b, L, how])
print('designs read', n, ' bounds computed', len(rows), ' beats live', len(beats), ' ties', len(ties))
for r in sorted(beats)[:20]: print('BEAT', r)
for r in ties[:5]: print('tie', r)
