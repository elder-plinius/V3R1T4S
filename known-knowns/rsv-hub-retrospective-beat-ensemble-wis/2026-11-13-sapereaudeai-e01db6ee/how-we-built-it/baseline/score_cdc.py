"""Scoring for the CDCgov RSV hub (route b), PREREG.md R2-R9.
- model-output: data/cdcgov/hub/model-output/<model>/<reference_date>-<model>.(csv|parquet) as fetched at the pinned
  commit e947ca8; target wk inc rsv hosp, output_type quantile, reference_date in 2025-09-01..2026-08-31.
- truth: target-data/oracle-output.parquet (pinned), keyed by (location, target_end_date).
- WIS: wis.wis_pinball on the 23 levels (checked against wis_interval on every scored row).
- stationary bootstrap (Politis-Romano) over reference dates, ratio-of-means statistic (copied from run 2026-11-13-0104).
"""
import os, sys, glob
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wis import LEVELS, wis_pinball, wis_interval  # noqa: E402

LEVS = [round(float(x), 4) for x in LEVELS]
TARGET = "wk inc rsv hosp"
WINDOW = ("2025-09-01", "2026-08-31")
K = ["reference_date", "location", "horizon"]


def _loc(s):
    s = s.astype(str)
    return s.where(s == "US", s.str.zfill(2))


def read_one(f):
    d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype={"location": str, "output_type_id": str})
    d["location"] = _loc(d["location"])
    d["reference_date"] = pd.to_datetime(d["reference_date"]).dt.strftime("%Y-%m-%d")
    d["target_end_date"] = pd.to_datetime(d["target_end_date"]).dt.strftime("%Y-%m-%d")
    d["horizon"] = d["horizon"].astype(int)
    d = d[(d.target.astype(str) == TARGET) & (d.output_type.astype(str) == "quantile")].copy()
    d["lev"] = pd.to_numeric(d.output_type_id, errors="coerce").round(4)
    return d[["reference_date", "location", "horizon", "target_end_date", "lev", "value"]]


def load_models(mo_dir, models=None, window=WINDOW):
    parts = []
    for f in sorted(glob.glob(os.path.join(mo_dir, "*", "*"))):
        if not (f.endswith(".parquet") or f.endswith(".csv")):
            continue
        m = os.path.basename(os.path.dirname(f))
        if models and m not in models:
            continue
        rd = os.path.basename(f)[:10]
        if not (window[0] <= rd <= window[1]):
            continue
        d = read_one(f)
        d["model_id"] = m
        parts.append(d)
    return pd.concat(parts, ignore_index=True)


def wide(d):
    W = d.pivot_table(index=["model_id"] + K + ["target_end_date"], columns="lev", values="value", aggfunc="first")
    W = W[[x for x in LEVS if x in W.columns]]
    n0 = len(W)
    W = W.dropna()
    if len(W.columns) != 23:
        raise SystemExit("missing levels")
    return W.reset_index(), n0 - len(W)


def load_truth(oracle_path):
    o = pd.read_parquet(oracle_path)
    # the oracle repeats each value once per output_type (quantile, sample); scoring uses the quantile rows
    o = o[(o.target == TARGET) & (o.output_type == "quantile")].copy()
    o["location"] = _loc(o["location"])
    o["target_end_date"] = pd.to_datetime(o["target_end_date"]).dt.strftime("%Y-%m-%d")
    if o.duplicated(["location", "target_end_date"]).any():
        raise SystemExit("duplicate oracle rows")
    return o.set_index(["location", "target_end_date"]).oracle_value


def truth_from_vintage(ts_path, as_of=None, first_report=False):
    ts = pd.read_parquet(ts_path)
    ts = ts[ts.target == TARGET].copy()
    ts["as_of"] = ts.as_of.astype(str)
    ts["target_end_date"] = ts.target_end_date.astype(str)
    ts["location"] = _loc(ts["location"])
    if first_report:
        ts = ts.sort_values("as_of").drop_duplicates(["location", "target_end_date"], keep="first")
    else:
        ts = ts[ts.as_of == as_of]
    return ts.set_index(["location", "target_end_date"]).observation


def score_wide(W, truth):
    S = W.copy()
    S["y"] = truth.reindex(list(zip(S.location, S.target_end_date))).to_numpy()
    S = S[~S.y.isna()].copy()
    Q = S[LEVS].to_numpy(float)
    y = S.y.to_numpy(float)
    S["wis"] = wis_pinball(Q, y)
    S["wis_int"] = wis_interval(Q, y)
    S["ae"] = np.abs(y - Q[:, 11])
    S["cov50"] = ((y >= Q[:, 6]) & (y <= Q[:, 16])).astype(float)
    S["cov95"] = ((y >= Q[:, 1]) & (y <= Q[:, 21])).astype(float)
    return S


def stationary_bootstrap_idx(n, L, B, seed):
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


def paired_bootstrap(A, Bm, L=3, B=10000, seed=20261113):
    A = np.asarray(A, float); Bm = np.asarray(Bm, float)
    n = len(A)
    rel = A[:, 0].sum() / A[:, 1].sum() / (Bm[:, 0].sum() / Bm[:, 1].sum()) - 1
    idx = stationary_bootstrap_idx(n, L, B, seed)
    ma = A[idx, 0].sum(1) / A[idx, 1].sum(1)
    mb = Bm[idx, 0].sum(1) / Bm[idx, 1].sum(1)
    r = ma / mb - 1
    return dict(n_dates=n, rel=rel, rel_lo=float(np.quantile(r, 0.05)), rel_hi=float(np.quantile(r, 0.95)))


def compare(ours, theirs, label, L=3):
    """ours/theirs: scored task tables (K + wis); compared on theirs' scored tasks (our forecast for the same task)."""
    J = theirs[K + ["wis"]].merge(ours[K + ["wis"]], on=K, how="left", suffixes=("_c", "_o"))
    missing = int(J.wis_o.isna().sum())
    J = J.dropna(subset=["wis_o"])
    g = J.groupby("reference_date").agg(so=("wis_o", "sum"), sc=("wis_c", "sum"), n=("wis_o", "size")).sort_index()
    A = np.column_stack([g.so, g.n]); Bm = np.column_stack([g.sc, g.n])
    bs = paired_bootstrap(A, Bm, L=L)
    rng = np.random.default_rng(1)
    d = g.so / g.n - g.sc / g.n
    w = g.n.to_numpy(float)
    obs = float(np.sum(d * w) / w.sum())
    flips = rng.choice([-1, 1], size=(10000, len(d)))
    perm = (flips * d.to_numpy() * w).sum(1) / w.sum()
    return dict(comparator=label, tasks=len(J), missing_ours=missing, dates=len(g), wis_ours=J.wis_o.mean(),
                wis_comp=J.wis_c.mean(), rel=bs["rel"], rel_lo=bs["rel_lo"], rel_hi=bs["rel_hi"],
                signflip_p=float(np.mean(perm <= obs))), J
