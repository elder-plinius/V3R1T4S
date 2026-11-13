"""Hub-format check of our files against hub-config/tasks.json (2024-25 round) and coverage of every hub-ensemble task.
usage: python validate_format.py"""
import os, sys, glob, json
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(RUN, "attempts", "evaluator", "code"))
from parse_mo import load_all  # noqa: E402
cfg = json.load(open(os.path.join(RUN, "data", "hopkins", "hub-config_tasks.json")))
mt = cfg["rounds"][0]["model_tasks"][0]
ti = mt["task_ids"]
ok_orig = set((ti["origin_date"]["required"] or []) + (ti["origin_date"]["optional"] or []))
ok_loc = set((ti["location"]["required"] or []) + (ti["location"]["optional"] or []))
ok_age = set((ti["age_group"]["required"] or []) + (ti["age_group"]["optional"] or []))
ok_hz = set((ti["horizon"]["required"] or []) + (ti["horizon"]["optional"] or []))
levels = set(round(x, 4) for x in mt["output_type"]["quantile"]["output_type_id"]["required"])
cols = ["origin_date", "target", "horizon", "location", "age_group", "output_type", "output_type_id", "value"]
bad = []
files = sorted(glob.glob(os.path.join(RUN, "attempts", "forecaster", "result", "forecasts", "*-V3R1T4S-asofKA.csv")))
allr = []
for f in files:
    d = pd.read_csv(f, dtype={"location": str, "age_group": str, "output_type_id": str})
    o = os.path.basename(f)[:10]
    if list(d.columns) != cols: bad.append((o, "columns"))
    if set(d.origin_date) != {o}: bad.append((o, "origin_date"))
    if o not in ok_orig: bad.append((o, "origin not in tasks.json"))
    if pd.Timestamp(o).dayofweek != 6: bad.append((o, "not Sunday"))
    if set(d.target) != {"inc hosp"}: bad.append((o, "target"))
    if not set(d.location) <= ok_loc: bad.append((o, "location"))
    if not set(d.age_group) <= ok_age: bad.append((o, "age_group"))
    hz = set(d.horizon) - ok_hz
    if set(d.output_type) != {"quantile"}: bad.append((o, "output_type"))
    if set(round(float(x), 4) for x in d.output_type_id) != levels: bad.append((o, "levels"))
    if (d.value < 0).any() or d.value.isna().any(): bad.append((o, "values"))
    w = d.assign(l=d.output_type_id.astype(float)).sort_values(["horizon", "location", "age_group", "l"])
    if (w.groupby(["horizon", "location", "age_group"]).value.diff().dropna() < -1e-9).any(): bad.append((o, "non-monotone"))
    if d.duplicated(["horizon", "location", "age_group", "output_type_id"]).any(): bad.append((o, "duplicates"))
    allr.append(d.assign(horizon_extra=len(hz)))
D = pd.concat(allr)
print("files", len(files), "rows", len(D), "problems", bad if bad else "none")
print("horizons produced", sorted(D.horizon.unique()), "(-1 is outside tasks.json; used only to cover hub-baseline tasks; hub-ensemble uses 0..4)")
hub = load_all()
E = hub[(hub.model_id == "hub-ensemble") & (hub.origin_date >= "2024-10-01")].drop_duplicates(["origin_date", "horizon", "location", "age_group"])
k = ["origin_date", "horizon", "location", "age_group"]
m = E[k].merge(D[k].drop_duplicates(), on=k, how="left", indicator=True)
print("hub-ensemble 2024-25 tasks", len(E), "covered by ours", int((m._merge == "both").sum()), "missing", int((m._merge != "both").sum()))
