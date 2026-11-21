"""Reconstruct the public report's LCO CV splits (drevalpy v1.3.1 semantics).

The public report (dilis-lab.github.io/drevalpy-report, evaluation files dated 2025-05-26) was
generated with drevalpy ~v1.3.1. In v1.3.1, _leave_group_out_cv shuffles rows with the LEGACY
global numpy RNG (np.random.seed(42); np.random.permutation) and carves the validation set by
GROUP with train_test_split(unique_train_groups, test_size=0.1, random_state=42) (also legacy
RNG). drevalpy v1.6.0 switched to np.random.default_rng(42), which produces DIFFERENT partitions
at the same nominal seed. The legacy RandomState(42) sequence is stable across numpy/sklearn
versions, so this script reproduces the report's split membership exactly.

Flow replicated from v1.3.1 experiment.py lines 118-132 + dataset.py _leave_group_out_cv:
  1. load CTRPv2.csv exactly as the loader does (dtype str ids, strip commas from pubchem_id)
  2. remove_nan_responses()
  3. np.random.seed(42); shuffled_indices = np.random.permutation(len)
  4. GroupKFold(n_splits=10).split(X, groups=cell_line_ids)  (GroupKFold is deterministic)
  5. per fold: train_test_split(unique_train_groups, test_size=0.1, shuffle=True,
     random_state=42) -> validation cell lines
Writes cv_split_i_{train,validation,test}.csv in the same format drevalpy saves/loads, so the
v1.6.0 pipeline loads them as-is (prepare_response_splits loads existing split dirs).

Usage: python recreate_report_splits.py <output_split_dir>
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, train_test_split

DATA_CSV = os.path.join("data", "CTRPv2", "CTRPv2.csv")
MEASURE = "LN_IC50_curvecurator"


def main() -> None:
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    # step 1: identical read path to drevalpy's _read_response_frame
    df = pd.read_csv(DATA_CSV, dtype={"pubchem_id": str, "cell_line_name": str})
    df["pubchem_id"] = df["pubchem_id"].str.replace(",", "", regex=False)
    response = df[MEASURE].to_numpy()
    cell_line_ids = df["cell_line_name"].to_numpy()
    drug_ids = df["pubchem_id"].to_numpy()
    tissues = df["tissue"].to_numpy()

    # step 2: remove_nan_responses
    mask = ~np.isnan(response)
    response, cell_line_ids, drug_ids, tissues = (
        response[mask], cell_line_ids[mask], drug_ids[mask], tissues[mask],
    )
    print(f"rows after NaN removal: {len(response)}")

    # step 3: legacy global-RNG shuffle (the v1.3.1 semantics)
    np.random.seed(42)
    shuffled = np.random.permutation(len(response))
    response = response[shuffled].copy()
    cell_line_ids = cell_line_ids[shuffled].copy()
    drug_ids = drug_ids[shuffled].copy()
    tissues = tissues[shuffled].copy()

    # step 4: GroupKFold over cell lines
    gkf = GroupKFold(n_splits=10)
    for i, (train_idx, test_idx) in enumerate(gkf.split(response, groups=cell_line_ids)):
        # step 5: v1.3.1 group-level validation split (legacy RNG via train_test_split)
        unique_train_groups = np.unique(cell_line_ids[train_idx])
        train_groups, val_groups = train_test_split(
            unique_train_groups, test_size=0.1, shuffle=True, random_state=42
        )
        train_idx2 = np.where(np.isin(cell_line_ids, train_groups))[0]
        val_idx2 = np.where(np.isin(cell_line_ids, val_groups))[0]
        cols = ["cell_line_name", "pubchem_id", "response", "tissue"]
        for mode, idx in (("train", train_idx2), ("validation", val_idx2), ("test", test_idx)):
            part = pd.DataFrame(
                {
                    "cell_line_name": cell_line_ids[idx],
                    "pubchem_id": drug_ids[idx],
                    "response": response[idx],
                    "tissue": tissues[idx],
                }
            )[cols]
            part.to_csv(os.path.join(out_dir, f"cv_split_{i}_{mode}.csv"), index=False)
        tcl = set(cell_line_ids[test_idx])
        trcl = set(cell_line_ids[train_idx2])
        vacl = set(cell_line_ids[val_idx2])
        print(
            f"split {i}: train {len(train_idx2)} rows / {len(trcl)} CLs; "
            f"val {len(val_idx2)} rows / {len(vacl)} CLs; test {len(test_idx)} rows / {len(tcl)} CLs; "
            f"overlaps train&test={len(tcl & trcl)} val&test={len(tcl & vacl)}"
        )
    print("done")


if __name__ == "__main__":
    main()
