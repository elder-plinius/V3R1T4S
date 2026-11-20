# Reproduce this claim in a fresh shell

Everything needed is inside this folder. Python 3 with `numpy`, `scipy` and `scikit-learn`. On the machine this
was run on the interpreter is a project virtual environment; below it is written `python` (the original line
named that interpreter by its absolute local path, which was redacted for publication - it is the only edit made
to this file for the package, and it changes no command and no number).
Run every command from this folder. `-I` is used so nothing is imported from the data directory.

## 0. The input file

```
sha256sum data/gb1_data_full.csv
# 93588112a14fe5ad1789fbfd16d63549c3d24f2d9a68ae96967c801a23a529de
```

That is `data/gb1/gb1_data_full.csv` from the plmfit repository, used unchanged. The sequences are the full
265-residue 5LDE chain A construct; nothing was trimmed, padded or re-derived.

## 1. Check the scorer on a known positive and a known negative

```
python -I code/boot_mean.py --selftest data/gb1_data_full.csv three_vs_rest
```

Expected (and saved in `result/score_selftest.out`): `rho = 1.000000` when the prediction is the target,
`rho = -1.000000` when it is minus the target, `SELFTEST: PASS`, over 5,743 test rows.

## 2. Refit both sealed configurations

```
mkdir -p rebuild
python -I code/fit_sealed.py data/gb1_data_full.csv rebuild --config A
python -I code/fit_sealed.py data/gb1_data_full.csv rebuild --config B
```

Expected: `2691 train / 299 validation / 5743 test`; 2,990 fitting rows for A and 2,691 for B; and

```
pred_configA_all_seed{1,2,3}.csv        sha256 30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2
pred_configB_trainonly_seed{1,2,3}.csv  sha256 e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490
```

identical to the six files in `result/`. The three seeds give the same bytes by design; the program prints
`DETERMINISM CHECK: 1 distinct prediction-file sha256 over 3 seeds`. The configurations are literals in
`code/fit_sealed.py` (`SEALED`), copied from `UNSCORED-PREDICTION-as-sealed.md` and from the two `WOULD SELECT:`
lines of `the-earlier-runs/extrap_select.out`.

## 3. Score them

```
python -I code/boot_mean.py data/gb1_data_full.csv three_vs_rest 0.8791 --full 0.8991 --published 0.8995 \
  result/pred_configA_all_seed1.csv result/pred_configA_all_seed2.csv result/pred_configA_all_seed3.csv
python -I code/boot_mean.py data/gb1_data_full.csv three_vs_rest 0.8791 --full 0.8991 --published 0.8995 \
  result/pred_configB_trainonly_seed1.csv result/pred_configB_trainonly_seed2.csv result/pred_configB_trainonly_seed3.csv
```

Expected, and saved verbatim in `result/scores.out`:

| | per-seed Spearman | mean | sd | mean's bootstrap 95% interval |
|---|---|---|---|---|
| A | 0.902852, 0.902852, 0.902852 | 0.902852 | 0.000000 | [0.898044, 0.907247] |
| B | 0.897451, 0.897451, 0.897451 | 0.897451 | 0.000000 | [0.892649, 0.901823] |

The bootstrap is 10,000 resamples of the 5,743 test sequences with `numpy.random.default_rng(0)`; each resample is
scored under all three seeds' predictions and the three Spearmans averaged, so the interval is the interval **of
the mean**. Per-seed intervals are printed for information and gate nothing.

## 4. Re-run the leakage test yourself

```
python -I code/make_nan_copy.py data/gb1_data_full.csv three_vs_rest rebuild/nan.csv
python -I code/fit_sealed.py rebuild/nan.csv rebuild --config A --tag NAN_
python -I code/fit_sealed.py rebuild/nan.csv rebuild --config B --tag NAN_
cmp rebuild/pred_NAN_configA_all_seed1.csv result/pred_configA_all_seed1.csv
cmp rebuild/pred_NAN_configB_trainonly_seed1.csv result/pred_configB_trainonly_seed1.csv
```

Expected: `nan.csv` has sha256 `c50240964016608e53869bee05e7c3071a6734cb52c6fdfae70adf5469464497`, all 5,743
test scores replaced, and every `cmp` silent. Saved output: `result/leak_test.out`.

## 5. Independent check without this code at all

The model is ordinary ridge regression. Build, for each sequence, the one-hot indicator features of the four site
residues (4 x 20), of every pair of sites (6 x 400, scaled by `s2`) and of every triple (4 x 8,000, scaled by
`s3`), fit `sklearn.linear_model.Ridge(alpha=..., fit_intercept=True)` to `log(y + c)` on the fitting rows, and
predict the test rows. For A use `s2=0.5, s3=0.25, alpha=0.03, c=0.001` on the 2,990 `train`+`validation` rows;
for B use `s2=1, s3=1, alpha=0.001, c=0.01` on the 2,691 `train` rows. That primal fit and the dual kernel form
in `code/gb1k.py` agree to about 2e-14; the identity used is

```
K(i,j) = m + s2^2 * C(m,2) + s3^2 * C(m,3),   m = #{sites where i and j carry the same residue}
```

with the intercept implemented by double-centring the Gram matrix. Note that `C(m,4) = [m == 4]` is the identity
matrix on distinct genotypes, so a fourth-order block would only shift `alpha`.

## 6. The bar

`status/plmfit_README_2026-11-20-0535_preclaim.md`, sha256
`51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`, fetched 2026-11-20T05:42:28Z, HTTP 200, from
`https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md`. Line 209:
`| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |`.
