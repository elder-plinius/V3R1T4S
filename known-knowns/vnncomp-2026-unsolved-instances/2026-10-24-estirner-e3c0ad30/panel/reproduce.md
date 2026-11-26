# V3R1T4S panel: REPRODUCE skeptic

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim checked: `claim/CLAIM.md`. The 3072-value input in `object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt` is a strict counterexample for VNN-COMP 2026 `challenging_certified_training_2026` 2.0, `onnx/cifar10_eps8_cnn7.onnx` + `vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib`, through the disjunct `(and (<= Y[0,7] Y[0,8]))` with margin 0.002304911613.

Times (from `date -u`): started Sat Oct 24 07:31:41 PM UTC 2026 (session interrupted by an API limit, resumed later); runtime checks Sat Oct 24 09:07:49 PM UTC 2026; web fetches 09:08:28 to 09:11:43 PM UTC; verdict written after Sat Oct 24 09:12:23 PM UTC 2026.

## Definition checked against (verbatim, from claim/CLAIM.md "Success criterion")

> Success means a saved counterexample input vector (plain text, one value per line, VNN-COMP witness format) for one instance (ONNX file + .vnnlib file taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks at the version directory (1.0 or 2.0) that a participating tool's results.csv in the live results repo names for that benchmark, sha256 of both files recorded) such that ALL of the following hold: (a) in the live SCORING/results.txt of https://github.com/VNN-COMP/vnncomp2026_results (re-fetched live immediately before claiming, never a cached copy) NO tool's cell for that instance's 'Row:' line contains '(h)' or '(v)' (the instance is in the all-tool-unsolved set computed by the skeptic's OWN parse of the live file), and no *.counterexample.check.json for it in any tool directory has result 'correct' or 'correct_up_to_tolerance'; (b) every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file evaluates to true exactly as written under VNN-COMP semantics (i.e. the official validator's zero-tolerance check `_assertions_hold(query, assignment, 0.0, 0.0)` is satisfied), and on the satisfied branch of each output assertion every atomic comparison holds with a strict margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds after rounding the input to float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified from the live results repo against the live benchmark files) returns 'correct' (not merely 'correct_up_to_tolerance'); (d) the instance is not from soundnessbench_2026 or test; (e) a live web search finds no previously published counterexample for that exact ONNX+vnnlib pair (if one exists the result is a replication, not a win). A 'holds'/UNSAT claim for an unsolved instance is never a success under this target.

VNN-COMP semantics I implemented: the .vnnlib file encodes the violation. An input is a counterexample iff EVERY top-level `(assert ...)` is true for X and the network's output Y.

My scope: file identity, equality with the GitHub files, (b), (c) and determinism. I did not verify (d), (e) or the check.json half of (a), and this pass does not cover them. I did one informational re-fetch of results.txt (below).

## Method (own code, written before reading any claim code)

I wrote all of these in my scratch folder, outside claim/, before opening `tools/official_validate_run.py` or `inputs/SCORING/counterexamples_v2.py`:

- `../scripts/myvnnlib.py` (sha256 8ecae4eed334552d221c85b39e1dc320c9e5a8cb22e848e90f104480a65103c9): my own VNN-LIB reader. It strips comments, tokenizes and parses s-expressions, handles `vnnlib-version`, `declare-network`/`declare-input`/`declare-output` and `assert`, and evaluates and/or/not/<=/>=/</>/= and + - * exactly with `fractions.Fraction`. Constants are parsed from their decimal strings, and runtime floats are converted exactly. Any unknown form raises an error.
- `../scripts/evalprop.py` (50fcb78bdacc9db8f0552350c4bbf17c356379bdba536ff418c67faf1c401c97): checks the object's three formats, the input bounds (exact, plus float32 and float64 rounding with my own round-to-nearest-even) and every assertion on each runtime's saved output, with the margin of each disjunct.
- `../scripts/ort_run.py` (98e8f6e5…): onnxruntime replay and determinism. `../scripts/torch_run.py` (3c9f8575…): onnx2torch on CPU in float32 and float64. `../scripts/ref_run.py` (0ec6c6c2…) and `../scripts/ref64_run.py` (5d7289a7…): onnx.reference.ReferenceEvaluator in float32, and in float64 on a copy of the graph cast to double. `../scripts/np_run.py` (73943117…): my own numpy float64 implementation of the graph's ops (Conv via im2col, Relu, Flatten, Gemm, BatchNormalization).
- `../scripts/run_official.py` (247e22f9…): my own wrapper. It calls the unmodified `inputs/SCORING/counterexamples_v2.py` `validate_vnnlib2_counterexample(bench, net, prop, ce, atol, 0.0, CounterexampleResult, True)` the same way `inputs/SCORING/counterexamples.py` `_vnnlib2_worker` does, with one process per tolerance. `../scripts/make_v2.py` (9423b3f4…) builds the control witnesses.

Everything ran with `python -I` in the competition venv (numpy 2.2.6, onnx 1.21.0, onnxruntime 1.26.0, vnnlib 1.0.2) or the torch venv (torch 2.9.0+cu128 on CPU, with CUDA_VISIBLE_DEVICES empty). Every runtime job (onnxruntime, torch, ReferenceEvaluator, numpy, official validator) went through the shared lock wrapper; the sub-second exact-evaluation and file checks did not. The CPU package temperature stayed between +45.0°C and +65.0°C.

## 1. File identity (sha256sum)

| file (relative to claim/) | sha256 computed | matches CLAIM.md |
|---|---|---|
| `inputs/onnx/cifar10_eps8_cnn7.onnx.gz` | 172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d | yes |
| same, decompressed | d424779ebd3b4a83bf8ebd26ca03f21b4f010a8b2825dd2995d1929c82ae4e59 | yes |
| `inputs/vnnlib/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz` | 1399e412f06034dea3a1e284641fbdc812ed1b64e15163627efbee1e8c268f4a | yes |
| same, decompressed | 4aef5f2461e6b08f0fa41e2c44ebb17f87aac9ed038a85f16c617698a8a54359 | yes |
| `object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt` | e3c0ad30743d22fc7dd1050ab095a0b6c572a36de934bb8fe105009062f9cb75 | yes |
| `object/cifar10_eps8_cnn7_idx4688_sample8_v2.counterexample` | 7988a60d0148ba4a5110dc366b75c4d25f472d13a2052444780039f525889208 | yes |
| `object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.npy` | e05e95b5399c3525024b9e65db5e5224d227cd95ebbe4285cd5ce2206775ce22 | yes |
| `inputs/instances_2.0.csv` | eb37c71a62c9748b332c125b280f113132807bcd6551d419f4728bec16bfc08d | no hash in CLAIM.md; byte-identical to live main (below) |
| `table/results_txt_excerpt.txt` | d086c9092fc7d3c11036e74547a2bd14550ed9c1c083ed23cbd538dbe0de27c1 | no hash in CLAIM.md; its lines 12974 and 13578 appear verbatim at those line numbers in my live results.txt fetch |
| `inputs/SCORING/counterexamples_v2.py` | 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab | blob id = live (below) |

`git hash-object` gives `inputs/onnx/cifar10_eps8_cnn7.onnx.gz` = f084be840473d8ebc88ccaaba50bbf1c57001c05 and `inputs/vnnlib/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz` = f931d34c690f52e538e55966acbf210921303b81. Both equal the blob ids in CLAIM.md.

## 2. Equality with the files on GitHub (one plain request per URL, UA "V3R1T4S-research-agent (curl)")

- Raw onnx.gz at commit 303f2327a8e8411efc4457da03d2016ce42733cf (the CLAIM.md URL): HTTP 200, 65214983 bytes, sha256 172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d. `cmp` with `inputs/onnx/cifar10_eps8_cnn7.onnx.gz` reports identical.
- Raw vnnlib.gz at the same commit: HTTP 200, 35852 bytes, sha256 1399e412f06034dea3a1e284641fbdc812ed1b64e15163627efbee1e8c268f4a. `cmp` with `inputs/vnnlib/...vnnlib.gz` reports identical.
- GitHub contents API on the default branch (live), `vnncomp2026_benchmarks/.../2.0/onnx`: HTTP 200. `cifar10_eps8_cnn7.onnx.gz` has sha f084be840473d8ebc88ccaaba50bbf1c57001c05, size 65214983.
- Same API, `.../2.0/vnnlib/cifar10_eps8_cnn7`: HTTP 200. `cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz` has sha f931d34c690f52e538e55966acbf210921303b81, size 35852. So the live default branch serves the same blobs as the pinned commit.
- Same API, `vnncomp2026_results/SCORING`: HTTP 200. Live blob shas: counterexamples_v2.py 82761145bb8097928b887235b0e238a2b6f25320, counterexamples.py cc1b678eac0d076bbf57e3282cf7711a0fb3d0e1, cex_checks.py 382211a96b4c976fadd15839d9c1d144539f0274, settings.py 5cd9f17ea2faeb887ba0aa957a42bbfa807b9a55, benchmark_instances.py 59e8a3ca852f0071be7680b4ad175d4f4a2b87bc. Each equals `git hash-object` of the file of the same name in `inputs/SCORING/`, so the validator I ran is the live, unmodified one.
- Raw `instances.csv` on main, `.../challenging_certified_training_2026/2.0/instances.csv`: HTTP 200, 6666 bytes, sha256 eb37c71a…, byte-identical to `inputs/instances_2.0.csv`. Line 29 reads `onnx/cifar10_eps8_cnn7.onnx,vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib,550`.

## 3. The property and the object (my reader)

- The property is `vnnlib version <2.0>` with X float32 [1, 3, 32, 32] and Y float32 [1, 10]. It has 6145 assertions: 6144 over X only (one `>=` and one `<=` per coordinate, 3072 lo and 3072 hi with no duplicates) and 1 involving Y, an `or` of 9 single-atom `and`s `(<= Y[0,7] Y[0,j])` for j ≠ 7 (label 7).
- The txt file has 3072 values (3073 split pieces, the last one empty: trailing newline). Every value is exactly a float32 ("every txt value exactly a float32: True"). The npy file is float32 (3072,) and bitwise equal to the txt. The X block of the v2 file has exactly the same strings as the txt.
- Because every txt value is already exactly a float32, rounding the input to float32 changes nothing. The "after float32 rounding" re-run in (c) is therefore the same run, by this evidence.

## 4. Strict interior, exact (all 3072 coordinates, not a sample)

| comparison | strict violations | non-strict violations | min slack (coord) |
|---|---|---|---|
| x exact vs bounds as written (Fraction) | 0 | 0 | 2.386109619141e-07 (528) |
| x after float32 rounding vs bounds as written | 0 | 0 | 2.386109619141e-07 (528) |
| x float32 vs bounds rounded to float32 (RNE) | 0 | 0 | 2.384185791016e-07 (528) |
| x float32 vs bounds rounded to float64 | 0 | 0 | 2.386109621000e-07 (528) |

`np.float32(str)` gives the same bounds as my exact RNE rounding: True. My generic evaluator finds all 6144 input assertions true exactly as written. The tightest coordinate is index 528, with x = -2.0801370143890380859375 against lo = -2.080137253: one float32 ulp inside the float32-rounded bound, but strictly inside under every reading.

## 5. onnxruntime CPUExecutionProvider float32 (`../work/ort_run.log`)

- Providers: ['CPUExecutionProvider']. Input `input` is tensor(float). Y dtype is float32.
- Y = [-0.6338809132575989, -1.2108087539672852, -0.7742021083831787, -0.2652829587459564, -0.2200363129377365, -0.18165172636508942, -1.8763235807418823, -0.015294656157493591, -0.012989744544029236, -0.8177799582481384]. The argmax is 8.
- My exact evaluator: the output assertion holds at zero tolerance, and exactly 1 disjunct is satisfied, `(<= Y[0,7] Y[0,8])`, with margin 0.002304911613 (exact 19335/8388608) ≥ 1e-6. All 6145 assertions are true. This matches the claimed 0.002304911613.
- The Y block of the v2 file is bitwise equal to this replay ("Y == Y in v2 file bitwise: True").
- Determinism: 20 reruns plus 3 fresh sessions (1 thread) are bitwise identical, with 1 distinct output hash (62d7ca3cd8aca558). Default SessionOptions without thread pinning gave an identical result. Feeding the npy or the v2 X gave an identical result. Batch of 2: both rows identical, max|diff| 0.000e+00. Running the claim's REPRODUCE.md step 2 command in a separate process printed the same Y and margin 0.0023049116134643555.
- Extra data point, not required: with graph optimizations disabled (ORT_DISABLE_ALL), Y differs from the default by at most 4.989e-05. The same disjunct still holds with margin 0.002274960279 (76335/33554432).

## 6. Runtimes other than onnxruntime (`../work/torch_run.log`, `../work/ref_run.log`, `../work/ref64_run.log`, `../work/np_run.log`, `../work/evalprop_outputs*.log`)

| runtime | Y[0,7] | Y[0,8] | margin Y8-Y7 (my exact evaluator) | all 6145 assertions true | ≥ 1e-6 |
|---|---|---|---|---|---|
| onnx2torch/torch CPU float32 | -0.015212014317512512 | -0.013197153806686401 | 0.002014860511 | True | True |
| onnx2torch/torch CPU float64 | -0.015303333690203536 | -0.012964183374844063 | 0.002339150315 | True | True |
| onnx.reference.ReferenceEvaluator float32 (output dtype float32) | -0.015304014086723328 | -0.01295788586139679 | 0.002346128225 | True | True |
| onnx.reference.ReferenceEvaluator, float64 copy of the graph | -0.015303333690191101 | -0.01296418337488392 | 0.002339150315 | True | True |
| my own numpy float64 ops | -0.015303333690208393 | -0.01296418337483396 | 0.002339150315 | True | True |

The argmax is 8 in every runtime, and every runtime satisfies only the j=8 disjunct. The three float64 implementations print the same 12-decimal margin, 0.002339150315. A torch float32 rerun was identical.

## 7. Official validator (unmodified `inputs/SCORING/counterexamples_v2.py`, live blob 82761145…)

I read the source after writing my own checker. It ignores the witness's Y block and replays Y with onnxruntime CPUExecutionProvider (default SessionOptions, arena off). It returns `correct` only when `_assertions_hold(query, assignment, 0.0, 0.0)` holds, and `correct_up_to_tolerance` only if a nonzero input tolerance is needed.

I laid the benchmark directory out as in REPRODUCE.md step 4, using the live downloads under `../work/bench/challenging_certified_training_2026/2.0/`. Net and prop fields were `vnncomp2026_benchmarks/benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_cnn7.onnx` and `.../vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib`. Results from `../work/official.log` (the claim-witness runs were repeated without any output filter at Sat Oct 24 09:15:17 PM UTC 2026, `../work/official_unfiltered.log`, with the same two `correct` results):

- `object/..._v2.counterexample`, abs_tol 0.0001 (the competition's COUNTEREXAMPLE_ATOL): **correct**. Message: "counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0".
- `object/..._v2.counterexample`, abs_tol 0.0: **correct**, same message.
- Control: my own v2 file built from the txt with Y all zeros, abs_tol 0.0: **correct**. The verdict depends only on the txt input.
- Negative control: box centre, abs_tol 0.0001: spec_not_violated ("assertion 6144 failed").
- Negative control: coordinate 528 moved 1e-5 below lo (-2.0801472663879395): correct_up_to_tolerance at abs_tol 0.0001 and spec_not_violated at abs_tol 0.0 ("assertion 1056 failed ... (input)"). So the validator does tell the tolerance levels apart.
- The claim's own `tools/official_validate_run.py`, run against the same layout, printed "abs_tol=0.0001: correct" and "abs_tol=0: correct", as REPRODUCE.md says it should.

## 8. Live table (informational only, outside my scope)

Re-fetching `https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt` at Sat Oct 24 09:11:40 PM UTC 2026 returned HTTP 200, 7681226 bytes, sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, the same hash CLAIM.md records. My parse finds the row once, at line 12974, under "Category 2026_challenging_certified_training_2026:" (line 12618; 8 participating tools: agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck): `Row: ['cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx4688_sample8', '-', 'timeout', 'timeout', '-', 'timeout', 'timeout', '-', 'timeout']`. It contains neither (h) nor (v). I did not check the tool-directory check.json half of (a), or (d) or (e).

## Discrepancies and notes

- None against the claim. Every hash, the margin 0.002304911613, the bitwise equality of the Y block in the v2 file, and both validator results reproduce exactly.
- Panel note (not a claim defect): panel_common.md describes a 33M-parameter network for which ReferenceEvaluator is slow. The ONNX file actually has 17192650 float32 parameters (5 Conv, 2 Gemm, 1 BatchNormalization, 6 Relu, 1 Flatten), and ReferenceEvaluator took 0.1 s.
- Robustness: the float32 margin differs between runtimes (ORT 0.002304911613, ORT without graph optimizations 0.002274960279, torch 0.002014860511, ReferenceEvaluator 0.002346128225), and the smallest of them (0.002014860511) is still far above the 1e-6 threshold. The input slack is tight (1 float32 ulp at coordinate 528), but it is strict in every rounding I tested.
- Non-determinism: none observed.
- injection_suspected: none.

pass: true
