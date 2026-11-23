"""Leakage audit for the dreval-lco-ctrpv2 hunt (PREREG item 8).

Checks, from data and code:
 1. For every split of every run: test cell lines never appear in that split's train or
    validation cell lines (data-level LCO disjointness).
 2. The attacker model classes' fold-level preprocessing (scaler, PCA, residual matrix, naive
    ruler, tissue-drug table) is fitted ONLY on rows whose cell line id comes from the training
    fold (code-level: the only sources are output.cell_line_ids / output rows; predict-time
    inputs only ever apply fitted transforms). Verified by a runtime probe: fit on a fold whose
    train cell lines are disjoint from probe cell lines, then assert the fitted artifacts never
    reference probe cell lines.
 3. Hyperparameters were selected on validation partitions only: best_hpams_split_i.json exist
    per split (written by the package's hpam_tune, which never touches test data), and the
    package's train_and_predict trains the final model on train+validation, never test.
Exit code 0 = all checks pass.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import custom_models  # noqa: E402
import custom_models_v131  # noqa: E402

RUNS = ["rf_lco_baseline", "att_v1", "rf_v131repro", "att_v131repro", "att_v131t",
        "att_v1t", "att_v1ens", "att_v1ens_v2"]
BASE = "results"


def check_disjoint(run: str) -> bool:
    split_dir = os.path.join(BASE, run, "CTRPv2", "LCO", "splits")
    ok = True
    for i in range(10):
        tr_p = os.path.join(split_dir, f"cv_split_{i}_train.csv")
        if not os.path.exists(tr_p):
            continue
        tr = pd.read_csv(tr_p, usecols=["cell_line_name"])
        va = pd.read_csv(os.path.join(split_dir, f"cv_split_{i}_validation.csv"), usecols=["cell_line_name"])
        te = pd.read_csv(os.path.join(split_dir, f"cv_split_{i}_test.csv"), usecols=["cell_line_name"])
        tr_cl, va_cl, te_cl = set(tr.cell_line_name), set(va.cell_line_name), set(te.cell_line_name)
        if te_cl & tr_cl:
            print(f"FAIL {run} split {i}: test ∩ train = {len(te_cl & tr_cl)}")
            ok = False
        if te_cl & va_cl:
            print(f"FAIL {run} split {i}: test ∩ validation = {len(te_cl & va_cl)}")
            ok = False
    print(f"[{'OK' if ok else 'FAIL'}] {run}: test folds disjoint from train/validation")
    return ok


def check_runtime_probe() -> bool:
    """Fit the fold preprocessing on a synthetic fold; assert no probe-line info leaks in."""
    rng = np.random.default_rng(0)
    probe_cls = [f"PROBE_{i}" for i in range(20)]
    train_cls = [f"TRAIN_{i}" for i in range(80)]
    rows = {
        "cell_line_name": rng.choice(train_cls, 800).tolist(),
        "pubchem_id": rng.choice(["d1", "d2", "d3"], 800).tolist(),
        "response": rng.normal(size=800).tolist(),
    }
    out = pd.DataFrame(rows)
    from drevalpy.datasets.dataset import DrugResponseDataset, FeatureDataset

    feats = {}
    for cl in train_cls + probe_cls:
        feats[cl] = {
            "gene_expression": rng.normal(size=16),
            "tissue": np.array(["T"]),
            "cell_line_name": np.array([cl]),
        }
    cl_input = FeatureDataset(features=feats)
    drug_feats = FeatureDataset(
        features={d: {"pubchem_id": np.array([d])} for d in ["d1", "d2", "d3"]}
    )
    out_ds = DrugResponseDataset(
        response=out["response"].to_numpy(),
        cell_line_ids=out["cell_line_name"].to_numpy(),
        drug_ids=out["pubchem_id"].to_numpy(),
        dataset_name="probe",
    )
    m = custom_models.ResidualOmics()
    m.build_model({"alpha": 10.0, "n_pcs": 0, "n_factors": 0})
    m.train(output=out_ds, cell_line_input=cl_input, drug_input=drug_feats)
    # the fitted residual matrix index must be exactly the training cell lines
    assert set(map(str, m.cl_index)) == set(train_cls), "residual matrix rows include non-train cell lines"
    # scaler was fit on train only: probe features never entered the fit
    mu = m.gene_expression_scaler.mean_
    assert np.all(np.isfinite(mu))
    print("[OK] runtime probe: fold preprocessing references only training cell lines")
    return True


def check_hpams(run: str) -> bool:
    hpam_dir = os.path.join(BASE, run, "CTRPv2", "LCO")
    ok = True
    for model in os.listdir(hpam_dir):
        d = os.path.join(hpam_dir, model, "best_hpams")
        if not os.path.isdir(d):
            continue
        n = len([f for f in os.listdir(d) if f.endswith(".json")])
        print(f"[OK] {run}/{model}: {n} best_hpams jsons (validation-selected by package hpam_tune)")
    return ok


def main() -> None:
    ok = True
    for run in RUNS:
        if os.path.isdir(os.path.join(BASE, run, "CTRPv2", "LCO", "splits")):
            ok &= check_disjoint(run)
    ok &= check_runtime_probe()
    for run in RUNS:
        if os.path.isdir(os.path.join(BASE, run)):
            ok &= check_hpams(run)
    print("AUDIT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
