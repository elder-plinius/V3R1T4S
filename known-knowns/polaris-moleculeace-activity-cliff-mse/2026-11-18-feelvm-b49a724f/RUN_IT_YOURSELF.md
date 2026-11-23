# RUN IT YOURSELF

Everything below runs from this package folder. `<PYTHON>` = any python with scikit-learn +
rdkit installed (the producing run used scikit-learn 1.9.1, rdkit 2026.09.2; the objects are
deterministic SVR fits, so versions only need to be recent). Nothing in this folder contains a
dataset: the MoleculeACE CSV is fetched from its public source and pinned by sha256.

## 1. The one-command check (standalone, from the definition)

```
sh verify-it-yourself/run_checks.sh
```

Expected final line: `VERIFY_P2: PASS`. What it recomputes from scratch: official split
(2476/621), 296 cliff test molecules, both prediction files' exact test-row indices and csv
sha, cliff-subset MSE (M1 0.550194 vs B 0.634574 — strictly lower), non-cliff MSE
(0.333430 vs 0.399311 — not worse), the baseline B recomputed from the definition
(SVR C=10, epsilon=0.1, gamma=0.01, rbf, Morgan ECFP radius 2 / 1024 bits, official train
rows; max diff 0.00e+00 vs object/B_predictions.json), and stereo-stripped InChIKey
train/test disjointness. ~1 minute laptop CPU + one CSV fetch.

## 2. Rebuild the object from scratch (optional; ~2 minutes)

The recipe is in object/spec_m1.json (6 SVR members with configs + combiner weights).
A re-implementation from that spec must produce bit-identical predictions:

```python
import json, numpy as np
from sklearn.svm import SVR
from rdkit import Chem
from sklearn.linear_model import Ridge
# 1) fetch the pinned CSV, parse train rows (split=='train'), compute Morgan r=2 1024-bit ECFP4,
#    Morgan r=3 2048-count ECFP6CNT, and feature-connectivity r=2 1024-bit FCFP4 fingerprints
# 2) fit the 6 SVRs of spec_m1.json on all 2476 train rows (column 'y')
# 3) apply the spec's non-negative-ridge weights to the 6 test predictions
# -> equals object/M1_predictions.json to floating-point exactness
```

The producing code for every number in this package is in how-we-built-it/code/ (paths inside
those copies are shown relative to the producing run folder; the working entry points are
baseline_B_244.py, M1_read.py, null_test_244.py, sweep_244.py on top of mace_common.py).

## 3. The null test (optional; ~2 h laptop CPU)

400 label-shuffle controls of the frozen recipe (rng seeds 20261118+k): every control lands at
overall test MSE 3.02-4.05 (train-mean level), the real run at 0.436751 — see
how-we-built-it/null_test.md.

## What came from where

- CHEMBL244_Ki.csv: molML/MoleculeACE main,
  MoleculeACE/Data/benchmark_data/CHEMBL244_Ki.csv (sha256 b296c595...)
- Baseline config: MoleculeACE/Data/configures/benchmark/CHEMBL244_Ki/SVM_ECFP.yml
- Baseline published values: MoleculeACE/Data/results/MoleculeACE_results.csv
  (row CHEMBL244_Ki/SVM/ECFP: rmse 0.715, cliff_rmse 0.797)
