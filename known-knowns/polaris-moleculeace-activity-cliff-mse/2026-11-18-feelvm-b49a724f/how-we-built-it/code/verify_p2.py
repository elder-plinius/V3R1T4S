"""Independent p2 verifier (step 5 self-break): recompute everything from the CSV and the two
prediction files; judge the criterion literally. Standalone, no attack code imported.

Usage: python verify_p2.py
Exit 0 iff every check passes.
"""
import csv
import hashlib
import json
import sys

import numpy as np
from sklearn.metrics import mean_squared_error

RUN = r"<RUNDIR>"
CSV = RUN + r"\data\moleculeace_csv\CHEMBL244_Ki.csv"
SHA_EXPECTED = "b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2"


def main():
    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name + " " + str(detail))
        ok = ok and bool(cond)

    sha = hashlib.sha256(open(CSV, "rb").read()).hexdigest()
    check("csv sha256", sha == SHA_EXPECTED, sha[:16])

    with open(CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    test_rows = [i for i, r in enumerate(rows) if r["split"] == "test"]
    train_rows = [i for i, r in enumerate(rows) if r["split"] == "train"]
    cliff_te = [i for i in test_rows if rows[i]["cliff_mol"] == "1"]
    check("cliff test molecules >= 40", len(cliff_te) >= 40, len(cliff_te))

    def load(p):
        d = json.load(open(p))
        check("  indices exact", d["test_row_indices"] == test_rows)
        check("  sha recorded", d["csv_sha256"] == SHA_EXPECTED)
        return np.array(d["y_pred"], dtype=float)

    M1 = load(RUN + r"\attempts\cliff-fx\result\M1_predictions.json")
    B = load(RUN + r"\baseline\baseline_B_test_predictions.npy" if False else RUN +
             r"\attempts\cliff-fx\result\B_predictions.json")

    y = np.array([float(rows[i]["y"]) for i in test_rows])
    cm = np.array([rows[i]["cliff_mol"] == "1" for i in test_rows])

    m1_cliff, m1_non = mean_squared_error(y[cm], M1[cm]), mean_squared_error(y[~cm], M1[~cm])
    b_cliff, b_non = mean_squared_error(y[cm], B[cm]), mean_squared_error(y[~cm], B[~cm])
    print(f"M1  cliff {m1_cliff:.6f} noncliff {m1_non:.6f}")
    print(f"B   cliff {b_cliff:.6f} noncliff {b_non:.6f}")
    check("cliff MSE strictly lower", m1_cliff < b_cliff, f"delta {b_cliff - m1_cliff:.6f}")
    check("noncliff not worse", m1_non <= b_non, f"delta {m1_non - b_non:.6f}")

    # baseline fidelity: B must equal the repo-config SVR predictions recomputed here
    sys.path.insert(0, RUN + r"\.venv-mace\Lib\site-packages")  # not used; venv python runs this
    from rdkit import Chem
    from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
    from sklearn.svm import SVR

    def ecfp(ms, r=2, n=1024):
        X = np.zeros((len(ms), n))
        for i, m in enumerate(ms):
            fp = GetMorganFingerprintAsBitVect(m, r, nBits=n)
            for b in fp.GetOnBits():
                X[i, b] = 1
        return X

    mols_tr = [Chem.MolFromSmiles(rows[i]["smiles"]) for i in train_rows]
    mols_te = [Chem.MolFromSmiles(rows[i]["smiles"]) for i in test_rows]
    y_tr = np.array([float(rows[i]["y"]) for i in train_rows])
    Xtr, Xte = ecfp(mols_tr), ecfp(mols_te)
    m = SVR(C=10, epsilon=0.1, gamma=0.01).fit(Xtr, y_tr)
    yb = m.predict(Xte)
    check("B == repo-config SVR recomputed", float(np.max(np.abs(yb - B))) < 1e-9,
          f"max diff {np.max(np.abs(yb - B)):.2e}")

    # no test molecule (by stereo-stripped InChIKey) in train
    from rdkit.Chem.inchi import MolToInchiKey
    def ik(i):
        mm = Chem.Mol(mols_te[0]) if False else Chem.MolFromSmiles(rows[i]["smiles"])
        Chem.RemoveStereochemistry(mm)
        return MolToInchiKey(mm)
    tr_iks = set(ik(i) for i in train_rows)
    te_iks = set(ik(i) for i in test_rows)
    check("no InChIKey train/test overlap", not (tr_iks & te_iks))

    print("VERIFY_P2:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
