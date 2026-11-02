import numpy as np, time, sys
from core import *; from seeds import *
T = table(); N = int(sys.argv[1]); rng = np.random.default_rng(5); rt = T[N]
cs = {'0': np.zeros(4), 'h1': np.array([1, 0, 0, 0.]), 'h2': np.full(4, .5), 'e': np.array([.5, .5, 0, 0]), 'f': np.array([2/3, 2/3, 2/3, 0])}
for name, L in [('D4', D4), ('A4', A4 * np.sqrt(2) / np.sqrt(2))]:
    for cn, c in cs.items():
        for jit in [0.0, 0.3]:
            rs = []
            for s in range(2):
                x = lattice_cut(L, N, c + rng.normal(size=4) * 0.05 * (jit > 0), rng, jit)
                y, r = relax(x * (1 - rt) / np.linalg.norm(x, axis=1).max(), rt, k0=1e1, kfac=3)
                rs.append(r - rt)
            print(name, cn, jit, np.round(rs, 5), flush=True)
