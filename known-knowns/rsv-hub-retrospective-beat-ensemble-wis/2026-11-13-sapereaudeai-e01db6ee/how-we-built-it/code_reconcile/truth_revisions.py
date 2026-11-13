"""C5 (PREREG.md): in-season truth rows that differ between the 2026-11-04 and 2026-11-12 vintages of time-series.parquet,
and whether oracle-output equals the 2026-11-12 vintage. usage: python -I truth_revisions.py HUB OUT"""
import sys, os, numpy as np, pandas as pd
hub, out = sys.argv[1:3]
ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
for c in ("target_end_date", "as_of"): ts[c] = pd.to_datetime(ts[c]).dt.strftime("%Y-%m-%d")
ts["location"] = ts["location"].astype(str)
lo, hi = "2025-09-13", "2026-06-20"
a = ts[(ts["as_of"] == "2026-11-04") & ts["target_end_date"].between(lo, hi)]
b = ts[(ts["as_of"] == "2026-11-12") & ts["target_end_date"].between(lo, hi)]
k = ["target", "location", "target_end_date"]
m = a.merge(b, on=k, how="outer", suffixes=("_1104", "_1112"), indicator=True)
L = []; P = L.append
P("in-season window target_end_date %s..%s; rows in 2026-11-12 vintage: %d (%s)" % (lo, hi, len(b), ", ".join("%s %d" % kv for kv in b.groupby("target").size().items())))
P("rows only in one vintage: %s" % m["_merge"].value_counts().to_dict())
both = m[m["_merge"] == "both"].copy()
both["changed"] = np.abs(both["observation_1112"] - both["observation_1104"]) > 1e-12
ch = both[both["changed"]].copy()
P("rows whose value changed 2026-11-04 -> 2026-11-12: %d of %d (%s)" % (len(ch), len(both), ", ".join("%s %d" % kv for kv in ch.groupby("target").size().items())))
if len(ch):
    ch["rel_old"] = np.abs(ch["observation_1112"] - ch["observation_1104"]) / np.abs(ch["observation_1104"])
    ch["rel_new"] = np.abs(ch["observation_1112"] - ch["observation_1104"]) / np.abs(ch["observation_1112"])
    r = ch.sort_values("rel_old", ascending=False).iloc[0]
    P("largest relative change: %.4f relative to the 2026-11-04 value (%.4f relative to the 2026-11-12 value): %s %s %s %g -> %g" % (r["rel_old"], r["rel_new"], r["target"], r["location"], r["target_end_date"], r["observation_1104"], r["observation_1112"]))
    P("max relative change over changed rows: %.4f (vs 11-04 value), %.4f (vs 11-12 value)" % (ch["rel_old"].max(), ch["rel_new"].max()))
    P("changed target_end_date range: %s..%s" % (ch["target_end_date"].min(), ch["target_end_date"].max()))
o = pd.read_parquet(os.path.join(hub, "target-data", "oracle-output.parquet"))
o = o[o["output_type"] == "quantile"].copy(); o["target_end_date"] = pd.to_datetime(o["target_end_date"]).dt.strftime("%Y-%m-%d"); o["location"] = o["location"].astype(str)
lv = ts[ts["as_of"] == "2026-11-12"]
j = o.merge(lv, on=k, how="left")
P("oracle-output quantile rows: %d; matched in the 2026-11-12 vintage: %d; equal values: %d" % (len(o), int(j["observation"].notna().sum()), int((np.abs(j["oracle_value"] - j["observation"]) < 1e-12).sum())))
open(out, "w", newline="\n").write("\n".join(L) + "\n"); print("\n".join(L))
