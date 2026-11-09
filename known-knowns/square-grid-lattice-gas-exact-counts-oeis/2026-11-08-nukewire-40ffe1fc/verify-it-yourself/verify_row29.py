#!/usr/bin/env python
"""Standalone checker for the A210662 row-29 claim (k = 12..28). Python 3.8+
STANDARD LIBRARY ONLY. Run from the package folder. Last line: PASS or FAIL.

What it verifies, from the definition (monomer-dimer tilings of the k x n
board = matchings of the k x n grid graph):
  1. its OWN exact big-int DP (independent of the how-we-built-it code)
     recomputes every published table cell with n <= 15 (120 cells) against
     the-record-we-beat's decoded b-file, and the claimed row-29 cells
     k = 12..15 (4 cells) against object/a210662_row29.txt;
  2. CRT over how-we-built-it/runA29_residues.txt (22 set-A29 primes)
     reproduces the object values for all 17 claimed cells and ALL 378
     published cells exactly, per cell only where that cell's 22-prime
     modulus covers the rigorous bound 3^(n*k);
  3. CRT over how-we-built-it/runB29_residues.txt (22 disjoint set-B29
     primes) reproduces the same 17 object values; and the j=28 column
     CRT-equals the row-28 anchor object wherever covered;
  4. primality (deterministic Miller-Rabin, bases 2..37, valid < 3.3e24) and
     disjointness of the two prime sets; per-k moduli exceed 3^(29k).
"""
import sys


def fail(msg):
    print('FAIL:', msg)
    print('FAIL')
    sys.exit(1)


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
        x = x + m * (((r - x) % p) * pow(m, -1, p) % p)
        m *= p
    return x, m


def load_res(path):
    res = {}
    for line in open(path):
        t = line.split()
        if len(t) == 4 and t[0].startswith('p='):
            p, k, j, r = (int(x.split('=')[1]) for x in t)
            res.setdefault((k, j), {})[p] = r
    return res


def main():
    OBJ = 'object/a210662_row29.txt'
    BF = 'the-record-we-beat/b210662_snapshot.txt'
    RA = 'how-we-built-it/runA29_residues.txt'
    RB = 'how-we-built-it/runB29_residues.txt'
    ANC = 'how-we-built-it/a210662_row28_anchor.txt'
    try:
        obj = {}
        for line in open(OBJ):
            t = line.split()
            if len(t) == 2:
                obj[int(t[0])] = int(t[1])
    except FileNotFoundError:
        fail('missing ' + OBJ)
    if sorted(obj) != list(range(12, 29)):
        fail(f'object must hold exactly k=12..28 (got {sorted(obj)})')
    vals = [l.split()[1] for l in open(BF) if l.strip()]
    if len(vals) != 378:
        fail('b-file snapshot must hold 378 terms')
    tri, i = {}, 0
    for n in range(1, 28):
        for k in range(1, n + 1):
            tri[(n, k)] = int(vals[i])
            i += 1
    A, B = load_res(RA), load_res(RB)

    # 1. own DP (published n<=15 = 120 cells; claimed k=12..15 = 4 cells)
    ndp = 0
    for (n, k), v in tri.items():
        if n <= 15:
            if matchings(k, n) != v:
                fail(f'own DP vs published T({n},{k})')
            ndp += 1
    for k in range(12, 16):
        if matchings(k, 29) != obj[k]:
            fail(f'own DP vs claimed T(29,{k})')
    print(f'1. own exact DP: {ndp} published cells (n<=15) + claimed cells '
          'k=12..15 reproduced')

    # 4. primes
    pa = sorted({p for d in A.values() for p in d})
    pb = sorted({p for d in B.values() for p in d})
    if len(pa) != 22 or len(pb) != 22:
        fail(f'prime sets sized {len(pa)}/{len(pb)}')
    if set(pa) & set(pb):
        fail(f'prime overlap {set(pa) & set(pb)}')
    for p in pa + pb:
        if not is_prime(p):
            fail(f'composite modulus {p}')
    print('4. 22+22 proven primes, disjoint')

    # 2/3. CRT per run, per-cell coverage; anchor check
    anc = {}
    for line in open(ANC):
        t = line.split()
        if len(t) == 2 and t[0].isdigit():
            anc[int(t[0])] = int(t[1])
    if len(anc) != 27:
        fail(f'anchor object must hold 27 cells (got {len(anc)})')
    for name, R in (('A', A), ('B', B)):
        npub = nanc = 0
        for (n, k), v in tri.items():
            d = R.get((k, n))
            if not d:
                continue
            x, m = crt(sorted(d.items()))
            if 3 ** (n * k) < m:
                npub += 1
                if x != v:
                    fail(f'{name} CRT vs published T({n},{k})')
        for k, v in anc.items():
            d = R.get((k, 28))
            if not d:
                continue
            x, m = crt(sorted(d.items()))
            if 3 ** (28 * k) < m:
                nanc += 1
                if x != v:
                    fail(f'{name} CRT vs row-28 anchor T(28,{k})')
        for k in range(12, 29):
            d = R.get((k, 29))
            if not d or len(d) != 22:
                fail(f'{name} k={k}: needs 22 residues')
            x, m = crt(sorted(d.items()))
            if 3 ** (29 * k) >= m:
                fail(f'{name} k={k}: modulus under the 3^(29k) bound')
            if x != obj[k]:
                fail(f'{name} CRT vs claimed T(29,{k})')
        print(f'2/3. run{name} CRT: {npub} published + {nanc} anchor cells '
              'exact; 17/17 claimed cells exact')
    print('PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
