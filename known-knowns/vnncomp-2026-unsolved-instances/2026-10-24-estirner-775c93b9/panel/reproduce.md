# REPRODUCE skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Run window (from `date -u`): Sat Oct 24 04:34:06 PM UTC 2026 to Sat Oct 24 05:01:44 PM UTC 2026.
injection_suspected: none observed (no file or web response contained instructions).

## Definition checked against (quoted from claim/CLAIM.md, "Success criterion (verbatim ...)")

> (b) every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when
> the ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib
> file evaluates to true exactly as written under VNN-COMP semantics (i.e. the official validator's zero-tolerance
> check `_assertions_hold(query, assignment, 0.0, 0.0)` is satisfied), and on the satisfied branch of each output
> assertion every atomic comparison holds with a strict margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required
> direction); (c) the same holds after rounding the input to float32 and re-running, AND in a second runtime that is
> not onnxruntime (onnx2pytorch/torch or onnx.reference.ReferenceEvaluator), AND the competition's own
> SCORING/counterexamples_v2.py (run unmodified from the live results repo against the live benchmark files) returns
> 'correct' (not merely 'correct_up_to_tolerance');

The claimed value: the disjunct `(and (<= Y[0,5] Y[0,2]))` holds, margin Y[0,2] - Y[0,5] = 0.01176285744.

## Method

I wrote my own checker before looking at claim/tools/ (I only hashed claim/tools/; I never opened or ran it). Scratch scripts are
outside claim/: `work/scripts/vnncheck.py` (sha256 2f749ea0...56cd) has a tokenizer and S-expression parser for
VNN-LIB 2.0 (`vnnlib-version`, `declare-network`, `assert`; it fails on any unknown form), a row-major index map,
and an evaluator for `and/or/not/<=/>=/</>/+/-/*` in exact `fractions.Fraction` arithmetic. Decimal constants
become `Fraction(str)`, and network outputs are converted exactly from their float32/float64 values. It records
every atomic comparison with its signed margin. A second, regex-only bound reader (`work/scripts/inputs_check.py`)
cross-checks the input box. Runtimes: `run_ort.py` (onnxruntime), `run_torch.py` (onnx2torch, CPU), `run_ref.py`
and `ref_probe.py` (onnx.reference), `drive_official.py` (my own driver for the unmodified official validator).
Every job of more than a few seconds ran through the shared cpu1.sh lock. Package temperature stayed between
+68.0 C and +80.0 C.

## Results (every number copied from command output)

1. **File identity (sha256sum).** Every hash in CLAIM.md matches:
   - `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` 7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8 (132594607 bytes); decompressed e3940df279250819ea8f6776458429981c29ff1bdd719083cc5b4c1e9c3ff873 (140757533 bytes)
   - `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz` 3e9340de6e0237635a572457218e5c4f74b298e20ff69dc482a627e85206d1fe; decompressed 5593601c97c83875dba34d251ba1b772f299bd4b622e5646bb520c260169bd85
   - `object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt` 775c93b9b508b63002b8da10ce73cf317537692b3ef7d0e2b84747f67367baca
   - `object/cifar10_eps8_wide_cnn7_idx6249_sample7_v2.counterexample` 9910a4f00246b11f4d2c5cfd566804e0bebbe7d9fbd5dd373e35377ca4971dc3
   - `object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.npy` fdaea2ac5bbe2b2dceba9cddb64e9749a99b42334df44ee42aa697ea86327cf7
   - `inputs/sibling_validated_witness/...idx637_sample0.counterexample.gz` 63ca2d1b46f830a2cec0813d2ca2b9440049f4c51f4d51890c8ae0240899af37

2. **The three object files agree.** The txt file has 3072 lines, and 0 of its decimal strings fail to be an exact
   float32 value. The npy file is float32 with shape (3072,) and is bit-identical to the txt values. The v2 file has
   header `sat` / `X float32 [1, 3, 32, 32]` and 3072 X strings that are identical to the txt strings. Its 10 Y
   values exactly equal my onnxruntime output (see item 4).

3. **Input bounds, exact.** My parser finds 6145 assertions: 6144 input-bound atoms and 1 output assertion. 0
   coordinates lack a bound, and there are **0 strict-bound violations**. This holds both for the values as written
   (`Fraction` of the decimal strings) and for the float32-rounded values, which are bit-identical because every
   string is exactly a float32. The minimum gap to a bound is 2.37924438e-07, at flat index 78. The regex reader
   independently finds lo 3072 / hi 3072 and 0 strict violations. Box widths range from 0.155079364 to 0.31466961.
   111 coordinates sit on the last float32 inside a bound (the next float32 outward would cross it); they are still
   strictly inside.

4. **onnxruntime 1.26.0 CPUExecutionProvider, float32** (onnx 1.21.0, numpy 2.2.6; opset 18; graph ops Conv x5,
   Relu x6, Flatten, Gemm x2, BatchNormalization; 35188618 initializer parameters).
   - Y = [-1.7233030796051025, -3.504415512084961, 0.3472158908843994, 0.2884974479675293, 0.05927523970603943,
     0.3354530334472656, -0.5704138875007629, -0.7080146074295044, -2.996689796447754, -2.8960139751434326], argmax 2.
   - My checker finds every one of the 6145 assertions true at zero tolerance. The output disjunction holds through
     `(and (<= Y[0,5] Y[0,2]))` only. Its exact margin is Y2 - Y5 = 49337/4194304 = **0.011762857437133789**, which
     is >= 1e-6. The claimed value is 0.01176285744 (abs diff 2.8662109375e-12, i.e. the claim rounded to 10
     significant digits). All other disjuncts are false. The closest is `(<= Y[0,5] Y[0,3])` at -0.0469555854797.
   - **Determinism.** Two runs in one session are bitwise equal. `intra_op_num_threads=1` gives bitwise the same
     output as the default. A second, separate process gives the same Y-bytes sha256
     5cbc536c36c4cd97e995129b74128d0225a5e535a704b508f895b3b04c5ac9c6 both times.
   - Extra robustness check: with `ORT_DISABLE_ALL` graph optimizations, Y moves by at most 2.8014183044433594e-06.
     The margin becomes 0.0117614865303 and the checker still passes.

5. **Second runtimes (not onnxruntime), checked by my checker:**
   - onnx2torch / torch 2.9.0+cu128, CPU, `.eval()`, float32: all assertions true, margin 0.011764973402. Two runs
     are identical.
   - The same in float64 (weights converted with `.double()`, float64 input): all assertions true, margin
     0.0117608594799. Two runs are identical.
   - onnx.reference.ReferenceEvaluator (onnx 1.21.0), float32: all assertions true, margin 0.0117572247982. Two
     runs are bitwise equal. It used op classes `ops_optimized.op_conv_optimized.Conv`, `op_gemm.Gemm_7`,
     `op_batch_normalization.BatchNormalization_14`, `op_relu.Relu` and `op_flatten.Flatten`. After the run,
     `'onnxruntime' in sys.modules` was False and `'torch' in sys.modules` was False. It took 0.1 s (its optimized
     numpy Conv), not the minutes the kit warned about. Its output differs from onnxruntime (Y2
     0.3472099006175995 vs 0.3472158908843994), so it is an independent computation.
   - In every runtime the satisfied branch and argmax 2 are the same, and every margin is far above the 1e-6
     threshold (smallest 0.0117572247982).

6. **Official validator, unmodified.** I compared the git blob sha1 of each of the five `inputs/SCORING/*.py` files
   (computed locally) with the results-repo tree at eea564f5d0a8751d8321a409214db14d03f452b8 (GitHub API, HTTP 200,
   not truncated). All 5 match, e.g. counterexamples_v2.py 82761145bb8097928b887235b0e238a2b6f25320.
   - The validator ran from a scratch copy of `inputs/SCORING` whose five sha256 values equal the originals.
   - My own driver laid out `bench/challenging_certified_training_2026/2.0/{onnx,vnnlib/cifar10_eps8_wide_cnn7}`
     with byte-identical copies of the two .gz files. It called `validate_vnnlib2_counterexample` the way
     `SCORING/counterexamples.py::_vnnlib2_worker` does, with the results.csv-style network and property paths, using
     onnx 1.21.0, ort 1.26.0, numpy 2.2.6 and vnnlib 1.0.2. Results:
     - abs_tol=0.0001, rel_tol=0.0, ignore_ce_outputs=True: `result='correct'`, "all assertions hold with
       input_tolerance=0.0, output_tolerance=0.0"
     - abs_tol=0.0, ignore_ce_outputs=True: `result='correct'`, same rationale
     - abs_tol=0.0, ignore_ce_outputs=False: `result='correct'`, same rationale
   - I did not import `settings.py`, because on import it asserts that a benchmark-repo directory exists. Instead I
     used its values COUNTEREXAMPLE_ATOL = 1e-4 and COUNTEREXAMPLE_RTOL = 0.0 (settings.py lines 71-72).

7. **Is this the competition's network? (sibling witness).** I replayed alpha_beta_crown's witness for
   idx637_sample0 through onnxruntime on this network file. Its blob matches
   `alpha_beta_crown/2026_challenging_certified_training_2026/...idx637_sample0.counterexample.gz` in the eea564f5
   tree, and the provided check.json matches alpha_beta_crown's too.
   - The result reproduces the tool's reported Y to max |diff| 3.3974647521972656e-06.
   - The branch `(<= Y[0,3] Y[0,8])` (disjunct #7) has margin 0.000238880515099, matching the check.json rationale
     "prop #7 violated: [-0.00023888]".
   - Caveat: that check.json says benchmark version "1.0", while the sibling .vnnlib in the package is the 2.0 file.
     Against the 2.0 bounds my strict checker finds 1483 sibling coordinates on or outside a bound (min gap
     -4.98291e-10). This is consistent with a witness clipped to the 1.0 box and then compared with the 2.0 file's
     10-digit decimal bounds. It says nothing about the claimed witness, whose minimum gap is 2.379e-07.

8. **Provenance spot checks (one plain request each, UA "V3R1T4S-research-agent (curl)"):**
   - Benchmarks raw vnnlib.gz at commit 303f2327...: HTTP 200, 35086 bytes, sha256 3e9340de...d1fe, which equals
     `inputs/vnnlib/...vnnlib.gz`.
   - Benchmarks raw `2.0/instances.csv` at 303f2327: HTTP 200, 6666 bytes, sha256 eb37c71a...c08d, which equals
     `inputs/instances_2.0.csv`. Line 38 is
     `onnx/cifar10_eps8_wide_cnn7.onnx,vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib,550`.
   - Public share (sciebo WebDAV URL from CLAIM.md) onnx.gz: HTTP 200, 132594607 bytes, sha256
     7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8, which equals `inputs/onnx/...onnx.gz`.
   - Live `SCORING/results.txt` (main), fetched between 04:58:19 and 04:58:34 PM UTC: HTTP 200, 7681226 bytes,
     sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (equals the claimed fetch). The instance
     row is `Row: ['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx6249_sample7', '-', 'timeout', 'timeout',
     'timeout', 'timeout', 'timeout', '-', 'timeout']`, with no `(h)` and no `(v)`. Lines 13087 and 13587 of the
     live file are identical to `table/results_txt_excerpt.txt`.
   - In the eea564f5 tree, no path contains `idx6249_sample7`, so no tool has a counterexample or check.json for
     this instance.

## Not checked by this skeptic

Criterion (e), a live web search for a previously published counterexample, is left to the novelty skeptic. For
(d), the category is challenging_certified_training_2026, which is neither soundnessbench_2026 nor test.

## Verdict

Every property I was asked to reproduce holds when checked from the saved files with my own exact checker: strict
input bounds (as written and after float32 rounding), every assertion true at zero tolerance, and a satisfied-branch
margin >= 1e-6. This holds in onnxruntime (deterministic across runs, threads and processes), onnx2torch float32 and
float64, and onnx.reference float32. The unmodified official validator returns `correct` at zero tolerance. The
claimed margin 0.01176285744 is the exact float32 margin 0.011762857437133789 rounded to 10 significant digits. I
found no mismatch, missing object or non-determinism.

pass: true
