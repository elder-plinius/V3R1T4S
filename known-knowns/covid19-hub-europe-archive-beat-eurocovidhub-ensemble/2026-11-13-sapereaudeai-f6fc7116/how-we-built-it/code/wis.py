"""WIS as scoringutils 1.x computes it for a 23-quantile forecast (Bracher et al. 2021):
WIS = (0.5|y-m| + sum_k alpha_k/2 * IS_alpha_k) / (K + 0.5), which equals the mean over the 23 quantile rows of the
range score each row carries. Decomposition: sharpness (dispersion), underprediction, overprediction."""
import numpy as np
Q23 = np.array([0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99])

def wis_decomp(Q, y):
    """Q: (n, 23) predictions at Q23 (columns in Q23 order); y: (n,). Returns dict of arrays."""
    Q = np.asarray(Q, float); y = np.asarray(y, float)
    m = Q[:, 11]
    K = 11
    disp = np.zeros_like(y); under = np.maximum(y - m, 0.0) * 0.5; over = np.maximum(m - y, 0.0) * 0.5
    for k in range(K):
        lo, hi = Q[:, k], Q[:, 22 - k]
        alpha = 2 * Q23[k]
        disp += alpha / 2 * (hi - lo)
        under += np.maximum(y - hi, 0.0)
        over += np.maximum(lo - y, 0.0)
    d = K + 0.5
    disp, under, over = disp / d, under / d, over / d
    # contrast only: interval form with 1/(K+1) normalisation and the median at full weight
    alt = (disp * d + (under + over) * d + 0.5 * np.abs(y - m)) / (K + 1)
    return {"wis_alt_k1": alt, "wis": disp + under + over, "sharpness": disp, "underprediction": under, "overprediction": over,
            "ae_median": np.abs(y - m),
            "cov_50": ((y >= Q[:, 6]) & (y <= Q[:, 16])).astype(float),
            "cov_95": ((y >= Q[:, 1]) & (y <= Q[:, 21])).astype(float)}

def wis_point(m, y):
    """Point-only forecast converted to a median (EuroForecastHub): one range-0 row, WIS = |y - m|."""
    m = np.asarray(m, float); y = np.asarray(y, float)
    return {"wis_alt_k1": np.abs(y - m), "wis": np.abs(y - m), "sharpness": np.zeros_like(y), "underprediction": np.maximum(y - m, 0.0),
            "overprediction": np.maximum(m - y, 0.0), "ae_median": np.abs(y - m),
            "cov_50": np.full_like(y, np.nan), "cov_95": np.full_like(y, np.nan)}
