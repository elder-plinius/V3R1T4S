"""Quick screen: loose descents from alternating seeds for a fixed time; prints gap to table."""
import sys, time, os
import numpy as np
from pen import normalize, coarse, descend, save, maxcos
from seeds import SEEDS

d, N, sec, seed, outdir, table = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
rng = np.random.default_rng(seed)
t0 = time.time()
best, bestc, by = None, 9.0, None
names = ["rand", "simp", "cross"]
k = 0
while time.time() - t0 < sec or best is None:
    nm = names[k % 3]; k += 1
    X = normalize(SEEDS[nm](rng, d, N))
    X = coarse(X)
    X, c = descend(X, minstep=1e-7, iters=500)
    if c < bestc:
        best, bestc, by = X, c, nm
os.makedirs(outdir, exist_ok=True)
save(os.path.join(outdir, f"{d}_{N}.txt"), best, bestc, d, N, table)
print(f"{d} {N} loose_best={bestc:.9f} table={table} gap={bestc - float(table):.3e} seed={by} tries={k}", flush=True)
