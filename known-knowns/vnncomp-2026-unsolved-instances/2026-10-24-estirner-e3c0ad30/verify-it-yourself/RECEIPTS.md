# Receipts (real output, copied from the runs on the claimant machine)

```
$ VNN_CACHE=<cache with the two benchmark files> VNN_PYTHON=<python 3.12, numpy 2.2.6, onnx 1.21.0, onnxruntime 1.26.0> sh verify-it-yourself/run_checks.sh
2026-10-24T21:02:06Z
cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz: sha256 OK
cifar10_eps8_cnn7.onnx.gz: sha256 OK
1. float32 exact: True
2. strictly inside every bound: True | smallest slack 2.386109619140625e-07
3. onnxruntime CPU: argmax 8; best disjunct (<= Y[0,7] Y[0,8]) margin 0.002304911613 -> True
3. onnx.reference: argmax 8; best disjunct (<= Y[0,7] Y[0,8]) margin 0.002346128225 -> True
PASS
```

```
$ VNN_CACHE=<same cache> python3 verify-it-yourself/official_validate.py
2026-10-24T21:02:07Z
SCORING/counterexamples_v2.py sha256 OK
SCORING/benchmark_instances.py sha256 OK
SCORING/cex_checks.py sha256 OK
bench/onnx/cifar10_eps8_cnn7.onnx.gz sha256 OK
bench/vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz sha256 OK
abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
```
