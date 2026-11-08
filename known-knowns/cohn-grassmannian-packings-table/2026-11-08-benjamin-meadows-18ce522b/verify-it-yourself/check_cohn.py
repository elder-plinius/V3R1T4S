#!/usr/bin/env python3
"""Check one configuration against a Cohn-family table cell, from the definition, in the Python standard library.

usage:
  check_cohn.py spherical    <file> <d> <N>    <claimed cos>    <table cos>    [sha256]
  check_cohn.py grassmannian <file> <m> <n> <N> <claimed value> <table value> <bound> [sha256]
  check_cohn.py harmonic     <file> <N> <n>    <claimed E>      <table min E>  [sha256]

The file holds one vector per line (comma-separated coordinates); lines starting with '#' are a header and are skipped.
Every coordinate must carry at least 20 significant digits. All arithmetic is Decimal at 60 digits.

spherical:    normalise each vector; c* = max over i < j of <x_i, x_j>. PASS needs |c* - claimed| < 1e-20 and
              table - c* >= 1e-10.
grassmannian: lines 1..n span subspace 1, the next n lines subspace 2, and so on. Each block is orthonormalised
              (Gram-Schmidt, which spans the same subspace as QR); value = min over i < j of n - ||U_i^T U_j||_F^2.
              PASS needs |value - claimed| < 1e-20, value - table >= 1e-9 and value <= bound + 1e-10.
harmonic:     normalise; E* = sum over i < j of |x_i - x_j|^-(n-2). PASS needs |E* - claimed| < 1e-20 and
              table - E* >= max(1e-9, 1e-12 E*).

The last line printed is PASS or FAIL, and the exit status is 0 only on PASS."""
import hashlib
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60


def sig_digits(tok):
    return len(tok.strip().lstrip('+-').lower().split('e')[0].replace('.', '').lstrip('0'))


def read_vectors(path, dim):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        rows.append(line.split(','))
    bad = [k for k, r in enumerate(rows) if len(r) != dim]
    fewest = min(sig_digits(t) for r in rows for t in r)
    return rows, bad, fewest


def unit(v):
    n = sum(c * c for c in v).sqrt()
    return [c / n for c in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def spherical(path, d, N):
    rows, bad, fewest = read_vectors(path, d)
    P = [unit([Decimal(t) for t in r]) for r in rows]
    best, pair = None, None
    for i in range(len(P)):
        a = P[i]
        for j in range(i):
            c = dot(a, P[j])
            if best is None or c > best:
                best, pair = c, (j, i)
    return len(rows), bad, fewest, best, 'closest pair (0-based rows) %s' % (pair,)


def gram_schmidt(block):
    out = []
    for v in block:
        w = list(v)
        for q in out:
            p = dot(w, q)
            w = [x - p * y for x, y in zip(w, q)]
        out.append(unit(w))
    return out


def grassmannian(path, m, n, N):
    rows, bad, fewest = read_vectors(path, m)
    V = [[Decimal(t) for t in r] for r in rows]
    U = [gram_schmidt(V[k * n:(k + 1) * n]) for k in range(len(V) // n)]
    best, pair = None, None
    for i in range(len(U)):
        for j in range(i):
            f = sum(dot(a, b) ** 2 for a in U[i] for b in U[j])
            v = n - f
            if best is None or v < best:
                best, pair = v, (j, i)
    return len(rows) // n if len(rows) % n == 0 else -1, bad, fewest, best, 'closest pair (0-based subspaces) %s' % (pair,)


def harmonic(path, N, n):
    rows, bad, fewest = read_vectors(path, n)
    P = [unit([Decimal(t) for t in r]) for r in rows]
    s = n - 2
    E = Decimal(0)
    dmin = None
    for i in range(len(P)):
        for j in range(i):
            d2 = sum((x - y) ** 2 for x, y in zip(P[i], P[j]))
            dmin = d2 if dmin is None or d2 < dmin else dmin
            E += 1 / (d2 ** (s // 2) * (d2.sqrt() if s % 2 else 1))
    return len(rows), bad, fewest, E, 'smallest pairwise distance %s' % (format(dmin.sqrt(), '.12f'),)


def main():
    kind, path = sys.argv[1], sys.argv[2]
    a = sys.argv[3:]
    ok = True
    if kind == 'spherical':
        d, N = int(a[0]), int(a[1]); claimed, table = Decimal(a[2]), Decimal(a[3]); sha = a[4] if len(a) > 4 else None
        count, bad, fewest, val, note = spherical(path, d, N)
    elif kind == 'grassmannian':
        m, n, N = int(a[0]), int(a[1]), int(a[2]); claimed, table, bound = Decimal(a[3]), Decimal(a[4]), Decimal(a[5])
        sha = a[6] if len(a) > 6 else None
        count, bad, fewest, val, note = grassmannian(path, m, n, N)
    elif kind == 'harmonic':
        N, n = int(a[0]), int(a[1]); claimed, table = Decimal(a[2]), Decimal(a[3]); sha = a[4] if len(a) > 4 else None
        count, bad, fewest, val, note = harmonic(path, N, n)
    else:
        print('FAIL: unknown kind %r' % kind); sys.exit(1)
    if sha:
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        print('sha256', h)
        if h != sha:
            print('FAIL: the file is not the claimed object (sha256 differs)'); ok = False
    print('objects:', count, ' expected:', N, ' fewest significant digits in a coordinate:', fewest)
    if count != N:
        print('FAIL: wrong number of objects'); ok = False
    if bad:
        print('FAIL: %d lines have the wrong number of coordinates' % len(bad)); ok = False
    if fewest < 20:
        print('FAIL: a coordinate has fewer than 20 significant digits'); ok = False
    print('computed =', format(val, '.40f'))
    print('claimed  =', claimed, ' difference =', format(abs(val - claimed), '.3e'))
    print(note)
    if abs(val - claimed) >= Decimal('1e-20'):
        print('FAIL: the computed value does not match the claimed value'); ok = False
    if kind == 'spherical':
        gap, need = table - val, Decimal('1e-10')
        print('table cos - c* =', format(gap, '.15e'), ' (need >= 1e-10)')
    elif kind == 'grassmannian':
        gap, need = val - table, Decimal('1e-9')
        print('value - table =', format(gap, '.15e'), ' (need >= 1e-9)')
        print('bound - value =', format(bound - val, '.15e'), ' (need >= -1e-10)')
        if val > bound + Decimal('1e-10'):
            print('FAIL: the value exceeds the listed bound'); ok = False
    else:
        gap, need = table - val, max(Decimal('1e-9'), Decimal('1e-12') * val)
        print('table min E - E* =', format(gap, '.15e'), ' (need >= %s)' % format(need, '.3e'))
    if gap < need:
        print('FAIL: the margin over the table is too small'); ok = False
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
