"""Deep search for one cell: phase 1 many loose restarts, keep the top K;
phase 2 full descent of each to 1e-14 step. Saves the best to outdir."""
import sys, time, os, heapq
import numpy as np
from pen import normalize, coarse, descend, save, maxcos
from seeds import SEEDS

d, N, sec, seed, outdir, table = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
K = 6
rng = np.random.default_rng(seed)
t0 = time.time()
pool = []
names = ["rand", "simp", "cross"]
k = 0
while time.time() - t0 < 0.55 * sec:
    nm = names[k % 3]; k += 1
    X = normalize(SEEDS[nm](rng, d, N))
    X = coarse(X)
    X, c = descend(X, minstep=1e-7, iters=500)
    heapq.heappush(pool, (-c, k, X))
    if len(pool) > K:
        heapq.heappop(pool)
print(f"{d} {N} phase1 tries={k} top={sorted(-p[0] for p in pool)}", flush=True)
best, bestc = None, 9.0
for negc, _, X in sorted(pool, key=lambda p: -p[0]):
    X, c = descend(X, step=1e-6, minstep=1e-14, iters=4000,
                   deadline=t0 + sec)
    print(f"{d} {N} polished {-negc:.10f} -> {c:.15f}", flush=True)
    if c < bestc:
        best, bestc = X, c
os.makedirs(outdir, exist_ok=True)
save(os.path.join(outdir, f"{d}_{N}.txt"), best, bestc, d, N, table)
print(f"{d} {N} FINAL best={bestc:.15f} table={table} margin={float(table) - bestc:.3e}", flush=True)
