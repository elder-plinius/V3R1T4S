import Physlib
import V3R1T4SSpec

/-!
# Fully explicit paths: the restricted Lorentz group is path connected (imports only Physlib)

Every element of `SO(n)` is a product of pairs `hh u * hh v` of Householder reflections
(`elim_general`, explicit Householder QR elimination). Each pair is joined to `1` by the explicit
path `t ↦ hh u * hh ((1 - t) • u + t • v)`, `t ∈ [0, 1]`; if that segment passes through `0`, then
`v` is a negative multiple of `u`, so `hh v = hh u` and the pair is already `1`. No connectedness of
`{w ≠ 0}` is needed, there is no restriction on `n`, and no import beyond `Physlib`.
-/

open Matrix

namespace V3R1T4SConstructExplicit

noncomputable section

variable {n : ℕ}

/-- Householder matrix of `w` (equal to `1` when `w = 0`, because `2 / 0 = 0`). -/
def hh (w : Fin n → ℝ) : Matrix (Fin n) (Fin n) ℝ := 1 - (2 / (w ⬝ᵥ w)) • vecMulVec w w

lemma hh_mulVec (w x : Fin n → ℝ) : hh w *ᵥ x = x - ((2 / (w ⬝ᵥ w)) * (w ⬝ᵥ x)) • w := by
  simp [hh, sub_mulVec, smul_mulVec, vecMulVec_mulVec, smul_smul]

lemma hh_transpose (w : Fin n → ℝ) : (hh w)ᵀ = hh w := by
  simp [hh, transpose_vecMulVec]

lemma hh_mulVec_hh_mulVec (w x : Fin n → ℝ) : hh w *ᵥ (hh w *ᵥ x) = x := by
  rw [hh_mulVec, hh_mulVec, dotProduct_sub, dotProduct_smul, smul_eq_mul, sub_sub, ← add_smul]
  by_cases h : w ⬝ᵥ w = 0
  · simp [h]
  · have hc : (2 / (w ⬝ᵥ w)) * (w ⬝ᵥ w) = 2 := by field_simp
    have : 2 / (w ⬝ᵥ w) * (w ⬝ᵥ x) +
        2 / (w ⬝ᵥ w) * (w ⬝ᵥ x - 2 / (w ⬝ᵥ w) * (w ⬝ᵥ x) * (w ⬝ᵥ w)) = 0 := by
      linear_combination (-(2 / (w ⬝ᵥ w) * (w ⬝ᵥ x))) * hc
    rw [this, zero_smul, sub_zero]

lemma hh_mul_self (w : Fin n → ℝ) : hh w * hh w = 1 :=
  ext_of_mulVec_single fun i => by rw [← mulVec_mulVec, hh_mulVec_hh_mulVec, one_mulVec]

lemma hh_mem (w : Fin n → ℝ) : hh w ∈ orthogonalGroup (Fin n) ℝ := by
  rw [mem_orthogonalGroup_iff, hh_transpose, hh_mul_self]

lemma dot_self_ne_zero {w : Fin n → ℝ} (hw : w ≠ 0) : w ⬝ᵥ w ≠ 0 := by
  rwa [Ne, dotProduct_self_eq_zero]

lemma det_hh {w : Fin n → ℝ} (hw : w ≠ 0) : (hh w).det = -1 := by
  have h1 : hh w = 1 + replicateCol Unit (-(2 / (w ⬝ᵥ w)) • w) * replicateRow Unit w := by
    rw [← vecMulVec_eq, hh, sub_eq_add_neg]
    congr 1
    ext i j
    simp [vecMulVec_apply]
    ring
  rw [h1, det_one_add_replicateCol_mul_replicateRow, dotProduct_smul, smul_eq_mul]
  have hc : (2 / (w ⬝ᵥ w)) * (w ⬝ᵥ w) = 2 := by field_simp [dot_self_ne_zero hw]
  linear_combination -hc

lemma hh_mulVec_of_dot_eq_zero {w x : Fin n → ℝ} (h : w ⬝ᵥ x = 0) : hh w *ᵥ x = x := by
  simp [hh_mulVec, h]

lemma hh_sub_mulVec {a b : Fin n → ℝ} (hab : a ≠ b) (hn : a ⬝ᵥ a = b ⬝ᵥ b) :
    hh (a - b) *ᵥ a = b := by
  rw [hh_mulVec]
  have hw : (a - b) ⬝ᵥ (a - b) ≠ 0 := dot_self_ne_zero (sub_ne_zero.mpr hab)
  have h1 : (a - b) ⬝ᵥ (a - b) = 2 * ((a - b) ⬝ᵥ a) := by
    simp only [sub_dotProduct, dotProduct_sub]
    rw [dotProduct_comm b a]
    linarith [hn]
  have h2 : (2 / ((a - b) ⬝ᵥ (a - b))) * ((a - b) ⬝ᵥ a) = 1 := by
    rw [h1] at hw ⊢
    have : (a - b) ⬝ᵥ a ≠ 0 := fun h => hw (by rw [h, mul_zero])
    field_simp
  rw [h2, one_smul, sub_sub_cancel]

lemma dot_pres {A : Matrix (Fin n) (Fin n) ℝ} (hA : A ∈ orthogonalGroup (Fin n) ℝ)
    (x y : Fin n → ℝ) : (A *ᵥ x) ⬝ᵥ (A *ᵥ y) = x ⬝ᵥ y := by
  rw [mem_orthogonalGroup_iff'] at hA
  rw [dotProduct_mulVec, ← vecMul_transpose, vecMul_vecMul, hA, vecMul_one]

/-- General explicit elimination (Householder QR, two reflections per column). -/
lemma elim_general (P : Matrix (Fin n) (Fin n) ℝ → Prop) (h1 : P 1)
    (hstep : 1 < n → ∀ u v : Fin n → ℝ, u ≠ 0 → v ≠ 0 → ∀ B : Matrix (Fin n) (Fin n) ℝ,
      B ∈ specialOrthogonalGroup (Fin n) ℝ → P B → P (hh u * hh v * B)) (k : ℕ) :
    ∀ A : Matrix (Fin n) (Fin n) ℝ, A ∈ specialOrthogonalGroup (Fin n) ℝ →
      (∀ i : Fin n, k ≤ i.val → A *ᵥ Pi.single i 1 = Pi.single i 1) → P A := by
  induction k with
  | zero =>
    intro A _ hfix
    have hA1 : A = 1 := ext_of_mulVec_single (fun i => by rw [hfix i (Nat.zero_le _), one_mulVec])
    rw [hA1]
    exact h1
  | succ k ih =>
    intro A hA hfix
    have hAo : A ∈ orthogonalGroup (Fin n) ℝ := (mem_specialOrthogonalGroup_iff.mp hA).1
    have hdet : A.det = 1 := (mem_specialOrthogonalGroup_iff.mp hA).2
    by_cases hk : k < n
    swap
    · exact ih A hA (fun i hi => absurd (lt_of_lt_of_le i.2 (not_lt.mp hk)) (not_lt.mpr hi))
    set kk : Fin n := ⟨k, hk⟩ with hkk
    set a := A *ᵥ Pi.single kk 1 with ha_def
    by_cases ha : a = Pi.single kk 1
    · apply ih A hA
      intro i hi
      rcases Nat.lt_or_eq_of_le hi with h | h
      · exact hfix i h
      · have : i = kk := Fin.ext h.symm
        subst this
        exact ha
    · set w := a - Pi.single kk 1 with hw_def
      have hw : w ≠ 0 := sub_ne_zero.mpr ha
      have ha_norm : a ⬝ᵥ a = Pi.single kk 1 ⬝ᵥ Pi.single kk 1 := dot_pres hAo _ _
      have hperp : ∀ i : Fin n, k + 1 ≤ i.val → w ⬝ᵥ Pi.single i 1 = 0 := by
        intro i hi
        have h1 : a ⬝ᵥ Pi.single i 1 = Pi.single kk 1 ⬝ᵥ Pi.single i 1 := by
          conv_lhs => rw [← hfix i hi]
          exact dot_pres hAo _ _
        rw [hw_def, sub_dotProduct, h1, sub_self]
      have hHa : hh w *ᵥ a = Pi.single kk 1 := hh_sub_mulVec ha ha_norm
      have hfixHA : ∀ i : Fin n, k ≤ i.val → (hh w * A) *ᵥ Pi.single i 1 = Pi.single i 1 := by
        intro i hi
        rw [← mulVec_mulVec]
        rcases Nat.lt_or_eq_of_le hi with h | h
        · rw [hfix i h, hh_mulVec_of_dot_eq_zero (hperp i h)]
        · have : i = kk := Fin.ext h.symm
          subst this
          exact hHa
      rcases Nat.eq_zero_or_pos k with hk0 | hk0
      · exfalso
        have hHA : hh w * A = 1 :=
          ext_of_mulVec_single (fun i => by rw [hfixHA i (by omega), one_mulVec])
        have hAH : A = hh w := by
          calc A = hh w * (hh w * A) := by rw [← Matrix.mul_assoc, hh_mul_self, Matrix.one_mul]
            _ = hh w := by rw [hHA, Matrix.mul_one]
        rw [hAH, det_hh hw] at hdet
        norm_num at hdet
      · set z : Fin n := ⟨0, by omega⟩ with hz_def
        have hz : (Pi.single z 1 : Fin n → ℝ) ≠ 0 := by
          intro h
          have := congrFun h z
          simp at this
        set A2 := hh (Pi.single z 1) * (hh w * A) with hA2_def
        have hdet2 : A2.det = 1 := by
          rw [hA2_def, det_mul, det_mul, det_hh hz, det_hh hw, hdet]
          norm_num
        have hA2 : A2 ∈ specialOrthogonalGroup (Fin n) ℝ := mem_specialOrthogonalGroup_iff.mpr
          ⟨mul_mem (hh_mem _) (mul_mem (hh_mem _) hAo), hdet2⟩
        have hfix2 : ∀ i : Fin n, k ≤ i.val → A2 *ᵥ Pi.single i 1 = Pi.single i 1 := by
          intro i hi
          rw [hA2_def, ← mulVec_mulVec, hfixHA i hi]
          apply hh_mulVec_of_dot_eq_zero
          have hzi : z ≠ i := by
            intro h
            have := congrArg Fin.val h
            simp [hz_def] at this
            omega
          rw [single_dotProduct, one_mul, Pi.single_apply]
          simp [hzi]
        have hA_eq : A = hh w * hh (Pi.single z 1) * A2 := by
          rw [hA2_def, Matrix.mul_assoc, ← Matrix.mul_assoc (hh (Pi.single z 1)),
            hh_mul_self, Matrix.one_mul, ← Matrix.mul_assoc, hh_mul_self, Matrix.one_mul]
        rw [hA_eq]
        exact hstep (by omega) w (Pi.single z 1) hw hz A2 hA2 (ih A2 hA2 hfix2)

lemma hh_mul_hh_mem_SO {u v : Fin n → ℝ} (hu : u ≠ 0) (hv : v ≠ 0) :
    hh u * hh v ∈ specialOrthogonalGroup (Fin n) ℝ :=
  mem_specialOrthogonalGroup_iff.mpr ⟨mul_mem (hh_mem u) (hh_mem v),
    by rw [det_mul, det_hh hu, det_hh hv]; norm_num⟩

/-- Householder reflections only depend on the line spanned by the vector. -/
lemma hh_smul {c : ℝ} (hc : c ≠ 0) (w : Fin n → ℝ) : hh (c • w) = hh w := by
  unfold hh
  congr 1
  rw [smul_dotProduct, dotProduct_smul, smul_vecMulVec, vecMulVec_smul, smul_smul, smul_smul,
    smul_eq_mul, smul_eq_mul]
  by_cases h : w ⬝ᵥ w = 0
  · simp [h]
  · congr 1
    field_simp

/-- If the segment from `u` to `v` passes through `0`, the two reflections agree. -/
lemma hh_eq_of_segment {u v : Fin n → ℝ} (hu : u ≠ 0) (hv : v ≠ 0) {t : ℝ}
    (h0 : (1 - t) • u + t • v = 0) : hh v = hh u := by
  have ht0 : t ≠ 0 := by
    rintro rfl
    simp at h0
    exact hu h0
  have hv' : v = (-((1 - t) / t)) • u := by
    have h1 : t • v = -((1 - t) • u) := by
      rw [add_comm] at h0
      exact eq_neg_of_add_eq_zero_left h0
    calc v = t⁻¹ • (t • v) := by rw [smul_smul, inv_mul_cancel₀ ht0, one_smul]
      _ = (-((1 - t) / t)) • u := by
        rw [h1, smul_neg, smul_smul, ← neg_smul, div_eq_inv_mul]
  have hc : -((1 - t) / t) ≠ 0 := by
    intro hc
    rw [hc, zero_smul] at hv'
    exact hv hv'
  rw [hv', hh_smul hc]

/-- The explicit path `t ↦ hh u * hh ((1 - t) • u + t • v)` from `1` to `hh u * hh v`, inside `SO(n)`,
when the segment from `u` to `v` avoids `0`. -/
def pairPath {u v : Fin n → ℝ} (hu : u ≠ 0)
    (hseg : ∀ t : ℝ, 0 ≤ t → t ≤ 1 → (1 - t) • u + t • v ≠ 0) (hv : v ≠ 0) :
    Path (1 : specialOrthogonalGroup (Fin n) ℝ) ⟨hh u * hh v, hh_mul_hh_mem_SO hu hv⟩ where
  toFun t := ⟨hh u * hh ((1 - (t : ℝ)) • u + (t : ℝ) • v),
    hh_mul_hh_mem_SO hu (hseg t t.2.1 t.2.2)⟩
  continuous_toFun := by
    have hden : ∀ t : unitInterval, ((1 - (t : ℝ)) • u + (t : ℝ) • v) ⬝ᵥ
        ((1 - (t : ℝ)) • u + (t : ℝ) • v) ≠ 0 := fun t => dot_self_ne_zero (hseg t t.2.1 t.2.2)
    apply Continuous.subtype_mk
    unfold hh
    apply continuous_const.mul
    apply continuous_const.sub
    exact (continuous_const.div (by fun_prop) hden).smul (by fun_prop)
  source' := Subtype.ext (by simp [hh_mul_self])
  target' := Subtype.ext (by simp)

/-- Every product of two Householder reflections is joined to `1` inside `SO(n)` (any `n`). -/
lemma pair_joined {u v : Fin n → ℝ} (hu : u ≠ 0) (hv : v ≠ 0) :
    Joined (1 : specialOrthogonalGroup (Fin n) ℝ) ⟨hh u * hh v, hh_mul_hh_mem_SO hu hv⟩ := by
  by_cases h : ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ (1 - t) • u + t • v = 0
  · obtain ⟨t, -, -, h0⟩ := h
    have : (⟨hh u * hh v, hh_mul_hh_mem_SO hu hv⟩ : specialOrthogonalGroup (Fin n) ℝ) = 1 :=
      Subtype.ext (by simp [hh_eq_of_segment hu hv h0, hh_mul_self])
    rw [this]
  · simp only [not_exists, not_and] at h
    exact ⟨pairPath hu (fun t h0 h1 => h t h0 h1) hv⟩

/-- Every element of `SO(n)` is joined to `1` inside `SO(n)`. -/
theorem SO_joined (A : specialOrthogonalGroup (Fin n) ℝ) : Joined 1 A :=
  elim_general (n := n)
    (fun M => ∀ hM : M ∈ specialOrthogonalGroup (Fin n) ℝ,
      Joined (1 : specialOrthogonalGroup (Fin n) ℝ) ⟨M, hM⟩)
    (fun _ => Joined.refl _)
    (fun _ u v hu hv _ hB hPB _ => by
      have := (pair_joined hu hv).mul (hPB hB)
      rw [mul_one] at this
      exact this)
    n A.1 A.2 (fun i hi => absurd i.2 (not_lt.mpr hi)) A.2

/-- `SO(n)` is path connected, for every `n`. -/
theorem SO_pathConnectedSpace : PathConnectedSpace (specialOrthogonalGroup (Fin n) ℝ) :=
  pathConnectedSpace_iff_eq.mpr ⟨1, Set.eq_univ_of_forall fun A => SO_joined A⟩

/-- The restricted Lorentz group is path connected. -/
theorem restricted_isPathConnected {d : ℕ} :
    IsPathConnected (LorentzGroup.restricted d : Set (LorentzGroup d)) := by
  have h1 : PathConnectedSpace (specialOrthogonalGroup (Fin d) ℝ) := SO_pathConnectedSpace
  have h2 : PathConnectedSpace (Lorentz.Velocity d) :=
    pathConnectedSpace_iff_univ.mpr Lorentz.Velocity.isPathConnected
  have h3 : PathConnectedSpace (LorentzGroup.restricted d) :=
    LorentzGroup.toBoostRotation.symm.surjective.pathConnectedSpace
      LorentzGroup.toBoostRotation.symm.continuous
  exact isPathConnected_iff_pathConnectedSpace.mpr h3

/-- FXNL5, from path-connectedness. -/
theorem restricted_isConnected_explicit {d : ℕ} :
    IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d)) :=
  restricted_isPathConnected.isConnected

end

end V3R1T4SConstructExplicit

theorem V3R1T4S.claim : V3R1T4S.spec :=
  fun {_} => V3R1T4SConstructExplicit.restricted_isConnected_explicit
