"""The frozen E2 pipeline that produced object/preds.csv, in portable form.

Run from a folder containing the official inputs as:
    table_v1.parquet            (https://data.polarishub.io/dataset/polaris/kinase-pkis2-1/table.parquet)
    bench_pkis2-lok-slk-c-1.json (https://polarishub.io/api/v1/benchmark/polaris/pkis2-lok-slk-c-1)

    python lokslk_pipeline.py            # writes preds.csv (132 rows x 2 targets)

Pinned requirements (any recent versions of the same stack reproduce the same ranking):
    python 3.15.2, scikit-learn 1.9.1, lightgbm, rdkit 2026.09.2, pandas, pyarrow, numpy

Recipe (frozen before the single test read; see PREREG.v3.md in this folder):
  per target T in {CLASS_LOK, CLASS_SLK}:
    A: ExtraTreesRegressor(800, max_features=0.1, min_samples_leaf=1, random_state=0) trained on the
       continuous percent-inhibition label of T over the 508 official train rows;
    B: LGBMClassifier(400, learning_rate=0.05, num_leaves=15, min_child_samples=10, random_state=0)
       trained on the CLASS label of T over the same rows;
    blend: rank-normalise A and B over the 132 test rows and average;
    probability: Platt scaling fitted on the 10-partition out-of-fold blend scores of the train rows
    (monotone, so PR-AUC/ROC are unchanged by it).

No test-row label of any column is read. The features are ECFP4 counts (2048) and 18 RDKit
physchem descriptors computed from the SMILES column.
"""
import json
import os

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, Crippen, Descriptors, rdMolDescriptors
from scipy.stats import rankdata
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
import lightgbm as lgb

RDLogger.DisableLog("rdApp.*")

HERE = os.path.dirname(os.path.abspath(__file__))


def features(smiles):
    mols = [Chem.MolFromSmiles(s) for s in smiles]
    assert all(m is not None for m in mols)
    gen = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
    ecfp = np.vstack([gen.GetCountFingerprintAsNumPy(m).astype(np.float32) for m in mols])
    phys = np.array([[Descriptors.MolWt(m), Descriptors.MolLogP(m),
                      rdMolDescriptors.CalcTPSA(m), rdMolDescriptors.CalcNumHBD(m),
                      rdMolDescriptors.CalcNumHBA(m), rdMolDescriptors.CalcNumRotatableBonds(m),
                      rdMolDescriptors.CalcNumRings(m), rdMolDescriptors.CalcNumAromaticRings(m),
                      rdMolDescriptors.CalcNumAliphaticRings(m), rdMolDescriptors.CalcFractionCSP3(m),
                      rdMolDescriptors.CalcNumHeavyAtoms(m), rdMolDescriptors.CalcNumHeteroatoms(m),
                      rdMolDescriptors.CalcNumAmideBonds(m), rdMolDescriptors.CalcNumBridgeheadAtoms(m),
                      rdMolDescriptors.CalcNumSpiroAtoms(m), Descriptors.LabuteASA(m),
                      Crippen.MolMR(m), Descriptors.BalabanJ(m)]
                     for m in mols], dtype=np.float32)
    # the producing run used cached float32 blocks for both fingerprints and descriptors;
    # replicating that rounding makes the retrained object bit-identical
    return np.hstack([ecfp, phys]).astype(np.float64)


def blend(reg, clf):
    n = len(reg)
    return 0.5 * rankdata(reg) / n + 0.5 * rankdata(clf) / n


def oof_platt(df, tr, X, cont, cls):
    """10 scaffold-grouped partitions; out-of-fold blend scores; Platt fit.

    NOTE: cont and cls are already sliced to the train rows, and the fold indices
    a, b below are POSITIONAL over those train rows, so the feature matrix must
    be the train-sliced matrix X[tr], never the full-table X.
    """
    Xtr = X[tr]
    scaf = []
    for m in [Chem.MolFromSmiles(s) for s in df["smiles"]]:
        try:
            from rdkit.Chem.Scaffolds import MurckoScaffold
            scaf.append(MurckoScaffold.MurckoScaffoldSmiles(mol=m))
        except Exception:
            scaf.append("")
    import hashlib as H
    groups = np.array([int(H.sha256(s.encode()).hexdigest()[:8], 16) for s in scaf])[tr]
    parts = []
    for seed in range(10):
        uniq = np.unique(groups)
        perm = np.random.default_rng(seed).permutation(uniq)
        mp = {u: i for i, u in enumerate(perm)}
        order = np.array([mp[u] for u in groups])
        parts.append(list(GroupKFold(n_splits=5).split(np.zeros((len(tr), 1)), cls, order)))
    oof_reg = np.full((10, len(tr)), np.nan)
    oof_clf = np.full((10, len(tr)), np.nan)
    for s in range(10):
        for a, b in parts[s]:
            m = ExtraTreesRegressor(n_estimators=800, max_features=0.1, min_samples_leaf=1,
                                    random_state=s, n_jobs=8).fit(Xtr[a], cont[a])
            oof_reg[s, b] = m.predict(Xtr[b])
            m = lgb.LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=15,
                                   min_child_samples=10, random_state=s, verbose=-1,
                                   n_jobs=8).fit(Xtr[a], cls[a])
            oof_clf[s, b] = m.predict_proba(Xtr[b])[:, 1]
    n = len(tr)
    per = [0.5 * rankdata(oof_reg[s]) / n + 0.5 * rankdata(oof_clf[s]) / n for s in range(10)]
    oof = np.mean(per, axis=0)
    lr = LogisticRegression(C=1e6, max_iter=1000).fit(oof.reshape(-1, 1), cls.astype(int))
    return float(lr.coef_[0, 0]), float(lr.intercept_[0])


def main():
    bench = json.load(open(os.path.join(HERE, "bench_pkis2-lok-slk-c-1.json")))
    df = pd.read_parquet(os.path.join(HERE, "table_v1.parquet"))
    tr = np.asarray(bench["split"][0], int)
    te = np.asarray(bench["split"][1], int)
    X = features(df["smiles"].tolist())
    out = {}
    for tgt, cont_col in [("CLASS_LOK", "LOK"), ("CLASS_SLK", "SLK")]:
        cont = df[cont_col].to_numpy(float)[tr]
        cls = df[tgt].to_numpy(float)[tr]
        a = ExtraTreesRegressor(n_estimators=800, max_features=0.1, min_samples_leaf=1,
                                random_state=0, n_jobs=8).fit(X[tr], cont)
        reg = a.predict(X[te])
        b = lgb.LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=15,
                               min_child_samples=10, random_state=0, verbose=-1,
                               n_jobs=8).fit(X[tr], cls)
        clf = b.predict_proba(X[te])[:, 1]
        s = blend(reg, clf)
        pa, pb = oof_platt(df, tr, X, cont, cls)
        out[tgt] = np.clip(1.0 / (1.0 + np.exp(-(pa * s + pb))), 1e-6, 1 - 1e-6)
        print(tgt, "platt a=%.6f b=%.6f" % (pa, pb))
    pd.DataFrame({"row_index": te, "CLASS_LOK": out["CLASS_LOK"],
                  "CLASS_SLK": out["CLASS_SLK"]}).to_csv(os.path.join(HERE, "preds.csv"), index=False)
    print("wrote preds.csv with", len(te), "rows")


if __name__ == "__main__":
    main()
