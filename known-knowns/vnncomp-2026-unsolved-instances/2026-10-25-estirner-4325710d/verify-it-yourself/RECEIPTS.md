# Receipts (real output, copied from the runs on the claimant machine)

`sh verify-it-yourself/run_checks.sh` (with VNN_CACHE holding the two benchmark files), started 2026-10-25T19:13:41Z:

```
model_64_idx_6371_eps_1.00000.vnnlib.gz: sha256 OK
3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz: sha256 OK
1. float32 exact: True
2. strictly inside every bound: True | smallest slack 0.001953125
3. onnxruntime CPU: argmax 9; best disjunct (>= Y[0,9] Y[0,17]) margin 0.9993293141 -> True
3. onnx.reference: argmax 9; best disjunct (>= Y[0,9] Y[0,17]) margin 0.9993293141 -> True
PASS
```

`python3 verify-it-yourself/official_validate.py`, started 2026-10-25T19:13:42Z:

```
SCORING/counterexamples_v2.py sha256 OK
SCORING/benchmark_instances.py sha256 OK
SCORING/cex_checks.py sha256 OK
bench/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz sha256 OK
bench/vnnlib/model_64_idx_6371_eps_1.00000.vnnlib.gz sha256 OK
abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
```
