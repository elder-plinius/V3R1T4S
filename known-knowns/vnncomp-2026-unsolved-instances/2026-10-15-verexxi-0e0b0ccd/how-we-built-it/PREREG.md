# PREREG (written 2026-10-14T20:06:02Z, before any attack output was scored)

criterion: the bank success criterion copied verbatim in target.md, judged per instance (one instance per claim).
statistic: for a candidate d vector, the exact integer logit lead G = max_{c != t} L_c - L_t of the validated
  exact model (bnn4864.py); a candidate is submitted to the checks only when G >= 2.
checks that decide a claim (all required):
  1. unmodified SCORING/counterexamples_v2.py (live results repo, sha256 5ab7a4df...) validate_vnnlib2_counterexample
     with abs_tol = 0.0 returns 'correct' on the VNN-LIB 2.0 witness file;
  2. every input coordinate strictly inside its vnnlib bounds (lo < x < hi) and exact in float32;
  3. on the satisfied disjunct, Y[c] - Y[t] >= 1e-6 in onnxruntime CPU float32;
  4. the same in onnx.reference.ReferenceEvaluator (second runtime, not onnxruntime);
  5. the live SCORING/results.txt row re-fetched right before claiming has no '(h)'/'(v)';
  6. a web search finds no published counterexample for the same ONNX+vnnlib pair.
thresholds: G >= 2 (ties and G = 0 do not count); output margin >= 1e-6; input strictness at zero tolerance.
null_test: not needed because the claim is an explicit witness checked by the official deterministic validator
