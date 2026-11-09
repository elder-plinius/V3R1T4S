import numpy as np, time, cupy as cp
from labsgpu import SkewGPU, skew_expand, energy_ref, is_skew
rng = np.random.default_rng(5); fails = 0
for L, tbl in [(21, 64), (101, 4096), (451, 8192)]:
    n = (L - 1) // 2; W = 64
    g = SkewGPU(L, W); seqs = np.stack([skew_expand(rng.choice([-1, 1], size=n + 1)) for _ in range(W)]); g.set_start(np.arange(W), seqs)
    t0 = time.time(); g.run_saw(min(3000, tbl // 2), tbl, 77); cp.cuda.Device(0).synchronize(); dt = time.time() - t0
    bE, bS, E, S = g.get()
    for w in range(W):
        if int(E[w]) != energy_ref(S[w]) or int(bE[w]) != energy_ref(bS[w]) or not is_skew(S[w]): fails += 1
    print(f"L={L}: SAW {min(3000, tbl//2)} steps x {W} walkers in {dt:.2f}s; best E {int(bE.min())} F {L*L/(2*int(bE.min())):.3f}; stuck steps {int(cp.asnumpy(g.stuck).sum())}", flush=True)
print('FAILURES', fails)
