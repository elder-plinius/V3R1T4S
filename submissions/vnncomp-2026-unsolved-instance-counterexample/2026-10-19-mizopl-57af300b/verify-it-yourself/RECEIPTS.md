# Verification Receipts (`vnncomp-2026-unsolved-instance-counterexample`)

## 1. Execution Receipt (`verify-it-yourself/run_checks.sh`)

```text
=== [1/2] Verifying VNN-COMP 2026 counterexample tinyimagenet_eps1_wide_cnn7_idx7687_sample8 ===
Verified tinyimagenet_eps1_wide_cnn7_idx7687_sample8 counterexample: strict_interior=True (min_lb=1.669e-06, min_ub=1.669e-06), prop #178 violated (Y[179]-Y[153] = +0.04230213 >= 1e-6)
PASS
=== [2/2] Negative control: corrupting X_0 to 1.0 (must fail strict interior box check) ===
Negative control rejected as expected.
ALL CHECKS PASS
```

## 2. Four-Runtime & Official VNN-COMP 2026 Validator Receipt

When evaluated with `tinyimagenet_eps1_wide_cnn7.onnx` (`141,147,418` bytes, `sha256: 7bc65dc63a7f8536ed80aa0755cdc1870d2041358190ec0e8cba544c3b5d00c6`):
- **Strict interior input box check (`float32`):** `12,288 / 12,288` coordinates satisfy `lb_i < x_i < ub_i` (`min_lb = 1.668930e-06`, `min_ub = 1.668930e-06`, `0` boundary coordinates).
- **`onnxruntime` (`CPUExecutionProvider`, `float32`):** `Y[179] = +3.68928146`, `Y[153] = +3.64697933`, `margin = +0.04230213 >= 1e-6`.
- **`onnx.reference.ReferenceEvaluator` (`float32`):** `Y[179] = +3.68928385`, `Y[153] = +3.64697695`, `margin = +0.04230690 >= 1e-6`.
- **Independent PyTorch `float32` layer-by-layer:** `margin = +0.04228902 >= 1e-6`.
- **Independent PyTorch `float64` (`double`) layer-by-layer:** `Y[179] = +3.68928006`, `Y[153] = +3.64697104`, `margin = +0.04230902 >= 1e-6`.
- **Official VNN-COMP 2026 v1.0 validator (`verify-it-yourself/counterexamples.py`, `abs_tol=0.0, rel_tol=0.0`):** `'correct'`.
- **Official VNN-COMP 2026 v2.0 validator (`verify-it-yourself/counterexamples_v2.py`, `abs_tol=0.0, rel_tol=0.0`):** `'correct'`.
- **Official `verify-it-yourself/cex_checks.py` (`object/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.check.json`):** `"result": "correct"`, `"establishes_sat": true`, `"score_credit": true`.
