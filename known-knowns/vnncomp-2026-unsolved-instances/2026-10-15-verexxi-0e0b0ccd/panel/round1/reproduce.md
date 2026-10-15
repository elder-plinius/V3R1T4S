# REPRODUCE skeptic verdict: panel-claim-m48-6371-e3

Read only inside the claim folder; own scripts and scratch were kept in a separate work folder. run_official.py was
read only after my own checker (written from the definition) had produced its result.

## Definition checked against (quoted from CLAIM.md, bank success criterion)
"(b) every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the
ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file
evaluates to true exactly as written under VNN-COMP semantics (i.e. the official validator's zero-tolerance check
`_assertions_hold(query, assignment, 0.0, 0.0)` is satisfied), and on the satisfied branch of each output assertion every
atomic comparison holds with a strict margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds
after rounding the input to float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or
onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified ...) returns
'correct' (not merely 'correct_up_to_tolerance')"
Claim sentence: Y[0,9] - Y[0,17] >= 1e-6 so the disjunct (>= Y[0,9] Y[0,17]) holds, for the 2.0 files.

## SHA256SUMS
`sha256sum -c SHA256SUMS`: all 22 entries OK (0 non-OK), checked before and again after running the validator.
Both ONNX copies (1.0 and 2.0) have the same sha256 (6f4969db...); the vnnlib copies differ (1.0: flat X_i; 2.0: X[0,h,w,c]).

## My own checker (independent parse; exact Fraction arithmetic; no vnnlib library)
Parsed benchmark/2.0 vnnlib.gz line by line, rejecting any unrecognised line. Output (copied):
- witness values 6912 (one per line, trailing newline)
- all decimals exactly equal to their float32 value: True
- witness_v2 header ['sat', 'X float32 [1, 48, 48, 3]'], X block identical to witness_plain: True
- lo 6912 hi 6912 disjuncts 42 (one per c != 17, each `(and (>= Y[0,c] Y[0,17]))`; no duplicate or missing coordinate)
- strict violations 0; min distance of any coordinate to a bound = 1/512 = 0.001953125 (exact)
- onnxruntime CPU float32: Y9 = 0.8807970285415649, Y17 = 0.11920291185379028, argmax 9; only true disjunct is c=9,
  Y9 - Y17 = 0.7615941166877747 (>= 1e-6); output shape (1,43) float32, sums to 1 (softmax)
- onnx.reference.ReferenceEvaluator float32: Y9 = 0.8807970285415649, Y17 = 0.11920291930437088, argmax 9;
  Y9 - Y17 = 0.7615941092371941 (>= 1e-6); max |ort - ref| = 7.45e-09
- ort re-run with 5 fresh sessions: bitwise identical output each time (deterministic)
- FAILS: [] ; MYCHECK PASS
Extra: 1.0 vnnlib (flat X_0..X_6911) has 6912 lo / 6912 hi, bounds identical to the 2.0 bounds in (h,w,c) row-major order,
and 0 strict violations by the same witness.

## Official validator (unmodified, run as REPRODUCE.md says, `python run_official.py 2.0`)
version 2.0 abs_tol=0.0: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
version 2.0 abs_tol=0.0001: ('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')
(`run_official.py 1.0` gives 'unsupported', parse error at line 4; as REPRODUCE.md says, the validator only parses VNN-LIB 2.0.)
Official result matches my checker: both say the witness is a valid counterexample.

## Table facts visible in the package (not live-refetched by me)
table_record/results.txt (fetch status 200, fetched 2026-10-15T00:28:04Z) has the Row for this instance with cells
['timeout','timeout','timeout']; the three tools' results.csv rows are timeout / run_instance_timeout / timeout; alpha_beta_crown and
pyrat name 1.0, vibecheck names 2.0, as the claim says.

## Not verified by me (outside what the saved files can show)
Live re-fetch of the table, absence of *.counterexample.check.json in the tool directories, and the web search for prior
published counterexamples (criteria a and e) are not reproducible from the claim folder; this verdict covers the
numerical/validity claim (criteria b, c) only. No mismatch, missing object or non-determinism found.

context: subagent (same VM)
pass: true
