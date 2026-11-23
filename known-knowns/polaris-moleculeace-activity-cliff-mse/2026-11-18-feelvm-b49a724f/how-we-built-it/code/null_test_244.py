"""PREREG.v2 §4 null test: 400 controls — frozen M1 recipe retrained with SHUFFLED train labels.

Frozen recipe = the 6 M1 members + the frozen combiner weights from M1_read (fit on real-label
OOF). Each control k: permute y_train with rng(20261118+k), refit every member on all 2476
train rows, predict the official test rows, apply the frozen weights. Record overall/cliff/
noncliff MSE. The real M1 (mse_all 0.43675104854437247) must beat every control on overall
test MSE. Features are cached once (no per-control featurization).
"""
import json
import os
import sys
import time

import numpy as np
from sklearn.svm import SVR

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mace_common import ecfp_count, featurize, load_dataset  # noqa: E402

t0 = time.time()
ds = load_dataset("CHEMBL244_Ki")
tr_idx = np.where(ds["train"])[0]
te_idx = np.where(ds["test"])[0]
mols_tr = [ds["mols"][i] for i in tr_idx]
mols_te = [ds["mols"][i] for i in te_idx]
y_tr0 = ds["y"][tr_idx]
y_te = ds["y"][te_idx]
c_te = ds["cliff"][te_idx] == 1

Xs = {}
Xs_te = {}
for f in ["ECFP4", "ECFP6", "FCFP4"]:
    Xs[f], Xs_te[f] = featurize(mols_tr, f), featurize(mols_te, f)
Xs["ECFP6CNT"] = ecfp_count(mols_tr, 3, 2048)
Xs_te["ECFP6CNT"] = ecfp_count(mols_te, 3, 2048)
print("feats cached %.0fs" % (time.time() - t0), flush=True)

# frozen weights from M1_read_result.json (the real-run combiner)
M1 = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "M1_read_result.json")))
W = M1["weights"]
MEMBERS = M1["members"]

CONFIGS = {
    "B_SVR_ECFP4": ("ECFP4", 10, 0.01),
    "SVR_ECFP6CNT_C30_g0.003": ("ECFP6CNT", 30, 0.003),
    "SVR_FCFP4_C100_g0.01": ("FCFP4", 100, 0.01),
    "SVR_ECFP6_C30_g0.01": ("ECFP6", 30, 0.01),
    "SVR_FCFP4_C30_g0.003": ("FCFP4", 30, 0.003),
    "SVR_FCFP4_C30_g0.01": ("FCFP4", 30, 0.01),
}


def recipe_predict(y_tr):
    total = np.zeros(len(te_idx))
    for n in MEMBERS:
        f, C, g = CONFIGS[n]
        m = SVR(C=C, epsilon=0.1, gamma=g).fit(Xs[f], y_tr)
        total += W[n] * m.predict(Xs_te[f])
    # weights sum ~1 (positive ridge); normalize defensively
    return total / sum(W[n] for n in MEMBERS)


mses = []
for k in range(400):
    rng = np.random.default_rng(20261118 + k)
    y_tr = rng.permutation(y_tr0)
    yh = recipe_predict(y_tr)
    mses.append(float(np.mean((y_te - yh) ** 2)))
    if (k + 1) % 40 == 0:
        print(f"control {k+1}/400 mse={mses[-1]:.4f} min_so_far={min(mses):.4f} (%.0fs)" % (time.time() - t0), flush=True)

best_control = min(mses)
real = M1["mse_all"]
out = {"controls": 400, "best_control_overall_mse": best_control, "real_overall_mse": real,
       "real_beats_all_controls": bool(real < best_control),
       "control_summary": {"min": best_control, "median": float(np.median(mses)), "max": max(mses)},
       "command": "python null_test_244.py (attempts/cliff-fx/code)"}
print(json.dumps(out, indent=1))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
json.dump(out, open(os.path.join(OUT, "null_test_244.json"), "w"), indent=1)
np.save(os.path.join(OUT, "null_control_mses.npy"), np.array(mses))
print("WROTE output/null_test_244.json")
