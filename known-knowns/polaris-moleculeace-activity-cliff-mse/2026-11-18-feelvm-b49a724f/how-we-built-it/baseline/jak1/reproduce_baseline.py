"""Step 3c: reproduce the MoleculeACE paper baseline on CHEMBL2835_Ki.

RF_ECFP (n_estimators=250) and SVM_ECFP (C=10000, epsilon=0.1, gamma=0.01, rbf) from
MoleculeACE/Data/configures/benchmark/CHEMBL2835_Ki/*.yml, ECFP radius 2 / 1024 bits
(from MoleculeACE/benchmark/featurization.py). Official split column. 5 seeds each.
Expected (paper corrected results CSV): RF RMSE 0.3876 (MSE 0.150236);
SVM RMSE from data/MoleculeACE_results.csv row CHEMBL2835_Ki/SVM/ECFP (read in-script).
Tolerance: ±10% relative on the 5-seed mean RMSE.
"""
import csv
import json
import os
import sys

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attempts"))
from mace_common import RUN, ecfp, load_dataset  # noqa: E402

ds = load_dataset()
X = ecfp(ds["mols"], radius=2, nbits=1024)
X_tr, X_te = X[ds["train"]], X[ds["test"]]
y_tr, y_te = ds["y"][ds["train"]], ds["y"][ds["test"]]

# expected values read from the repo's corrected results CSV (not from memory)
expected = {}
with open(os.path.join(RUN, "data", "MoleculeACE_results.csv"), newline="") as f:
    for r in csv.DictReader(f):
        if r["dataset"] == "CHEMBL2835_Ki" and r["algorithm"] in ("RF", "SVM") and r["descriptor"] == "ECFP":
            expected[r["algorithm"]] = float(r["rmse"])
print("expected RMSE from repo results CSV:", expected)

results = {}
for name, mk in [
    ("RF_ECFP", lambda s: RandomForestRegressor(n_estimators=250, random_state=s, n_jobs=-1)),
    ("SVM_ECFP", lambda s: SVR(C=10000, epsilon=0.1, gamma=0.01, kernel="rbf")),
]:
    mses = []
    for s in range(5):
        m = mk(s)
        m.fit(X_tr, y_tr)
        yh = m.predict(X_te)
        mses.append(mean_squared_error(y_te, yh))
    rmse_mean = float(np.sqrt(np.mean(mses)))
    results[name] = {"mses": [float(x) for x in mses], "rmse_5seed_mean": rmse_mean,
                     "expected_rmse": expected.get("SVM" if name.startswith("SVM") else "RF")}
    print(f"{name}: per-seed MSE {[round(m,4) for m in mses]}, 5-seed mean RMSE {rmse_mean:.4f}, "
          f"expected {results[name]['expected_rmse']}")

# tolerance check
for name, r in results.items():
    exp = r["expected_rmse"]
    tol = exp * 0.10
    ok = abs(r["rmse_5seed_mean"] - exp) <= tol
    print(f"{name}: reproduced={'YES' if ok else 'NO'} (|diff| {abs(r['rmse_5seed_mean']-exp):.4f} vs tol {tol:.4f})")

json.dump(results, open(os.path.join(RUN, "baseline", "baseline_results.json"), "w"), indent=1)
print("WROTE baseline/baseline_results.json")
