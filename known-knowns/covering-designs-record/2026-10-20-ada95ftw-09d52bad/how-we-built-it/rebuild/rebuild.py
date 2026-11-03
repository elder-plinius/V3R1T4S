#!/usr/bin/env python3
"""Optional rebuild (needs numpy + ortools): PSL(2,7) acting on the disjoint union of its coset spaces of degree 24
(H = Z7) and 14 (H = A4, either class) = 38 points; exact orbit set cover of all 3-subsets by 6-subset orbits (SCIP).
One of the two 24+14 G-sets gives an optimal orbit cover with 469 blocks. Writes rebuilt_<n>.txt."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsets, kmcover
order, acts = gsets.actions('PSL27', gsets.all_groups()['PSL27'], 40)
for combo in itertools.product(range(len(acts)), repeat=2):
    if [acts[i][0] for i in combo] != [24, 14]: continue
    perms = [[] for _ in acts[0][2]]; off = 0
    for i in combo:
        d, h, pa = acts[i]
        for j, p in enumerate(pa): perms[j] += [x + off for x in p]
        off += d
    r = kmcover.solve_mip(perms, 38, 6, 3, cap=120, threads=1)
    print('G-set', [(acts[i][0], acts[i][1]) for i in combo], r['status'], 'blocks', r.get('best'), 'bound', r.get('bound'),
          'valid', kmcover.check(r['blocks'], 38, 6, 3) if 'blocks' in r else None, flush=True)
    if r.get('best'):
        open(f"rebuilt_{r['best']}.txt", 'w').write('\n'.join(' '.join(map(str, b)) for b in r['blocks']) + '\n')
