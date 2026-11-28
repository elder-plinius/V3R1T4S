"""Exact checker for a Delsarte linear-programming upper bound on A(n,d,w), written from the definition.

Definition. Binary constant-weight code, length n, weight w, minimum Hamming distance d = 2*delta, w <= n-w.
The words are the vertices of the Johnson scheme J(n,w); two words at Hamming distance 2x are at Johnson
distance x (x = 0..w). v_x = C(w,x)*C(n-w,x) is the valency of relation x. The eigenvalue of relation x on the
k-th eigenspace is the Eberlein polynomial
    E_x(k) = sum_{j=0}^{x} (-1)^j C(k,j) C(w-k,x-j) C(n-w-k,x-j),
the multiplicity of eigenspace k is mu_k = C(n,k) - C(n,k-1), and the dual eigenvalues are
    Q_k(x) = mu_k * E_x(k) / v_x.
For a code with inner distribution a_0 = 1, a_x >= 0 (x = 0..w; a_x = 0 for 0 < x < delta), Delsarte's
inequalities are  sum_x a_x Q_k(x) >= 0  for k = 1..w.  Since a_0 Q_k(0) = mu_k this reads
    - sum_{x>=delta} a_x Q_k(x) <= mu_k.
Dual certificate: y_k >= 0 (k = 1..w) with  sum_k y_k * (-Q_k(x)) >= 1 for every x in delta..w.
Then for any code  |C| = 1 + sum_{x>=delta} a_x <= 1 + sum_x a_x sum_k y_k(-Q_k(x)) <= 1 + sum_k y_k mu_k.
The checker verifies, in fractions.Fraction: eigenvalue orthogonality for this (n,w) (self-test), y_k >= 0,
dual feasibility for every x, and that floor(1 + sum_k y_k mu_k) equals the claimed U.
Usage: python3 -I check_delsarte.py CERT.json n d w U      (CERT.json must hold the dual under key "y")
       python3 -I check_delsarte.py --selftest
"""
import json, sys
from fractions import Fraction as F
from math import comb, floor


def C(a, b):
    return comb(a, b) if 0 <= b <= a else 0


def eberlein(n, w, x, k):
    return sum((-1) ** j * C(k, j) * C(w - k, x - j) * C(n - w - k, x - j) for j in range(x + 1))


def tables(n, w):
    v = [C(w, x) * C(n - w, x) for x in range(w + 1)]
    mu = [C(n, k) - C(n, k - 1) for k in range(w + 1)]
    Q = [[F(mu[k] * eberlein(n, w, x, k), v[x]) for x in range(w + 1)] for k in range(w + 1)]
    return v, mu, Q


def orthogonality(n, w):
    """sum_k mu_k E_i(k) E_j(k) = C(n,w) v_i [i==j], and Q_k(0) = mu_k."""
    v, mu, Q = tables(n, w)
    for i in range(w + 1):
        for j in range(w + 1):
            s = sum(mu[k] * eberlein(n, w, i, k) * eberlein(n, w, j, k) for k in range(w + 1))
            if s != (C(n, w) * v[i] if i == j else 0):
                return False
    return all(Q[k][0] == mu[k] for k in range(w + 1))


def dual_bound(n, d, w, y):
    """y: dict k -> Fraction. Returns exact bound 1 + sum y_k mu_k, raising AssertionError if y is not feasible."""
    assert d % 2 == 0 and w <= n - w
    delta = d // 2
    v, mu, Q = tables(n, w)
    assert all(0 <= k <= w for k in y), 'index out of range'
    assert 0 not in y or y[0] == 0
    for k, val in y.items():
        assert val >= 0, ('negative dual', k)
    for x in range(delta, w + 1):
        s = sum(val * (-Q[k][x]) for k, val in y.items())
        assert s >= 1, ('dual infeasible at x', x, s)
    return 1 + sum(val * mu[k] for k, val in y.items())


def vertex_lp(n, d, w):
    """Tiny exact primal LP by vertex enumeration (for self-tests with at most 4 variables)."""
    from itertools import combinations
    delta = d // 2
    v, mu, Q = tables(n, w)
    xs = list(range(delta, w + 1))
    rows = [([-Q[k][x] for x in xs], mu[k]) for k in range(1, w + 1)]
    for i in range(len(xs)):
        rows.append(([F(-1) if t == i else F(0) for t in range(len(xs))], F(0)))
    best = None
    m = len(xs)
    for sel in combinations(range(len(rows)), m):
        A = [list(rows[r][0]) + [F(rows[r][1])] for r in sel]
        ok = True
        for c in range(m):
            p = next((r for r in range(c, m) if A[r][c] != 0), None)
            if p is None:
                ok = False; break
            A[c], A[p] = A[p], A[c]
            A[c] = [t / A[c][c] for t in A[c]]
            for r in range(m):
                if r != c:
                    f = A[r][c]
                    A[r] = [a - f * b for a, b in zip(A[r], A[c])]
        if not ok:
            continue
        sol = [A[i][m] for i in range(m)]
        if all(sum(a * s for a, s in zip(r[0], sol)) <= r[1] for r in rows):
            val = 1 + sum(sol)
            if best is None or val > best:
                best = val
    return best


def main():
    if sys.argv[1] == '--selftest':
        # Hand-checkable cells: A(7,4,3)=7 (Fano plane), A(8,4,4)=14 (Steiner S(3,4,8)), A(6,4,3)=4, A(10,6,5)=6, A(9,4,3)=12.
        for (n, d, w, known) in [(6, 4, 3, 4), (7, 4, 3, 7), (8, 4, 4, 14), (10, 6, 5, 6), (9, 4, 3, 12)]:
            assert orthogonality(n, w), ('orthogonality', n, w)
            lp = vertex_lp(n, d, w)
            print(f'selftest A({n},{d},{w}): eigenvalue orthogonality ok; exact Delsarte LP optimum {lp} (best known A = {known})')
            assert lp >= known
        print('SELFTEST OK')
        return
    path, n, d, w, U = sys.argv[1], *map(int, sys.argv[2:6])
    cert = json.load(open(path))
    assert orthogonality(n, w), 'eigenvalue self-test failed'
    y = {int(k): F(s) for k, s in cert['y'].items()}
    bound = dual_bound(n, d, w, y)
    print(f'A({n},{d},{w}): exact dual objective {bound} = {float(bound):.6f}; floor {floor(bound)}; claimed U {U}')
    if 'lp_optimum' in cert:
        print('certificate states lp_optimum', cert['lp_optimum'], 'match' if F(cert['lp_optimum']) == bound else 'DIFFERENT')
    assert floor(bound) == U, 'floor of objective differs from claimed U'
    # optional: primal point (for information; not needed for validity of the upper bound)
    if 'a' in cert:
        a = {int(k): F(s) for k, s in cert['a'].items()}
        v, mu, Q = tables(n, w)
        feas = all(x >= d // 2 and val >= 0 for x, val in a.items()) and all(
            -sum(val * Q[k][x] for x, val in a.items()) <= mu[k] for k in range(1, w + 1))
        print('primal point in certificate feasible:', feas, ' its objective:', 1 + sum(a.values()))
    print(f'PASS: A({n},{d},{w}) <= {U}')


if __name__ == '__main__':
    main()
