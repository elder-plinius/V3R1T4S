# RUN IT YOURSELF

Everything runs from this package folder. `object/preds.csv` is the claimed object; the check needs
only a Python 3.8+ interpreter (standard library; no third-party packages).

## 1. The one-command check

POSIX shells / Git-bash / WSL:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: ~30 seconds (rows, metrics, margin, a 10,000-resample
bootstrap, the null-model calibration, a corruption self-test, and an online cross-check of the
official input pins that is skipped silently when offline). The full checker output is captured in
`verify-it-yourself/RECEIPTS.md`.

The checker re-implements PR-AUC and ROC-AUC from the definition in pure Python (validated against
scikit-learn to 12 decimals in the producing run) and verifies:

- 132 prediction rows, in the exact official `split[1]` order, probabilities in [0,1] for both
  targets, against the official test labels recorded in `object/official_inputs.json`;
- CLASS_LOK pr_auc **0.634333770922**, roc_auc 0.880208333333, CLASS_SLK pr_auc 0.377856659137,
  two-target mean 0.506095215029;
- the margin rule: CLASS_LOK pr_auc >= 0.2553191489361702 + 0.020;
- the bootstrap rule: >= 95% of 10,000 test-row resamples above the best listed value
  (measured: 1.000000);
- the harness calibration: a constant all-positive prediction gives exactly the listed null-model
  values (CLASS_LOK 0.18181818181818182 = 24/132, CLASS_SLK 0.09848484848484848 = 13/132).

## 2. Re-derive the official labels yourself (optional, needs pandas + pyarrow)

`object/official_inputs.json` records the official split and the 132 test labels together with the
sha256 pins of the official files. To re-extract them from the primary source instead:

```sh
curl -sS -o table.parquet https://data.polarishub.io/dataset/polaris/kinase-pkis2-1/table.parquet
curl -sS -o bench.json https://polarishub.io/api/v1/benchmark/polaris/pkis2-lok-slk-c-1
python - <<'EOF'
import json, hashlib, pandas as pd
print(hashlib.sha256(open('table.parquet','rb').read()).hexdigest())
print(hashlib.sha256(open('bench.json','rb').read()).hexdigest())
b = json.load(open('bench.json')); df = pd.read_parquet('table.parquet')
te = b['split'][1]
yL = df['CLASS_LOK'].to_numpy(float)[te]; yS = df['CLASS_SLK'].to_numpy(float)[te]
print('test rows', len(te), 'LOK positives', int(yL.sum()), 'SLK positives', int(yS.sum()))
EOF
```

The two printed hashes must equal the pins in `object/official_inputs.json`
(`table_v1.parquet` 653d2b6f..., bench json b7a58de2...). `run_checks.sh` does this cross-check
automatically when online.

## 3. Retrain the frozen recipe from scratch (optional, needs rdkit + lightgbm + scikit-learn)

```sh
cd how-we-built-it
curl -sS -O https://data.polarishub.io/dataset/polaris/kinase-pkis2-1/table.parquet
curl -sS -O https://polarishub.io/api/v1/benchmark/polaris/pkis2-lok-slk-c-1
python lokslk_pipeline.py
```

Writes `preds.csv` (132 rows). Fitting takes about 10 minutes on a laptop CPU and reproduces the
shipped object's ranking (the Platt coefficients are printed as a=9.000716 b=-7.882329 for CLASS_LOK
and a=5.744524 b=-5.822587 for CLASS_SLK). The recipe fits only on the 508 official train rows; no
test-row label is read anywhere in the script.
