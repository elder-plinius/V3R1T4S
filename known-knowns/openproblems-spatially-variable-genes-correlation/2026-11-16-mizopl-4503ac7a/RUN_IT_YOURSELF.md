# Run It Yourself

## 1. Full Blind-Panel & Certificate Verification

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output ends with:

```text
PASS
```

## 2. Adversarial Negative Control (`--corrupt`)

To verify that perturbing a certificate value exits with non-zero status (`1`) and prints `FAIL` on the final line:

```sh
sh verify-it-yourself/run_checks.sh --corrupt
```

## 3. Recomputing the Controlled Mechanistic Ablation (`p3`) & Depth-Paradox Stress Suite

```sh
python3 -B how-we-built-it/ablation_p3.py
python3 -B how-we-built-it/stress_test_depth_paradox.py
```
