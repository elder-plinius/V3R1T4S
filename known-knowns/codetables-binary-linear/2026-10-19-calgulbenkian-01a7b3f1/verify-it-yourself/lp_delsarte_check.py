"""Exact check of a Delsarte linear-programming dual certificate that no [n,k,D]_q code exists. Standard library only.
Usage: python3 lp_delsarte_check.py object.json D
The certificate is f(w) = 1 + sum_{j=1..m} y_j K_j(w; n, q) with rational y_j >= 0, where K_j is the Krawtchouk
polynomial K_j(w) = sum_r (-1)^r (q-1)^(j-r) C(w,r) C(n-w, j-r).
If f(w) <= 0 for every integer w in D..n, then every code of length n over an alphabet of size q with minimum
distance at least D has at most f(0) words (Delsarte).  A linear [n,k] code has q^k words, so if f(0) < q^k there is
no [n,k,D']_q code with D' >= D.  Here D is passed on the command line (it is the live upper bound of the table
cell), not read from the object.  The last line printed is a JSON object with the result."""
import sys, json
from fractions import Fraction as F
from math import comb


def K(j, w, n, q):
    return sum((-1) ** r * (q - 1) ** (j - r) * comb(w, r) * comb(n - w, j - r) for r in range(0, j + 1))


def main(path, D):
    d = json.load(open(path))
    q, n, k = d['q'], d['n'], d['k']
    ys = [F(s) for s in d['y_multipliers_rational']]
    assert all(y >= 0 for y in ys), 'negative multiplier'
    P = lambda w: 1 + sum(y * K(j + 1, w, n, q) for j, y in enumerate(ys))
    worst = max(P(w) for w in range(D, n + 1))
    p0 = P(0)
    ok = worst <= 0 and p0 < q ** k
    print('q=%d n=%d k=%d D=%d degree=%d' % (q, n, k, D, len(ys)))
    print('f(0) = %s  (approx %.6f) ; q^k = %d' % (p0, float(p0), q ** k))
    print('max over integers w in D..n of f(w) = %s (approx %.6e)' % (worst, float(worst)))
    print('object field P_at_0_rational = %s (agrees: %s)' % (d.get('P_at_0_rational'), str(F(d.get('P_at_0_rational', '0')) == p0)))
    print(json.dumps({"q": q, "n": n, "k": k, "D": D, "f0_lt_qk": bool(p0 < q ** k), "max_f_le_0": bool(worst <= 0),
                      "VALID": bool(ok)}))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
