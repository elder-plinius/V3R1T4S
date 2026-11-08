# RECEIPTS: real output of verify-it-yourself/run_checks.sh

Run from this folder on 2026-11-08 with Python 3.12, numpy 2.2.6 and onnxruntime 1.26.0 on the CPU (two threads; PYTHON
set to that interpreter). Output, unedited.

Default (NREF = 256), 10:16:55Z to 10:17:50Z (date -u):

```
1. object hashes: ok (2 files)
2. ONNX signature: ok (spins [batch, 100] float32 -> log_abs_psi [batch], phase [batch])
3. reference table (100 rows): max |d log|psi|| 7.63e-06, max |d phase| 9.32e-10 rad
4. symmetries: ok (translations, spin flip, C4v with B1 characters; worst deviation 6.6e-06)
5. local energies of 256 saved configurations: mean diff 2.85e-05, max |diff| 7.18e-04, mean E_loc -253.802293 (recorded -253.802322)
PASS
```

All saved configurations (NREF = 2048), 10:17:50Z to 10:25:03Z:

```
1. object hashes: ok (2 files)
2. ONNX signature: ok (spins [batch, 100] float32 -> log_abs_psi [batch], phase [batch])
3. reference table (100 rows): max |d log|psi|| 7.63e-06, max |d phase| 9.32e-10 rad
4. symmetries: ok (translations, spin flip, C4v with B1 characters; worst deviation 6.6e-06)
5. local energies of 2048 saved configurations: mean diff 1.04e-05, max |diff| 1.02e-03, mean E_loc -253.803492 (recorded -253.803502)
PASS
```

The recorded local energies come from the measurement code on the GPU during measurement S2 (network in float32, sum
over the 16 images in float64); the ONNX file sums the images in float32, as in training, and runs on the CPU. The
differences are that float32 rounding.
