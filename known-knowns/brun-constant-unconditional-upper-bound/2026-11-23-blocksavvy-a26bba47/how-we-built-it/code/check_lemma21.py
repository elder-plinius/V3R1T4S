"""Empirical consistency check (not a proof) of Dunn/Klyve Lemma 2.1 shape on our exact table:
   V(z) >= V(L) + (log z - log L)/(2 pi2) + c3 (3/sqrt z - 9/sqrt L)   for L < z <= 1e10, L in {1e6, 1e7, 1e8, 1e9}.
   Also reports E(z) = V(z) - log(z)/(2 C2) and sqrt(z)*|E(z) - E(1e10)| to see whether a c/sqrt(z) error of size ~12.6 is plausible."""
import os, numpy as np, math
W = os.environ.get("BRUN_WORK", "work") + "/"
raw = np.fromfile(W + "Vfx_chunks_1e10.bin", dtype=np.uint8).reshape(-1, 24)
u = raw[:, :16].copy().view("<u8").reshape(-1, 2); V = u[:, 1].astype(np.float64) + u[:, 0].astype(np.float64) / 2.0**64
z = np.arange(1, len(V) + 1, dtype=np.float64) * 1e4
C2 = 0.66016181584686957; pi2u = 0.6601619; c3 = 12.6244
for L in (1e6, 1e7, 1e8, 1e9):
    k = int(L // 1e4) - 1; m = z > L
    slack = V[m] - (V[k] + (np.log(z[m]) - math.log(L)) / (2 * pi2u) + c3 * (3 / np.sqrt(z[m]) - 9 / math.sqrt(L)))
    print("L=%.0e: min slack %.3e (needs >= 0), at z=%.3e; slack with c3=0: %.3e" % (L, slack.min(), z[m][slack.argmin()],
          (V[m] - (V[k] + (np.log(z[m]) - math.log(L)) / (2 * pi2u))).min()))
E_ = V - np.log(z) / (2 * C2); Einf = E_[-1]
for a, b in ((1e4, 1e6), (1e6, 1e8), (1e8, 1e10)):
    m = (z >= a) & (z <= b); print("z in [%.0e,%.0e]: E range [%.9f, %.9f]; max sqrt(z)|E-E(1e10)| = %.3f" % (a, b, E_[m].min(), E_[m].max(), (np.sqrt(z[m]) * np.abs(E_[m] - Einf)).max()))
