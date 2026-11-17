# PREREG: erdos-677-lcm-blocks, run 2026-10-24-0818

Frozen at: 2026-10-24T08:24:04Z (date -u), before any attack program of this run was started.

## Criterion (verbatim, from target.md)

Success = a kernel-checked proof of `Erdos677.erdos_677` ("∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠
lcmInterval n k") or of its negation (a counterexample). Partial wins (workspace only, not prize solutions): an
exhaustive, uncapped verification of the statement for a stated range of (n, k) with a checkable certificate; a
machine-checked proof for a fixed small k.

## Planned claim (at most one claim goes to the panel tonight)

C-R2: "For every k with 1 ≤ k ≤ K*, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k, M(m,k) ≠ M(n,k)", where K* is
the largest k for which every step below completes tonight for all of 3..K*. If K* < 23 the claim is not made.

## The judge (all must hold, all computed in this run, after this file's timestamp)

1. k ≤ 2: Lemma A (R(k) = 1), written out in the claim's proof file.
2. Small X: an exhaustive window search complete in m (Lemma A) for every 3 ≤ k ≤ K* and n + k ≤ N_small with
   N_small ≥ 10^6 + K* (so it covers every X = n + (k+1)/2 < 10^6), every candidate pair then judged by exact
   integer lcm comparison: 0 counterexamples.
3. Margin: for every admissible r of every k ≤ K* and every real X ≥ 10^6, c(1−η) < X(ρX − Y(X)) < c(1+η) with
   η = 10^−3, established by a check whose arithmetic is rigorous (exact rationals, or interval arithmetic with
   outward rounding): 0 failures. A float-only margin makes the claim NUMERICAL and it is not panelled as a proof.
4. Enumeration: deep_rig with QMAX = 10^495 and enough digits that the continued-fraction safety check never fires
   prints a TOTAL line with product_solutions = 0 for every k ≤ K*.
5. Every candidate that passes a filter is judged by exact integer arithmetic; checker/check677.py is the reference
   judge for any reported triple.

A counterexample, if one appears, is judged by checker/check677.py (PASS) and checker/lean_claim_check.py with
checker/spec_677_negation.lean (PASS).

Lens results not in C-R2 (an R1 extension past 10^8, cross-checks) are reported as lens results, not claims.

null_test: not needed because the claim is an exhaustive deterministic verification judged by exact arithmetic (and a
counterexample would be an explicit triple judged by exact arithmetic and the Lean kernel); no statistical or
search-score claim is made.
