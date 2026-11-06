#!/usr/bin/env python3
"""Standalone consistency checker (standard library only). Run from the package folder:
   python3 verify-it-yourself/check_consistency.py
Checks the recorded run summary against itself and against recorded primecount values:
 - windows are 0..W-1 with lo = 1500000000000001 + 2*2^30*w, cumulative prime counts add up, no window is missing
 - block count = floor((total_primes - 1536 - 1) / 8192) summed with the stream carry rule, depth histogram sums to the block count
 - max depth in histogram == max over windows == RESULT.json; every depth < 1536 (overlap condition); unclean (row 1280) blocks == 0
 - every recorded primecount check: sieved cumulative count == pi(hi) - pi(1.5e15-1), hi = last odd number of the window
 - every 4096th block first prime is increasing and the block ids are consecutive multiples of 4096, covering the range."""
import csv, glob, json, sys, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'object')
A0, NB = 1_500_000_000_000_001, 1 << 30
M, O = 8192, 1536
res = json.load(open(os.path.join(base, 'RESULT.json')))
rows = []
for f in sorted(glob.glob(os.path.join(base, 'windows_*.csv'))):
    rows += list(csv.DictReader(open(f)))
ok = True
def req(c, msg):
    global ok
    print(('ok:   ' if c else 'FAIL: ') + msg)
    ok = ok and c
req([int(r['w']) for r in rows] == list(range(len(rows))), f"{len(rows)} windows numbered consecutively from 0")
cum = 0; mx = 0; badlo = 0; carry = 0; chunks = 0
for r in rows:
    w = int(r['w'])
    badlo += int(r['lo']) != A0 + 2 * NB * w
    n = int(r['nprimes']); cum += n
    if cum != int(r['cum_primes']): req(False, f"cumulative mismatch at window {w}"); break
    total = carry + n; nch = (total - O - 1) // M; carry = total - nch * M; chunks += nch
    if int(r['chunks_done']) != chunks: req(False, f"chunks_done mismatch at window {w}"); break
    mx = max(mx, int(r['win_max_depth']))
req(badlo == 0, "window start values follow lo = 1500000000000001 + 2*2^30*w")
req(cum == res['total_primes'], f"cumulative primes {cum} == RESULT total_primes")
req(chunks == res['blocks'], f"blocks {chunks} == RESULT blocks (carry rule reproduced)")
hist = {int(r['depth']): int(r['count']) for r in csv.DictReader(open(os.path.join(base, 'depth_histogram.csv')))}
req(sum(hist.values()) == chunks, "depth histogram sums to the number of blocks")
req(max(hist) == mx == res['max_depth'], f"max depth {max(hist)} == max over windows {mx} == RESULT {res['max_depth']}")
req(max(hist) < O and 0xFFFF not in hist, f"every depth < overlap {O} (no flagged block)")
req(res['unclean_row1280_blocks'] == 0, "RESULT: blocks whose owned row-1280 entries are not all in {0,2}: 0")
pc = list(csv.DictReader(open(os.path.join(base, 'primecount_checks.csv'))))
byw = {int(r['w']): int(r['cum_primes']) for r in rows}
good = 0
for r in pc:
    w = int(r['w']); hi = A0 + 2 * NB * w + 2 * NB - 2
    if int(r['hi']) == hi and byw[w] == int(r['sieved']) == int(r['primecount_minus_base']): good += 1
req(good == len(pc) and len(pc) > 0, f"{good}/{len(pc)} recorded primecount checks equal the sieved cumulative counts")
fp = list(csv.DictReader(open(os.path.join(base, 'chunk_first_primes_summary.csv')))) if os.path.exists(os.path.join(base, 'chunk_first_primes_summary.csv')) else []
ids = []; prev = 0
for f in sorted(glob.glob(os.path.join(base, 'block_firstprimes_*.csv'))):
    for r in csv.DictReader(open(f)):
        ids.append(int(r['block'])); v = int(r['first_prime']); d = int(r['depth'])
        if v <= prev or d >= O: ok = False; print('FAIL: order or depth at block', r['block'])
        prev = v
req(ids == [4096 * i for i in range(len(ids))] and len(ids) == (chunks + 4095) // 4096, f"{len(ids)} sampled first primes at blocks 0, 4096, 8192, ... in increasing order")
req(res['last_owned_first_prime_of_stream'] > 1_600_000_000_000_000, "range reaches beyond 1.6e15")
print('PASS' if ok else 'FAIL')
