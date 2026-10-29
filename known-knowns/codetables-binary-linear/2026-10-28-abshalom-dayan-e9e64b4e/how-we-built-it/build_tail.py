"""Build a Construction X code from a tailg solution. Base: one-point Hermitian codes on the 27 affine points of
y^3 + y = x^4 over GF(9) (monomials x^i y^j, j <= 2, ordered by pole order 3i + 4j). Rows of pole <= a get zero tail;
the r = K_b - K_a rows of pole in (a, b] get tail entry (p_t)_j for tail column t (p_t = the tailg point index in
PG(r-1,9), lexicographic order, first nonzero coordinate 1). Usage: build_tail.py a b idx,idx,... OUT"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hermitian import pts, pw
from gf9lib import MUL, rref9
a, b = int(sys.argv[1]), int(sys.argv[2]); idx = [int(t) for t in sys.argv[3].split(',')]
mons = sorted([(i, j) for j in range(3) for i in range(30) if 3 * i + 4 * j <= b], key=lambda t: 3 * t[0] + 4 * t[1])
pole = [3 * i + 4 * j for i, j in mons]
rows = [[MUL[pw(x, i)][pw(y, j)] for x, y in pts] for i, j in mons]
Ka = sum(1 for p in pole if p <= a); r = len(rows) - Ka
proj = [v for v in itertools.product(range(9), repeat=r) if [x for x in v if x][0:1] == [1]]
P = [proj[t] for t in idx]
G = [row + ([0] * len(P) if k < Ka else [p[k - Ka] for p in P]) for k, row in enumerate(rows)]
R, piv = rref9(G)
print("monomials", mons, "poles", pole); print("tail points", P); print("k", len(G), "n", len(G[0]), "rank", len(R))
open(sys.argv[4], "w").write("%d %d\n" % (len(G), len(G[0])) + "\n".join(" ".join(map(str, x)) for x in G) + "\n")
