"""Self-test of wis.py against an independent pinball (quantile-score) form: mean over the 23 quantiles of
2*(1(y<q)-tau)*(q-y). Known positive: a point-mass forecast at m gives WIS = |y-m|*(1/23)*... checked as
(identical quantiles q=m) => WIS = |y - m| * mean_tau(2*|1(y<m)-tau|) computed directly; plus the decomposition
sums to WIS. Known negative: a 1/(K+1) normalisation of the interval form differs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from wis import wis_decomp, Q23
rng = np.random.default_rng(20261113)
Q = np.sort(rng.lognormal(5, 1, (20000, 23)), axis=1); y = rng.lognormal(5, 1.3, 20000)
pin = np.mean(2 * ((y[:, None] < Q).astype(float) - Q23[None, :]) * (Q - y[:, None]), axis=1)
d = wis_decomp(Q, y)
e1 = np.max(np.abs(d["wis"] - pin))
e2 = np.max(np.abs(d["sharpness"] + d["underprediction"] + d["overprediction"] - d["wis"]))
# known positive: all quantiles equal m -> sharpness 0, WIS = mean_tau 2|1(y<m)-tau||m-y|
M = np.full((3, 23), 50.0); yy = np.array([40.0, 50.0, 80.0]); dp = wis_decomp(M, yy)
exp = np.array([np.mean(2 * np.abs((v < 50) - Q23) * abs(50 - v)) for v in yy])
pos = np.allclose(dp["wis"], exp) and np.allclose(dp["sharpness"], 0)
# known negative: interval form with 1/(K+1) and full-weight median differs
alt = np.abs(y - Q[:, 11])
for k in range(11):
    a = 2 * Q23[k]; l, u = Q[:, k], Q[:, 22 - k]
    alt = alt + a / 2 * ((u - l) + 2 / a * (l - y) * (y < l) + 2 / a * (y - u) * (y > u))
alt = alt / 12
neg = np.max(np.abs(alt - d["wis"])) > 1e-6
print("max |wis - pinball form| =", e1); print("max |components - wis| =", e2)
print("known positive (point mass):", pos); print("known negative (1/(K+1) form differs):", neg)
print("SELFTEST", "PASS" if (e1 < 1e-9 and e2 < 1e-9 and pos and neg) else "FAIL")
