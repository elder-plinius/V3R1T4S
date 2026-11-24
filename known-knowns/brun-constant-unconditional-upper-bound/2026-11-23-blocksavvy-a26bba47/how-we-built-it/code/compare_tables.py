"""Compare the rigorous fixed-point V tables (vsieve_fx) with Dunn's V_list (interval lower bounds) and the old double table."""
import numpy as np, h5py
import os
W = os.environ.get("BRUN_WORK", "work") + "/"
raw = np.fromfile(W + "Vfx_chunks_1e10.bin", dtype=np.uint8).reshape(-1, 24)
lo = raw[:, :16].copy().view("<u8").reshape(-1, 2)  # little-endian u128 = lo64 + 2^64 hi64
S = lo[:, 1].astype(np.float64) + lo[:, 0].astype(np.float64) / 2.0**64   # value of S/2^64 (float, for comparison only)
C = raw[:, 16:].copy().view("<u8").ravel()
VL = h5py.File(os.environ.get("DUNN_VLIST", "data/dunn_V_list_lfs.jld2"), "r")["V_list"][:]
D = np.fromfile(W + "Vfx_dense_1e8.bin"); old = np.memmap(W + "V_1e8.bin", dtype=np.float64, mode="r")
print("chunks:", len(S), "dense:", len(D))
k = np.arange(1, len(S) + 1) * 10000
print("chunk vs dense at multiples of 1e4 <= 1e8: max |diff| =", np.max(np.abs(S[:10000] - D[k[:10000]])))
d = S - VL
print("ours - Dunn over 1e6 checkpoints: min %.3e max %.3e ; Dunn <= ours everywhere: %s" % (d.min(), d.max(), bool(np.all(d >= -1e-12))))
print("ours - Dunn at 1e8, 1e9, 1e10:", d[9999], d[99999], d[-1])
print("dense vs old double table max |diff|:", np.max(np.abs(D - old)))
print("V_lo(1e10) =", repr(S[-1]), " count =", int(C[-1]), " monotone:", bool(np.all(np.diff(S) >= 0)))
