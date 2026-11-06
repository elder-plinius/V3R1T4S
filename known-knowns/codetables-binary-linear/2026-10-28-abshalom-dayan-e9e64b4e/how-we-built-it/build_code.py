"""Rebuild the claim object from its construction. Usage: python3 build_code.py out.json
Runs build_tail.py (the Construction X builder: one-point Hermitian code C(D,17P) with zero tail, plus the 4 monomials
of pole order 18..21 with the 5 tail columns given as PG(3,9) point indices 0, 2, 11, 22, 588 in lexicographic order,
first nonzero coordinate 1) and to_json.py (writes the JSON object)."""
import sys, os, subprocess
h = os.path.dirname(os.path.abspath(__file__)); tmp = sys.argv[1] + ".code"
subprocess.run([sys.executable, os.path.join(h, "build_tail.py"), "17", "21", "0,2,11,22,588", tmp], check=True)
subprocess.run([sys.executable, os.path.join(h, "to_json.py"), tmp, "10", 'Construction X with a general tail: rows 1..15 = one-point Hermitian code C(D,17P) on the 27 affine points of y^3 + y = x^4 over GF(9) (monomials x^i y^j, j <= 2, pole order 3i + 4j <= 17, ordered by pole order; points (x,y) in lexicographic order of the encoding) with zero tail; rows 16..19 = monomials of pole order 18, 19, 20, 21 (x^6, x^5 y, x^4 y^2, x^7) with 5 tail columns whose entries for those 4 rows are the PG(3,9) points (0,0,0,1), (0,0,1,1), (0,1,0,1), (0,1,1,3), (1,6,1,2).', sys.argv[1]], check=True)
os.remove(tmp)
