import Physlib
import Mathlib.LinearAlgebra.ExteriorAlgebra.Basis
import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction

/-! Sorry-free intermediate lemmas (kernel-first lens), part 1:
`finrank ℝ (CliffordAlgebra diracForm) = 16` and the reduction of injectivity to `16 ≤ finrank ℝ diracAlgebra`. -/

open spaceTime spaceTime.γ Fermion.Dirac

namespace KF

/-- A basis of the Clifford algebra indexed by `Finset (Fin 4)`, from the exterior algebra. -/
noncomputable def clBasis : Module.Basis (Finset (Fin 4)) ℝ (CliffordAlgebra diracForm) :=
  (Pi.basisFun ℝ (Fin 4)).ExteriorAlgebra.map (CliffordAlgebra.equivExterior diracForm).symm

theorem finrank_cl : Module.finrank ℝ (CliffordAlgebra diracForm) = 16 := by
  rw [Module.finrank_eq_card_basis clBasis, Fintype.card_finset, Fintype.card_fin]; rfl

theorem finite_cl : Module.Finite ℝ (CliffordAlgebra diracForm) := Module.Finite.of_basis clBasis

/-- The dimension count: a lower bound `16 ≤ finrank ℝ diracAlgebra` suffices for injectivity. -/
theorem glue (h16 : 16 ≤ Module.finrank ℝ diracAlgebra) : Function.Injective ofCliffordAlgebra := by
  haveI : Module.Finite ℝ (CliffordAlgebra diracForm) := Module.Finite.of_basis clBasis
  have hsurj : Function.Surjective ofCliffordAlgebra.toLinearMap := ofCliffordAlgebra_surjective
  have hle := LinearMap.finrank_le_finrank_of_surjective hsurj
  have heq : Module.finrank ℝ (CliffordAlgebra diracForm) = Module.finrank ℝ diracAlgebra := by
    rw [finrank_cl] at hle ⊢; omega
  exact (LinearMap.injective_iff_surjective_of_finrank_eq_finrank heq).mpr hsurj

/-- Upper bound for the Dirac algebra from Physlib's surjectivity alone. -/
theorem finrank_dirac_le : Module.finrank ℝ diracAlgebra ≤ 16 := by
  haveI : Module.Finite ℝ (CliffordAlgebra diracForm) := Module.Finite.of_basis clBasis
  have hsurj : Function.Surjective ofCliffordAlgebra.toLinearMap := ofCliffordAlgebra_surjective
  have hle := LinearMap.finrank_le_finrank_of_surjective hsurj
  rw [finrank_cl] at hle; exact hle

end KF

#print axioms KF.finrank_cl
#print axioms KF.finite_cl
#print axioms KF.glue
#print axioms KF.finrank_dirac_le
