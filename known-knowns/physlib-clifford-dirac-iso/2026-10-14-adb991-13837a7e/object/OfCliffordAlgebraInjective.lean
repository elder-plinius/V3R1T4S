import Physlib
import Mathlib.LinearAlgebra.ExteriorAlgebra.Basis
import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction
import V3R1T4SSpec

/-!
# Injectivity of `spaceTime.γ.ofCliffordAlgebra` by a dimension count (V3R1T4S, lens kernel-first)

* `finrank ℝ (CliffordAlgebra diracForm) = 16`: Mathlib's basis of the exterior algebra indexed by `Finset (Fin 4)`
  transported along `CliffordAlgebra.equivExterior` (2 is invertible in ℝ).
* `16 ≤ finrank ℝ diracAlgebra`: the images of the 16 ordered Clifford monomials are ℝ-linearly independent; this is
  checked after the ℝ-linear (indeed multiplicative) change of coordinates `toChiral`, which sends the Dirac-basis
  gamma matrices to Physlib's explicit chiral-basis matrices `Fermion.Dirac.gamma_toMatrix`, by reading off eight
  matrix entries (real and imaginary parts).
* Physlib's `ofCliffordAlgebra_surjective` gives `finrank diracAlgebra ≤ 16`, so the ranks agree and a surjective
  linear map between spaces of equal finite dimension is injective.
-/

open spaceTime spaceTime.γ Fermion.Dirac

namespace KF

/-! ## The Clifford algebra has dimension 16 -/

/-- A basis of the Clifford algebra indexed by `Finset (Fin 4)`, from the exterior algebra. -/
noncomputable def clBasis : Module.Basis (Finset (Fin 4)) ℝ (CliffordAlgebra diracForm) :=
  (Pi.basisFun ℝ (Fin 4)).ExteriorAlgebra.map (CliffordAlgebra.equivExterior diracForm).symm

theorem finrank_cl : Module.finrank ℝ (CliffordAlgebra diracForm) = 16 := by
  rw [Module.finrank_eq_card_basis clBasis, Fintype.card_finset, Fintype.card_fin]; rfl

/-- The dimension count: a lower bound `16 ≤ finrank ℝ diracAlgebra` suffices for injectivity. -/
theorem glue (h16 : 16 ≤ Module.finrank ℝ diracAlgebra) : Function.Injective ofCliffordAlgebra := by
  haveI : Module.Finite ℝ (CliffordAlgebra diracForm) := Module.Finite.of_basis clBasis
  have hsurj : Function.Surjective ofCliffordAlgebra.toLinearMap := ofCliffordAlgebra_surjective
  have hle := LinearMap.finrank_le_finrank_of_surjective hsurj
  have heq : Module.finrank ℝ (CliffordAlgebra diracForm) = Module.finrank ℝ diracAlgebra := by
    rw [finrank_cl] at hle ⊢; omega
  exact (LinearMap.injective_iff_surjective_of_finrank_eq_finrank heq).mpr hsurj

/-! ## Sixteen independent elements of `diracAlgebra` -/

/-- Dirac coordinates back to Physlib's chiral coordinates (an algebra automorphism of the matrices). -/
noncomputable def toChiral : Matrix (Fin 4) (Fin 4) ℂ ≃ₐ[ℂ] Matrix (Fin 4) (Fin 4) ℂ :=
  endEquivMatrix.symm.trans (LinearMap.toMatrixAlgEquiv chiralBasis)

theorem toChiral_gamma (μ : Fin 1 ⊕ Fin 3) :
    toChiral (endEquivMatrix (gamma μ)) = LinearMap.toMatrix chiralBasis chiralBasis (gamma μ) := by
  simp [toChiral, LinearMap.toMatrixAlgEquiv]

/-- Physlib's chiral gamma matrices (`Fermion.Dirac.gamma_toMatrix`), indexed by `Fin 4`. -/
def C : Fin 4 → Matrix (Fin 4) (Fin 4) ℂ := ![
  !![0, 0, 1, 0; 0, 0, 0, 1; 1, 0, 0, 0; 0, 1, 0, 0],
  !![0, 0, 0, 1; 0, 0, 1, 0; 0, -1, 0, 0; -1, 0, 0, 0],
  !![0, 0, 0, -Complex.I; 0, 0, Complex.I, 0; 0, Complex.I, 0, 0; -Complex.I, 0, 0, 0],
  !![0, 0, 1, 0; 0, 0, 0, -1; -1, 0, 0, 0; 0, 1, 0, 0]]

/-- The Clifford generators. -/
noncomputable def e (i : Fin 4) : CliffordAlgebra diracForm := CliffordAlgebra.ι diracForm (Pi.single i 1)

theorem fse0 : (finSumFinEquiv.symm (0 : Fin 4) : Fin 1 ⊕ Fin 3) = Sum.inl 0 := rfl
theorem fse1 : (finSumFinEquiv.symm (1 : Fin 4) : Fin 1 ⊕ Fin 3) = Sum.inr 0 := rfl
theorem fse2 : (finSumFinEquiv.symm (2 : Fin 4) : Fin 1 ⊕ Fin 3) = Sum.inr 1 := rfl
theorem fse3 : (finSumFinEquiv.symm (3 : Fin 4) : Fin 1 ⊕ Fin 3) = Sum.inr 2 := rfl

theorem toChiral_e (i : Fin 4) :
    toChiral ((ofCliffordAlgebra (e i) : diracAlgebra) : Matrix (Fin 4) (Fin 4) ℂ) = C i := by
  rw [e, ofCliffordAlgebra_ι_single, one_smul]
  change toChiral (endEquivMatrix (gamma (finSumFinEquiv.symm i))) = C i
  rw [toChiral_gamma]
  fin_cases i
  · rw [show ((⟨0, by decide⟩ : Fin 4)) = 0 from rfl, fse0, gamma_toMatrix]; rfl
  · rw [show ((⟨1, by decide⟩ : Fin 4)) = 1 from rfl, fse1, gamma_toMatrix]; rfl
  · rw [show ((⟨2, by decide⟩ : Fin 4)) = 2 from rfl, fse2, gamma_toMatrix]; rfl
  · rw [show ((⟨3, by decide⟩ : Fin 4)) = 3 from rfl, fse3, gamma_toMatrix]; rfl

/-- The 16 ordered Clifford monomials. -/
noncomputable def mon : Fin 16 → CliffordAlgebra diracForm := ![1, e 0, e 1, e 2, e 3,
  e 0 * e 1, e 0 * e 2, e 0 * e 3, e 1 * e 2, e 1 * e 3, e 2 * e 3,
  e 0 * e 1 * e 2, e 0 * e 1 * e 3, e 0 * e 2 * e 3, e 1 * e 2 * e 3, e 0 * e 1 * e 2 * e 3]

/-- Their images, as products of chiral matrices. -/
def W : Fin 16 → Matrix (Fin 4) (Fin 4) ℂ := ![1, C 0, C 1, C 2, C 3,
  C 0 * C 1, C 0 * C 2, C 0 * C 3, C 1 * C 2, C 1 * C 3, C 2 * C 3,
  C 0 * C 1 * C 2, C 0 * C 1 * C 3, C 0 * C 2 * C 3, C 1 * C 2 * C 3, C 0 * C 1 * C 2 * C 3]

/-- The ℝ-linear map `diracAlgebra → matrices`, `x ↦ toChiral x`. -/
noncomputable def Lmap : diracAlgebra →ₗ[ℝ] Matrix (Fin 4) (Fin 4) ℂ :=
  (toChiral.toLinearMap.restrictScalars ℝ).comp diracAlgebra.val.toLinearMap

theorem Lmap_apply (x : diracAlgebra) : Lmap x = toChiral (x : Matrix (Fin 4) (Fin 4) ℂ) := rfl

theorem Lmap_mon (k : Fin 16) : Lmap (ofCliffordAlgebra (mon k)) = W k := by
  rw [Lmap_apply]
  fin_cases k <;> simp [mon, W, map_mul, toChiral_e]

/-- The 16 chiral products are ℝ-linearly independent: eight entries (two per support pattern) suffice. -/
theorem linInd_W : LinearIndependent ℝ W := by
  rw [Fintype.linearIndependent_iff]
  intro g hg
  have h00 := congrFun (congrFun hg 0) 0
  have h11 := congrFun (congrFun hg 1) 1
  have h01 := congrFun (congrFun hg 0) 1
  have h10 := congrFun (congrFun hg 1) 0
  have h02 := congrFun (congrFun hg 0) 2
  have h20 := congrFun (congrFun hg 2) 0
  have h03 := congrFun (congrFun hg 0) 3
  have h12 := congrFun (congrFun hg 1) 2
  simp [W, C, Fin.sum_univ_succ, Matrix.mul_apply, Fin.sum_univ_four, Matrix.sum_apply,
    Complex.ext_iff, Matrix.cons_val_two, Matrix.cons_val_three] at h00 h11 h01 h10 h02 h20 h03 h12
  intro k
  fin_cases k <;> simp <;> linarith

theorem linInd_v : LinearIndependent ℝ (fun k => ofCliffordAlgebra (mon k)) := by
  apply LinearIndependent.of_comp Lmap
  have : (Lmap ∘ fun k => ofCliffordAlgebra (mon k)) = W := funext Lmap_mon
  rw [this]; exact linInd_W

theorem finrank_dirac_ge : 16 ≤ Module.finrank ℝ diracAlgebra := by
  simpa using linInd_v.fintype_card_le_finrank

theorem injective_ofCliffordAlgebra : Function.Injective ofCliffordAlgebra :=
  glue finrank_dirac_ge

end KF

theorem V3R1T4S.claim : V3R1T4S.spec := KF.injective_ofCliffordAlgebra
