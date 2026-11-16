# How We Found It

_Note: contributor text, unverified._

During our live status audit of `google-deepmind/formal-conjectures` (`main` commit `e028240a6182`), we observed that `ramsey_number_five_five_lower_bound` (`R(5,5) >= 43`) had just received an upstream `formal_proof` link in PR `#7998`, whereas `RamseyNumbers.ramsey_number_six_six_lower_bound` (`R(6,6) >= 102`) remained an unclaimed `sorry` with zero open PRs.

Direct enumeration of all `C(101, 6) = 1,265,904,540` 6-subsets on `Fin 101` is far too large for Lean's kernel `decide` without `native_decide` (which is forbidden). Instead, we exploited the full algebraic symmetry of the 101-vertex Paley graph `P(101)` inside Lean 4:
1. Multiplication by the quadratic nonresidue `2` mod `101` yields an explicit graph isomorphism `P(101) ≃g P(101)ᶜ`, reducing `(P(101)ᶜ).CliqueFree 6` to `P(101).CliqueFree 6`.
2. Affine transformations `w ↦ (v₁ - v₀)⁻¹ (w - v₀)` on `ZMod 101` act transitively on adjacent pairs, mapping any hypothetical 6-clique to one containing `0` and `1` and reducing the search to 4-clique-freeness on their 24 common neighbors (`794` adjacency checks).
3. Encoding the branch-and-bound checker with pure structural recursion on `Nat` and `List` (avoiding `WellFounded.fix`) allowed Lean's kernel to discharge the finite check via `decide` in under a second using only `[propext, Classical.choice, Quot.sound]`.
