# Run It Yourself — `plmfit-trastuzumab-cdrh3-binding-mcc` (`2026-11-08-mizopl-465b77e7`)

## 1. Fast Standalone Verification (`< 1s`, Standard Python + NumPy)

From the package root, run:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/verify.py`, which checks:
1. All `SHA256SUMS` digests across `object/`.
2. `object/manifest_sha256.json` (`sha256: 96429fd22f9ecaedadc97e21506e19752e2f18e7a77216836ff535a347b27d6d`) and `object/certificate.json` (`sha256: 465b77e779fe37b92f9da4444bb53016a97449138ba4c28fb1d13a863e47908c`), including all `10 x 20` Empirical-Bayes `P_eb` and `M_prior` matrices, L1/Frobenius norms, simplex stacking weights, and `3 x 3` cross-seed dot-product matrices.
3. All `12` keyed prediction CSV part files (`object/seed_{42,43,44}_{trackB_cv_learned,trackA_canonical}_part{1,2}.csv`, `36,386` test rows per seed), verifying exact per-part `L1`, `L2`, `mean`, `std`, positive counts, and threshold consistency `pred_2body == (score_2body >= tau_cv)` and `pred_1body == (score_1body >= tau_cv_1b)`.

To run the negative control (adversarial corruption rejection):

```sh
python3 verify-it-yourself/verify.py --corrupt
```

## 2. Full End-to-End Retraining & Live Ground-Truth Recomputation (`< 90s` on Laptop CPU)

1. Download the official `LSSI-ETH/plmfit` `herH3` dataset (`17,149,024` bytes, `sha256: 5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`):

```sh
mkdir -p how-we-built-it/data
curl -sSL https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/data/herH3/herH3_data_full.csv -o how-we-built-it/data/herH3_data_full.csv
shasum -a 256 how-we-built-it/data/herH3_data_full.csv
```

2. Re-run `sh verify-it-yourself/run_checks.sh` (which automatically detects `how-we-built-it/data/herH3_data_full.csv`, verifies its SHA-256, and recomputes `MCC = 0.421004` directly against `binary_score`), or retrain both `Track A` and `Track B` from scratch on the `174` single-mutant rows across seeds `42, 43, 44`:

```sh
python3 how-we-built-it/bet11_dual_canonical_and_cv_learned_solver.py
```
