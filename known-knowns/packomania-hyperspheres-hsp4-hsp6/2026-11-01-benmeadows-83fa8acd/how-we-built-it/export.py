"""Convert a search output (points in unit ball, maximise min distance D) to ball centres.

usage: python3 export.py in.npy out.txt table_value
Centres c = s x with s chosen slightly below 1 - r so that the boundary constraint has
a margin; the file carries 20 significant digits per coordinate.
"""
import sys
import numpy as np
from mpmath import mp, mpf

mp.dps = 40
x = np.load(sys.argv[1]); out = sys.argv[2]; rt = sys.argv[3]
n = x.shape[0]
nr = np.linalg.norm(x, axis=1)
x = x / max(1.0, nr.max())
dif = x[:, None, :] - x[None, :, :]
dd = np.sqrt((dif ** 2).sum(-1)); dd[np.diag_indices(n)] = 9
D = dd.min()
r = D / (2 + D)
s = 1 - r
c = [[mpf(float(v)) * mpf(float(s)) for v in row] for row in x]
with open(out, "w") as fh:
    fh.write(f"# hsp4 N={n} search_r={r:.15f} table_r={rt} centres in unit 4-ball\n")
    for row in c:
        fh.write(" ".join(mp.nstr(v, 20, min_fixed=-1, max_fixed=1) for v in row) + "\n")
print(n, r)
