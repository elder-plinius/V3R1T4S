import sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from pfmodel import Model
m = Model(sys.argv[2], 50, "0.01")
for k in range(m.nT):
    S = (m.Q[k] + m.Q[k].T) / 2.0
    ev = np.linalg.eigvalsh(S)
    print("t=%d diag median %.0f | eig max %.0f | #eig<50: %d | #eig<500: %d | #eig<5000: %d" % (
        k, np.median(np.diag(m.Q[k])), ev[-1], (ev < 50).sum(), (ev < 500).sum(), (ev < 5000).sum()))
# does the covariance change across periods (beyond price scaling)?
import gzip
rows = {}
with gzip.open(sys.argv[2] + "/covariance_matrices.txt.gz", "rt") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        t, a, b, v = line.split()
        if (a, b) in (("AAPL", "AAPL"), ("AAPL", "NVDA")):
            rows.setdefault((a, b), []).append((int(t), v))
for k, v in rows.items():
    print(k, v[:4])
