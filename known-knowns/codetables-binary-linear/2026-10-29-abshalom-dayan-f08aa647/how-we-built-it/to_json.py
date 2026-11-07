"""Code file ("k n" + rows) -> claim JSON object. Usage: to_json.py CODE D CONSTRUCTION OUT"""
import sys, json
L = open(sys.argv[1]).read().split("\n"); k, n = map(int, L[0].split())
G = [list(map(int, l.split())) for l in L[1:1 + k]]
o = {"target_id": "codetables-binary-linear", "q": 9, "n": n, "k": k, "d": int(sys.argv[2]),
     "field": "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8)", "G": G, "construction": sys.argv[3]}
open(sys.argv[4], "w").write(json.dumps(o) + "\n")
