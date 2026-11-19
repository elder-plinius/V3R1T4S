"""PREREG.v2 baseline read B: MoleculeACE repo config SVM/ECFP on CHEMBL244_Ki.

Config from data/repo_config244/SVM_ECFP.yml: C=10, epsilon=0.1, gamma=0.01, kernel=rbf.
ECFP: Morgan radius 2, 1024 bits. Deterministic (single SVR).
Expected (corrected results CSV): overall RMSE 0.715 (tol 0.6435-0.7865), cliff RMSE 0.797.
This is a declared baseline test read (PREREG.v2 §3).
"""
import json
import os
import sys

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mace_common import ecfp, load_dataset  # noqa: E402

ds = load_dataset("CHEMBL244_Ki")
X = ecfp(ds["mols"], 2, 1024)
X_tr, X_te = X[ds["train"]], X[ds["test"]]
y_tr, y_te = ds["y"][ds["train"]], ds["y"][ds["test"]]
cliff_te = ds["cliff"][ds["test"]] == 1

m = SVR(C=10, epsilon=0.1, gamma=0.01, kernel="rbf")
m.fit(X_tr, y_tr)
yh = m.predict(X_te)

mse = mean_squared_error(y_te, yh)
rmse = float(np.sqrt(mse))
mse_cliff = mean_squared_error(y_te[cliff_te], yh[cliff_te])
mse_non = mean_squared_error(y_te[~cliff_te], yh[~cliff_te])
rmse_cliff = float(np.sqrt(mse_cliff))

out = {"model": "SVM/ECFP repo config CHEMBL244_Ki (C=10, eps=0.1, gamma=0.01, rbf)",
       "mse": float(mse), "rmse": rmse,
       "mse_cliff": float(mse_cliff), "rmse_cliff": rmse_cliff,
       "mse_noncliff": float(mse_non), "rmse_noncliff": float(np.sqrt(mse_non)),
       "expected_rmse_paper": 0.715, "expected_rmse_cliff_paper": 0.797,
       "tolerance": [0.6435, 0.7865],
       "reproduced": bool(0.6435 <= rmse <= 0.7865),
       "n_cliff_test": int(cliff_te.sum()), "n_noncliff_test": int((~cliff_te).sum())}
print(json.dumps(out, indent=1))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fx-baseline")
os.makedirs(OUT, exist_ok=True)
json.dump(out, open(os.path.join(OUT, "baseline_B_chembl244.json"), "w"), indent=1)
np.save(os.path.join(OUT, "baseline_B_test_predictions.npy"), yh)
print("WROTE fx-baseline/baseline_B_chembl244.json + predictions")
