# Receipts (real output, copied from the runs on the claimant machine)

```
$ VNN_CACHE=<cache with the two benchmark files> PYTHON=<python 3.12, numpy 2.2.6, onnx 1.21.0, onnxruntime 1.26.0> sh verify-it-yourself/run_checks.sh
2026-10-24T17:05:28Z
cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz: sha256 OK
cifar10_eps8_wide_cnn7.onnx.gz: sha256 OK
1. float32 exact: True
2. strictly inside every bound: True | smallest slack 2.379244384765625e-07
3. onnxruntime CPU: argmax 2; best disjunct (<= Y[0,5] Y[0,2]) margin 0.01176285744 -> True
3. onnx.reference: argmax 2; best disjunct (<= Y[0,5] Y[0,2]) margin 0.0117572248 -> True
PASS
```

```
$ VNN_CACHE=<same cache> python3 verify-it-yourself/official_validate.py
2026-10-24T17:09:01Z
SCORING/counterexamples_v2.py sha256 OK
SCORING/benchmark_instances.py sha256 OK
SCORING/cex_checks.py sha256 OK
bench/onnx/cifar10_eps8_wide_cnn7.onnx.gz sha256 OK
bench/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz sha256 OK
abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
```
