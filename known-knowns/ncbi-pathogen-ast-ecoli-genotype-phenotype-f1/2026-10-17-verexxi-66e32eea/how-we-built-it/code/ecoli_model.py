"""Per-antibiotic learned predictor vs the published genotype rule (PMC13513162), cluster-held-out evaluation.
usage: ecoli_model.py PREP_DIR OUT_DIR [split_mode]   split_mode: cluster (default, PREREG primary) | random (p3 demo)
Reads PREP_DIR/isolates.csv.gz, long_rs.csv.gz, split.csv. Test labels are used only in the final scoring block."""
import sys, os, json, hashlib, re, numpy as np, pandas as pd, lightgbm as lgb
from sklearn.model_selection import GroupKFold
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ecoli_rules import ANTIBIOTICS, tokens, predict as rule_predict, ACQ_BLA
prep, out = sys.argv[1], sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "cluster"; os.makedirs(out, exist_ok=True)
iso = pd.read_csv(os.path.join(prep, "isolates.csv.gz"), dtype=str, keep_default_na=False).set_index("target_acc")
L = pd.read_csv(os.path.join(prep, "long_rs.csv.gz"), dtype=str)
sp = pd.read_csv(os.path.join(prep, "split.csv"), dtype=str).set_index("target_acc")
if mode == "random":   # leakage demo: isolate-level split with the same 20% rate, ignoring clusters
    sp["split"] = ["test" if int(hashlib.sha256(("V3R1T4S-ecoli-random|" + k).encode()).hexdigest(), 16) % 100 < 20 else "train" for k in sp.index]
iso["split"] = sp.split; iso["cluster"] = sp.cluster
TOK = {i: tokens(f) for i, f in iso.AMR_genotypes.items()}
train_iso = iso.index[iso.split == "train"]
def tkey(n, s): return ("n:" if s in ("COMPLETE", "POINT") else "p:") + n
cnt = pd.Series([tkey(n, s) for i in train_iso for n, s in set(TOK[i])]).value_counts()
VOC = sorted(cnt[cnt >= 10].index); vix = {k: j for j, k in enumerate(VOC)}
def year(s):
    m = re.search(r"(19|20)\d\d", str(s)); return float(m.group(0)) if m else np.nan
cats = {c: {v: k for k, v in enumerate(sorted(set(iso.loc[train_iso, c])))} for c in ("scientific_name", "epi_type") if c in iso}
def featurize(ids):
    X = np.zeros((len(ids), len(VOC) + 14), dtype=np.float32)
    for r, i in enumerate(ids):
        tk = TOK[i]
        for n, s in tk:
            j = vix.get(tkey(n, s))
            if j is not None: X[r, j] = 1
        b = len(VOC)
        X[r, b] = len(tk)
        X[r, b + 1] = sum(1 for n, s in tk if s in ("COMPLETE", "POINT") and ACQ_BLA.match(n))
        X[r, b + 2] = sum(1 for n, s in tk if s == "POINT" and re.match(r"^(gyrA|parC|parE)_", n))
        for k, ab in enumerate(ANTIBIOTICS): X[r, b + 3 + k] = rule_predict(ab, iso.at[i, "AMR_genotypes"]) == "R"
        X[r, b + 11] = year(iso.at[i, "collection_date"]) if "collection_date" in iso else np.nan
        X[r, b + 12] = cats["scientific_name"].get(iso.at[i, "scientific_name"], -1) if "scientific_name" in cats else -1
        X[r, b + 13] = cats["epi_type"].get(iso.at[i, "epi_type"], -1) if "epi_type" in cats else -1
    return X
P = dict(objective="binary", learning_rate=0.03, num_leaves=15, min_child_samples=20, feature_fraction=0.8,
         bagging_fraction=0.8, bagging_freq=1, lambda_l2=1.0, verbose=-1, num_threads=4, seed=20261016)
def f1acc(y, p):
    tp = int(((p == 1) & (y == 1)).sum()); fp = int(((p == 1) & (y == 0)).sum()); fn = int(((p == 0) & (y == 1)).sum()); tn = int(((p == 0) & (y == 0)).sum())
    return (2 * tp / max(2 * tp + fp + fn, 1)), (tp + tn) / max(len(y), 1), dict(TP=tp, FP=fp, TN=tn, FN=fn)
res = {}; allpred = []
for ab in ANTIBIOTICS:
    g = L[L.antibiotic == ab].copy(); g["split"] = g.isolate.map(iso.split); g["cluster"] = g.isolate.map(iso.cluster)
    tr = g[g.split == "train"].reset_index(drop=True); te = g[g.split == "test"].reset_index(drop=True)
    Xtr = featurize(tr.isolate); ytr = (tr.AST_call == "R").astype(int).to_numpy()
    oof = np.zeros(len(tr)); iters = []
    for k, (a, b) in enumerate(GroupKFold(5).split(Xtr, ytr, tr.cluster)):
        bst = lgb.train(P, lgb.Dataset(Xtr[a], ytr[a]), 3000, valid_sets=[lgb.Dataset(Xtr[b], ytr[b])],
                        callbacks=[lgb.early_stopping(100, verbose=False)])
        iters.append(bst.best_iteration); oof[b] = bst.predict(Xtr[b], num_iteration=bst.best_iteration)
    grid = np.unique(np.round(oof, 4)); best = max(grid, key=lambda t: f1acc(ytr, (oof >= t).astype(int))[0])
    nt = int(np.mean(iters)); bst = lgb.train(P, lgb.Dataset(Xtr, ytr), nt)
    bst.save_model(os.path.join(out, f"model_{ab.replace(' ', '_')}.txt"))
    Xte = featurize(te.isolate); prob = bst.predict(Xte); pm = (prob >= best).astype(int)
    pr = np.array([rule_predict(ab, iso.at[i, "AMR_genotypes"]) == "R" for i in te.isolate]).astype(int)
    # ---- final scoring: the only use of test labels ----
    yte = (te.AST_call == "R").astype(int).to_numpy()
    f1m, accm, cmm = f1acc(yte, pm); f1r, accr, cmr = f1acc(yte, pr)
    cl = te.cluster.to_numpy(); uc, inv = np.unique(cl, return_inverse=True)
    rows_of = [np.where(inv == k)[0] for k in range(len(uc))]
    rng = np.random.default_rng(20261016); bm, br = [], []
    for _ in range(10000):
        idx = np.concatenate([rows_of[k] for k in rng.integers(0, len(uc), len(uc))])
        bm.append(f1acc(yte[idx], pm[idx])[0]); br.append(f1acc(yte[idx], pr[idx])[0])
    bm, br = np.array(bm), np.array(br); d = bm - br
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    res[ab] = dict(n_train=len(tr), n_test=len(te), n_test_clusters=len(uc), test_R=int(yte.sum()), n_trees=nt, threshold=float(best),
                   oof_train_f1=f1acc(ytr, (oof >= best).astype(int))[0],
                   model=dict(F1=f1m, accuracy=accm, CI_F1=q(bm), **cmm), rule=dict(F1=f1r, accuracy=accr, CI_F1=q(br), **cmr),
                   diff_CI=q(d), vocab=len(VOC), mode=mode)
    print(ab, json.dumps({k: v for k, v in res[ab].items() if k in ("n_test", "test_R", "model", "rule", "diff_CI")}), flush=True)
    allpred.append(pd.DataFrame(dict(isolate=te.isolate, antibiotic=ab, cluster=te.cluster, AST_call=te.AST_call,
                                     rule_pred=np.where(pr == 1, "R", "S"), model_prob=np.round(prob, 6), model_pred=np.where(pm == 1, "R", "S"))))
json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
pd.concat(allpred).to_csv(os.path.join(out, "test_predictions.csv"), index=False)
print("JOB DONE", flush=True)
