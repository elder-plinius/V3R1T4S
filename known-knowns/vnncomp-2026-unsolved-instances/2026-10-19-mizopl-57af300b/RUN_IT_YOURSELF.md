# Run It Yourself (`vnncomp-2026-unsolved-instance-counterexample`)

## One-line check

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_vnncomp_cex.py` on `object/` and `the-record-we-beat/`, and then tests a corrupted copy of `object/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample` (with `X_0` set outside the input box) to confirm that any tampering is rejected. Expected last line: `ALL CHECKS PASS`.

## Direct Python verification

```sh
python3 verify-it-yourself/check_vnncomp_cex.py
```

Expected output:
```text
Verified tinyimagenet_eps1_wide_cnn7_idx7687_sample8 counterexample: strict_interior=True (min_lb=1.669e-06, min_ub=1.669e-06), prop #178 violated (Y[179]-Y[153] = +0.04230213 >= 1e-6)
PASS
```
(When `tinyimagenet_eps1_wide_cnn7.onnx` is present in the package directory or temp cache, `check_vnncomp_cex.py` also executes live `onnxruntime` CPU, `onnx.reference.ReferenceEvaluator`, and the official VNN-COMP 2026 v1.0 and v2.0 validators at `abs_tol=0.0, rel_tol=0.0`.)
