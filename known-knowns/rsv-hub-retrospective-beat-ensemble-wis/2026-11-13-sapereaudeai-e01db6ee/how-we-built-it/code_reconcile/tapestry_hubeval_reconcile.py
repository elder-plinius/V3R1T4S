"""C7 (PREREG.v2.md): RSV 2025-2026 rows of ACCIDDA/tapestry hub-evaluation.md / B2-screen manifest.json (6546e06):
RSVHub-ensemble and UGA_flucast-INFLAenza on the ensemble-defined units both cover.
usage: python -I tapestry_hubeval_reconcile.py HUB MANIFEST_JSON OUT"""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models, wis, LEVELS, _loc
hub, mf, out = sys.argv[1:4]
man = json.load(open(mf, encoding="utf-8"))
cases = [c for c in man["cases"] if c.get("hub") == "rsv" and c.get("season") == "2025-2026"]
w = load_models(hub, models=["RSVHub-ensemble", "UGA_flucast-INFLAenza"])
w = w[w["horizon"].between(0, 3) & (w["location"] != "72")].copy()
w["consistent"] = (pd.to_datetime(w["reference_date"]) + pd.to_timedelta(7 * w["horizon"], unit="D")).dt.strftime("%Y-%m-%d") == w["target_end_date"]
w = w[w["consistent"]]
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
ts["target_end_date"] = pd.to_datetime(ts["target_end_date"]).dt.strftime("%Y-%m-%d"); ts["as_of"] = pd.to_datetime(ts["as_of"]).dt.strftime("%Y-%m-%d"); ts["location"] = _loc(ts["location"])
key = ["reference_date", "location", "horizon", "target_end_date"]
L = []; P = L.append
for c in cases:
    t = c["target"]
    pub = {s["model"]: s for s in c["summary"]}
    best = None
    for a in sorted(ts[ts["target"] == t]["as_of"].unique()):
        if a < "2026-06-01": continue
        tv = ts[(ts["target"] == t) & (ts["as_of"] == a)][["location", "target_end_date", "observation"]]
        d = w[w["target"] == t].merge(tv, on=["location", "target_end_date"], how="inner")
        d = d[np.isfinite(d["observation"])]
        d["wis"] = wis(d[[round(l, 4) for l in LEVELS]].to_numpy(float), LEVELS, d["observation"].to_numpy(float))
        d["ae"] = np.abs(d[0.5] - d["observation"])
        ens = d[d["model"] == "RSVHub-ensemble"]; uga = d[d["model"] == "UGA_flucast-INFLAenza"]
        common = ens.merge(uga[key], on=key)[key]
        e2 = ens.merge(common, on=key); u2 = uga.merge(common, on=key)
        res = {"RSVHub-ensemble": (len(e2), e2["wis"].mean(), e2["ae"].mean()), "UGA_flucast-INFLAenza": (len(u2), u2["wis"].mean(), u2["ae"].mean())}
        err = max(abs(res[m][1] / pub[m]["wis"] - 1) for m in res)
        if best is None or err < best[0]: best = (err, a, res, len(ens))
    err, a, res, nens = best
    P("%s: published n_units %d, n_comparison_units %d; best truth vintage as_of %s (max relative |diff| of the two WIS %.3g); ensemble units with truth %d" % (t, c["n_units"], c["n_comparison_units"], a, err, nens))
    for m, (n, mw, ma) in res.items():
        P("  %-22s n %d (published %d)  WIS %.10g (published %.10g)  MAE %.10g (published %.10g)" % (m, n, pub[m]["n"], mw, pub[m]["wis"], ma, pub[m]["ae_median"]))
open(out, "w", newline="\n").write("\n".join(L) + "\n"); print("\n".join(L))
