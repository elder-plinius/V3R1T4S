module

public import APAP.BohrFourier
public import APAP.Physics.Unbalancing

import AddCombi.Mathlib.Algebra.BigOperators.Ring.Finset
import AddCombi.Mathlib.Algebra.GroupWithZero.Indicator
import AddCombi.Mathlib.Algebra.Order.GroupWithZero.Indicator
import APAP.Mathlib.Algebra.BigOperators.Pi
import APAP.Mathlib.Algebra.Group.Action.Pointwise.Set.Basic
import APAP.Mathlib.Algebra.Group.Translate
import APAP.Prereqs.Convolution.Discrete.Basic
import APAP.Prereqs.Convolution.Norm
import APAP.Prereqs.FourierTransform.Discrete
import APAP.Prereqs.Inner.Hoelder.Discrete
import APAP.Prereqs.LpNorm.Discrete.Basic
import Mathlib.Algebra.Group.Action.Pointwise.Finset
import Mathlib.Algebra.Order.Floor.Semifield
import Mathlib.Algebra.Order.Star.Real
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Bohr DRC sifting, Hölder lifting, `L^p` orthogonality, and single almost-periodicity step
-/

@[expose] public section

attribute [-simp] Real.log_inv

open Finset hiding card
open Fintype (card)
open Function MeasureTheory RCLike Real
open scoped NNReal ENNReal BigOperators ComplexConjugate Pointwise Indicator translate mu

local notation3 "𝓛" x:arg => 1 + Real.log x⁻¹

namespace BohrStep

section CurlogExtra

lemma curlog_mul_add {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 𝓛 (x * y) ≤ 𝓛 x + 𝓛 y := by
  have hlog : log (x * y)⁻¹ = log x⁻¹ + log y⁻¹ := by
    rw [mul_inv, log_mul (by positivity) (by positivity)]
  linarith

lemma rpow_inv_neg_curlog_le {x : ℝ} (hx₀ : 0 ≤ x) (hx₁ : x ≤ 1) :
    x⁻¹ ^ (𝓛 x)⁻¹ ≤ exp 1 := by
  obtain rfl | hx₀ := hx₀.eq_or_lt
  · simp [(exp_pos _).le]
  obtain rfl | hx₁ := hx₁.eq_or_lt
  · simp
  have hx := (one_lt_inv₀ hx₀).2 hx₁
  calc
    x⁻¹ ^ (𝓛 x)⁻¹ ≤ x⁻¹ ^ (log x⁻¹)⁻¹ := by
      gcongr
      · exact hx.le
      · exact log_pos hx
      · simp
    _ ≤ exp 1 := x⁻¹.rpow_inv_log_le_exp_one

end CurlogExtra

section BohrDRC
variable {G : Type*} [DecidableEq G] [Fintype G] [AddCommGroup G]

private def cBohr (p : ℕ) (A : Finset G) (s : Fin p → G) : Finset G :=
  univ.inf fun i ↦ s i +ᵥ A

set_option backward.isDefEq.respectTransparency false in
private lemma lemma_0_bohr (p : ℕ) (B₁ B₂ A : Finset G) (f : G → ℝ) :
    ∑ s, ⟪𝟭_[↑(B₁ ∩ cBohr p A s), ℝ] ○ᵈ 𝟭_[↑(B₂ ∩ cBohr p A s)], f⟫_[ℝ] =
      (#B₁ * #B₂) • ∑ x, (μ_[ℝ] B₁ ○ᵈ μ B₂) x * (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x ^ p * f x := by
  simp_rw [mul_assoc]
  simp only [wInner_one_eq_sum, inner_apply', RCLike.conj_to_real, mul_sum, sum_mul, smul_sum,
    @sum_comm _ _ (Fin p → G), sum_dddconv_mul, dddconv_apply_sub, Fintype.sum_pow,
    Set.map_indicator_one]
  congr with b₁
  congr with b₂
  refine Fintype.sum_equiv (Equiv.neg _) _ _ fun s ↦ ?_
  rw [← smul_mul_assoc, mul_smul_mul_comm, card_smul_mu_apply, card_smul_mu_apply,
    coe_inter, coe_inter, Set.indicator_one_inter_apply, Set.indicator_one_inter_apply,
    mul_mul_mul_comm, prod_mul_distrib]
  simp [cBohr, indicator_one_inf_apply, sub_eq_add_neg, mul_assoc, add_comm]

private lemma sum_cBohr (p : ℕ) (B A : Finset G) : ∑ s, #(B ∩ cBohr p A s) = #A ^ p * #B := by
  simp only [card_eq_sum_indicator_one, Set.indicator_one_inter_apply, cBohr,
    indicator_one_inf_apply, mul_sum, sum_mul, coe_inter, coe_vadd_finset, sum_pow', @sum_comm G,
    Fintype.piFinset_univ, ← translate_indicator_one, translate_apply]
  congr with x
  exact Fintype.sum_equiv (Equiv.subLeft fun _ ↦ x) _ _ fun s ↦ mul_comm _ _

private lemma sum_cast_cBohr (p : ℕ) (B A : Finset G) :
    ∑ s, (#(B ∩ cBohr p A s) : ℝ) = #A ^ p * #B := by
  rw [← Nat.cast_sum, sum_cBohr]; norm_cast

variable [MeasurableSpace G]

/-- High-value difference set for general `(B₁, B₂)` Dependent Random Choice sifting. -/
noncomputable def sBohr (p : ℝ≥0) (ε : ℝ) (B₁ B₂ A : Finset G) : Finset G :=
  {x | (1 - ε) * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] < (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x}

@[simp]
lemma mem_sBohr {p : ℝ≥0} {ε : ℝ} {B₁ B₂ A : Finset G} {x : G} :
    x ∈ sBohr p ε B₁ B₂ A ↔
      (1 - ε) * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] <
        (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x := by
  simp [sBohr]

lemma mem_sBohr' {p : ℝ≥0} {ε : ℝ} {B₁ B₂ A : Finset G} {x : G} :
    x ∈ sBohr p ε B₁ B₂ A ↔
      (1 - ε) * ‖μ_[ℝ] A ○ᵈ μ A‖_[p, μ B₁ ○ᵈ μ B₂] < (μ_[ℝ] A ○ᵈ μ A) x := by
  obtain rfl | hA := A.eq_empty_or_nonempty
  · simp
  · simp [← card_smul_mu, -nsmul_eq_mul, smul_dddconv, dddconv_smul, wLpNorm_nsmul, hA.card_pos]

variable [DiscreteMeasurableSpace G]

set_option backward.isDefEq.respectTransparency false in
private lemma wLpNorm_dddconv_pos {p : ℕ} (hp : p ≠ 0) {B₁ B₂ A : Finset G}
    (hB : (B₁ ∩ B₂).Nonempty) (hA : A.Nonempty) :
    (0 : ℝ) < ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p := by
  rw [wLpNorm_pow_eq_sum_norm hp]
  refine sum_pos' (fun x _ ↦ by positivity) ⟨0, mem_univ _, smul_pos ?_ <| pow_pos ?_ _⟩
  · obtain ⟨b, hb⟩ := hB
    obtain ⟨hb₁, hb₂⟩ := mem_inter.mp hb
    rw [dddconv_eq_sum_sub']
    have hterm : 0 < μ_[ℝ≥0] B₁ b * conj (μ_[ℝ≥0] B₂ (b - 0)) := by
      simp only [sub_zero, conj_trivial, mu_apply, hb₁, hb₂, ite_true, mul_one]
      have h1 : 0 < #B₁ := Finset.card_pos.mpr ⟨b, hb₁⟩
      have h2 : 0 < #B₂ := Finset.card_pos.mpr ⟨b, hb₂⟩
      positivity
    exact hterm.trans_le
      (Finset.single_le_sum (f := fun t ↦ μ_[ℝ≥0] B₁ t * conj (μ_[ℝ≥0] B₂ (t - 0)))
        (fun _ _ ↦ _root_.zero_le) (mem_univ b))
  · obtain ⟨a, ha⟩ := hA
    have hpos_val : 0 < (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) 0 := by
      rw [dddconv_eq_sum_sub']
      have hterm : (0 : ℝ) < 𝟭_[(A : Set G), ℝ] a * conj (𝟭_[(A : Set G), ℝ] (a - 0)) := by
        simp [ha]
      exact hterm.trans_le
        (Finset.single_le_sum
          (f := fun y ↦ 𝟭_[(A : Set G), ℝ] y * conj (𝟭_[(A : Set G), ℝ] (y - 0)))
          (fun y _ ↦ mul_nonneg (Set.indicator_one_nonneg y)
            (by rw [conj_to_real]; exact Set.indicator_one_nonneg (y - 0)))
          (mem_univ a))
    exact norm_pos_iff.mpr hpos_val.ne'

set_option backward.isDefEq.respectTransparency false in
/-- Unconditional Dependent Random Choice on `(B₁, B₂)` without `sorried positivity extensions`. -/
lemma drc_bohr {p : ℕ} (hp₂ : 2 ≤ p) {B₁ B₂ A : Finset G} (f : G → ℝ≥0)
    (hB : (B₁ ∩ B₂).Nonempty) (hA : A.Nonempty) :
    ∃ A₁, A₁ ⊆ B₁ ∧ ∃ A₂, A₂ ⊆ B₂ ∧
      ⟪μ_[ℝ] A₁ ○ᵈ μ A₂, (↑) ∘ f⟫_[ℝ] * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p ≤
        2 * ∑ x, (μ_[ℝ] B₁ ○ᵈ μ B₂) x * (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x ^ p * f x ∧
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #A₁ / #B₁ ∧
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #A₂ / #B₂ := by
  have hB₁_ne : B₁.Nonempty := hB.mono inter_subset_left
  have hB₂_ne : B₂.Nonempty := hB.mono inter_subset_right
  have hp₀ : p ≠ 0 := by positivity
  have hnorm_pos := wLpNorm_dddconv_pos hp₀ hB hA
  set M : ℝ :=
    2⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p * (sqrt #B₁ * sqrt #B₂) / #A ^ p
      with hM_def
  have hM : 0 < M := by rw [hM_def]; positivity
  set A₁ := fun s ↦ B₁ ∩ cBohr p A s
  set A₂ := fun s ↦ B₂ ∩ cBohr p A s
  set g : (Fin p → G) → ℝ := fun s ↦ #(A₁ s) * #(A₂ s) with hg_def
  have hg : ∀ s, 0 ≤ g s := fun s ↦ by rw [hg_def]; dsimp; positivity
  have hgB : ∑ s, g s = #B₁ * #B₂ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p := by
    have hAdddconv : 0 ≤ 𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A] :=
      dddconv_nonneg' Set.indicator_one_nonneg Set.indicator_one_nonneg
    simpa only [wLpNorm_pow_eq_sum_norm hp₀, norm_of_nonneg (hAdddconv _), NNReal.smul_def,
      NNReal.coe_dddconv, NNReal.coe_comp_mu, wInner_one_eq_sum, Pi.one_apply, inner_apply',
      ← coe_inter, conj_to_real, mul_one, sum_dddconv, sum_indicator_one, nsmul_eq_mul,
      Nat.cast_mul, g, A₁, A₂] using! lemma_0_bohr p B₁ B₂ A 1
  have hg_sum_lt : ∑ s, g s < 2 * ∑ s with M ^ 2 ≤ g s, g s := by
    by_cases h : ∀ s, g s ≠ 0 → M ^ 2 ≤ g s
    · rw [← sum_filter_ne_zero (s := filter _ _), Finset.filter_comm,
        filter_true_of_mem fun s hs ↦ h s (mem_filter.1 hs).2, ← sum_filter_ne_zero]
      refine lt_mul_of_one_lt_left (sum_pos (fun s hs ↦ (h _ (mem_filter.1 hs).2).trans_lt' <|
        by positivity) ?_) one_lt_two
      rw [← sum_filter_ne_zero] at hgB
      exact nonempty_of_sum_ne_zero <| hgB.trans_ne <| by positivity
    push Not at h
    obtain ⟨s, hs⟩ := h
    suffices hlt : (2 : ℝ) * ∑ s with g s < M ^ 2, g s < ∑ s, g s by
      have hsplit : (2 : ℝ) * ∑ s with g s < M ^ 2, g s + 2 * ∑ s with M ^ 2 ≤ g s, g s =
          ∑ s, g s + ∑ s, g s := by
        simp_rw [← not_le, ← compl_filter, ← mul_add, sum_compl_add_sum, two_mul]
      linarith
    rw [← lt_div_iff₀' (zero_lt_two' ℝ), div_eq_inv_mul]
    calc
      ∑ s with g s < M ^ 2, g s = ∑ s with g s < M ^ 2 ∧ g s ≠ 0, sqrt (g s) * sqrt (g s) := by
        simp_rw [mul_self_sqrt (hg _), ← filter_filter, sum_filter_ne_zero]
      _ < ∑ s with g s < M ^ 2 ∧ g s ≠ 0, M * sqrt (g s) :=
        sum_lt_sum_of_nonempty ⟨s, mem_filter.2 ⟨mem_univ _, hs.symm⟩⟩ fun s' hs' ↦ by
          simp only [mem_filter, mem_univ, true_and] at hs'
          exact mul_lt_mul_of_pos_right ((sqrt_lt' hM).2 hs'.1) <|
            sqrt_pos.2 <| (hg _).lt_of_ne' hs'.2
      _ ≤ ∑ s, M * sqrt (g s) := sum_le_univ_sum_of_nonneg fun _ ↦ by positivity
      _ = M * (∑ s, sqrt #(A₁ s) * sqrt #(A₂ s)) := by
        simp_rw [mul_sum, g, sqrt_mul <| Nat.cast_nonneg _]
      _ ≤ M * (sqrt (∑ s, #(A₁ s)) * sqrt (∑ s, #(A₂ s))) := by
        gcongr; exact sum_sqrt_mul_sqrt_le _ (fun _ ↦ by positivity) fun _ ↦ by positivity
      _ = _ := by
        rw [sum_cast_cBohr, sum_cast_cBohr, sqrt_mul', sqrt_mul', mul_mul_mul_comm (sqrt _),
          mul_self_sqrt, ← mul_assoc, hM_def, div_mul_cancel₀, ← sqrt_mul, mul_assoc,
          mul_self_sqrt, hgB, mul_right_comm, mul_assoc]
        all_goals positivity
  have hcard_from_M {s : Fin p → G} (hsM : M ^ 2 ≤ g s) :
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #(A₁ s) / #B₁ ∧
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #(A₂ s) / #B₂ := by
    have hprod : (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) /
        #A ^ (2 * p) ≤ #(A₁ s) / #B₁ * (#(A₂ s) / #B₂) := by
      rw [div_mul_div_comm, le_div_iff₀ (by positivity)]
      simpa [hg_def, hM_def, mul_pow, div_pow, pow_mul', show (2 : ℝ) ^ 2 = 4 by norm_num,
        mul_div_right_comm] using hsM
    exact ⟨hprod.trans <| mul_le_of_le_one_right (by positivity) <|
      div_le_one_of_le₀ (Nat.cast_le.2 <| card_mono inter_subset_left) (by positivity),
      hprod.trans <| mul_le_of_le_one_left (by positivity) <|
      div_le_one_of_le₀ (Nat.cast_le.2 <| card_mono inter_subset_left) (by positivity)⟩
  have hrel (s : Fin p → G) : g s * ⟪μ_[ℝ] (A₁ s) ○ᵈ μ (A₂ s), (↑) ∘ f⟫_[ℝ] =
      ⟪𝟭_[(A₁ s : Set G), ℝ] ○ᵈ 𝟭_[A₂ s], (↑) ∘ f⟫_[ℝ] := by
    rw [hg_def]
    dsimp only
    rw [← card_smul_mu (K := ℝ) (A₁ s), ← card_smul_mu (K := ℝ) (A₂ s), smul_dddconv,
      dddconv_smul, ← Nat.cast_smul_eq_nsmul ℝ, ← Nat.cast_smul_eq_nsmul ℝ,
      wInner_smul_left, wInner_smul_left, smul_eq_mul, smul_eq_mul]
    simp only [star_trivial]
    ring
  set F_rhs : ℝ := ∑ x, (μ_[ℝ] B₁ ○ᵈ μ B₂) x * (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x ^ p * f x
  have hF_nonneg : 0 ≤ F_rhs := by
    refine Finset.sum_nonneg fun x _ ↦ mul_nonneg (mul_nonneg ?_ ?_) (by positivity)
    · exact dddconv_apply_nonneg' mu_nonneg mu_nonneg x
    · exact pow_nonneg (dddconv_apply_nonneg' Set.indicator_one_nonneg Set.indicator_one_nonneg x) _
  rcases eq_or_lt_of_le hF_nonneg with hF0 | hFpos
  · have hne_M : ({s : Fin p → G | M ^ 2 ≤ g s} : Finset _).Nonempty := by
      refine nonempty_of_sum_ne_zero (f := g) ?_
      have hpos_sum : 0 < ∑ s, g s := by rw [hgB]; positivity
      linarith
    obtain ⟨s, hs_mem⟩ := hne_M
    have hsM : M ^ 2 ≤ g s := (mem_filter.mp hs_mem).2
    have hsum_zero : ∑ s', ⟪𝟭_[(A₁ s' : Set G), ℝ] ○ᵈ 𝟭_[A₂ s'], (↑) ∘ f⟫_[ℝ] = 0 := by
      rw [lemma_0_bohr]
      change (#B₁ * #B₂) • F_rhs = 0
      rw [← hF0, smul_zero]
    have hterm_nonneg : ∀ s', 0 ≤ ⟪𝟭_[(A₁ s' : Set G), ℝ] ○ᵈ 𝟭_[A₂ s'], (↑) ∘ f⟫_[ℝ] := by
      intro s'
      rw [wInner_one_eq_sum]
      refine Finset.sum_nonneg fun x _ ↦ ?_
      simp only [Function.comp_apply, inner_apply', conj_to_real]
      exact mul_nonneg (dddconv_apply_nonneg' Set.indicator_one_nonneg Set.indicator_one_nonneg x)
        (by positivity)
    have hs_zero : ⟪𝟭_[(A₁ s : Set G), ℝ] ○ᵈ 𝟭_[A₂ s], (↑) ∘ f⟫_[ℝ] = 0 :=
      le_antisymm ((Finset.single_le_sum (fun s' _ ↦ hterm_nonneg s') (mem_univ s)).trans_eq
        hsum_zero) (hterm_nonneg s)
    have hgs_pos : 0 < g s := (pow_pos hM 2).trans_le hsM
    have hmu_zero : ⟪μ_[ℝ] (A₁ s) ○ᵈ μ (A₂ s), (↑) ∘ f⟫_[ℝ] = 0 := by
      nlinarith [hrel s, hs_zero]
    obtain ⟨hc₁, hc₂⟩ := hcard_from_M hsM
    refine ⟨A₁ s, inter_subset_left, A₂ s, inter_subset_left, ?_, hc₁, hc₂⟩
    rw [hmu_zero, zero_mul, ← hF0, mul_zero]
  · suffices hlt :
        ∑ s, ⟪𝟭_[(A₁ s : Set G), ℝ] ○ᵈ 𝟭_[A₂ s], (↑) ∘ f⟫_[ℝ] *
            ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p <
          ∑ s, 𝟭_[({s | M ^ 2 ≤ g s} : Finset _)] s * g s * (2 * F_rhs) by
      obtain ⟨s, -, hs⟩ := exists_lt_of_sum_lt hlt
      simp only [Set.indicator_apply, boole_mul] at hs
      split_ifs at hs with hsM; swap
      · simp only [zero_mul, wInner_one_eq_sum, Function.comp_apply, inner_apply',
          conj_to_real] at hs
        have hnn : 0 ≤ 𝟭_[(A₁ s : Set G), ℝ] ○ᵈ 𝟭_[A₂ s] :=
          dddconv_nonneg' Set.indicator_one_nonneg Set.indicator_one_nonneg
        cases hs.not_ge <|
          mul_nonneg (sum_nonneg fun x _ ↦ mul_nonneg (hnn x) <| by positivity) hnorm_pos.le
      have hsM' : M ^ 2 ≤ g s := by simpa using hsM
      obtain ⟨hc₁, hc₂⟩ := hcard_from_M hsM'
      have hgs_pos : 0 < g s := (pow_pos hM 2).trans_le hsM'
      refine ⟨A₁ s, inter_subset_left, A₂ s, inter_subset_left, ?_, hc₁, hc₂⟩
      refine (lt_of_mul_lt_mul_left (hs.trans_eq' ?_) hgs_pos.le).le
      rw [← mul_assoc, hrel s]
    have hlhs : ∑ s, ⟪𝟭_[(A₁ s : Set G), ℝ] ○ᵈ 𝟭_[A₂ s], (↑) ∘ f⟫_[ℝ] *
          ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p =
        F_rhs * ∑ s, g s := by
      rw [← sum_mul, lemma_0_bohr, nsmul_eq_mul, Nat.cast_mul]
      change (#B₁ * #B₂ : ℝ) * F_rhs * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p = _
      rw [hgB]; ring
    have hrhs : ∑ s, 𝟭_[({s | M ^ 2 ≤ g s} : Finset _)] s * g s * (2 * F_rhs) =
        F_rhs * (2 * ∑ s with M ^ 2 ≤ g s, g s) := by
      simp only [Set.indicator_apply, boole_mul, mem_coe, mem_filter, mem_univ, true_and,
        ← sum_mul, ← sum_filter]
      ring
    rw [hlhs, hrhs]
    exact mul_lt_mul_of_pos_left hg_sum_lt hFpos

set_option backward.isDefEq.respectTransparency false in
/-- Unconditional Bohr DRC sifting on `(B₁, B₂)` without `sorried positivity extensions`. -/
lemma sifting_bohr (B₁ B₂ : Finset G) {p : ℕ} {A : Finset G} {ε δ : ℝ}
    (hε : 0 < ε) (hε₁ : ε ≤ 1) (hδ : 0 < δ) (hp : Even p) (hp₂ : 2 ≤ p)
    (hpε : ε⁻¹ * log (2 / δ) ≤ p) (hB : (B₁ ∩ B₂).Nonempty) (hA : A.Nonempty) :
    ∃ A₁, A₁ ⊆ B₁ ∧ ∃ A₂, A₂ ⊆ B₂ ∧
      1 - δ ≤ ∑ x ∈ sBohr p ε B₁ B₂ A, (μ_[ℝ] A₁ ○ᵈ μ A₂) x ∧
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #A₁ / #B₁ ∧
      (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) / #A ^ (2 * p) ≤
        #A₂ / #B₂ := by
  obtain ⟨A₁, hAB₁, A₂, hAB₂, h, hcard₁, hcard₂⟩ :=
    drc_bohr hp₂ 𝟭_[(sBohr p ε B₁ B₂ A)ᶜ] hB hA
  refine ⟨A₁, hAB₁, A₂, hAB₂, ?_, hcard₁, hcard₂⟩
  have hp₀ : 0 < p := by positivity
  have hnorm_pos := wLpNorm_dddconv_pos hp₀.ne' hB hA
  have aux (c : Finset G) (r : ℝ)
      (hc : (4 : ℝ)⁻¹ * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ (2 * p) /
        #A ^ (2 * p) ≤ #c / r) : c.Nonempty := by
    simp_rw [nonempty_iff_ne_empty]
    rintro rfl
    simp [pow_mul', inv_mul_le_iff₀ (zero_lt_four' ℝ), div_nonpos_iff,
      (pow_pos hnorm_pos 2).not_ge, hp₀.ne', hA.ne_empty] at hc
  have hA₁ : A₁.Nonempty := aux _ _ hcard₁
  have hA₂ : A₂.Nonempty := aux _ _ hcard₂
  rw [sub_le_comm]
  calc
    1 - ∑ x ∈ sBohr p ε B₁ B₂ A, (μ_[ℝ] A₁ ○ᵈ μ A₂) x
      = ∑ x ∈ (sBohr p ε B₁ B₂ A)ᶜ, (μ_[ℝ] A₁ ○ᵈ μ A₂) x := by
        simp_rw [sub_eq_iff_eq_add', sum_add_sum_compl, sum_dddconv, map_mu]
        rw [sum_mu _ hA₁, sum_mu _ hA₂, one_mul]
    _ = ⟪μ_[ℝ] A₁ ○ᵈ μ A₂, (↑) ∘ 𝟭_[(sBohr (↑p) ε B₁ B₂ A)ᶜ, ℝ≥0]⟫_[ℝ] := by
        simp [wInner_one_eq_sum, -mem_compl, -mem_sBohr, Set.indicator_apply]
        simp only [← ite_not (_ ∈ sBohr p ε B₁ B₂ A), ← mem_compl, apply_ite]
        simp [-mem_compl]
    _ ≤ (2 * ∑ x, (μ_[ℝ] B₁ ○ᵈ μ B₂) x * (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x ^ p *
          (𝟭_[(sBohr (↑p) ε B₁ B₂ A)ᶜ, ℝ≥0] x : ℝ)) /
          ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p :=
        (le_div_iff₀ hnorm_pos).2 h
    _ ≤ δ := by
        rw [div_le_iff₀ hnorm_pos, ← le_div_iff₀' (zero_lt_two' ℝ)]
        simp only [apply_ite NNReal.toReal, Set.indicator_apply, NNReal.coe_one, NNReal.coe_zero,
          mul_boole, Fintype.sum_ite_mem, mul_div_right_comm, ← coe_compl, mem_coe]
        have hBconv : 0 ≤ μ_[ℝ] B₁ ○ᵈ μ B₂ := dddconv_nonneg' mu_nonneg mu_nonneg
        have hAconv : 0 ≤ 𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A] :=
          dddconv_nonneg' Set.indicator_one_nonneg Set.indicator_one_nonneg
        calc
          ∑ x ∈ (sBohr p ε B₁ B₂ A)ᶜ, (μ_[ℝ] B₁ ○ᵈ μ B₂) x * (𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]) x ^ p
            ≤ ∑ x ∈ (sBohr p ε B₁ B₂ A)ᶜ,
                (μ_[ℝ] B₁ ○ᵈ μ B₂) x *
                  ((1 - ε) * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂]) ^ p := by
              gcongr with x hx
              · exact hBconv x
              · exact hAconv x
              · simpa using hx
          _ ≤ ∑ x, (μ_[ℝ] B₁ ○ᵈ μ B₂) x *
                ((1 - ε) * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂]) ^ p := by
              gcongr
              · intro x _ _
                exact mul_nonneg (hBconv x) (hp.pow_nonneg _)
              · exact subset_univ _
          _ = ‖μ_[ℝ] B₁‖_[1] * ‖μ_[ℝ] B₂‖_[1] *
                ((1 - ε) ^ p * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p) := by
              simp_rw [← dL1Norm_dddconv mu_nonneg mu_nonneg, dL1Norm_eq_sum_norm,
                norm_of_nonneg (hBconv _), sum_mul, mul_pow]
          _ ≤ (1 - ε) ^ p * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p := by
              grw [dL1Norm_mu_le_one, dL1Norm_mu_le_one, one_mul, one_mul]
          _ ≤ δ / 2 * ‖𝟭_[(A : Set G), ℝ] ○ᵈ 𝟭_[A]‖_[p, μ B₁ ○ᵈ μ B₂] ^ p := by
              refine mul_le_mul_of_nonneg_right ?_ (hp.pow_nonneg _)
              calc
                (1 - ε) ^ p ≤ exp (-ε) ^ p := by gcongr; exact one_sub_le_exp_neg _
                _ = exp (-(ε * p)) := by rw [← neg_mul, exp_mul, rpow_natCast]
                _ ≤ exp (-log (2 / δ)) :=
                  exp_monotone <| neg_le_neg <| (inv_mul_le_iff₀ hε).1 hpε
                _ = δ / 2 := by rw [exp_neg, exp_log (by positivity), inv_div]

end BohrDRC

section ShellAndOrthogonality
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

omit [MeasurableSpace G] [DiscreteMeasurableSpace G] in
/-- Pointwise shell approximation for `(μ A ○ᵈ μ B.finset) x` on `(κ • B).finset`. -/
lemma abs_mu_dddconv_mu_bohr_sub {B : BohrSet G} (hreg : B.IsRegular)
    {A : Finset G} (hAB : A ⊆ B.finset) (hA : A.Nonempty)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1)
    {x : G} (hx : x ∈ (κ • B).finset) :
    |(μ_[ℝ] A ○ᵈ μ B.finset) x - (#B.finset : ℝ)⁻¹| ≤ 100 * B.rank * κ / #A := by
  rcases Nat.eq_zero_or_pos B.rank with hd0 | hd_pos
  · have hfreq : B.frequencies = ∅ := Finset.card_eq_zero.mp hd0
    have hB_univ : B.finset = Finset.univ := by
      ext z; simp [BohrSet.mem_finset, BohrSet.mem_chordSet_iff_nnnorm_width, hfreq]
    have hval : (μ_[ℝ] A ○ᵈ μ B.finset) x = (#B.finset : ℝ)⁻¹ := by
      rw [hB_univ, dddconv_eq_sum_sub']
      have hterm : ∀ y : G, μ_[ℝ] A y * conj (μ_[ℝ] Finset.univ (y - x)) =
          μ_[ℝ] A y * (#(Finset.univ : Finset G) : ℝ)⁻¹ := fun y ↦ by simp [mu_apply]
      simp_rw [hterm, ← Finset.sum_mul, sum_mu ℝ hA, one_mul]
    simp [hval, hd0]
  · have hd1 : (1 : ℝ) ≤ B.rank := Nat.one_le_cast.mpr hd_pos
    have hκ1 : κ ≤ 1 := by nlinarith
    let B_in := ((1 - κ) • B).finset
    have hsub_in : B_in ⊆ B.finset := by
      simpa [B_in, one_smul] using BohrSet.smul_finset_mono (by linarith) (by linarith : 1 - κ ≤ 1)
    have hA_pos : (0 : ℝ) < #A := by exact_mod_cast hA.card_pos
    have hB_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
    rw [le_div_iff₀ hA_pos]
    have hexpand : ((μ_[ℝ] A ○ᵈ μ B.finset) x - (#B.finset : ℝ)⁻¹) * #A =
        ∑ y ∈ A, (μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹) := by
      rw [sub_mul, dddconv_eq_sum_sub', Finset.sum_mul]
      have hsumA : ∑ y : G, μ_[ℝ] A y * conj (μ_[ℝ] B.finset (y - x)) * (#A : ℝ) =
          ∑ y ∈ A, μ_[ℝ] B.finset (y - x) := by
        rw [← Finset.sum_subset (Finset.subset_univ A)]
        · refine Finset.sum_congr rfl fun y hy ↦ ?_
          simp only [mu_apply, hy, ite_true, mul_one, conj_to_real]
          split_ifs
          · field_simp [hA_pos.ne']
          · simp
        · intro y _ hy; simp [mu_apply, hy]
      have hconst : (#B.finset : ℝ)⁻¹ * (#A : ℝ) = ∑ _y ∈ A, (#B.finset : ℝ)⁻¹ := by
        simp [mul_comm]
      rw [hsumA, hconst, ← Finset.sum_sub_distrib]
    rw [← abs_of_pos hA_pos, ← abs_mul, hexpand]
    have hzero_in : ∀ y ∈ B_in, μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹ = 0 := by
      intro y hy
      have hyx : y - x ∈ B.finset := by
        have hmem : y + (-x) ∈ ((1 - κ) • B).finset + (κ • B).finset :=
          Finset.add_mem_add hy (BohrSet.neg_mem_finset.mpr hx)
        have hsub := BohrSet.smul_add_smul_finset_subset (B := B) (by linarith) hκ₀ hmem
        simpa [sub_add_cancel, one_smul, ← sub_eq_add_neg] using hsub
      simp [mu_apply, hyx]
    have hpt : ∀ y : G, |μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹| ≤ (#B.finset : ℝ)⁻¹ := by
      intro y
      have hinv_nn : (0 : ℝ) ≤ (#B.finset : ℝ)⁻¹ := by positivity
      simp only [mu_apply, mul_boole]
      split_ifs <;> simp [abs_of_nonneg hinv_nn]
    calc
      |∑ y ∈ A, (μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹)|
        ≤ ∑ y ∈ A, |μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹| :=
          Finset.abs_sum_le_sum_abs _ _
      _ = ∑ y ∈ A \ B_in, |μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹| := by
          symm
          refine Finset.sum_subset sdiff_subset fun y hyA hy_not ↦ ?_
          rw [Finset.mem_sdiff, not_and_or, not_not] at hy_not
          rcases hy_not with h | hy_in
          · exact absurd hyA h
          · simp [hzero_in y hy_in]
      _ ≤ ∑ y ∈ B.finset \ B_in, |μ_[ℝ] B.finset (y - x) - (#B.finset : ℝ)⁻¹| :=
          Finset.sum_le_sum_of_subset_of_nonneg (sdiff_subset_sdiff hAB Subset.rfl)
            fun _ _ _ ↦ abs_nonneg _
      _ ≤ ∑ _y ∈ B.finset \ B_in, (#B.finset : ℝ)⁻¹ :=
          Finset.sum_le_sum fun y _ ↦ hpt y
      _ = ((#B.finset : ℝ) - (#B_in : ℝ)) * (#B.finset : ℝ)⁻¹ := by
          have hcs : (#(B.finset \ B_in) : ℝ) + (#B_in : ℝ) = (#B.finset : ℝ) := by
            exact_mod_cast Finset.card_sdiff_add_card_eq_card hsub_in
          have hcs' : (#(B.finset \ B_in) : ℝ) = (#B.finset : ℝ) - (#B_in : ℝ) := by linarith
          simp [hcs']
      _ ≤ (100 * B.rank * κ * (#B.finset : ℝ)) * (#B.finset : ℝ)⁻¹ := by
          gcongr
          have hlo := hreg.le_card_one_sub_smul hκ₀ hκ
          linarith
      _ = 100 * B.rank * κ := by field_simp [hB_pos.ne']

/-- Hölder lifting on a regular Bohr set (`hoelder-lifting` in the blueprint). -/
lemma hoelder_lifting {B : BohrSet G} (hreg : B.IsRegular)
    {A M C : Finset G} (hAB : A ⊆ B.finset) (hA : A.Nonempty)
    (hCM : C ⊆ M) {α_B γ ε κ : ℝ} (hα : α_B = (#A : ℝ) / #B.finset)
    (hγ₀ : 0 < γ) (hγC : γ * #M ≤ #C) (hM_ne : M.Nonempty)
    (hε₀ : 0 < ε) (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1)
    (hκ_small : 1200 * B.rank * κ ≤ ε * α_B)
    (hC_sub : C ⊆ (κ • B).finset)
    (hAC : ε ≤ |(#B.finset : ℝ) * ⟪μ_[ℝ] A ∗ᵈ μ A, μ C⟫_[ℝ] - 1|) :
    ε / (4 * #B.finset) ≤
      ‖(μ_[ℝ] A - μ B.finset) ∗ᵈ (μ A - μ B.finset)‖_[↑(2 * ⌈𝓛 γ⌉₊), μ M] := by
  have hM_pos : (0 : ℝ) < #M := by exact_mod_cast hM_ne.card_pos
  have hC_pos : (0 : ℝ) < #C := (mul_pos hγ₀ hM_pos).trans_le hγC
  have hC_ne : C.Nonempty := Finset.card_pos.mp (by exact_mod_cast hC_pos)
  have hC_le_M : (#C : ℝ) ≤ #M := by exact_mod_cast Finset.card_le_card hCM
  have hγ₁ : γ ≤ 1 := by nlinarith
  have hB_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
  have hA_pos : (0 : ℝ) < #A := by exact_mod_cast hA.card_pos
  let μA : G → ℝ := μ A
  let μB : G → ℝ := μ B.finset
  let μC : G → ℝ := μ C
  have hμB_sym : ∀ z : G, μB (-z) = μB z := fun z ↦ by
    have := congr_fun (conjneg_mu ℝ B.finset) z
    simpa [μB, conjneg_apply, BohrSet.neg_finset] using this
  have hcross_err : ∀ (S : Finset G), S.Nonempty → S ⊆ B.finset →
      |⟪μB ∗ᵈ μ_[ℝ] S, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| ≤ 200 * B.rank * κ / #S := by
    intro S hS_ne hSB
    have hS_pos : (0 : ℝ) < #S := by exact_mod_cast hS_ne.card_pos
    have hsym_eq : ⟪μB ∗ᵈ μ_[ℝ] S, μC⟫_[ℝ] = ∑ y : G, μ_[ℝ] S y * (μB ∗ᵈ μC) y := by
      rw [wInner_one_eq_sum]
      simp only [inner_apply', conj_to_real]
      simp_rw [ddconv_eq_sum_sub μB (μ_[ℝ] S), ddconv_eq_sum_sub μB μC,
        Finset.sum_mul, Finset.mul_sum]
      rw [Finset.sum_comm]
      refine Finset.sum_congr rfl fun y _ ↦ Finset.sum_congr rfl fun x _ ↦ ?_
      have hxy : μB (x - y) = μB (y - x) := by rw [← hμB_sym (y - x), neg_sub]
      rw [hxy]; ring
    have hbase : ∑ y : G, μ_[ℝ] S y * μB y = (#B.finset : ℝ)⁻¹ := by
      have h1 : ∑ y : G, μ_[ℝ] S y * μB y = ∑ y ∈ S, (#S : ℝ)⁻¹ * (#B.finset : ℝ)⁻¹ := by
        rw [← Finset.sum_subset (Finset.subset_univ S)]
        · exact Finset.sum_congr rfl fun y hy ↦ by simp [μB, mu_apply, hy, hSB hy]
        · intro y _ hy; simp [mu_apply, hy]
      rw [h1, Finset.sum_const, nsmul_eq_mul, ← mul_assoc, mul_inv_cancel₀ hS_pos.ne', one_mul]
    rw [hsym_eq, ← hbase, ← Finset.sum_sub_distrib]
    have hfactor : ∀ y : G, μ_[ℝ] S y * (μB ∗ᵈ μC) y - μ_[ℝ] S y * μB y =
        μ_[ℝ] S y * ((μB ∗ᵈ μC - μB) y) := fun _ ↦ (mul_sub _ _ _).symm
    simp_rw [hfactor]
    calc
      |∑ y : G, μ_[ℝ] S y * ((μB ∗ᵈ μC - μB) y)|
        ≤ ∑ y : G, |μ_[ℝ] S y * ((μB ∗ᵈ μC - μB) y)| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ y : G, (#S : ℝ)⁻¹ * |(μB ∗ᵈ μC - μB) y| := by
          refine Finset.sum_le_sum fun y _ ↦ ?_
          rw [abs_mul, abs_of_nonneg (mu_nonneg y)]
          refine mul_le_mul_of_nonneg_right ?_ (abs_nonneg _)
          simp only [mu_apply, mul_boole]; split_ifs <;> simp [inv_nonneg.mpr hS_pos.le]
      _ = (#S : ℝ)⁻¹ * ‖μB ∗ᵈ μC - μB‖_[1] := by
          rw [← Finset.mul_sum, dL1Norm_eq_sum_norm]; rfl
      _ ≤ (#S : ℝ)⁻¹ * (200 * B.rank * κ) := by
          gcongr
          exact hreg.dL1Norm_mu_ddconv_sub_le hκ₀ hκ mu_nonneg (sum_mu ℝ hC_ne)
            (fun y hy ↦ hC_sub (by simpa [μC] using hy))
      _ = 200 * B.rank * κ / #S := by ring
  have herrA : |⟪μB ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| ≤ 200 * B.rank * κ / #A :=
    hcross_err A hA hAB
  have herrB : |⟪μB ∗ᵈ μB, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| ≤ 200 * B.rank * κ / #B.finset :=
    hcross_err B.finset B.finset_nonempty Subset.rfl
  let G_fn : G → ℝ := (μA - μB) ∗ᵈ (μA - μB)
  have hexp_inner : ⟪G_fn, μC⟫_[ℝ] =
      ⟪μA ∗ᵈ μA, μC⟫_[ℝ] - 2 * ⟪μB ∗ᵈ μA, μC⟫_[ℝ] + ⟪μB ∗ᵈ μB, μC⟫_[ℝ] := by
    have hconv_exp : G_fn = μA ∗ᵈ μA - (μB ∗ᵈ μA + μB ∗ᵈ μA) + μB ∗ᵈ μB := by
      dsimp [G_fn]
      rw [sub_ddconv, ddconv_sub, ddconv_sub, ddconv_comm μA μB]
      ext x; simp [Pi.sub_apply, Pi.add_apply]; ring
    rw [hconv_exp, wInner_add_left, wInner_sub_left, wInner_add_left]
    ring
  have hinner_ge : ε / (2 * #B.finset) ≤ |⟪G_fn, μC⟫_[ℝ]| := by
    have hA_le_B : (#A : ℝ) ≤ #B.finset := by exact_mod_cast Finset.card_le_card hAB
    have herrB' : |⟪μB ∗ᵈ μB, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| ≤ 200 * B.rank * κ / #A :=
      herrB.trans (div_le_div_of_nonneg_left (by positivity) hA_pos hA_le_B)
    have hdiff : |⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹)| ≤
        600 * B.rank * κ / #A := by
      have hrew : ⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹) =
          -2 * (⟪μB ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹) +
            (⟪μB ∗ᵈ μB, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹) := by
        rw [hexp_inner]; ring
      have h600_eq : 600 * (B.rank : ℝ) * κ / #A =
          2 * (200 * B.rank * κ / #A) + 200 * B.rank * κ / #A := by ring
      rw [hrew, h600_eq]
      refine (abs_add_le _ _).trans ?_
      rw [abs_mul, show |(-2 : ℝ)| = 2 by norm_num]
      linarith
    have htarget : ε / #B.finset ≤ |⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| := by
      rw [div_le_iff₀ hB_pos]
      have hmul_id : (#B.finset : ℝ) * ⟪μA ∗ᵈ μA, μC⟫_[ℝ] - 1 =
          (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹) * #B.finset := by
        field_simp [hB_pos.ne']
      have hmul : |(#B.finset : ℝ) * ⟪μA ∗ᵈ μA, μC⟫_[ℝ] - 1| =
          |⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| * #B.finset := by
        rw [hmul_id, abs_mul, abs_of_pos hB_pos]
      dsimp [μA, μC] at hmul ⊢
      linarith
    have h600 : 600 * B.rank * κ / #A ≤ ε / (2 * #B.finset) := by
      rw [div_le_div_iff₀ hA_pos (by positivity)]
      have hα_mul : α_B * #B.finset = #A := by rw [hα, div_mul_cancel₀ _ hB_pos.ne']
      nlinarith
    have htri : |⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹| ≤
        |⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹)| + |⟪G_fn, μC⟫_[ℝ]| := by
      have h_id : ⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹ =
          -(⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹)) + ⟪G_fn, μC⟫_[ℝ] := by
        ring
      calc
        |⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹|
          = |-(⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹)) + ⟪G_fn, μC⟫_[ℝ]| :=
            congr_arg abs h_id
        _ ≤ |-(⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹))| + |⟪G_fn, μC⟫_[ℝ]| :=
            abs_add_le _ _
        _ = |⟪G_fn, μC⟫_[ℝ] - (⟪μA ∗ᵈ μA, μC⟫_[ℝ] - (#B.finset : ℝ)⁻¹)| + |⟪G_fn, μC⟫_[ℝ]| := by
            rw [abs_neg]
    have hhalf : ε / #B.finset - ε / (2 * #B.finset) = ε / (2 * #B.finset) := by ring
    linarith
  set p := 2 * ⌈𝓛 γ⌉₊
  have hp1 : 1 < p :=
    Nat.succ_le_iff.1 (le_mul_of_one_le_right zero_le_two <|
      Nat.ceil_pos.2 <| BohrFourier.curlog_pos hγ₀.le hγ₁)
  have hp_ne : p ≠ 0 := by omega
  have hp'' : (p : ℝ≥0).HolderConjugate _ := .conjExponent <| mod_cast hp1
  have : (p : ℝ≥0∞).HolderConjugate _ := hp''.coe_ennreal
  let G_M : G → ℝ := fun x ↦ if x ∈ M then G_fn x else 0
  have hinner_M : ⟪G_fn, μC⟫_[ℝ] = ⟪G_M, μC⟫_[ℝ] := by
    simp only [wInner_one_eq_sum, inner_apply', conj_to_real]
    refine Finset.sum_congr rfl fun x _ ↦ ?_
    by_cases hxC : x ∈ C
    · simp [G_M, hCM hxC]
    · simp [μC, mu_apply, hxC]
  have hGM_norm : ‖G_M‖_[p] = (#M : ℝ) ^ ((p : ℝ)⁻¹) * ‖G_fn‖_[p, μ M] := by
    have hp_pos_real : (0 : ℝ) < p := by exact_mod_cast (Nat.zero_lt_of_lt hp1)
    have hpow_eq : ‖G_M‖_[p] ^ p = (#M : ℝ) * ‖G_fn‖_[p, μ M] ^ p := by
      rw [dLpNorm_pow_eq_sum_norm hp_ne, wLpNorm_pow_eq_sum_norm hp_ne]
      simp only [NNReal.smul_def, smul_eq_mul, NNReal.coe_mu]
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun x _ ↦ ?_
      by_cases hxM : x ∈ M
      · simp [G_M, hxM, mu_apply, mul_inv_cancel_left₀ hM_pos.ne']
      · simp [G_M, hxM, mu_apply, hp_ne]
    have h1 := congr_arg (fun t : ℝ ↦ t ^ ((p : ℝ)⁻¹)) hpow_eq
    rw [← rpow_natCast, ← rpow_mul (by positivity), mul_inv_cancel₀ hp_pos_real.ne', rpow_one,
      mul_rpow hM_pos.le (by positivity), ← rpow_natCast, ← rpow_mul (by positivity),
      mul_inv_cancel₀ hp_pos_real.ne', rpow_one] at h1
    exact h1
  have hμC_norm : ‖μC‖_[NNReal.conjExponent p] = (#C : ℝ) ^ (-(p : ℝ)⁻¹) := by
    rw [dLpNorm_mu hp''.symm.lt.le hC_ne, hp''.symm.coe.inv_sub_one, NNReal.coe_natCast]
  have hratio_le : (#M : ℝ) ^ ((p : ℝ)⁻¹) * (#C : ℝ) ^ (-(p : ℝ)⁻¹) ≤ 2 := by
    have hrew : (#M : ℝ) ^ ((p : ℝ)⁻¹) * (#C : ℝ) ^ (-(p : ℝ)⁻¹) =
        ((#M : ℝ) / #C) ^ ((p : ℝ)⁻¹) := by
      rw [div_eq_mul_inv, mul_rpow hM_pos.le (by positivity), inv_rpow hC_pos.le,
        rpow_neg hC_pos.le]
    rw [hrew]
    have hMC_le : (#M : ℝ) / #C ≤ γ⁻¹ := by
      rw [div_le_iff₀ hC_pos]
      have := mul_le_mul_of_nonneg_left hγC (inv_nonneg.mpr hγ₀.le)
      rwa [inv_mul_cancel_left₀ hγ₀.ne'] at this
    calc
      ((#M : ℝ) / #C) ^ ((p : ℝ)⁻¹)
        ≤ γ⁻¹ ^ ((p : ℝ)⁻¹) := rpow_le_rpow (by positivity) hMC_le (by positivity)
      _ = √(γ⁻¹ ^ ((↑⌈1 + log γ⁻¹⌉₊)⁻¹ : ℝ)) := by
          unfold p
          push_cast
          rw [mul_inv_rev, rpow_mul (by positivity), sqrt_eq_rpow, one_div]
      _ ≤ √(γ⁻¹ ^ ((1 + log γ⁻¹)⁻¹ : ℝ)) := by
          have : 1 ≤ γ⁻¹ := (one_le_inv₀ hγ₀).2 hγ₁
          have : 0 < 𝓛 γ := BohrFourier.curlog_pos hγ₀.le hγ₁
          grw [← Nat.le_ceil]
      _ ≤ √(exp 1) := by gcongr; exact rpow_inv_neg_curlog_le hγ₀.le hγ₁
      _ ≤ √2.7182818286 := by gcongr; exact exp_one_lt_d9.le
      _ ≤ 2 := by rw [sqrt_le_iff]; norm_num
  have hhoelder : |⟪G_fn, μC⟫_[ℝ]| ≤ 2 * ‖G_fn‖_[p, μ M] := by
    rw [hinner_M]
    calc
      |⟪G_M, μC⟫_[ℝ]| ≤ ‖G_M‖_[p] * ‖μC‖_[NNReal.conjExponent p] :=
        abs_wInner_one_le_dLpNorm_mul_dLpNorm _ _
      _ = ((#M : ℝ) ^ ((p : ℝ)⁻¹) * (#C : ℝ) ^ (-(p : ℝ)⁻¹)) * ‖G_fn‖_[p, μ M] := by
        rw [hGM_norm, hμC_norm]; ring
      _ ≤ 2 * ‖G_fn‖_[p, μ M] :=
        mul_le_mul_of_nonneg_right hratio_le (by positivity)
  have hdiv4 : ε / (4 * #B.finset) = (ε / (2 * #B.finset)) / 2 := by ring
  rw [hdiv4, div_le_iff₀ (zero_lt_two' ℝ)]
  linarith

/-- `L^p` orthogonality + unbalancing on a regular Bohr set (`Lp-orth` in the blueprint). -/
lemma Lp_orth {B : BohrSet G} (hreg : B.IsRegular)
    {A : Finset G} (hAB : A ⊆ B.finset) (hA : A.Nonempty)
    {p : ℕ} (hp : p ≠ 0) {α_B ε₀ κ_ν : ℝ}
    (hα : α_B = (#A : ℝ) / #B.finset)
    (hε₀ : 0 < ε₀) (hε₁ : ε₀ ≤ 1)
    (hκ₀ : 0 ≤ κ_ν) (hκ : 100 * (B.rank : ℝ) * κ_ν ≤ 1)
    (hκ_small : 1200 * B.rank * κ_ν ≤ ε₀ * α_B)
    {ν : G → ℝ≥0} {h : G → ℂ} (hν_pd : h ○ᵈ h = (↑) ∘ ν) (hν₁ : ∑ x, ν x = 1)
    (hν_supp : ∀ x, ν x ≠ 0 → x ∈ (κ_ν • B).finset)
    (hnorm_ge : ε₀ ≤ (#B.finset : ℝ) * ‖(μ_[ℝ] A - μ B.finset) ○ᵈ (μ A - μ B.finset)‖_[p, ν]) :
    ∃ p' : ℕ, 1 ≤ p' ∧ (p' : ℝ) ≤ 2 ^ 10 * ε₀⁻¹ ^ 2 * p ∧
      1 + ε₀ / 4 ≤ (#B.finset : ℝ) * ‖μ_[ℝ] A ○ᵈ μ A‖_[p', ν] := by
  have hB_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
  have hA_pos : (0 : ℝ) < #A := by exact_mod_cast hA.card_pos
  let f : G → ℝ := #B.finset • ((μ_[ℝ] A - μ B.finset) ○ᵈ (μ A - μ B.finset))
  let g : G → ℂ := fun x ↦ ((sqrt (#B.finset : ℝ) * (μ_[ℝ] A x - μ B.finset x) : ℝ) : ℂ)
  have hf_pd : g ○ᵈ g = (↑) ∘ f := by
    ext x
    rw [Function.comp_apply]
    dsimp only [f, Pi.smul_apply]
    rw [nsmul_eq_mul]
    rw [dddconv_eq_sum_sub' g g,
      dddconv_eq_sum_sub' (μ_[ℝ] A - μ_[ℝ] B.finset) (μ_[ℝ] A - μ_[ℝ] B.finset),
      Complex.ofReal_mul, Complex.ofReal_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl fun y _ ↦ ?_
    have hsq : ((sqrt (#B.finset : ℝ) : ℂ) * (sqrt (#B.finset : ℝ) : ℂ)) =
        ((#B.finset : ℝ) : ℂ) := by
      norm_cast
      exact mul_self_sqrt hB_pos.le
    dsimp only [g, Pi.sub_apply]
    have hconj_r : conj (μ_[ℝ] A (y - x) - μ B.finset (y - x)) =
        μ_[ℝ] A (y - x) - μ B.finset (y - x) := star_trivial _
    rw [hconj_r, Complex.ofReal_mul, Complex.ofReal_mul, Complex.ofReal_mul, map_mul,
      Complex.conj_ofReal, Complex.conj_ofReal]
    calc
      ((sqrt (#B.finset : ℝ) : ℂ) * ((μ_[ℝ] A y - μ B.finset y : ℝ) : ℂ)) *
          ((sqrt (#B.finset : ℝ) : ℂ) * ((μ_[ℝ] A (y - x) - μ B.finset (y - x) : ℝ) : ℂ))
        = ((sqrt (#B.finset : ℝ) : ℂ) * (sqrt (#B.finset : ℝ) : ℂ)) *
            (((μ_[ℝ] A y - μ B.finset y : ℝ) : ℂ) *
              ((μ_[ℝ] A (y - x) - μ B.finset (y - x) : ℝ) : ℂ)) := by ring
      _ = ((#B.finset : ℝ) : ℂ) * (((μ_[ℝ] A y - μ B.finset y : ℝ) : ℂ) *
            ((μ_[ℝ] A (y - x) - μ B.finset (y - x) : ℝ) : ℂ)) := by rw [hsq]
  have hf_norm : ε₀ ≤ ‖f‖_[p, ν] := by
    dsimp [f]
    rw [wLpNorm_nsmul, nsmul_eq_mul]
    exact hnorm_ge
  obtain ⟨p', hp'upper, hunb⟩ :=
    unbalancing' p hp ε₀ hε₀ hε₁ ν f g h hf_pd hν_pd hν₁ hf_norm
  have hp'pos : 1 ≤ p' := by
    by_contra! hp'0
    interval_cases p'
    simp at hunb
    linarith
  have hp'ne : p' ≠ 0 := by omega
  let target : G → ℝ := #B.finset • (μ_[ℝ] A ○ᵈ μ A)
  let target_mod : G → ℝ := fun x ↦ if ν x = 0 then f x + 1 else target x
  have hpt_err : ∀ x : G, |(f x + 1) - target_mod x| ≤ ε₀ / 4 := by
    intro x
    by_cases hνx : ν x = 0
    · simp only [target_mod, hνx, ite_true, sub_self, abs_zero]
      positivity
    · simp only [target_mod, hνx, ite_false]
      have hx_in : x ∈ (κ_ν • B).finset := hν_supp x hνx
      have hnx_in : -x ∈ (κ_ν • B).finset := BohrSet.neg_mem_finset.mpr hx_in
      have h1 := abs_mu_dddconv_mu_bohr_sub hreg hAB hA hκ₀ hκ hx_in
      have h2_raw := abs_mu_dddconv_mu_bohr_sub hreg hAB hA hκ₀ hκ hnx_in
      have h2 : |(μ_[ℝ] B.finset ○ᵈ μ A) x - (#B.finset : ℝ)⁻¹| ≤ 100 * B.rank * κ_ν / #A := by
        have hsym : (μ_[ℝ] B.finset ○ᵈ μ A) x = (μ_[ℝ] A ○ᵈ μ B.finset) (-x) := by
          simp only [dddconv_eq_sum_sub', conj_to_real]
          refine Finset.sum_bij (fun y _ ↦ y - x)
            (fun _ _ ↦ mem_univ _)
            (fun _ _ _ _ h ↦ sub_left_inj.mp h)
            (fun z _ ↦ ⟨z + x, mem_univ _, add_sub_cancel_right z x⟩)
            (fun y _ ↦ by
              have harg : y - x - -x = y := by abel
              rw [harg, mul_comm])
        rwa [hsym]
      have h3_raw := abs_mu_dddconv_mu_bohr_sub hreg Subset.rfl B.finset_nonempty hκ₀ hκ hx_in
      have hA_le_B : (#A : ℝ) ≤ #B.finset := by exact_mod_cast Finset.card_le_card hAB
      have h3 : |(μ_[ℝ] B.finset ○ᵈ μ B.finset) x - (#B.finset : ℝ)⁻¹| ≤
          100 * B.rank * κ_ν / #A :=
        h3_raw.trans (div_le_div_of_nonneg_left (by positivity) hA_pos hA_le_B)
      set e₁ : ℝ := (μ_[ℝ] A ○ᵈ μ B.finset) x - (#B.finset : ℝ)⁻¹
      set e₂ : ℝ := (μ_[ℝ] B.finset ○ᵈ μ A) x - (#B.finset : ℝ)⁻¹
      set e₃ : ℝ := (μ_[ℝ] B.finset ○ᵈ μ B.finset) x - (#B.finset : ℝ)⁻¹
      have hexp_pt : (f x + 1) - target x = (#B.finset : ℝ) * (-e₁ - e₂ + e₃) := by
        have hddd : ((μ_[ℝ] A - μ B.finset) ○ᵈ (μ A - μ B.finset)) x =
            (μ_[ℝ] A ○ᵈ μ A) x - (μ_[ℝ] A ○ᵈ μ B.finset) x -
              (μ_[ℝ] B.finset ○ᵈ μ A) x + (μ_[ℝ] B.finset ○ᵈ μ B.finset) x := by
          rw [sub_dddconv, dddconv_sub, dddconv_sub]
          simp only [Pi.sub_apply]
          ring
        dsimp [f, target, e₁, e₂, e₃]
        rw [nsmul_eq_mul, nsmul_eq_mul, hddd]
        field_simp [hB_pos.ne']
        ring
      rw [hexp_pt, abs_mul, abs_of_pos hB_pos]
      have hsum3 : |-e₁ - e₂ + e₃| ≤ 300 * B.rank * κ_ν / #A := by
        have ht1 := abs_add_le (-e₁ - e₂) e₃
        have ht2 : |-e₁ - e₂| ≤ |e₁| + |e₂| := by
          rw [show -e₁ - e₂ = -(e₁ + e₂) by ring, abs_neg]
          exact abs_add_le e₁ e₂
        have h300_eq : 300 * (B.rank : ℝ) * κ_ν / #A =
            100 * B.rank * κ_ν / #A + 100 * B.rank * κ_ν / #A + 100 * B.rank * κ_ν / #A := by
          ring
        rw [h300_eq]
        linarith
      calc
        (#B.finset : ℝ) * |-e₁ - e₂ + e₃|
          ≤ (#B.finset : ℝ) * (300 * B.rank * κ_ν / #A) :=
            mul_le_mul_of_nonneg_left hsum3 hB_pos.le
        _ ≤ ε₀ / 4 := by
            rw [mul_div_assoc', div_le_iff₀ hA_pos]
            have hα_mul : α_B * #B.finset = #A := by rw [hα, div_mul_cancel₀ _ hB_pos.ne']
            nlinarith
  have hmod_norm : ‖target_mod‖_[p', ν] = ‖target‖_[p', ν] := by
    rw [wLpNorm_eq_sum_norm (mod_cast hp'ne) (ENNReal.natCast_ne_top p'),
      wLpNorm_eq_sum_norm (mod_cast hp'ne) (ENNReal.natCast_ne_top p')]
    congr 1
    refine Finset.sum_congr rfl fun x _ ↦ ?_
    by_cases hνx : ν x = 0
    · simp [hνx]
    · simp [target_mod, hνx]
  have hdiff_norm : ‖(f + 1) - target_mod‖_[p', ν] ≤ ε₀ / 4 := by
    calc
      ‖(f + 1) - target_mod‖_[p', ν]
        = ‖fun x ↦ |(f x + 1) - target_mod x|‖_[p', ν] := by
          rw [wLpNorm_eq_sum_norm (mod_cast hp'ne) (ENNReal.natCast_ne_top p'),
            wLpNorm_eq_sum_norm (mod_cast hp'ne) (ENNReal.natCast_ne_top p')]
          simp [Pi.sub_apply, Pi.add_apply]
      _ ≤ ‖fun _ : G ↦ ε₀ / 4‖_[p', ν] :=
          wLpNorm_mono (fun _ ↦ abs_nonneg _) hpt_err
      _ = ε₀ / 4 := by
          have h1 := wLpNorm_smul (ε₀ / 4) (1 : G → ℝ) p' ν
          have hone : ‖(1 : G → ℝ)‖_[p', ν] = 1 := by
            rw [wLpNorm_one (mod_cast hp'ne) (ENNReal.natCast_ne_top p'), hν₁]
            simp
          have hfn : (ε₀ / 4) • (1 : G → ℝ) = fun _ ↦ ε₀ / 4 := by ext; simp
          rw [← hfn, h1, hone, mul_one, coe_nnNorm, Real.norm_of_nonneg (by positivity)]
  have htri_lp : ‖f + 1‖_[p', ν] ≤ ‖target_mod‖_[p', ν] + ‖(f + 1) - target_mod‖_[p', ν] := by
    have := wLpNorm_add_le (p := (p' : ℝ≥0∞)) (mod_cast hp'pos) ν target_mod ((f + 1) - target_mod)
    simpa [add_sub_cancel] using this
  have htarget_norm : ‖target‖_[p', ν] = (#B.finset : ℝ) * ‖μ_[ℝ] A ○ᵈ μ A‖_[p', ν] := by
    dsimp [target]
    rw [wLpNorm_nsmul, nsmul_eq_mul]
  refine ⟨p', hp'pos, hp'upper, ?_⟩
  linarith

end ShellAndOrthogonality

private lemma prop_it_bounds {rk d p' q' : ℕ} {α_U α_sift ε₁ : ℝ}
    (hα₀ : 0 < α_U) (hα₁ : α_U ≤ 1)
    (hε₁₀ : 0 < ε₁) (hε₁₁ : ε₁ ≤ 1)
    (hp' : 1 ≤ p') (hq'_ne : q' ≠ 0)
    (hq'_upper : (q' : ℝ) ≤ 2 ^ 9 * (p' : ℝ) / ε₁ ^ 2)
    (hα_sift_def : α_sift = 4⁻¹ * α_U ^ (2 * q'))
    (hrk : (rk : ℝ) ≤ d + 2 ^ 44 * 𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4) :
    (rk : ℝ) ≤ d + 2 ^ 128 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12 ∧
    exp (-2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U + log (d + 1 : ℝ)) +
      (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 / ε₁ ^ 14)) ≤
      exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε₁ / 8 * α_sift / (d + 1 : ℝ)) +
        (𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4) * 𝓛 (ε₁ / 8 * α_sift * α_sift))) := by
  have hLα : 1 ≤ 𝓛 α_U := BohrFourier.one_le_curlog hα₀.le hα₁
  have hα_sift₀ : 0 < α_sift := by rw [hα_sift_def]; positivity
  have hα_sift₁ : α_sift ≤ 1 := by
    rw [hα_sift_def]
    have : α_U ^ (2 * q') ≤ 1 := pow_le_one₀ hα₀.le hα₁
    linarith
  have hL_sift_nn : 0 ≤ 𝓛 α_sift :=
    zero_le_one.trans (BohrFourier.one_le_curlog hα_sift₀.le hα_sift₁)
  have hL_sift : 𝓛 α_sift ≤ 8 * (q' : ℝ) * 𝓛 α_U := by
    rw [hα_sift_def]
    have hpow_le := BohrFourier.curlog_pow_le (x := α_U) (mul_ne_zero two_ne_zero hq'_ne)
    calc
      𝓛 (4⁻¹ * α_U ^ (2 * q'))
        ≤ (4⁻¹ : ℝ)⁻¹ * 𝓛 (α_U ^ (2 * q')) :=
          BohrFourier.curlog_mul_le (by norm_num) (by norm_num) (by positivity)
            (pow_le_one₀ hα₀.le hα₁)
      _ ≤ (4⁻¹ : ℝ)⁻¹ * ((2 * q' : ℕ) * 𝓛 α_U) :=
          mul_le_mul_of_nonneg_left hpow_le (by positivity)
      _ = 8 * (q' : ℝ) * 𝓛 α_U := by push_cast; ring
  refine ⟨?_, exp_le_exp.mpr ?_⟩
  · calc
      (rk : ℝ)
        ≤ d + 2 ^ 44 * 𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4 := hrk
      _ = d + 2 ^ 56 * 𝓛 α_sift ^ 4 / ε₁ ^ 4 := by ring
      _ ≤ d + 2 ^ 56 * (8 * (q' : ℝ) * 𝓛 α_U) ^ 4 / ε₁ ^ 4 := by gcongr
      _ = d + 2 ^ 68 * (q' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 4 := by ring
      _ ≤ d + 2 ^ 68 * (2 ^ 9 * (p' : ℝ) / ε₁ ^ 2) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 4 := by gcongr
      _ = d + 2 ^ 104 * ((p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12) := by ring
      _ ≤ d + 2 ^ 128 * ((p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12) := by
          gcongr <;> norm_num
      _ = d + 2 ^ 128 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12 := by ring
  · have hp'1 : (1 : ℝ) ≤ p' := by exact_mod_cast hp'
    have hL_eps : 𝓛 (ε₁ / 8) ≤ 9 / ε₁ := by
      have h1 : log ((ε₁ / 8)⁻¹) ≤ (ε₁ / 8)⁻¹ := Real.log_le_self (by positivity)
      have h2 : (ε₁ / 8)⁻¹ = 8 / ε₁ := by ring
      have h3 : (1 : ℝ) ≤ 1 / ε₁ := (le_div_iff₀ hε₁₀).mpr (by linarith)
      have h9_eq : 9 / ε₁ = 8 / ε₁ + 1 / ε₁ := by ring
      linarith
    have hL_d : 𝓛 ((d + 1 : ℝ)⁻¹) = 1 + log (d + 1 : ℝ) := by simp
    have hq'_part : 8 * (q' : ℝ) * 𝓛 α_U ≤ 2 ^ 12 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) := by
      calc
        8 * (q' : ℝ) * 𝓛 α_U ≤ 8 * (2 ^ 9 * (p' : ℝ) / ε₁ ^ 2) * 𝓛 α_U := by gcongr
        _ = 2 ^ 12 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) := by ring
    have hpL : 1 ≤ (p' : ℝ) * 𝓛 α_U := one_le_mul_of_one_le_of_one_le hp'1 hLα
    have hterm1 : 𝓛 (ε₁ / 8 * α_sift / (d + 1 : ℝ)) ≤
        2 ^ 13 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U + log (d + 1 : ℝ)) := by
      have hrew : ε₁ / 8 * α_sift / (d + 1 : ℝ) = (ε₁ / 8) * α_sift * (d + 1 : ℝ)⁻¹ := by ring
      rw [hrew]
      have hadd1 := curlog_mul_add (by positivity : 0 < (ε₁ / 8) * α_sift)
        (by positivity : 0 < (d + 1 : ℝ)⁻¹)
      have hadd2 := curlog_mul_add (by positivity : 0 < ε₁ / 8) hα_sift₀
      have h9 : 9 / ε₁ + 1 ≤ 10 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) := by
        have ha : 9 / ε₁ + 1 ≤ 10 / ε₁ ^ 2 := by
          rw [div_add_one hε₁₀.ne', div_le_div_iff₀ hε₁₀ (by positivity)]; nlinarith
        exact ha.trans (by
          rw [show 10 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) =
            (10 / ε₁ ^ 2) * ((p' : ℝ) * 𝓛 α_U) by ring]
          exact le_mul_of_one_le_right (by positivity) hpL)
      have hlog_nn : 0 ≤ log (d + 1 : ℝ) := log_nonneg (by linarith [Nat.cast_nonneg (α := ℝ) d])
      linarith
    have hterm2_L : 𝓛 (ε₁ / 8 * α_sift * α_sift) ≤ 2 ^ 14 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) := by
      have hadd1 := curlog_mul_add (by positivity : 0 < ε₁ / 8 * α_sift) hα_sift₀
      have hadd2 := curlog_mul_add (by positivity : 0 < ε₁ / 8) hα_sift₀
      have h9 : 9 / ε₁ ≤ 9 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) := by
        have ha : 9 / ε₁ ≤ 9 / ε₁ ^ 2 := by
          rw [div_le_div_iff₀ hε₁₀ (by positivity)]; nlinarith
        exact ha.trans (by
          rw [show 9 * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U) = (9 / ε₁ ^ 2) * ((p' : ℝ) * 𝓛 α_U) by ring]
          exact le_mul_of_one_le_right (by positivity) hpL)
      linarith
    have hterm2_front : 𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4 ≤
        2 ^ 60 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12 := by
      calc
        𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4
          = 2 ^ 12 * 𝓛 α_sift ^ 4 / ε₁ ^ 4 := by ring
        _ ≤ 2 ^ 12 * (8 * (q' : ℝ) * 𝓛 α_U) ^ 4 / ε₁ ^ 4 := by gcongr
        _ = 2 ^ 24 * (q' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 4 := by ring
        _ ≤ 2 ^ 24 * (2 ^ 9 * (p' : ℝ) / ε₁ ^ 2) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 4 := by gcongr
        _ = 2 ^ 60 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12 := by ring
    set X₁ : ℝ := (d + 1 : ℝ) * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U + log (d + 1 : ℝ))
    set X₂ : ℝ := (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 / ε₁ ^ 14
    have hterm2 : (𝓛 α_sift ^ 3 * 𝓛 α_sift / (ε₁ / 8) ^ 4) * 𝓛 (ε₁ / 8 * α_sift * α_sift) ≤
        2 ^ 74 * X₂ := by
      have h1 := mul_le_mul hterm2_front hterm2_L
        (BohrFourier.curlog_pos (by positivity)
          (by have := mul_le_mul_of_nonneg_left hα_sift₁ (by positivity : 0 ≤ ε₁ / 8 * α_sift)
              nlinarith)).le
        (by positivity)
      exact h1.trans_eq (by dsimp [X₂]; ring)
    have hd_term1 : (d + 1 : ℝ) * 𝓛 (ε₁ / 8 * α_sift / (d + 1 : ℝ)) ≤ 2 ^ 13 * X₁ := by
      have := mul_le_mul_of_nonneg_left hterm1 (by positivity : 0 ≤ (d + 1 : ℝ))
      exact this.trans_eq (by dsimp [X₁]; ring)
    have hpos_A : 0 ≤ X₁ := by
      dsimp [X₁]
      have : 0 ≤ log (d + 1 : ℝ) := log_nonneg (by linarith [Nat.cast_nonneg (α := ℝ) d])
      positivity
    have hpos_B : 0 ≤ X₂ := by dsimp [X₂]; positivity
    linarith

section PropIt
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

private lemma exists_shift_wLpNorm_ge {K₁ K₂ : Finset G} (hK₁ : K₁.Nonempty) (hK₂ : K₂.Nonempty)
    {q' : ℕ} (hq' : q' ≠ 0) (g : G → ℝ) {R : ℝ} (hR : 0 ≤ R)
    (hge : R ≤ ‖g‖_[q', (μ_[ℝ≥0] K₁ ○ᵈ μ K₁) ∗ᵈ (μ K₂ ○ᵈ μ K₂)]) :
    ∃ x₀ : G, (K₁ ∩ (x₀ +ᵥ K₂)).Nonempty ∧ R ≤ ‖g‖_[q', μ K₁ ○ᵈ μ (x₀ +ᵥ K₂)] := by
  let ν : G → ℝ≥0 := (μ_[ℝ≥0] K₁ ○ᵈ μ K₁) ∗ᵈ (μ K₂ ○ᵈ μ K₂)
  have hpow : R ^ q' ≤ ∑ y : G, (ν y : ℝ) * ‖g y‖ ^ q' := by
    have h1 := pow_le_pow_left₀ hR hge q'
    rwa [wLpNorm_pow_eq_sum_norm hq'] at h1
  have hK₁_pos : (0 : ℝ) < #K₁ := by exact_mod_cast hK₁.card_pos
  have hK₂_pos : (0 : ℝ) < #K₂ := by exact_mod_cast hK₂.card_pos
  have hident : ∑ y : G, (ν y : ℝ) * ‖g y‖ ^ q' =
      (#K₁ * #K₂ : ℝ)⁻¹ * ∑ ab ∈ K₁ ×ˢ K₂,
        ∑ y : G, (μ_[ℝ] K₁ ○ᵈ μ ((ab.1 - ab.2) +ᵥ K₂)) y * ‖g y‖ ^ q' := by
    have hlhs : ∑ y : G, (ν y : ℝ) * ‖g y‖ ^ q' =
        ((#K₁ : ℝ) ^ 2)⁻¹ * ((#K₂ : ℝ) ^ 2)⁻¹ *
          ∑ a₁ ∈ K₁, ∑ a₂ ∈ K₁, ∑ b₁ ∈ K₂, ∑ b₂ ∈ K₂, ‖g ((a₁ - a₂) + (b₁ - b₂))‖ ^ q' := by
      have hν_real : ∀ y : G, (ν y : ℝ) = ((μ_[ℝ] K₁ ○ᵈ μ K₁) ∗ᵈ (μ K₂ ○ᵈ μ K₂)) y := fun y ↦ by
        simp only [ν, ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply, NNReal.coe_sum,
          NNReal.coe_mul, NNReal.coe_mu]
      simp_rw [hν_real]
      rw [sum_ddconv_mul]
      simp_rw [mul_assoc, ← Finset.mul_sum, sum_dddconv_mul]
      have hsum_mu : ∀ (S : Finset G) (φ : G → ℝ),
          ∑ z : G, μ_[ℝ] S z * φ z = (#S : ℝ)⁻¹ * ∑ z ∈ S, φ z := fun S φ ↦ by
        rw [← Finset.sum_subset (Finset.subset_univ S)]
        · simp_rw [mu_apply]; simp [Finset.mul_sum]
        · intro z _ hz; simp [mu_apply, hz]
      simp_rw [RCLike.conj_to_real, mul_assoc, ← Finset.mul_sum, hsum_mu K₁, hsum_mu K₂,
        ← Finset.mul_sum]
      ring
    have hrhs_inner : ∀ (a₂ b₁ : G),
        ∑ y : G, (μ_[ℝ] K₁ ○ᵈ μ ((a₂ - b₁) +ᵥ K₂)) y * ‖g y‖ ^ q' =
          (#K₁ : ℝ)⁻¹ * (#K₂ : ℝ)⁻¹ *
            ∑ a₁ ∈ K₁, ∑ b₂ ∈ K₂, ‖g ((a₁ - a₂) + (b₁ - b₂))‖ ^ q' := by
      intro a₂ b₁
      rw [sum_dddconv_mul]
      have hsum_K₁ : ∀ φ : G → ℝ, ∑ z : G, μ_[ℝ] K₁ z * φ z = (#K₁ : ℝ)⁻¹ * ∑ z ∈ K₁, φ z := by
        intro φ
        rw [← Finset.sum_subset (Finset.subset_univ K₁)]
        · simp_rw [mu_apply]; simp [Finset.mul_sum]
        · intro z _ hz; simp [mu_apply, hz]
      have hsum_K₂_shift : ∀ φ : G → ℝ,
          ∑ z : G, μ_[ℝ] ((a₂ - b₁) +ᵥ K₂) z * φ z =
            (#K₂ : ℝ)⁻¹ * ∑ b₂ ∈ K₂, φ ((a₂ - b₁) + b₂) := by
        intro φ
        rw [← Finset.sum_subset (Finset.subset_univ ((a₂ - b₁) +ᵥ K₂))]
        · simp_rw [mu_apply, Finset.card_vadd_finset]
          have hbij : ∑ z ∈ (a₂ - b₁) +ᵥ K₂,
                (#K₂ : ℝ)⁻¹ * ite (z ∈ (a₂ - b₁) +ᵥ K₂) 1 0 * φ z =
              ∑ b₂ ∈ K₂, (#K₂ : ℝ)⁻¹ * φ ((a₂ - b₁) + b₂) := by
            refine Finset.sum_bij (fun z _ ↦ -(a₂ - b₁) + z)
              (fun z hz ↦ by
                rcases mem_vadd_finset.mp hz with ⟨b₂, hb₂, rfl⟩
                have hc1 : -(a₂ - b₁) + ((a₂ - b₁) +ᵥ b₂) = b₂ := by
                  simp only [vadd_eq_add]; abel
                rwa [hc1])
              (fun _ _ _ _ h ↦ add_left_cancel h)
              (fun b₂ hb₂ ↦ ⟨(a₂ - b₁) + b₂, mem_vadd_finset.mpr ⟨b₂, hb₂, rfl⟩, by abel⟩)
              (fun z hz ↦ by
                have hc2 : a₂ - b₁ + (b₁ - a₂ + z) = z := by abel
                simp [hz, hc2])
          rw [hbij, ← Finset.mul_sum]
        · intro z _ hz; simp [mu_apply, hz]
      simp_rw [RCLike.conj_to_real, mul_assoc, ← Finset.mul_sum, hsum_K₁, hsum_K₂_shift,
        ← Finset.mul_sum]
      have harg : ∀ a₁ b₂ : G, a₁ - ((a₂ - b₁) + b₂) = (a₁ - a₂) + (b₁ - b₂) := by intros; abel
      simp_rw [harg]
    rw [hlhs, Finset.sum_product]
    simp_rw [hrhs_inner, ← Finset.mul_sum]
    have hswap : ∑ a₁ ∈ K₁, ∑ a₂ ∈ K₁, ∑ b₁ ∈ K₂, ∑ b₂ ∈ K₂, ‖g ((a₁ - a₂) + (b₁ - b₂))‖ ^ q' =
        ∑ a₂ ∈ K₁, ∑ b₁ ∈ K₂, ∑ a₁ ∈ K₁, ∑ b₂ ∈ K₂, ‖g ((a₁ - a₂) + (b₁ - b₂))‖ ^ q' := by
      rw [Finset.sum_comm]
      exact Finset.sum_congr rfl fun a₂ _ ↦ Finset.sum_comm
    rw [hswap, mul_inv, sq, sq, mul_inv, mul_inv]
    ring
  rw [hident] at hpow
  have hex : ∃ ab ∈ K₁ ×ˢ K₂,
      R ^ q' ≤ ∑ y : G, (μ_[ℝ] K₁ ○ᵈ μ ((ab.1 - ab.2) +ᵥ K₂)) y * ‖g y‖ ^ q' := by
    by_contra! hlt
    have hsum_lt : ∑ ab ∈ K₁ ×ˢ K₂,
          ∑ y : G, (μ_[ℝ] K₁ ○ᵈ μ ((ab.1 - ab.2) +ᵥ K₂)) y * ‖g y‖ ^ q' <
        (#K₁ * #K₂ : ℝ) * R ^ q' := by
      calc
        ∑ ab ∈ K₁ ×ˢ K₂, ∑ y : G, (μ_[ℝ] K₁ ○ᵈ μ ((ab.1 - ab.2) +ᵥ K₂)) y * ‖g y‖ ^ q'
          < ∑ _ab ∈ K₁ ×ˢ K₂, R ^ q' :=
            Finset.sum_lt_sum_of_nonempty (hK₁.product hK₂) hlt
        _ = (#K₁ * #K₂ : ℝ) * R ^ q' := by simp [card_product]
    have hprod_pos : 0 < (#K₁ * #K₂ : ℝ) := by positivity
    have := (le_inv_mul_iff₀ hprod_pos).mp hpow
    linarith
  obtain ⟨⟨a₂, b₁⟩, hab, hge_ab⟩ := hex
  obtain ⟨ha₂, hb₁⟩ := mem_product.mp hab
  refine ⟨a₂ - b₁, ⟨a₂, mem_inter.mpr ⟨ha₂, mem_vadd_finset.mpr ⟨b₁, hb₁, ?_⟩⟩⟩, ?_⟩
  · simp only [vadd_eq_add]; abel
  refine le_of_pow_le_pow_left₀ hq' (by positivity) ?_
  rw [wLpNorm_pow_eq_sum_norm hq']
  simpa [NNReal.smul_def, smul_eq_mul, NNReal.coe_dddconv, NNReal.coe_comp_mu] using hge_ab

private lemma prop_it_dens {B_amb K₃ : BohrSet G} {U A₁ A₂ S : Finset G}
    (hU : U.Nonempty) (hA₁_ne : A₁.Nonempty) (hA₂_ne : A₂.Nonempty)
    {α_U ε₁ : ℝ} (hα_U : α_U = (#U : ℝ) / #B_amb.finset)
    (hε₁₀ : 0 < ε₁) (hε₁₁ : ε₁ ≤ 1)
    (hS_high : ∀ y ∈ S, (1 + ε₁ / 2) / #B_amb.finset ≤ (μ_[ℝ] U ○ᵈ μ U) y)
    (hK₃_mass : 1 - ε₁ / 4 ≤ ∑ y ∈ S, (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y) :
    (1 + ε₁ / 8) * α_U ≤ ‖𝟭_[(U : Set G), ℝ] ∗ᵈ μ K₃.finset‖_[∞] := by
  have hB_pos : (0 : ℝ) < #B_amb.finset := by exact_mod_cast B_amb.card_finset_pos
  have hU_pos : (0 : ℝ) < #U := by exact_mod_cast hU.card_pos
  have hconv_nn : 0 ≤ μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂) :=
    ddconv_nonneg' mu_nonneg (dddconv_nonneg' mu_nonneg mu_nonneg)
  have hassoc : μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂) = (μ_[ℝ] K₃.finset ∗ᵈ μ A₁) ○ᵈ μ A₂ := by
    simp_rw [← ddconv_conjneg, ddconv_assoc]
  have hprod_ge : 1 + ε₁ / 8 ≤ (1 + ε₁ / 2) * (1 - ε₁ / 4) := by
    have hsq : 0 ≤ ε₁ * (1 - ε₁) := mul_nonneg hε₁₀.le (sub_nonneg.mpr hε₁₁)
    linarith
  have hchain : (1 + ε₁ / 8) / #B_amb.finset ≤ ‖μ_[ℝ] K₃.finset ∗ᵈ μ U‖_[∞] := by
    calc
      (1 + ε₁ / 8) / #B_amb.finset
        ≤ ((1 + ε₁ / 2) / #B_amb.finset) * (1 - ε₁ / 4) := by
          rw [div_mul_eq_mul_div]; exact div_le_div_of_nonneg_right hprod_ge hB_pos.le
      _ ≤ ((1 + ε₁ / 2) / #B_amb.finset) *
            ∑ y ∈ S, (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y :=
          mul_le_mul_of_nonneg_left hK₃_mass (by positivity)
      _ = ∑ y ∈ S, ((1 + ε₁ / 2) / #B_amb.finset) *
            (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y := Finset.mul_sum ..
      _ ≤ ∑ y ∈ S, (μ_[ℝ] U ○ᵈ μ U) y * (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y :=
          Finset.sum_le_sum fun y hy ↦ mul_le_mul_of_nonneg_right (hS_high y hy) (hconv_nn y)
      _ ≤ ∑ y : G, (μ_[ℝ] U ○ᵈ μ U) y * (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y :=
          Finset.sum_le_sum_of_subset_of_nonneg (subset_univ S) fun y _ _ ↦
            mul_nonneg (dddconv_apply_nonneg' mu_nonneg mu_nonneg y) (hconv_nn y)
      _ = ⟪μ_[ℝ] K₃.finset ∗ᵈ μ U, μ U ∗ᵈ μ A₂ ○ᵈ μ A₁⟫_[ℝ] := by
          simp_rw [hassoc]
          rw [← wInner_one_dddconv_eq_ddconv_wInner_one, dddconv_right_comm,
            ddconv_dddconv_right_comm (μ U), wInner_one_dddconv_eq_ddconv_wInner_one,
            ← dddconv_wInner_one_eq_wInner_one_ddconv, ← conj_wInner_symm]
          simp only [wInner_one_eq_sum, inner_apply, conj_trivial]
      _ ≤ ‖μ_[ℝ] K₃.finset ∗ᵈ μ U‖_[∞] * ‖μ_[ℝ] U ∗ᵈ μ A₂ ○ᵈ μ A₁‖_[1] :=
          wInner_one_le_dLpNorm_mul_dLpNorm ∞ 1
      _ = ‖μ_[ℝ] K₃.finset ∗ᵈ μ U‖_[∞] := by
          rw [dL1Norm_dddconv (ddconv_nonneg' mu_nonneg mu_nonneg) mu_nonneg,
            dL1Norm_ddconv mu_nonneg mu_nonneg, dL1Norm_mu hU, dL1Norm_mu hA₂_ne,
            dL1Norm_mu hA₁_ne, mul_one, mul_one, mul_one]
  have hsmul_inf : (#U : ℝ) * ‖μ_[ℝ] K₃.finset ∗ᵈ μ U‖_[∞] =
      ‖𝟭_[(U : Set G), ℝ] ∗ᵈ μ K₃.finset‖_[∞] := by
    rw [ddconv_comm (μ_[ℝ] K₃.finset) (μ U), ← card_smul_mu, smul_ddconv, dLpNorm_nsmul,
      nsmul_eq_mul]
  rw [← hsmul_inf, hα_U]
  have hmul := mul_le_mul_of_nonneg_left hchain hU_pos.le
  have hrew : (#U : ℝ) * ((1 + ε₁ / 8) / #B_amb.finset) =
      (1 + ε₁ / 8) * ((#U : ℝ) / #B_amb.finset) := by ring
  linarith

/-- Single Bohr iteration step (`prop-it` in the blueprint), combining DRC sifting and
`BohrFourier.th_ap_int`. -/
lemma prop_it {B_amb K₁ K₂ : BohrSet G} (hK₁_reg : K₁.IsRegular)
    (hK₂_reg : K₂.IsRegular) (hK₂_pos : K₂.PosWidth)
    {d : ℕ} (hK₁_rk : K₁.rank ≤ d) (hK₂_rk : K₂.rank ≤ d)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (d : ℝ) * κ ≤ 1)
    (hK₂_sub : K₂.finset ⊆ (κ • K₁).finset)
    {U : Finset G} (hU_sub : U ⊆ B_amb.finset) (hU : U.Nonempty)
    {α_U ε₁ : ℝ} (hα_U : α_U = (#U : ℝ) / #B_amb.finset)
    (hε₁₀ : 0 < ε₁) (hε₁₁ : ε₁ ≤ 1)
    {p' : ℕ} (hp' : 1 ≤ p')
    (hlp : 1 + ε₁ ≤ (#B_amb.finset : ℝ) *
      ‖μ_[ℝ] U ○ᵈ μ U‖_[p', (μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)]) :
    ∃ K₃ : BohrSet G,
      K₃.finset ⊆ K₂.finset ∧
      K₃.IsRegular ∧
      K₃.PosWidth ∧
      (K₃.rank : ℝ) ≤ d + 2 ^ 128 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / ε₁ ^ 12 ∧
      exp (-2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U + log (d + 1 : ℝ)) +
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 / ε₁ ^ 14)) * #K₂.finset ≤ #K₃.finset ∧
      (1 + ε₁ / 8) * α_U ≤ ‖𝟭_[(U : Set G), ℝ] ∗ᵈ μ K₃.finset‖_[∞] := by
  have hB_pos : (0 : ℝ) < #B_amb.finset := by exact_mod_cast B_amb.card_finset_pos
  have hU_pos : (0 : ℝ) < #U := by exact_mod_cast hU.card_pos
  have hU_le : (#U : ℝ) ≤ #B_amb.finset := by exact_mod_cast Finset.card_le_card hU_sub
  have hα₀ : 0 < α_U := by rw [hα_U]; positivity
  have hα₁ : α_U ≤ 1 := by rw [hα_U]; exact div_le_one_of_le₀ hU_le hB_pos.le
  set q' : ℕ := max (2 * p') (2 * ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊) with hq'_def
  have hq'_even : Even q' := by
    rw [hq'_def]
    rcases max_choice (2 * p') (2 * ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊) with h | h <;>
      rw [h] <;> exact even_two_mul _
  have hq'₂ : 2 ≤ q' := by rw [hq'_def]; exact le_trans (by omega) (le_max_left _ _)
  have hq'_ne : q' ≠ 0 := by omega
  have hp'_le_q' : p' ≤ q' := by rw [hq'_def]; exact le_trans (by omega) (le_max_left _ _)
  have hq'_sift : (ε₁ / 4)⁻¹ * log (2 / (ε₁ / 8)) ≤ q' := by
    have heq : (ε₁ / 4)⁻¹ * log (2 / (ε₁ / 8)) = 4 * ε₁⁻¹ * log (16 / ε₁) := by ring_nf
    rw [heq, hq'_def]
    calc
      4 * ε₁⁻¹ * log (16 / ε₁) ≤ (⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊ : ℝ) := Nat.le_ceil _
      _ ≤ 2 * (⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊ : ℝ) := by
          linarith [Nat.cast_nonneg (α := ℝ) ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊]
      _ ≤ max (2 * p') (2 * ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊) := by
          exact_mod_cast le_max_right (2 * p') _
  have hq'_upper : (q' : ℝ) ≤ 2 ^ 9 * (p' : ℝ) / ε₁ ^ 2 := by
    have hε_inv1 : 1 ≤ ε₁⁻¹ := (one_le_inv₀ hε₁₀).2 hε₁₁
    have hp'1 : (1 : ℝ) ≤ p' := by exact_mod_cast hp'
    have hleft : (2 * p' : ℝ) ≤ 2 ^ 9 * (p' : ℝ) / ε₁ ^ 2 := by
      rw [le_div_iff₀ (by positivity)]
      have hε_sq : ε₁ ^ 2 ≤ 1 := pow_le_one₀ hε₁₀.le hε₁₁
      nlinarith
    have hlog16_ge1 : 1 ≤ log (16 / ε₁) := by
      rw [← log_exp 1]
      exact log_le_log (exp_pos 1) (exp_one_lt_d9.le.trans (by
        have : (16 : ℝ) ≤ 16 / ε₁ := (le_div_iff₀ hε₁₀).mpr (by linarith)
        linarith))
    have hceil_arg : (2⁻¹ : ℝ) ≤ 4 * ε₁⁻¹ * log (16 / ε₁) := by nlinarith
    have hright : (2 * ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊ : ℝ) ≤ 2 ^ 9 * (p' : ℝ) / ε₁ ^ 2 := by
      calc
        (2 * ⌈4 * ε₁⁻¹ * log (16 / ε₁)⌉₊ : ℝ)
          ≤ 2 * (2 * (4 * ε₁⁻¹ * log (16 / ε₁))) := by
            gcongr; exact Nat.ceil_le_two_mul hceil_arg
        _ ≤ 2 * (2 * (4 * ε₁⁻¹ * (16 / ε₁))) := by
            gcongr; exact Real.log_le_self (by positivity)
        _ = 2 ^ 8 / ε₁ ^ 2 := by ring
        _ ≤ 2 ^ 9 * (p' : ℝ) / ε₁ ^ 2 := by
            rw [div_le_div_iff_of_pos_right (by positivity)]
            linarith
    rw [hq'_def]
    push_cast
    exact max_le hleft hright
  have hlp_q' : (1 + ε₁) / #B_amb.finset ≤
      ‖μ_[ℝ] U ○ᵈ μ U‖_[q',
        (μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)] := by
    have hν_prob : ∑ y : G,
        (((μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)) y : ℝ≥0∞) = 1 := by
      have hreal : ∑ y : G,
          (((μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)) y : ℝ) = 1 := by
        have hνR : (fun y ↦ (((μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ
            (μ K₂.finset ○ᵈ μ K₂.finset)) y : ℝ)) =
            (μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset) := by
          ext y
          simp only [ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply, NNReal.coe_sum,
            NNReal.coe_mul, NNReal.coe_mu]
        rw [show (∑ y : G, _) = ∑ y : G, ((μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ
            (μ K₂.finset ○ᵈ μ K₂.finset)) y by simp_rw [← hνR],
          sum_ddconv, sum_dddconv, sum_dddconv]
        simp [sum_mu ℝ K₁.finset_nonempty, sum_mu ℝ K₂.finset_nonempty]
      have hsum_nn : ∑ y : G,
          ((μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)) y = 1 := by
        exact_mod_cast hreal
      exact_mod_cast hsum_nn
    rw [div_le_iff₀ hB_pos, mul_comm]
    exact hlp.trans (mul_le_mul_of_nonneg_left (wLpNorm_mono_right hν_prob (mod_cast hp'_le_q') _)
      hB_pos.le)
  obtain ⟨x₀, hinter, hshift_lp⟩ :=
    exists_shift_wLpNorm_ge K₁.finset_nonempty K₂.finset_nonempty hq'_ne
      (μ_[ℝ] U ○ᵈ μ U) (by positivity) hlp_q'
  obtain ⟨A₁, hA₁_sub, A₂, hA₂_sub, hsift_sum, hA₁_card, hA₂_card⟩ :=
    sifting_bohr K₁.finset (x₀ +ᵥ K₂.finset) (by positivity) (by linarith)
      (by positivity : 0 < ε₁ / 8) hq'_even hq'₂ hq'_sift hinter hU
  set α_sift : ℝ := 4⁻¹ * α_U ^ (2 * q') with hα_sift_def
  have hα_sift₀ : 0 < α_sift := by rw [hα_sift_def]; positivity
  have hα_sift₁ : α_sift ≤ 1 := by
    rw [hα_sift_def]
    have : α_U ^ (2 * q') ≤ 1 := pow_le_one₀ hα₀.le hα₁
    linarith
  have hnorm_ratio : α_U ≤
      ‖𝟭_[(U : Set G), ℝ] ○ᵈ 𝟭_[U]‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] / #U := by
    rw [le_div_iff₀ hU_pos]
    have hsmul : ‖𝟭_[(U : Set G), ℝ] ○ᵈ 𝟭_[U]‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] =
        (#U : ℝ) ^ 2 * ‖μ_[ℝ] U ○ᵈ μ U‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] := by
      rw [← card_smul_mu (K := ℝ) U, smul_dddconv, dddconv_smul, wLpNorm_nsmul, wLpNorm_nsmul,
        nsmul_eq_mul, nsmul_eq_mul]
      simp only [star_trivial]
      ring
    rw [hsmul]
    have hge1 : 1 / #B_amb.finset ≤ ‖μ_[ℝ] U ○ᵈ μ U‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] :=
      (div_le_div_of_nonneg_right (by linarith) hB_pos.le).trans hshift_lp
    calc
      α_U * #U = (#U : ℝ) ^ 2 * (1 / #B_amb.finset) := by rw [hα_U]; ring
      _ ≤ (#U : ℝ) ^ 2 * ‖μ_[ℝ] U ○ᵈ μ U‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] :=
        mul_le_mul_of_nonneg_left hge1 (by positivity)
  have hsift_base : α_sift ≤
      4⁻¹ * ‖𝟭_[(U : Set G), ℝ] ○ᵈ 𝟭_[U]‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] ^ (2 * q') /
        #U ^ (2 * q') := by
    rw [mul_div_assoc, ← div_pow, hα_sift_def]
    gcongr
  have hA₁_lb : α_sift * #K₁.finset ≤ #A₁ := by
    rw [← le_div_iff₀ (by exact_mod_cast K₁.card_finset_pos)]
    exact hsift_base.trans hA₁_card
  have hA₂_lb : α_sift * #K₂.finset ≤ #A₂ := by
    have hM₂_card : #(x₀ +ᵥ K₂.finset) = #K₂.finset := Finset.card_vadd_finset x₀ K₂.finset
    rw [← hM₂_card, ← le_div_iff₀ (by rw [hM₂_card]; exact_mod_cast K₂.card_finset_pos)]
    exact hsift_base.trans hA₂_card
  have hA₂_vadd_sub : (-x₀) +ᵥ A₂ ⊆ K₂.finset := by
    intro z hz
    rcases mem_vadd_finset.mp hz with ⟨y, hy, rfl⟩
    rcases mem_vadd_finset.mp (hA₂_sub hy) with ⟨w, hw, rfl⟩
    simpa using hw
  set S_sift : Finset G := sBohr q' (ε₁ / 4) K₁.finset (x₀ +ᵥ K₂.finset) U with hS_sift_def
  set S_high : Finset G := {y | (1 + ε₁ / 2) / #B_amb.finset ≤ (μ_[ℝ] U ○ᵈ μ U) y} with hS_high_def
  set D : Finset G := (-x₀) +ᵥ ((1 + κ) • K₁).finset with hD_def
  set S : Finset G := S_high ∩ D with hS_def
  have hs_sub_high : S_sift ⊆ S_high := by
    intro y hy
    rw [hS_sift_def, mem_sBohr'] at hy
    rw [hS_high_def]
    simp only [mem_filter, mem_univ, true_and]
    have hprod : 1 + ε₁ / 2 ≤ (1 - ε₁ / 4) * (1 + ε₁) := by
      have : 0 ≤ ε₁ * (1 - ε₁) := mul_nonneg hε₁₀.le (sub_nonneg.mpr hε₁₁)
      linarith
    calc
      (1 + ε₁ / 2) / #B_amb.finset
        ≤ ((1 - ε₁ / 4) * (1 + ε₁)) / #B_amb.finset :=
          div_le_div_of_nonneg_right hprod hB_pos.le
      _ = (1 - ε₁ / 4) * ((1 + ε₁) / #B_amb.finset) := by ring
      _ ≤ (1 - ε₁ / 4) * ‖μ_[ℝ] U ○ᵈ μ U‖_[q', μ K₁.finset ○ᵈ μ (x₀ +ᵥ K₂.finset)] :=
          mul_le_mul_of_nonneg_left hshift_lp (by linarith)
      _ ≤ (μ_[ℝ] U ○ᵈ μ U) y := hy.le
  have hsupp_in_D : ∀ y : G, (μ_[ℝ] A₁ ○ᵈ μ A₂) y ≠ 0 → y ∈ D := by
    intro y hy
    rcases support_dddconv_subset' _ _ hy with ⟨a₁, ha₁, a₂, ha₂, rfl⟩
    have ha₁_K₁ : a₁ ∈ K₁.finset := hA₁_sub (by simpa using ha₁)
    have ha₂_M₂ : a₂ ∈ x₀ +ᵥ K₂.finset := hA₂_sub (by simpa using ha₂)
    rcases mem_vadd_finset.mp ha₂_M₂ with ⟨w, hw, rfl⟩
    have hnw : -w ∈ (κ • K₁).finset := BohrSet.neg_mem_finset.mpr (hK₂_sub hw)
    have hmem_add : a₁ + (-w) ∈ ((1 : ℝ) • K₁).finset + (κ • K₁).finset := by
      rw [one_smul]
      exact Finset.add_mem_add ha₁_K₁ hnw
    have hsum_in := BohrSet.smul_add_smul_finset_subset zero_le_one hκ₀ hmem_add
    rw [hD_def]
    refine mem_vadd_finset.mpr ⟨a₁ + (-w), hsum_in, ?_⟩
    simp only [vadd_eq_add]
    abel
  have hS_mass : 1 - ε₁ / 8 ≤ ∑ y ∈ S, (μ_[ℝ] A₁ ○ᵈ μ A₂) y := by
    refine hsift_sum.trans ?_
    have h1 : ∑ y ∈ S_sift, (μ_[ℝ] A₁ ○ᵈ μ A₂) y = ∑ y ∈ S_sift ∩ D, (μ_[ℝ] A₁ ○ᵈ μ A₂) y := by
      symm
      refine Finset.sum_subset inter_subset_left fun y hy hy_not ↦ ?_
      by_contra hne
      exact hy_not (mem_inter.mpr ⟨hy, hsupp_in_D y hne⟩)
    rw [h1]
    have hsub_inter : S_sift ∩ D ⊆ S := fun z hz ↦ by
      rw [hS_def]
      exact mem_inter.mpr ⟨hs_sub_high (mem_inter.mp hz).1, (mem_inter.mp hz).2⟩
    exact Finset.sum_le_sum_of_subset_of_nonneg hsub_inter
      fun y _ _ ↦ dddconv_apply_nonneg' mu_nonneg mu_nonneg y
  have hS_card : #S ≤ 2 * #K₁.finset := by
    have hK₁_rk_real : (K₁.rank : ℝ) ≤ d := by exact_mod_cast hK₁_rk
    have hκ_K₁ : 100 * (K₁.rank : ℝ) * κ ≤ 1 :=
      (mul_le_mul_of_nonneg_right (by linarith) hκ₀).trans hκ
    have hreal : (#S : ℝ) ≤ 2 * #K₁.finset := by
      calc
        (#S : ℝ) ≤ #D := by rw [hS_def]; exact_mod_cast Finset.card_le_card inter_subset_right
        _ = #((1 + κ) • K₁).finset := by rw [hD_def, Finset.card_vadd_finset]
        _ ≤ (1 + 100 * K₁.rank * κ) * #K₁.finset := hK₁_reg.card_one_add_smul_le hκ₀ hκ_K₁
        _ ≤ 2 * #K₁.finset := by nlinarith [Nat.cast_nonneg (α := ℝ) #K₁.finset]
    exact_mod_cast hreal
  obtain ⟨K₃, hK₃_sub, hK₃_reg, hK₃_pos, hK₃_rk, hK₃_size, hK₃_ap⟩ :=
    BohrFourier.th_ap_int (B := K₁) (B' := K₂) hK₂_reg hK₂_pos hK₂_rk
      hα_sift₀ hα_sift₁ hα_sift₀ hα_sift₁ (by positivity : 0 < ε₁ / 8) (by linarith)
      hA₁_lb hA₂_vadd_sub hA₂_lb hS_card
  obtain ⟨hK₃_rk', hK₃_exp⟩ :=
    prop_it_bounds hα₀ hα₁ hε₁₀ hε₁₁ hp' hq'_ne hq'_upper hα_sift_def hK₃_rk
  have hK₃_size' :
      exp (-2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) / ε₁ ^ 2 * 𝓛 α_U + log (d + 1 : ℝ)) +
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 / ε₁ ^ 14)) * #K₂.finset ≤ #K₃.finset :=
    (mul_le_mul_of_nonneg_right hK₃_exp (Nat.cast_nonneg _)).trans hK₃_size
  have hK₃_mass : 1 - ε₁ / 4 ≤ ∑ y ∈ S, (μ_[ℝ] K₃.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y := by
    have hlo := (neg_le_abs _).trans hK₃_ap
    linarith
  have hA₁_ne : A₁.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
    exact (mul_pos hα_sift₀ (by exact_mod_cast K₁.card_finset_pos)).trans_le hA₁_lb
  have hA₂_ne : A₂.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
    exact (mul_pos hα_sift₀ (by exact_mod_cast K₂.card_finset_pos)).trans_le hA₂_lb
  have hS_high_fn : ∀ y ∈ S, (1 + ε₁ / 2) / #B_amb.finset ≤ (μ_[ℝ] U ○ᵈ μ U) y := fun y hy ↦ by
    rw [hS_def] at hy
    have hy1 := (mem_inter.mp hy).1
    rw [hS_high_def] at hy1
    exact (mem_filter.mp hy1).2
  exact ⟨K₃, hK₃_sub, hK₃_reg, hK₃_pos, hK₃_rk', hK₃_size',
    prop_it_dens hU hA₁_ne hA₂_ne hα_U hε₁₀ hε₁₁ hS_high_fn hK₃_mass⟩

end PropIt

end BohrStep
