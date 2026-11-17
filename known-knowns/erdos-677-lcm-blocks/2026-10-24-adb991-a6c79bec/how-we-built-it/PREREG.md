# PREREG: erdos-677-lcm-blocks

Frozen at: 2026-10-15T07:28:24Z (date -u), before any attack program was run.

## Criterion (verbatim, from target.md)

Success = a kernel-checked proof of `Erdos677.erdos_677` ("∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠
lcmInterval n k") or of its negation (a counterexample). Partial wins (workspace only, not prize solutions): an
exhaustive, uncapped verification of the statement for a stated range of (n, k) with a checkable certificate; a
machine-checked proof for a fixed small k.

## The judge

1. `checker/lean_claim_check.py` with `checker/spec_677_negation.lean` (counterexample) or `checker/spec_677.lean`
   (proof) prints PASS: clean compile, no sorry/axiom/native_decide, axioms ⊆ {propext, Classical.choice, Quot.sound}.
2. For a counterexample, `checker/check677.py N M K` must also print PASS (exact integers).
3. A range verification counts only if every (n, k) in the stated range is covered with no cap on m (the candidate
   m's must be provably complete, e.g. via a Størmer/Lehmer argument), with the certificate saved.

null_test: not needed because every claim here is an explicit triple or a proof judged by exact arithmetic and the
Lean kernel; no statistical or search-score claim is made.
