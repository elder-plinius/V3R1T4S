# Current wrapper receipt (2026-10-15)

Real end-to-end run on Linux x86_64, Python 3.12.14, NumPy 2.3.5.
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; exit code **0**.
Release inputs and checker sources were fetched from upstream commit
`371938deefd77b9e6a95d2a0c3e2d3c6ead7eaac` and verified against its Git blob IDs.
These are actual scientific checker outputs, not synthetic fixture output.

ONNX Runtime 1.23.2, CPUExecutionProvider, float32. Both witnesses and all six negative controls ran. The pinned benchmark commit is `303f2327a8e8411efc4457da03d2016ce42733cf`; compressed and decompressed model/property hashes appear below. Optional `onnx.reference` and `OFFICIAL=1` validation were not run.

Command (from this family directory, with the stated Python environment):

```sh
PYTHON=/path/to/qualification/venv/bin/python OFFICIAL=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 sh verify-it-yourself/run_checks.sh
```

Exact source and output SHA-256:

- `run_checks.sh`: `af8f2df03faa3218e20c123f35045591122fe2737d55ef41b126b798d32f2987`
- `known-knowns/check_harness_contract.py`: `f0f43ba4ab6970001f228affb5a95f9ec5d37b115f8487c7ce4cc11ce9e5a070`
- Raw combined stdout/stderr below: `0aea4c3540e47ca0e7ef96ce0ae080f4fc97d1a6dd51a86b51265b4243561347`

## Complete current output

```text
== sha256 of the witnesses against INDEX.csv
witnesses/model_30_idx_1703_eps_1/witness_plain.txt: matches INDEX.csv
witnesses/model_30_idx_1703_eps_1/witness_v2.txt: matches INDEX.csv
witnesses/model_30_idx_178_eps_1/witness_plain.txt: matches INDEX.csv
witnesses/model_30_idx_178_eps_1/witness_v2.txt: matches INDEX.csv
== standalone checker
benchmark repository VNN-COMP/vnncomp2026_benchmarks at commit 303f2327a8e8411efc4457da03d2016ce42733cf
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz
  onnx.gz sha256 baeca5c8bcf58a9b8bf8a22cf59fffd2fc5e2baac0fd1e5be467dbb716f78a83 (pinned)
  onnx    sha256 9fb711d9b0019889d648df23ce477a083f0f6d6ef13f732de284a607f0abdce6 (pinned)
== instance 3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30 + model_30_idx_1703_eps_1.00000
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz
  vnnlib.gz sha256 5e4318e8e9320325f0d03f110439f1febe8b34a407bafd4e737359cb958f590a (pinned)
  vnnlib    sha256 cdd6b802863e0f0d7f958e2474743cb7a8706ce75478e8d721462b1a212551d5 (pinned)
  property: 5400 input assertions, 1 output assertion(s); all 2700 coordinates bounded above and below: True
  witness sha256 80f4b5a8284931dd0f970d61f1289db47b62a46856edbcb9f19c76334c5580f8; every value exactly representable in float32: True
  input box, exact rationals, strict: True; smallest distance to a bound = 1/1024 = 0.0009765625
  onnxruntime 1.23.2 CPU float32: output assertion holds at zero tolerance: True; margin 0.99990918; argmax 22
  (onnx not installed: second runtime skipped)
  witness_v2.txt X block equals witness_plain.txt exactly: True
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 margin=0.99990918 min_input_slack=0.0009765625 witness=witnesses/model_30_idx_1703_eps_1/witness_plain.txt
== instance 3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30 + model_30_idx_178_eps_1.00000
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_178_eps_1.00000.vnnlib.gz
  vnnlib.gz sha256 3b690c291a9f43f4a47ad1987d92abc301c9075fa7567418a1599fe142c3b20e (pinned)
  vnnlib    sha256 746adabaff524f20fd49e6dd246a3346cbf1a9f32d55c80346d6b76ecf094571 (pinned)
  property: 5400 input assertions, 1 output assertion(s); all 2700 coordinates bounded above and below: True
  witness sha256 83c8b41e31f7f44ada880ffd67de003e06891d9b3994a18a49154af36f35ac98; every value exactly representable in float32: True
  input box, exact rationals, strict: True; smallest distance to a bound = 1/1024 = 0.0009765625
  onnxruntime 1.23.2 CPU float32: output assertion holds at zero tolerance: True; margin 0.96402755; argmax 15
  (onnx not installed: second runtime skipped)
  witness_v2.txt X block equals witness_plain.txt exactly: True
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_178_eps_1.00000 margin=0.96402755 min_input_slack=0.0009765625 witness=witnesses/model_30_idx_178_eps_1/witness_plain.txt
== negative controls (each must FAIL)
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_1703 on_bound: expected semantic rejection
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_1703 outside: expected semantic rejection
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_1703 centre: expected semantic rejection
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_178 on_bound: expected semantic rejection
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_178 outside: expected semantic rejection
HARNESS CONTROL PASS vnn: expected semantic rejection
control idx_178 centre: expected semantic rejection
ALL CHECKS PASSED
```

---

## Historical receipts

The records below are preserved from earlier runs of the former wrapper. Their
wrapper messages do not describe the current run; use the complete current
output above for the current wrapper contract. Historical comparison dates and
optional-runtime coverage remain those stated in the original records.

# Check results (VNN-COMP 2026 counterexamples)

`PYTHON=<python3.12 with numpy 2.5.3, onnx 1.23.2, onnxruntime 1.31.0, vnnlib 1.0.2> OFFICIAL=1 sh verify-it-yourself/run_checks.sh`
was run on the shipped files from 2026-10-12T03:40:24Z to 03:40:35Z on the build machine (macOS). Exit code 0, last
line `ALL CHECKS PASSED`. The benchmark files were downloaded at that time from the pinned commit and matched the
pinned sha256.

| instance | strictly inside (exact) | min slack | float32-exact | onnxruntime margin | onnx.reference margin | ORT − ref | official validator (1e-4 / 0) | verdict |
|---|---|---|---|---|---|---|---|---|
| `model_30_idx_1703_eps_1.00000` | yes, 5400/5400 | 2^-10 | yes | 0.99990918 (argmax 22, true 25) | 0.99990918 | 0.0 | correct / correct | PASS |
| `model_30_idx_178_eps_1.00000` | yes, 5400/5400 | 2^-10 | yes | 0.96402755 (argmax 15, true 13) | 0.96402755 | 0.0 | correct / correct | PASS |

Negative controls (`mutate.py`): for both instances, a pixel moved onto its bound and a pixel moved 2^-10 outside
each fail the strict input check, and the unperturbed image (box centre) fails the output assertion under both runtimes;
all six are reported `VNNCHECK FAIL`.

Earlier independent checks (not shipped): the finder's own checker, a second checker written from the problem
statement before the search, and the checkers of three independent reviewers (own VNN-LIB parsers, exact-rational
input checks, onnxruntime, onnx.reference and a NumPy forward pass of the binarized network), plus the unmodified
official validator; all gave the same margins and `correct`.

## Raw output

```
== sha256 of the witnesses against INDEX.csv
witnesses/model_30_idx_1703_eps_1/witness_plain.txt: matches INDEX.csv
witnesses/model_30_idx_1703_eps_1/witness_v2.txt: matches INDEX.csv
witnesses/model_30_idx_178_eps_1/witness_plain.txt: matches INDEX.csv
witnesses/model_30_idx_178_eps_1/witness_v2.txt: matches INDEX.csv
== standalone checker
benchmark repository VNN-COMP/vnncomp2026_benchmarks at commit 303f2327a8e8411efc4457da03d2016ce42733cf
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz
  onnx.gz sha256 baeca5c8bcf58a9b8bf8a22cf59fffd2fc5e2baac0fd1e5be467dbb716f78a83 (pinned)
  onnx    sha256 9fb711d9b0019889d648df23ce477a083f0f6d6ef13f732de284a607f0abdce6 (pinned)
== instance 3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30 + model_30_idx_1703_eps_1.00000
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz
  vnnlib.gz sha256 5e4318e8e9320325f0d03f110439f1febe8b34a407bafd4e737359cb958f590a (pinned)
  vnnlib    sha256 cdd6b802863e0f0d7f958e2474743cb7a8706ce75478e8d721462b1a212551d5 (pinned)
  property: 5400 input assertions, 1 output assertion(s); all 2700 coordinates bounded above and below: True
  witness sha256 80f4b5a8284931dd0f970d61f1289db47b62a46856edbcb9f19c76334c5580f8; every value exactly representable in float32: True
  input box, exact rationals, strict: True; smallest distance to a bound = 1/1024 = 0.0009765625
  onnxruntime 1.31.0 CPU float32: output assertion holds at zero tolerance: True; margin 0.99990918; argmax 22
  onnx.reference 1.23.2: output assertion holds at zero tolerance: True; margin 0.99990918; argmax 22
  max |onnxruntime - onnx.reference| = 0.0
  witness_v2.txt X block equals witness_plain.txt exactly: True
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 margin=0.99990918 min_input_slack=0.0009765625 witness=witnesses/model_30_idx_1703_eps_1/witness_plain.txt
== instance 3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30 + model_30_idx_178_eps_1.00000
  GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_178_eps_1.00000.vnnlib.gz
  vnnlib.gz sha256 3b690c291a9f43f4a47ad1987d92abc301c9075fa7567418a1599fe142c3b20e (pinned)
  vnnlib    sha256 746adabaff524f20fd49e6dd246a3346cbf1a9f32d55c80346d6b76ecf094571 (pinned)
  property: 5400 input assertions, 1 output assertion(s); all 2700 coordinates bounded above and below: True
  witness sha256 83c8b41e31f7f44ada880ffd67de003e06891d9b3994a18a49154af36f35ac98; every value exactly representable in float32: True
  input box, exact rationals, strict: True; smallest distance to a bound = 1/1024 = 0.0009765625
  onnxruntime 1.31.0 CPU float32: output assertion holds at zero tolerance: True; margin 0.96402755; argmax 15
  onnx.reference 1.23.2: output assertion holds at zero tolerance: True; margin 0.96402755; argmax 15
  max |onnxruntime - onnx.reference| = 0.0
  witness_v2.txt X block equals witness_plain.txt exactly: True
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_178_eps_1.00000 margin=0.96402755 min_input_slack=0.0009765625 witness=witnesses/model_30_idx_178_eps_1/witness_plain.txt
== negative controls (each must FAIL)
control idx_1703 on_bound: 1 failed check(s), VNNCHECK FAIL (expected)
control idx_1703 outside: 1 failed check(s), VNNCHECK FAIL (expected)
control idx_1703 centre: 2 failed check(s), VNNCHECK FAIL (expected)
control idx_178 on_bound: 1 failed check(s), VNNCHECK FAIL (expected)
control idx_178 outside: 1 failed check(s), VNNCHECK FAIL (expected)
control idx_178 centre: 2 failed check(s), VNNCHECK FAIL (expected)
== official validator (SCORING/counterexamples_v2.py, unmodified)
GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING/counterexamples_v2.py
SCORING/counterexamples_v2.py sha256 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab (pinned)
GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING/benchmark_instances.py
SCORING/benchmark_instances.py sha256 5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229 (pinned)
GET https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING/cex_checks.py
SCORING/cex_checks.py sha256 695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5 (pinned)
3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_178_eps_1.00000 abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_178_eps_1.00000 abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
OFFICIAL VALIDATOR: both correct
ALL CHECKS PASSED
```
