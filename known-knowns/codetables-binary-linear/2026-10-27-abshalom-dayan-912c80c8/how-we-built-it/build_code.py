"""Rebuild the claim object from its construction. Usage: python3 build_code.py out.json
Rows 1-17: the plain one-point Hermitian code C(D,19P) (monomials x^i y^j, j <= 2, pole order 3i + 4j <= 19, sorted
by pole order) evaluated at the 27 affine points of y^3 + y = x^4 over GF(9) (hermitian.pts: x then y in the a + 3b
encoding), followed by the tail (0, 0). Row 18: x^4 y^2 (pole order 20), tail (0, 1). Row 19: x^7 (pole order 21),
tail (1, 1)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hermitian import pts, pw
from gf9lib import MUL
mons = sorted([(i, j) for j in range(3) for i in range(30) if 3 * i + 4 * j <= 21], key=lambda t: 3 * t[0] + 4 * t[1])
pole = [3 * i + 4 * j for i, j in mons]
rows = [[MUL[pw(x, i)][pw(y, j)] for x, y in pts] for i, j in mons]
tail = {20: [0, 1], 21: [1, 1]}
G = [r + tail.get(p, [0, 0]) for r, p in zip(rows, pole)]
obj = {"target_id": "codetables-binary-linear", "q": 9, "n": 29, "k": 19, "d": 8,
 "field": "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8)",
 "G": G,
 "construction": "Construction X with a non-Reed-Solomon tail: rows 1-17 are the plain one-point Hermitian code C(D,19P) "
   "(monomials x^i y^j, j <= 2, pole order 3i + 4j <= 19, evaluated at the 27 affine points of y^3 + y = x^4 over GF(9), "
   "points ordered by x then y in the a + 3b encoding) followed by two zeros; row 18 is x^4 y^2 (pole order 20) followed "
   "by (0, 1); row 19 is x^7 (pole order 21) followed by (1, 1). Found by an exhaustive search over all 2-column tails "
   "for C(D,19P) inside C(D,21P)."}
json.dump(obj, open(sys.argv[1], "w"))
