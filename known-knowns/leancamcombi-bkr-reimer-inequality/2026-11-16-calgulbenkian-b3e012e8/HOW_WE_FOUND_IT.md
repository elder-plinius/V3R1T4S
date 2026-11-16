# How We Found It

_Note: contributor text, unverified._

To formalize David Reimer's general 2000 inequality `2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ` cleanly inside `CamCombi/PlainCombi/VanDenBergKesten.lean` without altering its three lightweight `public import` lines or pulling in heavy real vector-space / matrix-rank machinery, we recast the Borgs–Chayes–Randall orthogonality proof of Reimer's Butterfly Lemma purely over `ℤ` (`Finset β → ℤ`) inside a `private` auxiliary section:
1. Defining explicit `{-1, 0, 1}`-valued functions `vecUR`, `vecUY`, and `vecVB` allowed all three cross-block orthogonality identities to be discharged directly via coordinate-flip involutions (`toggle a t` and `Finset.sum_involution`).
2. Strict positive-definiteness of the integer dot product `zdot f f = ∑ t, f t * f t` split any `ℤ`-linear dependence on `W ⊕ S₁ ⊕ S₂` into three separate block equations.
3. Within the butterfly block `W`, observing `zdot (vecVB w b) (vecUR w) % 2 = 1` while `¬(w ⊆ u) → zdot (vecVB w b) (vecUR u) % 2 = 0` gave an elementary mod-2 parity descent on minimal odd-coefficient support, which combined with fraction-free integer Gaussian elimination (`int_lin_indep_card_le`) proved `#W ≤ #(R ∩ Y')` and, via subcube fiber bijections (`Finset.card_bij`), concluded `Finset.card_certificator_le`.
