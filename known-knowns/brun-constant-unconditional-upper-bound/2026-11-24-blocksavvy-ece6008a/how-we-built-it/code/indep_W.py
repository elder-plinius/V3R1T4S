"""Independent check of the W tables (different algorithm: numpy smallest-prime-factor sieve, float64 terms, numpy cumsum)
at 40 random n <= 1e7 and at chunk points k*1e4 <= 1e7. Expect relative agreement ~1e-12 and table >= independent value*(1-1e-12)."""
import numpy as np
N = 10**7
spf = np.zeros(N + 1, dtype=np.int32)
for p in range(2, int(N**0.5) + 1):
    if spf[p] == 0:
        blk = spf[p*p::p]; blk[blk == 0] = p
spf[spf == 0] = np.arange(N + 1)[spf == 0]
g = np.zeros(N + 1); g[1] = 1.0
for n in range(3, N + 1, 2):
    p = spf[n]; m = n // p
    if m % p == 0 or g[m] == 0.0: continue
    g[n] = g[m] * p / (p - 2)
Wi = np.cumsum(g)
import os; W = os.environ.get("BRUN_WORK", "work") + "/"
Wd = np.memmap(W + "Wfx_dense_1e7.bin", dtype=np.float64, mode="r")
raw = np.fromfile(W + "Wfx_chunks_1e10.bin", dtype=np.uint8).reshape(-1, 16).copy().view("<u8").reshape(-1, 2)
Wc = raw[:, 1].astype(np.float64) * 2.0**24 + raw[:, 0].astype(np.float64) / 2.0**40
rng = np.random.default_rng(20261124); pts = sorted(set(rng.integers(1, N, 40).tolist() + [100, 20000, N]))
worst = 0; viol = 0
for n in pts:
    r = Wd[n] / Wi[n] - 1; worst = max(worst, abs(r)); viol += Wd[n] < Wi[n] * (1 - 1e-12)
for k in range(1, N // 10**4 + 1):
    r = Wc[k - 1] / Wi[k * 10**4] - 1; worst = max(worst, abs(r)); viol += Wc[k - 1] < Wi[k * 10**4] * (1 - 1e-12)
print("dense pts %d, chunk pts %d, max rel diff %.3e, violations %d -> %s" % (len(pts), N // 10**4, worst, viol, "PASS" if viol == 0 and worst < 1e-9 else "FAIL"))
