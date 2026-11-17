import Physlib

abbrev V3R1T4S.GaugeGroupPS : Type :=
  Matrix.specialUnitaryGroup (Fin 4) ℂ × Matrix.specialUnitaryGroup (Fin 2) ℂ ×
    Matrix.specialUnitaryGroup (Fin 2) ℂ

noncomputable def V3R1T4S.psMatrix4 (x : StandardModel.GaugeGroupI) : Matrix (Fin 4) (Fin 4) ℂ :=
  Matrix.reindex finSumFinEquiv finSumFinEquiv
    (Matrix.fromBlocks ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) 0 0
      (((x.2.2 : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)))

noncomputable def V3R1T4S.psMatrixR (x : StandardModel.GaugeGroupI) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![(x.2.2 : ℂ) ^ 3, (x.2.2 : ℂ)⁻¹ ^ 3]

def V3R1T4S.spec : Prop :=
  ∃ f : StandardModel.GaugeGroupI →* V3R1T4S.GaugeGroupPS,
    (∀ x, ((f x).1 : Matrix (Fin 4) (Fin 4) ℂ) = V3R1T4S.psMatrix4 x ∧
      ((f x).2.1 : Matrix (Fin 2) (Fin 2) ℂ) = (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
      ((f x).2.2 : Matrix (Fin 2) (Fin 2) ℂ) = V3R1T4S.psMatrixR x) ∧
    f.ker = StandardModel.gaugeGroupℤ₃SubGroup

namespace V3R1T4S.KF

/-! ### Scalars of modulus one -/

lemma coe_ne_zero (a : unitary ℂ) : (a : ℂ) ≠ 0 := by
  intro h
  have h1 := Unitary.coe_star_mul_self a
  rw [h, star_zero, zero_mul] at h1
  exact zero_ne_one h1

lemma star_coe (a : unitary ℂ) : star (a : ℂ) = (a : ℂ)⁻¹ :=
  eq_inv_of_mul_eq_one_left (Unitary.coe_star_mul_self a)

lemma star_pow3_mul (a : unitary ℂ) : star ((a : ℂ) ^ 3) * (a : ℂ) ^ 3 = 1 := by
  rw [star_pow, ← mul_pow, Unitary.coe_star_mul_self, one_pow]

lemma star_invpow3_mul (a : unitary ℂ) : star ((a : ℂ)⁻¹ ^ 3) * (a : ℂ)⁻¹ ^ 3 = 1 := by
  rw [star_pow, star_inv₀, star_coe, inv_inv, ← mul_pow, mul_inv_cancel₀ (coe_ne_zero a), one_pow]

/-! ### The 4×4 component -/

lemma blockA_unitary (x : StandardModel.GaugeGroupI) :
    star ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) *
      ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) = 1 := by
  have hh : star (x.1 : Matrix (Fin 3) (Fin 3) ℂ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.mp (Matrix.specialUnitaryGroup_le_unitaryGroup x.1.2)
  rw [star_smul, Matrix.smul_mul, Matrix.mul_smul, smul_smul, hh, Unitary.coe_star_mul_self, one_smul]

lemma blockD_unitary (a : unitary ℂ) :
    star (((a : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)) *
      (((a : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)) = 1 := by
  rw [star_smul, star_one, Matrix.smul_mul, Matrix.mul_smul, smul_smul, star_invpow3_mul,
    one_smul, Matrix.one_mul]

lemma reindex_one :
    Matrix.reindex finSumFinEquiv finSumFinEquiv
      (1 : Matrix (Fin 3 ⊕ Fin 1) (Fin 3 ⊕ Fin 1) ℂ) = 1 := by
  rw [Matrix.reindex_apply, Matrix.submatrix_one_equiv]

lemma psMatrix4_unitary (x : StandardModel.GaugeGroupI) :
    star (psMatrix4 x) * psMatrix4 x = 1 := by
  have hA := blockA_unitary x
  have hD := blockD_unitary x.2.2
  rw [Matrix.star_eq_conjTranspose] at hA hD
  rw [psMatrix4, Matrix.star_eq_conjTranspose, Matrix.conjTranspose_reindex, Matrix.reindex_apply,
    Matrix.reindex_apply, Matrix.submatrix_mul_equiv, Matrix.fromBlocks_conjTranspose,
    Matrix.fromBlocks_multiply]
  simp only [Matrix.conjTranspose_zero, Matrix.zero_mul, Matrix.mul_zero, add_zero, zero_add, hA, hD,
    Matrix.fromBlocks_one, Matrix.submatrix_one_equiv]

lemma psMatrix4_det (x : StandardModel.GaugeGroupI) : (psMatrix4 x).det = 1 := by
  have hdet : (x.1 : Matrix (Fin 3) (Fin 3) ℂ).det = 1 :=
    (Matrix.mem_specialUnitaryGroup_iff.mp x.1.2).2
  rw [psMatrix4, Matrix.det_reindex_self, Matrix.det_fromBlocks_zero₂₁, Matrix.det_smul,
    Matrix.det_smul, hdet, Matrix.det_one]
  simp only [Fintype.card_fin, pow_one, mul_one]
  rw [← mul_pow, mul_inv_cancel₀ (coe_ne_zero x.2.2), one_pow]

lemma psMatrix4_mem (x : StandardModel.GaugeGroupI) :
    psMatrix4 x ∈ Matrix.specialUnitaryGroup (Fin 4) ℂ :=
  Matrix.mem_specialUnitaryGroup_iff.mpr
    ⟨Matrix.mem_unitaryGroup_iff'.mpr (psMatrix4_unitary x), psMatrix4_det x⟩

lemma psMatrix4_mul (x y : StandardModel.GaugeGroupI) :
    psMatrix4 (x * y) = psMatrix4 x * psMatrix4 y := by
  have hu : ((x * y).2.2 : ℂ) = (x.2.2 : ℂ) * (y.2.2 : ℂ) := rfl
  have hm : ((x * y).1 : Matrix (Fin 3) (Fin 3) ℂ) =
      (x.1 : Matrix (Fin 3) (Fin 3) ℂ) * (y.1 : Matrix (Fin 3) (Fin 3) ℂ) := rfl
  rw [psMatrix4, psMatrix4, psMatrix4, Matrix.reindex_apply, Matrix.reindex_apply, Matrix.reindex_apply,
    Matrix.submatrix_mul_equiv, Matrix.fromBlocks_multiply]
  congr 1
  rw [Matrix.fromBlocks_inj]
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [hu, hm, Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.mul_zero, add_zero]
  · rw [Matrix.mul_zero, Matrix.zero_mul, add_zero]
  · rw [Matrix.mul_zero, Matrix.zero_mul, add_zero]
  · rw [hu, Matrix.zero_mul, zero_add, Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.one_mul,
      mul_inv, mul_pow]

/-! ### The right-handed 2×2 component -/

lemma psMatrixR_unitary (x : StandardModel.GaugeGroupI) :
    star (psMatrixR x) * psMatrixR x = 1 := by
  rw [psMatrixR, Matrix.star_eq_conjTranspose, Matrix.diagonal_conjTranspose,
    Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  funext i
  fin_cases i
  · exact star_pow3_mul x.2.2
  · exact star_invpow3_mul x.2.2

lemma psMatrixR_det (x : StandardModel.GaugeGroupI) : (psMatrixR x).det = 1 := by
  rw [psMatrixR, Matrix.det_diagonal, Fin.prod_univ_two]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [← mul_pow, mul_inv_cancel₀ (coe_ne_zero x.2.2), one_pow]

lemma psMatrixR_mem (x : StandardModel.GaugeGroupI) :
    psMatrixR x ∈ Matrix.specialUnitaryGroup (Fin 2) ℂ :=
  Matrix.mem_specialUnitaryGroup_iff.mpr
    ⟨Matrix.mem_unitaryGroup_iff'.mpr (psMatrixR_unitary x), psMatrixR_det x⟩

lemma psMatrixR_mul (x y : StandardModel.GaugeGroupI) :
    psMatrixR (x * y) = psMatrixR x * psMatrixR y := by
  rw [psMatrixR, psMatrixR, psMatrixR, Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i
  · show ((x.2.2 : ℂ) * (y.2.2 : ℂ)) ^ 3 = (x.2.2 : ℂ) ^ 3 * (y.2.2 : ℂ) ^ 3
    exact mul_pow _ _ 3
  · show ((x.2.2 : ℂ) * (y.2.2 : ℂ))⁻¹ ^ 3 = (x.2.2 : ℂ)⁻¹ ^ 3 * (y.2.2 : ℂ)⁻¹ ^ 3
    rw [mul_inv, mul_pow]

/-! ### The homomorphism -/

noncomputable def hom4 : StandardModel.GaugeGroupI →* Matrix.specialUnitaryGroup (Fin 4) ℂ :=
  MonoidHom.mk' (fun x => ⟨psMatrix4 x, psMatrix4_mem x⟩) (fun x y => Subtype.ext (psMatrix4_mul x y))

noncomputable def homR : StandardModel.GaugeGroupI →* Matrix.specialUnitaryGroup (Fin 2) ℂ :=
  MonoidHom.mk' (fun x => ⟨psMatrixR x, psMatrixR_mem x⟩) (fun x y => Subtype.ext (psMatrixR_mul x y))

noncomputable def inclSM : StandardModel.GaugeGroupI →* GaugeGroupPS :=
  hom4.prod (StandardModel.GaugeGroupI.toSU2.prod homR)

lemma inclSM_apply (x : StandardModel.GaugeGroupI) :
    ((inclSM x).1 : Matrix (Fin 4) (Fin 4) ℂ) = psMatrix4 x ∧
      ((inclSM x).2.1 : Matrix (Fin 2) (Fin 2) ℂ) = (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
      ((inclSM x).2.2 : Matrix (Fin 2) (Fin 2) ℂ) = psMatrixR x :=
  ⟨rfl, rfl, rfl⟩

/-! ### The kernel -/

lemma psMatrix4_eq_one_iff (x : StandardModel.GaugeGroupI) :
    psMatrix4 x = 1 ↔ (x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 ∧ (x.2.2 : ℂ)⁻¹ ^ 3 = 1 := by
  constructor
  · intro h
    have hb : Matrix.fromBlocks ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) 0 0
        (((x.2.2 : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)) = Matrix.fromBlocks 1 0 0 1 := by
      apply (Matrix.reindex finSumFinEquiv finSumFinEquiv).injective
      rw [Matrix.fromBlocks_one, reindex_one]
      exact h
    rw [Matrix.fromBlocks_inj] at hb
    refine ⟨hb.1, ?_⟩
    have hD := congrFun (congrFun hb.2.2.2 0) 0
    simpa using hD
  · rintro ⟨hA, hD⟩
    rw [psMatrix4, hA, hD, one_smul, Matrix.fromBlocks_one, reindex_one]

lemma psMatrixR_eq_one_iff (x : StandardModel.GaugeGroupI) :
    psMatrixR x = 1 ↔ (x.2.2 : ℂ) ^ 3 = 1 := by
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    rw [psMatrixR, Matrix.diagonal_apply_eq, Matrix.one_apply_eq] at h00
    exact h00
  · intro h3
    rw [psMatrixR, inv_pow, h3, inv_one, ← Matrix.diagonal_one]
    congr 1
    funext i
    fin_cases i <;> rfl

lemma inclSM_eq_one_iff (x : StandardModel.GaugeGroupI) :
    inclSM x = 1 ↔ (x.2.2 : ℂ) ^ 3 = 1 ∧ (x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 ∧
      (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 := by
  have e1 : inclSM x = 1 ↔ psMatrix4 x = 1 ∧ (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧
      psMatrixR x = 1 := by
    constructor
    · intro h
      exact ⟨congrArg (fun p : GaugeGroupPS => (p.1 : Matrix (Fin 4) (Fin 4) ℂ)) h,
        congrArg (fun p : GaugeGroupPS => (p.2.1 : Matrix (Fin 2) (Fin 2) ℂ)) h,
        congrArg (fun p : GaugeGroupPS => (p.2.2 : Matrix (Fin 2) (Fin 2) ℂ)) h⟩
    · rintro ⟨h4, h2, hR⟩
      exact Prod.ext (Subtype.ext h4) (Prod.ext (Subtype.ext h2) (Subtype.ext hR))
  rw [e1, psMatrix4_eq_one_iff, psMatrixR_eq_one_iff]
  constructor
  · rintro ⟨⟨hA, _⟩, h2, h3⟩
    exact ⟨h3, hA, h2⟩
  · rintro ⟨h3, hA, h2⟩
    refine ⟨⟨hA, ?_⟩, h2, h3⟩
    rw [inv_pow, h3, inv_one]

lemma coe_root (a : unitary ℂ) (h3 : (a : ℂ) ^ 3 = 1) :
    (((StandardModel.gaugeGroupℤ₃RootToℤ₆Root (rootsOfUnity.mkOfPowEq (a : ℂ) h3) :
      rootsOfUnity 6 ℂ) : ℂˣ) : ℂ) = (a : ℂ) := rfl

theorem inclSM_ker : inclSM.ker = StandardModel.gaugeGroupℤ₃SubGroup := by
  ext x
  rw [MonoidHom.mem_ker, StandardModel.mem_gaugeGroupℤ₃SubGroup_iff, inclSM_eq_one_iff]
  constructor
  · rintro ⟨h3, hA, h2⟩
    have h21 : (x.2.2 : ℂ) ^ 2 * (x.2.2 : ℂ) = 1 := by linear_combination h3
    have hh : (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = ((x.2.2 : ℂ) ^ 2) • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
      rw [← hA, smul_smul, h21, one_smul]
    refine ⟨rootsOfUnity.mkOfPowEq (x.2.2 : ℂ) h3, ?_⟩
    apply StandardModel.GaugeGroupI.ext
    · rw [StandardModel.gaugeGroupℤ₃OfRoot_toSU3]
      apply Subtype.ext
      rw [StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id, coe_root]
      exact hh.symm
    · rw [StandardModel.gaugeGroupℤ₃OfRoot_toSU2]
      apply Subtype.ext
      rw [StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id, coe_root, ← star_pow, h3, star_one, one_smul]
      exact h2.symm
    · rw [StandardModel.gaugeGroupℤ₃OfRoot_toU1]
      apply Subtype.ext
      rw [StandardModel.gaugeGroupℤ₆UnitaryOfRoot_coe, coe_root]
      rfl
  · rintro ⟨β, rfl⟩
    have hb3 : ((β : ℂˣ) : ℂ) ^ 3 = 1 := (mem_rootsOfUnity' 3 (β : ℂˣ)).mp β.prop
    have hU : ((StandardModel.gaugeGroupℤ₃OfRoot β).2.2 : ℂ) = ((β : ℂˣ) : ℂ) := rfl
    have hS3 : ((StandardModel.gaugeGroupℤ₃OfRoot β).1 : Matrix (Fin 3) (Fin 3) ℂ) =
        ((β : ℂˣ) : ℂ) ^ 2 • (1 : Matrix (Fin 3) (Fin 3) ℂ) :=
      StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id (StandardModel.gaugeGroupℤ₃RootToℤ₆Root β)
    have hS2 : ((StandardModel.gaugeGroupℤ₃OfRoot β).2.1 : Matrix (Fin 2) (Fin 2) ℂ) =
        star ((β : ℂˣ) : ℂ) ^ 3 • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
      StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id (StandardModel.gaugeGroupℤ₃RootToℤ₆Root β)
    refine ⟨?_, ?_, ?_⟩
    · rw [hU]
      exact hb3
    · have hb21 : ((β : ℂˣ) : ℂ) * ((β : ℂˣ) : ℂ) ^ 2 = 1 := by linear_combination hb3
      rw [hU, hS3, smul_smul, hb21, one_smul]
    · rw [hS2, ← star_pow, hb3, star_one, one_smul]


/-! ### Sharpness control (not part of the claim): the kernel is NOT the ℤ₆ subgroup.
The sixth root `ζ = -1` gives `gaugeGroupℤ₆OfRoot ζ = (1, -1, -1)`, whose image `(-1, -1, -1)` is not `1`. -/
theorem inclSM_ker_ne_Z6 : inclSM.ker ≠ StandardModel.gaugeGroupℤ₆SubGroup := by
  intro h
  have hmem : StandardModel.gaugeGroupℤ₆OfRoot
      (rootsOfUnity.mkOfPowEq (-1 : ℂ) (by norm_num : (-1 : ℂ) ^ 6 = 1)) ∈ inclSM.ker := by
    rw [h]
    exact StandardModel.gaugeGroupℤ₆OfRoot_mem _
  rw [MonoidHom.mem_ker, inclSM_eq_one_iff] at hmem
  obtain ⟨h3, -, -⟩ := hmem
  have hz : ((StandardModel.gaugeGroupℤ₆OfRoot
      (rootsOfUnity.mkOfPowEq (-1 : ℂ) (by norm_num : (-1 : ℂ) ^ 6 = 1))).2.2 : ℂ) = -1 := rfl
  rw [hz] at h3
  norm_num at h3

/-! ### Sanity: the ℤ₃ kernel is nontrivial (the primitive cube root survives in the kernel). -/
theorem inclSM_ker_ne_bot : inclSM.ker ≠ ⊥ := by
  intro h
  have hp := Complex.isPrimitiveRoot_exp 3 (by norm_num)
  have hmem : StandardModel.gaugeGroupℤ₃OfRoot (rootsOfUnity.mkOfPowEq _ hp.pow_eq_one) ∈
      inclSM.ker := by
    rw [inclSM_ker]
    exact StandardModel.gaugeGroupℤ₃OfRoot_mem _
  rw [h, Subgroup.mem_bot] at hmem
  have hU := congrArg (fun y : StandardModel.GaugeGroupI => ((y.2.2 : unitary ℂ) : ℂ)) hmem
  exact hp.ne_one (by norm_num) hU

end V3R1T4S.KF

#print axioms V3R1T4S.KF.inclSM_ker_ne_Z6
#print axioms V3R1T4S.KF.inclSM_ker_ne_bot
