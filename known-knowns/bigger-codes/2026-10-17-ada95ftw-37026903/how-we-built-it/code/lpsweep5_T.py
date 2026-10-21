"""Extra rows: a_x <= T(x,w ; x,n-w ; d), the doubly-constant-weight maximum (pairs (R,S), R an x-subset of a w-set,
S an x-subset of an (n-w)-set, distance |R^R'|+|S^S'| >= d), bounded by the Johnson-type recursion
T(a,A;b,B) <= floor(B/b * T(a,A;b-1,B-1)) and floor(A/a * T(a-1,A-1;b,B)), with T(a,A;0,B) = U(A,d,a),
T(0,A;b,B) = U(B,d,b). Conservative rule (no single-value table inputs) as in lpsweep3."""
import sys, json
sys.argv = ['x', '../../tools', '../../data/Andw.html']
src = open('code/lpsweep3_conservative.py').read()
pre = src.split("res = []")[0]
exec(pre)
from functools import lru_cache
@lru_cache(None)
def T(a, A, b, B, d):
    if a < 0 or b < 0 or a > A or b > B: return 0
    if b == 0: return U(A, d, a)
    if a == 0: return U(B, d, b)
    t = comb(A, a) * U(B, d, b)
    t = min(t, comb(B, b) * U(A, d, a))
    t = min(t, (B * T(a, A, b - 1, B - 1, d)) // b, (A * T(a - 1, A - 1, b, B, d)) // a)
    return t
_build = build
def build(n, d, w, moments=True, xb=True):
    X, rows, rhs, tags = _build(n, d, w, moments, xb)
    for i, x in enumerate(X):
        r = [F(0)] * len(X); r[i] = F(1); rows.append(r); rhs.append(F(T(x, w, x, n - w, d))); tags.append(f'T{x}')
    return X, rows, rhs, tags
res = []
for k, (lo, hi, raw) in sorted(TABLE.items()):
    n, d, w = k
    if 2 * w > n or hi is None: continue
    r = certify(n, d, w)
    if r and r['bound'] < hi:
        o = dict(cell=k, table=raw, bound=r['bound'], cert=str(r['cert']), active=[t for t, y in zip(r['tags'], r['y']) if y != 0]); res.append(o); print(o, flush=True)
    if r and r['bound'] < lo: print('BUG below lo', k)
json.dump(res, open('output/sweep5_T.json', 'w'), indent=1, default=str)
print('robust cells below table (with T rows):', len(res))
