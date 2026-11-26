# CRITERION skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
target: vnncomp-2026-unsolved-instance-counterexample
work window (UTC, from `date -u`): 2026-10-24T19:31:40Z to 2026-10-24T21:10:14Z
injection_suspected: none (no fetched page or program output addressed AI agents)

## What I compared against

- The success criterion quoted in `CLAIM.md` is a verbatim substring of `success_criterion` for this id in the pinned
  bank (`repo/bank/targets.json`, repo commit d14b0098c7dc3c372fa861a00175d3775aa097e7). I checked this by string
  containment (True).
- The pinned `TROPHY_CASE.md` and `known-knowns/` have no line containing `cnn7`, `challenging_certified` or `idx8072`.
  The two existing vnncomp-2026 rows are traffic_signs_recognition_2023 instances. Nothing subsumes this claim.

## Clause by clause

### Preamble: files unmodified at the version directory named by a results.csv, sha256 recorded

- Local hashes (sha256sum) match CLAIM.md: `inputs/onnx/cifar10_eps8_cnn7.onnx.gz`
  172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d (decompressed
  d424779ebd3b4a83bf8ebd26ca03f21b4f010a8b2825dd2995d1929c82ae4e59);
  `inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz`
  db437615a60f98e58989e7acfe165b3a6fc10d44ef5bc37ed4bdf3e568186fa5 (decompressed
  fb2928b748185d63e091943af317fbb33ecfed1b521773edddc9d96fdf0e41e5).
- `git hash-object` of the two .gz files: f084be840473d8ebc88ccaaba50bbf1c57001c05 and
  6b2f50fefbd4871361c7d17e80477ec0cd24879e. The GitHub contents API (HTTP 200, 2026-10-24T21:03:21Z to 21:03:23Z)
  gives exactly these blob ids, with sizes 65214983 and 34824, under
  `benchmarks/challenging_certified_training_2026/2.0/{onnx,vnnlib/cifar10_eps8_cnn7}`. It gives them both at
  ref 303f2327a8e8411efc4457da03d2016ce42733cf and at ref main. The benchmarks repo's main is 303f2327 (committed
  2026-07-07T10:57:07Z), so these are the live files. `inputs/instances_2.0.csv` blob
  f47cf61cc2cd0a544d92c4ad49d0dbaf377238d9 equals the live 2.0/instances.csv.
- Version directory: I fetched the results.csv of agate, vibecheck and act for this category at results commit
  eea564f5 (HTTP 200). All 120 benchmark paths in each name `challenging_certified_training_2026/2.0/`. I did not
  fetch n2v's results.csv, so CLAIM.md's mention of n2v is not verified by me (not needed: one tool suffices).
  cora, neuralsat, nnenum and super_simple_vnn_comp name 1.0.

### (a) live table and counterexample files: MET

- I fetched live results.txt once at 2026-10-24T21:02:15Z: HTTP 200, 7681226 bytes, sha256
  ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, identical to the claimant's 19:29:58Z fetch.
  Its git blob 5edd8632dc9b8e1e7013fd0bc1d22aa4ac46afe8 equals SCORING/results.txt in the live tree.
- My own parse gives 3618 `Row:` lines and 127 all-tool-unsolved (no `(h)`/`(v)` in any cell), 21 of them in
  2026_challenging_certified_training_2026. The target row (line 12985) is in that set:
  agate `-`, alpha_beta_crown `timeout`, n2v `timeout`, neuralsat `-`, nnv `timeout`, pyrat `timeout`,
  super_simple_vnn_comp `-`, vibecheck `timeout`.
- The raw results.csv rows also show no tool resolved it: agate unknown, vibecheck timeout, act unknown, cora unknown,
  neuralsat unknown, nnenum error_exit_code_1, super_simple_vnn_comp no_result_in_file.
- Results repo main is eea564f5d0a8751d8321a409214db14d03f452b8 (committed 2026-08-03T14:03:54Z). Its recursive tree
  (HTTP 200, 2026-10-24T21:02:43Z) is not truncated and has 27250 entries. Zero paths contain `idx8072_sample9`. So no
  counterexample or `.check.json` file exists for this instance in any tool directory. The clause holds vacuously:
  no such file exists, so none can say correct.

### (b) strict interior, every assertion, output margin >= 1e-6: MET

- The .vnnlib (VNN-LIB 2.0) has 6145 asserts: 3072 `>=` and 3072 `<=` input bounds, one per coordinate of
  X[0,c,h,w], plus one output `or` of 9 single-comparison disjuncts `(<= Y[0,3] Y[0,j])`, j != 3. There are no
  other assertions.
- The 3072 lines of `object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt` are each exactly a float32 value
  (Fraction of the decimal string equals Fraction of the float32: True). They are bit-identical to the `.npy` and to
  the X block of `object/cifar10_eps8_cnn7_idx8072_sample9_v2.counterexample`.
- Strict interior, exact rational comparison with zero tolerance: lo < x < hi for all 3072 coordinates (True).
  The minimum slack is 2.379202880859375e-07, at flat index 873. 2768 coordinates have slack < 1e-6, which means they
  sit 1 to 2 float32 ulps inside a bound. The criterion's 1e-6 requirement is on the output comparison of the
  satisfied branch, not on input slack, so this is allowed as written. The same strictness holds with the bounds cast
  to float32, which is what numpy 2 (NEP 50) does inside the validator's comparison (True).
- onnxruntime 1.26.0 CPUExecutionProvider, float32, arena off (the validator's options):
  Y[0,2] = 0.3705556392669678, Y[0,3] = 0.3676401972770691, so Y[0,3] <= Y[0,2] with margin
  0.0029154419898986816. That is about 2915 times the required 1e-6. The other eight disjuncts are all false
  (largest Yj - Y3 = -0.227678418, for j = 6). Only one output assertion exists, and its satisfied branch has a
  single atomic comparison. The v2 file's Y block equals this replay (max abs diff 0.0).
- Robustness to measured runtime differences: across ORT option sets (default/arena off, ORT_DISABLE_ALL,
  ORT_ENABLE_BASIC, ORT_ENABLE_ALL) the largest output spread is 6.0558319091796875e-05. The margin ranges from
  0.002897500991821289 (optimizations disabled/basic) to 0.0029154419898986816. The margin sits three orders of
  magnitude above 1e-6 and about 48 times above the observed spread.

### (c) float32 re-rounding, second runtime, official validator `correct`: MET

- The input is already exactly float32. Re-rounding the decimals through float64 to float32 changes no bits, so the
  float32 replay is the one above.
- Second runtimes, not onnxruntime. The conversion was onnx2torch, run under torch 2.9.0+cu128 (the criterion's
  wording is "onnx2pytorch/torch"; this is the torch branch). Results:
  torch CPU float32 Y2-Y3 = 0.002780228853225708; torch CPU float64 = 0.0029126814974439474;
  torch CUDA float32 (TF32 off) = 0.0029075145721435547; torch CUDA float64 = 0.0029126814974519966.
  In all four, argmax is 2 and every other disjunct is negative (max other about -0.2277).
- I also wrote my own float64 numpy forward pass of the 15-node graph (Conv, Relu, Flatten, Gemm,
  BatchNormalization), with no ORT and no torch: Y2-Y3 = 0.0029126814974743676, max other -0.22768652444944648.
  I did not run onnx.reference.ReferenceEvaluator; torch covers the clause.
- Official validator: `inputs/SCORING/counterexamples_v2.py` has git blob 82761145bb8097928b887235b0e238a2b6f25320.
  That equals SCORING/counterexamples_v2.py in the live results tree at eea564f5, as do cex_checks.py,
  benchmark_instances.py, settings.py and counterexamples.py. I imported it unmodified, on copies of the two
  hash-verified benchmark files laid out as `benchmarks/challenging_certified_training_2026/2.0/...`, with the
  results.csv network/property fields.
- I called `validate_vnnlib2_counterexample(..., abs_tol, 0.0, CounterexampleResult, True)` exactly as
  counterexamples.py's v2 worker dispatches it. Importing SCORING/settings.py fails its local benchmark-repo path
  assertion, so my driver copies COUNTEREXAMPLE_ATOL 1e-4 and RTOL 0.0 from settings.py lines 71-72. Versions:
  onnxruntime 1.26.0, onnx 1.21.0, numpy 2.2.6, vnnlib 1.0.2.
- Output: `abs_tol=0.0001 -> correct | ... all assertions hold with input_tolerance=0.0, output_tolerance=0.0` and
  `abs_tol=0.0 -> correct | ... all assertions hold with input_tolerance=0.0, output_tolerance=0.0`. That is
  `correct`, not `correct_up_to_tolerance`.

### (d) not soundnessbench_2026 or test: MET

- The category is 2026_challenging_certified_training_2026.

### (e) no previously published counterexample: MET as far as I searched (NOVELTY searches deeper)

- Two web searches (`"cifar10_eps8_cnn7_idx8072_sample9"`; `challenging_certified_training_2026 VNN-COMP
  cifar10_eps8_cnn7 counterexample`) returned nothing about this instance.
- The benchmark's own README names its source repo, kkaulen/vnncomp_challenging_certified_training at
  b4caf3d72d4f4442a640e1ef5aa1bce165815456 (tree HTTP 200, 2026-10-24T21:06:48Z). Its
  `verification_results/cifar10_eps8_cnn7.json` (HTTP 200, sha256
  cc59887d424fb623ce356beea655c01743b37eec606d6fcd4202b460807720e6) records idx 8072 as `"result": "timeout"`
  (abCROWN, 1004.6271016597748 s). It is one of 134 timeouts (6317 sat, 3549 unsat). So the benchmark authors
  published no counterexample for it either.
- The claim's wording ("strict", "zero tolerance", "no participating tool resolved", `correct`) does not go beyond
  the evidence above.

### Null model

- The centre of the input box is classified as label 3: argmax 3, best disjunct Y2-Y3 = -0.335584.
- 200 random points (100 uniform in the box, 100 near-corner): 0 of 200 satisfy any disjunct; the best
  max-disjunct margin is -0.15022385120391846.
- So the instance is not trivially violated; the witness is a genuine search result, not a default point.

### Scope

- One instance, one witness, no bundling. The full criterion is met.

criterion_met: full
confirmed_scope: The float32 input in object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt (sha256 38855485249d98be61182cb41f1c3d370a4e3208e0cf8efb2796feabc7f3cc29) lies strictly inside every input bound of the unmodified live VNN-COMP 2026 challenging_certified_training_2026 version-2.0 instance given by inputs/onnx/cifar10_eps8_cnn7.onnx.gz (git blob f084be840473d8ebc88ccaaba50bbf1c57001c05) + inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz (git blob 6b2f50fefbd4871361c7d17e80477ec0cd24879e) and satisfies its output disjunct Y[0,3] <= Y[0,2] with margin 0.0029154419898986816 under onnxruntime 1.26.0 CPU float32 (0.0027802 to 0.0029127 under torch CPU/CUDA float32/float64 and an independent numpy float64 pass), the unmodified inputs/SCORING/counterexamples_v2.py returns correct at abs_tol 0.0, and the live results.txt (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, fetched 2026-10-24T21:02:15Z) shows no tool resolving it, with no counterexample file for it in the results tree at eea564f5.

pass: true