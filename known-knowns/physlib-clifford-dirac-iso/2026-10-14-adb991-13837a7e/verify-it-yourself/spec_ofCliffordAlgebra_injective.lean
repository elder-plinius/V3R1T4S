import Physlib

/-! Frozen statement for physlib-clifford-dirac-iso: Physlib's TODO "Prove injectivity of ofCliffordAlgebra and
construct the full isomorphism." (Physlib/Relativity/CliffordAlgebra.lean, line 40 of the status page fetched
2026-10-14T06:16:28Z). `spaceTime.γ.ofCliffordAlgebra : CliffordAlgebra diracForm →ₐ[ℝ] diracAlgebra` is already
proved surjective in Physlib (`ofCliffordAlgebra_surjective`); the claim is that it is injective, hence an algebra
isomorphism. -/
def V3R1T4S.spec : Prop := Function.Injective spaceTime.γ.ofCliffordAlgebra
