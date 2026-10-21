#!/usr/bin/env python3
"""Standalone exact verifier for a Delsarte-type LP upper bound on A(n,d,w) (binary constant-weight codes).
Python 3 standard library only.  usage: python3 verify.py cert.json

Notation: C is an (n,d,w) code, d = 2*delta.  For words u,v of weight w the Johnson distance is
x = |u \\ v| = (Hamming distance)/2.  Inner distribution: a_x = (1/|C|) #{(u,v) in C^2 : x(u,v) = x}, so a_0 = 1,
a_x = 0 for 0 < x < delta, a_x >= 0, and |C| = 1 + sum_{x>=delta} a_x.
Valid inequalities checked here (each certificate row is one of these, recomputed from scratch):
  D<k>  (Delsarte 1973):  sum_x a_x Q_k(x) >= 0, i.e.  -sum_{x>=delta} a_x Q_k(x) <= Q_k(0) = m_k,
        Q_k(x) = dual eigenvalue of the Johnson scheme J(n,w) (w <= n/2), computed below by the dual-Hahn formula
        Q_k(x) = m_k * sum_j (-1)^j C(k,j) C(n+1-k,j) / (C(w,j) C(n-w,j)) * C(x,j),  m_k = C(n,k) - C(n,k-1).
  R<x>  a_x <= C(w,x) * A(n-w, d, x): fix c in C. A codeword v at Johnson distance x from c is determined by the
        x-set R = c minus v and the x-set S = v minus c (S lies in the n-w coordinates outside c). Codewords with
        the same R differ only in S, so their S-sets have pairwise Hamming distance >= d: at most A(n-w,d,x) of them
        per R, and there are C(w,x) choices of R. The bound holds for every c, hence for the average a_x.
        (For x = w: the codewords disjoint from c form an (n-w,d,w) code.) The numeric value of A(n-w,d,x) is an
        upper bound read from Brouwer's table (cert field table_inputs; see CLAIM.md).
Certificate: nonnegative rationals y_r with sum_r y_r * row_r(x) >= 1 for every x in delta..w.  Then
|C| = 1 + sum_x a_x <= 1 + sum_x a_x sum_r y_r row_r(x) <= 1 + sum_r y_r rhs_r.
The script also self-tests the Q formula: the Delsarte inequalities must hold for the inner distribution of ANY
subset of J(n,w) (random subsets of small schemes), and the eigenvalues P_k used in place of Q_k (a classic mix-up) must fail it."""
import json, sys, random, itertools
from fractions import Fraction as F
from math import comb, floor

def m(n, k): return comb(n, k) - (comb(n, k - 1) if k > 0 else 0)
def Q(n, w, k, x):
    return m(n, k) * sum(F((-1) ** j * comb(k, j) * comb(n + 1 - k, j), comb(w, j) * comb(n - w, j)) * comb(x, j) for j in range(k + 1))

def selftest():
    rnd = random.Random(1)
    for (n, w) in [(8, 3), (9, 4), (10, 4), (11, 5), (12, 4)]:
        V = [frozenset(c) for c in itertools.combinations(range(n), w)]
        for trial in range(30):
            S = rnd.sample(V, rnd.randint(2, min(40, len(V))))
            a = [F(0)] * (w + 1)
            for u in S:
                for v in S: a[w - len(u & v)] += 1
            a = [t / len(S) for t in a]
            for k in range(w + 1):
                assert sum(a[x] * Q(n, w, k, x) for x in range(w + 1)) >= 0, ('Delsarte fails', n, w, k)
        # negative control: the eigenvalues P_k(x) (Eberlein polynomials) used in place of the dual eigenvalues
        # Q_k(x) (a classic mix-up) must violate some inequality on some random subset
        def Qbad(k, x): return F(sum((-1) ** j * comb(x, j) * comb(w - x, k - j) * comb(n - w - x, k - j) for j in range(k + 1)))
        bad = False
        for trial in range(300):
            S = rnd.sample(V, rnd.randint(2, min(40, len(V))))
            a = [F(0)] * (w + 1)
            for u in S:
                for v in S: a[w - len(u & v)] += 1
            if any(sum(a[x] * Qbad(k, x) for x in range(w + 1)) < 0 for k in range(1, w + 1)): bad = True; break
        assert bad, 'negative control did not fail'
        # whole scheme: inner distribution of V is the valencies; Q_k sums to 0 for k >= 1
        val = [comb(w, x) * comb(n - w, x) for x in range(w + 1)]
        for k in range(1, w + 1): assert sum(val[x] * Q(n, w, k, x) for x in range(w + 1)) == 0
    print('selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK')

def main(path):
    c = json.load(open(path)); n, d, w = c['cell']['n'], c['cell']['d'], c['cell']['w']
    assert d % 2 == 0 and 2 * w <= n; delta = d // 2; X = range(delta, w + 1)
    tot = [F(0) for _ in X]; val = F(1)
    for r in c['constraints']:
        tag = r['tag']; y = F(r['dual']); assert y >= 0, 'negative dual'
        if tag.startswith('D'):
            k = int(tag[1:]); row = [-Q(n, w, k, x) for x in X]; rhs = Q(n, w, k, 0)
        elif tag.startswith('R'):
            xx = int(tag[1:]); assert delta <= xx <= w
            row = [F(1) if x == xx else F(0) for x in X]; rhs = F(comb(w, xx) * c['table_inputs']['A(%d,%d,%d)' % (n - w, d, xx)])
        else:
            raise SystemExit('unknown constraint ' + tag)
        assert [str(v) for v in row] == [r['coeffs'][str(x)] for x in X], ('row mismatch', tag)
        assert str(rhs) == r['rhs'], ('rhs mismatch', tag)
        for i in range(len(row)): tot[i] += y * row[i]
        val += y * rhs
    for x, t in zip(X, tot): print(f'  column x={x}: sum_r y_r row_r(x) = {t}  (needs >= 1)'); assert t >= 1
    print(f'certified: A({n},{d},{w}) <= {val} = {float(val):.6f}, hence A({n},{d},{w}) <= {floor(val)}')
    assert floor(val) == c['claimed_bound']
    print('VERIFIED bound', floor(val))

if __name__ == '__main__':
    selftest(); main(sys.argv[1])
