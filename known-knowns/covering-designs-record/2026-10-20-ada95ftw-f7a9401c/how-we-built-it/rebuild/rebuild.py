#!/usr/bin/env python3
"""Optional rebuild (needs numpy + ortools): PSL(2,7) (order 168) acting on the disjoint union of three coset spaces of
degree 14, 14 and 8 (36 points); exact orbit set cover of all 3-subsets by 5-subset orbits (SCIP). Solves the G-set
of the claimed design (812 blocks, OPTIMAL within this G-set). Writes rebuilt_<n>.txt."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsets, kmcover
order, acts = gsets.actions('PSL27', gsets.all_groups()['PSL27'], 40)
# The sampler (seed 1) lists PSL(2,7)'s transitive actions of degree <= 40 deterministically; indices 3 and 4 are the two
# degree-14 actions (point stabiliser of order 12, from the two classes of A4 subgroups) and index 5 is the degree-8
# action (stabiliser of order 21). This is job 680 of the run's job list.
for combo in [(3, 4, 5)]:
    assert order == 168 and [(acts[i][0], acts[i][1]) for i in combo] == [(14, 12), (14, 12), (8, 21)]
    perms = [[] for _ in acts[0][2]]; off = 0
    for i in combo:
        d, h, pa = acts[i]
        for j, p in enumerate(pa): perms[j] += [x + off for x in p]
        off += d
    r = kmcover.solve_mip(perms, 36, 5, 3, cap=120, threads=1)
    print('G-set', [(acts[i][0], acts[i][1]) for i in combo], r['status'], 'blocks', r.get('best'), 'bound', r.get('bound'),
          'valid', kmcover.check(r['blocks'], 36, 5, 3) if 'blocks' in r else None, flush=True)
    if r.get('best'):
        open(f"rebuilt_{r['best']}.txt", 'w').write('\n'.join(' '.join(map(str, b)) for b in r['blocks']) + '\n')
