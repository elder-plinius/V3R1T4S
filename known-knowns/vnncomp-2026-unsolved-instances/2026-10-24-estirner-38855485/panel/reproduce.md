# REPRODUCE skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim checked: the 3072-value input `object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt` is a strict
counterexample for VNN-COMP 2026 `challenging_certified_training_2026` (2.0) `onnx/cifar10_eps8_cnn7.onnx` +
`vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx8072_sample9.vnnlib`, through the disjunct `(and (<= Y[0,3] Y[0,2]))`
with claimed margin 0.00291544199.

Scope of this verdict: `pass: true` covers the checks assigned to the REPRODUCE skeptic. Those are file identity and
GitHub equality, criteria (b) and (c) in full, and my own spot-confirmation of (a) and (d). Criterion (e), the live
web search for a prior publication, is not assessed here.

Work window (from `date -u`): first command Sat Oct 24 07:31:41 PM UTC 2026 (session then cut by an API limit),
resumed Sat Oct 24 09:03:38 PM UTC 2026, last check Sat Oct 24 09:09:35 PM UTC 2026.

## Definition checked against (verbatim from claim/CLAIM.md, "Success criterion")

> Success means a saved counterexample input vector (plain text, one value per line, VNN-COMP witness format) for one
> instance (ONNX file + .vnnlib file taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks at the
> version directory (1.0 or 2.0) that a participating tool's results.csv in the live results repo names for that
> benchmark, sha256 of both files recorded) such that ALL of the following hold: (a) in the live SCORING/results.txt of
> https://github.com/VNN-COMP/vnncomp2026_results (re-fetched live immediately before claiming, never a cached copy) NO
> tool's cell for that instance's 'Row:' line contains '(h)' or '(v)' (the instance is in the all-tool-unsolved set
> computed by the skeptic's OWN parse of the live file), and no *.counterexample.check.json for it in any tool
> directory has result 'correct' or 'correct_up_to_tolerance'; (b) every input coordinate lies STRICTLY inside its
> vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the ONNX model is run on the input with onnxruntime
> CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file evaluates to true exactly as written under
> VNN-COMP semantics (i.e. the official validator's zero-tolerance check `_assertions_hold(query, assignment, 0.0,
> 0.0)` is satisfied), and on the satisfied branch of each output assertion every atomic comparison holds with a strict
> margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds after rounding the input to
> float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or
> onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified from the
> live results repo against the live benchmark files) returns 'correct' (not merely 'correct_up_to_tolerance'); (d) the
> instance is not from soundnessbench_2026 or test; (e) a live web search finds no previously published counterexample
> for that exact ONNX+vnnlib pair (if one exists the result is a replication, not a win). A 'holds'/UNSAT claim for an
> unsolved instance is never a success under this target.

VNN-COMP semantics used: the .vnnlib file encodes the violation, so a counterexample must make EVERY `assert` true.

## Method (my own checker, written before reading claim code)

I wrote my checker before opening `tools/` or `inputs/SCORING/`, and it does not use the claim's numbers. My scratch
scripts are in the sibling folder `mine/` outside claim/ (written below as `../mine/`):
- `../mine/vnnlib_exact.py`: a generic S-expression VNN-LIB reader (comments, `vnnlib-version`, `declare-network`
  with input/output declarations, `assert`, and/or/not, the comparisons <=, >=, <, >, =, the operators + - *,
  row-major multi-index `X[i,j,k,l]`). Unknown constructs raise an error. All arithmetic uses exact
  `fractions.Fraction`; constants are `Fraction(decimal string)` and network values are `Fraction(float(v))`, which is
  exact.
- `../mine/check_inputs.py` checks the input box exactly, float32 representability, and agreement between the
  txt, npy and v2 formats.
- `../mine/eval_outputs.py` evaluates EVERY assertion exactly at zero tolerance and prints every atom's margin.
- `../mine/run_ort.py` (onnxruntime plus determinism), `../mine/run_torch.py` (onnx2torch CPU f32/f64),
  `../mine/run_ref.py` and `../mine/run_ref2.py` (ReferenceEvaluator f32/f64 with onnxruntime import blocked, plus my
  own numpy forward pass in float64 and longdouble), `../mine/run_official.py` (driver for the unmodified validator),
  `../mine/make_controls.py` (negative controls).
- Heavy jobs went through the shared lock wrapper. Package temperature stayed at 46.0 to 62.0 C in every `sensors`
  reading.

## 1. File identity (sha256sum of the claim files)

| file | sha256 (computed) | matches CLAIM.md |
|---|---|---|
| `inputs/onnx/cifar10_eps8_cnn7.onnx.gz` (65214983 bytes) | 172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d | yes |
| decompressed network | d424779ebd3b4a83bf8ebd26ca03f21b4f010a8b2825dd2995d1929c82ae4e59 | yes |
| `inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz` | db437615a60f98e58989e7acfe165b3a6fc10d44ef5bc37ed4bdf3e568186fa5 | yes |
| decompressed property | fb2928b748185d63e091943af317fbb33ecfed1b521773edddc9d96fdf0e41e5 | yes |
| `object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt` | 38855485249d98be61182cb41f1c3d370a4e3208e0cf8efb2796feabc7f3cc29 | yes |
| `object/cifar10_eps8_cnn7_idx8072_sample9_v2.counterexample` | eaed7ec06e6c0430cb69508f60a86b7a38ddac2ddd15e0f142798cc389f5485a | yes |
| `object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.npy` | 923ce426ec4f25ef40500027d65de34a4f4c2c47799fb999143cbd411bcffe8d | yes |
| `inputs/instances_2.0.csv` | eb37c71a62c9748b332c125b280f113132807bcd6551d419f4728bec16bfc08d | (row 30 is the instance, timeout 550) |
| `inputs/SCORING/counterexamples_v2.py` | 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab | equals live (section 2) |

## 2. Equality with the live GitHub files (one plain request per URL, UA `V3R1T4S-research-agent (curl)`)

Fetched Sat Oct 24 09:05:08 PM UTC 2026 to 09:05:48 PM UTC 2026:
- benchmarks@303f2327 `.../2.0/vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz`: HTTP 200, 34824
  bytes, sha256 db437615a60f98e58989e7acfe165b3a6fc10d44ef5bc37ed4bdf3e568186fa5 (equals the claim copy).
- benchmarks@303f2327 `.../2.0/onnx/cifar10_eps8_cnn7.onnx.gz`: HTTP 200, 65214983 bytes, sha256
  172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d (equals the claim copy).
- benchmarks@303f2327 `.../2.0/instances.csv`: HTTP 200, 6666 bytes, sha256 eb37c71a...bfc08d (equals the claim copy).
- results `main` SCORING/counterexamples_v2.py (HTTP 200, 23193 bytes), benchmark_instances.py (200, 4883),
  cex_checks.py (200, 4856), counterexamples.py (200, 15899), settings.py (200, 10377). Each is sha256-identical to the
  claim's `inputs/SCORING/*` copy:
  - counterexamples_v2.py 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab
  - benchmark_instances.py 5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229
  - cex_checks.py 695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5
  - counterexamples.py 1d8ba5bca8fd1568a0da9f612d3bc1c3b725a7c0261064c3198abd2d0ce14a87
  - settings.py dbd190e5cd127a1e1ef8caa19d6416cf6c0d2e94e7698b9b22e96d43661d2039

Git blob ids. I computed them locally as sha1("blob <len>\0"+bytes) and compared them with the GitHub contents API,
fetched Sat Oct 24 09:06:06 PM UTC 2026, all HTTP 200:
- network: local f084be840473d8ebc88ccaaba50bbf1c57001c05; API at ref 303f2327 f084be84...c05 and at ref `main`
  f084be84...c05 (size 65214983).
- property: local 6b2f50fefbd4871361c7d17e80477ec0cd24879e; API at ref 303f2327 and at `main` both 6b2f50fe...79e
  (size 34824).
- benchmarks `main` HEAD is 303f2327a8e8411efc4457da03d2016ce42733cf (2026-07-07T10:57:07Z), so the pinned files are
  the live files. Results `main` HEAD is eea564f5d0a8751d8321a409214db14d03f452b8 (2026-08-03T14:03:54Z).

## 3. Strict interior (exact Fractions)

- The property file is VNN-LIB `<2.0>`. It declares X float32 [1, 3, 32, 32] and Y float32 [1, 10] and has 6145
  assertions: 3072 `>=` bounds, 3072 `<=` bounds and 1 output `or`. All 3072 coordinates have exactly one lower and
  one upper bound.
- The txt has 3072 lines with a single trailing newline. Every decimal string equals a float32 exactly: 0 coordinates
  fail `Fraction(s) == Fraction(float32(s))`. numpy's direct str->float32 parse is bitwise identical, so rounding to
  float32 is the identity.
- The npy (float32, shape (3072,)) is bitwise equal to the txt. The v2 file's 3072 X strings are identical to the txt
  strings, and its 10 Y values are exactly the onnxruntime outputs below.
- Strict interior lo < x < hi as written: 0 violations. min(x-lo) = 2.37920288086e-07 (coord 873); min(hi-x) =
  2.37932006836e-07 (coord 739).
- After float32 rounding: 0 violations, same minima.
- Float32 x against bounds that were themselves rounded to float32: 0 violations.
- Max |x-centre|/halfwidth = 0.999998487729781.
- Coordinates within 1e-6 of a bound: 2768 (within 1e-5: 2768; within 1e-3: 2769). 1477 coordinates are nearer
  their lower bound and 1595 nearer their upper bound.
- So most coordinates sit about 2.4e-7 inside a face of the box. All are strictly interior, as written and after
  float32 rounding.

## 4. onnxruntime 1.26.0 CPUExecutionProvider, float32 (numpy 2.2.6, onnx 1.21.0, Python 3.12.12)

Model: opset 18, ops {Conv: 5, Relu: 6, Flatten: 1, Gemm: 2, BatchNormalization: 1}, 17192650 parameters, all
float32. providers ['CPUExecutionProvider'].
- Y = [-0.668836236000061, -3.231144428253174, 0.3705556392669678, 0.3676401972770691, -0.6815515160560608,
  -0.8117337822914124, 0.13996177911758423, -7.477874279022217, -2.2412099838256836, -4.112461090087891]; argmax 2
  (the true label is 3).
- Exact evaluation of every assertion at zero tolerance: 6145 of 6145 true.
- The output `or` holds through `(<= Y[0,3] Y[0,2])` only. Its exact margin is Y[0,2]-Y[0,3] = 48913/16777216 =
  0.0029154419898986816, which is >= 1e-6 and equals the claimed 0.00291544199.
- The other eight disjuncts are false, with margins -1.0364764333 (Y0), -3.5987846255 (Y1), -1.0491917133 (Y4),
  -1.1793739796 (Y5), -0.22767841816 (Y6), -7.8455144763 (Y7), -2.6088501811 (Y8), -4.4801012874 (Y9).
- After float32 rounding: the input is bitwise unchanged (section 3), so the re-run gives the same result.

## 5. Determinism of the onnxruntime replay

- Same session, 10 repeats: bitwise identical.
- 3 fresh sessions: bitwise identical.
- intra_op threads 1, 2 and 4: bitwise identical.
- Default SessionOptions: bitwise identical.
- 3 separate processes x {memory arena on, off} (the validator turns the arena off): output sha256 prefix
  cc3feb421fc0aee2 in all 6 runs, margin 0.0029154419898986816 in all 6.
- Lower graph optimization levels (ORT_DISABLE_ALL / BASIC / EXTENDED) give a different but still deterministic
  margin of 0.002897500991821289, also >= 1e-6. The default ENABLE_ALL level used by the validator gives
  0.0029154419898986816.

## 6. Second runtimes (not onnxruntime), each evaluated with my exact checker

| runtime | Y[0,2]-Y[0,3] | argmax | assertions true |
|---|---|---|---|
| onnx2torch, torch 2.9.0+cu128, CPU float32 | 93289/33554432 = 0.002780228853225708 | 2 | 6145 of 6145 |
| onnx2torch, CPU float64 | 0.0029126814974439474 | 2 | 6145 of 6145 |
| onnx.reference.ReferenceEvaluator float32 (onnxruntime import blocked) | 0.002908378839492798 | 2 | 6145 of 6145 |
| ReferenceEvaluator float64 (initializers cast to double) | 0.002912681497474312 | 2 | 6145 of 6145 |
| my own numpy forward pass, float64 | 0.0029126814974527737 | 2 | 6145 of 6145 |
| my own numpy forward pass, longdouble (eps 1.084202172485504434e-19) | 0.0029126814974580082 | 2 | 6145 of 6145 |

- Every runtime gives the same satisfied disjunct with margin >= 1e-6, and each repeated run was identical.
- max |own_f64 - ReferenceEvaluator_f64| = 4.085620730620576e-14.
- Note on the panel's runtime estimate: ReferenceEvaluator took 0.04 s here (0.1 s including model load), not the
  expected 40+ minutes. The network has 17192650 parameters, not 33M. I confirmed it was the pure-numpy evaluator by
  setting `sys.modules['onnxruntime'] = None` before running it.

## 7. Official validator, unmodified

The checked file was the live-downloaded `SCORING/counterexamples_v2.py` (sha256 5ab7a4df..., identical to
`inputs/SCORING/counterexamples_v2.py`).
- Layout: the two live benchmark gz files under `<bench>/challenging_certified_training_2026/2.0/{onnx,vnnlib/cifar10_eps8_cnn7}/`
  (as in REPRODUCE step 4).
- Call: my driver `../mine/run_official.py` calls `validate_vnnlib2_counterexample(Path(bench), net, prop, ce,
  atol, 0.0, CounterexampleResult, True)`, exactly as SCORING/counterexamples.py `_vnnlib2_worker` does.
  `CounterexampleResult` is copied verbatim, and the same 1-thread default-session patch is applied.
- Tolerance: COUNTEREXAMPLE_ATOL 0.0001 / RTOL 0.0, read from settings.py. Importing settings.py asserts that a local
  benchmark-repo path exists, so I read the two constants from its text instead.
- Network and property fields: the agate results.csv strings.
- The query is parsed by the official `vnnlib` package, version 1.0.2 (from `importlib.metadata`).

Results:
- `cifar10_eps8_cnn7_idx8072_sample9_v2.counterexample | abs_tol=0.0001 | correct | counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`
- `... | abs_tol=0 | correct | ... all assertions hold with input_tolerance=0.0, output_tolerance=0.0`
- The claim's wrapper `tools/official_validate_run.py` (read after my checker was written) gives the same two
  `correct` lines.
- Negative controls (mine), to show the validator and my checker can reject:
  - Box centre: validator `spec_not_violated` at 1e-4 and at 0 (assertion 6144 failed). My checker: 6144 of 6145
    true, argmax 3, margin -0.33558373153209686.
  - Claimed point with coord 873 moved 1e-5 below its lower bound: validator `correct_up_to_tolerance` at 1e-4 and
    `spec_not_violated` at 0 (assertion 1746, input). My checker: 6144 of 6145, FAIL.

## 8. Live table and other conditions (my own parse)

- results.txt (raw `main`): HTTP 200, 7681226 bytes, sha256
  ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, fetched Sat Oct 24 09:05:48 PM UTC 2026 (equal
  to the claim's record).
  - Under `Category 2026_challenging_certified_training_2026 has 60 (from agate)` (8 participating tools), exactly one
    Row line matches, at line 12985: `['cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx8072_sample9', '-', 'timeout',
    'timeout', '-', 'timeout', 'timeout', '-', 'timeout']`. No cell contains `(h)` or `(v)`.
- Results tree at eea564f5 (API, HTTP 200, 10027325 bytes, truncated False, 27250 entries): no path containing both
  `eps8_cnn7` and `idx8072_sample9`. That filter would catch the competition's naming
  `<tool>/2026_challenging_certified_training_2026/cifar10_eps8_cnn7_cifar10_eps8_cnn7_idx8072_sample9.counterexample*`,
  so there is no counterexample or check.json for this instance in any tool directory.
- Results.csv files for the category also exist for act, cora and nnenum, which are not among the 8 participants.
  Their row 30 for this instance, fetched at eea564f5 (all HTTP 200):
  - agate: version dir 2.0, `unknown`
  - act: 2.0, `unknown`
  - cora: 1.0, `unknown`
  - nnenum: 1.0, `error_exit_code_1`
  None resolved it. agate (a participant) names version directory 2.0, which matches the claim.
- (d) The category is challenging_certified_training_2026, which is neither soundnessbench_2026 nor test.
- (e) Live web search for a prior published counterexample: not part of my REPRODUCE scope and not performed by me.

## Discrepancies found

- None in the claim. Every hash, blob id, bound, assertion, margin and validator verdict reproduces exactly.
- The claimed margin 0.00291544199 is the onnxruntime ENABLE_ALL value 0.0029154419898986816.
- Other runtimes and onnxruntime optimization levels give 0.00278 to 0.00292, all far above 1e-6.

No injection suspected: no file, page or program output attempted to instruct me.

pass: true
