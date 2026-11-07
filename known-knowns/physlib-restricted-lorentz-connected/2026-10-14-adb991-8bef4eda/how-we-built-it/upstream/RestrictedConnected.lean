/-
Draft written in the V3R1T4S run 2026-10-14-0608 (construct-space lens); not submitted anywhere.
-/
module

public import Physlib.Relativity.LorentzGroup.Restricted.FromBoostRotation
public import Mathlib.Analysis.Normed.Module.Connected
/-!

# Connectedness of the restricted Lorentz group

The special orthogonal group `SO(n)` and the restricted Lorentz group are connected.

## i. Overview

The Householder reflection `householder w = 1 - (2 / (w ⬝ᵥ w)) • vecMulVec w w` reflects in the
hyperplane orthogonal to `w`. If an element `A` of `SO(n)` fixes `e i` for all `i > k`, then
`householder (A e k - e k)` moves `A e k` to `e k` and still fixes those `e i`; a second reflection
`householder (e 0)` restores the determinant. So `A` is reduced to `1` by products of two
reflections. Each such product lies in the identity component of `SO(n)`, because
`w ↦ householder u * householder w` is continuous on the connected set `{w ≠ 0}` and equals `1` at
`w = u`. Hence `SO(n)` is connected, for every `n`. The restricted Lorentz group is homeomorphic to
`Velocity d × SO(d)` (`LorentzGroup.toBoostRotation`), so it is connected too.

## ii. Key results

- `Matrix.specialOrthogonalGroup_connectedSpace` : `SO(n)` is connected.
- `LorentzGroup.restricted_isConnected` : the restricted Lorentz group is connected.
- `LorentzGroup.restricted_eq_connectedComponent_one` : it is the identity component.

## iii. Table of contents

- A. Householder reflections
- B. Connectedness of the special orthogonal group
- C. Connectedness of the restricted Lorentz group

## iv. References

- No external references.

-/

@[expose] public section

noncomputable section

namespace Matrix

variable {n : ℕ}

/-!

## A. Householder reflections

-/

/-- The Householder reflection in the hyperplane orthogonal to `w`. It equals `1` when `w = 0`. -/
def householder (w : Fin n → ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  1 - (2 / (w ⬝ᵥ w)) • vecMulVec w w

lemma householder_mulVec (w x : Fin n → ℝ) :
    householder w *ᵥ x = x - ((2 / (w ⬝ᵥ w)) * (w ⬝ᵥ x)) • w := by
  simp [householder, sub_mulVec, smul_mulVec, vecMulVec_mulVec, smul_smul]

lemma householder_transpose (w : Fin n → ℝ) : (householder w)ᵀ = householder w := by
  simp [householder, transpose_vecMulVec]

lemma householder_mulVec_householder_mulVec (w x : Fin n → ℝ) :
    householder w *ᵥ (householder w *ᵥ x) = x := by
  rw [householder_mulVec, householder_mulVec, dotProduct_sub, dotProduct_smul, smul_eq_mul,
    sub_sub, ← add_smul]
  by_cases h : w ⬝ᵥ w = 0
  · simp [h]
  · have hc : (2 / (w ⬝ᵥ w)) * (w ⬝ᵥ w) = 2 := by field_simp
    have : 2 / (w ⬝ᵥ w) * (w ⬝ᵥ x) +
        2 / (w ⬝ᵥ w) * (w ⬝ᵥ x - 2 / (w ⬝ᵥ w) * (w ⬝ᵥ x) * (w ⬝ᵥ w)) = 0 := by
      linear_combination (-(2 / (w ⬝ᵥ w) * (w ⬝ᵥ x))) * hc
    rw [this, zero_smul, sub_zero]

@[simp]
lemma householder_mul_self (w : Fin n → ℝ) : householder w * householder w = 1 :=
  ext_of_mulVec_single fun _ => by
    rw [← mulVec_mulVec, householder_mulVec_householder_mulVec, one_mulVec]

lemma householder_mem_orthogonalGroup (w : Fin n → ℝ) :
    householder w ∈ orthogonalGroup (Fin n) ℝ := by
  rw [mem_orthogonalGroup_iff, householder_transpose, householder_mul_self]

lemma det_householder {w : Fin n → ℝ} (hw : w ≠ 0) : (householder w).det = -1 := by
  have h1 : householder w =
      1 + replicateCol Unit (-(2 / (w ⬝ᵥ w)) • w) * replicateRow Unit w := by
    rw [← vecMulVec_eq, householder, sub_eq_add_neg]
    congr 1
    ext i j
    simp [vecMulVec_apply]
    ring
  rw [h1, det_one_add_replicateCol_mul_replicateRow, dotProduct_smul, smul_eq_mul]
  have hw' : w ⬝ᵥ w ≠ 0 := by rwa [Ne, dotProduct_self_eq_zero]
  have hc : (2 / (w ⬝ᵥ w)) * (w ⬝ᵥ w) = 2 := by field_simp
  linear_combination -hc

lemma householder_mulVec_of_dotProduct_eq_zero {w x : Fin n → ℝ} (h : w ⬝ᵥ x = 0) :
    householder w *ᵥ x = x := by
  simp [householder_mulVec, h]

/-- The Householder reflection in `a - b` sends `a` to `b` when `a ≠ b` have the same length. -/
lemma householder_sub_mulVec {a b : Fin n → ℝ} (hab : a ≠ b) (hn : a ⬝ᵥ a = b ⬝ᵥ b) :
    householder (a - b) *ᵥ a = b := by
  rw [householder_mulVec]
  have hw : (a - b) ⬝ᵥ (a - b) ≠ 0 := by rwa [Ne, dotProduct_self_eq_zero, sub_eq_zero]
  have h1 : (a - b) ⬝ᵥ (a - b) = 2 * ((a - b) ⬝ᵥ a) := by
    simp only [sub_dotProduct, dotProduct_sub]
    rw [dotProduct_comm b a]
    linarith [hn]
  have h2 : (2 / ((a - b) ⬝ᵥ (a - b))) * ((a - b) ⬝ᵥ a) = 1 := by
    rw [h1] at hw ⊢
    have : (a - b) ⬝ᵥ a ≠ 0 := fun h => hw (by rw [h, mul_zero])
    field_simp
  rw [h2, one_smul, sub_sub_cancel]

/-!

## B. Connectedness of the special orthogonal group

-/

lemma householder_mul_householder_mem_specialOrthogonalGroup {u v : Fin n → ℝ} (hu : u ≠ 0)
    (hv : v ≠ 0) : householder u * householder v ∈ specialOrthogonalGroup (Fin n) ℝ :=
  mem_specialOrthogonalGroup_iff.mpr ⟨mul_mem (householder_mem_orthogonalGroup u)
    (householder_mem_orthogonalGroup v), by rw [det_mul, det_householder hu, det_householder hv]; norm_num⟩

/-- A product of two Householder reflections lies in the identity component of `SO(n)`:
  `w ↦ householder u * householder w` maps the connected set `{w ≠ 0}` into `SO(n)` and is `1` at
  `w = u`. -/
lemma householder_mul_householder_mem_connectedComponent_one (hn : 1 < n) {u v : Fin n → ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) :
    (⟨householder u * householder v, householder_mul_householder_mem_specialOrthogonalGroup hu hv⟩ :
      specialOrthogonalGroup (Fin n) ℝ) ∈ connectedComponent 1 := by
  have : ConnectedSpace ({0}ᶜ : Set (Fin n → ℝ)) := isConnected_iff_connectedSpace.mp
    (isConnected_compl_singleton_of_one_lt_rank (by simpa using hn) 0)
  let f : ({0}ᶜ : Set (Fin n → ℝ)) → specialOrthogonalGroup (Fin n) ℝ := fun w =>
    ⟨householder u * householder w.1, householder_mul_householder_mem_specialOrthogonalGroup hu
      (Set.mem_compl_singleton_iff.mp w.2)⟩
  have hden (w : ({0}ᶜ : Set (Fin n → ℝ))) : w.1 ⬝ᵥ w.1 ≠ 0 := by
    rw [Ne, dotProduct_self_eq_zero]
    exact Set.mem_compl_singleton_iff.mp w.2
  have hf : Continuous f := by
    refine Continuous.subtype_mk (continuous_const.mul (continuous_const.sub ?_)) _
    exact (continuous_const.div (by fun_prop) hden).smul (by fun_prop)
  have h1 : f ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩ = 1 := Subtype.ext (by simp [f])
  have hrange := (isConnected_range hf).isPreconnected.subset_connectedComponent
    (Set.mem_range_self ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩)
  rw [h1] at hrange
  exact hrange ⟨⟨v, Set.mem_compl_singleton_iff.mpr hv⟩, rfl⟩

/-- One elimination step: if `A` is orthogonal, fixes `e i` for `k < i`, and `A e k ≠ e k`, then
  `householder (A e k - e k) * A` fixes `e i` for `k ≤ i`. -/
lemma householder_mul_mulVec_single {A : Matrix (Fin n) (Fin n) ℝ}
    (hA : A ∈ orthogonalGroup (Fin n) ℝ) (k : Fin n)
    (hfix : ∀ i : Fin n, k < i → A *ᵥ Pi.single i 1 = Pi.single i 1)
    (ha : A *ᵥ Pi.single k 1 ≠ Pi.single k 1) (i : Fin n) (hi : k ≤ i) :
    (householder (A *ᵥ Pi.single k 1 - Pi.single k 1) * A) *ᵥ Pi.single i 1 = Pi.single i 1 := by
  rw [mem_orthogonalGroup_iff'] at hA
  have dot (x y : Fin n → ℝ) : (A *ᵥ x) ⬝ᵥ (A *ᵥ y) = x ⬝ᵥ y := by
    rw [dotProduct_mulVec, ← vecMul_transpose, vecMul_vecMul, hA, vecMul_one]
  rw [← mulVec_mulVec]
  rcases hi.lt_or_eq with h | rfl
  · have h1 : (A *ᵥ Pi.single k 1) ⬝ᵥ Pi.single i 1 = Pi.single k 1 ⬝ᵥ Pi.single i 1 := by
      conv_lhs => rw [← hfix i h]
      exact dot _ _
    rw [hfix i h, householder_mulVec_of_dotProduct_eq_zero (by rw [sub_dotProduct, h1, sub_self])]
  · exact householder_sub_mulVec ha (dot _ _)

/-- The inductive step of the elimination, from `k` to `k + 1`. -/
lemma mem_connectedComponent_one_of_fix_succ {k : ℕ}
    (ih : ∀ A : specialOrthogonalGroup (Fin n) ℝ,
      (∀ i : Fin n, k ≤ i.val → A.1 *ᵥ Pi.single i 1 = Pi.single i 1) → A ∈ connectedComponent 1)
    (A : specialOrthogonalGroup (Fin n) ℝ)
    (hfix : ∀ i : Fin n, k + 1 ≤ i.val → A.1 *ᵥ Pi.single i 1 = Pi.single i 1) :
    A ∈ connectedComponent 1 := by
  obtain ⟨hAo, hdet⟩ := mem_specialOrthogonalGroup_iff.mp A.2
  by_cases hk : k < n
  swap
  · exact ih A fun i hi => absurd (lt_of_lt_of_le i.2 (not_lt.mp hk)) (not_lt.mpr hi)
  let kk : Fin n := ⟨k, hk⟩
  by_cases ha : A.1 *ᵥ Pi.single kk 1 = Pi.single kk 1
  · refine ih A fun i hi => ?_
    rcases hi.lt_or_eq with h | h
    · exact hfix i h
    · rw [show i = kk from Fin.ext h.symm]
      exact ha
  have hw : A.1 *ᵥ Pi.single kk 1 - Pi.single kk 1 ≠ 0 := sub_ne_zero.mpr ha
  have hHA := householder_mul_mulVec_single hAo kk (fun i h => hfix i h) ha
  set H := householder (A.1 *ᵥ Pi.single kk 1 - Pi.single kk 1)
  rcases Nat.eq_zero_or_pos k with hk0 | hk0
  · -- for `k = 0` the reflection alone fixes everything, so `A = H` has determinant `-1`
    have h1 : H * A.1 = 1 := ext_of_mulVec_single fun i => by
      rw [hHA i (Fin.mk_le_of_le_val (by omega)), one_mulVec]
    have h2 : A.1 = H := by
      calc A.1 = H * (H * A.1) := by rw [← Matrix.mul_assoc, householder_mul_self, Matrix.one_mul]
        _ = H := by rw [h1, Matrix.mul_one]
    rw [h2, det_householder hw] at hdet
    norm_num at hdet
  -- for `k ≥ 1`, compose with the reflection in `e 0`, which fixes `e i` for `i ≥ k`
  let z : Fin n := ⟨0, by omega⟩
  have hz : (Pi.single z 1 : Fin n → ℝ) ≠ 0 := fun h => by simpa using congrFun h z
  let A2 : specialOrthogonalGroup (Fin n) ℝ := ⟨householder (Pi.single z 1) * (H * A.1),
    mem_specialOrthogonalGroup_iff.mpr ⟨mul_mem (householder_mem_orthogonalGroup _)
      (mul_mem (householder_mem_orthogonalGroup _) hAo), by
        rw [det_mul, det_mul, det_householder hz, det_householder hw, hdet]; norm_num⟩⟩
  have hA2 : A2 ∈ connectedComponent 1 := ih A2 fun i hi => by
    have hzi : z ≠ i := fun h => by
      have := congrArg Fin.val h
      simp [z] at this
      omega
    simp only [A2]
    rw [← mulVec_mulVec, hHA i hi, householder_mulVec_of_dotProduct_eq_zero]
    simp [hzi]
  convert mul_mem_connectedComponent_one
    (householder_mul_householder_mem_connectedComponent_one (by omega) hw hz) hA2 using 1
  apply Subtype.ext
  simp only [Submonoid.coe_mul, A2]
  rw [← Matrix.mul_assoc, Matrix.mul_assoc H, householder_mul_self, Matrix.mul_one,
    ← Matrix.mul_assoc, householder_mul_self, Matrix.one_mul]

/-- Elimination: an element of `SO(n)` fixing `e i` for all `i ≥ k` is in the identity
  component. -/
lemma mem_connectedComponent_one_of_fix (k : ℕ) (A : specialOrthogonalGroup (Fin n) ℝ)
    (hfix : ∀ i : Fin n, k ≤ i.val → A.1 *ᵥ Pi.single i 1 = Pi.single i 1) :
    A ∈ connectedComponent 1 := by
  induction k generalizing A with
  | zero =>
    have : A = 1 := Subtype.ext <| ext_of_mulVec_single fun i => by
      rw [hfix i (Nat.zero_le _)]
      exact (one_mulVec _).symm
    rw [this]
    exact mem_connectedComponent
  | succ k ih => exact mem_connectedComponent_one_of_fix_succ ih A hfix

/-- The special orthogonal group `SO(n)` is connected, for every `n`. -/
lemma specialOrthogonalGroup_connectedSpace :
    ConnectedSpace (specialOrthogonalGroup (Fin n) ℝ) :=
  connectedSpace_iff_connectedComponent.mpr ⟨1, Set.eq_univ_of_forall fun A =>
    mem_connectedComponent_one_of_fix n A fun i hi => absurd i.2 (not_lt.mpr hi)⟩

end Matrix

/-!

## C. Connectedness of the restricted Lorentz group

-/

namespace LorentzGroup

open Matrix
open minkowskiMatrix
open TopologicalSpace

/-- The restricted Lorentz group is connected. -/
lemma restricted_isConnected {d : ℕ} :
    IsConnected (restricted d : Set (LorentzGroup d)) := by
  have := specialOrthogonalGroup_connectedSpace (n := d)
  have : ConnectedSpace (Lorentz.Velocity d) :=
    connectedSpace_iff_univ.mpr Lorentz.Velocity.isPathConnected.isConnected
  exact isConnected_iff_connectedSpace.mpr
    (toBoostRotation.symm.surjective.connectedSpace toBoostRotation.symm.continuous)

/-- The restricted Lorentz group is the connected component of the identity. -/
lemma restricted_eq_connectedComponent_one {d : ℕ} :
    (restricted d : Set (LorentzGroup d)) = connectedComponent 1 :=
  restricted_eq_identity_component_of_isConnected restricted_isConnected

end LorentzGroup

end
