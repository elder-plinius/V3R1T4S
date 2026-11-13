"""Re-derive the hub's row-exclusion rules (code/evaluation/load_and_score_models.r + EuroForecastHub::add_status and
score_forecasts, read as text) on every row of the fetched forecast files, and compare the resulting row set with
the published scores.csv row set.
Usage: python -I rederive_exclusions.py <run_data_dir> <recomputed_rows.csv.gz> <out_txt>"""
import sys, os
import numpy as np, pandas as pd
data, recf, outf = sys.argv[1], sys.argv[2], sys.argv[3]
KEY = ["model", "target_variable", "forecast_date", "horizon", "location"]
pub = pd.read_csv(os.path.join(data, "scores.csv"), dtype={"location": str})
rec = pd.read_csv(recf, dtype={"location": str})
n0 = int((rec["horizon"] == 0).sum())
rec = rec[rec["horizon"].between(1, 4)].copy()  # the hub's targets are 1-4 wk ahead
tdir = os.path.join(data, "truth")
def rd(p): return pd.read_csv(p, dtype={"location": str})
cases = rd(os.path.join(tdir, "ECDC", "truth_ECDC-Incident Cases.csv"))
owid = rd(os.path.join(tdir, "OWID", "truth_OWID-Incident Hospitalizations.csv"))
# add_status as written: hosp status from the OWID file, case AND death status from the ECDC *cases* file
st = pd.concat([owid.assign(target_variable="inc hosp"), cases.assign(target_variable="inc case"),
                cases.assign(target_variable="inc death")])[["target_variable", "location", "date", "status"]]
st = st.rename(columns={"date": "target_end_date"}).drop_duplicates(["target_variable", "location", "target_end_date"])
an = rd(os.path.join(tdir, "anomalies", "anomalies.csv"))
R = rec.merge(st, on=["target_variable", "location", "target_end_date"], how="left")
R["status"] = R["status"].fillna("final")
R["is_anomaly"] = R.merge(an[["target_variable", "location", "target_end_date"]].assign(a=1),
                          on=["target_variable", "location", "target_end_date"], how="left")["a"].notna().values
prev = (pd.to_datetime(R["forecast_date"]) - pd.Timedelta(days=2)).dt.strftime("%Y-%m-%d")
R["prev_end"] = prev
R["after_anomaly"] = R.merge(an[["target_variable", "location", "target_end_date"]].rename(
    columns={"target_end_date": "prev_end"}).assign(a=1), on=["target_variable", "location", "prev_end"],
    how="left")["a"].notna().values
R["has_truth"] = R["true_value"].notna()
R["scorable_q"] = (R["nq"] == 23) | (R["nq"] == 1)
R["kept"] = R.has_truth & (R.status == "final") & ~R.is_anomaly & ~R.after_anomaly & R.scorable_q
P = pub[KEY].assign(in_pub=True)
M = R.merge(P, on=KEY, how="outer", indicator=True)
lines = [f"rows with horizon 0 ('0 wk ahead') dropped (not a hub target): {n0}"]
lines.append(f"rows in fetched files (hub targets, horizons 1-4): {len(R)}")
lines.append(f"published rows: {len(pub)}")
for col in ["has_truth", "scorable_q"]:
    lines.append(f"rows failing {col}: {int((~R[col]).sum())}")
lines.append(f"rows with status != final: {int((R.status != 'final').sum())}")
lines.append(f"rows on an anomaly week (truth anti-join): {int(R.is_anomaly.sum())}")
lines.append(f"rows of forecasts made directly after an anomaly: {int(R.after_anomaly.sum())}")
lines.append(f"rows kept by the re-derived rules: {int(R.kept.sum())}")
kept = M[M["_merge"] != "right_only"]
both = M[M["_merge"] == "both"]
lines.append(f"published rows found in fetched files: {len(both)}; published rows not in any fetched file: {int((M['_merge']=='right_only').sum())}")
lines.append(f"kept AND published: {int((both.kept == True).sum())}")
lines.append(f"kept but NOT published: {int(((M['_merge']=='left_only') & (M.kept == True)).sum())}")
lines.append(f"published but NOT kept: {int((both.kept == False).sum())}")
X = M[(M['_merge'] == 'left_only') & (M.kept == True)]
if len(X):
    lines.append("kept-but-not-published by model/target_variable:")
    lines.append(X.groupby(["model", "target_variable"]).size().to_string())
    lines.append("kept-but-not-published by target_end_date (first 20):")
    lines.append(X.groupby("target_end_date").size().head(20).to_string())
Y = both[both.kept == False]
if len(Y):
    lines.append("published-but-not-kept, reason counts:")
    for c in ["has_truth", "scorable_q"]:
        lines.append(f"  not {c}: {int((~Y[c].astype(bool)).sum())}")
    lines.append(f"  status != final: {int((Y.status != 'final').sum())}; anomaly: {int(Y.is_anomaly.sum())}; after anomaly: {int(Y.after_anomaly.sum())}")
    lines.append(Y.groupby(["model", "target_variable", "location"]).size().head(30).to_string())
D = M[M['_merge'] == 'left_only']
lines.append("all fetched-file rows NOT published, by reason (a row may have several):")
lines.append(f"  no truth: {int((~D.has_truth.astype(bool)).sum())}; status != final: {int((D.status != 'final').sum())}; anomaly: {int(D.is_anomaly.astype(bool).sum())}; after anomaly: {int(D.after_anomaly.astype(bool).sum())}; not 23 quantiles/point: {int((~D.scorable_q.astype(bool)).sum())}")
open(outf, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
