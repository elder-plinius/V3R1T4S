# REPRODUCE skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim checked: the 3072-value input `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` is a strict
counterexample for `onnx/cifar10_eps8_wide_cnn7.onnx` + `vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib`
(challenging_certified_training_2026, version 2.0), satisfying the disjunct `(and (<= Y[0,4] Y[0,6]))` with claimed
margin 0.0004062354565.

Work started 2026-10-24 18:20:13 UTC (`date -u`).

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
> VNN-COMP semantics (i.e. the official validator's zero-tolerance check `_assertions_hold(query, assignment, 0.0, 0.0)`
> is satisfied), and on the satisfied branch of each output assertion every atomic comparison holds with a strict
> margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds after rounding the input to
> float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or
> onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified from the
> live results repo against the live benchmark files) returns 'correct' (not merely 'correct_up_to_tolerance'); (d) the
> instance is not from soundnessbench_2026 or test; (e) a live web search finds no previously published counterexample
> for that exact ONNX+vnnlib pair (if one exists the result is a replication, not a win). A 'holds'/UNSAT claim for an
> unsolved instance is never a success under this target.

VNN-COMP semantics used by my checker: the .vnnlib file encodes the violation; an input X with Y = N(X) is a
counterexample iff EVERY top-level `(assert ...)` is true. `and`/`or` are the usual connectives; comparisons are exact.

My scope as REPRODUCE skeptic: (b), (c), and the identity/provenance of every file. I did not verify (a) (live table /
unsolved status) or (e) (prior publication); (d) is true by name (the category is challenging_certified_training_2026).

## My own checker (written before reading any claim code)

`claim/tools/` was never read or run. My scripts (in my scratch folder, outside claim/):
- `vnncheck.py`: my own tokenizer and S-expression parser for VNN-LIB (comments, `declare-network`, `assert`, `and`,
  `or`, `not`, `<=`, `>=`, `<`, `>`, `=`, indexed variables, decimal constants), with an evaluator that compares
  everything exactly with `fractions.Fraction` (decimal constants parsed from their strings; float values converted
  exactly). It rejects any form it does not know.
- `check_inputs.py`: strict input-bound check, three ways.
- `eval_outputs.py`: evaluates all assertions for a given runtime output; reports every disjunct and its margin.
- `run_ort.py`, `run_torch_numpy.py` (onnx2torch, plus my own numpy forward pass written from the ONNX node list),
  `run_ref.py` (onnx.reference), `run_sibling.py`, `run_official.py` (calls the unmodified official function).

Survey of the property file (my parse): 6145 top-level asserts = 3072 `(>= X[...] c)` + 3072 `(<= X[...] c)` (exactly
one lower and one upper bound for each of the 3072 coordinates, no duplicates) + 1 output assert, an `or` of 9 single-atom
`and`s `(<= Y[0,4] Y[0,k])`, k in {0,1,2,3,5,6,7,8,9}. Declarations: `X float32 [1, 3, 32, 32]`, `Y float32 [1, 10]`.
Header comment: label 4, L_inf epsilon 0.03137254901960784.

## 1. File identity (sha256sum)

| file (relative to claim/) | sha256 I computed | matches CLAIM.md |
|---|---|---|
| `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` (132594607 bytes) | 7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8 | yes |
| same, decompressed (140757533 bytes) | e3940df279250819ea8f6776458429981c29ff1bdd719083cc5b4c1e9c3ff873 | yes |
| `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` | c64e879e9a88b80384dc67f3b84cd8f12a299c9488f136961cb8f226e9f01a59 | yes |
| same, decompressed | 2fad12842961518733ccae34ef7430f08d6e653b1d7acb30671135e019c5d45e | yes |
| `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` | 36afa0dd0c97274d86c6c31f0b42cfab276b522b393a8374a9bb2e18391696b4 | yes |
| `object/cifar10_eps8_wide_cnn7_idx7490_sample8_v2.counterexample` | 9f66bd2131f63cb25c28e2c04046374108bdf80929d7e8ad9f94185dfd26fef5 | yes |
| `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.npy` | ea1e84a99c52e3a145e1dabaab317e92a5a44ff3b5ea3f233707b3a0fd960bff | yes |
| `inputs/sibling_validated_witness/...idx637_sample0.counterexample.gz` | 63ca2d1b46f830a2cec0813d2ca2b9440049f4c51f4d51890c8ae0240899af37 | yes |
| `inputs/instances_2.0.csv` | eb37c71a62c9748b332c125b280f113132807bcd6551d419f4728bec16bfc08d | (not listed; see 2) |
| `inputs/SCORING/counterexamples_v2.py` | 5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab | (not listed; see 2) |
| `inputs/SCORING/benchmark_instances.py` | 5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229 | (not listed; see 2) |
| `inputs/SCORING/cex_checks.py` | 695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5 | (not listed; see 2) |

## 2. Public-source identity (one plain request per URL, `-A "V3R1T4S-research-agent (curl)"`, no retries)

| URL | time (UTC) | HTTP | bytes | result |
|---|---|---|---|---|
| https://rwth-aachen.sciebo.de/public.php/dav/files/gEMDMstBiSHAAAS/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx.gz | 18:40:55 to 18:41:52 | 200 | 132594607 | sha256 7e65aedd...f5f8; `cmp` byte-identical to `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` |
| https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/challenging_certified_training_2026/2.0/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz | 18:42:28 | 200 | 33067 | sha256 c64e879e...1a59; byte-identical to `inputs/vnnlib/...vnnlib.gz` |
| https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/challenging_certified_training_2026/2.0/instances.csv | 18:47:32 | 200 | 6666 | byte-identical to `inputs/instances_2.0.csv`; line 39 is `onnx/cifar10_eps8_wide_cnn7.onnx,vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib,550` |
| https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING/{counterexamples_v2.py, benchmark_instances.py, cex_checks.py} | 18:47:10 | 200, 200, 200 | 23193, 4883, 4856 | all three byte-identical to `inputs/SCORING/` copies |
| https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/counterexamples_v2.py | 18:47:10 | 200 | 23193 | byte-identical to `inputs/SCORING/counterexamples_v2.py` |

So the network, the property, the instances list and the validator I ran are the public files, unmodified. The
benchmarks commit 303f2327 and results commit eea564f5 are the ones CLAIM.md names; I did not check independently that
303f2327 is the benchmarks repo's current head.

## 3. Witness files and strict input bounds (exact, `fractions.Fraction`)

- txt: 3072 lines, every line a plain decimal; all 3072 strings are exactly float32 values (string value == its float32
  rounding: 3072 of 3072). So "as written" and "rounded to float32" are the same tensor (input sha256
  76554d9c139cf85c21dcb0f30a0168f272abf135f28bd9baaa54ecacdf47d0e3 both ways).
- The v2 file's X block has the same 3072 strings as the txt (identical: True); the npy (float32, shape (3072,)) holds
  exactly the same values (True). The v2 file's 10 Y values equal my onnxruntime output exactly (True).
- Strict bounds, against the bounds parsed from the .vnnlib text:

| comparison | strict violations | non-strict violations | min(x - lo) | min(hi - x) |
|---|---|---|---|---|
| x as written vs decimal bounds | 0 | 0 | 2.379464e-07 (coord 1398) | 2.379689e-07 (coord 2070) |
| x rounded to float32 vs decimal bounds | 0 | 0 | 2.379464e-07 (coord 1398) | 2.379689e-07 (coord 2070) |
| x float32 vs bounds rounded to float32 | 0 | 0 | 2.384186e-07 (coord 20) | 2.384186e-07 (coord 19) |

  The tightest coordinates sit 0.998 float32 ulps from a bound (min distance to lo 0.998 ulps, to hi 0.998 ulps): the
  witness is pushed to the edge of the box but every coordinate is strictly inside under every reading, including the
  float32-vs-float32 comparison the official validator performs. The definition asks for strictness at zero tolerance,
  not for a margin on the inputs.

## 4. onnxruntime CPUExecutionProvider, float32 (onnxruntime 1.26.0, venv pins numpy 2.2.6 / onnx 1.21.0)

Network graph (my read): opset 18, input `input` [batch,3,32,32] float, output `output` [batch,10] float;
5 Conv, 6 Relu, 1 Flatten, 2 Gemm, 1 BatchNormalization; 35188618 parameters, all float32.

Output (both separate processes, intra/inter-op threads 1):
`Y = [-2.3425824642181396, -1.9580364227294922, 0.3085559606552124, -0.31000083684921265, 0.48005759716033936,
-0.4104645848274231, 0.48046383261680603, -0.68595951795578, -4.591410160064697, -1.724597692489624]`, argmax 6
(the property's label is 4). Ranking 6, 4, 2, ...

My evaluator: assertions true 6145 of 6145 (zero tolerance, exact). Satisfied disjunct: `(and (<= Y[0,4] Y[0,6]))`
only (the other 8 are false). Margin Y[0,6] - Y[0,4] = 0.0004062354564666748 (exact 13631/33554432), >= 1e-6: True.
Claimed 0.0004062354565; |difference| 3.3325176385795574e-14 (the claim rounds to 13 significant digits). Agrees.

Determinism: run 1 and run 2 (separate processes) each did 2 in-process repeats; all four outputs have sha256
c06448bf53d14963b888d1f13342e5c500dca14b096186a37809b63b60a340c4, and the saved npy files are byte-identical (`cmp`,
sha256 fb5b1c0e75248c13a13a6282e330bf1f7b6ef88ce916210eefa732068926e9d2 both). A session with default options (all
graph optimizations, default threads) gives the same bytes (identical True). With graph optimizations disabled
(ORT_DISABLE_ALL) the output differs slightly but still satisfies all 6145 assertions, margin 0.00040724873542785645.
Determinism was checked on this one machine and onnxruntime build only.

## 5. Second runtimes (not onnxruntime), CPU

| runtime | Y[0,4] | Y[0,6] | argmax | assertions true (my evaluator) | margin Y6 - Y4 |
|---|---|---|---|---|---|
| onnx2torch, torch 2.9.0+cu128, CPU, float32 | 0.48006099462509155 | 0.4804673492908478 | 6 | 6145 of 6145 | 0.0004063546657562256 |
| onnx2torch, CPU, float64 (model .double(), float32 input upcast) | 0.4800591671905963 | 0.480463215399486 | 6 | 6145 of 6145 | 0.0004040482088896735 |
| my own numpy forward pass, float64 | 0.48005916719060915 | 0.48046321539949066 | 6 | 6145 of 6145 | 0.0004040482088815134 |
| my own numpy forward pass, long double (float128) | 0.48005916719060837 | 0.4804632153994889 | 6 | (margin printed only) | 0.00040404820888047987 |
| onnx.reference.ReferenceEvaluator (onnx 1.21.0), float32 | 0.4800585210323334 | 0.48046573996543884 | 6 | 6145 of 6145 | 0.00040721893310546875 |

max |onnx2torch float64 - own numpy float64| over the 10 outputs = 1.2823075934420558e-14. onnx2torch float32 repeat
identical: True. Across every runtime I ran, the margin lies between 0.0004040482088815134 and 0.00040724873542785645.
The spread, 3.200526547376579e-06, is far below the margin, and the smallest margin is 404.0482088804799 times the
1e-6 floor. The
float64/long-double values give the best estimate of the network's exact output at this input; it also satisfies the
property, with margin 0.000404048...

Note: `run_torch_numpy.py` exited with code 1 at its very last print line (a dictionary-key typo: numpy names long
double `float128`). Every number above was printed and all npy files were saved before that line; the omitted line was
only a float64 vs long-double difference. From the printed values, the two margins differ by 1.0335157209218071e-15.

### 5b. onnx.reference.ReferenceEvaluator

I ran it once, through the CPU lock, with a 2700 s cap. The job was queued at 18:47:32 UTC, its python process started
18:49:51 and the job ended 18:51:18 with exit 0. The script reported `elapsed 0.5 s` for model load plus evaluation,
much faster than the rules warned.
Input sha256 76554d9c139cf85c21dcb0f30a0168f272abf135f28bd9baaa54ecacdf47d0e3 (same tensor as the onnxruntime runs).
Output dtype float32, shape (1, 10):
`Y = [-2.342583179473877, -1.9580367803573608, 0.3085569143295288, -0.3100006580352783, 0.4800585210323334,
-0.41046449542045593, 0.48046573996543884, -0.6859582662582397, -4.591413974761963, -1.7245986461639404]`, argmax 6.

My evaluator: assertions true 6145 of 6145 (zero tolerance, exact); satisfied disjunct `(and (<= Y[0,4] Y[0,6]))`
only, margin 0.00040721893310546875 (exact 427/1048576), >= 1e-6: True. This output is not a copy of the onnxruntime
output (bytes identical: False; max |ref - ort| = 3.814697265625e-06), so it is an independent float32 computation.
Its margin also lies inside the range given above for the other runtimes.

## 6. Official validator, unmodified `inputs/SCORING/counterexamples_v2.py` (byte-identical to the live results repo)

I called `validate_vnnlib2_counterexample(Path(benchmark_dir), net, prop, ce_path, abs_tol, 0.0, CounterexampleResult, True)`,
the same call the official `counterexamples.py` makes for version 2.0. I used the same CounterexampleResult string values,
because `counterexamples.py` itself imports `vnnlib_v1` and `cachier`, which are not in the package. Each call ran in its
own process. The benchmark dir was a fresh layout in my scratch folder, `challenging_certified_training_2026/2.0/{onnx,vnnlib/cifar10_eps8_wide_cnn7}/`,
holding copies of the two claim gz files. Fields were the results.csv-style paths
`vnncomp2026_benchmarks/benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx` and
`.../2.0/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib`. The validator resolved them to
`onnx/cifar10_eps8_wide_cnn7.onnx.gz` (sha256 7e65aedd...f5f8) and `vnnlib/.../cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz`
(sha256 c64e879e...1a59). Witness `object/cifar10_eps8_wide_cnn7_idx7490_sample8_v2.counterexample` (sha256 9f66bd21...ef5).
Packages: vnnlib 1.0.2, ort 1.26.0, onnx 1.21.0, numpy 2.2.6.

- abs_tol=0.0001: `correct | counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`
- abs_tol=0: `correct | counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0`

The validator returns `correct` only when `_assertions_hold(query, assignment, 0.0, 0.0)` holds (code read), and it
ignores the witness's own Y values and replays the network itself, so its result does not depend on the Y block.

Negative control (to show both checkers can fail): the box centre, (lo+hi)/2 per coordinate rounded to float32 (strictly
inside). The official validator at abs_tol=0.0001 says `spec_not_violated | ... assertion 6144 failed with tolerance 0.0 (output/mixed)`.
My onnxruntime replay plus evaluator says argmax 4, assertions true 6144 of 6145, every disjunct false (closest
Y6 - Y4 = -0.25862205028533936).

## 7. Sibling witness: the network file behaves like the one the competition validated

`inputs/sibling_validated_witness/`: alpha_beta_crown's witness for `cifar10_eps8_wide_cnn7_idx637_sample0`, with its
check.json (`result: correct`, `version: 1.0`, rationale `prop #7 violated: [-0.00023888]`). I replayed it on our network
file with onnxruntime CPU float32. Y8 - Y3 = 0.00023888051509857178 (official replay in check.json: 0.00023888).
Max |our replay - solver-reported Y| = 3.3974647521972656e-06. So our network file reproduces the validated replay
to every digit the check.json prints.

Against the *2.0* sibling property in the same folder, that witness is strictly inside only 1589 of 3072 bounds, and
4662 of 6145 assertions are true. This is no defect: the check.json says it was validated against version 1.0, and the
1.0 and 2.0 properties of that sample evidently have different input boxes. Only the network comparison is evidence
here, and it matches.

## Injection check

Nothing in the claim text, the validator source or any program output asked me to do anything. injection_suspected: none.

## Verdict

Everything I was asked to reproduce holds, from files whose hashes match CLAIM.md and the public sources:
- The witness is strictly inside every input bound, exactly, as written and as float32.
- onnxruntime CPU float32 makes all 6145 assertions true at zero tolerance through `(<= Y[0,4] Y[0,6])`, margin
  0.0004062354564666748, which matches the claimed 0.0004062354565.
- The result is deterministic.
- onnx2torch (float32 and float64), onnx.reference.ReferenceEvaluator (float32) and my own numpy forward pass
  (float64 and long double) agree, with margins >= 0.000404.
- The unmodified, byte-verified official validator returns `correct` at zero tolerance.
- The network file is byte-identical to the public share copy.

Outside my scope: criteria (a) and (e).

pass: true
