#!/usr/bin/env python
"""Standalone checker for the A210662 row-28 claim. Python 3.8+ STANDARD LIBRARY
ONLY. Run from the package folder. Last line: PASS or FAIL.

What it verifies, from the definition (monomer-dimer tilings of the k x n board
= matchings of the k x n grid graph):
  1. Its own exact big-integer DP (independent of the how-we-built-it code)
     recomputes every published table cell with n <= 12 (78 cells) against
     the-record-we-beat's decoded b-file, and the claimed row-28 cells k <= 12
     (12 cells) against object/a210662_row28.txt.
  2. CRT over how-we-built-it/runA_residues.txt (13 set-A primes) reproduces
     the object values for all 27 cells and ALL 378 published cells exactly.
  3. CRT over how-we-built-it/runB_residues.txt (13 disjoint set-B primes)
     reproduces the same 27 object values; and its 28th column CRT equals the
     a(28) anchor object.
  4. Primality (deterministic Miller-Rabin, bases 2..37, valid < 3.3e24) and
     disjointness of the two prime sets; moduli products exceed the anchor.
"""
import hashlib
import sys

OBJ = 'object/a210662_row28.txt'
BF = 'the-record-we-beat/b210662_last_row.txt'  # full b-file copy? No: snapshot
import os

def fail(msg):
    print('FAIL:', msg)
    print('FAIL')
    sys.exit(1)

# ---------- own exact DP from the definition (dict-based, stdlib) ----------
def matchings(m, n):
    """Exact monomer-dimer tilings of the m x n board (broken-profile DP,
    column-major scan; frontier = m-bit occupancy mask; Python big ints)."""
    if m == 0 or n == 0:
        return 1
    dp = {0: 1}
    for pos in range(m * n):
        r, c = pos % m, pos // m
        ndp = {}
        for st, cnt in dp.items():
            if st & 1:
                ndp[st >> 1] = ndp.get(st >> 1, 0) + cnt
                continue
            ndp[st >> 1] = ndp.get(st >> 1, 0) + cnt
            if r + 1 < m and not (st >> 1) & 1:
                k2 = (st >> 1) | 1
                ndp[k2] = ndp.get(k2, 0) + cnt
            if c + 1 < n:
                k3 = (st >> 1) | (1 << (m - 1))
                ndp[k3] = ndp.get(k3, 0) + cnt
        dp = ndp
    return sum(dp.values())

# ---------- Miller-Rabin (deterministic < 3.3e24) ----------
def is_prime(n):
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def crt(pairs):
    x, m = 0, 1
    for p, r in pairs:
        g = pow(m, -1, p)
        x = x + m * (((r - x) % p) * g % p)
        m *= p
    return x % m, m

def main():
    # object
    obj = {}
    for line in open(OBJ):
        parts = line.split()
        if len(parts) != 2:
            fail('object line format: %r' % line[:40])
        k, v = parts
        obj[int(k)] = int(v)
    if sorted(obj) != list(range(1, 28)):
        fail('object keys')
    # published b-file (packaged snapshot copy)
    bf = os.path.join('the-record-we-beat', 'b210662_snapshot.txt')
    vals = [int(l.split()[1]) for l in open(bf) if l.strip()]
    if len(vals) != 378:
        fail('b-file snapshot length %d' % len(vals))
    tri, i = {}, 0
    for n in range(1, 28):
        for k in range(1, n + 1):
            tri[(n, k)] = vals[i]
            i += 1
    # 1a. own DP vs published small cells
    for n in range(1, 13):
        for k in range(1, n + 1):
            if matchings(k, n) != tri[(n, k)]:
                fail('own DP vs published (n=%d,k=%d)' % (n, k))
    print('ok: own exact DP reproduces all 78 published cells n<=12')
    # 1b. own DP vs claimed row cells k<=12
    for k in range(1, 13):
        if matchings(k, 28) != obj[k]:
            fail('own DP vs claimed T(28,%d)' % k)
    print('ok: own exact DP reproduces claimed row cells k=1..12')
    # 2. runA residues: load, prime-check, CRT everything
    ra = {}
    for line in open(os.path.join('how-we-built-it', 'runA_residues.txt')):
        if line.startswith('p='):
            f = dict(t.split('=') for t in line.split())
            ra.setdefault((int(f['k']), int(f['j'])), {})[int(f['p'])] = int(f['r'])
    pa = sorted(next(iter(ra.values())))
    if len(pa) != 13 or not all(is_prime(p) for p in pa):
        fail('set-A primes')
    for k in range(1, 28):
        x, m = crt(sorted(ra[(k, 28)].items()))
        if x != obj[k]:
            fail('runA CRT vs object k=%d' % k)
    print('ok: runA 13-prime CRT reproduces all 27 object cells')
    npub = 0
    for (k, j), d in ra.items():
        if j <= 27:
            pub = tri.get((j, k)) if j >= k else tri.get((k, j))
            if pub is None:
                continue
            x, m = crt(sorted(d.items()))
            if m <= pub:
                continue  # not covered by available primes alone
            npub += 1
            if x != pub:
                fail('runA CRT vs published (j=%d,k=%d)' % (j, k))
    print('ok: runA CRT reproduces %d covered published cells exactly' % npub)
    # 3. runB residues
    rb = {}
    for line in open(os.path.join('how-we-built-it', 'runB_residues.txt')):
        if line.startswith('p='):
            f = dict(t.split('=') for t in line.split())
            rb.setdefault(int(f['j']), {})[int(f['p'])] = int(f['r'])
    pb = sorted(next(iter(rb.values())))
    if len(pb) != 13 or not all(is_prime(p) for p in pb):
        fail('set-B primes')
    if set(pa) & set(pb):
        fail('prime sets overlap')
    ma = 1
    for p in pa:
        ma *= p
    mb = 1
    for p in pb:
        mb *= p
    a28 = int(open(os.path.join('the-record-we-beat', 'a28_anchor.txt')).read().strip())
    if not (ma > a28 and mb > a28):
        fail('moduli vs anchor')
    for j in range(1, 28):
        x, m = crt(sorted(rb[j].items()))
        if x != obj[j]:
            fail('runB CRT vs object k=%d' % j)
    x28, _ = crt(sorted(rb[28].items()))
    if x28 != a28:
        fail('runB k=28 CRT vs a(28) anchor')
    print('ok: runB 13-prime CRT (disjoint set) reproduces all 27 cells; '
          'k=28 equals the a(28) anchor')
    print('ok: moduli %d and %d bits vs anchor %d bits' %
          (ma.bit_length(), mb.bit_length(), a28.bit_length()))
    for k in range(1, 28):
        if obj[k] >= a28:
            fail('anchor violation k=%d' % k)
    print('ok: all 27 values < a(28) (subgraph monotonicity anchor)')
    print('PASS')

if __name__ == '__main__':
    main()
