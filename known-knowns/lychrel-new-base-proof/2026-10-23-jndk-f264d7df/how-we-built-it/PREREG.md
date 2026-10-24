# PREREG (frozen 2026-10-23T18:45:23Z, before any attack output exists)

Criterion: verbatim in target.md (bank success_criterion and partial wins p1, p2).

## Statistic / checker that judges a candidate
A candidate is (base b, seed x0, entry step t0, period p, growth g): the checker attempts/verifier/code/rle_check.py
(written from the definition in this run) does, with no other input:
1. simulates x0 exactly (integer digit lists) to x_{t0}, ..., x_{t0+2p}, checking no iterate before x_{t0+p} is a palindrome;
2. infers templates T_i(m) (i<p) from the run-length encodings of x_{t0+i} and x_{t0+p+i} (same digit sequence of runs
   required; slope = length difference; T_i(0) = x_{t0+i});
3. proves symbolically, for all m >= M0 (M0 computed from the orderings of affine boundaries), that
   RA(T_i(m)) = T_{i+1}(m) for i<p-1 and RA(T_{p-1}(m)) = T_0(m+1), with run lengths as affine functions of m;
4. checks every m < M0 by exact integer computation;
5. proves non-palindromicity of every T_i(m): symbolically for m >= M0 (run-digit sequence differs from its reverse),
   exactly for m < M0.
PASS only if all five hold. Thresholds: none (exact). The bank base condition: b not a power of 2 and not in {11,17,20,26}.

Calibration (must pass before any scoring): known positives = base 2 seed 22 (10110), Seal base 4/11/17/26 cycles
(data/seal_letter_mathpages.html); known negatives = single-digit mutations of each Seal cycle row (must FAIL).

null_test: not needed because any claim is an explicit object (start number plus templates) verified by a deterministic exact checker against the bank's literal criterion; exclusion results from the exterior automaton are exhaustive finite-graph computations, not statistical claims.

## Discovery procedures (not judges)
- orbit-lock hunter (attempts/orbit-lock): seeds and step caps declared in its NOTES.md before its job runs.
- exterior automaton (attempts/exterior-automaton): an exclusion is stated only for (base, period, overflow signature)
  cases whose finite reachability graph was fully explored without a cap.
