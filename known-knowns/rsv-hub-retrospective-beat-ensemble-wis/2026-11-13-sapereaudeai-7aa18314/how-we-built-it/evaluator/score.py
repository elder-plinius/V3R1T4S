"""Scoring for the HopkinsIDD RSV hub (route a).
- truth: target-data/2026-06-05_rsvnet_hospitalization.csv at hub commit 6bf251ac (target "inc hosp"), keyed by
  (location, age_group, target_end_date).
- WIS: wis.wis_pinball on the hub's 23 levels (== scoringutils/hubEvals WIS with weigh = TRUE, median counted once;
  checked against the interval form in wis.py self-test and in validate_scorer.py).
- stationary bootstrap (Politis & Romano 1994) over reference dates, ratio-of-means statistic.
"""
import os, sys
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wis import LEVELS, wis_pinball, wis_interval  # noqa: E402

RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TRUTH = os.path.join(RUN, "data", "hopkins", "hub", "target-data", "2026-06-05_rsvnet_hospitalization.csv")
LEVS = [round(float(x), 4) for x in LEVELS]
KEYS = ["origin_date", "horizon", "location", "age_group", "target_end_date"]


DERIVED = {"0-0.99": ["0-0.49", "0.5-0.99"], "1-4": ["1-1.99", "2-4"], "5-64": ["5-17", "18-49", "50-64"]}


def load_truth(path=TRUTH):
    """PREREG R4: direct 'inc hosp' rows, plus the submission groups as exact sums of the file's own finer groups
    (a derived value is missing if any component is missing)."""
    t = pd.read_csv(path, dtype={"location": str, "age_group": str})
    t = t[t.target == "inc hosp"].copy()
    t["target_end_date"] = pd.to_datetime(t["date"]).dt.strftime("%Y-%m-%d")
    t = t[["location", "age_group", "target_end_date", "value"]]
    if t.duplicated(["location", "age_group", "target_end_date"]).sum():
        raise SystemExit("duplicate truth rows")
    W = t.pivot(index=["location", "target_end_date"], columns="age_group", values="value")
    parts = [t]
    for g, comp in DERIVED.items():
        if g in W.columns:
            continue
        v = W[comp].sum(axis=1, min_count=len(comp))
        v[W[comp].isna().any(axis=1)] = np.nan
        parts.append(v.rename("value").reset_index().assign(age_group=g))
    T = pd.concat(parts, ignore_index=True).rename(columns={"value": "truth"})
    T = T[~T.truth.isna()]
    return T[["location", "age_group", "target_end_date", "truth"]]


def score_wide(W, truth):
    """W: wide quantile table with KEYS (+ model_id etc.) and LEVS columns. Adds truth, wis, ae, cov50, cov90."""
    S = W.merge(truth, on=["location", "age_group", "target_end_date"], how="left")
    S = S[~S.truth.isna()].copy()
    Q = S[LEVS].to_numpy(float)
    y = S.truth.to_numpy(float)
    S["wis"] = wis_pinball(Q, y)
    S["wis_int"] = wis_interval(Q, y)
    S["ae"] = np.abs(y - Q[:, 11])
    S["cov50"] = ((y >= Q[:, 6]) & (y <= Q[:, 16])).astype(float)
    S["cov90"] = ((y >= Q[:, 3]) & (y <= Q[:, 19])).astype(float)
    return S


def stationary_bootstrap_idx(n, L, B, seed):
    """B index arrays of length n, stationary bootstrap with mean block length L (geometric), wrap-around."""
    rng = np.random.default_rng(seed)
    p = 1.0 / L
    out = np.empty((B, n), dtype=int)
    for b in range(B):
        i = rng.integers(n)
        for t in range(n):
            if t > 0:
                if rng.random() < p:
                    i = rng.integers(n)
                else:
                    i = (i + 1) % n
            out[b, t] = i
    return out


def paired_bootstrap(per_date_a, per_date_b, L=3, B=10000, seed=20261113):
    """per_date_a/b: arrays (n_dates, 2) of [sum WIS, count] per reference date (chronological), on common tasks.
    Returns point relative difference (mean_a/mean_b - 1), the 90% interval, and the difference of means interval."""
    A = np.asarray(per_date_a, float); Bm = np.asarray(per_date_b, float)
    n = len(A)
    rel = A[:, 0].sum() / A[:, 1].sum() / (Bm[:, 0].sum() / Bm[:, 1].sum()) - 1
    dif = A[:, 0].sum() / A[:, 1].sum() - Bm[:, 0].sum() / Bm[:, 1].sum()
    idx = stationary_bootstrap_idx(n, L, B, seed)
    ma = A[idx, 0].sum(1) / A[idx, 1].sum(1)
    mb = Bm[idx, 0].sum(1) / Bm[idx, 1].sum(1)
    r = ma / mb - 1
    d = ma - mb
    return dict(n_dates=n, rel=rel, rel_lo=np.quantile(r, 0.05), rel_hi=np.quantile(r, 0.95),
                dif=dif, dif_lo=np.quantile(d, 0.05), dif_hi=np.quantile(d, 0.95))
