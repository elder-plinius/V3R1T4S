"""C3 (PREREG.md): reconcile ACCIDDA/EpiBenchmark rsv25-26_complete-model-scores.parquet (blob 4300c200) with the hub files.
usage: python -I epibench_reconcile.py HUB EPIBENCH_SCORES OUT"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models, oracle, wis, LEVELS, _loc

hub, scf, out = sys.argv[1:4]
L5 = [0.025, 0.25, 0.5, 0.75, 0.975]
s = pd.read_parquet(scf)
s["location"] = _loc(s["location"])
w = load_models(hub, models=["RSVHub-ensemble", "RSVHub-baseline"])
w = w[w["target"] == "wk inc rsv hosp"]
key = ["model", "reference_date", "location", "horizon", "target_end_date"]
m = s.merge(w, on=key, how="left", indicator=True)
lines = []
P = lines.append
P("EpiBenchmark rows: %d (%s); rows without a matching hub forecast: %d" % (len(s), ", ".join("%s %d" % kv for kv in s.groupby("model").size().items()), int((m["_merge"] != "both").sum())))
m = m[m["_merge"] == "both"].copy()
o = oracle(hub)
o = o[o["target"] == "wk inc rsv hosp"]
m = m.merge(o[["location", "target_end_date", "oracle_value"]], on=["location", "target_end_date"], how="left")
P("rows without a pinned oracle value: %d" % int(m["oracle_value"].isna().sum()))
Q5 = m[L5].to_numpy(float); Q23 = m[[round(l, 4) for l in LEVELS]].to_numpy(float)
y0 = m["oracle_value"].to_numpy(float)
m["wis5_oracle"] = wis(Q5, L5, y0)
m["wis23_oracle"] = wis(Q23, LEVELS, y0)
d = np.abs(m["wis5_oracle"] - m["wis"])
P("(a) pinned oracle truth: rows with |5-level WIS - published wis| <= 1e-6: %d of %d" % (int((d <= 1e-6).sum()), len(m)))
# (b) implied truth: y = median +- ae_median, the candidate that reproduces the published wis
med = m[0.5].to_numpy(float); ae = m["ae_median"].to_numpy(float)
c1, c2 = med + ae, med - ae
w1, w2 = wis(Q5, L5, c1), wis(Q5, L5, c2)
e1, e2 = np.abs(w1 - m["wis"].to_numpy()), np.abs(w2 - m["wis"].to_numpy())
# a row's candidates: those reproducing its wis within 1e-6; the bias sign (scoringutils: negative when y > median)
# breaks ties; then one value per (location, target_end_date) must fit every row of that pair (both models, all horizons)
bias = m["bias"].to_numpy(float)
ok1, ok2 = e1 <= 1e-6, e2 <= 1e-6
pick = np.where(ok1 & ~ok2, 1, np.where(ok2 & ~ok1, 2, np.where(bias < 0, 1, np.where(bias > 0, 2, 1))))
yrow = np.where(pick == 1, c1, c2)
m["y_row"] = yrow
cons = m.groupby(["location", "target_end_date"])["y_row"].agg(lambda v: v.round(9).nunique())
P("    (location, target_end_date) pairs whose rows imply more than one truth value: %d of %d" % (int((cons > 1).sum()), len(cons)))
yimp = yrow; eimp = np.abs(wis(Q5, L5, yimp) - m["wis"].to_numpy())
m["y_implied"] = yimp
amb = ok1 & ok2 & (ae > 0)
P("(b) implied truth (median +- ae_median): rows where both candidates reproduce the wis (ae > 0; bias sign used): %d" % int(amb.sum()))
P("    rows reproduced within 1e-6 by the chosen implied truth: %d of %d; max |diff| %.3g" % (int((eimp <= 1e-6).sum()), len(m), eimp.max()))
pairs = m.drop_duplicates(["location", "target_end_date"])[["location", "target_end_date", "y_implied", "oracle_value"]]
diffp = pairs[np.abs(pairs["y_implied"] - pairs["oracle_value"]) > 1e-9]
P("    implied truth vs pinned oracle: %d of %d (location, target_end_date) pairs differ" % (len(diffp), len(pairs)))
# which time-series vintage matches the implied truth best
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
ts = ts[ts["target"] == "wk inc rsv hosp"].copy()
ts["target_end_date"] = pd.to_datetime(ts["target_end_date"]).dt.strftime("%Y-%m-%d"); ts["as_of"] = pd.to_datetime(ts["as_of"]).dt.strftime("%Y-%m-%d")
ts["location"] = _loc(ts["location"])
j = pairs.merge(ts, on=["location", "target_end_date"], how="inner")
j["eq"] = np.abs(j["observation"] - j["y_implied"]) <= 1e-9
g = j.groupby("as_of").agg(n=("eq", "size"), match=("eq", "sum"))
g = g[g["n"] == len(pairs)] if (g["n"] == len(pairs)).any() else g
best = g.sort_values("match", ascending=False).head(5)
P("    time-series vintages covering all %d pairs, best matches with the implied truth (as_of: matching pairs):" % len(pairs))
for a, r in best.iterrows():
    P("      %s: %d of %d" % (a, r["match"], r["n"]))
# direct, non-circular check: truth = the best-matching vintage, scored without using ae_median
va = best.index[0]
tv = ts[ts["as_of"] == va][["location", "target_end_date", "observation"]]
mv = m.merge(tv, on=["location", "target_end_date"], how="left")
wv = wis(mv[L5].to_numpy(float), L5, mv["observation"].to_numpy(float))
dv = np.abs(wv - mv["wis"].to_numpy())
P("(c) truth = time-series.parquet as_of %s (no use of ae_median): rows with |5-level WIS - published wis| <= 1e-6: %d of %d; max |diff| %.3g" % (va, int((dv <= 1e-6).sum()), len(mv), np.nanmax(dv)))
P("per model on EpiBenchmark's task set (52 locations incl. US, horizons 0-3, 28 dates):")
P("  model             n     published mean wis | ours 5-level, pinned oracle | ours 5-level, implied truth | ours 23-level, pinned oracle (object's metric)")
m["wis5_implied"] = wis(Q5, L5, yimp)
for mo, g2 in m.groupby("model"):
    P("  %-16s %5d   %.6f | %.6f | %.6f | %.6f" % (mo, len(g2), g2["wis"].mean(), g2["wis5_oracle"].mean(), g2["wis5_implied"].mean(), g2["wis23_oracle"].mean()))
cov = m.groupby("model").apply(lambda g2: pd.Series({"cov50_pub": g2["interval_coverage_50"].mean(), "cov95_pub": g2["interval_coverage_95"].mean()}), include_groups=False)
P("published coverage: " + "; ".join("%s cov50 %.6f cov95 %.6f" % (k, r["cov50_pub"], r["cov95_pub"]) for k, r in cov.iterrows()))
open(out, "w", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
