# Honesty gate: physlib-clifford-dirac-iso (run 2026-10-14-0615)

status: CONFIRMED_SOLUTION
confirmed_scope: Against Physlib commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean 4 v4.34.1), object/OfCliffordAlgebraInjective.lean is a kernel-checked, sorry-free proof, depending only on propext, Classical.choice and Quot.sound, of the frozen statement `Function.Injective spaceTime.γ.ofCliffordAlgebra` for Physlib's own unmodified `ofCliffordAlgebra : CliffordAlgebra diracForm →ₐ[ℝ] diracAlgebra`, from which, with Physlib's `ofCliffordAlgebra_surjective`, the ℝ-algebra isomorphism `CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra` follows by a one-line `AlgEquiv.ofBijective` that the panel compiled separately with the same three axioms and that the object itself does not state.

Read by the run's main session at 2026-10-14T07:34Z: reproduce.md, novelty.md and criterion.md, each from a fresh
subagent context that saw only claim/, each ending `pass: true`.

Downgrade checks (kit/RUN.md step 7), none triggered:
- Hedging: none. NOVELTY limits its verdict to novelty and notes that the mathematics is textbook; the scope below
  claims only the formal proof.
- Reproduction: REPRODUCE wrote its own statements before opening the object, derived them from `V3R1T4S.claim`
  (including the full `AlgEquiv`, built in one line with Physlib's surjectivity), ran the checker twice with
  identical output (PASS), replayed the module with leanchecker, walked the axioms independently of `#print axioms`,
  and confirmed dim_ℝ diracAlgebra = 16 with exact rational arithmetic.
- Strictly better than the live record: the status page (fetched again by NOVELTY at 2026-10-14T07:00:56Z, HTTP 200,
  same sha256 70ca93d773d8a8f2c2fe43e607125ae1d3042d7530bace4371cd5eba5bf8de0d) still has the TODO, and Physlib's
  Dirac API map lists the isomorphism as `done: false`; no proof in any of the 1731 upstream refs scanned, in the
  inspected forks, in Mathlib or in the literature searched. The fetch is less than 6 hours old.
- Stretched criterion or hidden quantifier: the frozen statement is a closed proposition about Physlib's own map;
  CRITERION's negative control (Physlib's surjectivity renamed as the claim) is rejected by the checker.
- Scope: the confirmed_scope sentence above is CRITERION's, verbatim. It covers injectivity, and says that the
  isomorphism is a one-line corollary the panel compiled, not a declaration of the object.
- One object, one statement; no sampling; no evasion.

Process notes (not affecting the result): REPRODUCE's `leanchecker --help` call replayed all of Physlib and reached
8.3 GB inside a Lean slot before the skeptic killed its own processes; all three noted that CLAIM.md names the
source copy's folder as data/ on one line while it is in source/ (same sha256).
