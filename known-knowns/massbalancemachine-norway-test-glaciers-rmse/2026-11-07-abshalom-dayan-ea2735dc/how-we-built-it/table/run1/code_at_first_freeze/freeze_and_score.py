"""Freeze a linear winter model (fit on all 18 training glaciers), write frozen JSON, then (with --score) score it once
on the test glaciers with lib/score.py and append to test_ledger.tsv.
Usage: python3 -I freeze_and_score.py <name> <comma-separated phis> [--score]"""
import hashlib, json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RUN = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(RUN, "lib"))
import numpy as np, mbdata, score
import cv_linear as L
name, cols = sys.argv[1], sys.argv[2].split(",")
assert len(cols) <= 20
tr = mbdata.load("train")
A, y, _ = L.design(tr, cols)
b = L.fit(A, y)
code_sha = {f: hashlib.sha256(open(os.path.join(p, f), "rb").read()).hexdigest()
            for p, f in [(HERE, "cv_linear.py"), (HERE, "freeze_and_score.py"), (os.path.join(RUN, "lib"), "mbdata.py"), (os.path.join(RUN, "lib"), "score.py")]}
frozen = {"model": name, "phis": cols, "coef": b.tolist(), "n_fitted_params": len(b), "season": "Bw (n_months 7)",
          "train_rmse_Bw": float(np.sqrt(np.mean((A @ b - y) ** 2))), "code_sha256": code_sha}
fp = os.path.join(HERE, "..", "frozen_%s.json" % name)
if "--score" not in sys.argv:
    json.dump(frozen, open(fp, "w"), indent=1); print(json.dumps(frozen, indent=1)); sys.exit()
fz = json.load(open(fp)); assert fz["coef"] == frozen["coef"], "refit differs from frozen"
fsha = hashlib.sha256(open(fp, "rb").read()).hexdigest()
te = mbdata.load("test")
P = L.phis(te)
monthly = sum(c * P[n] for c, n in zip(fz["coef"], fz["phis"]))
w = te["n_months"] == 7
r = score.rmse_by_season(te["gid"][w], monthly[w], te["balance"][w], te["n_months"][w])
assert r["n_Bw"] == 999
print("TEST", name, "Bw RMSE %.4f (n=%d), 2-dec %.2f" % (r["Bw"], r["n_Bw"], r["Bw"]))
with open(os.path.join(RUN, "test_ledger.tsv"), "a") as f:
    f.write("%s\t%s\t%s\tNA\t%.4f\tNA\tlinear-ti winter-only, %d params\n" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), name, fsha, r["Bw"], len(fz["coef"])))
