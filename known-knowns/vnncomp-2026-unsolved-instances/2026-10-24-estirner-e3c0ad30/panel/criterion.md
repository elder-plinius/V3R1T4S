# CRITERION skeptic verdict: vnncomp-2026-unsolved-instance-counterexample, challenging_certified_training_2026 (2.0), cifar10_eps8_cnn7 + cifar10_eps8_cnn7_idx4688_sample8

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Read: claim/ (CLAIM.md, REPRODUCE.md, inputs/, object/, table/, tools/), the pinned public repo copy (bank/targets.json,
TROPHY_CASE.md, known-knowns/ by grep), and the live web pages listed below, one request per URL. I read no other
skeptic's file. Checks ran 2026-10-24T21:01:25Z to 2026-10-24T21:10:37Z (`date -u`). Heavy jobs went through the shared
lock wrapper; the CPU package peaked at +68.0°C.

## The criterion text

The success criterion quoted in CLAIM.md is string-equal (`==` True, 2101 vs 2101 characters) to `success_criterion` of id `vnncomp-2026-unsolved-instance-counterexample`
in the pinned bank/targets.json (repo HEAD d14b0098c7dc3c372fa861a00175d3775aa097e7). I checked the full criterion, not a partial win (p1 and p2 are not needed).

## File identity (sha256 recorded, unmodified, right version directory)

- `sha256sum`: inputs/onnx/cifar10_eps8_cnn7.onnx.gz = 172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d,
  decompressed d424779ebd3b4a83bf8ebd26ca03f21b4f010a8b2825dd2995d1929c82ae4e59;
  inputs/vnnlib/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz = 1399e412f06034dea3a1e284641fbdc812ed1b64e15163627efbee1e8c268f4a,
  decompressed 4aef5f2461e6b08f0fa41e2c44ebb17f87aac9ed038a85f16c617698a8a54359. All four match CLAIM.md.
- `git hash-object` of the two .gz files: f084be840473d8ebc88ccaaba50bbf1c57001c05 and f931d34c690f52e538e55966acbf210921303b81.
- Live benchmarks repo: `commits/main` (HTTP 200, 2026-10-24T21:01:53Z) is 303f2327a8e8411efc4457da03d2016ce42733cf
  (committed 2026-07-07T10:57:07Z), so the commit named in CLAIM.md is the live head. Contents API at that commit (HTTP 200
  ×4, 2026-10-24T21:02:57Z): `benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_cnn7.onnx.gz` has blob f084be840473d8ebc88ccaaba50bbf1c57001c05,
  size 65214983, and `.../2.0/vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz` has blob f931d34c690f52e538e55966acbf210921303b81, size 35852.
  Both equal the local blob ids (git blob identity is a SHA-1 content hash of the exact bytes). I also re-fetched the vnnlib.gz raw from main
  (HTTP 200, 35852 bytes, 2026-10-24T21:07:33Z): sha256 1399e412f06034dea3a1e284641fbdc812ed1b64e15163627efbee1e8c268f4a.
- Version directory: I fetched all 11 `<tool>/2026_challenging_certified_training_2026/results.csv` from live results main (HTTP 200 each,
  2026-10-24T21:02:40Z). agate, n2v and vibecheck name `2.0` (120 path hits each), and these three are among the 8 scored
  "participating tools" in results.txt. act also names 2.0 but is not scored here. alpha_beta_crown, cora, neuralsat, nnenum, nnv, pyrat and super_simple_vnn_comp name `1.0`.
  For context, I checked that the 1.0 vnnlib (blob a2edf56101109a305a7242cebd6c18a2f710fd49, HTTP 200, 42733 bytes) encodes identical decimal strings for all 6144
  bounds and an identical 9-way disjunction. The 1.0 onnx.gz has a different blob (67619436566c63f95d228470c284d2a13d41fe34, same size 65214983). I did not compare its contents, and the claim does not rely on it.

## (a) live table, unsolved by every tool, no validated counterexample on file: HOLDS

- Live https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt, fetched once at
  2026-10-24T21:01:48Z: HTTP 200, 7681226 bytes, sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (equal to CLAIM.md).
  Live results main: eea564f5d0a8751d8321a409214db14d03f452b8 (committed 2026-08-03T14:03:54Z).
- My own parse: 3618 `Row:` lines, 127 with no `(h)`/`(v)` in any cell (21 of them in 2026_challenging_certified_training_2026).
  The instance has exactly one Row line, line 12974, in category 2026_challenging_certified_training_2026 (8 participating tools: agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck):
  `['cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx4688_sample8', '-', 'timeout', 'timeout', '-', 'timeout', 'timeout', '-', 'timeout']`, "True Result: -".
  The summary CSV line (13578) agrees. The instance is in the all-tool-unsolved set.
- The 11 results.csv rows for this instance give: act unknown, agate unknown, alpha_beta_crown timeout, cora unknown, n2v run_instance_timeout,
  neuralsat unknown, nnenum error_exit_code_1, nnv timeout, pyrat timeout, super_simple_vnn_comp no_result_in_file, vibecheck timeout. None is sat or unsat.
- Results tree at eea564f5 (`git/trees/...?recursive=1`, HTTP 200, 2026-10-24T21:02:21Z, truncated False, 27250 entries) has 0 paths containing
  `idx4688_sample8`, so the check.json clause is met because no such file exists. The only eps8_cnn7 (non-wide) check.json files in the category
  are for idx8090_sample7 (e.g. `vibecheck/2026_challenging_certified_training_2026/cifar10_eps8_cnn7_cifar10_eps8_cnn7_idx8090_sample7.counterexample.check.json`).

## (b) strict interior, every assertion at zero tolerance, margin >= 1e-6: HOLDS

- Object identity: object/...counterexample.txt has 3072 values, and every line is the exact decimal of a float32 (`float32(x)==x` for all: True).
  Its strings equal the 3072 X strings of object/..._v2.counterexample (True) and equal object/...counterexample.npy (float32, (3072,)) bitwise (True).
  sha256: txt e3c0ad30743d22fc7dd1050ab095a0b6c572a36de934bb8fe105009062f9cb75, v2 7988a60d0148ba4a5110dc366b75c4d25f472d13a2052444780039f525889208,
  npy e05e95b5399c3525024b9e65db5e5224d227cd95ebbe4285cd5ce2206775ce22.
- The .vnnlib has 6145 asserts: 3072 `>=` and 3072 `<=` bounds on X, one per coordinate, and nothing else references X. The 6145th is one output assertion,
  `(or (and (<= Y[0,7] Y[0,j])) ...)` for j != 7 (label 7).
- Exact check with `fractions.Fraction` of the decimal strings: coordinates not strictly inside = 0. Minimum x-lo = 2.386110e-07 (k=528),
  minimum hi-x = 2.386556e-07 (k=2206), coordinates within 1 float32 ulp of a bound = 0, and coordinates outside the float32-rounded bounds = 0.
  This check is needed because under numpy 2.2.6 `np.float32(0.1) == 0.1` is True: the validator's input comparison is done in
  float32, so its "correct" alone would not prove exact strictness.
- onnxruntime 1.26.0 CPUExecutionProvider, float32, default optimization (ENABLE_ALL): argmax 8. The disjunct Y[7] <= Y[8] holds with
  Y[8]-Y[7] = 0.002304911613, which is >= 1e-6. The other 8 disjuncts are false (closest Y[5]-Y[7] = -0.166357070208), so only one branch is satisfied.
- Robustness against runtime differences I measured: ORT DISABLE_ALL/BASIC/EXTENDED give Y8-Y7 = 0.002274960279 (max |dY| vs default 4.989e-05),
  ENABLE_ALL gives 0.002304911613, and 1 vs 2 intra-op threads change nothing. Ratio margin / largest ORT-internal difference = 46.2 (computed by command).

## (c) float32 rounding, a second runtime, official validator `correct`: HOLDS

- float32 rounding: the input is already float32-exact, so rounding is the identity (True) and the re-run is the ORT result above.
- Second runtime, onnx2torch on torch 2.9.0+cu128 run on CPU (CUDA hidden), graph ops Conv/BatchNormalization/Relu/Flatten/Gemm:
  float32 argmax 8, Y8-Y7 = 0.002014860511, Y[7]<=Y[8] True, max|Y-Y_ort| = 3.392e-04; float64 argmax 8, Y8-Y7 = 0.002339150315,
  max|Y-Y_ort| = 3.106e-05. Ratio torch-f32 margin / largest cross-runtime difference = 5.94; ORT margin / that difference = 6.80 (computed by command). I did not run onnx.reference.ReferenceEvaluator;
  the criterion's "or" is met by torch.
- Official validator: the live SCORING/counterexamples_v2.py (HTTP 200, 2026-10-24T21:01:53Z) has sha256 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab,
  equal to inputs/SCORING/. Its imports are also live and equal: benchmark_instances.py 5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229,
  cex_checks.py 695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5, and settings.py dbd190e5cd127a1e1ef8caa19d6416cf6c0d2e94e7698b9b22e96d43661d2039.
  settings.py is not imported because it asserts a local benchmark clone; I used its lines 71-72, ATOL 1e-4 and RTOL 0.0.
  My own driver calls `validate_vnnlib2_counterexample(Path(bench), net, prop, ce, atol, 0.0, CounterexampleResult, True)` the way
  SCORING/counterexamples.py does, with the network/property fields copied from vibecheck's results.csv. The resolved files were
  `challenging_certified_training_2026/2.0/onnx/cifar10_eps8_cnn7.onnx.gz` and `.../2.0/vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz`
  (the live-fetched vnnlib, and an onnx with the live blob id). Result on object/cifar10_eps8_cnn7_idx4688_sample8_v2.counterexample:
  `abs_tol=0.0001: correct` and `abs_tol=0: correct | counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`.
- Validator controls (my own witnesses): the box center, carrying the claimed Y lines, gives `spec_not_violated` at both tolerances, so witness outputs are ignored and replayed.
  The claimed witness with coordinate 528 moved 5e-5 below its lower bound gives `correct_up_to_tolerance` at 1e-4 and `spec_not_violated` at 0.
  The validator does discriminate.

## (d) not soundnessbench_2026 or test: HOLDS. The category is 2026_challenging_certified_training_2026.

## (e) no previously published counterexample: HOLDS as far as a live search can establish

- WebSearch "\"cifar10_eps8_cnn7_idx4688_sample8\"": no result mentions it. WebSearch "\"cifar10_eps8_cnn7\" counterexample VNN-COMP 2026":
  nothing on this instance. WebSearch "challenging_certified_training_2026 VNN-COMP benchmark counterexample idx4688": nothing on this instance.
- GitHub `search/issues?q=cifar10_eps8_cnn7+org:VNN-COMP` (HTTP 200, 2026-10-24T21:09:29Z): total_count 1, VNN-COMP/vnncomp2026 issue #4
  "[BENCHMARK] Challenging Certified Training" (open, 0 comments; HTTP 200 ×2, 2026-10-24T21:09:41Z). Its 4593 characters contain no "4688" and no "counterexample".
- In the live results repo, no tool has a counterexample file for this instance (see (a)). In the pinned repo, TROPHY_CASE.md and known-knowns/ have no line for
  idx4688 or cifar10_eps8_cnn7. The earlier vnncomp-2026 trophies are traffic_signs_recognition_2023 instances, a different pair, so this win is not subsumed.
- Wording: the claim sentence does not assert novelty beyond "no participating tool resolved", which (a) supports.

## Null model

- Box center: argmax 7, max_{j!=7} Yj - Y7 = -0.736128, and Y8-Y7 = -2.676960 at the center.
- 100 uniform-random points in the box: 0 violating, best max_{j!=7} Yj - Y7 = -0.557533.
- 100 random box corners: 0 violating, best -0.292560.
- So the property is not violated trivially. The witness is a non-trivial search result: L_inf distance from center 0.157334, with a fraction 0.8584 of coordinates at >= 95% of the half-width.

## Scope and wording

- One instance, one witness, no bundling. The claim sentence matches every measured number: margin 0.002304911613, disjunct `(and (<= Y[0,7] Y[0,8]))`, validator `correct`.
- The claim says nothing about the instance's other disjuncts, about other instances, or about the 1.0 network, and neither does my scope.
- Note for readers: the margin is small in absolute terms (0.002304911613 between Y[0,8] = -0.012989744544029236 and Y[0,7] = -0.015294656157493591 under ORT). It is 2304.9 times the 1e-6 threshold, and 6.80 times the largest runtime difference I measured
  (torch f32 vs ORT, 3.392e-04); the torch-f32 margin itself is 5.94 times that difference (ratios computed by command).

criterion_met: full
confirmed_scope: The 3072 float32 values in object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt (identical to the X block of object/cifar10_eps8_cnn7_idx4688_sample8_v2.counterexample) lie strictly inside every input bound of inputs/vnnlib/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz and, run through inputs/onnx/cifar10_eps8_cnn7.onnx.gz (both blob-identical, same git SHA-1 blob id, to challenging_certified_training_2026/2.0 at vnncomp2026_benchmarks commit 303f2327), satisfy its output disjunct Y[0,7] <= Y[0,8] with margin 0.002304911613 under onnxruntime 1.26.0 CPU float32, 0.002014860511 under onnx2torch/torch CPU float32 and 0.002339150315 in float64, are rated `correct` at abs_tol 0 by the unmodified live SCORING/counterexamples_v2.py, and that instance's Row line in the live SCORING/results.txt (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f) has no (h) or (v) in any of its 8 tool cells.
pass: true
