#!/usr/bin/env python3
"""Rebuild the candidate seed, record its templates, and brute-force template closure for m = 0..MMAX concretely."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from rle_check import find_and_prove, expand, ra, is_pal
specf, idx, inter, N, MMAX, tag = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
lines = [l.split('#')[0].split() for l in open(specf) if l.strip()]
v = list(map(int, lines[idx])); b, p, a = v[0], v[1], v[2]
L = v[3:3 + a]; R = v[3 + a:3 + 2 * a]; lb, rb = v[3 + 2 * a], v[4 + 2 * a]
I = [int(x) for x in inter.strip('.').split('.')] if inter.strip('.') else []
seed = L + [lb] * N + I + [rb] * N + R[::-1]
r = find_and_prove(b, seed, tmax=300, pmax=12)
T = r['templates']
bad = 0
for m in range(MMAX + 1):
    for i in range(p):
        x = expand(T[i], m); y = ra(x, b)
        z = expand(T[i + 1], m) if i + 1 < p else expand(T[0], m + 1)
        if y != z or is_pal(x):
            bad += 1; print('FAIL m', m, 'i', i)
out = dict(base=b, seed_digits_msb_first=seed, seed_len=len(seed), t0=r['t0'], p=p, M0=r['M0'], status=r['status'],
           templates=T, brute_closure_m_max=MMAX, brute_failures=bad)
json.dump(out, open(os.path.join(os.environ.get('JOB_OUT', '.'), 'candidate-%s.json' % tag), 'w'), indent=1)
print(tag, 'base', b, 'status', r['status'], 't0', r['t0'], 'p', p, 'seed_len', len(seed), 'brute m<=%d failures' % MMAX, bad)
for i, t in enumerate(T):
    print(' T%d' % i, ' '.join('%d^(%d+%dm)' % (d, a_, k) if k else ('%d^%d' % (d, a_) if a_ > 1 else '%d' % d) for d, (a_, k) in t))
