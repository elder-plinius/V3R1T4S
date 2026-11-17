"""Reconcile the p3 recomputation with the published row-level scores of the arXiv 2605.16238 analysis repository
(github.com/sarahmart/epi-hub-analysis at commit 2294a6331e6317059b49b20da893a86b2f0751dd,
data/processed/rsv/scores.parquet and data/season_summaries/rsv_summary.csv; its loader keeps only .csv model-output
files, src/load_hub.py keep_forecast_file).
usage: python p3_reconcile_k2.py <hub dir> <scores.parquet> <rsv_summary.csv> <out file>
For every published row (model, reference_date, location, horizon, target_end_date) it rescores the hub's own forecast
with wis.py twice: against the published truth_value and against the pinned oracle-output, and reports the agreement."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wis import LEVELS, wis_pinball  # noqa: E402

hub, sp, summ, out = sys.argv[1:5]
LEVS = [round(float(x), 4) for x in LEVELS]
TG = "wk inc rsv hosp"
K2 = pd.read_parquet(sp)
K2["reference_date"] = pd.to_datetime(K2.reference_date).dt.strftime("%Y-%m-%d")
K2["target_end_date"] = pd.to_datetime(K2.target_end_date).dt.strftime("%Y-%m-%d")
K2["location"] = K2.location.astype(str)
lines = ["published rows: %d, models: %s, reference dates %s..%s (%d), targets %s" % (
    len(K2), ", ".join(sorted(K2.model_id.unique())), K2.reference_date.min(), K2.reference_date.max(),
    K2.reference_date.nunique(), sorted(K2.target.unique()))]
parts = []
for m in sorted(K2.model_id.unique()):
    for f in sorted(glob.glob(os.path.join(hub, "model-output", m, "*"))):
        d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype={"location": str, "output_type_id": str})
        d = d[(d.target.astype(str) == TG) & (d.output_type.astype(str) == "quantile")].copy()
        d["location"] = d.location.astype(str).where(d.location.astype(str) == "US", d.location.astype(str).str.zfill(2))
        for c in ("reference_date", "target_end_date"):
            d[c] = pd.to_datetime(d[c]).dt.strftime("%Y-%m-%d")
        d["lev"] = pd.to_numeric(d.output_type_id).round(4)
        d["model_id"] = m
        parts.append(d[["model_id", "reference_date", "location", "horizon", "target_end_date", "lev", "value"]])
D = pd.concat(parts)
key = ["model_id", "reference_date", "location", "horizon", "target_end_date"]
W = D.pivot_table(index=key, columns="lev", values="value", aggfunc="first")[LEVS].reset_index()
J = K2.merge(W, on=key, how="left")
miss = int(J[LEVS[0]].isna().sum())
lines.append("published rows without a matching hub forecast: %d" % miss)
J = J.dropna(subset=LEVS)
Q = J[LEVS].to_numpy(float)
w_pub_truth = wis_pinball(Q, J.truth_value.to_numpy(float))
o = pd.read_parquet(os.path.join(hub, "target-data", "oracle-output.parquet"))
o = o[(o.target == TG) & (o.output_type == "quantile")].copy()
o["location"] = o.location.astype(str)
o["target_end_date"] = pd.to_datetime(o.target_end_date).dt.strftime("%Y-%m-%d")
J["oracle"] = o.set_index(["location", "target_end_date"]).oracle_value.reindex(list(zip(J.location, J.target_end_date))).to_numpy()
w_oracle = wis_pinball(Q, J.oracle.to_numpy(float))
dif = np.abs(w_pub_truth - J.wis.to_numpy(float))
lines.append("our WIS with the PUBLISHED truth_value vs the published wis, all %d rows: max |diff| %.3g, rows with |diff| > 1e-6: %d" % (
    len(J), dif.max(), int((dif > 1e-6).sum())))
tv = J.drop_duplicates(["location", "target_end_date"])
nd = int((tv.truth_value != tv.oracle).sum())
lines.append("truth values: published truth_value differs from the pinned oracle-output on %d of %d (location, target_end_date) pairs" % (nd, len(tv)))
J["w_oracle"] = w_oracle; J["w_pub"] = w_pub_truth
sub = J[(J.location != "US") & J.horizon.between(0, 3)]
S = pd.read_csv(summ)
lines.append("per model on the published summary task set (52 states, horizons 0-3): published mean WIS | ours with published truth | ours with pinned oracle")
for m, g in sub.groupby("model_id"):
    pub = S.loc[S.Model == m, "Mean WIS"]
    lines.append("  %-28s tasks %5d  %s | %.10g | %.6f" % (m, len(g), ("%.10g" % pub.iloc[0]) if len(pub) else "(no row)", g.w_pub.mean(), g.w_oracle.mean()))
lines.append("UGA_flucast-INFLAenza: absent from the published rows; the published loader keeps only .csv model-output files and "
             "UGA_flucast-INFLAenza submits .parquet files (%d of its in-season files are .parquet)." % len(
                 [f for f in glob.glob(os.path.join(hub, "model-output", "UGA_flucast-INFLAenza", "*")) if f.endswith(".parquet")]))
open(out, "w", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
