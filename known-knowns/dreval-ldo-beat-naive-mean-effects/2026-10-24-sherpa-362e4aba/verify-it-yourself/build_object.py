"""Build the claim's object: one plain CSV per CV split per split-generation, holding the ground truth and
both models' predictions for every test pair, plus the drug role of every drug in that split.
Values are rounded to 6 decimals (lnIC50 is O(1); the metric is quoted to 4 decimals)."""
import pathlib, pandas as pd
RES = pathlib.Path("${RESULTS}"); OUT = pathlib.Path("claim/object")
GEN = {"seed42": "repro_seed42", "independent": "indep_seed20261023"}
for tag, rid in GEN.items():
    base = RES / rid / "CTRPv2" / "LDO"; tot = 0
    for i in range(10):
        a = pd.read_csv(base / "PotencyTransfer" / "predictions" / f"predictions_split_{i}.csv", dtype={"pubchem_id": str})
        b = pd.read_csv(base / "NaiveMeanEffectsPredictor" / "predictions" / f"predictions_split_{i}.csv", dtype={"pubchem_id": str})
        # CTRPv2 contains 4,118 duplicated (cell line, drug) keys, so a key merge is not one-to-one.
        # drevalpy writes every model's predictions in the same test-set row order, which is VERIFIED
        # here rather than assumed: the identifier and ground-truth columns must agree row for row.
        assert len(a) == len(b), f"{tag} split {i}: differing row counts"
        assert (a.cell_line_name.values == b.cell_line_name.values).all(), f"{tag} split {i}: cell line order differs"
        assert (a.pubchem_id.values == b.pubchem_id.values).all(), f"{tag} split {i}: drug order differs"
        assert (a.response.round(9).values == b.response.round(9).values).all(), f"{tag} split {i}: ground truth differs"
        m = a.rename(columns={"predictions": "pred_PotencyTransfer"}).copy()
        m["pred_NaiveMeanEffectsPredictor"] = b["predictions"].values
        for c in ("response", "pred_PotencyTransfer", "pred_NaiveMeanEffectsPredictor"): m[c] = m[c].round(6)
        p = OUT / f"{tag}_split_{i}_test_predictions.csv.gz"
        m.to_csv(p, index=False, compression={"method": "gzip", "mtime": 0}); tot += p.stat().st_size
    sp = base / "splits"; rows = []
    for i in range(10):
        for role in ("train", "validation", "test"):
            f = sp / f"cv_split_{i}_{role}.csv"
            if f.exists():
                rows += [{"CV_split": i, "role": role, "pubchem_id": d} for d in sorted(pd.read_csv(f, dtype=str)["pubchem_id"].unique())]
    p = OUT / f"{tag}_split_drug_roles.csv.gz"
    pd.DataFrame(rows).to_csv(p, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"{tag}: 10 per-split files, {tot/1e6:.2f} MB total, largest {max((OUT/f'{tag}_split_{i}_test_predictions.csv.gz').stat().st_size for i in range(10))/1e6:.2f} MB; roles {p.stat().st_size/1e3:.0f} kB")
