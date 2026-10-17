#!/usr/bin/env python3
"""Exact checker for entanglement-assisted qutrit codes [[n,k,d;c]]_3 (run 2026-10-17-1119, scout).

Input: a text file, one stabilizer generator per line, 2n integers in {0,1,2} (X part x_1..x_n then Z part z_1..z_n),
separated by spaces or commas; blank lines and lines starting with # are ignored.
Definitions (bank criterion, eaqecc-qutrit-codetables-gaps):
  s = rank of S over GF(3); <u,v> = u_X.v_Z - u_Z.v_X (mod 3); c = rank(S J S^T)/2; k = n - s + c;
  d = min symplectic weight of v in span(S)^perp (symplectic dual) with v not in span(S) & span(S)^perp.
Symplectic weight of v = number of i with (x_i, z_i) != (0, 0). Exhaustive enumeration over span(S)^perp.
Usage: python3 eacheck.py GENFILE [--expect n,k,d,c]   prints n s c k d, then PASS/FAIL if --expect is given.
"""
import sys
import itertools
import numpy as np

P = 3


def rref(M):
    M = M.copy() % P
    r = 0
    piv = []
    rows, cols = M.shape
    for col in range(cols):
        pr = None
        for i in range(r, rows):
            if M[i, col] % P:
                pr = i
                break
        if pr is None:
            continue
        M[[r, pr]] = M[[pr, r]]
        inv = 1 if M[r, col] == 1 else 2  # inverses mod 3
        M[r] = (M[r] * inv) % P
        for i in range(rows):
            if i != r and M[i, col]:
                M[i] = (M[i] - M[i, col] * M[r]) % P
        piv.append(col)
        r += 1
        if r == rows:
            break
    return M[:r], piv


def rank(M):
    if M.size == 0:
        return 0
    return rref(M)[0].shape[0]


def nullspace(A):
    """Basis (rows) of {v : A v = 0} over GF(3)."""
    R, piv = rref(A)
    cols = A.shape[1]
    free = [j for j in range(cols) if j not in piv]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i, f]) % P
        basis.append(v)
    return np.array(basis, dtype=np.int64).reshape(len(basis), cols)


def symp(n):
    J = np.zeros((2 * n, 2 * n), dtype=np.int64)
    J[:n, n:] = np.eye(n, dtype=np.int64)
    J[n:, :n] = -np.eye(n, dtype=np.int64)
    return J % P


def analyse(S):
    S = np.array(S, dtype=np.int64) % P
    n = S.shape[1] // 2
    J = symp(n)
    Sb, _ = rref(S)
    s = Sb.shape[0]
    M = (Sb @ J @ Sb.T) % P
    two_c = rank(M)
    assert two_c % 2 == 0
    c = two_c // 2
    k = n - s + c
    # symplectic dual: v with Sb J v^T = 0
    D = nullspace((Sb @ J) % P)          # dim 2n - s
    # isotropic part: span(S) & span(S)^perp = {a Sb : a M = 0}
    A = nullspace(M.T % P)                # coefficient vectors a with a M = 0 (M antisymmetric)
    Iso = (A @ Sb) % P if A.shape[0] else np.zeros((0, 2 * n), dtype=np.int64)
    iso_dim = rank(Iso) if Iso.shape[0] else 0
    assert iso_dim == s - 2 * c
    # basis of D with Iso first: extend Iso to a basis of D
    B = Iso.copy()
    ext = []
    cur = iso_dim
    for v in D:
        T = np.vstack([B, v[None, :]]) if B.shape[0] else v[None, :]
        if rank(T) > cur:
            B = T
            ext.append(v)
            cur += 1
    E = np.array(ext, dtype=np.int64).reshape(len(ext), 2 * n)
    assert E.shape[0] == (2 * n - s) - iso_dim == 2 * k
    if k == 0:
        return dict(n=n, s=s, c=c, k=k, d=None)
    # enumerate v = a.Iso + b.E with b != 0; min symplectic weight
    best = 2 * n + 1
    Ib = Iso
    # all combinations of the iso part (3^iso_dim) as a matrix
    if iso_dim:
        coeffs = np.array(list(itertools.product(range(P), repeat=iso_dim)), dtype=np.int64)
        isoall = (coeffs @ Ib) % P
    else:
        isoall = np.zeros((1, 2 * n), dtype=np.int64)
    for b in itertools.product(range(P), repeat=E.shape[0]):
        if not any(b):
            continue
        w = (np.array(b, dtype=np.int64) @ E) % P
        V = (isoall + w) % P
        wt = ((V[:, :n] != 0) | (V[:, n:] != 0)).sum(axis=1).min()
        if wt < best:
            best = int(wt)
    return dict(n=n, s=s, c=c, k=k, d=best)


def load(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        rows.append([int(x) for x in line.replace(',', ' ').split()])
    return rows


if __name__ == '__main__':
    S = load(sys.argv[1])
    r = analyse(S)
    print("n %(n)d s %(s)d c %(c)d k %(k)d d %(d)s" % r)
    if '--expect' in sys.argv:
        n, k, d, c = map(int, sys.argv[sys.argv.index('--expect') + 1].split(','))
        ok = (r['n'], r['k'], r['d'], r['c']) == (n, k, d, c)
        print("PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
