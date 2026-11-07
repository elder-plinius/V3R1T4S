#!/usr/bin/env python3
"""Decision-rule check for A357953(10): Program A (search-engineer/out/A10_r*of32.txt, totF.c) vs Program B
(exact-eval-first/out/B10_r*of32.txt, main.go). Per residue class: graph count, max, histogram of per-graph maxima,
set of (graph6, max) with max >= 150, FNV-1a hash of the per-graph max sequence. Usage: compare_AB.py <Adir> <Bdir>"""
import re, sys
Ad, Bd = sys.argv[1], sys.argv[2]
def load(f):
    t = open(f).read()
    assert re.search(r'^fnv [0-9a-f]+$', t, re.M), f + ' incomplete'
    h = re.search(r'^n=10 mode=neighbours graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+) witness_rule_mask=(\d+) witness_state=(\d+)', t, re.M)
    hist = {int(a): int(b) for a, b in re.findall(r'^hist (\d+) (\d+)$', t, re.M)}
    high = sorted((g, int(v)) for v, g in re.findall(r'^high (\d+) (\S+)$', t, re.M))
    fnv = re.search(r'^fnv ([0-9a-f]+)$', t, re.M).group(1)
    return dict(graphs=int(h.group(1)), max=int(h.group(2)), wit=(h.group(3), int(h.group(4)), int(h.group(5))),
                hist=hist, high=high, fnv=fnv)
totA = totB = 0; MA = MB = 0; bad = 0; HA = {}; nh = 0; wits = []
for r in range(32):
    a = load(f'{Ad}/A10_r{r}of32.txt'); b = load(f'{Bd}/B10_r{r}of32.txt')
    same = a['graphs'] == b['graphs'] and a['max'] == b['max'] and a['hist'] == b['hist'] and a['high'] == b['high'] and a['fnv'] == b['fnv']
    assert sum(a['hist'].values()) == a['graphs']
    print(f"r{r:2d}/32 graphs A {a['graphs']} B {b['graphs']} max A {a['max']} B {b['max']} high {len(a['high'])}/{len(b['high'])} fnv {a['fnv']}/{b['fnv']} {'SAME' if same else 'DIFF'}")
    bad += not same; totA += a['graphs']; totB += b['graphs']; MA = max(MA, a['max']); MB = max(MB, b['max']); nh += len(a['high'])
    for k, v in a['hist'].items(): HA[k] = HA.get(k, 0) + v
    wits.append((a['max'], r, 'A', a['wit'])); wits.append((b['max'], r, 'B', b['wit']))
print('total graphs A', totA, 'B', totB, '== A001349(10) 11716571:', totA == totB == 11716571)
print('max A', MA, 'max B', MB, '| residue classes differing:', bad, '| graphs with max >= 150:', nh)
top = sorted(HA.items())[-12:]; print('top of combined histogram (value count):', ' '.join(f'{k}:{v}' for k, v in top))
for w in sorted(wits, reverse=True)[:6]: print('witness', w)
ok = bad == 0 and totA == totB == 11716571 and MA == MB
print('VERDICT', 'AGREE' if ok else 'DISAGREE', 'M =', MA if ok else None)
