"""Freeze and score once a linear winter model (fit on all 18 training glaciers; LW1 of run 2026-11-07-1434).
The frozen JSON records the sha256 of every code file used (all in this folder); 'score' refuses to run if any changed,
refits, checks the coefficients equal the frozen ones exactly, scores the 999 test winter points once and appends one
line to the ledger. Writes only to the paths given on the command line.
Usage: python3 -I -B freeze_linear.py freeze <frozen.json> <name> <comma-separated phis> '<chosen_by text>'
       python3 -I -B freeze_linear.py score <frozen.json> <ledger.tsv> '<ledger note>'"""
import datetime, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, mbdata, score
import cv_linear as L
CODE = ("mbdata.py", "score.py", "feats.py", "cv_linear.py", "freeze_linear.py")


def code_sha():
    return {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in CODE}


if __name__ == "__main__":
    mode, fp = sys.argv[1], sys.argv[2]
    tr = mbdata.load("train")
    if mode == "freeze":
        name, cols, chosen_by = sys.argv[3], sys.argv[4].split(","), sys.argv[5]
        assert len(cols) <= 20
        A, y, _ = L.design(tr, cols, season=7)
        b = L.fit(A, y)
        fz = {"model": name, "phis": cols, "coef": b.tolist(), "n_fitted_params": len(b), "season": "Bw (n_months 7)",
              "train_rmse_Bw": float(np.sqrt(np.mean((A @ b - y) ** 2))), "chosen_by": chosen_by, "code_sha256": code_sha()}
        assert not os.path.exists(fp), "refusing to overwrite " + fp
        json.dump(fz, open(fp, "w"), indent=1); print(json.dumps(fz, indent=1))
    else:
        ledger, note = sys.argv[3], sys.argv[4]
        fz = json.load(open(fp)); assert fz["code_sha256"] == code_sha(), "code changed since freeze"
        A, y, _ = L.design(tr, fz["phis"], season=7)
        assert L.fit(A, y).tolist() == fz["coef"], "refit differs from frozen"
        te = mbdata.load("test"); P = L.phis(te)
        monthly = sum(c * P[n] for c, n in zip(fz["coef"], fz["phis"]))
        w = te["n_months"] == 7
        r = score.rmse_by_season(te["gid"][w], monthly[w], te["balance"][w], te["n_months"][w])
        assert r["n_Bw"] == 999
        print("TEST", fz["model"], "Bw RMSE %.4f (n=%d), 2-dec %.2f, fitted parameters %d" % (r["Bw"], r["n_Bw"], r["Bw"], len(fz["coef"])))
        with open(ledger, "a") as f:
            f.write("%s\t%s\t%s\tNA\t%.4f\tNA\t%s\n" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), fz["model"],
                    hashlib.sha256(open(fp, "rb").read()).hexdigest(), r["Bw"], note))
