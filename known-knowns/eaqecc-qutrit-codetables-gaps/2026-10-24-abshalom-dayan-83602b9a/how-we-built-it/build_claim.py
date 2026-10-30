"""Build a claim JSON from the extended one-point Hermitian code E_m (optionally shortened): G9 (generator of C over
GF(9)), D9 = C^perp_H, S = phi(D9) over GF(3) (rows (x|z), x = a, z = b for a + b*w)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from gf9lib import herm_dual, phi_rows, gram_rank, rref9
from hermitian import code, shorten
m = int(sys.argv[1]); out = sys.argv[2]
G = code(m)
n = len(G[0]); K = len(G)
D = herm_dual(G, n)
S = phi_rows(D)
l = K - gram_rank(G)
obj = {
  "target_id": "eaqecc-qutrit-codetables-gaps",
  "n": n, "k": K - l, "c": n - K - l, "d": int(sys.argv[3]),
  "field": "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8); conj(x) = x^3",
  "S_convention": "S rows are (x|z) over GF(3), 2n columns; symplectic form <(x|z),(x'|z')> = x.z' - z.x' (J = [[0,I],[-I,0]]); S = phi(D9) with phi(a + b*w) = (a | b), rows r and w*r for each row r of D9",
  "G9": G, "D9": D, "S": S,
  "construction": f"extended one-point code of the Hermitian curve y^3 + y = x^4 over GF(9): rows are the monomials x^i y^j (j <= 2, 3i + 4j <= {m}) evaluated at the 27 affine points (x, y ordered by x then y in the encoding), last coordinate 1 for the monomial of pole order {m} and 0 otherwise",
}
json.dump(obj, open(out, "w"))
print(f"[{n},{K}] hull={l} -> [[{n},{K-l},?;{n-K-l}]]  S {len(S)}x{len(S[0])}  D9 {len(D)}x{n}")
