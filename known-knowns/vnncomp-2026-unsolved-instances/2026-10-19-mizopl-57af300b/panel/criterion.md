# Panelist Review — CRITERION

panelist: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: vnncomp-2026-unsolved-instance-counterexample
verdict: pass
confirmed_scope: An explicit VNN-COMP 2026 counterexample claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample (276,643 bytes, sha256 57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da) and VNN-LIB 2.0 companion claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample (150,938 bytes, sha256 a34ed0220c3d97b9e18aee27b1e44614853877a3c95036bd2a1718326fd491e4) for the unsolved 2026_challenging_certified_training_2026 instance tinyimagenet_eps1_wide_cnn7_idx7687_sample8 (True Result '-' in SCORING/results.txt across all 8 participating tools), with all 12,288 coordinates strictly inside the float32 input box (minimum boundary clearance 1.66893005e-06 above 0), violating the VNN-LIB safety specification via Y_179 - Y_153 = +0.04230213 in onnxruntime CPU, +0.04230690 in onnx.reference.ReferenceEvaluator, +0.04228902 in PyTorch float32, and +0.04230902 in PyTorch float64 (all at least 1e-6), and returning 'correct' under the official VNN-COMP 2026 validators counterexamples.py and counterexamples_v2.py with abs_tol=0.0, rel_tol=0.0.

## 1. Clause-by-Clause Audit Against Verbatim Success Criterion and Verification Method

### Clause (1): Eligible Unsolved VNN-COMP 2026 Benchmark Instance
- **Requirement:** A `(category, onnx_model, vnnlib_property)` triple in `vnncomp2026_benchmarks` with `category` not in `{soundnessbench_2026, test}` for which `vnncomp2026_results/SCORING/results.txt` records no `sat` or `unsat` result from any participating tool.
- **Independent Verification:**
  - Category is `2026_challenging_certified_training_2026`, which is in `vnncomp2026_benchmarks` and excluded from `{soundnessbench_2026, test}`.
  - Network is `claim/tinyimagenet_eps1_wide_cnn7.onnx` (`141,147,418` bytes, `sha256: 7bc65dc63a7f8536ed80aa0755cdc1870d2041358190ec0e8cba544c3b5d00c6`), taking input tensor `input` of shape `(1, 3, 64, 64)` (`12,288` `float32` coordinates) and producing `output` of shape `(1, 200)`.
  - Property is `vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib`, provided in `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib.gz` (`149,155` bytes, `sha256: a0d735b14a2797b25abc8cf27e74450a791196ccce28dc31f1305847e30ad688`; uncompressed `1,195,158` bytes, `sha256: 1e626b4cb58eb1b691ce67e3d0932f8367719113461985b849f6b43030781b7b`) and VNN-LIB 2.0 companion `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.vnnlib.gz` (`120,566` bytes, `sha256: c4133f011d4d610af5916b6b95cb3120079eedc17e89d6f6174387e4d79d2567`; uncompressed `983,379` bytes, `sha256: a7a28ac63604a368c36f653968c217abb28a723d162fb0dd9e1399c42d415657`).
  - Inspecting `claim/results.txt` (`7,681,226` bytes, `sha256: ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f`) at instance index `58` confirms:
    - `Row: ['tinyimagenet_eps1_wide_cnn7-tinyimagenet_eps1_wide_cnn7_idx7687_sample8', '-', '-', 'timeout', 'timeout', 'error', 'error', '-', '-']`
    - `True Result: -`
    - Every one of the 8 participating tools (`agate`, `alpha_beta_crown`, `n2v`, `neuralsat`, `nnv`, `pyrat`, `super_simple_vnn_comp`, `vibecheck`) has `score: 0, is_ver: False, is_fals: False, is_fastest: False`.
- **Status:** Satisfied.

### Clause (2): Concrete Input Vector in VNN-COMP `.counterexample` Format
- **Requirement:** An explicit input tensor `x` in the VNN-COMP `.counterexample` format matching the ONNX input shape.
- **Independent Verification:**
  - `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample` (`276,643` bytes, `sha256: 57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da`; compressed `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.gz`, `81,752` bytes, `sha256: a5fc7a1a64ba7dc5b022bc68cf06a9d68de11e1312490bc25253ecb05355bc56`) contains `12,288` finite ordered input assignments `X_0 .. X_12287` and `200` finite ordered output assignments `Y_0 .. Y_199`.
  - `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample` (`150,938` bytes, `sha256: a34ed0220c3d97b9e18aee27b1e44614853877a3c95036bd2a1718326fd491e4`) provides the matching VNN-LIB 2.0 assignment.
- **Status:** Satisfied.

### Clause (3): Zero-Tolerance Strict Box Interior Membership in IEEE-754 `float32`
- **Requirement:** Satisfies every input box/polytope constraint of `vnnlib_property` with zero tolerance (`input_tolerance = 0.0`, strictly inside the interval `(lo, hi)` where possible).
- **Independent Verification:**
  - Parsing the VNN-LIB 1.0 property via `claim/vnnlib_v1.py` (`read_vnnlib_simple`) yields a single input box `[lb, ub]` over `12,288` coordinates.
  - In IEEE-754 `float32`, all `12,288 / 12,288` coordinates of `x` satisfy strict inequality above `lb_i` and below `ub_i`:
    - `strict_low = 12288 / 12288`, `strict_high = 12288 / 12288`, `boundary_coords = 0`.
    - Minimum lower-bound clearance `min_i (x_i - lb_i) = 1.66893005e-06` (strictly positive).
    - Minimum upper-bound clearance `min_i (ub_i - x_i) = 1.66893005e-06` (strictly positive).
- **Status:** Satisfied.

### Clause (4): Multi-Runtime Forward Pass Violation with Safety Margin at Least `1e-6`
- **Requirement:** When evaluated through `onnx_model` by `onnxruntime` (`CPUExecutionProvider`, `float32`) AND by an independent reference implementation (`onnx.reference.ReferenceEvaluator` and PyTorch layer-by-layer in `float32` and `float64`), produces output `y` violating the property specification with safety margin at least `1e-6`.
- **Independent Verification:**
  - The property encodes ground-truth class `y_true = 153` and is violated when any rival class `k != 153` satisfies `Y_k - Y_153` at least `0` (specifically disjunct `#178`, corresponding to rival class `y_adv = 179`).
  - Live execution of `claim/tinyimagenet_eps1_wide_cnn7.onnx` on `x` across four independent evaluators yields:
    1. `onnxruntime` (`CPUExecutionProvider`, `float32`): `Y[179] = +3.68928146`, `Y[153] = +3.64697933`, violation margin `Y[179] - Y[153] = +0.04230213` (`42,302x` the `1e-6` threshold).
    2. `onnx.reference.ReferenceEvaluator` (`float32`): `Y[179] = +3.68928385`, `Y[153] = +3.64697695`, violation margin `Y[179] - Y[153] = +0.04230690` (`max_j |y_ORT[j] - y_ref[j]| = 1.538e-05`).
    3. Independent PyTorch `float32` layer-by-layer forward pass: violation margin `+0.04228902` (`+0.04228830` under `F.batch_norm`), matching `y_pt32` in `claim/linear_region_certificate_idx7687_sample8.npz` (`625,910` bytes, `sha256: ddc8939722fa56f48e05d6f822bd5a0cfd2ac5221c8128c5b529bb320dca8df1`) to `0.0` under explicit batch-norm arithmetic (`max_j |y_ORT[j] - y_pt32[j]| = 3.290e-05`).
    4. Independent PyTorch `float64` (`double`) layer-by-layer forward pass: `Y[179] = +3.68928006`, `Y[153] = +3.64697104`, violation margin `Y[179] - Y[153] = +0.04230902` (`max_j |y_ORT[j] - y_pt64[j]| = 9.739e-06`).
  - **Linear-Region Stability Check:** Across all 6 ReLU layers (`1,638,912` total ReLU units; `661,326` active units), `0 / 1,638,912` pre-activations sit at `0` in `float64` (`min |pre-activation| = 1.590828e-08` overall and `1.377821e-06` in the penultimate 512-unit layer `/layers/layers.18/Relu`, where active units have `min |pre-activation| = 1.486183e-02`). The exact `float64` affine functional `(grad64_179 - grad64_153) . x + (eff_bias64_179 - eff_bias64_153)` stored in `claim/linear_region_certificate_idx7687_sample8.npz` matches independent PyTorch `float64` autograd to `4.163e-17` and reproduces `y_pt64[179] - y_pt64[153] = +0.0423090243727917` to within `1e-15`, with `L1` dual norm `||grad64_179 - grad64_153||_1 = 53.40244898` (giving an affine `L_inf` decision-boundary distance of `7.922675e-04`).
- **Status:** Satisfied.

### Clause (5): Official VNN-COMP 2026 Validators (`abs_tol=0.0, rel_tol=0.0`)
- **Requirement:** Run the official VNN-COMP 2026 validators `SCORING/counterexamples_v2.py` and `SCORING/counterexamples.py` with `atol = 0.0, rtol = 0.0` and confirm `result == 'correct'`.
- **Independent Verification:**
  - Running `claim/counterexamples.py` (`get_ce_diff(..., abs_tol=0.0, rel_tol=0.0)`) returns `'correct'` with message `CE input X was inside box #0; max input violation=0.0` and `prop #178 violated: [-0.04230213]`.
  - Running `claim/counterexamples_v2.py` (`validate_vnnlib2_counterexample(..., abs_tol=0.0, rel_tol=0.0, ignore_ce_outputs=True)`) returns `'correct'` with message `counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`.
  - `claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.check.json` (`1,147` bytes, `sha256: 4faa45fce4f398e43b7ad916f198258820ef2dae49d8a7413e93e35e17b8ee51`) records `"result": "correct"`, `"establishes_sat": true`, `"score_credit": true`, and `"witness_sha256": "57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da"`.
  - Running `claim/author_checker_vnncomp_cex.py` directly exits with code `0` and prints `PASS`.
- **Status:** Satisfied.

## 2. Null Model and Perturbation Controls

- **Nominal box center `x_0 = (lb + ub) / 2`:** Evaluated through `onnxruntime` (`CPUExecutionProvider`, `float32`), `x_0` is robustly classified as the ground-truth class `153` (`Y[153] = +4.22429895`), with highest rival logit `Y[94] = +3.50107884` (overall worst-case margin `-0.72322011`, and rival `179` margin `Y[179] - Y[153] = -0.87677526`, strictly safe).
- **Uniform random sampling in `[lb, ub]` (`N = 400`, seed `20261019`):** `0 / 400` uniform random points inside the `float32` input box violate the specification; the maximum violation margin observed across all `400` random draws and all `199` rival classes is `-0.71405411` (strictly negative).
- **Conclusion:** Random sampling and nominal midpoint evaluation sit more than `0.71` logit units away from violating the safety specification, confirming that the counterexample `x` (`margin = +0.04230213`) is a non-trivial adversarial witness that meets the full success criterion without hidden quantifiers or stretched definitions.

pass: true
