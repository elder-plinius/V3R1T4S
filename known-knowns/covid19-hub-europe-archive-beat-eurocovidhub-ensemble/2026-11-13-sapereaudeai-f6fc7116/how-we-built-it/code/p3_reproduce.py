"""p3: recompute the European COVID-19 Forecast Hub archive's evaluation/scores.csv per-model WIS decomposition
from data-processed and the truth data.
Usage: python -I p3_reproduce.py <data_dir> <out_dir> [truth=primary|owidhosp|final0927|final0927_owidhosp]
Reads <data>/scores.csv, <data>/hub/data-processed/<model>/<file>.csv (file name from <data>/file_map.tsv if
listed there, else <forecast_date>-<model>.csv), <data>/truth/ECDC/truth_ECDC-Incident {Cases,Deaths,Hospitalizations}.csv."""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)  # all-NaN slices for components that are 0
import numpy as np, pandas as pd
from wis import wis_decomp, wis_point, Q23

data, out = sys.argv[1], sys.argv[2]
truth_mode = sys.argv[3] if len(sys.argv) > 3 else "primary"
os.makedirs(out, exist_ok=True)
COMP = ["wis", "sharpness", "underprediction", "overprediction"]
KEY = ["model", "target_variable", "forecast_date", "horizon", "location"]

pub = pd.read_csv(os.path.join(data, "scores.csv"), dtype={"location": str})

# ---- truth
tv_file = {"inc case": "Cases", "inc death": "Deaths", "inc hosp": "Hospitalizations"}
tr = []
for tv, f in tv_file.items():
    t = pd.read_csv(os.path.join(data, "truth", "ECDC", f"truth_ECDC-Incident {f}.csv"), dtype={"location": str})
    t["target_variable"] = tv
    tr.append(t[["target_variable", "location", "date", "value", "status"]])
truth = pd.concat(tr, ignore_index=True).rename(columns={"date": "target_end_date", "value": "true_value"})
if truth_mode in ("final0927", "final0927_owidhosp"):
    f = pd.read_csv(os.path.join(data, "truth", "ECDC", "final", "covid-cases-deaths-final_2024-09-27.csv"),
                    dtype={"location": str}).rename(columns={"date": "target_end_date", "value": "true_value"})
    f = f[["target_variable", "location", "target_end_date", "true_value"]]
    truth = pd.concat([truth[truth.target_variable == "inc hosp"].drop(columns="status"), f], ignore_index=True)
if truth_mode in ("owidhosp", "final0927_owidhosp"):
    # diagnosis only: hospitalisation truth ONLY from the archive's OWID file (it covers Czechia only); the
    # ECDC hospitalisation file is not used in this mode
    o = pd.read_csv(os.path.join(data, "truth", "OWID", "truth_OWID-Incident Hospitalizations.csv"),
                    dtype={"location": str}).rename(columns={"date": "target_end_date", "value": "true_value"})
    o["target_variable"] = "inc hosp"
    locs = set(o["location"])
    keep = truth.target_variable != "inc hosp"
    truth = pd.concat([o[["target_variable", "location", "target_end_date", "true_value"]], truth[keep]],
                      ignore_index=True)
truth = truth.drop_duplicates(["target_variable", "location", "target_end_date"])

# ---- forecasts: one file per published (model, forecast_date)
fmap = {}
mp = os.path.join(data, "file_map.tsv")  # published (model, forecast_date) -> non-Monday file name
if os.path.exists(mp):
    for l in open(mp, encoding="utf-8"):
        m, d, rel = l.rstrip("\n").split("\t"); fmap[(m, d)] = rel
keys = pub[["model", "forecast_date"]].drop_duplicates()
rows, missing = [], []
qcols = [f"{q:.3f}" for q in Q23]
for m, d in keys.values:
    rel = fmap.get((m, d), f"data-processed/{m}/{d}-{m}.csv")
    p = os.path.join(data, "hub", rel)
    if not os.path.exists(p):
        missing.append((m, d, rel)); continue
    fc = pd.read_csv(p, dtype={"location": str})
    hz = fc["target"].astype(str).str.extract(r"^(\d+) wk ahead ")[0]
    fc = fc[hz.notna()].copy(); fc["horizon"] = hz[hz.notna()].astype(int)
    fc["target_variable"] = fc["target"].str.replace(r"^\d+ wk ahead ", "", regex=True)
    g = ["target_variable", "horizon", "location", "target_end_date"]
    qq = fc[fc["type"] == "quantile"].copy()
    qq["q"] = qq["quantile"].astype(float).round(3).map(lambda v: f"{v:.3f}")
    qq = qq[qq["q"].isin(qcols)]
    W = qq.pivot_table(index=g, columns="q", values="value", aggfunc="first")
    pt = fc[fc["type"] == "point"].groupby(g)["value"].first().rename("point")
    W = W.join(pt, how="outer") if len(W) else pt.to_frame()
    for c in qcols:
        if c not in W.columns: W[c] = np.nan
    W = W.reset_index()
    # point-as-median where no 0.5 quantile (EuroForecastHub::score_forecasts)
    W["0.500"] = W["0.500"].where(W["0.500"].notna(), W["point"])
    W = W.merge(truth, on=["target_variable", "location", "target_end_date"], how="left")
    W["nq"] = W[qcols].notna().sum(axis=1)
    full = W[W["nq"] == 23]
    one = W[(W["nq"] == 1) & W["0.500"].notna()]
    other = W[(W["nq"] != 23) & ~((W["nq"] == 1) & W["0.500"].notna())]
    for part, kind in ((full, "q23"), (one, "point")):
        if not len(part): continue
        if kind == "q23":
            s = wis_decomp(part[qcols].to_numpy(), part["true_value"].to_numpy())
        else:
            s = wis_point(part["0.500"].to_numpy(), part["true_value"].to_numpy())
        r = part[g + ["true_value", "nq"]].copy()
        for k, v in s.items(): r[k] = v
        r["model"] = m; r["forecast_date"] = d; r["file"] = rel
        rows.append(r)
    if len(other):
        r = other[g + ["true_value", "nq"]].copy(); r["model"] = m; r["forecast_date"] = d; r["file"] = rel
        r["wis"] = np.nan; rows.append(r)

rec = pd.concat(rows, ignore_index=True)
rec.to_csv(os.path.join(out, f"recomputed_rows_{truth_mode}.csv.gz"), index=False)
pd.DataFrame(missing, columns=["model", "forecast_date", "file"]).to_csv(
    os.path.join(out, f"missing_files_{truth_mode}.csv"), index=False)

# ---- join on the published row keys
J = pub.merge(rec[KEY + ["target_end_date", "true_value", "nq"] + COMP + ["ae_median", "cov_50", "cov_95", "wis_alt_k1"]],
              on=KEY, how="left", suffixes=("_pub", "_rec"))
for c in COMP + ["ae_median"]:
    J[c + "_rec_r"] = np.round(J[c + "_rec"])  # numpy round = half to even, like R's round()
J["row_match_wis"] = (J["wis_rec_r"] == J["wis_pub"])
J["row_match_all4"] = np.all([J[c + "_rec_r"] == J[c + "_pub"] for c in COMP], axis=0)
J["covered"] = J["wis_rec"].notna()
J["row_match_wis_alt_k1"] = (np.round(J["wis_alt_k1"]) == J["wis_pub"])
J["row_match_ae"] = (np.round(J["ae_median_rec"]) == J["ae_median_pub"])
J["row_match_cov"] = ((J["cov_50_rec"] == J["cov_50_pub"]) & (J["cov_95_rec"] == J["cov_95_pub"])) | J["cov_50_pub"].isna()
J.to_csv(os.path.join(out, f"joined_rows_{truth_mode}.csv.gz"), index=False)

def summarise(by):
    res = []
    for k, G in J.groupby(by):
        k = k if isinstance(k, tuple) else (k,)
        C = G[G["covered"]]
        d = dict(zip(by, k)); d["rows_pub"] = len(G); d["rows_covered"] = len(C)
        d["rows_exact_all4"] = int(C["row_match_all4"].sum())
        for c in COMP:
            pm = G[c + "_pub"].mean(); pmc = C[c + "_pub"].mean()
            rm = C[c + "_rec_r"].mean(); ru = C[c + "_rec"].mean()
            d[c + "_pub"] = pm; d[c + "_pub_on_covered"] = pmc; d[c + "_rec"] = rm; d[c + "_rec_unrounded"] = ru
            d[c + "_reldiff"] = (rm - pmc) / pmc if pmc != 0 else np.nan
            d[c + "_absdiff"] = rm - pmc
        d["max_abs_reldiff"] = np.nanmax(np.abs([d[c + "_reldiff"] for c in COMP]))
        d["over_1pct"] = bool(d["max_abs_reldiff"] > 0.01) or d["rows_covered"] < 0.95 * d["rows_pub"]
        res.append(d)
    return pd.DataFrame(res)

S = summarise(["model"]); S.to_csv(os.path.join(out, f"per_model_{truth_mode}.csv"), index=False)
S2 = summarise(["model", "target_variable"]); S2.to_csv(os.path.join(out, f"per_model_target_{truth_mode}.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("truth:", truth_mode, "| published rows:", len(pub), "| covered:", int(J["covered"].sum()),
      "| rows exact on all 4 (rounded):", int(J["row_match_all4"].sum()), "| missing files:", len(missing))
cols = ["model", "rows_pub", "rows_covered", "rows_exact_all4"] + [c + "_pub_on_covered" for c in COMP[:1]] + \
       [c + "_rec" for c in COMP[:1]] + [c + "_reldiff" for c in COMP] + ["over_1pct"]
print(S[cols].to_string(index=False, float_format=lambda v: f"{v:.6g}"))
Cv = J[J["covered"]]
print("contrast: rows whose rounded 1/(K+1)-form WIS equals the published wis:", int(Cv["row_match_wis_alt_k1"].sum()), "of", len(Cv))
print("rows whose rounded ae_median matches:", int(Cv["row_match_ae"].sum()), "| rows whose cov_50 and cov_95 match:", int(Cv["row_match_cov"].sum()))
print("models over 1% (or <95% rows covered):", list(S.loc[S.over_1pct, "model"]))
