# Criterion skeptic verdict: vnncomp-2026-unsolved-instance-counterexample, traffic_signs_recognition_2023, model_48_idx_6371_eps_3.00000

Scope of what I read: only the claim folder (CLAIM.md, REPRODUCE.md, SHA256SUMS, run_official.py, SCORING/, benchmark/, table_record/, witness_plain.txt, witness_v2.txt). Scratch work only in a separate criterion_work directory. I did not re-fetch anything live and did not web-search. All SHA256SUMS entries verified OK.

## Clause-by-clause

Preliminary: version directory. table_record/vibecheck_results.csv names benchmark/2.0 for this instance; alpha_beta_crown_results.csv and pyrat_results.csv name 1.0. The criterion says "a participating tool's results.csv", so 2.0 (via vibecheck) is a legitimate choice. The ONNX gz is byte-identical across 1.0 and 2.0 (same sha256). The vnnlib differs in syntax (1.0 flat X_i/Y_j, 2.0 X[0,h,w,c]/Y[0,c]); I extracted the bounds from both and they are numerically identical. Both vnnlib files have 6912 lower bounds, 6912 upper bounds, and one (or ...) of 42 disjuncts (Y_c >= Y_17, c != 17).

(a) Unsolved in the live table: PARTIAL / NOT ESTABLISHED LIVE.
- In the package copy of results.txt (fetch_status 200, fetch_time 2026-10-15T00:28:04Z) the line `Row: [...model_48_idx_6371_eps_3.00000', 'timeout', 'timeout', 'timeout']` is the only Row for this instance, and the summary line for it reads timeout, timeout, timeout. No (h) or (v) in its cells. The three cells match the three tools that have this category (alpha_beta_crown, pyrat, vibecheck); each tool's results.csv in table_record/ shows timeout / run_instance_timeout / timeout for this instance. So on the cached copy the instance is all-tool-unsolved.
- Not establishable from the package: (i) that this copy equals the live file at the moment of claiming (the criterion demands a live re-fetch, never a cached copy, and I must not fetch); (ii) the "no *.counterexample.check.json with result correct / correct_up_to_tolerance in any tool directory" sub-clause: the package contains no tool directory listings or check.json files at all. A timeout in every cell makes a 'correct' check file unlikely but not excluded.

(b) Strictly inside, float32, assertions, 1e-6 margin: CONFIRMED (my own independent parse and run).
- 6912 values in witness_plain.txt (one per line), mapped to X[0,h,w,c] row-major (h,w,c). All lo < x < hi with zero tolerance; smallest distance to a bound is 0.001953125 (lo side) / 0.00390625 (hi side). The 1.0-copy bounds are the same, so the same holds there.
- Every value is exactly representable in float32 (float64 parse equals its float32 cast); strictly inside after float32 rounding as well.
- onnxruntime 1.31.0 CPUExecutionProvider, float32 input shape [1,48,48,3]: Y[0,9]=0.880797, Y[0,17]=0.11920291, Y[0,9]-Y[0,17]=0.7615941 >= 1e-6. Exactly one of the 42 disjuncts is satisfied (class 9, margin 0.76); the other 41 are not. The margin on the satisfied branch is about 7.6e5 times the required 1e-6. Same value with graph optimizations disabled and with a single thread.
- Null models: the box center is classified 17 (Y17=1.0); 300 uniform random points and 300 random box corners all stay at class 17 (0 violations). So the witness is not a trivial or generic point and the network/spec do not satisfy the disjunction by accident; this is a targeted point. (Ops include Sign, i.e. discontinuities, but the second runtime agrees, see (c).)

(c) Float32 rerun, second runtime, official validator: CONFIRMED.
- Float32 re-run: the inputs are already float32-exact, so identical.
- Second runtime not onnxruntime: onnx.reference.ReferenceEvaluator gives Y9-Y17 = 0.7615941, max output difference to ORT 7.5e-9, same single satisfied class. (torch/onnx2pytorch not tried; the criterion allows either.)
- Official validator, unmodified SCORING/counterexamples_v2.py (I ran the package's run_official.py with bytecode writing disabled): 2.0 with abs_tol 0.0 returns ('correct', '... all assertions hold with input_tolerance=0.0, output_tolerance=0.0'); with abs_tol 1e-4 also 'correct' (not correct_up_to_tolerance). The validator ignores the Y block of the witness and replays ONNX on CPU. 1.0 returns 'unsupported' (parser is VNN-LIB 2.0 only), which is irrelevant to a 2.0 claim. Caveats: my environment has newer numpy/onnx/onnxruntime than SCORING/requirements.txt pins, and the package's SCORING copy cannot be shown to be identical to the live results repo's file from inside the folder. The validator was run on the gz files as packaged.

(d) Benchmark not soundnessbench_2026 or test: CONFIRMED. Category is traffic_signs_recognition_2023 (2026_traffic_signs_recognition_2023 in results.txt).

(e) No previously published counterexample (live web search): NOT ESTABLISHED. The package cannot contain the result of a live web search and I did not search. This clause is a precondition for the result being a win rather than a replication; absent it, I cannot confirm the full criterion.

## Hidden quantifiers / stretched definitions noted
- "Participating tool's results.csv names the version" is satisfied only by vibecheck (2.0); two tools name 1.0. Acceptable under the literal wording ("a participating tool"), but the validator-clause is only passable on the 2.0 file, so the claim is correctly scoped to 2.0.
- witness_v2.txt carries a 'sat' header plus an X block and a Y block of the replayed outputs; its X block is identical to witness_plain.txt (6912 values). The official check ignores its Y block, so no reliance on it.
- Hash recorded is for the .gz files as shipped in the package; sha256 of the decompressed ONNX/vnnlib is not recorded. Minor.
- The enumerated criterion has no partial win that fits; this is a claim of the full criterion.

## Verdict
The mechanical content of (b), (c), (d) is genuinely confirmed by my own runs, and (a) holds on the cached results.txt copy. But (a) is required live (re-fetch immediately before claiming, plus the check.json sub-clause over tool directories) and (e) requires a live web search; neither can be established from the package, and the criterion says ALL clauses must hold with default false. These block a pass.

confirmed_scope: For the traffic_signs_recognition_2023 instance model_48_idx_6371_eps_3.00000 (ONNX and 2.0 vnnlib as packaged), the 6912-value input in witness_plain.txt lies strictly inside every vnnlib bound, is exact in float32, makes Y[0,9]-Y[0,17] = 0.7615941 under onnxruntime CPU float32 and the onnx reference evaluator, and the unmodified packaged SCORING/counterexamples_v2.py returns 'correct' at abs_tol 0.0 and 1e-4; the instance shows timeout, timeout, timeout in the packaged results.txt copy fetched 2026-10-15T00:28:04Z; live freshness, check.json absence, and non-prior-publication were not verified.
context: subagent (same VM)
pass: false
