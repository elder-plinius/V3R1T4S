"""Provenance check: is the evaluation repository's assembly (data/submissions.csv.gz) identical, row for row and value
for value, to the hub's own data-processed / data-processed_retrospective files we fetched?
Checked sets (whatever is on disk under data/hub/): ensemble/ (all 159 MeanEnsemble files, data-processed),
sample/ (pre-declared dates 2021-11-22, 2022-01-15, 2022-03-31 for every model, from the folder the released loader
reads), full/ (every other model and date, from the folder the released loader reads).
Usage: python -I p3_provenance.py <run_folder> <out_dir> [tag]"""
import sys, os, glob
import numpy as np, pandas as pd

RUN, OUT = sys.argv[1], sys.argv[2]
TAG = sys.argv[3] if len(sys.argv) > 3 else ""
D = os.path.join(RUN, "data")
K = ["location", "age_group", "forecast_date", "target_end_date", "target", "type", "quantile"]
files = sorted(glob.glob(os.path.join(D, "hub", "ensemble", "*", "*.csv"))) + \
    sorted(glob.glob(os.path.join(D, "hub", "sample", "*", "*", "*.csv"))) + \
    sorted(glob.glob(os.path.join(D, "hub", "full", "*", "*", "*.csv")))
by_model = {}
for f in files:
    by_model.setdefault(os.path.basename(os.path.dirname(f)), []).append(f)
lines = []
tot_rows = tot_mis = tot_val = 0
bad_files = []
for model, fl in sorted(by_model.items()):
    dates = sorted({os.path.basename(f)[:10] for f in fl})
    parts = []
    for ch in pd.read_csv(os.path.join(D, "eval_data", "submissions.csv.gz"), chunksize=1_000_000):
        parts.append(ch[(ch.model == model) & ch.forecast_date.isin(dates)])
    sub = pd.concat(parts, ignore_index=True)
    del parts
    sub["quantile"] = sub["quantile"].fillna(-1.0)
    for f in fl:
        date = os.path.basename(f)[:10]
        H = pd.read_csv(f)
        H["quantile"] = H["quantile"].fillna(-1.0)
        A = sub[sub.forecast_date == date]
        m = H.merge(A, on=K, how="outer", suffixes=("_hub", "_asm"), indicator=True)
        only_hub = int((m._merge == "left_only").sum())
        only_asm = int((m._merge == "right_only").sum())
        both = m[m._merge == "both"]
        a, b = both.value_hub.values.astype(float), both.value_asm.values.astype(float)
        neq = int((~(np.isclose(a, b, rtol=0, atol=1e-9) | (np.isnan(a) & np.isnan(b)))).sum())
        tot_rows += len(H); tot_mis += only_hub + only_asm; tot_val += neq
        rel = os.path.relpath(f, os.path.join(D, "hub")).replace(os.sep, "/")
        lines.append(f"{rel}\thub_rows={len(H)}\tasm_rows={len(A)}\tonly_hub={only_hub}\tonly_asm={only_asm}"
                     f"\tvalue_mismatch={neq}")
        if only_hub or only_asm or neq:
            bad_files.append(lines[-1])
    print(model, len(fl), "files checked", flush=True)
os.makedirs(OUT, exist_ok=True)
summary = (f"files_checked={len(files)} hub_rows={tot_rows} key_mismatches={tot_mis} value_mismatches={tot_val} "
           f"files_with_any_difference={len(bad_files)}")
with open(os.path.join(OUT, f"p3_provenance{TAG}.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n\n" + summary + "\n")
    for b in bad_files:
        fh.write("DIFF " + b + "\n")
print(summary)
for b in bad_files[:20]:
    print("DIFF", b)
