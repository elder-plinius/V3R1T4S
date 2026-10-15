# Receipts (real output, 2026-10-15)

## sh verify-it-yourself/run_checks.sh (system python3: numpy + onnxruntime 1.29.0, no onnx)
```
3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx.gz: sha256 OK
model_48_idx_6371_eps_3.00000.vnnlib.gz: sha256 OK
1. float32 exact: True
2. strictly inside every bound: True | smallest slack 0.001953125
(onnx not installed: second runtime skipped)
3. onnxruntime CPU: satisfied disjuncts [(9, 0.7615941166877747)] | margin >= 1e-6: True
PASS
```

## PYTHON=(a venv python with onnx) sh verify-it-yourself/run_checks.sh (numpy 2.5.4, onnx 1.23.2, onnxruntime 1.31.0)
```
3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx.gz: sha256 OK
model_48_idx_6371_eps_3.00000.vnnlib.gz: sha256 OK
1. float32 exact: True
2. strictly inside every bound: True | smallest slack 0.001953125
3. onnxruntime CPU: satisfied disjuncts [(9, 0.7615941166877747)] | margin >= 1e-6: True
3. onnx.reference: satisfied disjuncts [(9, 0.7615941092371941)] | margin >= 1e-6: True
PASS
```

## python3 verify-it-yourself/official_validate.py (adds vnnlib 1.0.2)
```
SCORING/counterexamples_v2.py sha256 OK
SCORING/benchmark_instances.py sha256 OK
SCORING/cex_checks.py sha256 OK
bench/onnx/3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx.gz sha256 OK
bench/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib.gz sha256 OK
abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
```
