#!/usr/bin/env python3
"""Verify a claim JSON (here object/lychrel_base13.json) with the GIVEN templates (no inference):
 (a) orbit entry: x_0 = seed; x_t = RA^t(seed); x_entry == T_0(0); x_1..x_entry not palindromes;
 (b) closure: RA(T_i(m)) == T_{i+1}(m) (i < p-1), RA(T_{p-1}(m)) == T_0(m+1): symbolically for m >= M0 (exact affine
     run-length simulation, rle_check.sym_ra) and by exact integer digit computation for 0 <= m <= max(M0, 200);
 (c) no T_i(m) is a palindrome: symbolically (run-digit sequence vs its reverse) plus exact check for m <= max(M0, 200)
     and at every m where two mirrored affine run lengths could coincide."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from rle_check import ra, is_pal, expand, sym_ra, normalize, shift, sym_nonpal
c = json.load(open(sys.argv[1]))
b, p, t0 = c['base'], c['period'], c['entry_step']
T = [[(d, (a, k)) for d, a, k in t] for t in c['templates']]
seed = c[[k for k in c if k.startswith('seed_digits')][0]]
ok = True
x = list(seed)
for t in range(1, t0 + 1):
    x = ra(x, b)
    if is_pal(x): ok = False; print('palindrome before entry at', t)
if x != expand(T[0], 0): ok = False; print('entry mismatch')
print('entry:', 'OK' if x == expand(T[0], 0) else 'FAIL', 'at step', t0)
M0 = 0
for i in range(p):
    res, M = sym_ra(T[i], b)
    tgt = normalize(T[i + 1] if i + 1 < p else shift(T[0]))
    _, Mt = sym_ra(tgt, b); M0 = max(M0, M, Mt)
    if res != tgt: ok = False; print('symbolic closure FAILS at template', i)
print('symbolic closure for m >= M0:', 'OK' if ok else 'FAIL', 'M0 =', M0)
lim = max(M0, 200); special = set()
for i in range(p):
    okp, sp = sym_nonpal(T[i])
    if not okp: ok = False; print('template', i, 'palindromic for all large m')
    special |= sp
bad = 0
for m in range(lim + 1):
    for i in range(p):
        xx = expand(T[i], m); yy = ra(xx, b)
        zz = expand(T[i + 1], m) if i + 1 < p else expand(T[0], m + 1)
        if yy != zz or is_pal(xx): bad += 1
for m in special:
    for i in range(p):
        if is_pal(expand(T[i], m)): bad += 1
print('exact closure and non-palindromicity for 0 <= m <= %d (+ special m %s): %s' % (lim, sorted(special), 'OK' if bad == 0 else 'FAIL (%d)' % bad))
ok &= (bad == 0)
print('CLAIM CHECK:', 'PASS' if ok else 'FAIL')
