"""C4 (PREREG.md): RSVHub-ensemble 2025-26 means vs ACCIDDA/tapestry B2-screen leaderboard.csv (both targets).
usage: python -I tapestry_reconcile.py HUB LEADERBOARD_CSV OUT"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models, oracle, wis, LEVELS, _loc

hub, lbf, out = sys.argv[1:4]
lb = pd.read_csv(lbf, dtype={"horizon": str})
lb = lb[(lb["model"] == "RSVHub-ensemble") & (lb["season"] == "2025-2026") & lb["target"].str.contains("rsv")]
w = load_models(hub, models=["RSVHub-ensemble"])
w = w[w["horizon"].between(0, 3)].copy()
w["geo"] = np.where(w["location"] == "US", "US", np.where(w["location"] == "72", "PR", "states_dc"))
o = oracle(hub)
w = w.merge(o, on=["target", "location", "target_end_date"], how="left")
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
ts["target_end_date"] = pd.to_datetime(ts["target_end_date"]).dt.strftime("%Y-%m-%d"); ts["as_of"] = pd.to_datetime(ts["as_of"]).dt.strftime("%Y-%m-%d")
ts["location"] = _loc(ts["location"])
Q = w[[round(l, 4) for l in LEVELS]].to_numpy(float)
w["wis_oracle"] = wis(Q, LEVELS, w["oracle_value"].to_numpy(float))
lines = []; P = lines.append
P("tapestry rows (RSVHub-ensemble, 2025-2026): %d" % len(lb))
def cells(df, col):
    r = {}
    for (t, g), d in df.groupby(["target", "geo"]):
        r[(t, g, "all")] = (len(d), d[col].mean())
        for h, dh in d.groupby("horizon"):
            r[(t, g, str(h))] = (len(dh), dh[col].mean())
    return r
co = cells(w.dropna(subset=["wis_oracle"]), "wis_oracle")
# best single vintage per target: truth from that as_of, tasks restricted to those with a value in it
best = {}
for t in sorted(lb["target"].unique()):
    sub = lb[lb["target"] == t]
    res = []
    for a in sorted(ts[ts["target"] == t]["as_of"].unique()):
        if a < "2026-06-01":
            continue
        tv = ts[(ts["target"] == t) & (ts["as_of"] == a)][["location", "target_end_date", "observation"]]
        wt = w[w["target"] == t].merge(tv, on=["location", "target_end_date"], how="inner")
        wt["wis_v"] = wis(wt[[round(l, 4) for l in LEVELS]].to_numpy(float), LEVELS, wt["observation"].to_numpy(float))
        cv = cells(wt, "wis_v")
        errs = []; nmatch = 0
        for _, r in sub.iterrows():
            k = (t, r["geography"], str(r["horizon"]))
            if k in cv:
                errs.append(abs(cv[k][1] - r["wis"]) / r["wis"]); nmatch += int(cv[k][0] == r["n"])
        res.append((max(errs) if errs else np.inf, a, nmatch, cv))
    res.sort(key=lambda x: x[0])
    best[t] = res[0]
P("target | geography | horizon | tapestry n, wis | ours pinned oracle n, wis (rel diff) | ours best vintage n, wis (rel diff)")
for _, r in lb.sort_values(["target", "geography", "horizon"]).iterrows():
    k = (r["target"], r["geography"], str(r["horizon"]))
    n0, v0 = co.get(k, (0, np.nan))
    e, a, nm, cv = best[r["target"]]
    n1, v1 = cv.get(k, (0, np.nan))
    P("%s | %s | %s | %d, %.8g | %d, %.8g (%+.4f%%) | %s: %d, %.8g (%+.4f%%)" % (r["target"], r["geography"], r["horizon"], r["n"], r["wis"], n0, v0, 100 * (v0 / r["wis"] - 1), a, n1, v1, 100 * (v1 / r["wis"] - 1)))
for t, (e, a, nm, cv) in best.items():
    P("best vintage for %s: as_of %s, max relative diff over the 10 cells %.3g, cells with equal n %d of 10" % (t, a, e, nm))
open(out, "w", newline="\n").write("\n".join(lines) + "\n"); print("\n".join(lines))
