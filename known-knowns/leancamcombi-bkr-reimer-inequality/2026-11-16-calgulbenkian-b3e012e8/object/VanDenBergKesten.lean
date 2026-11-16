/-
Copyright (c) 2022 Yaël Dillies. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yaël Dillies
-/
module

public import Mathlib.Data.Finset.Sups
public import Mathlib.Data.Fintype.Basic
public import Mathlib.Order.UpperLower.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sigma
import Mathlib.Data.Fintype.Sum
import Mathlib.Order.Minimal
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Set family certificates

This file defines the certificator of two families of sets. If we consider set families `𝒜` and `ℬ`
as probabilistic events, the size of the certificator `𝒜 □ ℬ` corresponds to the probability that
`𝒜` and `ℬ` occur "disjointly".

## Main declarations

* `finset.certificator`: Certificator of two elements of a Boolean algebra
* `finset.card_certificator_le`: The Van den Berg-Kesten-Reimer inequality: The probability that `𝒜`
  and `ℬ` occur "disjointly" is less than the product of their probabilities.

## References

* D. Reimer, *Proof of the Van den Berg–Kesten Conjecture*
-/

@[expose] public section

open scoped FinsetFamily

variable {α : Type*}

namespace Finset
section BooleanAlgebra
variable [BooleanAlgebra α] (s t u : Finset α) {a : α}

noncomputable def certificator : Finset α :=
  open scoped Classical in
  {a ∈ s ∩ t | ∃ x y, IsCompl x y ∧ (∀ ⦃b⦄, a ⊓ x = b ⊓ x → b ∈ s) ∧ ∀ ⦃b⦄, a ⊓ y = b ⊓ y → b ∈ t}

scoped[FinsetFamily] infixl:70 " □ " => Finset.certificator

variable {s t u}

@[simp] lemma mem_certificator :
    a ∈ s □ t ↔
      ∃ x y, IsCompl x y ∧ (∀ ⦃b⦄, a ⊓ x = b ⊓ x → b ∈ s) ∧ ∀ ⦃b⦄, a ⊓ y = b ⊓ y → b ∈ t := by
  classical
  rw [certificator, mem_filter, and_iff_right_of_imp]
  rintro ⟨u, v, _, hu, hv⟩
  exact mem_inter.2 ⟨hu rfl, hv rfl⟩

lemma certificator_subset_inter [DecidableEq α] : s □ t ⊆ s ∩ t := by
  unfold certificator; convert filter_subset ..

open scoped Classical in
lemma certificator_subset_disjSups : s □ t ⊆ s ○ t := by
  simp_rw [subset_iff, mem_certificator, mem_disjSups]
  rintro x ⟨u, v, huv, hu, hv⟩
  refine ⟨x ⊓ u, hu (inf_right_idem _ _).symm, x ⊓ v, hv (inf_right_idem _ _).symm,
    huv.disjoint.mono inf_le_right inf_le_right, ?_⟩
  rw [← inf_sup_left, huv.codisjoint.eq_top, inf_top_eq]

variable (s t u)

lemma certificator_comm : s □ t = t □ s := by
  ext s; rw [mem_certificator, exists_comm]; simp [isCompl_comm, and_comm]

lemma IsUpperSet.certificator_eq_inter [DecidableEq α] (hs : IsUpperSet (s : Set α))
    (ht : IsLowerSet (t : Set α)) : s □ t = s ∩ t := by
  refine
    certificator_subset_inter.antisymm fun a ha ↦ mem_certificator.2 ⟨a, aᶜ, isCompl_compl, ?_⟩
  rw [mem_inter] at ha
  simp only [@eq_comm _ ⊥, ← sdiff_eq, inf_idem, right_eq_inf, _root_.sdiff_self, sdiff_eq_bot_iff]
  exact ⟨fun b hab ↦ hs hab ha.1, fun b hab ↦ ht hab ha.2⟩

lemma IsLowerSet.certificator_eq_inter [DecidableEq α] (hs : IsLowerSet (s : Set α))
    (ht : IsUpperSet (t : Set α)) : s □ t = s ∩ t := by
  refine certificator_subset_inter.antisymm fun a ha ↦
    mem_certificator.2 ⟨aᶜ, a, isCompl_compl.symm, ?_⟩
  rw [mem_inter] at ha
  simp only [@eq_comm _ ⊥, ← sdiff_eq, inf_idem, right_eq_inf, _root_.sdiff_self, sdiff_eq_bot_iff]
  exact ⟨fun b hab ↦ hs hab ha.1, fun b hab ↦ ht hab ha.2⟩

open scoped Classical in
lemma IsUpperSet.certificator_eq_disjSups (hs : IsUpperSet (s : Set α))
    (ht : IsUpperSet (t : Set α)) : s □ t = s ○ t := by
  refine certificator_subset_disjSups.antisymm fun a ha ↦ mem_certificator.2 ?_
  obtain ⟨x, hx, y, hy, hxy, rfl⟩ := mem_disjSups.1 ha
  refine ⟨x, xᶜ, isCompl_compl, ?_⟩
  simp only [inf_of_le_right, le_sup_left, right_eq_inf, ← sdiff_eq, hxy.sup_sdiff_cancel_left]
  exact ⟨fun b hab ↦ hs hab hx, fun b hab ↦ ht (hab.trans_le sdiff_le) hy⟩

end BooleanAlgebra

section ReimerAuxiliary

private def toggle {β : Type*} [DecidableEq β] (a : β) (t : Finset β) : Finset β :=
  if a ∈ t then t.erase a else insert a t

private lemma mem_toggle_self {β : Type*} [DecidableEq β] (a : β) (t : Finset β) :
    a ∈ toggle a t ↔ a ∉ t := by
  by_cases h : a ∈ t <;> simp [toggle, h]

private lemma mem_toggle_of_ne {β : Type*} [DecidableEq β] {a x : β} (t : Finset β) (hne : x ≠ a) :
    x ∈ toggle a t ↔ x ∈ t := by
  by_cases h : a ∈ t <;> simp [toggle, h, hne]

private lemma toggle_involutive {β : Type*} [DecidableEq β] (a : β) (t : Finset β) :
    toggle a (toggle a t) = t := by
  ext x
  by_cases h : x = a
  · subst h; simp [mem_toggle_self]
  · simp [mem_toggle_of_ne _ h]

private lemma toggle_ne_self {β : Type*} [DecidableEq β] (a : β) (t : Finset β) :
    toggle a t ≠ t := by
  intro h
  have h1 := mem_toggle_self a t
  rw [h] at h1
  exact h1.mp (by tauto) (h1.mpr fun ha ↦ h1.mp ha ha)

private lemma neg_one_pow_card_toggle {β : Type*} [DecidableEq β] (a : β) (t : Finset β) :
    ((-1 : ℤ) ^ #(toggle a t)) = -((-1 : ℤ) ^ #t) := by
  by_cases h : a ∈ t
  · have hc : #(t.erase a) + 1 = #t := card_erase_add_one h
    simp only [toggle, h, ↓reduceIte]
    rw [← hc, pow_add, pow_one]
    ring
  · simp only [toggle, h, ↓reduceIte, card_insert_of_notMem h, pow_add, pow_one]
    ring

private lemma inter_toggle_of_mem {β : Type*} [DecidableEq β] {a : β} {s : Finset β} (ha : a ∈ s)
    (t : Finset β) : s ∩ toggle a t = toggle a (s ∩ t) := by
  ext x
  by_cases hx : x = a
  · subst hx; simp [mem_toggle_self, ha]
  · simp [mem_toggle_of_ne _ hx]

private lemma inter_toggle_of_notMem {β : Type*} [DecidableEq β] {a : β} {s : Finset β}
    (ha : a ∉ s) (t : Finset β) : s ∩ toggle a t = s ∩ t := by
  ext x
  by_cases hx : x = a
  · subst hx; simp [ha]
  · simp [mem_toggle_of_ne _ hx]

private lemma sdiff_toggle_of_mem {β : Type*} [DecidableEq β] {a : β} {w : Finset β} (ha : a ∈ w)
    (t : Finset β) : toggle a t \ w = t \ w := by
  ext x
  by_cases hx : x = a
  · subst hx; simp [ha]
  · simp [mem_toggle_of_ne _ hx]

private def reimerSpan {β : Type*} [DecidableEq β] [Fintype β] (u v : Finset β) :
    Finset (Finset β) :=
  univ.filter fun z ↦ u ∩ v ⊆ z ∧ z ⊆ u ∪ v

private lemma mem_reimerSpan {β : Type*} [DecidableEq β] [Fintype β] {u v z : Finset β} :
    z ∈ reimerSpan u v ↔ u ∩ v ⊆ z ∧ z ⊆ u ∪ v := by
  simp [reimerSpan]

private def vecUR {β : Type*} [DecidableEq β] (z t : Finset β) : ℤ :=
  if z ⊆ t then 1 else 0

private def vecUY {β : Type*} [DecidableEq β] (z t : Finset β) : ℤ :=
  if t ⊆ z then (-1 : ℤ) ^ #t else 0

private def vecVB {β : Type*} [DecidableEq β] (w b t : Finset β) : ℤ :=
  if t \ w = b \ w then (-1 : ℤ) ^ #(w ∩ b ∩ t) else 0

private def zdot {ι : Type*} [Fintype ι] (f g : ι → ℤ) : ℤ :=
  ∑ t : ι, f t * g t

private lemma zdot_comm {ι : Type*} [Fintype ι] (f g : ι → ℤ) : zdot f g = zdot g f := by
  unfold zdot
  exact sum_congr rfl fun t _ ↦ mul_comm (f t) (g t)

private lemma zdot_self_eq_zero {ι : Type*} [Fintype ι] {f : ι → ℤ} (h : zdot f f = 0) :
    ∀ t, f t = 0 := by
  intro t
  have hnonneg : ∀ x ∈ (univ : Finset ι), 0 ≤ f x * f x := fun x _ ↦ mul_self_nonneg (f x)
  have ht := (sum_eq_zero_iff_of_nonneg hnonneg).mp h t (mem_univ t)
  exact mul_self_eq_zero.mp ht

private lemma zdot_sum_sum {ι α₁ α₂ : Type*} [Fintype ι] (A : Finset α₁) (B : Finset α₂)
    (cA : α₁ → ℤ) (cB : α₂ → ℤ) (gA : α₁ → ι → ℤ) (gB : α₂ → ι → ℤ) :
    zdot (fun t ↦ ∑ a ∈ A, cA a * gA a t) (fun t ↦ ∑ b ∈ B, cB b * gB b t) =
      ∑ a ∈ A, ∑ b ∈ B, cA a * cB b * zdot (gA a) (gB b) := by
  unfold zdot
  calc
    ∑ t : ι, (∑ a ∈ A, cA a * gA a t) * (∑ b ∈ B, cB b * gB b t)
        = ∑ t : ι, ∑ a ∈ A, ∑ b ∈ B, cA a * cB b * (gA a t * gB b t) := by
          refine sum_congr rfl fun t _ ↦ ?_
          rw [sum_mul]
          refine sum_congr rfl fun a _ ↦ ?_
          rw [mul_sum]
          refine sum_congr rfl fun b _ ↦ by ring
    _ = ∑ a ∈ A, ∑ t : ι, ∑ b ∈ B, cA a * cB b * (gA a t * gB b t) := sum_comm
    _ = ∑ a ∈ A, ∑ b ∈ B, ∑ t : ι, cA a * cB b * (gA a t * gB b t) :=
          sum_congr rfl fun _ _ ↦ sum_comm
    _ = ∑ a ∈ A, ∑ b ∈ B, cA a * cB b * ∑ t : ι, gA a t * gB b t :=
          sum_congr rfl fun _ _ ↦ sum_congr rfl fun _ _ ↦ (mul_sum _ _ _).symm

private lemma zdot_vecUR_vecUY_of_ne {β : Type*} [DecidableEq β] [Fintype β]
    {z₁ z₂ : Finset β} (hne : z₁ ≠ z₂) : zdot (vecUR z₁) (vecUY z₂) = 0 := by
  unfold zdot
  by_cases hsub : z₁ ⊆ z₂
  · have hdiff : (z₂ \ z₁).Nonempty := sdiff_nonempty.mpr fun h ↦ hne (Subset.antisymm hsub h)
    obtain ⟨a, ha⟩ := hdiff
    rw [mem_sdiff] at ha
    refine sum_involution (fun t _ ↦ toggle a t) ?_ ?_ ?_ ?_
    · intro t _
      by_cases h1 : z₁ ⊆ t ∧ t ⊆ z₂
      · have h1' : z₁ ⊆ toggle a t ∧ toggle a t ⊆ z₂ := by
          constructor
          · intro x hx
            have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
            exact (mem_toggle_of_ne t hxa).mpr (h1.1 hx)
          · intro x hx
            by_cases hxa : x = a
            · exact hxa ▸ ha.1
            · exact h1.2 ((mem_toggle_of_ne t hxa).mp hx)
        simp only [vecUR, vecUY, h1.1, h1.2, h1'.1, h1'.2, ↓reduceIte, one_mul,
          neg_one_pow_card_toggle]
        ring
      · have h1' : ¬(z₁ ⊆ toggle a t ∧ toggle a t ⊆ z₂) := by
          intro h1'
          apply h1
          constructor
          · intro x hx
            have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
            exact (mem_toggle_of_ne t hxa).mp (h1'.1 hx)
          · intro x hx
            by_cases hxa : x = a
            · exact hxa ▸ ha.1
            · exact h1'.2 ((mem_toggle_of_ne t hxa).mpr hx)
        have hL : vecUR z₁ t * vecUY z₂ t = 0 := by
          by_cases hz1 : z₁ ⊆ t
          · have hz2 : ¬(t ⊆ z₂) := fun hz2 ↦ h1 ⟨hz1, hz2⟩
            simp [vecUR, vecUY, hz1, hz2]
          · simp [vecUR, hz1]
        have hR : vecUR z₁ (toggle a t) * vecUY z₂ (toggle a t) = 0 := by
          by_cases hz1 : z₁ ⊆ toggle a t
          · have hz2 : ¬(toggle a t ⊆ z₂) := fun hz2 ↦ h1' ⟨hz1, hz2⟩
            simp [vecUR, vecUY, hz1, hz2]
          · simp [vecUR, hz1]
        omega
    · intro t _ _; exact toggle_ne_self a t
    · intro t _; exact mem_univ _
    · intro t _; exact toggle_involutive a t
  · refine sum_eq_zero fun t _ ↦ ?_
    by_cases hz1 : z₁ ⊆ t
    · have hz2 : ¬(t ⊆ z₂) := fun hz2 ↦ hsub (hz1.trans hz2)
      simp [vecUR, vecUY, hz1, hz2]
    · simp [vecUR, hz1]

private lemma zdot_vecVB_vecUR_of_notMem {β : Type*} [DecidableEq β] [Fintype β]
    {w b z : Finset β} (hz : z ∉ reimerSpan w b) : zdot (vecVB w b) (vecUR z) = 0 := by
  rw [mem_reimerSpan, not_and_or] at hz
  unfold zdot
  rcases hz with hnotlo | hnothi
  · have hdiff : ((w ∩ b) \ z).Nonempty := sdiff_nonempty.mpr hnotlo
    obtain ⟨a, ha⟩ := hdiff
    rw [mem_sdiff, mem_inter] at ha
    refine sum_involution (fun t _ ↦ toggle a t) ?_ ?_ ?_ ?_
    · intro t _
      have hsd : toggle a t \ w = t \ w := sdiff_toggle_of_mem ha.1.1 t
      have hsub_iff : z ⊆ toggle a t ↔ z ⊆ t := by
        constructor <;> intro hsub x hx
        · have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
          exact (mem_toggle_of_ne t hxa).mp (hsub hx)
        · have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
          exact (mem_toggle_of_ne t hxa).mpr (hsub hx)
      by_cases hc : t \ w = b \ w ∧ z ⊆ t
      · have hc' : toggle a t \ w = b \ w ∧ z ⊆ toggle a t := ⟨hsd.trans hc.1, hsub_iff.mpr hc.2⟩
        have hint : w ∩ b ∩ toggle a t = toggle a (w ∩ b ∩ t) :=
          inter_toggle_of_mem (mem_inter.mpr ha.1) t
        simp only [vecVB, vecUR, hc.1, hc.2, hc'.1, hc'.2, ↓reduceIte, mul_one, hint,
          neg_one_pow_card_toggle]
        ring
      · have hc' : ¬(toggle a t \ w = b \ w ∧ z ⊆ toggle a t) := by
          rw [hsd, hsub_iff]; exact hc
        have hL : vecVB w b t * vecUR z t = 0 := by
          by_cases h1 : t \ w = b \ w
          · have h2 : ¬(z ⊆ t) := fun h2 ↦ hc ⟨h1, h2⟩
            simp [vecVB, vecUR, h1, h2]
          · simp [vecVB, h1]
        have hR : vecVB w b (toggle a t) * vecUR z (toggle a t) = 0 := by
          by_cases h1 : toggle a t \ w = b \ w
          · have h2 : ¬(z ⊆ toggle a t) := fun h2 ↦ hc' ⟨h1, h2⟩
            simp [vecVB, vecUR, h1, h2]
          · simp [vecVB, h1]
        omega
    · intro t _ _; exact toggle_ne_self a t
    · intro t _; exact mem_univ _
    · intro t _; exact toggle_involutive a t
  · have hdiff : (z \ (w ∪ b)).Nonempty := sdiff_nonempty.mpr hnothi
    obtain ⟨a, ha⟩ := hdiff
    rw [mem_sdiff, mem_union, not_or] at ha
    refine sum_eq_zero fun t _ ↦ ?_
    by_cases h1 : t \ w = b \ w
    · have h2 : ¬(z ⊆ t) := by
        intro hzt
        have hat : a ∈ t \ w := mem_sdiff.mpr ⟨hzt ha.1, ha.2.1⟩
        rw [h1, mem_sdiff] at hat
        exact ha.2.2 hat.1
      simp [vecVB, vecUR, h1, h2]
    · simp [vecVB, h1]

private lemma zdot_vecVB_vecUY_of_notMem {β : Type*} [DecidableEq β] [Fintype β]
    {w b z : Finset β} (hz : z ∉ reimerSpan wᶜ b) : zdot (vecVB w b) (vecUY z) = 0 := by
  rw [mem_reimerSpan, not_and_or] at hz
  unfold zdot
  rcases hz with hnotlo | hnothi
  · have hdiff : ((wᶜ ∩ b) \ z).Nonempty := sdiff_nonempty.mpr hnotlo
    obtain ⟨a, ha⟩ := hdiff
    rw [mem_sdiff, mem_inter, mem_compl] at ha
    refine sum_eq_zero fun t _ ↦ ?_
    by_cases h1 : t \ w = b \ w
    · have h2 : ¬(t ⊆ z) := by
        intro htz
        have hab : a ∈ b \ w := mem_sdiff.mpr ⟨ha.1.2, ha.1.1⟩
        rw [← h1, mem_sdiff] at hab
        exact ha.2 (htz hab.1)
      simp [vecVB, vecUY, h1, h2]
    · simp [vecVB, h1]
  · have hdiff : (z \ (wᶜ ∪ b)).Nonempty := sdiff_nonempty.mpr hnothi
    obtain ⟨a, ha⟩ := hdiff
    rw [mem_sdiff, mem_union, mem_compl, not_or, not_not] at ha
    refine sum_involution (fun t _ ↦ toggle a t) ?_ ?_ ?_ ?_
    · intro t _
      have hsd : toggle a t \ w = t \ w := sdiff_toggle_of_mem ha.2.1 t
      have hsub_iff : toggle a t ⊆ z ↔ t ⊆ z := by
        constructor <;> intro hsub x hx
        · by_cases hxa : x = a
          · exact hxa ▸ ha.1
          · exact hsub ((mem_toggle_of_ne t hxa).mpr hx)
        · by_cases hxa : x = a
          · exact hxa ▸ ha.1
          · exact hsub ((mem_toggle_of_ne t hxa).mp hx)
      by_cases hc : t \ w = b \ w ∧ t ⊆ z
      · have hc' : toggle a t \ w = b \ w ∧ toggle a t ⊆ z := ⟨hsd.trans hc.1, hsub_iff.mpr hc.2⟩
        have ha_not_wb : a ∉ w ∩ b := by rw [mem_inter]; exact fun h ↦ ha.2.2 h.2
        have hint : w ∩ b ∩ toggle a t = w ∩ b ∩ t := inter_toggle_of_notMem ha_not_wb t
        simp only [vecVB, vecUY, hc.1, hc.2, hc'.1, hc'.2, ↓reduceIte, hint,
          neg_one_pow_card_toggle]
        ring
      · have hc' : ¬(toggle a t \ w = b \ w ∧ toggle a t ⊆ z) := by
          rw [hsd, hsub_iff]; exact hc
        have hL : vecVB w b t * vecUY z t = 0 := by
          by_cases h1 : t \ w = b \ w
          · have h2 : ¬(t ⊆ z) := fun h2 ↦ hc ⟨h1, h2⟩
            simp [vecVB, vecUY, h1, h2]
          · simp [vecVB, h1]
        have hR : vecVB w b (toggle a t) * vecUY z (toggle a t) = 0 := by
          by_cases h1 : toggle a t \ w = b \ w
          · have h2 : ¬(toggle a t ⊆ z) := fun h2 ↦ hc' ⟨h1, h2⟩
            simp [vecVB, vecUY, h1, h2]
          · simp [vecVB, h1]
        omega
    · intro t _ _; exact toggle_ne_self a t
    · intro t _; exact mem_univ _
    · intro t _; exact toggle_involutive a t

private lemma neg_one_pow_emod_two (n : ℕ) : ((-1 : ℤ) ^ n) % 2 = 1 := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [pow_succ, Int.mul_emod, ih]
    decide

private lemma zdot_vecVB_vecUR_self_emod {β : Type*} [DecidableEq β] [Fintype β]
    (w b : Finset β) : zdot (vecVB w b) (vecUR w) % 2 = 1 := by
  unfold zdot
  have hsingle : ∑ t : Finset β, vecVB w b t * vecUR w t = (-1 : ℤ) ^ #(w ∩ b) := by
    rw [sum_eq_single (w ∪ b)]
    · have hsd : (w ∪ b) \ w = b \ w := by ext x; simp
      have hsub : w ⊆ w ∪ b := subset_union_left
      simp [vecVB, vecUR, hsd, hsub]
    · intro t _ hne
      by_cases h1 : t \ w = b \ w
      · have h2 : ¬(w ⊆ t) := by
          intro hwt
          apply hne
          ext x
          by_cases hxw : x ∈ w
          · exact ⟨fun _ ↦ mem_union_left b hxw, fun _ ↦ hwt hxw⟩
          · have hx : x ∈ t \ w ↔ x ∈ b \ w := by rw [h1]
            simp [mem_sdiff, hxw] at hx
            simp [hx, hxw]
        simp [vecVB, vecUR, h1, h2]
      · simp [vecVB, h1]
    · intro h; exact absurd (mem_univ _) h
  rw [hsingle]
  exact neg_one_pow_emod_two _

private lemma zdot_vecVB_vecUR_emod_of_not_subset {β : Type*} [DecidableEq β] [Fintype β]
    {w b u : Finset β} (hnot : ¬(w ⊆ u)) : zdot (vecVB w b) (vecUR u) % 2 = 0 := by
  have hdiff : (w \ u).Nonempty := sdiff_nonempty.mpr hnot
  obtain ⟨a, ha⟩ := hdiff
  rw [mem_sdiff] at ha
  unfold zdot
  set f : Finset β → ℤ := fun t ↦ vecVB w b t * vecUR u t
  have hsplit : (∑ t : Finset β, f t) =
      (∑ t ∈ univ.filter (fun t : Finset β ↦ a ∈ t), f t) +
      (∑ t ∈ univ.filter (fun t : Finset β ↦ a ∉ t), f t) := by
    rw [sum_filter_add_sum_filter_not univ (fun t : Finset β ↦ a ∈ t) f]
  have hbij : (∑ t ∈ univ.filter (fun t : Finset β ↦ a ∈ t), f t) =
      ∑ t ∈ univ.filter (fun t : Finset β ↦ a ∉ t), f (toggle a t) := by
    refine sum_bij (fun t _ ↦ toggle a t) ?_ ?_ ?_ ?_
    · intro t ht
      rw [mem_filter] at ht ⊢
      exact ⟨mem_univ _, fun h ↦ ((mem_toggle_self a t).mp h) ht.2⟩
    · intro t₁ _ t₂ _ hEq
      have := congrArg (toggle a) hEq
      simpa [toggle_involutive] using this
    · intro t ht
      rw [mem_filter] at ht
      refine ⟨toggle a t, ?_, toggle_involutive a t⟩
      rw [mem_filter]
      exact ⟨mem_univ _, (mem_toggle_self a t).mpr ht.2⟩
    · intro t _; rw [toggle_involutive]
  rw [hsplit, hbij, ← sum_add_distrib]
  have hdvd : ∀ t ∈ univ.filter (fun t : Finset β ↦ a ∉ t), 2 ∣ (f (toggle a t) + f t) := by
    intro t _
    have hsd : toggle a t \ w = t \ w := sdiff_toggle_of_mem ha.1 t
    have hsub_iff : u ⊆ toggle a t ↔ u ⊆ t := by
      constructor <;> intro hsub x hx
      · have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
        exact (mem_toggle_of_ne t hxa).mp (hsub hx)
      · have hxa : x ≠ a := fun hEq ↦ ha.2 (hEq ▸ hx)
        exact (mem_toggle_of_ne t hxa).mpr (hsub hx)
    by_cases hc : t \ w = b \ w ∧ u ⊆ t
    · have hc' : toggle a t \ w = b \ w ∧ u ⊆ toggle a t := ⟨hsd.trans hc.1, hsub_iff.mpr hc.2⟩
      have hev : (f (toggle a t) + f t) % 2 = 0 := by
        simp only [f, vecVB, vecUR, hc.1, hc.2, hc'.1, hc'.2, ↓reduceIte, mul_one]
        rw [Int.add_emod, neg_one_pow_emod_two, neg_one_pow_emod_two]
        decide
      exact Int.dvd_of_emod_eq_zero hev
    · have hc' : ¬(toggle a t \ w = b \ w ∧ u ⊆ toggle a t) := by
        rw [hsd, hsub_iff]; exact hc
      have h1 : f t = 0 := by
        by_cases hsd0 : t \ w = b \ w
        · have hsub0 : ¬(u ⊆ t) := fun h2 ↦ hc ⟨hsd0, h2⟩
          simp [f, vecUR, hsub0]
        · simp [f, vecVB, hsd0]
      have h2 : f (toggle a t) = 0 := by
        by_cases hsd0 : toggle a t \ w = b \ w
        · have hsub0 : ¬(u ⊆ toggle a t) := fun h2 ↦ hc' ⟨hsd0, h2⟩
          simp [f, vecUR, hsub0]
        · simp [f, vecVB, hsd0]
      rw [h1, h2, add_zero]
      exact dvd_zero 2
  exact Int.emod_eq_zero_of_dvd (dvd_sum hdvd)

private lemma vecUR_indep {β : Type*} [DecidableEq β] (S : Finset (Finset β))
    (c : Finset β → ℤ) (hsum : ∀ t, ∑ z ∈ S, c z * vecUR z t = 0) :
    ∀ z ∈ S, c z = 0 := by
  intro z hz
  induction hcard : #z using Nat.strong_induction_on generalizing z with
  | _ k ih =>
    have h0 := hsum z
    rw [sum_eq_single z] at h0
    · simpa [vecUR] using h0
    · intro y hy hyne
      by_cases hyz : y ⊆ z
      · have hlt : #y < k := by
          rw [← hcard]
          exact card_lt_card (ssubset_iff_subset_ne.mpr ⟨hyz, hyne⟩)
        rw [ih #y hlt y hy rfl, zero_mul]
      · simp [vecUR, hyz]
    · intro h; exact absurd hz h

private lemma vecUY_indep {β : Type*} [DecidableEq β] (S : Finset (Finset β))
    (c : Finset β → ℤ) (hsum : ∀ t, ∑ z ∈ S, c z * vecUY z t = 0) :
    ∀ z ∈ S, c z = 0 := by
  let topCard := #(S.biUnion id)
  intro z hz
  induction hgap : topCard - #z using Nat.strong_induction_on generalizing z with
  | _ k ih =>
    have h0 := hsum z
    rw [sum_eq_single z] at h0
    · simp only [vecUY, Subset.refl, ↓reduceIte, mul_eq_zero] at h0
      rcases h0 with hcz | hpow
      · exact hcz
      · exfalso
        have := neg_one_pow_emod_two #z
        rw [hpow] at this
        norm_num at this
    · intro y hy hyne
      by_cases hzy : z ⊆ y
      · have hlt_card : #z < #y := card_lt_card (ssubset_iff_subset_ne.mpr ⟨hzy, hyne.symm⟩)
        have hy_le : #y ≤ topCard := by
          refine card_le_card fun x hxy ↦ mem_biUnion.mpr ⟨y, hy, hxy⟩
        have hlt_gap : topCard - #y < k := by omega
        rw [ih (topCard - #y) hlt_gap y hy rfl, zero_mul]
      · simp [vecUY, hzy]
    · intro h; exact absurd hz h

private lemma vecVB_indep {β : Type*} [DecidableEq β] [Finite β] (W : Finset (Finset β))
    (b : Finset β → Finset β) (c : Finset β → ℤ)
    (hsum : ∀ t, ∑ w ∈ W, c w * vecVB w (b w) t = 0) :
    ∀ w ∈ W, c w = 0 := by
  let _ : Fintype β := Fintype.ofFinite β
  have hM : ∀ u ∈ W, ∑ w ∈ W, c w * zdot (vecVB w (b w)) (vecUR u) = 0 := by
    intro u _
    calc
      ∑ w ∈ W, c w * zdot (vecVB w (b w)) (vecUR u)
          = ∑ w ∈ W, ∑ t : Finset β, c w * (vecVB w (b w) t * vecUR u t) := by
            refine sum_congr rfl fun w _ ↦ ?_
            unfold zdot; rw [mul_sum]
      _ = ∑ t : Finset β, (∑ w ∈ W, c w * vecVB w (b w) t) * vecUR u t := by
            rw [sum_comm]
            refine sum_congr rfl fun t _ ↦ ?_
            rw [sum_mul]
            refine sum_congr rfl fun w _ ↦ by ring
      _ = 0 := by simp [hsum]
  suffices hall : ∀ n : ℕ, ∀ c' : Finset β → ℤ, (∑ w ∈ W, (c' w).natAbs) = n →
      (∀ u ∈ W, ∑ w ∈ W, c' w * zdot (vecVB w (b w)) (vecUR u) = 0) → ∀ w ∈ W, c' w = 0 by
    exact hall (∑ w ∈ W, (c w).natAbs) c rfl hM
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro c' hn hc'
    by_cases hn0 : n = 0
    · intro w hw
      have h0 : ∑ x ∈ W, (c' x).natAbs = 0 := hn.trans hn0
      have hw0 := Nat.eq_zero_of_le_zero ((single_le_sum (fun _ _ ↦ Nat.zero_le _) hw).trans h0.le)
      exact Int.natAbs_eq_zero.mp hw0
    · exfalso
      by_cases hodd : ∃ w ∈ W, c' w % 2 ≠ 0
      · let OddSet := W.filter fun w ↦ c' w % 2 ≠ 0
        have hne : OddSet.Nonempty := by
          obtain ⟨w, hw, hwo⟩ := hodd
          exact ⟨w, mem_filter.mpr ⟨hw, hwo⟩⟩
        obtain ⟨u₀, hu₀_mem, hu₀_min⟩ := OddSet.exists_minimalFor card hne
        have hu₀W : u₀ ∈ W := (mem_filter.mp hu₀_mem).1
        have hu₀_odd : c' u₀ % 2 ≠ 0 := (mem_filter.mp hu₀_mem).2
        have hzero := hc' u₀ hu₀W
        rw [← add_sum_erase W _ hu₀W] at hzero
        have hev_rest : 2 ∣ ∑ w ∈ W.erase u₀, c' w * zdot (vecVB w (b w)) (vecUR u₀) := by
          refine dvd_sum fun w hw ↦ ?_
          rw [mem_erase] at hw
          by_cases hcw : c' w % 2 = 0
          · exact dvd_mul_of_dvd_left (Int.dvd_of_emod_eq_zero hcw) _
          · have hw_odd : w ∈ OddSet := mem_filter.mpr ⟨hw.2, hcw⟩
            have hle : #u₀ ≤ #w := by
              by_cases hle0 : #w ≤ #u₀
              · exact hu₀_min hw_odd hle0
              · omega
            have hnot_sub : ¬(w ⊆ u₀) := by
              intro hsub
              exact hw.1 (eq_of_subset_of_card_le hsub hle)
            have hMev := zdot_vecVB_vecUR_emod_of_not_subset (b := b w) hnot_sub
            exact dvd_mul_of_dvd_right (Int.dvd_of_emod_eq_zero hMev) _
        obtain ⟨k, hk⟩ := hev_rest
        have hdiag := zdot_vecVB_vecUR_self_emod u₀ (b u₀)
        have hmod : (c' u₀ * zdot (vecVB u₀ (b u₀)) (vecUR u₀) + 2 * k) % 2 = 0 := by
          rw [← hk, hzero]; rfl
        rw [Int.add_mul_emod_self_left, Int.mul_emod, hdiag, mul_one, Int.emod_emod] at hmod
        exact hu₀_odd hmod
      · push Not at hodd
        let c'' : Finset β → ℤ := fun w ↦ c' w / 2
        have hmul : ∀ w ∈ W, c' w = 2 * c'' w := by
          intro w hw
          exact (Int.mul_ediv_cancel' (Int.dvd_of_emod_eq_zero (hodd w hw))).symm
        have hc'' : ∀ u ∈ W, ∑ w ∈ W, c'' w * zdot (vecVB w (b w)) (vecUR u) = 0 := by
          intro u hu
          have h2 : 2 * ∑ w ∈ W, c'' w * zdot (vecVB w (b w)) (vecUR u) = 0 := by
            rw [mul_sum]
            calc
              ∑ w ∈ W, 2 * (c'' w * zdot (vecVB w (b w)) (vecUR u))
                  = ∑ w ∈ W, c' w * zdot (vecVB w (b w)) (vecUR u) := by
                    refine sum_congr rfl fun w hw ↦ ?_
                    rw [hmul w hw]; ring
              _ = 0 := hc' u hu
          omega
        have hlt : (∑ w ∈ W, (c'' w).natAbs) < n := by
          have hex : ∃ w₀ ∈ W, c' w₀ ≠ 0 := by
            by_contra hall0
            push Not at hall0
            apply hn0
            rw [← hn]
            exact sum_eq_zero fun w hw ↦ Int.natAbs_eq_zero.mpr (hall0 w hw)
          obtain ⟨w₀, hw₀, hne0⟩ := hex
          have hle_all : ∀ w ∈ W, (c'' w).natAbs ≤ (c' w).natAbs := by
            intro w hw
            have := hmul w hw
            omega
          have hlt_one : (c'' w₀).natAbs < (c' w₀).natAbs := by
            have := hmul w₀ hw₀
            omega
          have hsum_lt := sum_lt_sum hle_all ⟨w₀, hw₀, hlt_one⟩
          omega
        have hzero'' := ih (∑ w ∈ W, (c'' w).natAbs) hlt c'' rfl hc''
        apply hn0
        rw [← hn]
        refine sum_eq_zero fun w hw ↦ ?_
        rw [hmul w hw, hzero'' w hw, mul_zero]; rfl

private lemma int_lin_indep_card_le :
    ∀ (m : ℕ) {ι : Type*} [Fintype ι] (v : Fin m → ι → ℤ),
      (∀ c : Fin m → ℤ, (∀ j : ι, ∑ i : Fin m, c i * v i j = 0) → ∀ i : Fin m, c i = 0) →
      m ≤ Fintype.card ι
  | 0, _, _, _, _ => Nat.zero_le _
  | m + 1, ι, _, v, hind => by
    classical
    have hv0 : ∃ j₀ : ι, v 0 j₀ ≠ 0 := by
      by_contra hall
      push Not at hall
      let c : Fin (m + 1) → ℤ := fun i ↦ if i = 0 then 1 else 0
      have hc0 : c 0 = 0 := hind c (fun j ↦ by simp [c, hall j]) 0
      simp [c] at hc0
    obtain ⟨j₀, hj₀⟩ := hv0
    let ι' := {j : ι // j ≠ j₀}
    let v' : Fin m → ι' → ℤ := fun i j ↦ v 0 j₀ * v i.succ j.1 - v i.succ j₀ * v 0 j.1
    have hind' : ∀ c' : Fin m → ℤ, (∀ j : ι', ∑ i : Fin m, c' i * v' i j = 0) →
        ∀ i : Fin m, c' i = 0 := by
      intro c' hc' i₀
      let c : Fin (m + 1) → ℤ := Fin.cases (-∑ i : Fin m, c' i * v i.succ j₀)
        (fun i ↦ c' i * v 0 j₀)
      have hsum_all : ∀ j : ι, ∑ k : Fin (m + 1), c k * v k j = 0 := by
        intro j
        rw [Fin.sum_univ_succ]
        simp only [c, Fin.cases_zero, Fin.cases_succ]
        by_cases hj : j = j₀
        · subst hj
          rw [neg_mul]
          have : (∑ x : Fin m, c' x * v 0 j * v x.succ j) =
              (∑ x : Fin m, c' x * v x.succ j) * v 0 j := by
            rw [sum_mul]
            exact sum_congr rfl fun x _ ↦ by ring
          linarith
        · have h0 := hc' ⟨j, hj⟩
          have hrew : (-∑ i : Fin m, c' i * v i.succ j₀) * v 0 j +
              ∑ i : Fin m, c' i * v 0 j₀ * v i.succ j =
              ∑ i : Fin m, c' i * v' i ⟨j, hj⟩ := by
            rw [neg_mul, sum_mul, ← sum_neg_distrib, ← sum_add_distrib]
            refine sum_congr rfl fun i _ ↦ ?_
            dsimp [v']; ring
          exact hrew.trans h0
      have hci := hind c hsum_all i₀.succ
      simp only [c, Fin.cases_succ, mul_eq_zero] at hci
      exact hci.resolve_right hj₀
    have hle := int_lin_indep_card_le m v' hind'
    have hcard : Fintype.card ι' + 1 = Fintype.card ι := by
      have h1 : Fintype.card ι' = #((univ : Finset ι).erase j₀) := by
        rw [← card_univ]
        refine card_bij (fun x _ ↦ x.1) ?_ ?_ ?_
        · intro x _; exact mem_erase.mpr ⟨x.2, mem_univ x.1⟩
        · intro a _ b _ h; exact Subtype.ext h
        · intro y hy; exact ⟨⟨y, (mem_erase.mp hy).1⟩, mem_univ _, rfl⟩
      have h2 : #((univ : Finset ι).erase j₀) + 1 = Fintype.card ι := by
        simpa [card_univ] using card_erase_add_one (mem_univ j₀)
      omega
    omega

private lemma reimer_butterfly_card_le {β : Type*} [DecidableEq β] [Fintype β]
    (W : Finset (Finset β)) (b : Finset β → Finset β) :
    #W ≤ #((W.biUnion fun w ↦ reimerSpan w (b w)) ∩
      (W.biUnion fun w ↦ reimerSpan wᶜ (b w))) := by
  set R := W.biUnion fun w ↦ reimerSpan w (b w)
  set Yp := W.biUnion fun w ↦ reimerSpan wᶜ (b w)
  set S₁ := (univ : Finset (Finset β)) \ R
  set S₂ := R \ Yp
  let Idx := {w // w ∈ W} ⊕ {z // z ∈ S₁} ⊕ {z // z ∈ S₂}
  let φ : Idx → Finset β → ℤ := fun idx ↦
    match idx with
    | Sum.inl w => vecVB w.1 (b w.1)
    | Sum.inr (Sum.inl z) => vecUR z.1
    | Sum.inr (Sum.inr z) => vecUY z.1
  have hφ_indep : ∀ c : Idx → ℤ, (∀ t : Finset β, ∑ i : Idx, c i * φ i t = 0) →
      ∀ i : Idx, c i = 0 := by
    intro c hsum
    let f₁ : Finset β → ℤ := fun t ↦ ∑ w ∈ W.attach, c (Sum.inl w) * vecVB w.1 (b w.1) t
    let f₂ : Finset β → ℤ := fun t ↦ ∑ z ∈ S₁.attach, c (Sum.inr (Sum.inl z)) * vecUR z.1 t
    let f₃ : Finset β → ℤ := fun t ↦ ∑ z ∈ S₂.attach, c (Sum.inr (Sum.inr z)) * vecUY z.1 t
    have hf123 : ∀ t, f₁ t + f₂ t + f₃ t = 0 := by
      intro t
      have h0 := hsum t
      simp only [Idx, φ, Fintype.sum_sum_type, univ_eq_attach] at h0
      dsimp [f₁, f₂, f₃]
      linarith
    have h12 : zdot f₁ f₂ = 0 := by
      rw [zdot_sum_sum]
      refine sum_eq_zero fun w _ ↦ sum_eq_zero fun z _ ↦ ?_
      have hzR : z.1 ∉ reimerSpan w.1 (b w.1) := by
        intro hmem
        exact (mem_sdiff.mp z.2).2 (mem_biUnion.mpr ⟨w.1, w.2, hmem⟩)
      rw [zdot_vecVB_vecUR_of_notMem hzR, mul_zero]
    have h13 : zdot f₁ f₃ = 0 := by
      rw [zdot_sum_sum]
      refine sum_eq_zero fun w _ ↦ sum_eq_zero fun z _ ↦ ?_
      have hzY : z.1 ∉ reimerSpan w.1ᶜ (b w.1) := by
        intro hmem
        exact (mem_sdiff.mp z.2).2 (mem_biUnion.mpr ⟨w.1, w.2, hmem⟩)
      rw [zdot_vecVB_vecUY_of_notMem hzY, mul_zero]
    have h23 : zdot f₂ f₃ = 0 := by
      rw [zdot_sum_sum]
      refine sum_eq_zero fun z₁ _ ↦ sum_eq_zero fun z₂ _ ↦ ?_
      have hne : z₁.1 ≠ z₂.1 := by
        intro hEq
        exact (mem_sdiff.mp z₁.2).2 (hEq ▸ (mem_sdiff.mp z₂.2).1)
      rw [zdot_vecUR_vecUY_of_ne hne, mul_zero]
    have hf1_self : zdot f₁ f₁ = 0 := by
      have h0 : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₁ = 0 := by
        unfold zdot; simp [hf123]
      have hexp : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₁ =
          zdot f₁ f₁ + zdot f₂ f₁ + zdot f₃ f₁ := by
        unfold zdot
        simp only [add_mul, sum_add_distrib]
      rw [zdot_comm f₂ f₁, zdot_comm f₃ f₁, h12, h13, add_zero, add_zero] at hexp
      exact hexp.symm.trans h0
    have hf2_self : zdot f₂ f₂ = 0 := by
      have h0 : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₂ = 0 := by
        unfold zdot; simp [hf123]
      have hexp : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₂ =
          zdot f₁ f₂ + zdot f₂ f₂ + zdot f₃ f₂ := by
        unfold zdot
        simp only [add_mul, sum_add_distrib]
      rw [zdot_comm f₃ f₂, h12, h23, zero_add, add_zero] at hexp
      exact hexp.symm.trans h0
    have hf3_self : zdot f₃ f₃ = 0 := by
      have h0 : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₃ = 0 := by
        unfold zdot; simp [hf123]
      have hexp : zdot (fun t ↦ f₁ t + f₂ t + f₃ t) f₃ =
          zdot f₁ f₃ + zdot f₂ f₃ + zdot f₃ f₃ := by
        unfold zdot
        simp only [add_mul, sum_add_distrib]
      rw [h13, h23, zero_add, zero_add] at hexp
      exact hexp.symm.trans h0
    have hf1_zero := zdot_self_eq_zero hf1_self
    have hf2_zero := zdot_self_eq_zero hf2_self
    have hf3_zero := zdot_self_eq_zero hf3_self
    intro idx
    match idx with
    | Sum.inl ⟨w, hw⟩ =>
      let cW : Finset β → ℤ := fun x ↦ if hx : x ∈ W then c (Sum.inl ⟨x, hx⟩) else 0
      have hWsum : ∀ t, ∑ x ∈ W, cW x * vecVB x (b x) t = 0 := by
        intro t
        rw [← sum_attach W]
        convert hf1_zero t using 1
        refine sum_congr rfl fun ⟨x, hx⟩ _ ↦ by simp [cW, hx]
      have h0 := vecVB_indep W b cW hWsum w hw
      simpa [cW, hw] using h0
    | Sum.inr (Sum.inl ⟨z, hz⟩) =>
      let cS1 : Finset β → ℤ := fun x ↦ if hx : x ∈ S₁ then c (Sum.inr (Sum.inl ⟨x, hx⟩)) else 0
      have hS1sum : ∀ t, ∑ x ∈ S₁, cS1 x * vecUR x t = 0 := by
        intro t
        rw [← sum_attach S₁]
        convert hf2_zero t using 1
        refine sum_congr rfl fun ⟨x, hx⟩ _ ↦ by simp [cS1, hx]
      have h0 := vecUR_indep S₁ cS1 hS1sum z hz
      simpa [cS1, hz] using h0
    | Sum.inr (Sum.inr ⟨z, hz⟩) =>
      let cS2 : Finset β → ℤ := fun x ↦ if hx : x ∈ S₂ then c (Sum.inr (Sum.inr ⟨x, hx⟩)) else 0
      have hS2sum : ∀ t, ∑ x ∈ S₂, cS2 x * vecUY x t = 0 := by
        intro t
        rw [← sum_attach S₂]
        convert hf3_zero t using 1
        refine sum_congr rfl fun ⟨x, hx⟩ _ ↦ by simp [cS2, hx]
      have h0 := vecUY_indep S₂ cS2 hS2sum z hz
      simpa [cS2, hz] using h0
  let e : Fin (Fintype.card Idx) ≃ Idx := (Fintype.equivFin Idx).symm
  have hcard_le : Fintype.card Idx ≤ Fintype.card (Finset β) := by
    refine int_lin_indep_card_le (Fintype.card Idx) (fun i ↦ φ (e i)) ?_
    intro c hc i
    have hsum_idx : ∀ t : Finset β, ∑ idx : Idx, c (e.symm idx) * φ idx t = 0 := by
      intro t
      rw [← e.sum_comp (fun idx ↦ c (e.symm idx) * φ idx t)]
      simpa using hc t
    simpa using hφ_indep (fun idx ↦ c (e.symm idx)) hsum_idx (e i)
  have hIdx_card : Fintype.card Idx = #W + (#S₁ + #S₂) := by
    simp [Idx, Fintype.card_sum, Fintype.card_coe]
  have hR_part : #(R ∩ Yp) + #S₂ = #R := by
    dsimp [S₂]
    have := card_sdiff_add_card_inter R Yp
    omega
  have hU_part : #R + #S₁ = Fintype.card (Finset β) := by
    dsimp [S₁]
    have hsub : R ⊆ (univ : Finset (Finset β)) := subset_univ R
    have := card_sdiff_add_card_eq_card hsub
    rw [card_univ] at this
    omega
  omega

private def liftSub {α : Type*} [DecidableEq α] (S v : Finset α)
    (z : Finset {x : α // x ∉ S}) : Finset α :=
  v ∪ z.image Subtype.val

private def projSub {α : Type*} [DecidableEq α] [Fintype α] (S r : Finset α) :
    Finset {x : α // x ∉ S} :=
  univ.filter fun x ↦ x.1 ∈ r

private lemma mem_liftSub_iff {α : Type*} [DecidableEq α] {S v : Finset α} (hv : v ⊆ S)
    {z : Finset {x : α // x ∉ S}} {x : α} :
    x ∈ liftSub S v z ↔ (x ∈ S ∧ x ∈ v) ∨ ∃ hx : x ∉ S, ⟨x, hx⟩ ∈ z := by
  unfold liftSub
  rw [mem_union, mem_image]
  constructor
  · rintro (hxv | ⟨⟨y, hy⟩, hyz, rfl⟩)
    · exact Or.inl ⟨hv hxv, hxv⟩
    · exact Or.inr ⟨hy, hyz⟩
  · rintro (⟨_, hxv⟩ | ⟨hx, hxz⟩)
    · exact Or.inl hxv
    · exact Or.inr ⟨⟨x, hx⟩, hxz, rfl⟩

private lemma projSub_liftSub {α : Type*} [DecidableEq α] [Fintype α] {S v : Finset α}
    (hv : v ⊆ S) (z : Finset {x : α // x ∉ S}) :
    projSub S (liftSub S v z) = z := by
  ext ⟨x, hx⟩
  simp only [projSub, mem_filter, mem_univ, true_and, mem_liftSub_iff hv]
  constructor
  · rintro (⟨hxS, _⟩ | ⟨_, hxz⟩)
    · exact absurd hxS hx
    · exact hxz
  · intro hxz; exact Or.inr ⟨hx, hxz⟩

private lemma liftSub_projSub {α : Type*} [DecidableEq α] [Fintype α] {S r : Finset α} :
    liftSub S (r ∩ S) (projSub S r) = r := by
  ext x
  rw [mem_liftSub_iff inter_subset_right]
  by_cases hx : x ∈ S
  · simp [hx]
  · simp [projSub, hx]

end ReimerAuxiliary

open scoped FinsetFamily

variable [DecidableEq α] [Fintype α] {𝒜 ℬ 𝒞 : Finset (Finset α)}

/-- The **Van den Berg-Kesten-Reimer Inequality**: The probability that `𝒜` and `ℬ` occur
"disjointly" is less than the product of their probabilities. -/
lemma card_certificator_le : 2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ := by
  classical
  let W_sub (S v : Finset α) : Finset (Finset {x : α // x ∉ S}) :=
    univ.filter fun z ↦ liftSub S v z ∈ 𝒜 □ ℬ
  let P_sub (S v : Finset α) : Finset (Finset {x : α // x ∉ S}) :=
    univ.filter fun z ↦ liftSub S v z ∈ 𝒜 ∧ liftSub S v zᶜ ∈ ℬ
  have hslice : ∀ S : Finset α, ∀ v ∈ S.powerset, #(W_sub S v) ≤ #(P_sub S v) := by
    intro S v hv
    rw [mem_powerset] at hv
    let xChoice : Finset α → Finset α := fun w ↦
      if hw : w ∈ 𝒜 □ ℬ then Classical.choose (mem_certificator.mp hw) else ∅
    let yChoice : Finset α → Finset α := fun w ↦
      if hw : w ∈ 𝒜 □ ℬ then
        Classical.choose (Classical.choose_spec (mem_certificator.mp hw))
      else ∅
    let bMap : Finset {x : α // x ∉ S} → Finset {x : α // x ∉ S} := fun z ↦
      let w := liftSub S v z
      univ.filter fun u ↦ (u ∈ z ↔ u.1 ∈ xChoice w)
    have hbf : #(W_sub S v) ≤
        #(((W_sub S v).biUnion fun z ↦ reimerSpan z (bMap z)) ∩
          ((W_sub S v).biUnion fun z ↦ reimerSpan zᶜ (bMap z))) :=
      reimer_butterfly_card_le (W_sub S v) bMap
    refine hbf.trans (card_le_card fun z hz ↦ ?_)
    rw [mem_inter, mem_biUnion, mem_biUnion] at hz
    obtain ⟨⟨z₁, hz₁, hzR⟩, ⟨z₂, hz₂, hzY⟩⟩ := hz
    simp only [P_sub, mem_filter, mem_univ, true_and]
    constructor
    · simp only [W_sub, mem_filter, mem_univ, true_and] at hz₁
      have hspec := Classical.choose_spec (Classical.choose_spec (mem_certificator.mp hz₁))
      have hx_eq : xChoice (liftSub S v z₁) = Classical.choose (mem_certificator.mp hz₁) := by
        dsimp only [xChoice]
        split_ifs
        rfl
      rw [mem_reimerSpan] at hzR
      refine hspec.2.1 ?_
      rw [← hx_eq]
      ext a
      simp only [mem_inter]
      constructor <;> rintro ⟨haL, haX⟩
      · refine ⟨?_, haX⟩
        rw [mem_liftSub_iff hv] at haL ⊢
        rcases haL with ⟨haS, hav⟩ | ⟨haS, haz₁⟩
        · exact Or.inl ⟨haS, hav⟩
        · refine Or.inr ⟨haS, hzR.1 (mem_inter.mpr ⟨haz₁, ?_⟩)⟩
          simp [bMap, haz₁, haX]
      · refine ⟨?_, haX⟩
        rw [mem_liftSub_iff hv] at haL ⊢
        rcases haL with ⟨haS, hav⟩ | ⟨haS, haz⟩
        · exact Or.inl ⟨haS, hav⟩
        · refine Or.inr ⟨haS, ?_⟩
          have hu := hzR.2 haz
          rw [mem_union] at hu
          rcases hu with h1 | h2
          · exact h1
          · simp only [bMap, mem_filter, mem_univ, true_and] at h2
            exact h2.mpr haX
    · simp only [W_sub, mem_filter, mem_univ, true_and] at hz₂
      have hspec := Classical.choose_spec (Classical.choose_spec (mem_certificator.mp hz₂))
      have hx_eq : xChoice (liftSub S v z₂) = Classical.choose (mem_certificator.mp hz₂) := by
        dsimp only [xChoice]
        split_ifs
        rfl
      have hy_eq : yChoice (liftSub S v z₂) =
          Classical.choose (Classical.choose_spec (mem_certificator.mp hz₂)) := by
        dsimp only [yChoice]
        split_ifs
        rfl
      have hcompl : IsCompl (xChoice (liftSub S v z₂)) (yChoice (liftSub S v z₂)) := by
        rw [hx_eq, hy_eq]; exact hspec.1
      have hy_iff : ∀ a : α, a ∈ yChoice (liftSub S v z₂) ↔ a ∉ xChoice (liftSub S v z₂) := by
        intro a
        rw [← hcompl.compl_eq, mem_compl]
      rw [mem_reimerSpan] at hzY
      refine hspec.2.2 ?_
      rw [← hy_eq]
      ext a
      simp only [mem_inter]
      constructor <;> rintro ⟨haL, haY⟩
      · refine ⟨?_, haY⟩
        have ha_notX : a ∉ xChoice (liftSub S v z₂) := (hy_iff a).mp haY
        rw [mem_liftSub_iff hv] at haL ⊢
        rcases haL with ⟨haS, hav⟩ | ⟨haS, haz₂⟩
        · exact Or.inl ⟨haS, hav⟩
        · refine Or.inr ⟨haS, ?_⟩
          rw [mem_compl]
          intro h_in_z
          have hu := hzY.2 h_in_z
          rw [mem_union, mem_compl] at hu
          rcases hu with hnot2 | hb2
          · exact hnot2 haz₂
          · simp only [bMap, mem_filter, mem_univ, true_and] at hb2
            exact ha_notX (hb2.mp haz₂)
      · refine ⟨?_, haY⟩
        have ha_notX : a ∉ xChoice (liftSub S v z₂) := (hy_iff a).mp haY
        rw [mem_liftSub_iff hv] at haL ⊢
        rcases haL with ⟨haS, hav⟩ | ⟨haS, hazc⟩
        · exact Or.inl ⟨haS, hav⟩
        · refine Or.inr ⟨haS, ?_⟩
          rw [mem_compl] at hazc
          by_contra hnot_z₂
          apply hazc
          refine hzY.1 (mem_inter.mpr ⟨mem_compl.mpr hnot_z₂, ?_⟩)
          simp [bMap, hnot_z₂, ha_notX]
  have hLHS : ∑ S : Finset α, ∑ v ∈ S.powerset, #(W_sub S v) =
      2 ^ Fintype.card α * #(𝒜 □ ℬ) := by
    have hperS : ∀ S : Finset α, ∑ v ∈ S.powerset, #(W_sub S v) = #(𝒜 □ ℬ) := by
      intro S
      rw [← card_sigma]
      refine card_bij (fun p _ ↦ liftSub S p.1 p.2) ?_ ?_ ?_
      · intro p hp
        rw [mem_sigma] at hp
        exact (mem_filter.mp hp.2).2
      · intro p₁ hp₁ p₂ hp₂ hEq
        rw [mem_sigma, mem_powerset] at hp₁ hp₂
        have hv1 : liftSub S p₁.1 p₁.2 ∩ S = p₁.1 := by
          ext x
          rw [mem_inter, mem_liftSub_iff hp₁.1]
          constructor
          · rintro ⟨(⟨_, hxv⟩ | ⟨hxS, _⟩), hxS'⟩
            · exact hxv
            · exact absurd hxS' hxS
          · intro hxv; exact ⟨Or.inl ⟨hp₁.1 hxv, hxv⟩, hp₁.1 hxv⟩
        have hv2 : liftSub S p₂.1 p₂.2 ∩ S = p₂.1 := by
          ext x
          rw [mem_inter, mem_liftSub_iff hp₂.1]
          constructor
          · rintro ⟨(⟨_, hxv⟩ | ⟨hxS, _⟩), hxS'⟩
            · exact hxv
            · exact absurd hxS' hxS
          · intro hxv; exact ⟨Or.inl ⟨hp₂.1 hxv, hxv⟩, hp₂.1 hxv⟩
        have hp12 : p₁.1 = p₂.1 := by rw [← hv1, hEq, hv2]
        rcases p₁ with ⟨v₁, z₁⟩
        rcases p₂ with ⟨v₂, z₂⟩
        dsimp at hp12 hEq
        subst hp12
        have hz12 : z₁ = z₂ := by
          rw [← projSub_liftSub hp₁.1 z₁, hEq, projSub_liftSub hp₁.1 z₂]
        exact Sigma.ext rfl (heq_of_eq hz12)
      · intro w hw
        refine ⟨⟨w ∩ S, projSub S w⟩, ?_, liftSub_projSub⟩
        rw [mem_sigma, mem_powerset]
        refine ⟨inter_subset_right, ?_⟩
        simp only [W_sub, mem_filter, mem_univ, true_and, liftSub_projSub]
        exact hw
    simp [hperS, card_univ, Fintype.card_finset]
  have hRHS : ∑ S : Finset α, ∑ v ∈ S.powerset, #(P_sub S v) = #𝒜 * #ℬ := by
    rw [sum_sigma', ← card_sigma, ← card_product]
    refine card_bij (fun q _ ↦ (liftSub q.1.1 q.1.2 q.2, liftSub q.1.1 q.1.2 q.2ᶜ)) ?_ ?_ ?_
    · intro q hq
      rw [mem_sigma] at hq
      have hP := (mem_filter.mp hq.2).2
      exact mem_product.mpr hP
    · intro q₁ hq₁ q₂ hq₂ hEq
      rw [mem_sigma, mem_sigma, mem_powerset] at hq₁ hq₂
      have hEq1 : liftSub q₁.1.1 q₁.1.2 q₁.2 = liftSub q₂.1.1 q₂.1.2 q₂.2 :=
        congrArg Prod.fst hEq
      have hEq2 : liftSub q₁.1.1 q₁.1.2 q₁.2ᶜ = liftSub q₂.1.1 q₂.1.2 q₂.2ᶜ :=
        congrArg Prod.snd hEq
      have hS_char : ∀ (S v : Finset α) (hv : v ⊆ S) (z : Finset {x : α // x ∉ S}) (x : α),
          (x ∈ liftSub S v z ↔ x ∈ liftSub S v zᶜ) ↔ x ∈ S := by
        intro S v hv z x
        rw [mem_liftSub_iff hv, mem_liftSub_iff hv]
        by_cases hxS : x ∈ S
        · simp [hxS]
        · simp [hxS, mem_compl]
      have hS12 : q₁.1.1 = q₂.1.1 := by
        ext x
        rw [← hS_char q₁.1.1 q₁.1.2 hq₁.1.2 q₁.2 x,
            ← hS_char q₂.1.1 q₂.1.2 hq₂.1.2 q₂.2 x, hEq1, hEq2]
      rcases q₁ with ⟨⟨S₁, v₁⟩, z₁⟩
      rcases q₂ with ⟨⟨S₂, v₂⟩, z₂⟩
      dsimp at hS12 hEq1
      subst hS12
      have hv12 : v₁ = v₂ := by
        ext x
        by_cases hxS : x ∈ S₁
        · have h := Finset.ext_iff.mp hEq1 x
          rw [mem_liftSub_iff hq₁.1.2, mem_liftSub_iff hq₂.1.2] at h
          simpa [hxS] using h
        · exact ⟨fun h ↦ absurd (hq₁.1.2 h) hxS, fun h ↦ absurd (hq₂.1.2 h) hxS⟩
      subst hv12
      have hz12 : z₁ = z₂ := by
        rw [← projSub_liftSub hq₁.1.2 z₁, hEq1, projSub_liftSub hq₁.1.2 z₂]
      subst hz12
      rfl
    · intro ry hry
      rw [mem_product] at hry
      rcases ry with ⟨r, y⟩
      let S : Finset α := univ.filter fun x ↦ (x ∈ r ↔ x ∈ y)
      let v : Finset α := r ∩ S
      let z : Finset {x : α // x ∉ S} := projSub S r
      have hr_eq : liftSub S v z = r := liftSub_projSub
      have hy_eq : liftSub S v zᶜ = y := by
        ext x
        rw [mem_liftSub_iff inter_subset_right]
        by_cases hxS : x ∈ S
        · have hiff : x ∈ r ↔ x ∈ y := (mem_filter.mp hxS).2
          simp [hxS, hiff]
        · have hniff : ¬(x ∈ r ↔ x ∈ y) := fun h ↦ hxS (mem_filter.mpr ⟨mem_univ x, h⟩)
          constructor
          · rintro (⟨hxS', _⟩ | ⟨_, hxz⟩)
            · exact absurd hxS' hxS
            · simp only [z, mem_compl, projSub, mem_filter, mem_univ, true_and] at hxz
              tauto
          · intro hxy
            refine Or.inr ⟨hxS, ?_⟩
            simp only [z, mem_compl, projSub, mem_filter, mem_univ, true_and]
            tauto
      refine ⟨⟨⟨S, v⟩, z⟩, ?_, Prod.ext hr_eq hy_eq⟩
      rw [mem_sigma, mem_sigma, mem_powerset]
      refine ⟨⟨mem_univ S, inter_subset_right⟩, ?_⟩
      simp [P_sub, hr_eq, hy_eq, hry.1, hry.2]
  calc
    2 ^ Fintype.card α * #(𝒜 □ ℬ)
        = ∑ S : Finset α, ∑ v ∈ S.powerset, #(W_sub S v) := hLHS.symm
    _ ≤ ∑ S : Finset α, ∑ v ∈ S.powerset, #(P_sub S v) :=
        sum_le_sum fun S _ ↦ sum_le_sum (hslice S)
    _ = #𝒜 * #ℬ := hRHS

end Finset
