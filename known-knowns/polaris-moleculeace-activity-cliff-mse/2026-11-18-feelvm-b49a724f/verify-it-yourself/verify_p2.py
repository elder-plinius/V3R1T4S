"""Standalone verifier for the p2 claim — written from the criterion definition alone.

Run from the package folder:
    python verify-it-yourself/verify_p2.py   (or sh verify-it-yourself/run_checks.sh)

Needs: python with scikit-learn + rdkit (pinned: scikit-learn 1.9.1, rdkit 2026.09.2; any recent
version works — the objects are deterministic SVR fits). The MoleculeACE CSV is fetched from its
public source on first run and pinned by sha256 (no dataset is bundled in this package).
"""
import csv
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
CSV_URL = "https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL244_Ki.csv"
CSV = os.path.join(PKG, "data_CHEMBL244_Ki.csv")   # fetched on demand, kept for reruns
SHA_EXPECTED = "b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2"


def get_csv():
    if not os.path.exists(CSV):
        print("fetching", CSV_URL)
        req = urllib.request.Request(CSV_URL, headers={"User-Agent": "V3R1T4S-package-verifier"})
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
        open(CSV, "wb").write(body)
    return CSV


def main():
    import numpy as np
    from sklearn.metrics import mean_squared_error

    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name + " " + str(detail))
        ok = ok and bool(cond)

    p = get_csv()
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    check("csv sha256", sha == SHA_EXPECTED, sha[:16])

    with open(p, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    test_rows = [i for i, r in enumerate(rows) if r["split"] == "test"]
    train_rows = [i for i, r in enumerate(rows) if r["split"] == "train"]
    cliff_te = [i for i in test_rows if rows[i]["cliff_mol"] == "1"]
    check("cliff test molecules >= 40", len(cliff_te) >= 40, len(cliff_te))
    check("test/train sizes 621/2476", len(test_rows) == 621 and len(train_rows) == 2476)

    def load(rel):
        d = json.load(open(os.path.join(PKG, rel)))
        check("  " + rel + " indices exact", d["test_row_indices"] == test_rows)
        check("  " + rel + " sha recorded", d["csv_sha256"] == SHA_EXPECTED)
        check("  " + rel + " one y per test molecule", len(d["y_pred"]) == len(test_rows))
        return np.array(d["y_pred"], dtype=float)

    M1 = load(os.path.join("object", "M1_predictions.json"))
    B = load(os.path.join("object", "B_predictions.json"))

    y = np.array([float(rows[i]["y"]) for i in test_rows])
    cm = np.array([rows[i]["cliff_mol"] == "1" for i in test_rows])

    m1_cliff, m1_non = mean_squared_error(y[cm], M1[cm]), mean_squared_error(y[~cm], M1[~cm])
    b_cliff, b_non = mean_squared_error(y[cm], B[cm]), mean_squared_error(y[~cm], B[~cm])
    print(f"M1  cliff {m1_cliff:.9f} noncliff {m1_non:.9f}")
    print(f"B   cliff {b_cliff:.9f} noncliff {b_non:.9f}")
    check("cliff MSE strictly lower", m1_cliff < b_cliff, f"delta {b_cliff - m1_cliff:.6f}")
    check("noncliff not worse", m1_non <= b_non, f"delta {m1_non - b_non:.6f}")

    # baseline fidelity: B must equal the repo-config SVR recomputed from the definition
    from rdkit import Chem, RDLogger
    from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
    from sklearn.svm import SVR
    RDLogger.DisableLog("rdApp.*")

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

    from rdkit.Chem.inchi import MolToInchiKey
    def ik(i):
        mm = Chem.MolFromSmiles(rows[i]["smiles"])
        Chem.RemoveStereochemistry(mm)
        return MolToInchiKey(mm)
    tr_iks = set(ik(i) for i in train_rows)
    te_iks = set(ik(i) for i in test_rows)
    check("no InChIKey train/test overlap", not (tr_iks & te_iks))

    print("VERIFY_P2:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
