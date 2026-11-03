#!/usr/bin/env python3
"""Optional rebuild (needs numpy + ortools): S5 acting on the disjoint union of coset spaces of degree 20, 10 and 5
(35 points); exact orbit set cover of all 3-subsets by 5-subset orbits (SCIP). Solves the G-set
of the claimed design (713 blocks, OPTIMAL within this G-set). Writes rebuilt_<n>.txt."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsets, kmcover
order, acts = gsets.actions('S5', gsets.all_groups()['S5'], 40)
# S5 has three classes of index-20 subgroups and two of index 10; the sampler (seed 1) lists them deterministically.
# The claimed design is invariant under action indices (7, 10, 13); the other five 20+10+5 G-sets reach only 768-780
# blocks within 120 s.
for combo in [(7, 10, 13)]:
    assert [(acts[i][0], acts[i][1]) for i in combo] == [(20, 6), (10, 12), (5, 24)]
    perms = [[] for _ in acts[0][2]]; off = 0
    for i in combo:
        d, h, pa = acts[i]
        for j, p in enumerate(pa): perms[j] += [x + off for x in p]
        off += d
    r = kmcover.solve_mip(perms, 35, 5, 3, cap=120, threads=1)
    print('G-set', [(acts[i][0], acts[i][1]) for i in combo], r['status'], 'blocks', r.get('best'), 'bound', r.get('bound'),
          'valid', kmcover.check(r['blocks'], 35, 5, 3) if 'blocks' in r else None, flush=True)
    if r.get('best'):
        open(f"rebuilt_{r['best']}.txt", 'w').write('\n'.join(' '.join(map(str, b)) for b in r['blocks']) + '\n')
