"""Build a claim JSON from the extended one-point Hermitian code E_m with some coordinates deleted (puncturing) and
then some columns of the punctured code multiplied by w (an element of norm -1, which flips that column's sign in the
Hermitian Gram matrix and so changes the hull). Adapted from build_obj.py of an earlier run (not shipped).
Usage: build_punct_obj.py m out.json d_claimed deleted_cols scaled_cols
  deleted_cols: comma list of 0-based coordinates of E_m (27 = P_inf) to delete
  scaled_cols:  comma list of 0-based columns of the punctured code to multiply by w"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import herm_dual, phi_rows, gram_rank, rref9, scale_cols
from hermitian import code, pts
m = int(sys.argv[1]); out = sys.argv[2]; dcl = int(sys.argv[3])
dele = [int(c) for c in sys.argv[4].split(',')] if sys.argv[4] else []
cols = [int(c) for c in sys.argv[5].split(',')] if len(sys.argv) > 5 and sys.argv[5] else []
G0 = code(m)
keep = [t for t in range(28) if t not in dele]
G = [[r[t] for t in keep] for r in G0]
if cols:
    G = scale_cols(G, set(cols), 3)          # 3 encodes w; w^4 = -1, so norm(w) = w^(3+1) = -1
n = len(G[0]); K = len(G)
assert len(rref9(G)[0]) == K
D = herm_dual(G, n)
S = phi_rows(D)
l = K - gram_rank(G)
obj = {
  "target_id": "eaqecc-qutrit-codetables-gaps",
  "n": n, "k": K - l, "c": n - K - l, "d": dcl,
  "field": "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8); conj(x) = x^3",
  "S_convention": "S rows are (x|z) over GF(3), 2n columns; symplectic form <(x|z),(x'|z')> = x.z' - z.x' (J = [[0,I],[-I,0]]); S = phi(D9) with phi(a + b*w) = (a | b), rows r and w*r for each row r of D9",
  "G9": G, "D9": D, "S": S,
  "construction": f"extended one-point code of the Hermitian curve y^3 + y = x^4 over GF(9): rows are the monomials x^i y^j (j <= 2, 3i + 4j <= {m}) evaluated at the 27 affine points (x, y ordered by x then y in the encoding), last coordinate 1 for the monomial of pole order {m} and 0 otherwise"
                  + (f"; then coordinates {dele} (0-based; the affine points {[pts[t] for t in dele if t < 27]} as encoded (x, y)) deleted" if dele else "")
                  + (f"; then columns {cols} (0-based, of the punctured code) multiplied by w" if cols else ""),
}
json.dump(obj, open(out, "w"))
print(f"E_{m} deleted={dele} scaled_cols={cols} [{n},{K}] hull={l} -> [[{n},{K-l},?;{n-K-l}]]  S {len(S)}x{len(S[0])}  D9 {len(D)}x{n}")
