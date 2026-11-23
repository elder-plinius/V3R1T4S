# Pre-Registration: `leanapap-kelley-meka-integer-bound`

frozen_utc: 2026-11-16T16:24:36Z
target_id: leanapap-kelley-meka-integer-bound
upstream_commit: fb5cb9c4f594cbeeb160c715618d13640984c521
null_test: not needed because kernel-checked formal proof in Lean 4

## Verbatim Criterion & Gates

1. Prove `BohrSet.regularity` sorry-free in `APAP/Prereqs/Bohr/Regular.lean` with its statement unchanged (`p1`), prove the prime `ZMod q` `1/12` bound (`p2`), and prove the full corrected `theorem int` in `APAP/Integer.lean` with `open Finset Real` and exact statement:
   `∃ c > 0, ∃ C > 0, ∀ ⦃A : Finset ℕ⦄ ⦃N : ℕ⦄, A ⊆ range N → ThreeAPFree (α := ℕ) A → (#A : ℝ) ≤ C * N / exp (c * log N ^ (12⁻¹ : ℝ))`.
2. Zero `sorry`, `admit`, `axiom`, `native_decide`, or transitive import of `APAP.Prereqs.DummyPositivity`; `#print axioms int` must show only `{propext, Classical.choice, Quot.sound}`.
3. Full `lake build` across the entire `LeanAPAP` repository succeeds with exit status `0`.
