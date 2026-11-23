"""CHEMBL244_Ki integrity + API identity check (before the p2 attack).

Verifies: sha256, split counts vs Polaris API (incl. exact test-index identity),
cliff counts, InChIKey disjointness, label map, checker controls.
"""
import json
import os
import sys

import numpy as np
from sklearn.metrics import mean_squared_error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mace_common import RUN, inchikeys, load_dataset  # noqa: E402

ds = load_dataset("CHEMBL244_Ki")
print("dataset", ds["name"], "sha256", ds["sha256"])
print("n=%d train=%d test=%d cliff_train=%d cliff_test=%d" % (
    len(ds["y"]), ds["train"].sum(), ds["test"].sum(),
    (ds["cliff"][ds["train"]] == 1).sum(), (ds["cliff"][ds["test"]] == 1).sum()))

A = np.vstack([ds["y"], np.ones_like(ds["y"])]).T
coef, *_ = np.linalg.lstsq(A, ds["y_p"], rcond=None)
resid = np.abs(A @ coef - ds["y_p"]).max()
print("label map y[pKi]=%.6f*y+%.6f max resid %.2e" % (coef[0], coef[1], resid))
print("unparseable:", sum(1 for m in ds["mols"] if m is None))

iks = inchikeys(ds)
tr = set(iks[i] for i in np.where(ds["train"])[0])
te = set(iks[i] for i in np.where(ds["test"])[0])
print("InChIKey train∩test:", len(tr & te))

# API identity
api = json.load(open(os.path.join(RUN, "data", "api-moleculeace-chembl244-ki.json"), encoding="utf-8"))
sp = api["split"]
test_idx_csv = sorted(np.where(ds["test"])[0].tolist())
train_idx_csv = sorted(np.where(ds["train"])[0].tolist())
print("API split[0]==CSV train indices:", sorted(sp[0]) == train_idx_csv)
print("API split[1]==CSV test indices:", sorted(sp[1]) == test_idx_csv)

# checker controls
y_te = ds["y"][ds["test"]]
y_tr_mean = ds["y"][ds["train"]].mean()
mse_pos = mean_squared_error(y_te, np.full_like(y_te, y_tr_mean))
exp = float(np.mean((y_te - y_tr_mean) ** 2))
print("POSITIVE CONTROL: %.9f vs %.9f match=%s" % (mse_pos, exp, np.isclose(mse_pos, exp)))
print("NEGATIVE CONTROL: %.9f" % mean_squared_error(y_te, y_te))

json.dump({"sha256": ds["sha256"], "n": int(len(ds["y"])), "ntrain": int(ds["train"].sum()),
           "ntest": int(ds["test"].sum()), "cliff_test": int((ds["cliff"][ds["test"]] == 1).sum()),
           "api_split_identity": bool(sorted(sp[1]) == test_idx_csv and sorted(sp[0]) == train_idx_csv),
           "inchikey_overlap": len(tr & te)},
          open(os.path.join(RUN, "data", "integrity_chembl244.json"), "w"), indent=1)
print("WROTE data/integrity_chembl244.json")
