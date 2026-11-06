"""Build the n=9 frame cap S = {0}xB0 u {1}xC u {2}x(D C), D = diag(2,2,2,2,2,1,1,1), C = the 512-cap of F_3^8,
B0 = an exact maximum cap inside K = F_3^8 \\ -(C + D C) (CP-SAT OPTIMAL). Writes the 9-digit file (first digit = slice)."""
import numpy as np, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framelib import *
spec = sys.argv[1] if len(sys.argv) > 1 else 'diag22222111'
out = sys.argv[2] if len(sys.argv) > 2 else '../out/cap_n9_frame.txt'
n = 8
C = load(RUN + '/checker/record_512_n8.txt', 8)
M = np.diag([int(c) for c in spec[4:]])
C2 = (C @ M.T) % 3
K = np.flatnonzero(K_of(C, C2))
st, sz, bnd, B0 = maxcap_in(K, 8, time_limit=120, workers=2)
print('K', len(K), 'B0', st, sz, bnd)
B0 = dec(np.array(B0), 8)
rows = []
for pre, B in [(0, B0), (1, C), (2, C2)]:
    for r in B:
        rows.append(str(pre) + ''.join(str(int(x)) for x in r))
assert len(set(rows)) == len(rows)
with open(out, 'w') as f:
    f.write('\n'.join(rows) + '\n')
print('wrote', out, 'size', len(rows))
