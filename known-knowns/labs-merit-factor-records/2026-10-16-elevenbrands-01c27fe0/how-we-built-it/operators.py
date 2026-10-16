#!/usr/bin/env python3
"""object-as-data lens: structure of the Table 3 records of arXiv:2607.09688v1 and exhaustive operator scans.
H1 window relations between records (up to reverse / negate / alternate-negate).
H2 end operators: drop 0..2 symbols at each end, then add 0..2 symbols (all signs) at each end.
H3 interior single insertion (every position, both signs) and single deletion (every position).
Search-side energy: numpy int64 correlate; every hit is re-judged by baseline/labs_energy.py."""
import json, itertools, sys
import numpy as np
recs = json.load(open(sys.argv[1]))
base = {r['L']: r['E'] for r in recs}
def E(a):
    c = np.correlate(a, a, 'full')[len(a):]; return int((c.astype(np.int64) ** 2).sum())
def arr(seq): return np.array([1 if ch == '+' else -1 for ch in seq], dtype=np.int64)
def syms(a):
    alt = np.array([(-1) ** i for i in range(len(a))], dtype=np.int64)
    for x in (a, -a, a[::-1], -a[::-1], a * alt, -a * alt, (a * alt)[::-1], -(a * alt)[::-1]): yield x
def tostr(a): return ''.join('+' if v > 0 else '-' for v in a)
# H1
print('== H1 window relations (shorter record appears inside longer one, up to symmetry)')
rel = 0
for A in recs:
    for B in recs:
        d = B['L'] - A['L']
        if 0 < d <= 3:
            sb = B['seq']
            hits = [i for x in syms(arr(A['seq'])) for i in [sb.find(tostr(x))] if i >= 0]
            if hits: rel += 1; print('  L=%d inside L=%d at offset %s' % (A['L'], B['L'], sorted(set(hits))))
print('  relations found:', rel)
# H2 + H3
best = {}; hits = []; ncand = 0
def consider(a, how):
    global ncand
    ncand += 1; L = len(a); e = E(a)
    if L not in best or e < best[L][0]: best[L] = (e, how, tostr(a))
    if L in base and e < base[L]: hits.append((L, e, base[L], how, tostr(a)))
adds = [()] + [(x,) for x in (1, -1)] + list(itertools.product((1, -1), repeat=2))
for r in recs:
    a = arr(r['seq']); L = len(a)
    for dl in range(3):
        for dr in range(3):
            core = a[dl:L - dr]
            for p in adds:
                for q in adds:
                    if dl == dr == 0 and not p and not q: continue
                    consider(np.concatenate([np.array(p, dtype=np.int64), core, np.array(q, dtype=np.int64)]), 'end L%d dl%d dr%d p%s q%s' % (L, dl, dr, p, q))
    for i in range(L + 1):
        for v in (1, -1): consider(np.concatenate([a[:i], np.array([v], dtype=np.int64), a[i:]]), 'ins L%d at %d %+d' % (L, i, v))
    for i in range(L): consider(np.concatenate([a[:i], a[i + 1:]]), 'del L%d at %d' % (L, i))
print('== H2/H3 candidates scanned:', ncand)
print('== Table 3 lengths: best operator candidate vs published record (E)')
for L in sorted(base):
    if L in best: print('  L=%d best_cand_E=%d record_E=%d diff=%+d via %s' % (L, best[L][0], base[L], best[L][0] - base[L], best[L][1]))
print('== candidates strictly below a Table 3 record:', len(hits))
for h in hits: print('  HIT', h[:4])
json.dump({'hits': hits, 'best_nontable': {L: best[L] for L in sorted(best) if L not in base}}, open('operator_scan.json', 'w'))
