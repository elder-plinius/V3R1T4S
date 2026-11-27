#!/usr/bin/env python3
"""Write a scheme JSON as three plain text factor files u.txt, v.txt, w.txt (one line per term, index:coefficient).
Usage: export_txt.py scheme.json outdir"""
import json, sys, os
from fractions import Fraction
s = json.load(open(sys.argv[1]))
n1, n2, n3 = s["format"]
terms = s["terms"]
R = len(terms)
os.makedirs(sys.argv[2], exist_ok=True)
conv = "m_k = (sum u_k[i*%d+j] A[i][j]) * (sum v_k[j*%d+l] B[j][l]);  C[i][l] = sum_k w_k[i*%d+l] m_k" % (n2, n3, n3)
for ax, what in (("u", "A (%dx%d), index i*%d+j" % (n1, n2, n2)), ("v", "B (%dx%d), index j*%d+l" % (n2, n3, n3)),
                 ("w", "C (%dx%d), index i*%d+l" % (n1, n3, n3))):
    with open(os.path.join(sys.argv[2], ax + ".txt"), "w") as out:
        out.write("# factor %s of a bilinear scheme for <%d,%d,%d> over Q; entries of %s\n" % (ax, n1, n2, n3, what))
        out.write("# format %d %d %d\n# rank %d\n# convention: %s\n" % (n1, n2, n3, R, conv))
        out.write("# one line per term k = 0..%d: space-separated index:coefficient (integer or p/q)\n" % (R - 1))
        for t in terms:
            out.write(" ".join("%d:%s" % (int(i), str(Fraction(c))) for i, c in sorted(t[ax], key=lambda x: int(x[0]))) + "\n")
print("wrote", R, "terms to", sys.argv[2])
