"""Genuinely independent LDO split generation (PREREG.v5). drevalpy 1.3.5's own split_dataset, with one
change: GroupKFold inside drevalpy.datasets.dataset is given shuffle=True and the seed, so the package's
stated intent ('shuffle, since GroupKFold does not implement this') actually takes effect.
Accepts the generation only if it passes the pre-registered independence check against seed 42."""
import os
import sys, os, functools, numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
import drevalpy.datasets.dataset as dsmod
from drevalpy.datasets.loader import load_ctrpv2
out, seed, ref = sys.argv[1], int(sys.argv[2]), sys.argv[3]
dsmod.GroupKFold = functools.partial(GroupKFold, shuffle=True, random_state=seed)
ds = load_ctrpv2(path_data=os.environ.get("DATA", "./data")); ds.remove_nan_responses()
ds.split_dataset(n_cv_splits=10, mode="LDO", split_validation=True, validation_ratio=0.1, random_state=seed)
new = [frozenset(s["test"].drug_ids.astype(str)) for s in ds.cv_splits]
old = [frozenset(pd.read_csv(f"{ref}/cv_split_{i}_test.csv", dtype=str)["pubchem_id"]) for i in range(10)]
J = np.array([[len(a & b) / len(a | b) for b in old] for a in new])
identical = sum(a in set(old) for a in new); mean_best = J.max(1).mean()
print(f"test folds identical to a seed-42 fold: {identical}/10   mean best-match Jaccard: {mean_best:.3f}   max: {J.max():.3f}")
print("fold sizes (drugs):", [len(a) for a in new], "| union covers", len(frozenset().union(*new)), "drugs")
assert identical == 0 and mean_best < 0.25, "independence check FAILED -- generation rejected"
os.makedirs(out, exist_ok=True); ds.save_splits(path=out); print("ACCEPTED; saved to", out)
