"""Freeze and score once: model kinds 'gbm' (plain GBM), 'blend' (w_s * GBM + (1 - w_s) * linear per season) and
'hybrid' (GBM fitted on the residual of the linear model, init offset). All fitting uses the 18 training glaciers only.
The frozen JSON records the sha256 of every code file the model uses (all in this folder); 'score' refuses to run if
any of them changed, refits from the training CSV, checks the training fit equals the frozen one, then scores the test
glaciers once and appends one line to the ledger. Writes only to the paths given on the command line.
Usage: python3 -I -B freeze_score.py freeze <frozen.json> <name> <kind> '<gbm cfg json>' '<extra json: n_trees, w_gbm, chosen_by>'
       python3 -I -B freeze_score.py score <frozen.json> <ledger.tsv> <test monthly pred .npy> '<ledger note>'"""
import datetime, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, mbdata, gbm, feats, score
import combined as C

SEASON = {12: "Ba", 7: "Bw", 5: "Bs"}
CODE = ("mbdata.py", "score.py", "gbm.py", "feats.py", "cv_linear.py", "combined.py", "freeze_score.py")


def code_sha():
    return {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in CODE}


def build(fz, tr):
    c = dict(fz["cfg"]); c["n_max"] = fz["n_trees"]
    X, _ = feats.build(tr, c["fs"])
    coefs = C.fit_all(tr); coefs["route"] = "direct"
    lin_tr = C.monthly(tr, coefs)
    m = gbm.GBM(n_trees=c["n_max"], lr=c["lr"], depth=c["depth"], lam=c["lam"], min_child=c["min_child"],
                subsample=c["subsample"], colsample=c.get("colsample", 1), seed=c["seed"], monotone=c.get("monotone"))
    m.fit(X, tr["gid"], tr["balance"], init=lin_tr if fz["kind"] == "hybrid" else None)
    return m, coefs


def predict(fz, m, coefs, d):
    X, _ = feats.build(d, fz["cfg"]["fs"]); lin = C.monthly(d, coefs)
    if fz["kind"] == "gbm":
        return m.predict(X)
    if fz["kind"] == "hybrid":
        return m.predict(X, init=lin)
    g = m.predict(X); w = np.array([fz["w_gbm"][SEASON[int(k)]] for k in d["n_months"]])
    return w * g + (1 - w) * lin


if __name__ == "__main__":
    mode, fp = sys.argv[1], sys.argv[2]
    tr = mbdata.load("train")
    if mode == "freeze":
        name, kind, cfg, extra = sys.argv[3], sys.argv[4], json.loads(sys.argv[5]), json.loads(sys.argv[6])
        fz = {"model": name, "kind": kind, "cfg": cfg, "n_trees": extra["n_trees"], "w_gbm": extra.get("w_gbm"),
              "chosen_by": extra.get("chosen_by"), "code_sha256": code_sha()}
        m, coefs = build(fz, tr)
        fz["train_fit"] = score.rmse_by_season(tr["gid"], predict(fz, m, coefs, tr), tr["balance"], tr["n_months"])
        assert not os.path.exists(fp), "refusing to overwrite " + fp
        json.dump(fz, open(fp, "w"), indent=1); print(json.dumps(fz, indent=1))
    else:
        ledger, pred_out, note = sys.argv[3], sys.argv[4], sys.argv[5]
        fz = json.load(open(fp)); assert fz["code_sha256"] == code_sha(), "code changed since freeze"
        m, coefs = build(fz, tr)
        r0 = score.rmse_by_season(tr["gid"], predict(fz, m, coefs, tr), tr["balance"], tr["n_months"])
        assert all(abs(r0[k] - fz["train_fit"][k]) < 1e-12 for k in ("Ba", "Bw", "Bs")), "refit differs from frozen"
        te = mbdata.load("test"); p = predict(fz, m, coefs, te)
        r = score.rmse_by_season(te["gid"], p, te["balance"], te["n_months"], check_counts=True)
        print("TEST", fz["model"], json.dumps(r)); print("2-dec: Ba %.2f Bw %.2f Bs %.2f" % (r["Ba"], r["Bw"], r["Bs"]))
        np.save(pred_out, p)
        with open(ledger, "a") as f:
            f.write("%s\t%s\t%s\t%.4f\t%.4f\t%.4f\t%s\n" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), fz["model"],
                    hashlib.sha256(open(fp, "rb").read()).hexdigest(), r["Ba"], r["Bw"], r["Bs"], note))
