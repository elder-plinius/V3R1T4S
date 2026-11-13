"""Reconcile ACCIDDA/tapestry docs/experiments/google-comparison-20261005 (06508218) with the hub files:
Google_SAI-RSVEns pooled natural-scale WIS (per-seed.csv) and per-location summed WIS of Google_SAI-RSVEns and
RSVHub-ensemble (native-location-scores.csv), truth = time-series.parquet as_of 2026-09-02 (its provenance.json),
states+DC (no US, no 72), horizons 0-3, tasks where both models have forecasts.
usage: python -I tapestry_google_reconcile.py HUB GOOGLE_DIR OUT"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models, wis, LEVELS, _loc
hub, gd, out = sys.argv[1:4]
w = load_models(hub, models=["Google_SAI-RSVEns", "RSVHub-ensemble"])
w = w[(w["target"] == "wk inc rsv hosp") & w["horizon"].between(0, 3) & ~w["location"].isin(["US", "72"])].copy()
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
ts["target_end_date"] = pd.to_datetime(ts["target_end_date"]).dt.strftime("%Y-%m-%d"); ts["as_of"] = pd.to_datetime(ts["as_of"]).dt.strftime("%Y-%m-%d"); ts["location"] = _loc(ts["location"])
tv = ts[(ts["target"] == "wk inc rsv hosp") & (ts["as_of"] == "2026-09-02")][["location", "target_end_date", "observation"]]
w = w.merge(tv, on=["location", "target_end_date"], how="inner")
w["wis"] = wis(w[[round(l, 4) for l in LEVELS]].to_numpy(float), LEVELS, w["observation"].to_numpy(float))
k = ["reference_date", "location", "horizon", "target_end_date"]
g = w[w["model"] == "Google_SAI-RSVEns"]; e = w[w["model"] == "RSVHub-ensemble"]
c = g[k].merge(e[k], on=k)
g2 = g.merge(c, on=k); e2 = e.merge(c, on=k)
ps = pd.read_csv(os.path.join(gd, "per-seed.csv"))
pub = ps[(ps["target"] == "wk inc rsv hosp") & (ps["scale"] == "native")]["pooled_google_wis"].unique()
L = []; P = L.append
P("Google_SAI-RSVEns and RSVHub-ensemble common hosp tasks (states+DC, h0-3, truth as_of 2026-09-02): %d; dates %d (%s..%s); locations %d" % (len(c), c["reference_date"].nunique(), c["reference_date"].min(), c["reference_date"].max(), c["location"].nunique()))
P("pooled Google_SAI-RSVEns mean WIS: ours %.12g; published (per-seed.csv, native, all seeds) %s" % (g2["wis"].mean(), ", ".join("%.12g" % v for v in pub)))
nl = pd.read_csv(os.path.join(gd, "native-location-scores.csv"), dtype={"location": str})
nl = nl[(nl["target"] == "wk inc rsv hosp") & (nl["scope"] == "frozen_all") & (nl["seed"] == 42)]
nl["location"] = _loc(nl["location"])
sg = g2.groupby("location")["wis"].sum(); se = e2.groupby("location")["wis"].sum()
m = nl.set_index("location")
dg = (m["google"] - sg.reindex(m.index)).abs().max(); de = (m["ensemble"] - se.reindex(m.index)).abs().max()
P("per-location summed WIS vs native-location-scores.csv (frozen_all, seed 42; %d locations): max |diff| google %.3g, ensemble %.3g" % (len(m), dg, de))
open(out, "w", newline="\n").write("\n".join(L) + "\n"); print("\n".join(L))
