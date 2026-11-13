"""Independent Python re-implementation of the hubverse / scoringutils (1.x score() + summarise_scores()) quantile scores
used by the FluSight WIS report. Written from the documented definitions:
  WIS (Bracher et al. 2021, PLoS Comput Biol 17:e1008618; scoringutils weigh=TRUE, count_median_twice=FALSE)
    = 1/(K+1/2) * ( 1/2 |y-m| + sum_k alpha_k/2 * IS_alpha_k ),  IS_a = (u-l) + 2/a (l-y)1{y<l} + 2/a (y-u)1{y>u}
    which equals the mean over the 23 quantile levels of 2 x pinball loss.
  relative skill (scoringutils pairwise_comparison): ratio(A,B) = sum WIS_A / sum WIS_B over common forecasts;
    theta_A = geometric mean over all models B (incl. A itself, ratio 1; NA ratios dropped); scaled = theta_A / theta_base.
"""
import numpy as np

LEVELS = np.array([0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,
                   0.8, 0.85, 0.9, 0.95, 0.975, 0.99])
MED = 11

def wis_pinball(Q, y):
    """Q: (n, 23) quantiles in LEVELS order; y: (n,). Mean over levels of 2*pinball."""
    y = np.asarray(y, float)[:, None]
    ind = (y < Q).astype(float)
    return np.mean(2.0 * (ind - LEVELS[None, :]) * (Q - y), axis=1)

def wis_interval(Q, y):
    """Bracher et al. interval form (independent cross-check of wis_pinball)."""
    y = np.asarray(y, float)
    K = 11
    tot = 0.5 * np.abs(y - Q[:, MED])
    for k in range(K):
        l, u = Q[:, k], Q[:, 22 - k]
        alpha = 2 * LEVELS[k]
        IS = (u - l) + (2 / alpha) * (l - y) * (y < l) + (2 / alpha) * (y - u) * (y > u)
        tot = tot + alpha / 2 * IS
    return tot / (K + 0.5)

def ae_median(Q, y):
    return np.abs(np.asarray(y, float) - Q[:, MED])

def coverage(Q, y, rng):
    lo = {50: 6, 95: 1}[rng]; hi = 22 - lo
    y = np.asarray(y, float)
    return ((y >= Q[:, lo]) & (y <= Q[:, hi])).astype(float)

def relative_skill(score_matrix, models, baseline):
    """score_matrix: (n_units, n_models) per-forecast WIS, NaN where a model has no scored forecast.
    Returns dict model -> scaled relative skill (theta / theta_baseline), and theta."""
    S = np.asarray(score_matrix, float)
    have = ~np.isnan(S)
    Sz = np.where(have, S, 0.0)
    m = len(models)
    logs = np.full((m, m), np.nan)
    for a in range(m):
        logs[a, a] = 0.0
        for b in range(a + 1, m):
            mask = have[:, a] & have[:, b]
            if not mask.any():
                continue
            r = Sz[mask, a].sum() / Sz[mask, b].sum()
            logs[a, b] = np.log(r); logs[b, a] = -np.log(r)
    theta = np.exp(np.nanmean(logs, axis=1))
    tb = theta[models.index(baseline)]
    return {mo: theta[i] / tb for i, mo in enumerate(models)}, {mo: theta[i] for i, mo in enumerate(models)}

if __name__ == "__main__":
    # self-tests: known positive (point forecast -> WIS = |y - m|), two forms agree, known negative (wrong normalisation differs)
    rng = np.random.default_rng(1)
    from statistics import NormalDist
    z = np.array([NormalDist().inv_cdf(p) for p in LEVELS])
    Q = 100 + 20 * z[None, :] + rng.normal(0, 5, (1000, 1))
    Q = np.sort(Q, axis=1)
    y = rng.normal(100, 30, 1000)
    a, b = wis_pinball(Q, y), wis_interval(Q, y)
    print("max |pinball - interval| =", np.max(np.abs(a - b)))
    P = np.full((3, 23), 50.0); yy = np.array([40.0, 50.0, 75.0])
    print("point forecast WIS =", wis_pinball(P, yy), "expected", np.abs(yy - 50))
    wrong = np.mean(2 * ((y[:, None] < Q) - LEVELS) * (Q - y[:, None]), axis=1) * 23 / 24   # a 1/12-style normalisation
    print("known negative: 1/12 normalisation differs by", np.max(np.abs(wrong - a)) > 1e-6)
    S = np.array([[1, 2, np.nan], [2, 4, 1], [3, 6, 3]], float)
    rs, th = relative_skill(S, ["A", "B", "C"], "B")
    print("relative skill toy", {k: round(v, 6) for k, v in rs.items()})
    ok = np.max(np.abs(a - b)) < 1e-9 and np.allclose(wis_pinball(P, yy), np.abs(yy - 50))
    print("SELFTEST", "PASS" if ok else "FAIL")
