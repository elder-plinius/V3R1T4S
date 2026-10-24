"""Score confirmatory predictions with drevalpy 1.3.5's OWN evaluation code, exactly the sequence
drevalpy-report runs: visualization.utils.parse_results -> prep_results (which applies
_normalize_metrics_by_mean_effects). Works on a copy containing only the listed models + the
normalization baseline + splits, so baselines still being written elsewhere cannot interfere.
usage: evaluate_with_drevalpy.py <run_id> <tag> <model> [<model> ...]"""
import os
import sys, os, shutil, pathlib, json, numpy as np, pandas as pd
from drevalpy.visualization.utils import parse_results, prep_results
run_id, tag, models = sys.argv[1], sys.argv[2], sys.argv[3:]
RESULTS = os.environ.get("RESULTS", "./results"); EVAL = os.environ.get("EVAL", "./eval")
src = pathlib.Path(RESULTS) / run_id / "CTRPv2" / "LDO"; dst_root = pathlib.Path(EVAL) / f"{run_id}_{tag}"
dst = dst_root / "CTRPv2" / "LDO"
if dst_root.exists(): shutil.rmtree(dst_root)
dst.mkdir(parents=True)
for m in set(models) | {"NaiveMeanEffectsPredictor"}:
    shutil.copytree(src / m, dst / m)
shutil.copytree(src / "splits", dst / "splits")
ev, ev_d, ev_c, tvp = parse_results(path_to_results=str(dst_root), dataset="CTRPv2")
ev, ev_d, ev_c, tvp = prep_results(ev, ev_d, ev_c, tvp, pathlib.Path(os.environ.get("DATA", "./data")))
ev.to_csv(dst_root / "evaluation_results.csv"); tvp.to_csv(dst_root / "true_vs_pred.csv")
ev = ev[(ev.test_mode == "LDO") & (ev.rand_setting == "predictions")]
out = {}
for alg in sorted(ev.algorithm.unique()):
    e = ev[ev.algorithm == alg]
    r = e["R^2: normalized"].astype(float); n = len(r)
    out[alg] = dict(n_splits=int(n), normR2_mean=float(r.mean()), normR2_sd=float(r.std(ddof=1)),
                    normR2_se=float(r.std(ddof=1) / np.sqrt(n)), normR2_per_split=[float(x) for x in r],
                    normPearson=float(e["Pearson: normalized"].astype(float).mean()),
                    normSpearman=float(e["Spearman: normalized"].astype(float).mean()),
                    R2_raw=float(e["R^2"].astype(float).mean()), n_pairs=int(len(tvp[tvp.algorithm == alg])))
json.dump(out, open(dst_root / "summary.json", "w"), indent=1)
for alg, o in out.items():
    print(f"{alg:28s} splits {o['n_splits']}  normR2 {o['normR2_mean']:+.4f}  SD {o['normR2_sd']:.4f}  SE {o['normR2_se']:.4f}"
          f"  normPearson {o['normPearson']:+.4f}  normSpearman {o['normSpearman']:+.4f}  pairs {o['n_pairs']}")
print("per-split normR2:", {a: [round(x, 4) for x in o["normR2_per_split"]] for a, o in out.items()})
