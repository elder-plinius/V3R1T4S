# RUN_IT_YOURSELF

## A. Verify the claim from the package alone (~1 min, stdlib only)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. It recomputes normalized Pearson 0.459961 / Spearman 0.443224 /
R^2 0.208691 (SE 0.013799) from `object/predictions/*.csv.gz` and
`object/naive_v131/*.csv.gz`, checks the p2 margins (+0.0253 / +0.0149 / R^2 floor) and the
honest near-miss (margin +0.0230 < 2xSE 0.0276), and verifies object sha256s.

## B. Full pipeline reproduction (~4-6 h, 16 cores; needs Python 3.11-3.13)

```sh
python3 -m venv venv && venv/Scripts/pip install drevalpy==1.6.0   # Windows path; on unix: venv/bin/pip
# data (the package's own dataset):
mkdir -p data && cd data
curl -A "V3R1T4S-agent/1.0" -o CTRPv2.zip "https://zenodo.org/api/records/23159774/files/CTRPv2.zip/content"
curl -A "V3R1T4S-agent/1.0" -o meta.zip "https://zenodo.org/api/records/23159774/files/meta.zip/content"
unzip -o CTRPv2.zip && unzip -o meta.zip && cd ..
cp how-we-built-it/*.py .
python3 run_ens_v2.py                        # the claim run (writes results/att_v1ens_v2/...)
python3 compute_naive_preds_v131.py att_v1ens_v2
python3 recompute_normalized.py att_v1ens_v2 EnsembleResidualOmics results v131
# expected: MEAN normR2=0.2087 (SE 0.0138)  normPearson=0.4600  normSpearman=0.4432
python3 run_model.py LN_IC50_curvecurator rf_check RandomForest   # same-splits baseline
python3 compute_naive_preds_v131.py rf_check
python3 recompute_normalized.py rf_check RandomForest results v131
# expected: MEAN normR2=0.1857 (SE 0.0122)  normPearson=0.4329  (published 0.1852/0.4347)
python3 audit_leakage.py                     # expect: AUDIT: PASS
```

RF trees are stochastic: expect +-0.005 run-to-run jitter on the baseline (the 0.02 gate
tolerance covers it). The attacker run is deterministic given the package version.

## C. Regenerate the CV splits byte-identically (~30 min)

The split CSVs are not in the package (114 MB); they are deterministic outputs of the pinned
package. Regenerate and compare sha256 against `object/SPLITS_MANIFEST.csv`:

```python
from drevalpy.datasets.loader import load_ctrpv2
resp = load_ctrpv2(path_data='data', measure='LN_IC50_curvecurator')
resp.remove_nan_responses()
resp.split_dataset(n_cv_splits=10, mode='LCO', split_validation=True,
                   validation_ratio=0.1, random_state=42, split_early_stopping=True)
resp.save_splits(path='fresh_splits')
# compare sha256 of fresh_splits/* against object/SPLITS_MANIFEST.csv rows
```

Expect: all 51 files byte-identical (verified during the run and by the panel).
