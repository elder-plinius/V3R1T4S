"""C4 follow-up: which task rule reproduces tapestry's ED n and wis for RSVHub-ensemble (2025-26)?
usage: python -I tapestry_ed_variants.py HUB LEADERBOARD_CSV OUT"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models, wis, LEVELS, _loc
hub, lbf, out = sys.argv[1:4]
T = "wk inc rsv prop ed visits"
lb = pd.read_csv(lbf, dtype={"horizon": str})
lb = lb[(lb["model"] == "RSVHub-ensemble") & (lb["season"] == "2025-2026") & (lb["target"] == T)]
w = load_models(hub, models=["RSVHub-ensemble"]); w = w[(w["target"] == T) & w["horizon"].between(0, 3)].copy()
w["geo"] = np.where(w["location"] == "US", "US", "states_dc")
w["consistent"] = (pd.to_datetime(w["reference_date"]) + pd.to_timedelta(7 * w["horizon"], unit="D")).dt.strftime("%Y-%m-%d") == w["target_end_date"]
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet")); ts = ts[ts["target"] == T].copy()
ts["target_end_date"] = pd.to_datetime(ts["target_end_date"]).dt.strftime("%Y-%m-%d"); ts["as_of"] = pd.to_datetime(ts["as_of"]).dt.strftime("%Y-%m-%d"); ts["location"] = _loc(ts["location"])
variants = {"all tasks": w, "drop rows with target_end_date != reference_date + 7*horizon": w[w["consistent"]],
            "drop the 2025-09-27 file": w[w["reference_date"] != "2025-09-27"]}
lines = []; P = lines.append
for name, d0 in variants.items():
    best = None
    for a in sorted(ts["as_of"].unique()):
        if a < "2026-06-01": continue
        tv = ts[ts["as_of"] == a][["location", "target_end_date", "observation"]]
        d = d0.merge(tv, on=["location", "target_end_date"], how="inner")
        d["w"] = wis(d[[round(l, 4) for l in LEVELS]].to_numpy(float), LEVELS, d["observation"].to_numpy(float))
        errs = []; neq = 0
        for _, r in lb.iterrows():
            sel = d[d["geo"] == r["geography"]] if r["horizon"] == "all" else d[(d["geo"] == r["geography"]) & (d["horizon"] == int(r["horizon"]))]
            errs.append(abs(sel["w"].mean() / r["wis"] - 1)); neq += int(len(sel) == r["n"])
        if best is None or max(errs) < best[0]: best = (max(errs), a, neq)
    P("%s: best as_of %s, max relative diff over 10 cells %.3g, cells with equal n %d of 10" % (name, best[1], best[0], best[2]))
open(out, "w", newline="\n").write("\n".join(lines) + "\n"); print("\n".join(lines))
