import Physlib
import V3R1T4SSpec

/-!
# Candidate proof of `V3R1T4S.spec` (physlib-gut-kernel-z6), kernel-first (direct) lens

For `x = (h, g, α) : SU(3) × SU(2) × U(1)` let `a = (α : ℂ)`. The frozen spec asks for a group
homomorphism `f : StandardModel.GaugeGroupI →* SU(5)` with `f x = blockdiag (a ^ 3 • g, a⁻¹ ^ 2 • h)`
(the matrix `V3R1T4S.inclSMMatrix x`) and `f.ker = StandardModel.gaugeGroupℤ₆SubGroup`.

* `inclSMMatrix_mem`: the matrix is unitary (block-wise, using `|a| = 1`) with determinant
  `(a ^ 3) ^ 2 * (a⁻¹ ^ 2) ^ 3 = 1`.
* `inclSMMatrix_one`, `inclSMMatrix_mul`: it is multiplicative (scalars commute with matrices).
* `inclSMHom`: the homomorphism, whose underlying matrix is `inclSMMatrix x` by definition.
* `inclSMMatrix_eq_one_iff`: `inclSMMatrix x = 1 ↔ a ^ 3 • g = 1 ∧ a⁻¹ ^ 2 • h = 1`.
* `ker_eq`: `⊆` takes determinants of `a ^ 3 • g = 1` to get `a ^ 6 = 1`, builds the sixth root of
  unity `rootsOfUnity.mkOfPowEq a`, and matches `gaugeGroupℤ₆OfRoot` componentwise; `⊇` evaluates the
  two blocks at `gaugeGroupℤ₆OfRoot ρ = (ρ ^ 2 • 1, (star ρ) ^ 3 • 1, ρ)`.
-/

open Matrix

namespace V3R1T4S.KF

lemma scal_mul_star (u : unitary ℂ) : (u : ℂ) * star (u : ℂ) = 1 := Unitary.coe_mul_star_self u

lemma scal_star_mul (u : unitary ℂ) : star (u : ℂ) * (u : ℂ) = 1 := Unitary.coe_star_mul_self u

lemma scal_ne_zero (u : unitary ℂ) : (u : ℂ) ≠ 0 := by
  intro h
  have := Unitary.coe_mul_star_self u
  rw [h, zero_mul] at this
  exact zero_ne_one this

lemma scal_inv (u : unitary ℂ) : (u : ℂ)⁻¹ = star (u : ℂ) :=
  inv_eq_of_mul_eq_one_right (Unitary.coe_mul_star_self u)

/-- `blockdiag (α ^ 3 g, α ^ (-2) h)` lies in `SU(5)`. -/
lemma inclSMMatrix_mem (x : StandardModel.GaugeGroupI) :
    inclSMMatrix x ∈ Matrix.specialUnitaryGroup (Fin 5) ℂ := by
  have hg := (Matrix.mem_specialUnitaryGroup_iff.mp x.2.1.2)
  have hh := (Matrix.mem_specialUnitaryGroup_iff.mp x.1.2)
  have hgu := Matrix.mem_unitaryGroup_iff.mp hg.1
  have hhu := Matrix.mem_unitaryGroup_iff.mp hh.1
  have ha := scal_ne_zero x.2.2
  rw [Matrix.mem_specialUnitaryGroup_iff, Matrix.mem_unitaryGroup_iff]
  constructor
  · simp only [inclSMMatrix, reindex_apply, star_eq_conjTranspose, conjTranspose_submatrix,
      submatrix_mul_equiv, fromBlocks_conjTranspose, fromBlocks_multiply, conjTranspose_smul,
      conjTranspose_zero, Matrix.mul_zero, Matrix.zero_mul, add_zero, zero_add]
    rw [star_eq_conjTranspose] at hgu hhu
    rw [smul_mul_smul_comm, smul_mul_smul_comm, hgu, hhu, scal_inv, star_pow, star_pow, star_star,
      ← mul_pow, ← mul_pow, scal_mul_star, scal_star_mul, one_pow, one_pow, one_smul, one_smul,
      fromBlocks_one, submatrix_one_equiv]
  · simp only [inclSMMatrix]
    rw [det_reindex_self, det_fromBlocks_zero₂₁, det_smul, det_smul, hg.2, hh.2]
    simp only [Fintype.card_fin, mul_one]
    field_simp

lemma inclSMMatrix_one : inclSMMatrix 1 = 1 := by
  simp [inclSMMatrix]

lemma inclSMMatrix_mul (x y : StandardModel.GaugeGroupI) :
    inclSMMatrix (x * y) = inclSMMatrix x * inclSMMatrix y := by
  simp only [inclSMMatrix, reindex_apply, submatrix_mul_equiv, fromBlocks_multiply,
    Matrix.mul_zero, Matrix.zero_mul, add_zero, zero_add, Prod.fst_mul, Prod.snd_mul,
    Submonoid.coe_mul, smul_mul_smul_comm, mul_pow, mul_inv]

/-- The homomorphism `inclSM : SU(3) × SU(2) × U(1) → SU(5)`, `(h, g, α) ↦ blockdiag (α ^ 3 g, α ^ (-2) h)`. -/
noncomputable def inclSMHom : StandardModel.GaugeGroupI →* GaugeGroupGG where
  toFun x := ⟨inclSMMatrix x, inclSMMatrix_mem x⟩
  map_one' := Subtype.ext inclSMMatrix_one
  map_mul' x y := Subtype.ext (inclSMMatrix_mul x y)

lemma inclSMHom_coe (x : StandardModel.GaugeGroupI) :
    (inclSMHom x : Matrix (Fin 5) (Fin 5) ℂ) = inclSMMatrix x := rfl

lemma inclSMMatrix_eq_one_iff (x : StandardModel.GaugeGroupI) :
    inclSMMatrix x = 1 ↔
      ((x.2.2 : ℂ) ^ 3) • (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧
      ((x.2.2 : ℂ)⁻¹ ^ 2) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 := by
  constructor
  · intro h
    rw [inclSMMatrix, ← Equiv.eq_symm_apply, reindex_symm, reindex_apply,
      Equiv.symm_symm, submatrix_one_equiv, ← fromBlocks_one, fromBlocks_inj] at h
    exact ⟨h.1, h.2.2.2⟩
  · rintro ⟨h1, h2⟩
    simp only [inclSMMatrix, h1, h2, fromBlocks_one, reindex_apply, submatrix_one_equiv]

/-- The kernel of `inclSMHom` is `StandardModel.gaugeGroupℤ₆SubGroup`. -/
lemma ker_eq : inclSMHom.ker = StandardModel.gaugeGroupℤ₆SubGroup := by
  ext x
  rw [MonoidHom.mem_ker, StandardModel.mem_gaugeGroupℤ₆SubGroup_iff]
  have hcoe : inclSMHom x = 1 ↔ inclSMMatrix x = 1 := by
    rw [← inclSMHom_coe]
    exact Subtype.ext_iff
  rw [hcoe, inclSMMatrix_eq_one_iff]
  constructor
  · rintro ⟨h1, h2⟩
    have hg := (Matrix.mem_specialUnitaryGroup_iff.mp x.2.1.2).2
    have h6 : (x.2.2 : ℂ) ^ 6 = 1 := by
      have := congrArg Matrix.det h1
      rw [det_smul, hg, det_one, Fintype.card_fin, mul_one, ← pow_mul] at this
      exact this
    refine ⟨rootsOfUnity.mkOfPowEq (x.2.2 : ℂ) h6, ?_⟩
    have ha := scal_ne_zero x.2.2
    apply StandardModel.GaugeGroupI.ext
    · apply Subtype.ext
      change (StandardModel.gaugeGroupℤ₆SU3OfRoot _).1 = (x.1 : Matrix (Fin 3) (Fin 3) ℂ)
      rw [StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id, rootsOfUnity.coe_mkOfPowEq]
      have := congrArg (fun M => ((x.2.2 : ℂ) ^ 2) • M) h2
      simp only [smul_smul] at this
      rw [inv_pow, mul_inv_cancel₀ (pow_ne_zero _ ha), one_smul] at this
      exact this.symm
    · apply Subtype.ext
      change (StandardModel.gaugeGroupℤ₆SU2OfRoot _).1 = (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ)
      rw [StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id, rootsOfUnity.coe_mkOfPowEq]
      have := congrArg (fun M => (star (x.2.2 : ℂ) ^ 3) • M) h1
      simp only [smul_smul] at this
      rw [← mul_pow, scal_star_mul, one_pow, one_smul] at this
      exact this.symm
    · apply Subtype.ext
      change ((rootsOfUnity.mkOfPowEq (x.2.2 : ℂ) h6 : ℂˣ) : ℂ) = (x.2.2 : ℂ)
      rw [rootsOfUnity.coe_mkOfPowEq]
  · rintro ⟨ρ, rfl⟩
    have hu : ((StandardModel.gaugeGroupℤ₆OfRoot ρ).2.2 : ℂ) = ((ρ : ℂˣ) : ℂ) := rfl
    have ha := scal_ne_zero (StandardModel.gaugeGroupℤ₆OfRoot ρ).2.2
    have hms := scal_mul_star (StandardModel.gaugeGroupℤ₆OfRoot ρ).2.2
    rw [hu] at ha hms
    refine ⟨?_, ?_⟩
    · change (((ρ : ℂˣ) : ℂ) ^ 3) • (StandardModel.gaugeGroupℤ₆SU2OfRoot ρ).1 = 1
      rw [StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id, smul_smul, ← mul_pow, hms, one_pow,
        one_smul]
    · change (((ρ : ℂˣ) : ℂ)⁻¹ ^ 2) • (StandardModel.gaugeGroupℤ₆SU3OfRoot ρ).1 = 1
      rw [StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id, smul_smul, ← mul_pow, inv_mul_cancel₀ ha,
        one_pow, one_smul]

end V3R1T4S.KF

theorem V3R1T4S.claim : V3R1T4S.spec :=
  ⟨V3R1T4S.KF.inclSMHom, fun _ => rfl, V3R1T4S.KF.ker_eq⟩
