# REPRODUCE skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

verdict time (date -u): 2026-10-25T18:53:56Z
claim: `object/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000.counterexample.txt`
is a strict counterexample for traffic_signs_recognition_2023 (2.0), `onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx` + `vnnlib/model_64_idx_6371_eps_1.00000.vnnlib`.

Result: everything I checked reproduces. The margin I measured, Y[0,9] - Y[0,17] under onnxruntime CPU float32, is
0.9993293141305912 (exactly 34336693777/34359738368). The claim gives 0.9993293141. The official validator returns
`correct` (not `correct_up_to_tolerance`) on 3 of 3 runs.

## What I checked (definition quoted from CLAIM.md's success criterion)

- (b) "every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the
  ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file
  evaluates to true exactly as written under VNN-COMP semantics (...) and on the satisfied branch of each output
  assertion every atomic comparison holds with a strict margin >= 1e-6"
- (c) "the same holds after rounding the input to float32 and re-running, AND in a second runtime that is not
  onnxruntime (onnx2pytorch/torch or onnx.reference.ReferenceEvaluator), AND the competition's own
  SCORING/counterexamples_v2.py (run unmodified from the live results repo against the live benchmark files) returns
  'correct' (not merely 'correct_up_to_tolerance')"
- plus file identities ("ONNX file + .vnnlib file taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks
  at the version directory ... sha256 of both files recorded").

I wrote my own checker before reading REPRODUCE.md, `tools/official_validate_run.py` or the SCORING code. It has its
own s-expression VNN-LIB parser, exact rational (fractions.Fraction) comparisons against the decimal bound strings,
generic evaluation of all 24577 assertions, and its own numpy evaluation of the graph. I did not use the author's tool.
I called the official validator through my own driver.

## File identity

- All 16 files in claim/ match the panel-start sha256 manifest (diff empty).
- `inputs/vnnlib/model_64_idx_6371_eps_1.00000.vnnlib.gz`: sha256 16efc2694a75e6595816806ff4cf168214e8a5ec368757dad7dc896033658b84,
  decompressed sha256 20e11ba548bf8702ada14bf2343c96df2c8c431be6ac8ca2eef671d0cfe982d3, git blob 021afd014a64d3b59a7c62f28d56c05bad4ca099.
- `inputs/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz`: sha256 818d676e69caadeb1c9044b9b6aa7d9896dfd2101842918869f9b291a9539b85,
  decompressed sha256 ef43530d3deb4880293b21252d9351d72de99e640be017fcbb6a48f4c1f56cca, git blob b3515c781e420e63a4c0d0e775b4d55a2f1fd6ee.
- `inputs/instances_2.0.csv`: git blob d1d97df9bb121d0ee8f4d8bfc5863d50641f8f54. The instance row is at line 36
  (`...ep_30.onnx,vnnlib/model_64_idx_6371_eps_1.00000.vnnlib,480.0`).
- I fetched each of the 3 files once from raw.githubusercontent at commit 303f2327a8e8411efc4457da03d2016ce42733cf
  (2026-10-25T18:32:13Z, HTTP 200 each) and once from `main` (18:32:14Z to 18:32:15Z, HTTP 200 each). All 6 downloads
  have the sha256 and git blob values above, so the files on main are the same as at the pinned commit.
- GitHub contents API at ref 303f2327 (18:32:26Z to 18:32:28Z, HTTP 200 each) gives sha d1d97df9…, 021afd01… and
  b3515c78… for instances.csv, the vnnlib.gz and the onnx.gz. All three match.
- I fetched the 5 SCORING files from vnncomp2026_results `main` (18:32:00Z to 18:32:02Z, HTTP 200 each). All are
  byte-identical to `inputs/SCORING/`:
  counterexamples_v2.py 5ab7a4df…faab, cex_checks.py 695fcd43…cfc5, settings.py dbd190e5…2039,
  counterexamples.py 1d8ba5bc…a87, benchmark_instances.py 5873d783…d229.

## Witness files agree with each other

- `.counterexample.txt` has 12288 lines plus a trailing newline. 0 lines are non-finite. Every line, read as an exact
  rational, equals a float32 (0 lines are not exact float32), so rounding to float32 is bitwise a no-op.
- `.counterexample.npy`: float32, shape [12288], bitwise equal to the txt values.
- `_v2.counterexample`: header `sat` / `X float32 [1, 64, 64, 3]`, 12288 X values and 43 Y values. X is bitwise equal
  to the txt, and 0 values differ from it as rationals. Its 43 Y values equal my onnxruntime output exactly.

## Input box (exact, all 12288 coordinates, not a sample)

- The vnnlib has 24577 assertions: 24576 atomic input bounds (one `<=` and one `>=` per coordinate, all present) and 1
  output assertion. None mixes inputs and outputs. Bound widths are {1, 2}: 10 coordinates have lo = 0 and 244 have
  hi = 255.
- Strict-interior violations: 0, both for the txt rationals and after float32 rounding. The smallest slack
  min(x - lo, hi - x) is 0.001953125.
- 9707 coordinates differ from the box midpoint. The largest deviation from the midpoint is 0.998046875.
- For context: the box midpoint itself is classified correctly (onnxruntime argmax 17, Y9 - Y17 = -1.0), so the witness
  is not just a misclassified clean image.

## Network replays (my checker; every assertion evaluated with exact rationals)

| runtime | assertions true | satisfied disjunct(s) | Y[0,9] | Y[0,17] | Y9 - Y17 |
|---|---|---|---|---|---|
| onnxruntime 1.26.0 CPUExecutionProvider, float32 | 24577/24577 | only k=9 | 0.9996646642684937 | 0.00033535013790242374 | 0.9993293141305912 |
| same, after float32 rounding of the input | 24577/24577 | only k=9 | 0.9996646642684937 | 0.00033535013790242374 | 0.9993293141305912 |
| onnx.reference.ReferenceEvaluator (onnx 1.21.0) | 24577/24577 | only k=9 | 0.9996646642684937 | 0.00033535013790242374 | 0.9993293141305912 |
| own numpy, float32 | 24577/24577 | only k=9 | 0.9996646642684937 | 0.00033535013790242374 | 0.9993293141305912 |
| own numpy, float64 | 24577/24577 | only k=9 | 0.9996646498695336 | 0.00033535013046647816 | 0.9993292997390671 |
| onnx2torch + torch 2.9.0 CPU, float32 | (output disjunction) | only k=9 | 0.9996646642684937 | 0.00033535013790242374 | 0.9993293141305912 |
| onnx2torch + torch 2.9.0 CPU, float64 | (output disjunction) | only k=9 | 0.9996646498695336 | 0.00033535013046647816 | 0.9993292997390671 |

- Determinism: 18 onnxruntime runs (optimisation levels default, ORT_DISABLE_ALL and ORT_ENABLE_ALL, 1 and 4 intra-op
  threads, 3 repeats each) are bitwise identical. onnx.reference is bitwise equal to onnxruntime. The largest
  difference between my numpy float32 run and onnxruntime is 0.0, and between my numpy float64 run and onnxruntime it
  is 1.4398960024308849e-08.
- Margin requirement: the satisfied branch `(and (>= Y[0,9] Y[0,17]))` has one atom, with margin 0.9993293141305912,
  which is >= 1e-6.
- Fragility of the binarised network: the smallest |Sign input| per Sign layer, float32 / float64, from my numpy
  evaluation (none is exactly 0):
  - BN15: 0.0006465241312980652 / 0.0006465240768193849
  - BN16: 8.279085159301758e-05 / 8.282937139147961e-05
  - flatten: 0.0016204789280891418 / 0.001620479177617734
  - BN18: 0.000557631254196167 / 0.0005576349794864655
  - the four `+0.1` re-sign layers: 0.8999999761581421 / 0.8999999985098839

  The smallest one (BN16, about 8.3e-05) is far above float32 rounding error at that magnitude, and the same signs
  come out in all five runtimes.

## Official validator (unmodified counterexamples_v2.py from the live results repo copy)

The files were laid out the way the repos expect, `vnncomp2026_results/SCORING/` next to
`vnncomp2026_benchmarks/benchmarks/traffic_signs_recognition_2023/2.0/{instances.csv,onnx/,vnnlib/}`, using the files
fetched at 303f2327. I called `validate_vnnlib2_counterexample(benchmark_dir, net, prop, ce, atol, Settings.COUNTEREXAMPLE_RTOL, CounterexampleResult, True)`
the way SCORING/counterexamples.py `_vnnlib2_worker` does. `CounterexampleResult` was taken from counterexamples.py's
own class body. The net and prop fields are the vibecheck results.csv paths. The witness was
`object/..._v2.counterexample`. Environment: onnx 1.21.0, onnxruntime 1.26.0, numpy 2.2.6, vnnlib 1.0.2.

- Run 1, atol=0.0001 (Settings.COUNTEREXAMPLE_ATOL), rtol=0.0: result=correct, "counterexample outputs ignored; using
  ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0"
- Run 2, the same settings: result=correct, with the same rationale.
- Run 3, atol=0.0: result=correct, with the same rationale.

## Table cross-check (one live fetch each; my primary role is the replay)

- SCORING/results.txt from vnncomp2026_results main (2026-10-25T18:35:09Z): HTTP 200, 7681226 bytes, sha256
  ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f. Line 102064 reads
  `Row: ['3_64_64_..._ep_30-model_64_idx_6371_eps_1.00000', 'timeout', 'timeout', 'timeout']`, and the category's tools
  are ['alpha_beta_crown', 'pyrat', 'vibecheck']. No cell contains (h) or (v).
- vibecheck/results.csv (18:53:32Z): HTTP 200, 837443 bytes, sha256 00a7f2bf0a89b530377fae7246c54657c165ccc4bc972463f511f35e1f9be209.
  Line 3351 names the `2.0` paths for this instance with result `timeout`.
- (d): the category is traffic_signs_recognition_2023, so it is neither soundnessbench_2026 nor test.
- I did not check: the results-repo tree for *.check.json files, or the web novelty search (e). These belong to the
  other skeptics.
- repo/TROPHY_CASE.md has no entry for this exact instance (0 lines match `6371` or `3_64_64`). repo/known-knowns
  contains one diagnostic line in an earlier attempt log that names this property file. It is not a witness file.

## Process notes

- My first checker launch was stopped by the agent harness while it was still waiting for the CPU lock, before it had
  run anything. I relaunched it and it completed (exit 0).
- My first official-validator launch failed on import, because settings.py asserts that `BENCHMARK_REPOS` (the
  repo-relative `../vnncomp2026_benchmarks`) exists. I fixed this by reproducing the repo directory layout. The
  validator code was not modified.
- Package temperature readings during my session ranged from 56 to 83 C.

injection_suspected: none

pass: true
