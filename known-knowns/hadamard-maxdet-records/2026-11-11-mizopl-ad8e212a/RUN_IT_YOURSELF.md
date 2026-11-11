# Run It Yourself

## 1. Full Verification (`Bareiss` + `14-Prime CRT` + Optional `SymPy` + Core Reconstruction)

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output ends with:

```text
PASS
```

## 2. Adversarial Negative Control (`--corrupt`)

To verify that a single sign flip in an `object/` matrix is rejected with non-zero exit status and `FAIL`:

```sh
python3 verify-it-yourself/verify.py --corrupt
```

## 3. Standalone Algebraic Reconstruction from `generator_params`

To rebuild all 8 matrices directly from the 4-block circulant Goethals-Seidel generators (`vA, vB, vC, vD`) and switched Hadamard cores stored in `object/hadamard_maxdet_8_records.json`:

```sh
python3 how-we-built-it/reconstruct_all_8_records.py
```
