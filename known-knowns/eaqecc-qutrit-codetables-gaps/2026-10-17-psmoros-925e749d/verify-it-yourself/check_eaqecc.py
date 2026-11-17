#!/usr/bin/env python3
"""Standalone checker (Python standard library only) for the entanglement-assisted qutrit code in
object/S_33_1_31_24.txt, written from the V3R1T4S bank definition (target eaqecc-qutrit-codetables-gaps):

  S = stabilizer generators on Alice's n qutrits, rows of 2n entries over GF(3) (X part, then Z part);
  s = rank(S); <u,v> = u_X.v_Z - u_Z.v_X (mod 3); c = rank(S J S^T)/2; k = n - s + c;
  d = minimum symplectic weight of vectors in span(S)^perp that are not in span(S) & span(S)^perp.
  (For v in span(S)^perp, "not in the isotropic part" is the same as "not in span(S)".)

Every vector of span(S)^perp is enumerated (here 3^10 = 59049), so d is exact.
Usage (from the package folder): python3 verify-it-yourself/check_eaqecc.py [object file] [n,k,d,c]
Last output line: PASS if (n,k,d,c) = (33,1,31,24) and d_lower = 25 < d <= d_upper = 32, else FAIL.
"""
import itertools
import sys

P = 3
CELL = (33, 1, 24)          # (n, k, c) cell of https://eaqecc.codetables.de/qutrit.php
TABLE = (25, 32)            # d_lower, d_upper of that cell (fetched 2026-10-17, page "Last change: 10.07.2025")


def load(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            row = [int(x) for x in line.replace(',', ' ').split()]
            if any(x not in (0, 1, 2) for x in row):
                raise ValueError("entry outside {0,1,2}")
            rows.append(row)
    if not rows or any(len(r) != len(rows[0]) for r in rows) or len(rows[0]) % 2:
        raise ValueError("ragged rows or odd column count")
    return rows


def rref(rows, ncols):
    M = [list(r) for r in rows]
    piv = []
    r = 0
    for col in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][col] % P), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 if M[r][col] == 1 else 2
        M[r] = [(x * inv) % P for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col]:
                f = M[i][col]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        piv.append(col)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def symp_prod(u, v, n):
    return (sum(u[i] * v[n + i] for i in range(n)) - sum(u[n + i] * v[i] for i in range(n))) % P


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'object/S_33_1_31_24.txt'
    S = load(path)
    n = len(S[0]) // 2
    R, piv = rref(S, 2 * n)
    s = len(R)
    G = [[symp_prod(a, b, n) for b in R] for a in R]
    rG, _ = rref(G, s)
    if len(rG) % 2:
        print("odd commutation rank")
        print("FAIL")
        return 1
    c = len(rG) // 2
    k = n - s + c
    # span(S)^perp = nullspace of the matrix A with A[i] = (row_i)J, i.e. v with <row_i, v> = 0 for all i
    A = [[(-r[n + j]) % P for j in range(n)] + [r[j] % P for j in range(n)] for r in R]
    AR, apiv = rref(A, 2 * n)
    free = [j for j in range(2 * n) if j not in apiv]
    D = []
    for f in free:
        v = [0] * (2 * n)
        v[f] = 1
        for i, pc in enumerate(apiv):
            v[pc] = (-AR[i][f]) % P
        D.append(v)
    assert all(symp_prod(g, v, n) == 0 for g in R for v in D)

    def in_span_S(v):
        w = list(v)
        for i, pc in enumerate(piv):
            if w[pc]:
                f = w[pc]
                w = [(a - f * b) % P for a, b in zip(w, R[i])]
        return not any(w)

    best = None
    count = 0
    for coeffs in itertools.product(range(P), repeat=len(D)):
        if not any(coeffs):
            continue
        v = [0] * (2 * n)
        for a, b in zip(coeffs, D):
            if a:
                v = [(x + a * y) % P for x, y in zip(v, b)]
        wt = sum(1 for i in range(n) if v[i] or v[n + i])
        if best is not None and wt > best:
            continue
        if in_span_S(v):
            continue
        if best is None or wt < best:
            best, count = wt, 1
        else:
            count += 1
    print("n %d s %d c %d k %d dim_dual %d d %s (vectors of weight d outside the isotropic part: %d)"
          % (n, s, c, k, len(D), best, count))
    expect = (33, 1, 31, 24)
    if len(sys.argv) > 2:
        expect = tuple(int(x) for x in sys.argv[2].split(','))
    ok = (n, k, best, c) == expect and (n, k, c) == CELL and TABLE[0] < best <= TABLE[1] and c >= 1 and k >= 1
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
