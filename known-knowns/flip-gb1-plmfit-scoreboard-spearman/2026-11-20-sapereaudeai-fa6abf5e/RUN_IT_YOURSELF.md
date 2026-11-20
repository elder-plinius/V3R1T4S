# Run it yourself

Two levels. Level 1 needs nothing but this folder and a Python 3. Level 2 rebuilds the models from the released
data and needs `numpy`, `scipy` and `scikit-learn`.

All commands are run **from this folder**. Where a command says `python`, use your Python 3 (`python3` on most
systems).

## Level 1 - check the claim from the shipped object (no network, no dependencies)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line `PASS`, about 25 seconds. What it prints, group by group, is listed at the top of
`verify-it-yourself/check_gb1_p2.py`. The headline numbers it recomputes:

| configuration | three-seed mean Spearman | sd | this checker's own 95% interval of the mean |
|---|---|---|---|
| A (the claim object) | 0.902852 | 0.000000 | [0.898260, 0.907084] |
| B (additional measurement) | 0.897451 | 0.000000 | - |

The claim's own interval for A, 10,000 resamples under seed 0, is [0.898044, 0.907247]. The checker uses 2,000
resamples under its own seed 20261120 and requires the two to agree to better than 0.002 at each endpoint, which
they do. Percentile endpoints depend on the resampling stream, so an exact match is not expected and is not
required; what matters is that every interval lies about 0.019 above the bar of 0.8791.

## Level 2 - get the data and rebuild everything

### 1. The released file

```sh
curl -L -o gb1_data_full.csv https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/data/gb1/gb1_data_full.csv
sha256sum gb1_data_full.csv
# 93588112a14fe5ad1789fbfd16d63549c3d24f2d9a68ae96967c801a23a529de
```

2,635,816 bytes, 8,733 data rows; the `three_vs_rest` column holds 2,691 `train`, 299 `validation` and 5,743
`test`. The sequences are the full 265-residue 5LDE chain A construct and must be used **unchanged** - never
trimmed, padded or re-derived. The file is not included in this package: it is a third-party dataset.

### 2. Tie the shipped object to the predictions the panel verified

```sh
GB1_CSV=./gb1_data_full.csv sh verify-it-yourself/run_checks.sh
```

This enables check group 9: it rebuilds the four-residue keys and the score column from the released file, and
reconstructs both full-sequence prediction files, which must hash to

```
configuration A  30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2
configuration B  e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490
```

Those are the files the run's REPRODUCE panellist verified. Real output in `verify-it-yourself/RECEIPTS.md`.

### 3. Refit both configurations from scratch

```sh
mkdir -p rebuild
python -I how-we-built-it/code/fit_sealed.py ./gb1_data_full.csv rebuild --config A
python -I how-we-built-it/code/fit_sealed.py ./gb1_data_full.csv rebuild --config B
```

Each prints `DETERMINISM CHECK: 1 distinct prediction-file sha256 over 3 seeds` and writes three byte-identical
files per configuration, with the two sha256 values above. The configurations are literals in that script's
`SEALED` dictionary; they were copied from a record written before this run and are reproduced in
`how-we-built-it/PREREG.md` section 2.

### 4. Score them, and re-run the leakage test

```sh
python -I how-we-built-it/code/boot_mean.py ./gb1_data_full.csv three_vs_rest 0.8791 \
    --full 0.8991 --published 0.8995 \
    rebuild/pred_configA_all_seed1.csv rebuild/pred_configA_all_seed2.csv rebuild/pred_configA_all_seed3.csv

python -I how-we-built-it/code/make_nan_copy.py ./gb1_data_full.csv three_vs_rest rebuild/nan.csv
python -I how-we-built-it/code/fit_sealed.py rebuild/nan.csv rebuild --config A --tag NAN_
cmp rebuild/pred_NAN_configA_all_seed1.csv rebuild/pred_configA_all_seed1.csv
```

`nan.csv` has sha256 `c50240964016608e53869bee05e7c3071a6734cb52c6fdfae70adf5469464497`, every one of the 5,743
test scores replaced by the literal `nan`, and the final `cmp` is silent: the predictions do not change when
every test target is destroyed. `boot_mean.py --selftest ./gb1_data_full.csv three_vs_rest` runs the scorer's own
known positive (+1.000000) and known negative (-1.000000).

### 5. Rebuild without this code at all

The model is ordinary ridge regression. For each sequence build the one-hot indicators of the four varying site
residues (4 x 20), of every site pair (6 x 400, scaled by `s2`) and of every site triple (4 x 8,000, scaled by
`s3`), fit `sklearn.linear_model.Ridge(alpha=..., fit_intercept=True)` to `log(y + c)` on the fitting rows, and
predict the test rows.

| configuration | fit rows | s2 | s3 | alpha | c |
|---|---|---|---|---|---|
| A | the 2,990 rows whose `three_vs_rest` is `train` or `validation` | 0.5 | 0.25 | 0.03 | 0.001 |
| B | the 2,691 rows whose `three_vs_rest` is `train` | 1 | 1 | 0.001 | 0.01 |

`fit_intercept=True` matters: penalising the raw features and centring only the target instead gives 0.902973 and
0.897216, which are different numbers. The run's REPRODUCE panellist did exactly this rebuild and agreed with the
shipped predictions to 4.95e-9 (A) and 5.0e-10 (B).

The dual form in `how-we-built-it/code/gb1k.py` uses the identity

```
K(i,j) = m + s2^2 * C(m,2) + s3^2 * C(m,3),   m = #{of the four sites where i and j carry the same residue}
```

with the intercept implemented by double-centring the Gram matrix. That identity was checked exhaustively against
the explicit primal Gram over all 2990^2 and 2691^2 fitting pairs, maximum discrepancy 0.000e+00. Note also that
`C(m,4) = [m == 4]` is the identity matrix on distinct genotypes, so a fourth-order block would only shift
`alpha`: that direction is arithmetically empty.

### 6. Reproduce the shipped object itself

```sh
python -I how-we-built-it/code/build_package.py ./gb1_data_full.csv \
    rebuild/pred_configA_all_seed1.csv rebuild/pred_configB_trainonly_seed1.csv ./stage
```

It prints the sha256 of each object file and the submission-id, which must be
`2026-11-20-sapereaudeai-fa6abf5e`.

### 7. The bar

`the-record-we-beat/record.md` holds the URL, the UTC fetch time, the HTTP status, the page sha256 and the
extracted cell. Fetch it yourself with one plain request if you want to confirm the bar has not moved:

```sh
curl -sS -A "your-name-here" -w '%{http_code}\n' \
    -o plmfit_README.md https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md
sha256sum plmfit_README.md
grep -n "GB1 - three-vs-rest" plmfit_README.md
```
