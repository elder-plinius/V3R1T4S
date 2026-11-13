"""Rebuild the KIT-frozen_baseline (the paper's FrozenBaseline: all quantiles = the 7-day sum as published on the
forecast date) from the hub's RAW triangle at the 2022-08-08 commit truncated to cells d + k <= t, and compare with the
evaluation repository's file data/submissions_KIT-frozen_baseline.csv.gz (built by the authors from the hub's dated
preprocessed vintages). Usage: python -I frozen_baseline_check.py <run_folder> <out_txt>"""
import sys, os
import numpy as np, pandas as pd
RUN, OUT = sys.argv[1], sys.argv[2]
F = pd.read_csv(os.path.join(RUN, "data/hub/truth/11c745322c055cfbd4f0c8f72241642a50aea399/COVID-19_hospitalizations.csv"))
vc = [f"value_{k}d" for k in range(81)]
F["date"] = pd.to_datetime(F.date)
B = pd.read_csv(os.path.join(RUN, "data/eval_data/submissions_KIT-frozen_baseline.csv.gz"))
B = B[B.type == "quantile"]
Bq = B.groupby(["location", "age_group", "forecast_date", "target_end_date"]).value.agg(["min", "max"]).reset_index()
assert (Bq["min"] == Bq["max"]).all() or Bq["min"].isna().any()
rows = []
for (loc, ag), G in F.groupby(["location", "age_group"]):
    G = G.set_index("date").sort_index()
    M = G[vc].to_numpy(float)
    dates = G.index
    for t in pd.date_range("2021-11-22", "2022-04-29"):
        lag = (t - dates).days.values
        mask = (np.arange(81)[None, :] <= lag[:, None]) & (lag[:, None] >= 0)
        asof = np.where(mask, np.nan_to_num(M), 0.0).sum(axis=1)
        s = pd.Series(asof, index=dates)
        for h in range(-28, 1):
            e = t + pd.Timedelta(days=h)
            w = s.loc[e - pd.Timedelta(days=6): e]
            rows.append((loc, ag, t.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"), float(w.sum()) if len(w) == 7 else np.nan))
R = pd.DataFrame(rows, columns=["location", "age_group", "forecast_date", "target_end_date", "raw_trunc"])
J = Bq.merge(R, on=["location", "age_group", "forecast_date", "target_end_date"], how="left")
d = (J["min"] - J.raw_trunc).abs()
lines = [f"baseline targets {len(J)}; equal to raw-truncation 7-day sums: {(d < 1e-9).sum()}; differ: {(d >= 1e-9).sum()}; "
         f"NaN: {d.isna().sum()}; max |diff| {d.max()}; sum |diff| {d.sum()}"]
bad = J[d >= 1e-9]
if len(bad):
    lines.append("differences by location:\n" + bad.groupby("location").size().to_string())
    lines.append(bad.head(10).to_string())
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
