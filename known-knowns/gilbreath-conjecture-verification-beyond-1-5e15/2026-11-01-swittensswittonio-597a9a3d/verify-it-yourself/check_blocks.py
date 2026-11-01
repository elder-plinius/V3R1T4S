#!/usr/bin/env python3
"""Standalone checker (Python standard library only), written from the definition.
Usage: python3 check_blocks.py blocks.csv
blocks.csv columns: block,first_prime,depth   (block c owns gap entries [8192c, 8192c+8192), reads 8192+1536 entries)
For every row: regenerate the 9729+ consecutive primes starting at first_prime with an independent bytearray sieve,
recompute the local depth (smallest k>=1 with every owned entry of row k in {0,2}) and compare. Also requires depth < 1536."""
import sys, csv, math
from itertools import compress
M, O = 8192, 1536
NEED = M + O + 1   # primes needed: M+O gaps

def small_primes(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i*i::i] = bytes(len(range(i*i, n + 1, i)))
    return list(compress(range(n + 1), s))

def primes_from(start, count, sp):
    out = []; span = 1 << 20; lo = start
    while len(out) < count:
        hi = lo + span
        seg = bytearray([1]) * span
        for p in sp:
            if p * p >= hi: break
            f = (-lo) % p
            if lo + f == p: f += p
            seg[f::p] = bytes(len(range(f, span, p)))
        out.extend(lo + i for i in compress(range(span), seg))
        lo = hi
    return out[:count]

def depth(primes):
    a = [primes[i+1] - primes[i] for i in range(M + O)]
    k = 1
    while k < O:
        if all(x == 0 or x == 2 for x in a[:M]): return k
        k += 1
        a = [abs(a[i] - a[i+1]) for i in range(len(a) - 1)]
    return None

rows = list(csv.DictReader(open(sys.argv[1])))
need_max = max(int(r['first_prime']) for r in rows) + 1_000_000
sp = small_primes(int(math.isqrt(need_max + 10_000_000)) + 1000)
bad = 0
for r in rows:
    fp = int(r['first_prime'])
    pr = primes_from(fp, NEED, sp)
    ok_first = pr[0] == fp
    d = depth(pr)
    ok = ok_first and d is not None and d == int(r['depth'])
    bad += (not ok)
    print(f"block={r['block']} first_prime={fp} first_is_prime={ok_first} depth_claimed={r['depth']} depth_recomputed={d} ok={ok}")
print('blocks checked', len(rows), 'mismatches', bad)
print('PASS' if bad == 0 and rows else 'FAIL')
