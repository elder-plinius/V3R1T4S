# Skeptic Panel Report — Role: REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: vnncomp-2026-unsolved-instance-counterexample

## 1. Mandate &Quoted Definition

Mandate:
> "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Quoted problem and success criterion from `claim/CLAIM.md`:
> "In the 7th International Verification of Neural Networks Competition (VNN-COMP 2026; benchmark freeze July 1 2026, scoring completed late July 2026 across 14 participating tools: alpha-beta-CROWN, NeuralSAT, PyRAT, CORA, NNV, nnenum, Marabou,SobolBox, VibeCheck, SuperSimpleVNNComp, FastBATLLNN, NeVer2, ROVER, act, agate, bright, n2v), an instance `(category, onnx_model, vnnlib_property)` is decided when at least one tool proves `unsat` (property holds) or produces a validated counterexample establishing `sat` (property violated, checked by `SCORING/counterexamples_v2.py` with `onnxruntime` CPU execution at `float32`). In `vnncomp2026_results/SCORING/results.txt`, any instance on which all participating tools returned `timeout`, `unknown`, or `error` (or whose submitted counterexample was rejected as `spec_not_violated` / `malformed_ce`) has no established ground truth. Excluding `soundnessbench_2026` (synthetic soundness-testing category) and `test`, find a certified counterexample input `x` (`float32` tensor matching the ONNX input shape) for at least one such unsolved VNN-COMP 2026 benchmark instance."
>
> "For a `(category, onnx_model, vnnlib_property)` triple in `vnncomp2026_benchmarks` (`category` not in `{soundnessbench_2026, test}`) for which `vnncomp2026_results/SCORING/results.txt` records no `sat` or `unsat` result from any participating tool: an explicit input tensor `x` (in the VNN-COMP `.counterexample` format) that (1) satisfies every input box/polytope constraint of `vnnlib_property` with zero tolerance (`input_tolerance = 0.0`, strictly inside the interval `lo < x_i < hi` where possible), and (2) when evaluated through `onnx_model` by `onnxruntime` (`CPUExecutionProvider`, `float32`) AND by an independent reference implementation (PyTorch / NumPy layer-by-layer or `onnx.reference.ReferenceEvaluator`), produces output `y` violating the property specification with safety margin at least `1e-6` (so `SCORING/counterexamples_v2.py` returns `'correct'`, not merely `'correct_up_to_tolerance'`)."

## 2. Independent Checker Written Before Reading Author Code

Before reading `claim/author_checker_vnncomp_cex.py`, I wrote a standalone verification script `indep_vnncomp_cex_check.py` directly from the mathematical definition of a VNN-LIB 1.0/2.0 SAT counterexample on an ONNX network:
1. Audited file existence, exact byte sizes, and SHA-256 digests of all saved files in `claim/` (both compressed `.gz` containers and uncompressed byte streams).
2. Verified directly against `claim/results.txt` that instance 58 (`tinyimagenet_eps1_wide_cnn7-tinyimagenet_eps1_wide_cnn7_idx7687_sample8`) in category `2026_challenging_certified_training_2026` has `True Result: -` (`Row: ['tinyimagenet_eps1_wide_cnn7-tinyimagenet_eps1_wide_cnn7_idx7687_sample8', '-', '-', 'timeout', 'timeout', 'error', 'error', '-', '-']`) and zero tools with `is_ver: True` or `is_fals: True`.
3. Independently parsed the VNN-LIB 1.0 property from `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib.gz` using regular expressions on stripped SMT-LIB assertions (`12,288` lower bounds, `12,288` upper bounds, and `199` output disjuncts comparing `Y_153` against `Y_c` for every rival class `c != 153`) and independently parsed `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample` (`12,288` input coordinates `X_0..X_12287` and `200` output coordinates `Y_0..Y_199`).
4. Checked strict interior input box membership (`lb_i < x_i < ub_i` with `0` boundary coordinates) in both IEEE-754 `float32` and `float64`.
5. Evaluated `claim/tinyimagenet_eps1_wide_cnn7.onnx` on `x` (`float32` tensor of shape `(1, 3, 64, 64)`) across four independent execution paths:
   - `onnxruntime.InferenceSession(..., providers=['CPUExecutionProvider'])` (`float32`),
   - `onnx.reference.ReferenceEvaluator` (`float32`),
   - an independent PyTorch `float32` layer-by-layer graph interpreter reconstructed directly from the ONNX initializers and nodes (`Constant`, `Sub`, `Div`, `Conv`, `BatchNormalization`, `Relu`, `Flatten`, `Gemm`),
   - an independent PyTorch `float64` (`double`) layer-by-layer graph interpreter reconstructed directly from the ONNX initializers and nodes.
6. Re-derived the exact local affine functional and input Jacobian `(w_179 - w_153)` at `x` in `float64` via PyTorch autograd and verified `claim/linear_region_certificate_idx7687_sample8.npz`.
7. Executed the unmodified official VNN-COMP 2026 validators `claim/counterexamples.py` (`get_ce_diff`) and `claim/counterexamples_v2.py` (`validate_vnnlib2_counterexample`) with `abs_tol=0.0, rel_tol=0.0`.
8. Tested three negative controls (box midpoint `0.5 * (lb + ub)`, single-coordinate upper-bound violation `x_0 = ub_0 + 1e-4`, and single-coordinate boundary clamping `x_0 = lb_0`) to confirm immediate rejection of non-counterexamples.

## 3. File Audit & SHA-256 Verification

| File in `claim/` | Size (bytes) | SHA-256 Digest | Uncompressed Size / SHA-256 |
|---|---:|---|---|
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample` | `276,643` | `57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da` | — |
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.gz` | `81,752` | `a5fc7a1a64ba7dc5b022bc68cf06a9d68de11e1312490bc25253ecb05355bc56` | `276,643` B / `57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da` |
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample` | `150,938` | `a34ed0220c3d97b9e18aee27b1e44614853877a3c95036bd2a1718326fd491e4` | — |
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.check.json` | `1,147` | `4faa45fce4f398e43b7ad916f198258820ef2dae49d8a7413e93e35e17b8ee51` | — |
| `claim/linear_region_certificate_idx7687_sample8.npz` | `625,910` | `ddc8939722fa56f48e05d6f822bd5a0cfd2ac5221c8128c5b529bb320dca8df1` | — |
| `claim/tinyimagenet_eps1_wide_cnn7.onnx` | `141,147,418` | `7bc65dc63a7f8536ed80aa0755cdc1870d2041358190ec0e8cba544c3b5d00c6` | — |
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib.gz` | `149,155` | `a0d735b14a2797b25abc8cf27e74450a791196ccce28dc31f1305847e30ad688` | `1,195,158` B / `1e626b4cb58eb1b691ce67e3d0932f8367719113461985b849f6b43030781b7b` |
| `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.vnnlib.gz` | `120,566` | `c4133f011d4d610af5916b6b95cb3120079eedc17e89d6f6174387e4d79d2567` | `983,379` B / `a7a28ac63604a368c36f653968c217abb28a723d162fb0dd9e1399c42d415657` |
| `claim/results.txt` | `7,681,226` | `ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f` | — |

## 4. Quantitative Verification & Determinism Results

Running `indep_vnncomp_cex_check.py` twice (`8.94s` and `7.82s`) produced identical bit-for-bit output across both runs (`diff` excluding timing line was empty):

- **Input box verification:**
  - `12,288 / 12,288` coordinates satisfy strict interior bounds `lb_i < x_i < ub_i` in IEEE-754 `float32` (`0` boundary coordinates).
  - Minimum lower-bound clearance in `float32`: `min_i(x_i - lb_i) = 1.668930e-06` (`1.668915e-06` in `float64`).
  - Minimum upper-bound clearance in `float32`: `min_i(ub_i - x_i) = 1.668930e-06` (`1.668466e-06` in `float64`).
- **Four-runtime forward-pass agreement:**
  - `max_j |y_ORT[j] - Y_file[j]| = 0.0e+00` (exact bit-for-bit match to `Y_0..Y_199` stored in `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample`).
  - `onnxruntime` (`CPUExecutionProvider`, `float32`): `Y_179 = 3.68928146`, `Y_153 = 3.64697933`, `margin = +0.04230213 >= 1e-6`, `argmax = 179`.
  - `onnx.reference.ReferenceEvaluator` (`float32`): `Y_179 = 3.68928385`, `Y_153 = 3.64697695`, `margin = +0.04230690 >= 1e-6`, `argmax = 179`, `max_j |y_ORT - y_ref| = 1.538e-05`.
  - Independent PyTorch `float32` layer-by-layer: `Y_179 = 3.68928003`, `Y_153 = 3.64699125`, `margin = +0.04228878 >= 1e-6` (`cert['y_pt32']` margin `+0.04228902`), `argmax = 179`, `max_j |y_ORT - y_pt32| = 3.290e-05`.
  - Independent PyTorch `float64` (`double`) layer-by-layer: `Y_179 = 3.689280060485644`, `Y_153 = 3.646971036112852`, `margin = +0.04230902437279171 >= 1e-6`, `argmax = 179`, `max_j |y_ORT - y_pt64| = 9.739e-06`.
- **Local affine certificate & independent Jacobian re-derivation:**
  - Certificate affine evaluation in `float64`: `w_179 . x + b_179 = 3.689280060485644` (`diff = 0.000e+00`), `w_153 . x + b_153 = 3.646971036112852` (`diff = 0.000e+00`), affine margin `(w_179 - w_153) . x + (b_179 - b_153) = +0.04230902437279038` (`diff = 1.332e-15` vs `margin_pt64`).
  - Independent `float64` PyTorch autograd Jacobian matches `(w_179 - w_153)` from `claim/linear_region_certificate_idx7687_sample8.npz` to `max_i |grad_i - (w_179 - w_153)_i| = 4.337e-17`.
- **Official VNN-COMP 2026 validators (`abs_tol=0.0, rel_tol=0.0`):**
  - `claim/counterexamples.py` (`get_ce_diff` on VNN-LIB 1.0): returned `'correct'` (`CE input X was inside box #0; max input violation=0.0; prop #178 violated: [-0.04230213]`).
  - `claim/counterexamples_v2.py` (`validate_vnnlib2_counterexample` on VNN-LIB 2.0): returned `'correct'` (`counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`).
- **Negative controls:**
  - Control A (box midpoint `0.5 * (lb + ub)`): rejected (`spec_not_violated`, `Y_179 - Y_153 = -0.876775 < 0`, `max_{c != 153}(Y_c - Y_153) = -0.723220 < 0`).
  - Control B (`x_0 = ub_0 + 1e-4`): rejected (`input_bounds_violated`, `min_ub_clear = -1.000166e-04 < 0`).
  - Control C (`x_0 = lb_0`): rejected by strict interior check (`strict_interior = False`).
- **Author checker comparison (`claim/author_checker_vnncomp_cex.py`):**
  - Executed after completing the independent checker; exited with code `0` and output:
    `Live ONNX + ReferenceEvaluator + Official VNN-COMP 2026 v1.0/v2.0 Validators: ALL PASSED (margin=+0.04230213)`
    `Verified tinyimagenet_eps1_wide_cnn7_idx7687_sample8 counterexample: strict_interior=True (min_lb=1.669e-06, min_ub=1.669e-06), prop #178 violated (Y[179]-Y[153] = +0.04230213 >= 1e-6)`
    `PASS`

pass: true
