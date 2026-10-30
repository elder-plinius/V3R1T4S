#!/usr/bin/env python3
"""Build a Construction X lead object (generalizes the earlier builder build_x_obj.py, not shipped here):
C1 = C(D_28, aQ + bP_inf), C2 = C(D_28, (a-1)Q + bP_inf) from deg3.py (Q = place IDX), basis "C2 rows, then rows of C1
raising the rank" (as prep_x.py), [5,3,3] tail M A on the points PTS (9 = infinity), columns marked '-' in EPS times w.
Usage: build_x_lead.py IDX a b PTS M EPS out.json d_claimed [out_G9.code]   (PTS, M comma-separated)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import ADD, MUL, herm_dual, phi_rows, gram_rank, rref9
import deg3
IDX, AA, BB = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
PTS = [int(x) for x in sys.argv[4].split(",")]
M = [int(x) for x in sys.argv[5].split(",")]
EPS = sys.argv[6]
G1, _ = deg3.code(IDX, AA, BB)
G2, _ = deg3.code(IDX, AA - 1, BB)
K1, K2, n0 = len(G1), len(G2), len(G1[0])
assert K1 - K2 == 3 and n0 == 28
assert len(rref9(G1 + G2)[0]) == K1, "C2 not inside C1"
B = [r[:] for r in G2]
for r in G1:
    if len(rref9(B + [r])[0]) > len(B):
        B.append(r)
assert len(B) == K1
A = [[0 if a == 9 else 1 for a in PTS], [0 if a == 9 else a for a in PTS], [1 if a == 9 else MUL[a][a] for a in PTS]]
G = []
for i, r in enumerate(B):
    tail = [0] * 5
    if i >= K2:
        for c in range(5):
            s = 0
            for l in range(3):
                s = ADD[s][MUL[M[(i - K2) * 3 + l]][A[l][c]]]
            tail[c] = s
    G.append(r + tail)
n = n0 + 5
assert len(EPS) == n
G = [[MUL[3][x] if EPS[t] == "-" else x for t, x in enumerate(r)] for r in G]
assert len(rref9(G)[0]) == K1
D = herm_dual(G, n)
S = phi_rows(D)
l = K1 - gram_rank(G)
out, dcl = sys.argv[7], int(sys.argv[8])
obj = {
  "target_id": "eaqecc-qutrit-codetables-gaps",
  "n": n, "k": K1 - l, "c": n - K1 - l, "d": dcl,
  "field": "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8); conj(x) = x^3",
  "S_convention": "S rows are (x|z) over GF(3), 2n columns; symplectic form <(x|z),(x'|z')> = x.z' - z.x' (J = [[0,I],[-I,0]]); S = phi(D9) with phi(a + b*w) = (a | b), rows r and w*r for each row r of D9",
  "G9": G, "D9": D, "S": S,
  "construction": ("Construction X over GF(9): C1 = C(D_28, %dQ + %dP_inf) and C2 = C(D_28, %dQ + %dP_inf) (Q = deg3.py place %d), AG codes" % (AA, BB, AA - 1, BB, IDX)) + ", AG codes of the Hermitian curve y^3 + y = x^4 (D_28 = 27 affine rational points ordered by x then y in the encoding, plus P_inf as the last coordinate via the generalized evaluation; Q the degree-3 place of a fixed point (x0, y0) over GF(729)), tail code [5,3,3] Reed-Solomon on the points %s (9 = infinity), rows 11..13 of the tail = M A with M = %s (row-major), then columns marked '-' in %s multiplied by w" % (PTS, M, EPS),
}
json.dump(obj, open(out, "w"))
if len(sys.argv) > 9:
    open(sys.argv[9], "w").write("%d %d\n" % (K1, n) + "".join(" ".join(map(str, r)) + "\n" for r in G))
print("X code [%d,%d] hull=%d -> [[%d,%d,?;%d]]  S %dx%d  D9 %dx%d" % (n, K1, l, n, K1 - l, n - K1 - l, len(S), len(S[0]), len(D), n))
