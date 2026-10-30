"""Extended one-point codes on the Hermitian curve y^3 + y = x^4 over GF(9) (27 affine points + P_inf; the curve
codetables.de uses for its [23..28, 9..14] codes). E_m: rows f in basis of L(m P_inf) (x^i y^j, j <= 2, 3i+4j <= m),
coordinates (f(P_1..P_27), [f is the monomial of pole order m]); d >= 28 - m (Goppa bound argument, extended).
Usage: hermitian.py m [shorten_spec]   shorten_spec = comma list of coordinate indices (27 = P_inf)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import ADD, MUL, rref9
def pw(x, e):
    r = 1
    for _ in range(e): r = MUL[r][x]
    return r
pts = [(x, y) for x in range(9) for y in range(9) if ADD[pw(y, 3)][y] == pw(x, 4)]
assert len(pts) == 27, len(pts)
def code(m):
    mons = sorted([(i, j) for j in range(3) for i in range(m + 1) if 3 * i + 4 * j <= m], key=lambda t: 3 * t[0] + 4 * t[1])
    top = mons[-1]; assert 3 * top[0] + 4 * top[1] == m
    return [[MUL[pw(x, i)][pw(y, j)] for x, y in pts] + [1 if (i, j) == top else 0] for i, j in mons]
def shorten(G, S):
    n = len(G[0]); order = list(S) + [c for c in range(n) if c not in S]
    R, piv = rref9([[r[c] for c in order] for r in G])
    sub = [row for row, pc in zip(R, piv) if pc >= len(S)]
    keep = [i for i, c in enumerate(order) if c not in S]
    return [[row[i] for i in keep] for row in sub]
if __name__ == "__main__":
    m = int(sys.argv[1]); G = code(m)
    if len(sys.argv) > 2 and sys.argv[2]:
        G = shorten(G, [int(c) for c in sys.argv[2].split(',')])
    print(len(G), len(G[0]))
    for r in G: print(" ".join(map(str, r)))
