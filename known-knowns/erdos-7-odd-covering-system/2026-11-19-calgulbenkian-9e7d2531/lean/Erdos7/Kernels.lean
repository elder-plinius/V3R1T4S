/-
Stage 4, Lemma 4: the fibre kernels.
* `unif_kernel`: uniform weight on the complement of the pure part (Lemma 4(1), pure deletion).
* `capped_kernel`: the capped (reweighted) fibre kernel of Lemma 4(2).
-/
import Mathlib

namespace Erdos7
open Finset
open scoped Classical

variable {α : Type} [Fintype α]

/-- A two-level weight `a` on `G`, `b` on `R`, `0` elsewhere. -/
private noncomputable def twoLevel (G R : Finset α) (a b : ℚ) (x : α) : ℚ :=
  (if x ∈ G then a else 0) + (if x ∈ R then b else 0)

private lemma twoLevel_sum (G R S : Finset α) (a b : ℚ) :
    ∑ x ∈ S, twoLevel G R a b x = (S ∩ G).card * a + (S ∩ R).card * b := by
  simp only [twoLevel, sum_add_distrib, sum_ite_mem, sum_const, nsmul_eq_mul]

/-- **Lemma 4(1), kernel form.** Deleting a set `P` with `|P| + s ≤ |α|`, `s > 0`: the uniform
probability weight on the complement of `P` gives every set `A` weight at most `|A| / s`. -/
theorem unif_kernel (P : Finset α) (s : ℕ) (hs : 0 < s) (hP : P.card + s ≤ Fintype.card α) :
    ∃ k : α → ℚ, (∀ x, 0 ≤ k x) ∧ ∑ x, k x = 1 ∧ (∀ x ∈ P, k x = 0) ∧
      ∀ A : Finset α, ∑ x ∈ A, k x ≤ (A.card : ℚ) / s := by
  have hc : (Pᶜ).card = Fintype.card α - P.card := card_compl P
  have hsc : s ≤ (Pᶜ).card := by omega
  have hpos : (0:ℚ) < (Pᶜ).card := by exact_mod_cast lt_of_lt_of_le hs hsc
  refine ⟨twoLevel Pᶜ ∅ (1 / (Pᶜ).card) 0, ?_, ?_, ?_, ?_⟩
  · intro x; simp only [twoLevel]; split_ifs <;> simp
  · rw [twoLevel_sum]; simp; field_simp
  · intro x hx; simp [twoLevel, hx]
  · intro A
    rw [twoLevel_sum]
    simp only [inter_empty, card_empty, Nat.cast_zero, zero_mul, add_zero]
    have h1 : ((A ∩ Pᶜ).card : ℚ) ≤ A.card := by exact_mod_cast card_le_card inter_subset_left
    have h2 : (s:ℚ) ≤ (Pᶜ).card := by exact_mod_cast hsc
    have hs' : (0:ℚ) < s := by exact_mod_cast hs
    rw [mul_one_div, div_le_div_iff₀ hpos hs']
    have h3 : (0:ℚ) ≤ A.card := by positivity
    nlinarith

/-- **Lemma 4(2), the capped fibre kernel.** `P` is the pure part (`|P| ≤ g0`), `B` the part of
the fibre covered by mixed classes, `G = (P ∪ B)ᶜ` the good part, `n = |α|`, `C > 0` the cap with
`C (n - g0) ≥ n` (that is `δ = 1 - 1/C ≥ ρ = g0/n`).  There is a probability weight `k` with
`k = 0` on `P`, `k ≤ C/n` pointwise, and `k(B) ≤ C (g0/n + |B|/n - δ)_+`. -/
theorem capped_kernel (P B : Finset α) (n g0 : ℕ) (hn : Fintype.card α = n) (hn0 : 0 < n)
    (C : ℚ) (hC : 0 < C) (hPg : P.card ≤ g0) (hCg : (n:ℚ) ≤ C * (n - g0)) :
    ∃ k : α → ℚ, (∀ x, 0 ≤ k x) ∧ ∑ x, k x = 1 ∧ (∀ x ∈ P, k x = 0) ∧ (∀ x, k x ≤ C / n) ∧
      ∑ x ∈ B, k x ≤ C * max 0 (((g0:ℚ) + B.card) / n - (1 - 1 / C)) := by
  set G : Finset α := (P ∪ B)ᶜ with hG
  set R : Finset α := B \ P with hR
  have hn' : (0:ℚ) < n := by exact_mod_cast hn0
  have hGR : Disjoint G R := by
    rw [disjoint_left]; intro x hx hx'
    simp only [hG, hR, mem_compl, mem_union, mem_sdiff] at hx hx'
    exact hx (Or.inr hx'.1)
  have hBG : B ∩ G = ∅ := by
    ext x; simp only [hG, mem_inter, mem_compl, mem_union]; tauto
  have hBR : B ∩ R = R := by
    ext x; simp only [hR, mem_inter, mem_sdiff]; tauto
  have hpart : G.card + P.card + R.card = n := by
    have h1 : P ∪ B = P ∪ R := by
      ext x; simp only [hR, mem_union, mem_sdiff]; tauto
    have h2 : (P ∪ R).card = P.card + R.card := by
      apply card_union_of_disjoint
      rw [disjoint_left]; intro x hx hx'
      exact (mem_sdiff.1 hx').2 hx
    have h3 : G.card = Fintype.card α - (P ∪ B).card := card_compl _
    have h4 : (P ∪ B).card ≤ Fintype.card α := card_le_univ _
    rw [h1, h2] at h3 h4; omega
  have hpartQ : (G.card : ℚ) + P.card + R.card = n := by exact_mod_cast hpart
  have hPgQ : (P.card : ℚ) ≤ g0 := by exact_mod_cast hPg
  have hRB : (R.card : ℚ) ≤ B.card := by exact_mod_cast card_le_card sdiff_subset
  have hzeroP : ∀ a b : ℚ, ∀ x ∈ P, twoLevel G R a b x = 0 := by
    intro a b x hx
    have h1 : x ∉ G := by simp [hG, hx]
    have h2 : x ∉ R := by simp [hR, hx]
    simp [twoLevel, h1, h2]
  have hle : ∀ a b c : ℚ, a ≤ c → b ≤ c → 0 ≤ c → ∀ x, twoLevel G R a b x ≤ c := by
    intro a b c ha hb hc x
    by_cases h1 : x ∈ G
    · have h2 : x ∉ R := disjoint_left.1 hGR h1
      simp [twoLevel, h1, h2, ha]
    · by_cases h2 : x ∈ R <;> simp [twoLevel, h1, h2, hb, hc]
  have hnn : ∀ a b : ℚ, 0 ≤ a → 0 ≤ b → ∀ x, 0 ≤ twoLevel G R a b x := by
    intro a b ha hb x
    simp only [twoLevel]; split_ifs <;> linarith
  have hCn : 0 ≤ C / n := by positivity
  by_cases hcase : (n:ℚ) ≤ C * G.card
  · -- enough good mass: uniform on `G`
    have hg : (0:ℚ) < G.card := by
      by_contra h
      have : (G.card : ℚ) = 0 := le_antisymm (not_lt.1 h) (by positivity)
      rw [this, mul_zero] at hcase; linarith
    refine ⟨twoLevel G R (1 / G.card) 0, hnn _ _ (by positivity) le_rfl, ?_, hzeroP _ _,
      hle _ _ _ ?_ hCn hCn, ?_⟩
    · rw [twoLevel_sum]; simp; field_simp
    · rw [div_le_div_iff₀ hg hn']; linarith
    · rw [twoLevel_sum, hBG]; simp
      exact mul_nonneg hC.le (le_max_left _ _)
  · -- cap active: `C/n` on `G`, the rest of the mass spread on `R = B \ P`
    push_neg at hcase
    have hRpos : (0:ℚ) < R.card := by
      have : C * (G.card : ℚ) < C * (n - g0) := lt_of_lt_of_le hcase hCg
      have := lt_of_mul_lt_mul_left this hC.le
      linarith
    have hb0 : 0 < 1 - C * G.card / n := by
      rw [sub_pos, div_lt_one hn']; exact hcase
    refine ⟨twoLevel G R (C / n) ((1 - C * G.card / n) / R.card), hnn _ _ hCn (by positivity), ?_,
      hzeroP _ _, hle _ _ _ le_rfl ?_ hCn, ?_⟩
    · rw [twoLevel_sum]; simp only [univ_inter]; field_simp; ring
    · rw [div_le_div_iff₀ hRpos hn']
      have h1 : (1 - C * G.card / n) * n = n - C * G.card := by field_simp
      rw [h1]
      have : C * (n - g0) ≤ C * (G.card + R.card) := by
        apply mul_le_mul_of_nonneg_left _ hC.le; linarith
      nlinarith
    · rw [twoLevel_sum, hBG, hBR]
      simp only [card_empty, Nat.cast_zero, zero_mul, zero_add]
      have h1 : (R.card : ℚ) * ((1 - C * G.card / n) / R.card) = 1 - C * G.card / n := by
        field_simp
      rw [h1]
      refine le_trans ?_ (mul_le_mul_of_nonneg_left (le_max_right _ _) hC.le)
      have h2 : C * (((g0:ℚ) + B.card) / n - (1 - 1 / C))
          = 1 - C * ((n:ℚ) - g0 - B.card) / n := by field_simp; ring
      rw [h2]
      have h3 : C * ((n:ℚ) - g0 - B.card) / n ≤ C * G.card / n := by
        apply div_le_div_of_nonneg_right _ hn'.le
        apply mul_le_mul_of_nonneg_left _ hC.le; linarith
      linarith

end Erdos7
