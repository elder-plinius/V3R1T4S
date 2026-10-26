"""Correctness tests for the skew kernels: dE vs brute force, and exact energy tracking over long runs."""
import sys, time
import numpy as np
from labsgpu import SkewGPU, skew_expand, energy_ref, energy_pure, is_skew

rng = np.random.default_rng(20261024)
fails = 0
for L in [5, 7, 9, 11, 13, 15, 17, 21, 23, 51, 53, 101, 103, 449, 451, 599]:
    n = (L - 1) // 2; W = 6
    seqs = np.stack([skew_expand(rng.choice([-1, 1], size=n + 1)) for _ in range(W)])
    for s in seqs:
        c = np.correlate(s.astype(np.int64), s.astype(np.int64), 'full')[L:]
        assert is_skew(s) and np.all(c[0::2] == 0), "odd lags must vanish"   # c[0] is lag 1
    g = SkewGPU(L, W); g.set_start(np.arange(W), seqs)
    bE, _, E, _ = g.get()
    assert all(int(E[w]) == energy_ref(seqs[w]) for w in range(W)), f"init energy mismatch L={L}"
    dE = g.dE_all()
    for w in range(W):
        base = energy_ref(seqs[w])
        for v in range(n + 1):
            t = seqs[w].astype(np.int64).copy(); t[v] = -t[v]
            if v < n: t[2 * n - v] = -t[2 * n - v]
            if energy_ref(t) - base != dE[w, v]:
                fails += 1
                if fails < 10: print(f"dE mismatch L={L} w={w} v={v}: gpu {dE[w, v]} true {energy_ref(t) - base}")
    print(f"L={L}: dE checked for {W}x{n + 1} moves", flush=True)

for L in [101, 119, 451]:
    n = (L - 1) // 2; W = 64
    seqs = np.stack([skew_expand(rng.choice([-1, 1], size=n + 1)) for _ in range(W)])
    g = SkewGPU(L, W); g.set_start(np.arange(W), seqs)
    t0 = time.time()
    for rep in range(5): g.run(2000, max(1, (n + 1) // 8), max(1, (n + 1) // 16), seed=1000 + rep)
    import cupy as cp; cp.cuda.Device(0).synchronize(); dt = time.time() - t0
    bE, bS, E, S = g.get()
    for w in range(W):
        if int(E[w]) != energy_ref(S[w]) or int(bE[w]) != energy_ref(bS[w]) or not is_skew(S[w]) or not is_skew(bS[w]):
            fails += 1; print(f"tracking mismatch L={L} w={w}: E {E[w]} vs {energy_ref(S[w])}, best {bE[w]} vs {energy_ref(bS[w])}")
    w0 = int(np.argmin(bE))
    assert energy_pure(bS[w0]) == int(bE[w0])
    print(f"L={L}: 64 walkers x 10000 steps in {dt:.2f}s ({64 * 10000 / dt:,.0f} steps/s); tracked energies exact; "
          f"best E={int(bE.min())} F={L * L / (2 * int(bE.min())):.4f}", flush=True)
print("FAILURES:", fails)
sys.exit(1 if fails else 0)
