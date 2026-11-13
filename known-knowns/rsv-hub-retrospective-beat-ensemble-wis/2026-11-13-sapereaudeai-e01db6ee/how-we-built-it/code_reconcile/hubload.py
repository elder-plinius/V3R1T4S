"""Loader for CDCgov/rsv-forecast-hub 2025-26 model-output (written for run 2026-11-13-0349, landscape lens).
Returns wide quantile tables keyed by (model, reference_date, location, horizon, target, target_end_date)."""
import os, numpy as np, pandas as pd

LEVELS = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,
          0.8, 0.85, 0.9, 0.95, 0.975, 0.99]

def _d(s):
    return pd.to_datetime(s).dt.strftime("%Y-%m-%d")

def _loc(s):
    s = s.astype(str)
    return s.where(~s.str.fullmatch(r"\d"), "0" + s)

def load_models(hub, models=None, first="2025-09-01", last="2026-08-31"):
    mo = os.path.join(hub, "model-output")
    parts = []
    for m in sorted(os.listdir(mo)):
        if models and m not in models:
            continue
        for f in sorted(os.listdir(os.path.join(mo, m))):
            rd = f[:10]
            if not (first <= rd <= last):
                continue
            p = os.path.join(mo, m, f)
            d = pd.read_parquet(p) if f.endswith(".parquet") else pd.read_csv(p, dtype={"location": str, "output_type_id": str})
            d = d[d["output_type"] == "quantile"].copy()
            d["model"] = m
            d["reference_date"] = _d(d["reference_date"]); d["target_end_date"] = _d(d["target_end_date"])
            d["location"] = _loc(d["location"]); d["level"] = d["output_type_id"].astype(float).round(4)
            parts.append(d[["model", "reference_date", "location", "horizon", "target", "target_end_date", "level", "value"]])
    a = pd.concat(parts, ignore_index=True)
    w = a.pivot_table(index=["model", "reference_date", "location", "horizon", "target", "target_end_date"],
                      columns="level", values="value", aggfunc="first")
    w = w[[round(l, 4) for l in LEVELS]]
    return w.reset_index()

def oracle(hub):
    o = pd.read_parquet(os.path.join(hub, "target-data", "oracle-output.parquet"))
    o = o[o["output_type"] == "quantile"].copy()
    o["target_end_date"] = _d(o["target_end_date"]); o["location"] = _loc(o["location"])
    return o.drop_duplicates(["target", "location", "target_end_date"])[["target", "location", "target_end_date", "oracle_value"]]

def wis(Q, levels, y):
    Q = np.asarray(Q, float); y = np.asarray(y, float)[:, None]; L = np.asarray(levels, float)[None, :]
    return np.mean(2.0 * ((y < Q).astype(float) - L) * (Q - y), axis=1)
