"""Load the HopkinsIDD RSV hub model-output (pinned commit 6bf251ac) into one long table.
Columns: model_id, file, retro (bool), origin_date, target, horizon, location, age_group, output_type, output_type_id, value,
target_end_date (= origin_date + 7*horizon - 1, as in the hub's scripts/ensemble.R).
Reads only data/hopkins/hub/model-output/ (as fetched)."""
import os, glob, sys
import pandas as pd, numpy as np

RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MO = os.path.join(RUN, "data", "hopkins", "hub", "model-output")


def read_one(f):
    if f.endswith(".parquet"):
        d = pd.read_parquet(f)
    else:
        d = pd.read_csv(f, dtype={"location": str, "age_group": str})
    d["location"] = d["location"].astype(str).str.zfill(2).where(d["location"].astype(str) != "US", "US")
    d["origin_date"] = pd.to_datetime(d["origin_date"]).dt.strftime("%Y-%m-%d")
    d["age_group"] = d["age_group"].astype(str)
    d["target"] = d["target"].astype(str)
    d["output_type"] = d["output_type"].astype(str)
    d["horizon"] = d["horizon"].astype(int)
    return d


def load_all():
    parts = []
    for f in sorted(glob.glob(os.path.join(MO, "*", "*"))):
        if not (f.endswith(".parquet") or f.endswith(".csv")):
            continue
        m = os.path.basename(os.path.dirname(f))
        d = read_one(f)
        d["model_id"] = m
        d["file"] = os.path.basename(f)
        d["retro"] = "-RETRO" in os.path.basename(f)
        parts.append(d)
    d = pd.concat(parts, ignore_index=True)
    d["target_end_date"] = (pd.to_datetime(d.origin_date) + pd.to_timedelta(7 * d.horizon - 1, unit="D")).dt.strftime("%Y-%m-%d")
    return d


def quantile_wide(d, levels):
    """Quantile rows -> one row per (model, file, origin, target, horizon, location, age) with 23 columns; drops tasks
    that do not have all levels."""
    q = d[(d.output_type == "quantile")].copy()
    q["lev"] = q.output_type_id.astype(float).round(4)
    keys = ["model_id", "file", "retro", "origin_date", "target", "horizon", "location", "age_group", "target_end_date"]
    W = q.pivot_table(index=keys, columns="lev", values="value", aggfunc="first")
    lv = [round(float(x), 4) for x in levels]
    missing = [x for x in lv if x not in W.columns]
    if missing:
        raise SystemExit("missing levels %s" % missing)
    W = W[lv]
    n0 = len(W)
    W = W.dropna()
    return W.reset_index(), n0 - len(W)


if __name__ == "__main__":
    d = load_all()
    print("rows", len(d), "files", d.file.nunique())
    for m, g in d.groupby("model_id"):
        lv = sorted(g[g.output_type == "quantile"].output_type_id.astype(float).round(4).unique())
        print(m, "files", g.file.nunique(), "retro files", g[g.retro].file.nunique(), "ages", sorted(g.age_group.unique()),
              "hz", sorted(g.horizon.unique()), "nloc", g.location.nunique(), "types", sorted(g.output_type.unique()),
              "targets", sorted(g.target.unique()), "nlev", len(lv))
