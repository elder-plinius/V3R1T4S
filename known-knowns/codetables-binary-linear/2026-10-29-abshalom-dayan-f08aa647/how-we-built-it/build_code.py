"""Rebuild the claim object from its construction. Usage: python3 build_code.py out.json
Runs build_tail.py (the Construction X builder: one-point Hermitian code C(D,16P) with zero tail, plus the 3 monomials
of pole order 17..19 with the 4 tail columns given as PG(2,9) point indices 0, 1, 2, 13 in lexicographic order,
first nonzero coordinate 1) and to_json.py (writes the JSON object)."""
import sys, os, subprocess
h = os.path.dirname(os.path.abspath(__file__)); tmp = sys.argv[1] + ".code"
subprocess.run([sys.executable, os.path.join(h, "build_tail.py"), "16", "19", "0,1,2,13", tmp], check=True)
subprocess.run([sys.executable, os.path.join(h, "to_json.py"), tmp, "11", 'Construction X with a general tail: rows 1..14 = one-point Hermitian code C(D,16P) on the 27 affine points of y^3 + y = x^4 over GF(9) (monomials x^i y^j, j <= 2, pole order 3i + 4j <= 16, ordered by pole order; points (x,y) in lexicographic order of the encoding) with zero tail; rows 15..17 = monomials of pole order 17, 18, 19 (x^3 y^2, x^6, x^5 y) with 4 tail columns whose entries for those 3 rows are the PG(2,9) points (0,0,1), (0,1,0), (0,1,1), (1,0,3).', sys.argv[1]], check=True)
os.remove(tmp)
