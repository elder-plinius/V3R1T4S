# PREREG: vnncomp-2026-unsolved-instance-counterexample (run 2026-10-24-1500)

Frozen at 2026-10-24T15:18:36Z (date -u), before any attack output on any target instance exists. Changes after this point go into a
new, timestamped PREREG.v2.md.

## Criterion (verbatim, bank repo commit d14b0098)

Success means a saved counterexample input vector (plain text, one value per line, VNN-COMP witness format) for one instance (ONNX file + .vnnlib file taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks at the version directory (1.0 or 2.0) that a participating tool's results.csv in the live results repo names for that benchmark, sha256 of both files recorded) such that ALL of the following hold: (a) in the live SCORING/results.txt of https://github.com/VNN-COMP/vnncomp2026_results (re-fetched live immediately before claiming, never a cached copy) NO tool's cell for that instance's 'Row:' line contains '(h)' or '(v)' (the instance is in the all-tool-unsolved set computed by the skeptic's OWN parse of the live file), and no *.counterexample.check.json for it in any tool directory has result 'correct' or 'correct_up_to_tolerance'; (b) every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file evaluates to true exactly as written under VNN-COMP semantics (i.e. the official validator's zero-tolerance check `_assertions_hold(query, assignment, 0.0, 0.0)` is satisfied), and on the satisfied branch of each output assertion every atomic comparison holds with a strict margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds after rounding the input to float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified from the live results repo against the live benchmark files) returns 'correct' (not merely 'correct_up_to_tolerance'); (d) the instance is not from soundnessbench_2026 or test; (e) a live web search finds no previously published counterexample for that exact ONNX+vnnlib pair (if one exists the result is a replication, not a win). A 'holds'/UNSAT claim for an unsolved instance is never a success under this target.

Partial win p1 (verbatim): A counterexample for an all-tool-unsolved 2026 instance (same set as criterion (a), criteria (d)-(e) also required) that satisfies all vnnlib assertions only with the competition's official input tolerance (inputs within the box up to atol 1e-4, outputs replayed by onnxruntime CPU), i.e. the unmodified SCORING/counterexamples_v2.py returns 'correct_up_to_tolerance' but not 'correct'; confirmed in a second non-onnxruntime runtime.

## The judge (what decides a claim)

A candidate input x for instance (ONNX N, property P) is a **claim candidate** only if ALL of these hold, each from a
saved command output:

1. **Own checker** `attempts/exact-scorer-first/code/vnncheck_own.py --margin 1e-6` prints `VERDICT: PASS` on the
   plain witness file: every input assertion strictly true in exact rationals, as written and after float32 rounding;
   onnxruntime CPUExecutionProvider float32 AND onnx.reference.ReferenceEvaluator: every assertion of P true at zero
   tolerance, and the output assertion's margin >= 1e-6 (atomic margin lhs - rhs in the required direction; `and` =
   min, `or` = max). Calibrated tonight: known positive (repo witness, traffic 3_30_30 idx 1703 eps 1) PASS with margin
   0.99990918 = the published value; known negative (box centre, cora mnist-trades img0) FAIL, margin -10.571.
2. **Official validator** `data/SCORING/counterexamples_v2.py` (unmodified, sha256 5ab7a4df...faab) through
   `official_validate_run.py` returns `correct` at abs_tol 0 (and at 1e-4). Calibrated tonight on the same positive
   (`correct`) and negative (`spec_not_violated`).
3. **Third runtime** (extra, not required by the criterion): the onnx2torch conversion in float32 and float64 on CPU
   gives the same satisfied disjunct with margin >= 1e-6.
4. **Table**: in `results.txt` re-fetched live immediately before claiming, my parse shows no `(h)`/`(v)` in the
   instance's `Row:` line, and the live results tree has no counterexample file for it; the category is not
   soundnessbench_2026 or test.
5. **Files**: N and P are taken unmodified from the 2.0 version directory of vnncomp2026_benchmarks at commit 303f2327
   (named by act, agate, n2v and vibecheck's results.csv for every target category), sha256 recorded. For the three
   wide CNN7 models, which the benchmarks repo distributes only through its own `setup.sh` (public sciebo share), the
   file provenance is a CRITERION question: in-git models are preferred, and a wide-model claim must say so.
6. **Novelty**: no published counterexample for the exact ONNX + vnnlib pair (lens leakage-and-settled and the NOVELTY
   skeptic), and the instance is not already claimed in this repository or its PRs.

Ranking statistic during the attack (not a claim statistic): the best output margin max over disjuncts (min over
atoms) reached by an input strictly inside the box, replayed on CPU in onnxruntime float32.

Safety margins I aim for before calling a candidate (stricter than the criterion, never looser): every coordinate at
least 1e-6 of its box width inside (or one float32 ulp, whichever is larger), and output margin >= 1e-4, so that the
three runtimes cannot flip the verdict.

## Pool (fixed now)

From the 127 all-tool-unsolved rows, excluded with reasons:
- already claimed: traffic 3_30_30 idx1703/idx178 eps1 (TROPHY 51-52), traffic 3_48_48 idx6371 eps3 (#146),
  tinyimagenet_eps1_wide_cnn7_idx7687_sample8 (open PR #566);
- proved UNSAT by the benchmark authors (round 2; re-derived by lens leakage-and-settled): cifar10_eps8_cnn7 idx1742
  samples 4/5/6, cifar10_eps8_wide_cnn7 idx741 sample4 and idx6515 samples 5/6;
- yolo_2023 (6): the properties pin input coordinates (lo == hi; bank PR #631's own count: 5 to 540 pinned coordinates
  per property), so `lo < x_i < hi` of criterion (b) is unsatisfiable under the pinned bank; checked in code by
  `attempts/exact-scorer-first/out/pinned_scan.txt` before any attack on them (none planned).

Order of attack: challenging_certified_training CNN7 rows (8 on in-git models, then 6 on wide models), cora_2024
(cifar10 6, mnist 21; competition timeout 30 s), traffic eps 1 (6), metaroom 1, ml4acopf 1, then cifar100/tinyimagenet
ResNets (62, PGD-filtered at construction).

## Null test

null_test: not needed because every claim is an explicit input vector judged by deterministic checkers (exact-rational
bound checks, onnxruntime/onnx.reference replay, the official validator) against a fixed property and the live table;
there is no search statistic or "beats chance" claim.

## Stop rules

- An instance's attack stops when its frozen budget for the night is spent (lens NOTES say the budget per instance
  before the run starts) or when a claim candidate passes judge items 1-3.
- One instance per claim; if several instances fall, each gets its own claim folder and panel (one carrier per
  instance).
