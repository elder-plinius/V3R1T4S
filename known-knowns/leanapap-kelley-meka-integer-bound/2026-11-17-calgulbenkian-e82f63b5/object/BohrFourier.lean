module

public import APAP.BohrBasic
public import APAP.Prereqs.LpNorm.Weighted
public import APAP.Prereqs.LargeSpec

public import Mathlib.Combinatorics.Additive.DoublingConst

import AddCombi.Concentration.MarcinkiewiczZygmund
import APAP.Mathlib.Basic.Complex.Basic
import APAP.Prereqs.Convolution.Discrete.Basic
import APAP.Prereqs.Convolution.Norm
import APAP.Prereqs.FourierTransform.Discrete
import APAP.Prereqs.Inner.Hoelder.Compact
import APAP.Prereqs.Inner.Hoelder.Discrete
import APAP.Prereqs.LpNorm.Discrete.Basic
import Mathlib.Algebra.Group.Action.Pointwise.Finset
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Algebra.Order.Star.Real
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Series
import Mathlib.Data.Finset.CastCard
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Fourier positivity on Bohr sets, localized almost-periodicity, and Bohr relative Chang's lemma
-/

@[expose] public section

attribute [-simp] Real.log_inv

open AddChar Finset Function MeasureTheory RCLike Real
open scoped NNReal ENNReal BigOperators Combinatorics.Additive ComplexConjugate Pointwise
  Indicator translate mu

local notation3 "𝓛" x:arg => 1 + Real.log x⁻¹
local notation:70 s:70 " ^^ " n:71 => Fintype.piFinset fun _ : Fin n ↦ s

namespace BohrFourier

section CurlogHelpers
variable {x y : ℝ}

lemma one_le_curlog (hx₀ : 0 ≤ x) (hx₁ : x ≤ 1) : 1 ≤ 𝓛 x := by
  obtain rfl | hx₀ := hx₀.eq_or_lt
  · simp
  have : 0 ≤ log x⁻¹ := log_nonneg ((one_le_inv₀ hx₀).2 hx₁)
  linarith

lemma curlog_pos (hx₀ : 0 ≤ x) (hx₁ : x ≤ 1) : 0 < 𝓛 x :=
  zero_lt_one.trans_le (one_le_curlog hx₀ hx₁)

lemma curlog_anti {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) : 𝓛 b ≤ 𝓛 a := by
  have hb : 0 < b := ha.trans_le hab
  have hinv : b⁻¹ ≤ a⁻¹ := inv_anti₀ ha hab
  have hlog : log b⁻¹ ≤ log a⁻¹ := log_le_log (inv_pos.mpr hb) hinv
  linarith

lemma curlog_mul_le (hx₀ : 0 < x) (hx₁ : x ≤ 1) (hy₀ : 0 < y) (hy₁ : y ≤ 1) :
    𝓛 (x * y) ≤ x⁻¹ * 𝓛 y := by
  suffices h : log x⁻¹ - (x⁻¹ - 1) ≤ (x⁻¹ - 1) * log y⁻¹ by
    rw [← sub_nonneg] at h ⊢
    convert h using 1
    rw [mul_inv, log_mul (by positivity) (by positivity)]
    ring
  calc
    log x⁻¹ - (x⁻¹ - 1) ≤ 0 := sub_nonpos.2 <| log_le_sub_one_of_pos <| by positivity
    _ ≤ (x⁻¹ - 1) * log y⁻¹ :=
      mul_nonneg (sub_nonneg.2 <| (one_le_inv₀ hx₀).2 hx₁)
        (log_nonneg ((one_le_inv₀ hy₀).2 hy₁))

lemma curlog_div_le (hx₀ : 0 < x) (hx₁ : x ≤ 1) (hy : 1 ≤ y) : 𝓛 (x / y) ≤ y * 𝓛 x := by
  simpa [div_eq_inv_mul] using curlog_mul_le (by positivity) (inv_le_one_of_one_le₀ hy) hx₀ hx₁

lemma curlog_pow_le {n : ℕ} (hn : n ≠ 0) : 𝓛 (x ^ n) ≤ n * 𝓛 x := by
  have hn1 : (1 : ℝ) ≤ n := Nat.one_le_cast.mpr (Nat.pos_of_ne_zero hn)
  rw [← inv_pow, log_pow]
  nlinarith

end CurlogHelpers

section PosDefMeasures
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

omit [MeasurableSpace G] [DiscreteMeasurableSpace G] in
private lemma weighted_even_pow_shift_le (m : ℕ) (f : G → ℝ) (h : G → ℂ)
    (ν : G → ℝ≥0) (hν : (fun y : G ↦ ((ν y : ℝ) : ℂ)) = h ○ᵈ h) (z : G) :
    ∑ y : G, (ν y : ℝ) * ‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m) ≤
      ∑ y : G, (ν y : ℝ) * ‖(f ○ᵈ f) y‖ ^ (2 * m) := by
  let F : G → ℂ := Complex.ofReal ∘ f
  have hF_conv : ∀ x : G, ((f ∗ᵈ f) x : ℂ) = (F ∗ᵈ F) x := fun x ↦
    Complex.ofReal_ddconv f f x
  have hF_dconv : ∀ x : G, ((f ○ᵈ f) x : ℂ) = (F ○ᵈ F) x := fun x ↦
    Complex.ofReal_dddconv f f x
  let N : ℝ := Fintype.card G
  have hexp_conv : ∀ y : G, (F ∗ᵈ F) (z + y) =
      (N : ℂ)⁻¹ * ∑ φ : AddChar G ℂ, (dft F φ ^ 2 * φ z) * φ y := by
    intro y
    have hinv := (dft_inversion (F ∗ᵈ F) (z + y)).symm
    rw [hinv, Finset.expect_eq_sum_div_card, Finset.card_univ, AddChar.card_eq, div_eq_inv_mul]
    congr 1
    refine Finset.sum_congr rfl fun φ _ ↦ ?_
    rw [dft_ddconv_apply, sq, map_add_eq_mul]; ring
  have hexp_dconv : ∀ y : G, (F ○ᵈ F) y =
      (N : ℂ)⁻¹ * ∑ φ : AddChar G ℂ, ((‖dft F φ‖ ^ 2 : ℝ) : ℂ) * φ y := by
    intro y
    have hinv := (dft_inversion (F ○ᵈ F) y).symm
    rw [hinv, Finset.expect_eq_sum_div_card, Finset.card_univ, AddChar.card_eq, div_eq_inv_mul]
    push_cast
    congr 1
    refine Finset.sum_congr rfl fun φ _ ↦ ?_
    rw [dft_dddconv_apply, Complex.mul_conj']
  have hdft_ν : ∀ γ : AddChar G ℂ,
      dft (fun y ↦ ((ν y : ℝ) : ℂ)) γ = ((‖dft h γ‖ ^ 2 : ℝ) : ℂ) := by
    intro γ
    rw [hν, dft_dddconv_apply, Complex.mul_conj', Complex.ofReal_pow]
  have hchar_orth : ∀ (ψ φ : Fin m → AddChar G ℂ),
      ∑ y : G, ((ν y : ℝ) : ℂ) * (∏ i, conj (ψ i y)) * (∏ i, φ i y) =
        ((‖dft h (∑ i, ψ i - ∑ i, φ i)‖ ^ 2 : ℝ) : ℂ) := by
    intro ψ φ
    rw [← hdft_ν (∑ i, ψ i - ∑ i, φ i), dft_apply, wInner_one_eq_sum]
    refine Finset.sum_congr rfl fun y _ ↦ ?_
    simp only [RCLike.inner_apply, AddChar.sub_apply, AddChar.sum_apply, map_mul, map_prod,
      map_neg_eq_conj, RCLike.conj_conj]
    ring
  let termL (ψ φ : Fin m → AddChar G ℂ) : ℂ :=
    (∏ i, conj (dft F (ψ i) ^ 2 * ψ i z)) * (∏ i, (dft F (φ i) ^ 2 * φ i z)) *
      ((‖dft h (∑ i, ψ i - ∑ i, φ i)‖ ^ 2 : ℝ) : ℂ)
  let termR (ψ φ : Fin m → AddChar G ℂ) : ℝ :=
    (∏ i, ‖dft F (ψ i)‖ ^ 2) * (∏ i, ‖dft F (φ i)‖ ^ 2) *
      ‖dft h (∑ i, ψ i - ∑ i, φ i)‖ ^ 2
  have hLHS : ((∑ y : G, (ν y : ℝ) * ‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m) : ℝ) : ℂ) =
      ((N⁻¹ ^ (2 * m) : ℝ) : ℂ) * ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, termL ψ φ := by
    have hpt : ∀ y : G, ((‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m) : ℝ) : ℂ) =
        conj ((F ∗ᵈ F) (z + y) ^ m) * ((F ∗ᵈ F) (z + y) ^ m) := by
      intro y
      rw [Real.norm_eq_abs, mul_comm 2 m, pow_mul, ← abs_pow, sq_abs,
        ← hF_conv (z + y), ← Complex.ofReal_pow, Complex.conj_ofReal]
      push_cast; ring
    push_cast
    simp_rw [← Complex.ofReal_pow, hpt]
    have hexp_pow : ∀ y : G, ((F ∗ᵈ F) (z + y)) ^ m =
        (N : ℂ)⁻¹ ^ m * ∑ φ ∈ univ ^^ m, (∏ i, (dft F (φ i) ^ 2 * φ i z)) * (∏ i, φ i y) := by
      intro y
      rw [hexp_conv y, mul_pow, Finset.sum_pow']
      congr 1
      refine Finset.sum_congr rfl fun φ _ ↦ ?_
      rw [Finset.prod_mul_distrib]
    simp_rw [hexp_pow]
    simp only [map_mul, map_pow, map_inv₀, Complex.conj_ofReal, map_sum, map_prod]
    have hN2m : (N : ℂ)⁻¹ ^ (2 * m) = (N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m := by
      rw [two_mul, pow_add]
    rw [hN2m]
    calc
      _ = ((N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m) *
          ∑ y : G, ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m,
            ((∏ i, conj (dft F (ψ i) ^ 2 * ψ i z)) * (∏ i, (dft F (φ i) ^ 2 * φ i z))) *
              (((ν y : ℝ) : ℂ) * (∏ i, conj (ψ i y)) * (∏ i, φ i y)) := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun y _ ↦ ?_
          have hpull : ∀ (c A B : ℂ), c * ((A * ∑ ψ ∈ univ ^^ m,
              (∏ i, conj (dft F (ψ i)) ^ 2 * conj (ψ i z)) * (∏ i, conj (ψ i y))) *
              (B * ∑ φ ∈ univ ^^ m, (∏ i, (dft F (φ i) ^ 2 * φ i z)) * (∏ i, φ i y))) =
              (A * B) * (c * ((∑ ψ ∈ univ ^^ m,
                (∏ i, conj (dft F (ψ i)) ^ 2 * conj (ψ i z)) * (∏ i, conj (ψ i y))) *
               (∑ φ ∈ univ ^^ m, (∏ i, (dft F (φ i) ^ 2 * φ i z)) * (∏ i, φ i y)))) :=
            fun _ _ _ ↦ by ring
          rw [hpull]
          congr 1
          rw [Finset.sum_mul_sum, Finset.mul_sum]
          refine Finset.sum_congr rfl fun ψ _ ↦ ?_
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun φ _ ↦ ?_
          simp only [map_mul, map_pow]
          ring
      _ = ((N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m) *
          ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, termL ψ φ := by
          congr 1
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun ψ _ ↦ ?_
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun φ _ ↦ ?_
          rw [← Finset.mul_sum, hchar_orth ψ φ]
  have hRHS : ((∑ y : G, (ν y : ℝ) * ‖(f ○ᵈ f) y‖ ^ (2 * m) : ℝ) : ℂ) =
      ((N⁻¹ ^ (2 * m) : ℝ) : ℂ) * ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, (termR ψ φ : ℂ) := by
    have hpt : ∀ y : G, ((‖(f ○ᵈ f) y‖ ^ (2 * m) : ℝ) : ℂ) =
        conj ((F ○ᵈ F) y ^ m) * ((F ○ᵈ F) y ^ m) := by
      intro y
      rw [Real.norm_eq_abs, mul_comm 2 m, pow_mul, ← abs_pow, sq_abs,
        ← hF_dconv y, ← Complex.ofReal_pow, Complex.conj_ofReal]
      push_cast; ring
    push_cast
    simp_rw [← Complex.ofReal_pow, hpt]
    have hexp_pow : ∀ y : G, ((F ○ᵈ F) y) ^ m =
        (N : ℂ)⁻¹ ^ m * ∑ φ ∈ univ ^^ m, (∏ i, ((‖dft F (φ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, φ i y) := by
      intro y
      rw [hexp_dconv y, mul_pow, Finset.sum_pow']
      congr 1
      refine Finset.sum_congr rfl fun φ _ ↦ ?_
      rw [Finset.prod_mul_distrib]
    simp_rw [hexp_pow]
    simp only [map_mul, map_pow, map_inv₀, Complex.conj_ofReal, map_sum, map_prod]
    have hN2m : (N : ℂ)⁻¹ ^ (2 * m) = (N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m := by
      rw [two_mul, pow_add]
    rw [hN2m]
    calc
      _ = ((N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m) *
          ∑ y : G, ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m,
            ((∏ i, ((‖dft F (ψ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, ((‖dft F (φ i)‖ ^ 2 : ℝ) : ℂ))) *
              (((ν y : ℝ) : ℂ) * (∏ i, conj (ψ i y)) * (∏ i, φ i y)) := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun y _ ↦ ?_
          have hpull : ∀ (c A B : ℂ), c * ((A * ∑ ψ ∈ univ ^^ m,
              (∏ i, ((‖dft F (ψ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, conj (ψ i y))) *
              (B * ∑ φ ∈ univ ^^ m, (∏ i, ((‖dft F (φ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, φ i y))) =
              (A * B) * (c * ((∑ ψ ∈ univ ^^ m,
                (∏ i, ((‖dft F (ψ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, conj (ψ i y))) *
               (∑ φ ∈ univ ^^ m, (∏ i, ((‖dft F (φ i)‖ ^ 2 : ℝ) : ℂ)) * (∏ i, φ i y)))) :=
            fun _ _ _ ↦ by ring
          rw [hpull]
          congr 1
          rw [Finset.sum_mul_sum, Finset.mul_sum]
          refine Finset.sum_congr rfl fun ψ _ ↦ ?_
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun φ _ ↦ ?_
          ring
      _ = ((N : ℂ)⁻¹ ^ m * (N : ℂ)⁻¹ ^ m) *
          ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, (termR ψ φ : ℂ) := by
          congr 1
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun ψ _ ↦ ?_
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun φ _ ↦ ?_
          rw [← Finset.mul_sum, hchar_orth ψ φ]
          dsimp [termR]
          push_cast
          rfl
  have hnorm_term : ∀ ψ φ, ‖termL ψ φ‖ = termR ψ φ := by
    intro ψ φ
    dsimp [termL, termR]
    rw [norm_mul, norm_mul, norm_prod, norm_prod, Complex.norm_real,
      Real.norm_of_nonneg (sq_nonneg _)]
    congr 2
    · refine Finset.prod_congr rfl fun i _ ↦ ?_
      rw [RCLike.norm_conj, norm_mul, norm_pow, AddChar.norm_apply, mul_one]
    · refine Finset.prod_congr rfl fun i _ ↦ ?_
      rw [norm_mul, norm_pow, AddChar.norm_apply, mul_one]
  have hRHS_real : ∑ y : G, (ν y : ℝ) * ‖(f ○ᵈ f) y‖ ^ (2 * m) =
      N⁻¹ ^ (2 * m) * ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, termR ψ φ := by
    apply Complex.ofReal_injective
    rw [hRHS]
    push_cast
    rfl
  have hN_nn : 0 ≤ N := Nat.cast_nonneg _
  rw [hRHS_real]
  calc
    ∑ y : G, (ν y : ℝ) * ‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m)
      = ‖((∑ y : G, (ν y : ℝ) * ‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m) : ℝ) : ℂ)‖ := by
        rw [Complex.norm_real, Real.norm_of_nonneg]
        exact Finset.sum_nonneg fun y _ ↦ mul_nonneg (NNReal.coe_nonneg _) (by positivity)
    _ = N⁻¹ ^ (2 * m) * ‖∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, termL ψ φ‖ := by
        rw [hLHS, norm_mul, Complex.norm_real, Real.norm_of_nonneg (by positivity)]
    _ ≤ N⁻¹ ^ (2 * m) * ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, ‖termL ψ φ‖ := by
        refine mul_le_mul_of_nonneg_left ?_ (by positivity)
        exact (norm_sum_le _ _).trans (Finset.sum_le_sum fun _ _ ↦ norm_sum_le _ _)
    _ = N⁻¹ ^ (2 * m) * ∑ ψ ∈ univ ^^ m, ∑ φ ∈ univ ^^ m, termR ψ φ := by
        simp_rw [hnorm_term]

/-- Weighted positive-definite convolution norm inequality (`pos-def-measures` in the blueprint). -/
lemma pos_def_measures {B : BohrSet G} (hreg : B.IsRegular) {p : ℕ} (hp₀ : p ≠ 0)
    (hp : Even p) (f : G → ℝ) {B₁ B₂ : Finset G} (hB₁₀ : B₁.Nonempty)
    (hB₂₀ : B₂.Nonempty) {κ₀ : ℝ} (hκ₀ : 0 ≤ κ₀)
    (hκ : 100 * (B.rank : ℝ) * (4 * κ₀) ≤ 1)
    (hB₁_sub : B₁ ⊆ (κ₀ • B).finset) (hB₂_sub : B₂ ⊆ (κ₀ • B).finset) :
    (2⁻¹ : ℝ) * ‖f ∗ᵈ f‖_[p, μ B.finset] ≤
      ‖f ○ᵈ f‖_[p, (μ_[ℝ≥0] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂)] := by
  obtain ⟨m, rfl⟩ := hp.two_dvd
  let ν : G → ℝ≥0 := (μ_[ℝ≥0] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂)
  let νR : G → ℝ := fun y ↦ (ν y : ℝ)
  have hνR_eq : νR = (μ_[ℝ] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂) := by
    ext y
    change (((μ_[ℝ≥0] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂)) y : ℝ) = _
    simp only [ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply, NNReal.coe_sum,
      NNReal.coe_mul, NNReal.coe_mu]
  have hνR_nonneg : 0 ≤ νR := fun _ ↦ NNReal.coe_nonneg _
  have hνR_sum : ∑ y : G, νR y = 1 := by
    rw [hνR_eq, sum_ddconv, sum_dddconv, sum_dddconv]
    simp [sum_mu ℝ hB₁₀, sum_mu ℝ hB₂₀]
  have hνR_supp : ∀ y : G, νR y ≠ 0 → y ∈ ((4 * κ₀) • B).finset := by
    intro y hy
    rw [hνR_eq] at hy
    have hmem : y ∈ support ((μ_[ℝ] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂)) := hy
    rcases support_ddconv_subset _ _ hmem with ⟨u, hu, v, hv, rfl⟩
    rcases support_dddconv_subset' _ _ hu with ⟨a₁, ha₁, a₂, ha₂, rfl⟩
    rcases support_dddconv_subset' _ _ hv with ⟨b₁, hb₁, b₂, hb₂, rfl⟩
    have ha₁' : a₁ ∈ (κ₀ • B).finset := hB₁_sub (by simpa using ha₁)
    have ha₂' : -a₂ ∈ (κ₀ • B).finset :=
      BohrSet.neg_mem_finset.mpr (hB₁_sub (by simpa using ha₂))
    have hb₁' : b₁ ∈ (κ₀ • B).finset := hB₂_sub (by simpa using hb₁)
    have hb₂' : -b₂ ∈ (κ₀ • B).finset :=
      BohrSet.neg_mem_finset.mpr (hB₂_sub (by simpa using hb₂))
    have h12 : a₁ - a₂ ∈ ((2 * κ₀) • B).finset := by
      have hm1 := BohrSet.smul_add_smul_finset_subset hκ₀ hκ₀ (Finset.add_mem_add ha₁' ha₂')
      simpa [← two_mul, ← sub_eq_add_neg] using hm1
    have h34 : b₁ - b₂ ∈ ((2 * κ₀) • B).finset := by
      have hm2 := BohrSet.smul_add_smul_finset_subset hκ₀ hκ₀ (Finset.add_mem_add hb₁' hb₂')
      simpa [← two_mul, ← sub_eq_add_neg] using hm2
    have h1234 := BohrSet.smul_add_smul_finset_subset (by positivity) (by positivity)
      (Finset.add_mem_add h12 h34)
    have h4 : (2 * κ₀ + 2 * κ₀ : ℝ) = 4 * κ₀ := by ring
    rwa [h4] at h1234
  let h : G → ℂ := μ_[ℂ] B₁ ∗ᵈ μ B₂
  have hν_complex : (fun y : G ↦ ((ν y : ℝ) : ℂ)) = h ○ᵈ h := by
    have hcast : (fun y : G ↦ ((ν y : ℝ) : ℂ)) =
        (μ_[ℂ] B₁ ○ᵈ μ B₁) ∗ᵈ (μ B₂ ○ᵈ μ B₂) := by
      ext y
      change (νR y : ℂ) = _
      rw [hνR_eq]
      simp only [ddconv_eq_sum_sub', dddconv_eq_sum_sub', Complex.ofReal_sum, Complex.ofReal_mul,
        Complex.ofReal_mu, conj_mu_apply]
    rw [hcast]
    apply dft_injective
    ext ψ
    simp only [h, dft_ddconv_apply, dft_dddconv_apply, map_mul]
    ring
  let W := ((1 + 4 * κ₀) • B).finset
  have hmaj : ∀ x : G, (μ_[ℝ] B.finset x) ≤ 2 * (μ_[ℝ] W ∗ᵈ νR) x :=
    hreg.mu_le_two_mul_ddconv (by positivity) hκ hνR_nonneg hνR_sum hνR_supp
  refine le_of_pow_le_pow_left₀ hp₀ (by positivity) ?_
  rw [mul_pow, wLpNorm_pow_eq_sum_norm hp₀, wLpNorm_pow_eq_sum_norm hp₀]
  simp only [NNReal.smul_def, smul_eq_mul, NNReal.coe_mu]
  have h2pow : (2⁻¹ : ℝ) ^ (2 * m) * 2 ≤ 1 := by
    have hp2 : 2 ≤ 2 * m := by omega
    calc
      (2⁻¹ : ℝ) ^ (2 * m) * 2 ≤ (2⁻¹ : ℝ) ^ 2 * 2 :=
        mul_le_mul_of_nonneg_right (pow_le_pow_of_le_one (by norm_num) (by norm_num) hp2)
          (by norm_num)
      _ ≤ 1 := by norm_num
  calc
    (2⁻¹ : ℝ) ^ (2 * m) * ∑ x : G, μ_[ℝ] B.finset x * ‖(f ∗ᵈ f) x‖ ^ (2 * m)
      ≤ (2⁻¹ : ℝ) ^ (2 * m) * ∑ x : G, (2 * (μ_[ℝ] W ∗ᵈ νR) x) * ‖(f ∗ᵈ f) x‖ ^ (2 * m) := by
        gcongr with x
        exact hmaj x
    _ = ((2⁻¹ : ℝ) ^ (2 * m) * 2) * ∑ x : G, (μ_[ℝ] W ∗ᵈ νR) x * ‖(f ∗ᵈ f) x‖ ^ (2 * m) := by
        simp_rw [mul_assoc (2 : ℝ), ← Finset.mul_sum, ← mul_assoc]
    _ ≤ 1 * ∑ x : G, (μ_[ℝ] W ∗ᵈ νR) x * ‖(f ∗ᵈ f) x‖ ^ (2 * m) := by
        gcongr
        exact Finset.sum_nonneg fun x _ ↦
          mul_nonneg (ddconv_apply_nonneg' (R := ℝ) mu_nonneg hνR_nonneg x) (by positivity)
    _ = ∑ z : G, μ_[ℝ] W z * (∑ y : G, νR y * ‖(f ∗ᵈ f) (z + y)‖ ^ (2 * m)) := by
        rw [one_mul, sum_ddconv_mul]
        simp_rw [Finset.mul_sum, mul_assoc]
    _ ≤ ∑ z : G, μ_[ℝ] W z * (∑ y : G, νR y * ‖(f ○ᵈ f) y‖ ^ (2 * m)) := by
        refine Finset.sum_le_sum fun z _ ↦ mul_le_mul_of_nonneg_left ?_ (mu_nonneg (K := ℝ) z)
        exact weighted_even_pow_shift_le m f h ν hν_complex z
    _ = ∑ y : G, (ν y : ℝ) * ‖(f ○ᵈ f) y‖ ^ (2 * m) := by
        rw [← Finset.sum_mul, sum_mu ℝ ((1 + 4 * κ₀) • B).finset_nonempty, one_mul]

end PosDefMeasures

section LocalizedAlmostPeriodicity
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

private lemma my_markov_local {α : Type*} {g : α → ℝ} {c ε : ℝ} {A : Finset α}
    (hc : 0 < c) (hg : ∀ a ∈ A, 0 ≤ g a) (h : ∑ a ∈ A, g a ≤ ε * c * #A) :
    (1 - ε) * #A ≤ #{a ∈ A | g a ≤ c} := by
  classical
  have h1 := h.trans'
    (sum_le_sum_of_subset_of_nonneg (filter_subset (¬g · ≤ c) A) fun i hi _ ↦ hg _ hi)
  have h2 := (card_nsmul_le_sum _ _ c (by simp +contextual [le_of_lt])).trans h1
  rw [nsmul_eq_mul, mul_right_comm] at h2
  have h3 := le_of_mul_le_mul_right h2 hc
  rw [filter_not, cast_card_sdiff (filter_subset _ _)] at h3
  linarith only [h3]

private lemma my_other_markov_local {α : Type*} {g : α → ℝ} {c ε : ℝ} {A : Finset α}
    (hc : 0 ≤ c) (hε : 0 ≤ ε) (hg : ∀ a ∈ A, 0 ≤ g a)
    (h : ∑ a ∈ A, g a ≤ ε * c * #A) : (1 - ε) * #A ≤ #{a ∈ A | g a ≤ c} := by
  rcases hc.lt_or_eq with (hc | rfl)
  · exact my_markov_local hc hg h
  simp only [mul_zero, zero_mul] at h
  classical
  rw [one_sub_mul, sub_le_comm, ← cast_card_sdiff (filter_subset _ A), ← filter_not,
    filter_false_of_mem]
  · simp only [card_empty, CharP.cast_eq_zero]; positivity
  intro i hi
  rw [(sum_eq_zero_iff_of_nonneg hg).1 (h.antisymm (sum_nonneg hg)) i hi]
  simp

private def LPropLocal (k m : ℕ) (ε : ℝ) (f : G → ℂ) (A : Finset G) (a : Fin k → G) : Prop :=
  ‖fun x : G ↦ ∑ i, f (x - a i) - (k • (μ A ∗ᵈ f)) x‖_[2 * m] ≤ k * ε * ‖f‖_[2 * m]

private noncomputable instance (k m : ℕ) (ε : ℝ) (f : G → ℂ) (A : Finset G) :
    DecidablePred (LPropLocal k m ε f A) := Classical.decPred _

private noncomputable def lLocal (k m : ℕ) (ε : ℝ) (f : G → ℂ) (A : Finset G) :
    Finset (Fin k → G) :=
  {x ∈ A ^^ k | LPropLocal k m ε f A x}

private lemma lemma28_local {A : Finset G} {f : G → ℂ} {ε : ℝ} {k m : ℕ}
    (hε : 0 < ε) (hm : 1 ≤ m) (hk : (64 : ℝ) * m / ε ^ 2 ≤ k) :
    (#A ^ k : ℝ) / 2 ≤ #(lLocal k m ε f A) := by
  have hk_pos : 0 < k := by
    rw [← @Nat.cast_pos ℝ]
    exact (div_pos (mul_pos (by norm_num) (by exact_mod_cast hm)) (pow_pos hε _)).trans_le hk
  rcases A.eq_empty_or_nonempty with (rfl | hA)
  · simp [zero_pow hk_pos.ne']
  have hm' : 2 * m ≠ 0 := by omega
  have hmeq : ((2 * m : ℕ) : ℝ≥0∞) = 2 * m := by rw [Nat.cast_mul, Nat.cast_two]
  have hmarkov_in : ∑ a ∈ A ^^ k,
      (‖fun x : G ↦ ∑ i : Fin k, f (x - a i) - (k • (μ A ∗ᵈ f)) x‖_[2 * m] ^ (2 * m) : ℝ) ≤
        1 / 2 * (k * ε * ‖f‖_[2 * m]) ^ (2 * m) * #A ^ k := by
    rw [← hmeq, mul_pow]
    simp only [dLpNorm_pow_eq_sum_norm hm']
    rw [sum_comm]
    have h_p1 : ∀ x : G, ∑ a ∈ A ^^ k,
        ‖∑ i, f (x - a i) - (k • (μ A ∗ᵈ f)) x‖ ^ (2 * m) ≤
      (8 * m) ^ m * k ^ (m - 1) *
        ∑ a ∈ A ^^ k, ∑ i, ‖f (x - a i) - (μ A ∗ᵈ f) x‖ ^ (2 * m) := fun x ↦ by
      let f' : G → ℂ := fun a ↦ f (x - a) - (μ A ∗ᵈ f) x
      calc
        _ = ∑ a ∈ A ^^ k, ‖∑ i, f' (a i)‖ ^ (2 * m) := by
          congr with a : 1
          simp only [sum_sub_distrib, Pi.smul_apply, sum_const, card_fin, f']
        _ ≤ (4 * m) ^ m * k ^ (m - 1) * ∑ a ∈ A ^^ k, ∑ i, ‖f' (a i)‖ ^ (2 * m) := by
          refine marcinkiewicz_zygmund_piFinset (by omega) f' ?_
          rw [sum_sub_distrib]
          simp only [sum_const]
          rw [← Pi.smul_apply (#A), ← smul_ddconv, card_smul_mu, ddconv_eq_sum_sub']
          simp only [boole_mul, Set.indicator_apply, mem_coe]
          rw [← sum_filter, filter_mem_eq_inter, univ_inter, sub_self]
        _ ≤ _ := by gcongr; norm_num
    refine (sum_le_sum fun x _ ↦ h_p1 x).trans ?_
    rw [← mul_sum]
    simp only [@sum_comm _ _ G]
    have h_norm_eq (a : Fin k → G) (i : Fin k) :
        ∑ x, ‖f (x - a i) - (μ A ∗ᵈ f) x‖ ^ (2 * m) =
          ‖τ (a i) f - μ A ∗ᵈ f‖_[2 * m] ^ (2 * m) := by
      rw [← hmeq, dLpNorm_pow_eq_sum_norm hm']
      simp only [Pi.sub_apply, translate_apply]
    simp only [h_norm_eq]
    have h_p2 :
        (8 * m) ^ m * k ^ (m - 1) * ∑ a ∈ A ^^ k, ∑ i, ‖τ (a i) f - μ A ∗ᵈ f‖_[2 * m] ^ (2 * m) ≤
          (8 * m) ^ m * k ^ (m - 1) * ∑ _a ∈ A ^^ k, ∑ _i : Fin k, (2 * ‖f‖_[2 * m]) ^ (2 * m) := by
      have hm_lt : 1 < 2 * m := by omega
      have hm'' : (1 : ℝ≥0∞) ≤ 2 * m := by rw [← hmeq, Nat.one_le_cast]; exact hm_lt.le
      gcongr with a _ i
      refine (dLpNorm_sub_le hm'').trans ?_
      rw [dLpNorm_translate, two_mul ‖f‖_[2 * m], add_le_add_iff_left]
      have hmeq' : ((2 * m : ℝ≥0) : ℝ≥0∞) = 2 * m := by
        rw [ENNReal.coe_mul, ENNReal.coe_two, ENNReal.coe_natCast]
      have h1lt : (1 : ℝ≥0) < 2 * m := by
        rw [← Nat.cast_two, ← Nat.cast_mul, Nat.one_lt_cast]; exact hm_lt
      rw [← hmeq', ddconv_comm]
      refine (dLpNorm_ddconv_le h1lt.le _ _).trans ?_
      rw [dL1Norm_mu hA, mul_one]
    refine le_trans (mod_cast h_p2) ?_
    simp only [sum_const, card_fin, Fintype.card_piFinset_const, nsmul_eq_mul]
    have hk_mul : (64 : ℝ) * m ≤ k * ε ^ 2 := by rwa [div_le_iff₀ (by positivity)] at hk
    have h_end : (8 * m : ℝ) ^ m * k ^ (m - 1) * (#A : ℝ) ^ k * (k * (2 * ‖f‖_[2 * m]) ^ (2 * m)) ≤
        1 / 2 * ((k * ε) ^ (2 * m) * ‖f‖_[2 * m] ^ (2 * m)) * (#A : ℝ) ^ k := by
      rw [mul_pow (2 : ℝ)]
      have hcoeff : (8 * m : ℝ) ^ m * k ^ (m - 1) * k * 2 ^ (2 * m) ≤
          1 / 2 * (k * ε) ^ (2 * m) := by
        calc
          (8 * m : ℝ) ^ m * k ^ (m - 1) * k * 2 ^ (2 * m)
            = (8 * m) ^ m * 2 ^ (2 * m) * (k ^ (m - 1) * k) := by ring
          _ = (64 * m * k / 2) ^ m := by
            rw [pow_sub_one_mul (by omega), pow_mul, ← mul_pow]; ring
          _ ≤ (k * ε ^ 2 * k / 2) ^ m := by gcongr
          _ = (k * ε) ^ (2 * m) / 2 ^ m := by ring_nf; simp_rw [one_div]
          _ ≤ (k * ε) ^ (2 * m) / 2 ^ 1 := by gcongr; norm_num
          _ = 1 / 2 * (k * ε) ^ (2 * m) := by ring
      calc
        (8 * m : ℝ) ^ m * k ^ (m - 1) * (#A : ℝ) ^ k * (k * (2 ^ (2 * m) * ‖f‖_[2 * m] ^ (2 * m)))
          = ((8 * m : ℝ) ^ m * k ^ (m - 1) * k * 2 ^ (2 * m)) *
              (‖f‖_[2 * m] ^ (2 * m) * (#A : ℝ) ^ k) := by ring
        _ ≤ (1 / 2 * (k * ε) ^ (2 * m)) * (‖f‖_[2 * m] ^ (2 * m) * (#A : ℝ) ^ k) :=
          mul_le_mul_of_nonneg_right hcoeff (by positivity)
        _ = 1 / 2 * ((k * ε) ^ (2 * m) * ‖f‖_[2 * m] ^ (2 * m)) * (#A : ℝ) ^ k := by ring
    rw [← dLpNorm_pow_eq_sum_norm hm' f, hmeq]
    push_cast at h_end ⊢
    linarith only [h_end]
  rw [← Nat.cast_pow, ← Fintype.card_piFinset_const] at hmarkov_in
  have hmk := my_other_markov_local (by positivity) (by norm_num)
    (fun _ _ ↦ by positivity) hmarkov_in
  norm_num1 at hmk
  rw [Fintype.card_piFinset_const, mul_comm, mul_one_div, Nat.cast_pow] at hmk
  refine hmk.trans_eq ?_
  rw [lLocal]
  congr with a : 3
  refine pow_le_pow_iff_left₀ ?_ ?_ ?_ <;> positivity

private lemma triangle_local {A : Finset G} {f : G → ℂ} {ε : ℝ} {k m : ℕ} {t : G} {a : Fin k → G}
    (ha : a ∈ lLocal k m ε f A) (ha' : (a + fun _ ↦ t) ∈ lLocal k m ε f A)
    (hk : 0 < k) (hm : 1 ≤ m) :
    ‖τ (-t) (μ A ∗ᵈ f) - μ A ∗ᵈ f‖_[2 * m] ≤ 2 * ε * ‖f‖_[2 * m] := by
  let f₁ : G → ℂ := fun x ↦ ∑ i, f (x - a i)
  let f₂ : G → ℂ := fun x ↦ ∑ i, f (x - a i - t)
  have hp : (1 : ℝ≥0∞) ≤ 2 * m := by norm_cast; omega
  have h₁ : ‖f₁ - k • (μ A ∗ᵈ f)‖_[2 * m] ≤ k * ε * ‖f‖_[2 * m] :=
    (Finset.mem_filter.mp ha).2
  have h₂ : ‖f₂ - k • (μ A ∗ᵈ f)‖_[2 * m] ≤ k * ε * ‖f‖_[2 * m] := by
    have h2' := (Finset.mem_filter.mp ha').2
    refine (le_of_eq ?_).trans h2'
    congr 1; ext x
    simp only [f₂, Pi.sub_apply, Pi.add_apply, sub_add_eq_sub_sub]
  have hf₁₂ : τ t f₁ = f₂ := by
    ext x
    simp only [f₁, f₂, translate_apply]
    exact Finset.sum_congr rfl fun i _ ↦ by rw [sub_right_comm]
  have h₅ : ‖τ (-t) (k • (μ A ∗ᵈ f)) - f₁‖_[2 * m] ≤ k * ε * ‖f‖_[2 * m] := by
    have htr : τ t (τ (-t) (k • (μ A ∗ᵈ f)) - f₁) = k • (μ A ∗ᵈ f) - f₂ := by
      rw [translate_sub_right, translate_translate, add_neg_cancel, translate_zero, hf₁₂]
    rw [← dLpNorm_translate t, htr, dLpNorm_sub_comm]
    exact h₂
  have hk_pos : (0 : ℝ) < k := by positivity
  refine le_of_mul_le_mul_left ?_ hk_pos
  rw [← nsmul_eq_mul, ← dLpNorm_nsmul _ (_ - μ A ∗ᵈ f), nsmul_sub,
    ← translate_smul_right (-t) (μ A ∗ᵈ f) k]
  calc
    ‖τ (-t) (k • (μ A ∗ᵈ f)) - k • (μ A ∗ᵈ f)‖_[2 * m]
      ≤ ‖τ (-t) (k • (μ A ∗ᵈ f)) - f₁‖_[2 * m] + ‖f₁ - k • (μ A ∗ᵈ f)‖_[2 * m] :=
        dLpNorm_sub_le_dLpNorm_sub_add_dLpNorm_sub hp
    _ ≤ k * ε * ‖f‖_[2 * m] + k * ε * ‖f‖_[2 * m] := add_le_add h₅ h₁
    _ = ↑k * (2 * ε * ‖f‖_[2 * m]) := by ring

/-- Localized `L^{2m}` almost-periodicity where the shift set is `(-s₀) +ᵥ T₀` with `T₀ ⊆ S`. -/
lemma almost_periodicity_sub {A S : Finset G} (hA : A.Nonempty) (hS : S.Nonempty)
    {ε K : ℝ} (hε : 0 < ε) (hε' : ε ≤ 1) (m : ℕ) (hm : 1 ≤ m) (f : G → ℂ)
    (hK₂ : 2 ≤ K) (hK : (σ[A, S] : ℝ) ≤ K) :
    ∃ (T₀ : Finset G) (s₀ : G),
      T₀ ⊆ S ∧
      K ^ (-512 * m / ε ^ 2 : ℝ) * #S ≤ #T₀ ∧
      ∀ t ∈ (-s₀) +ᵥ T₀, ‖τ t (μ A ∗ᵈ f) - μ A ∗ᵈ f‖_[2 * m] ≤ ε * ‖f‖_[2 * m] := by
  let k : ℕ := ⌈(64 : ℝ) * m / (ε / 2) ^ 2⌉₊
  have hk_pos : 0 < k := Nat.ceil_pos.mpr (by positivity)
  let L := lLocal k m (ε / 2) f A
  have hL_card : (#A : ℝ) ^ k / 2 ≤ #L :=
    lemma28_local (half_pos hε) hm (Nat.le_ceil _)
  have hL_ne : L.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
    exact hL_card.trans_lt' (by positivity)
  let g : (Fin k → G) × G → (Fin k → G) := fun p i ↦ p.1 i + p.2
  let Img : Finset (Fin k → G) := (L ×ˢ S).image g
  have hImg_sub : Img ⊆ (A + S) ^^ k := by
    intro x hx
    rcases Finset.mem_image.mp hx with ⟨⟨l, s⟩, hls, rfl⟩
    rcases Finset.mem_product.mp hls with ⟨hl, hs⟩
    have hlA : l ∈ A ^^ k := (Finset.mem_filter.mp hl).1
    exact Fintype.mem_piFinset.mpr fun i ↦ Finset.add_mem_add (Fintype.mem_piFinset.mp hlA i) hs
  have hImg_card : #Img ≤ #(A + S) ^ k :=
    (Finset.card_le_card hImg_sub).trans (by rw [Fintype.card_piFinset_const])
  have hImg_ne : Img.Nonempty := (hL_ne.product hS).image g
  have hpart : #L * #S = ∑ x ∈ Img, #{p ∈ L ×ˢ S | g p = x} := by
    rw [← Finset.card_product, ← Finset.card_eq_sum_card_fiberwise
      (fun p hp ↦ Finset.mem_image_of_mem g hp)]
  have hex_x : ∃ x₀ ∈ Img, #L * #S ≤ #Img * #{p ∈ L ×ˢ S | g p = x₀} := by
    have hsum : ∑ _x ∈ Img, (#L * #S) ≤ ∑ x ∈ Img, (#Img * #{p ∈ L ×ˢ S | g p = x}) := by
      rw [Finset.sum_const, smul_eq_mul, ← Finset.mul_sum, ← hpart]
    exact Finset.exists_le_of_sum_le hImg_ne hsum
  obtain ⟨x₀, hx₀, hfib_ge⟩ := hex_x
  let F : Finset ((Fin k → G) × G) := {p ∈ L ×ˢ S | g p = x₀}
  have hF_ne : F.Nonempty := by
    rcases Finset.mem_image.mp hx₀ with ⟨p₀, hp₀, hp₀_eq⟩
    exact ⟨p₀, Finset.mem_filter.mpr ⟨hp₀, hp₀_eq⟩⟩
  obtain ⟨⟨a, s₀⟩, has₀⟩ := hF_ne
  have haL : a ∈ L := (Finset.mem_product.mp (Finset.mem_filter.mp has₀).1).1
  have has₀_eq : g (a, s₀) = x₀ := (Finset.mem_filter.mp has₀).2
  let T₀ : Finset G := F.image Prod.snd
  have hT₀_sub : T₀ ⊆ S := by
    intro s hs
    rcases Finset.mem_image.mp hs with ⟨p, hp, rfl⟩
    exact (Finset.mem_product.mp (Finset.mem_filter.mp hp).1).2
  have hT₀_card : #T₀ = #F := by
    refine Finset.card_image_of_injOn fun p₁ hp₁ p₂ hp₂ hsnd ↦ ?_
    have hg1 : g p₁ = x₀ := (Finset.mem_filter.mp hp₁).2
    have hg2 : g p₂ = x₀ := (Finset.mem_filter.mp hp₂).2
    ext1
    · funext i
      have hi1 := congr_fun hg1 i
      have hi2 := congr_fun hg2 i
      dsimp [g] at hi1 hi2
      rw [hsnd] at hi1
      exact add_right_cancel (hi1.trans hi2.symm)
    · exact hsnd
  have hmul_le : #L * #S ≤ #(A + S) ^ k * #T₀ := by
    rw [hT₀_card]
    exact hfib_ge.trans (Nat.mul_le_mul_right _ hImg_card)
  have hT₀_ge : K ^ (-512 * m / ε ^ 2 : ℝ) * #S ≤ #T₀ := by
    have hAS_le : (#(A + S) : ℝ) ≤ K * #A := by
      rw [← Finset.cast_addConst_mul_card]
      gcongr
    have hk' : k = ⌈(256 : ℝ) * m / ε ^ 2⌉₊ := by
      dsimp [k]; congr 1; field_simp; ring
    have hAc_pos : (0 : ℝ) < (#A : ℝ) ^ k := by positivity
    have hK_pos : 0 < K := by positivity
    refine le_of_mul_le_mul_left ?_ hAc_pos
    rw [neg_mul, neg_div, Real.rpow_neg hK_pos.le, mul_left_comm,
      inv_mul_le_iff₀ (by positivity)]
    have hk_bound : (k : ℝ) + 1 ≤ 512 * m / ε ^ 2 := by
      rw [hk']
      set X : ℝ := (m : ℝ) / ε ^ 2
      have hX256 : (256 : ℝ) * m / ε ^ 2 = 256 * X := by dsimp [X]; ring
      have hX512 : (512 : ℝ) * m / ε ^ 2 = 512 * X := by dsimp [X]; ring
      rw [hX256, hX512]
      have h₄ : (⌈256 * X⌉₊ : ℝ) < 256 * X + 1 := Nat.ceil_lt_add_one (by dsimp [X]; positivity)
      have h₅ : (1 : ℝ) ≤ X := by
        have hm1 : (1 : ℝ) ≤ m := Nat.one_le_cast.mpr hm
        have hε2 : ε ^ 2 ≤ 1 := pow_le_one₀ hε.le hε'
        exact (one_le_div (by positivity)).mpr (hε2.trans hm1)
      linarith only [h₄, h₅]
    calc
      (#A : ℝ) ^ k * #S = 2 * ((#A : ℝ) ^ k / 2) * #S := by ring
      _ ≤ K * #L * #S := by gcongr
      _ = K * ↑(#L * #S) := by push_cast; ring
      _ ≤ K * ↑(#(A + S) ^ k * #T₀) := by gcongr
      _ = K * (#(A + S) : ℝ) ^ k * #T₀ := by push_cast; ring
      _ ≤ K * (K * #A) ^ k * #T₀ := by gcongr
      _ = K ^ ((k : ℝ) + 1) * (#A : ℝ) ^ k * #T₀ := by
        rw [Real.rpow_add hK_pos, Real.rpow_natCast, Real.rpow_one, mul_pow]; ring
      _ ≤ K ^ (512 * m / ε ^ 2 : ℝ) * ((#A : ℝ) ^ k * #T₀) := by
        rw [mul_assoc]
        exact mul_le_mul_of_nonneg_right
          (Real.rpow_le_rpow_of_exponent_le (one_le_two.trans hK₂) hk_bound) (by positivity)
  refine ⟨T₀, s₀, hT₀_sub, hT₀_ge, fun t ht ↦ ?_⟩
  rcases Finset.mem_vadd_finset.mp ht with ⟨s, hsT₀, rfl⟩
  rcases Finset.mem_image.mp hsT₀ with ⟨⟨l, s'⟩, hls_F, hs_eq⟩
  change s' = s at hs_eq
  subst hs_eq
  have hlL : l ∈ L := (Finset.mem_product.mp (Finset.mem_filter.mp hls_F).1).1
  have hgs : g (l, s') = x₀ := (Finset.mem_filter.mp hls_F).2
  have ha_shift : (a + fun _ ↦ (s₀ - s')) = l := by
    ext i
    have hi1 := congr_fun has₀_eq i
    have hi2 := congr_fun hgs i
    dsimp [g] at hi1 hi2
    have hsum : a i + s₀ = l i + s' := hi1.trans hi2.symm
    calc
      a i + (s₀ - s') = (a i + s₀) - s' := by abel
      _ = (l i + s') - s' := by rw [hsum]
      _ = l i := by abel
  have htri := triangle_local haL (by rwa [ha_shift]) hk_pos hm
  have hneg : -(s₀ - s') = -s₀ + s' := by abel
  have heps : 2 * (ε / 2) = ε := by ring
  simpa [hneg, heps] using htri

/-- Localized `L^∞` boosted almost-periodicity keeping `T = (-s₀) +ᵥ T₀` (`T₀ ⊆ S`). -/
lemma linfty_ap_boosted_sub {A S B_ind C_ind : Finset G}
    (hA : A.Nonempty) (hS : S.Nonempty) (hB : B_ind.Nonempty) (hC : C_ind.Nonempty)
    {ε K : ℝ} (hε₀ : 0 < ε) (hε₁ : ε ≤ 1) (k : ℕ) (hk : k ≠ 0)
    (hK₂ : 2 ≤ K) (hK : (σ[A, S] : ℝ) ≤ K) :
    ∃ (T₀ : Finset G) (s₀ : G),
      T₀ ⊆ S ∧
      K ^ (-4096 * ⌈1 + log (min 1 ((#C_ind : ℝ) / #B_ind))⁻¹⌉ *
        k ^ 2 / ε ^ 2 : ℝ) * #S ≤ #T₀ ∧
      ‖μ ((-s₀) +ᵥ T₀) ∗ᵈ^ k ∗ᵈ (μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind) -
          μ A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind‖_[∞] ≤ ε := by
  let r : ℝ := min 1 ((#C_ind : ℝ) / #B_ind)
  have hr₀ : 0 < r := lt_min zero_lt_one (by positivity)
  have hr₁ : r ≤ 1 := min_le_left _ _
  let m_real : ℝ := 1 + log r⁻¹
  have hm₀ : 0 < m_real := curlog_pos hr₀.le hr₁
  let m : ℕ := ⌈m_real⌉₊
  have hm₁ : 1 ≤ m := Nat.one_le_iff_ne_zero.mpr (Nat.ceil_pos.mpr hm₀).ne'
  let ε₁ : ℝ := ε / (k * exp 1)
  have hε₁_pos : 0 < ε₁ := by dsimp [ε₁]; positivity
  have hε₁_le : ε₁ ≤ 1 := by
    dsimp [ε₁]
    refine div_le_one_of_le₀ ?_ (by positivity)
    have hk1 : (1 : ℝ) ≤ k := Nat.one_le_cast.mpr (Nat.pos_of_ne_zero hk)
    have he1 : (1 : ℝ) ≤ exp 1 := one_le_exp zero_le_one
    nlinarith
  obtain ⟨T₀, s₀, hT₀_sub, hKT, hT⟩ :=
    almost_periodicity_sub hA hS hε₁_pos hε₁_le m hm₁ 𝟭_[B_ind] hK₂ hK
  norm_cast at hT
  let T := (-s₀) +ᵥ T₀
  have hcardT : #T = #T₀ := Finset.card_vadd_finset (-s₀) T₀
  have hKT_boost : K ^ (-4096 * ⌈m_real⌉ * k ^ 2 / ε ^ 2 : ℝ) * #S ≤ #T₀ := by
    refine le_trans ?_ hKT
    refine mul_le_mul_of_nonneg_right
      (Real.rpow_le_rpow_of_exponent_le (one_le_two.trans hK₂) ?_) (Nat.cast_nonneg _)
    rw [← natCast_ceil_eq_intCast_ceil hm₀.le]
    dsimp [ε₁, m]
    have hexp2 : exp 1 ^ 2 ≤ 8 := by
      calc
        exp 1 ^ 2 ≤ (2.7182818286 : ℝ) ^ 2 := by gcongr; exact exp_one_lt_d9.le
        _ ≤ 8 := by norm_num
    have hdiv_pos : 0 ≤ (⌈m_real⌉₊ : ℝ) * k ^ 2 / ε ^ 2 := by positivity
    have hcalc : (-512 * (⌈m_real⌉₊ : ℝ)) / (ε / (k * exp 1)) ^ 2 =
        (-512 * exp 1 ^ 2) * ((⌈m_real⌉₊ : ℝ) * k ^ 2 / ε ^ 2) := by field_simp
    have hcalc2 : (-4096 * (⌈m_real⌉₊ : ℝ) * k ^ 2 / ε ^ 2 : ℝ) =
        (-4096) * ((⌈m_real⌉₊ : ℝ) * k ^ 2 / ε ^ 2) := by ring
    rw [hcalc, hcalc2]
    nlinarith
  have hT_linf : ∀ t ∈ T,
      ‖τ t (μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind) - μ A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind‖_[∞] ≤ ε / k := by
    intro t ht
    set M : ℕ := 2 * m
    have hM₀ : (M : ℝ≥0) ≠ 0 := by dsimp [M]; positivity
    have hM₁ : 1 < (M : ℝ≥0) := by norm_cast; simp [← Nat.succ_le_iff, M]; omega
    have hM : (M : ℝ≥0).HolderConjugate (NNReal.conjExponent M) :=
      NNReal.HolderConjugate.conjExponent hM₁
    let _ : (M : ℝ≥0∞).HolderConjugate (NNReal.conjExponent M) := hM.coe_ennreal
    let G_diff : G → ℂ := τ t (μ A ∗ᵈ 𝟭_[B_ind]) - μ A ∗ᵈ 𝟭_[B_ind]
    have hpoint : ∀ x : G,
        (τ t (μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind) - μ A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind : G → ℂ) x =
          ∑ y : G, G_diff y * μ (x +ᵥ -C_ind) y := by
      intro x
      calc
        (τ t (μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind) - μ A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind : G → ℂ) x
          = (G_diff ∗ᵈ μ C_ind) x := by simp [sub_ddconv, G_diff]
        _ = ∑ y, G_diff y * μ C_ind (x - y) := ddconv_eq_sum_sub' ..
        _ = ∑ y, G_diff y * μ (x +ᵥ -C_ind) y := by simp [neg_add_eq_sub]
    rw [dLinftyNorm_eq_iSup_norm]
    refine ciSup_le fun x ↦ ?_
    have hT_M : ‖G_diff‖_[M] ≤ ε₁ * (#B_ind : ℝ) ^ (M : ℝ)⁻¹ := by
      simpa [G_diff, ← ENNReal.coe_natCast, dLpNorm_indicator_one hM₀] using hT t ht
    have hC_norm : ‖μ_[ℂ] (x +ᵥ -C_ind)‖_[NNReal.conjExponent M] =
        (#C_ind : ℝ) ^ (-(M : ℝ)⁻¹) := by
      rw [dLpNorm_mu hM.symm.lt.le hC.neg.vadd_finset, Finset.card_vadd_finset, Finset.card_neg,
        hM.symm.coe.inv_sub_one, NNReal.coe_natCast]
    have hrpow_exp : ((#C_ind : ℝ) / #B_ind) ^ (-(M : ℝ)⁻¹) ≤ exp 1 := by
      calc
        ((#C_ind : ℝ) / #B_ind) ^ (-(M : ℝ)⁻¹)
          ≤ r ^ (-(M : ℝ)⁻¹) :=
            rpow_le_rpow_of_nonpos hr₀ (min_le_right _ _) (neg_nonpos.mpr (by positivity))
        _ ≤ r ^ (-m_real⁻¹) := by
            refine rpow_le_rpow_of_exponent_ge hr₀ hr₁ (neg_le_neg (inv_anti₀ hm₀ ?_))
            have hm_le : m_real ≤ m := Nat.le_ceil _
            have h2m : (m : ℝ) ≤ M := by dsimp [M]; push_cast; linarith
            exact hm_le.trans h2m
        _ ≤ exp 1 := by
            rcases hr₁.eq_or_lt with hr_eq | hr_lt
            · rw [hr_eq, one_rpow]
              exact one_le_exp zero_le_one
            · have hlog_pos : 0 < log r⁻¹ := log_pos ((one_lt_inv₀ hr₀).mpr hr_lt)
              calc
                r ^ (-m_real⁻¹) ≤ r ^ (-(log r⁻¹)⁻¹) := by
                  refine rpow_le_rpow_of_exponent_ge hr₀ hr₁ (neg_le_neg (inv_anti₀ hlog_pos ?_))
                  dsimp [m_real]; linarith
                _ = (r⁻¹) ^ (log r⁻¹)⁻¹ := by
                  rw [rpow_neg hr₀.le, inv_rpow hr₀.le]
                _ ≤ exp 1 := r⁻¹.rpow_inv_log_le_exp_one
    calc
      ‖(τ t (μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind) - μ A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind : G → ℂ) x‖
        = ‖∑ y, G_diff y * μ (x +ᵥ -C_ind) y‖ := by rw [hpoint x]
      _ ≤ ∑ y, ‖G_diff y * μ (x +ᵥ -C_ind) y‖ := norm_sum_le _ _
      _ = ‖G_diff * μ (x +ᵥ -C_ind)‖_[1] := by rw [dL1Norm_eq_sum_norm]; rfl
      _ ≤ ‖G_diff‖_[M] * ‖μ_[ℂ] (x +ᵥ -C_ind)‖_[NNReal.conjExponent M] := dLpNorm_mul_le _ _
      _ ≤ (ε₁ * (#B_ind : ℝ) ^ (M : ℝ)⁻¹) * (#C_ind : ℝ) ^ (-(M : ℝ)⁻¹) := by
          rw [hC_norm]; gcongr
      _ = (ε / k) * (((#C_ind : ℝ) / #B_ind) ^ (-(M : ℝ)⁻¹) / exp 1) := by
          dsimp [ε₁]
          rw [rpow_neg (by positivity), rpow_neg (by positivity), div_rpow (by positivity)
            (by positivity), inv_div]
          field_simp [exp_ne_zero]
      _ ≤ (ε / k) * 1 := by
          gcongr
          exact (div_le_one (exp_pos 1)).mpr hrpow_exp
      _ = ε / k := mul_one _
  let F := μ_[ℂ] A ∗ᵈ 𝟭_[B_ind] ∗ᵈ μ C_ind
  have hT_ne : T.Nonempty := by
    have hpos : (0 : ℝ) < #T₀ := hKT_boost.trans_lt' (by positivity)
    rw [← Finset.card_pos, hcardT, ← @Nat.cast_pos ℝ]
    exact hpos
  refine ⟨T₀, s₀, hT₀_sub, hKT_boost, ?_⟩
  calc
    ‖μ T ∗ᵈ^ k ∗ᵈ F - F‖_[∞]
      = ‖𝔼 a ∈ T ^^ k, (τ (∑ i, a i) F - F)‖_[∞] := by
        rw [mu_iterConv_ddconv, Finset.expect_sub_distrib, Finset.expect_const hT_ne.piFinset_const]
    _ ≤ 𝔼 a ∈ T ^^ k, ‖τ (∑ i, a i) F - F‖_[∞] := dLpNorm_expect_le le_top
    _ ≤ 𝔼 _a ∈ T ^^ k, ε := by
        refine Finset.expect_le_expect fun a ha ↦ ?_
        calc
          ‖τ (∑ i, a i) F - F‖_[∞]
            ≤ ∑ i, ‖τ (a i) F - F‖_[∞] := dLpNorm_translate_sum_sub_le le_top _ _ _
          _ ≤ ∑ _i : Fin k, (ε / k) :=
            Finset.sum_le_sum fun i _ ↦ hT_linf (a i) (Fintype.mem_piFinset.mp ha i)
          _ = ε := by
            simp only [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
            exact mul_div_cancel₀ ε (Nat.cast_ne_zero.mpr hk)
    _ = ε := Finset.expect_const hT_ne.piFinset_const _

end LocalizedAlmostPeriodicity

section RelativeChang
variable {G : Type*} [AddCommGroup G] [Fintype G] [MeasurableSpace G] [DiscreteMeasurableSpace G]

omit [Fintype G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
/-- Riesz product `∏_{γ ∈ Γ} (1 + Re(ω γ * γ x))`. -/
noncomputable def rieszProd (Γ : Finset (AddChar G ℂ)) (ω : AddChar G ℂ → ℂ) (x : G) : ℝ :=
  ∏ γ ∈ Γ, (1 + (ω γ * γ x).re)

omit [Fintype G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
lemma rieszProd_pos_of_half [Finite G] {Γ : Finset (AddChar G ℂ)} {ω : AddChar G ℂ → ℂ}
    (hω : ∀ γ ∈ Γ, ‖ω γ‖ ≤ 2⁻¹) (x : G) : 0 < rieszProd Γ ω x := by
  unfold rieszProd
  refine Finset.prod_pos fun γ hγ ↦ ?_
  have h1 : |(ω γ * γ x).re| ≤ 2⁻¹ := by
    calc
      |(ω γ * γ x).re| ≤ ‖ω γ * γ x‖ := Complex.abs_re_le_norm _
      _ = ‖ω γ‖ := by rw [norm_mul, AddChar.norm_apply, mul_one]
      _ ≤ 2⁻¹ := hω γ hγ
  linarith [(abs_le.mp h1).1]

omit [Fintype G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
lemma rieszProd_factor_ge_half [Finite G] {ω_γ : ℂ} (hω : ‖ω_γ‖ ≤ 2⁻¹) (γ : AddChar G ℂ) (x : G) :
    2⁻¹ ≤ 1 + (ω_γ * γ x).re := by
  have h1 : |(ω_γ * γ x).re| ≤ 2⁻¹ := by
    calc
      |(ω_γ * γ x).re| ≤ ‖ω_γ * γ x‖ := Complex.abs_re_le_norm _
      _ = ‖ω_γ‖ := by rw [norm_mul, AddChar.norm_apply, mul_one]
      _ ≤ 2⁻¹ := hω
  linarith [(abs_le.mp h1).1]

omit [MeasurableSpace G] [DiscreteMeasurableSpace G] in
/-- A subset `Γ` is Riesz-good wrt probability weight `ν` if all `‖ω‖ ≤ 1/2` Riesz products have
expectation `≤ exp(#Γ / 32)`. -/
def RieszGood (ν : G → ℝ) (Γ : Finset (AddChar G ℂ)) : Prop :=
  ∀ ω : AddChar G ℂ → ℂ, (∀ γ ∈ Γ, ‖ω γ‖ ≤ 2⁻¹) →
    ∑ x : G, ν x * rieszProd Γ ω x ≤ exp ((#Γ : ℝ) / 32)

omit [MeasurableSpace G] [DiscreteMeasurableSpace G] in
lemma rieszGood_empty {ν : G → ℝ} (hν₁ : ∑ x : G, ν x = 1) : RieszGood ν ∅ := by
  intro _ _
  simp [rieszProd, hν₁]

private lemma sinh_div_cosh_quarter_le_half : |sinh (4⁻¹ : ℝ) / cosh (4⁻¹ : ℝ)| ≤ 2⁻¹ := by
  have he_lt : exp (4⁻¹ : ℝ) < 3 / 2 := by
    by_contra! hge
    have hpow : (3 / 2 : ℝ) ^ 4 ≤ exp (4⁻¹ : ℝ) ^ 4 := pow_le_pow_left₀ (by norm_num) hge 4
    have hexp4 : exp (4⁻¹ : ℝ) ^ 4 = exp 1 := by
      rw [← exp_nat_mul]; norm_num
    rw [hexp4] at hpow
    linarith [exp_one_lt_d9]
  have he_inv_gt : 2 / 3 < exp (-(4⁻¹ : ℝ)) := by
    rw [exp_neg]
    have h23 : exp (4⁻¹ : ℝ) < (2 / 3 : ℝ)⁻¹ := he_lt.trans_eq (by norm_num)
    exact (lt_inv_comm₀ (by norm_num) (exp_pos _)).mpr h23
  have hsinh_nonneg : 0 ≤ sinh (4⁻¹ : ℝ) := sinh_nonneg_iff.mpr (by norm_num)
  have hsinh_lt : sinh (4⁻¹ : ℝ) < 2⁻¹ := by
    rw [sinh_eq]
    linarith
  have hcosh_ge : 1 ≤ cosh (4⁻¹ : ℝ) := one_le_cosh _
  rw [abs_of_nonneg (div_nonneg hsinh_nonneg (by linarith))]
  exact (div_le_iff₀ (by linarith)).mpr (by nlinarith)

/-- Size upper bound for any `RieszGood` subset inside `largeSpec (μ T₀) 2⁻¹`. -/
lemma card_le_of_rieszGood {B₀ : BohrSet G} (hreg : B₀.IsRegular) (hpos : B₀.PosWidth)
    {T₀ : Finset G} (hT₀_ne : T₀.Nonempty) (hT₀_sub : T₀ ⊆ B₀.finset)
    {η₀ : ℝ} (hη₀ : 0 < η₀) (hη_card : η₀ * #B₀.finset ≤ #T₀)
    {Γ : Finset (AddChar G ℂ)} (hΓ_spec : Γ ⊆ largeSpec (μ_[ℂ] T₀) 2⁻¹)
    (hΓ_good : RieszGood (fun x ↦ B₀.bohrWeight x / ∑ z, B₀.bohrWeight z) Γ) :
    (#Γ : ℝ) ≤ 16 * log (4 / η₀) := by
  classical
  let Z : ℝ := ∑ z : G, B₀.bohrWeight z
  have hB₀_pos : (0 : ℝ) < #B₀.finset := by exact_mod_cast B₀.card_finset_pos
  have hZ_ge : (#B₀.finset : ℝ) ≤ Z := BohrSet.card_le_sum_bohrWeight hpos
  have hZ_le : Z ≤ 4 * (#B₀.finset : ℝ) := BohrSet.sum_bohrWeight_le hreg hpos
  have hZ_pos : 0 < Z := hB₀_pos.trans_le hZ_ge
  let ν : G → ℝ := fun x ↦ B₀.bohrWeight x / Z
  have hμ_norm : ‖μ_[ℂ] T₀‖_[1] = 1 := dL1Norm_mu hT₀_ne
  choose c hc_norm hc_eq using fun γ : AddChar G ℂ ↦
    Complex.exists_norm_mul_eq_self (dft (μ_[ℂ] T₀) γ)
  let u : AddChar G ℂ → ℂ := fun γ ↦ conj (c γ)
  have hcorr : ∀ γ ∈ Γ, 2⁻¹ ≤ (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, (u γ * conj (γ x)).re := by
    intro γ hγ
    have hmem := mem_largeSpec.mp (hΓ_spec hγ)
    rw [hμ_norm, mul_one] at hmem
    have hprod : u γ * dft (μ_[ℂ] T₀) γ = ((‖dft (μ_[ℂ] T₀) γ‖ : ℝ) : ℂ) := by
      dsimp [u]
      conv_lhs => rw [← hc_eq γ]
      rw [← mul_assoc, Complex.conj_mul', hc_norm γ, Complex.ofReal_one, one_pow, one_mul]
    have hre : (u γ * dft (μ_[ℂ] T₀) γ).re = ‖dft (μ_[ℂ] T₀) γ‖ := by
      rw [hprod, Complex.ofReal_re]
    have hmem' : 2⁻¹ ≤ (u γ * dft (μ_[ℂ] T₀) γ).re := by linarith only [hmem, hre]
    rw [dft_apply, wInner_one_eq_sum] at hmem'
    simp only [RCLike.inner_apply] at hmem'
    simp_rw [mul_comm (μ_[ℂ] T₀ _) (conj (γ _))] at hmem'
    have hsum_T₀ : (u γ * ∑ x : G, conj (γ x) * μ_[ℂ] T₀ x).re =
        (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, (u γ * conj (γ x)).re := by
      rw [Finset.mul_sum, Complex.re_sum]
      rw [← Finset.sum_subset (Finset.subset_univ T₀)]
      · rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun x hx ↦ ?_
        have hmu : μ_[ℂ] T₀ x = (((#T₀ : ℝ)⁻¹ : ℝ) : ℂ) := by
          simp [mu_apply, hx]
        rw [hmu, ← mul_assoc, mul_comm _ (((#T₀ : ℝ)⁻¹ : ℝ) : ℂ), Complex.re_ofReal_mul]
      · intro x _ hx
        simp [mu_apply, hx]
    linarith only [hmem', hsum_T₀]
  have hre_conj : ∀ (γ : AddChar G ℂ) (x : G),
      (u γ * conj (γ x)).re = (conj (u γ) * γ x).re := fun γ x ↦
    (Complex.conj_re (u γ * conj (γ x))).symm.trans (by simp [map_mul])
  let g : G → ℝ := fun x ↦ (4⁻¹ : ℝ) * ∑ γ ∈ Γ, (conj (u γ) * γ x).re
  have havg_ge : (#Γ : ℝ) / 8 ≤ (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, g x := by
    have hswap : (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, g x =
        (4⁻¹ : ℝ) * ∑ γ ∈ Γ, ((#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, (u γ * conj (γ x)).re) := by
      dsimp [g]
      simp_rw [← hre_conj, ← Finset.mul_sum]
      rw [Finset.sum_comm]
      ring
    rw [hswap]
    calc
      (#Γ : ℝ) / 8 = (4⁻¹ : ℝ) * ∑ _γ ∈ Γ, (2⁻¹ : ℝ) := by simp; ring
      _ ≤ (4⁻¹ : ℝ) * ∑ γ ∈ Γ, ((#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, (u γ * conj (γ x)).re) := by
        gcongr with γ hγ
        exact hcorr γ hγ
  have hjensen : exp ((#Γ : ℝ) / 8) ≤ (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x) := by
    let avg : ℝ := (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, g x
    have hT₀_pos : (0 : ℝ) < #T₀ := by exact_mod_cast hT₀_ne.card_pos
    have hstep : ∀ x ∈ T₀, 1 + (g x - avg) ≤ exp (g x) * exp (-avg) := fun x _ ↦ by
      calc
        1 + (g x - avg) ≤ exp (g x - avg) := by linarith [add_one_le_exp (g x - avg)]
        _ = exp (g x) * exp (-avg) := by rw [sub_eq_add_neg, exp_add]
    have hsum := Finset.sum_le_sum hstep
    have hsum_lhs : ∑ x ∈ T₀, (1 + (g x - avg)) = #T₀ := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_const, Finset.sum_const,
        nsmul_eq_mul, nsmul_eq_mul, mul_one]
      dsimp [avg]
      rw [mul_inv_cancel_left₀ hT₀_pos.ne']
      ring
    rw [hsum_lhs, ← Finset.sum_mul] at hsum
    have hexp_avg : exp avg ≤ (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x) := by
      have h1 := mul_le_mul_of_nonneg_right hsum (by positivity : 0 ≤ exp avg / #T₀)
      calc
        exp avg = (#T₀ : ℝ) * (exp avg / #T₀) := by field_simp [hT₀_pos.ne']
        _ ≤ ((∑ x ∈ T₀, exp (g x)) * exp (-avg)) * (exp avg / #T₀) := h1
        _ = (#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x) := by
            rw [mul_div_assoc', mul_assoc, ← exp_add, neg_add_cancel, exp_zero, mul_one,
              div_eq_inv_mul]
    exact (exp_le_exp.mpr havg_ge).trans hexp_avg
  have hT₀_to_ν : (η₀ / 4) * exp ((#Γ : ℝ) / 8) ≤ ∑ x : G, ν x * exp (g x) := by
    have hT₀_pos : (0 : ℝ) < #T₀ := by exact_mod_cast hT₀_ne.card_pos
    calc
      (η₀ / 4) * exp ((#Γ : ℝ) / 8)
        ≤ (η₀ / 4) * ((#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x)) :=
          mul_le_mul_of_nonneg_left hjensen (by positivity)
      _ ≤ ((#T₀ : ℝ) / Z) * ((#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x)) := by
          refine mul_le_mul_of_nonneg_right ?_
            (mul_nonneg (inv_nonneg.mpr (Nat.cast_nonneg _))
              (Finset.sum_nonneg fun _ _ ↦ (exp_pos _).le))
          rw [div_le_div_iff₀ (by norm_num) hZ_pos]
          nlinarith only [hη_card, hZ_le, hη₀]
      _ = ∑ x ∈ T₀, ν x * exp (g x) := by
          have : ((#T₀ : ℝ) / Z) * ((#T₀ : ℝ)⁻¹ * ∑ x ∈ T₀, exp (g x)) =
              Z⁻¹ * ∑ x ∈ T₀, exp (g x) := by field_simp [hT₀_pos.ne']
          rw [this, Finset.mul_sum]
          refine Finset.sum_congr rfl fun x hx ↦ ?_
          have hw1 : B₀.bohrWeight x = 1 :=
            BohrSet.bohrWeight_eq_one_of_mem hpos (hT₀_sub hx)
          dsimp [ν]; rw [hw1]; ring
      _ ≤ ∑ x : G, ν x * exp (g x) :=
          Finset.sum_le_univ_sum_of_nonneg fun x ↦
            mul_nonneg (div_nonneg (B₀.bohrWeight_pos x).le hZ_pos.le) (exp_pos _).le
  let th : ℝ := sinh (4⁻¹ : ℝ) / cosh (4⁻¹ : ℝ)
  let ω : AddChar G ℂ → ℂ := fun γ ↦ (th : ℂ) * conj (u γ)
  have hω_le : ∀ γ ∈ Γ, ‖ω γ‖ ≤ 2⁻¹ := fun γ _ ↦ by
    dsimp [ω, u]
    rw [norm_mul, Complex.norm_real, RCLike.norm_conj, RCLike.norm_conj, hc_norm γ, mul_one,
      Real.norm_eq_abs]
    exact sinh_div_cosh_quarter_le_half
  have hexp_pt : ∀ x : G, exp (g x) ≤ exp ((#Γ : ℝ) / 32) * rieszProd Γ ω x := by
    intro x
    have hprod_eq : exp (g x) = ∏ γ ∈ Γ, exp ((4⁻¹ : ℝ) * (conj (u γ) * γ x).re) := by
      dsimp [g]; rw [Finset.mul_sum, exp_sum]
    rw [hprod_eq]
    have hcosh_pos : 0 < cosh (4⁻¹ : ℝ) := cosh_pos _
    have hfac : ∀ γ ∈ Γ, exp ((4⁻¹ : ℝ) * (conj (u γ) * γ x).re) ≤
        cosh (4⁻¹ : ℝ) * (1 + (ω γ * γ x).re) := by
      intro γ _
      have hy : |(conj (u γ) * γ x).re| ≤ 1 := by
        calc
          |(conj (u γ) * γ x).re| ≤ ‖conj (u γ) * γ x‖ := Complex.abs_re_le_norm _
          _ = 1 := by
            dsimp [u]
            rw [norm_mul, RCLike.norm_conj, RCLike.norm_conj, hc_norm γ, AddChar.norm_apply,
              one_mul]
      have h1 := exp_mul_le_cosh_add_mul_sinh hy (4⁻¹ : ℝ)
      rw [mul_comm _ (4⁻¹ : ℝ)] at h1
      have hrew : cosh (4⁻¹ : ℝ) + (conj (u γ) * γ x).re * sinh (4⁻¹ : ℝ) =
          cosh (4⁻¹ : ℝ) * (1 + (ω γ * γ x).re) := by
        dsimp [ω, th]
        rw [mul_assoc, Complex.re_ofReal_mul]
        field_simp [hcosh_pos.ne']
      exact h1.trans_eq hrew
    calc
      ∏ γ ∈ Γ, exp ((4⁻¹ : ℝ) * (conj (u γ) * γ x).re)
        ≤ ∏ γ ∈ Γ, (cosh (4⁻¹ : ℝ) * (1 + (ω γ * γ x).re)) := by
          gcongr with γ hγ
          exact hfac γ hγ
      _ = cosh (4⁻¹ : ℝ) ^ #Γ * rieszProd Γ ω x := by
          rw [Finset.prod_mul_distrib, Finset.prod_const]; rfl
      _ ≤ (exp ((4⁻¹ : ℝ) ^ 2 / 2)) ^ #Γ * rieszProd Γ ω x := by
          gcongr
          · exact (rieszProd_pos_of_half hω_le x).le
          · exact cosh_le_exp_half_sq _
      _ = exp ((#Γ : ℝ) / 32) * rieszProd Γ ω x := by
          rw [← exp_nat_mul]; congr 2; ring
  have hupper : ∑ x : G, ν x * exp (g x) ≤ exp ((#Γ : ℝ) / 16) := by
    calc
      ∑ x : G, ν x * exp (g x)
        ≤ ∑ x : G, ν x * (exp ((#Γ : ℝ) / 32) * rieszProd Γ ω x) := by
          refine Finset.sum_le_sum fun x _ ↦ mul_le_mul_of_nonneg_left (hexp_pt x) ?_
          exact div_nonneg (B₀.bohrWeight_pos x).le hZ_pos.le
      _ = exp ((#Γ : ℝ) / 32) * ∑ x : G, ν x * rieszProd Γ ω x := by
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun _ _ ↦ by ring
      _ ≤ exp ((#Γ : ℝ) / 32) * exp ((#Γ : ℝ) / 32) :=
          mul_le_mul_of_nonneg_left (hΓ_good ω hω_le) (exp_pos _).le
      _ = exp ((#Γ : ℝ) / 16) := by rw [← exp_add]; congr 1; ring
  have hcomb : (η₀ / 4) * exp ((#Γ : ℝ) / 8) ≤ exp ((#Γ : ℝ) / 16) := hT₀_to_ν.trans hupper
  have hdiv : exp ((#Γ : ℝ) / 16) ≤ 4 / η₀ := by
    have h1 : (η₀ / 4) * exp ((#Γ : ℝ) / 16) ≤ 1 := by
      have hprod : exp ((#Γ : ℝ) / 8) = exp ((#Γ : ℝ) / 16) * exp ((#Γ : ℝ) / 16) := by
        rw [← exp_add]; congr 1; ring
      rw [hprod, ← mul_assoc] at hcomb
      exact le_of_mul_le_mul_right (by simpa using hcomb) (exp_pos _)
    rwa [div_mul_eq_mul_div, div_le_iff₀ (by norm_num), one_mul, ← le_div_iff₀' hη₀] at h1
  have hlog := log_le_log (exp_pos _) hdiv
  rw [log_exp] at hlog
  linarith

/-- Bohr relative Chang's lemma: every character in `largeSpec (μ T₀) 2⁻¹` is within `ε_spec` of `1`
on `(ρ • B₀) ⊓ ofWidth δ Γ` for a subset `Γ` of size `≤ 16 * log (4 / η₀)`. -/
lemma bohr_relative_chang {B₀ : BohrSet G} (hreg : B₀.IsRegular) (hpos : B₀.PosWidth)
    {T₀ : Finset G} (hT₀_ne : T₀.Nonempty) (hT₀_sub : T₀ ⊆ B₀.finset)
    {η₀ ε_spec : ℝ} (hη₀ : 0 < η₀) (hη_card : η₀ * #B₀.finset ≤ #T₀)
    (hε₀ : 0 < ε_spec) (hε₁ : ε_spec ≤ 1) :
    ∃ Γ ⊆ largeSpec (μ_[ℂ] T₀) 2⁻¹,
      (#Γ : ℝ) ≤ 16 * log (4 / η₀) ∧
      ∀ (ρ δ : ℝ), 0 < ρ → ∀ (hδ₀ : 0 < δ),
        ρ ≤ ε_spec / (2 ^ 18 * (B₀.rank + 1 : ℝ) ^ 2) →
        δ ≤ ε_spec / (2 ^ 10 * (#Γ + 1 : ℝ)) →
        ∀ y ∈ ((ρ • B₀) ⊓ BohrSet.ofWidth (fun _ ↦ (⟨δ, hδ₀.le⟩ : ℝ≥0)) Γ).finset,
          ∀ ψ ∈ largeSpec (μ_[ℂ] T₀) 2⁻¹, ‖1 - ψ y‖ ≤ ε_spec := by
  classical
  let Δ := largeSpec (μ_[ℂ] T₀) 2⁻¹
  let Z : ℝ := ∑ z : G, B₀.bohrWeight z
  have hB₀_pos : (0 : ℝ) < #B₀.finset := by exact_mod_cast B₀.card_finset_pos
  have hZ_pos : 0 < Z := hB₀_pos.trans_le (BohrSet.card_le_sum_bohrWeight hpos)
  let ν : G → ℝ := fun x ↦ B₀.bohrWeight x / Z
  have hν_sum : ∑ x : G, ν x = 1 := by
    dsimp [ν]; rw [← Finset.sum_div, div_self hZ_pos.ne']
  let goodSets : Finset (Finset (AddChar G ℂ)) :=
    Δ.powerset.filter fun Γ ↦ RieszGood ν Γ
  have hgood_ne : goodSets.Nonempty :=
    ⟨∅, Finset.mem_filter.mpr ⟨Finset.empty_mem_powerset Δ, rieszGood_empty hν_sum⟩⟩
  obtain ⟨Γ, hΓ_mem, hΓ_max⟩ := goodSets.exists_max_image Finset.card hgood_ne
  have hΓ_sub : Γ ⊆ Δ := Finset.mem_powerset.mp (Finset.mem_filter.mp hΓ_mem).1
  have hΓ_good : RieszGood ν Γ := (Finset.mem_filter.mp hΓ_mem).2
  have hΓ_card : (#Γ : ℝ) ≤ 16 * log (4 / η₀) :=
    card_le_of_rieszGood hreg hpos hT₀_ne hT₀_sub hη₀ hη_card hΓ_sub hΓ_good
  refine ⟨Γ, hΓ_sub, hΓ_card, fun ρ δ hρ₀ hδ₀ hρ_le hδ_le y hy ψ hψ ↦ ?_⟩
  let δ_nn : ℝ≥0 := ⟨δ, hδ₀.le⟩
  have hy_B₀ : y ∈ (ρ • B₀).finset :=
    BohrSet.finset_mono inf_le_left hy
  have hy_Γ : ∀ γ ∈ Γ, ‖1 - γ y‖ ≤ δ := by
    intro γ hγ
    have hy_inf : y ∈ (BohrSet.ofWidth (fun _ ↦ δ_nn) Γ).chordSet :=
      BohrSet.mem_finset.mp (BohrSet.finset_mono inf_le_right hy)
    have h1 := hy_inf γ
    change ‖1 - γ y‖₊ ≤ if γ ∈ Γ then (δ_nn : ℝ≥0∞) else ⊤ at h1
    rw [ite_eq_left hγ, ENNReal.coe_le_coe, ← NNReal.coe_le_coe] at h1
    exact h1
  by_cases hψΓ : ψ ∈ Γ
  · refine (hy_Γ ψ hψΓ).trans ?_
    have h1 : (1 : ℝ) ≤ 2 ^ 10 * (#Γ + 1 : ℝ) := by
      have : (0 : ℝ) ≤ #Γ := Nat.cast_nonneg _; linarith
    exact hδ_le.trans (div_le_self hε₀.le h1)
  · have hnot_good : ¬ RieszGood ν (insert ψ Γ) := by
      intro hgood_ins
      have hins_mem : insert ψ Γ ∈ goodSets :=
        Finset.mem_filter.mpr ⟨Finset.mem_powerset.mpr
          (Finset.insert_subset_iff.mpr ⟨hψ, hΓ_sub⟩), hgood_ins⟩
      have hle := hΓ_max (insert ψ Γ) hins_mem
      rw [Finset.card_insert_of_notMem hψΓ] at hle
      omega
    unfold RieszGood at hnot_good
    push Not at hnot_good
    obtain ⟨ω, hω_ins, hgt⟩ := hnot_good
    have hω_Γ : ∀ γ ∈ Γ, ‖ω γ‖ ≤ 2⁻¹ := fun γ hγ ↦ hω_ins γ (Finset.mem_insert_of_mem hγ)
    have hω_ψ : ‖ω ψ‖ ≤ 2⁻¹ := hω_ins ψ (Finset.mem_insert_self ψ Γ)
    let P : G → ℝ := rieszProd Γ ω
    let Z_P : ℝ := ∑ x : G, B₀.bohrWeight x * P x
    have hZ_P_pos : 0 < Z_P :=
      Finset.sum_pos (fun x _ ↦ mul_pos (B₀.bohrWeight_pos x) (rieszProd_pos_of_half hω_Γ x))
        ⟨0, Finset.mem_univ 0⟩
    have hsum_P_le : Z_P / Z ≤ exp ((#Γ : ℝ) / 32) := by
      have h1 := hΓ_good ω hω_Γ
      simpa [Z_P, ν, div_mul_eq_mul_div, ← Finset.sum_div] using h1
    have hsum_ins : ∑ x : G, ν x * rieszProd (insert ψ Γ) ω x =
        (Z_P / Z) + ((ω ψ * ∑ x : G, ((B₀.bohrWeight x * P x / Z : ℝ) : ℂ) * ψ x).re) := by
      have hprod_ins : ∀ x : G, rieszProd (insert ψ Γ) ω x = P x + P x * (ω ψ * ψ x).re := by
        intro x
        unfold rieszProd
        rw [Finset.prod_insert hψΓ]
        dsimp [P, rieszProd]
        ring
      simp_rw [hprod_ins, mul_add, Finset.sum_add_distrib]
      congr 1
      · dsimp [Z_P, ν]; simp_rw [div_mul_eq_mul_div, ← Finset.sum_div]
      · rw [Finset.mul_sum, Complex.re_sum]
        refine Finset.sum_congr rfl fun x _ ↦ ?_
        have hre1 : ν x * (P x * (ω ψ * ψ x).re) =
            ((B₀.bohrWeight x * P x / Z) * (ω ψ * ψ x).re) := by dsimp [ν]; ring
        rw [hre1, ← Complex.re_ofReal_mul]
        congr 1
        ring
    let μ_P : G → ℝ := fun x ↦ B₀.bohrWeight x * P x / Z_P
    have hcorr_ψ : (16⁻¹ : ℝ) < ‖∑ x : G, (μ_P x : ℂ) * ψ x‖ := by
      rw [Finset.card_insert_of_notMem hψΓ, Nat.cast_add, Nat.cast_one] at hgt
      have hratio : exp (32⁻¹ : ℝ) < 1 + ((ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x).re) := by
        have hdiv_pos : 0 < Z_P / Z := div_pos hZ_P_pos hZ_pos
        have hgt' : exp (((#Γ : ℝ) + 1) / 32) = exp ((#Γ : ℝ) / 32) * exp (32⁻¹ : ℝ) := by
          rw [← exp_add]; congr 1; ring
        rw [hgt', hsum_ins] at hgt
        have hmul_le : (Z_P / Z) * exp (32⁻¹ : ℝ) ≤ exp ((#Γ : ℝ) / 32) * exp (32⁻¹ : ℝ) :=
          mul_le_mul_of_nonneg_right hsum_P_le (exp_pos _).le
        have hlt2 : (Z_P / Z) * exp (32⁻¹ : ℝ) <
            (Z_P / Z) * (1 + (ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x).re) := by
          refine lt_of_le_of_lt hmul_le (hgt.trans_eq ?_)
          rw [mul_add, mul_one]
          congr 1
          rw [Finset.mul_sum, Finset.mul_sum, Complex.re_sum, Complex.re_sum, Finset.mul_sum]
          refine Finset.sum_congr rfl fun x _ ↦ ?_
          rw [← Complex.re_ofReal_mul]
          congr 1
          dsimp [μ_P]
          push_cast
          field_simp [hZ_pos.ne', hZ_P_pos.ne']
        exact lt_of_mul_lt_mul_left hlt2 hdiv_pos.le
      have hexp_ge : 1 + (32⁻¹ : ℝ) ≤ exp (32⁻¹ : ℝ) := by
        linarith [add_one_le_exp (32⁻¹ : ℝ)]
      have hre_gt : (32⁻¹ : ℝ) < (ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x).re := by linarith
      have hnorm_ge : (ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x).re ≤
          2⁻¹ * ‖∑ x : G, (μ_P x : ℂ) * ψ x‖ := by
        calc
          (ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x).re
            ≤ ‖ω ψ * ∑ x : G, (μ_P x : ℂ) * ψ x‖ := (le_abs_self _).trans (Complex.abs_re_le_norm _)
          _ = ‖ω ψ‖ * ‖∑ x : G, (μ_P x : ℂ) * ψ x‖ := norm_mul _ _
          _ ≤ 2⁻¹ * ‖∑ x : G, (μ_P x : ℂ) * ψ x‖ :=
            mul_le_mul_of_nonneg_right hω_ψ (norm_nonneg _)
      linarith
    have hshift_eq : (1 - ψ y) * ∑ x : G, (μ_P x : ℂ) * ψ x =
        ∑ u : G, ((μ_P u - μ_P (u - y) : ℝ) : ℂ) * ψ u := by
      rw [sub_mul, one_mul, Finset.mul_sum]
      have hsub_sum : ∑ x : G, ψ y * ((μ_P x : ℂ) * ψ x) =
          ∑ u : G, (μ_P (u - y) : ℂ) * ψ u := by
        refine Fintype.sum_equiv (Equiv.addRight y) _ _ fun x ↦ ?_
        simp only [Equiv.coe_addRight, add_sub_cancel_right, map_add_eq_mul]
        ring
      rw [hsub_sum, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl fun u _ ↦ ?_
      push_cast; ring
    have hP_ratio : ∀ (u v : G), (∀ γ ∈ Γ, ‖1 - γ (v - u)‖ ≤ δ) →
        P v ≤ exp ((#Γ : ℝ) * δ) * P u := by
      intro u v huv
      have hfac : ∀ γ ∈ Γ, 1 + (ω γ * γ v).re ≤ (1 + δ) * (1 + (ω γ * γ u).re) := by
        intro γ hγ
        have hge : 2⁻¹ ≤ 1 + (ω γ * γ u).re := rieszProd_factor_ge_half (hω_Γ γ hγ) γ u
        have hdiff : (ω γ * γ v).re - (ω γ * γ u).re ≤ 2⁻¹ * δ := by
          have hsub : ω γ * γ v - ω γ * γ u = ω γ * γ u * (γ (v - u) - 1) := by
            have : γ v = γ u * γ (v - u) := by rw [← map_add_eq_mul, add_sub_cancel]
            rw [this]; ring
          calc
            (ω γ * γ v).re - (ω γ * γ u).re = (ω γ * γ v - ω γ * γ u).re :=
              (Complex.sub_re _ _).symm
            _ ≤ ‖ω γ * γ v - ω γ * γ u‖ := (le_abs_self _).trans (Complex.abs_re_le_norm _)
            _ = ‖ω γ‖ * ‖γ u‖ * ‖1 - γ (v - u)‖ := by
                rw [hsub, norm_mul, norm_mul, norm_sub_rev]
            _ ≤ 2⁻¹ * 1 * δ := by
                rw [AddChar.norm_apply]
                exact mul_le_mul (by linarith [hω_Γ γ hγ]) (huv γ hγ) (norm_nonneg _)
                  (by norm_num)
            _ = 2⁻¹ * δ := by ring
        nlinarith
      calc
        P v = ∏ γ ∈ Γ, (1 + (ω γ * γ v).re) := rfl
        _ ≤ ∏ γ ∈ Γ, ((1 + δ) * (1 + (ω γ * γ u).re)) := by
          gcongr with γ hγ
          · intro i hi; linarith only [rieszProd_factor_ge_half (hω_Γ i hi) i v]
          · exact hfac γ hγ
        _ = (1 + δ) ^ #Γ * P u := by rw [Finset.prod_mul_distrib, Finset.prod_const]; rfl
        _ ≤ (exp δ) ^ #Γ * P u := by
          gcongr
          · exact (rieszProd_pos_of_half hω_Γ u).le
          · linarith [add_one_le_exp δ]
        _ = exp ((#Γ : ℝ) * δ) * P u := by rw [← exp_nat_mul]
    have hP_diff : ∀ u : G, |P (u - y) - P u| ≤
        (exp ((#Γ : ℝ) * δ) - 1) * (P u + P (u - y)) := by
      intro u
      have h1 : P (u - y) ≤ exp ((#Γ : ℝ) * δ) * P u := by
        refine hP_ratio u (u - y) fun γ hγ ↦ ?_
        have : u - y - u = -y := by abel
        rw [this, ← RCLike.norm_conj, map_sub, map_one, map_neg_eq_conj, RCLike.conj_conj]
        exact hy_Γ γ hγ
      have h2 : P u ≤ exp ((#Γ : ℝ) * δ) * P (u - y) := by
        refine hP_ratio (u - y) u fun γ hγ ↦ ?_
        have : u - (u - y) = y := by abel
        rw [this]
        exact hy_Γ γ hγ
      have hP1 : 0 ≤ P u := (rieszProd_pos_of_half hω_Γ u).le
      have hP2 : 0 ≤ P (u - y) := (rieszProd_pos_of_half hω_Γ (u - y)).le
      have hexp1 : 1 ≤ exp ((#Γ : ℝ) * δ) := one_le_exp (by positivity)
      rcases le_total (P u) (P (u - y)) with hle | hle
      · rw [abs_of_nonneg (sub_nonneg.mpr hle)]
        nlinarith
      · rw [abs_sub_comm, abs_of_nonneg (sub_nonneg.mpr hle)]
        nlinarith
    let α_w : ℝ := 1000 * (B₀.rank : ℝ) ^ 2 * ρ
    let α_P : ℝ := (#Γ : ℝ) * δ
    have hα_w_le : α_w ≤ ε_spec / 256 := by
      dsimp [α_w]
      have hd_le : (B₀.rank : ℝ) ^ 2 ≤ (B₀.rank + 1 : ℝ) ^ 2 := by gcongr; linarith
      have hpos_d : 0 < (B₀.rank + 1 : ℝ) ^ 2 := by positivity
      calc
        1000 * (B₀.rank : ℝ) ^ 2 * ρ
          ≤ 1000 * (B₀.rank + 1 : ℝ) ^ 2 * (ε_spec / (2 ^ 18 * (B₀.rank + 1 : ℝ) ^ 2)) := by
            gcongr
        _ = (1000 / 2 ^ 18) * ε_spec := by field_simp [hpos_d.ne']
        _ ≤ ε_spec / 256 := by linarith only [hε₀]
    have hα_P_le : α_P ≤ ε_spec / 1024 := by
      dsimp [α_P]
      have hr_le : (#Γ : ℝ) ≤ #Γ + 1 := by linarith
      have hpos_r : 0 < (#Γ + 1 : ℝ) := by positivity
      calc
        (#Γ : ℝ) * δ ≤ (#Γ + 1 : ℝ) * (ε_spec / (2 ^ 10 * (#Γ + 1 : ℝ))) := by gcongr
        _ = ε_spec / 1024 := by field_simp [hpos_r.ne']; norm_num
    have hexp_sub_le : ∀ {t : ℝ}, 0 ≤ t → t ≤ 2⁻¹ → exp t - 1 ≤ 2 * t := by
      intro t _ ht_half
      have hpos_1mt : 0 < 1 - t := by linarith
      have h1mt : 1 - t ≤ exp (-t) := by linarith [add_one_le_exp (-t)]
      have hexp_inv : exp t ≤ (1 - t)⁻¹ := by
        rw [← inv_inv (exp t), ← exp_neg]
        exact inv_anti₀ hpos_1mt h1mt
      have hinv_le : (1 - t)⁻¹ ≤ 1 + 2 * t := by
        rw [inv_le_iff_one_le_mul₀' hpos_1mt]
        nlinarith
      linarith
    have he_w : exp α_w - 1 ≤ ε_spec / 128 := by
      have hw_le_half : α_w ≤ 2⁻¹ := by linarith only [hα_w_le, hε₁]
      have hsub := hexp_sub_le (by dsimp [α_w]; positivity) hw_le_half
      linarith only [hsub, hα_w_le]
    have he_P : exp α_P - 1 ≤ ε_spec / 512 := by
      have hP_le_half : α_P ≤ 2⁻¹ := by linarith only [hα_P_le, hε₁]
      have hsub := hexp_sub_le (by dsimp [α_P]; positivity) hP_le_half
      linarith only [hsub, hα_P_le]
    have hL1_shift : ∑ u : G, |μ_P u - μ_P (u - y)| ≤ ε_spec / 16 := by
      have hpt_diff : ∀ u : G,
          |B₀.bohrWeight u * P u - B₀.bohrWeight (u - y) * P (u - y)| ≤
            (exp α_w - 1) * (B₀.bohrWeight u * P u) +
            (exp α_P - 1) * (exp α_w * (B₀.bohrWeight u * P u) +
              B₀.bohrWeight (u - y) * P (u - y)) := by
        intro u
        have hw_diff : |B₀.bohrWeight u - B₀.bohrWeight (u - y)| ≤
            (exp α_w - 1) * B₀.bohrWeight u := by
          rw [abs_sub_comm]
          exact BohrSet.abs_bohrWeight_sub_le hpos hρ₀.le hy_B₀ u
        have hw_mul : B₀.bohrWeight (u - y) ≤ exp α_w * B₀.bohrWeight u :=
          BohrSet.bohrWeight_sub_le_mul hpos hρ₀.le hy_B₀ u
        have hPu : 0 ≤ P u := (rieszProd_pos_of_half hω_Γ u).le
        have hPuy : 0 ≤ P (u - y) := (rieszProd_pos_of_half hω_Γ (u - y)).le
        have hw_nn : 0 ≤ B₀.bohrWeight (u - y) := (B₀.bohrWeight_pos _).le
        have hexpP_nn : 0 ≤ exp α_P - 1 := sub_nonneg.mpr (one_le_exp (by dsimp [α_P]; positivity))
        calc
          |B₀.bohrWeight u * P u - B₀.bohrWeight (u - y) * P (u - y)|
            = |(B₀.bohrWeight u - B₀.bohrWeight (u - y)) * P u +
                B₀.bohrWeight (u - y) * (P u - P (u - y))| := by ring_nf
          _ ≤ |(B₀.bohrWeight u - B₀.bohrWeight (u - y)) * P u| +
                |B₀.bohrWeight (u - y) * (P u - P (u - y))| := abs_add_le _ _
          _ = |B₀.bohrWeight u - B₀.bohrWeight (u - y)| * P u +
                B₀.bohrWeight (u - y) * |P (u - y) - P u| := by
                rw [abs_mul, abs_of_nonneg hPu, abs_mul, abs_of_nonneg hw_nn, abs_sub_comm (P u)]
          _ ≤ ((exp α_w - 1) * B₀.bohrWeight u) * P u +
                B₀.bohrWeight (u - y) * ((exp α_P - 1) * (P u + P (u - y))) :=
                add_le_add (mul_le_mul_of_nonneg_right hw_diff hPu)
                  (mul_le_mul_of_nonneg_left (hP_diff u) hw_nn)
          _ ≤ (exp α_w - 1) * (B₀.bohrWeight u * P u) +
                (exp α_P - 1) * (exp α_w * (B₀.bohrWeight u * P u) +
                  B₀.bohrWeight (u - y) * P (u - y)) := by
                have h1 : B₀.bohrWeight (u - y) * P u ≤ exp α_w * (B₀.bohrWeight u * P u) := by
                  rw [← mul_assoc]
                  exact mul_le_mul_of_nonneg_right hw_mul hPu
                have h1' : B₀.bohrWeight (u - y) * P u + B₀.bohrWeight (u - y) * P (u - y) ≤
                    exp α_w * (B₀.bohrWeight u * P u) + B₀.bohrWeight (u - y) * P (u - y) := by
                  linarith only [h1]
                have h2 : (exp α_P - 1) *
                    (B₀.bohrWeight (u - y) * P u + B₀.bohrWeight (u - y) * P (u - y)) ≤
                    (exp α_P - 1) *
                    (exp α_w * (B₀.bohrWeight u * P u) + B₀.bohrWeight (u - y) * P (u - y)) :=
                  mul_le_mul_of_nonneg_left h1' hexpP_nn
                linarith only [h2]
      have hsum_trans : ∑ u : G, B₀.bohrWeight (u - y) * P (u - y) = Z_P :=
        Fintype.sum_equiv (Equiv.subRight y) _ _ fun _ ↦ rfl
      have hsum_raw : ∑ u : G, |B₀.bohrWeight u * P u - B₀.bohrWeight (u - y) * P (u - y)| ≤
          ((exp α_w - 1) + (exp α_P - 1) * (exp α_w + 1)) * Z_P := by
        calc
          ∑ u : G, |B₀.bohrWeight u * P u - B₀.bohrWeight (u - y) * P (u - y)|
            ≤ ∑ u : G, ((exp α_w - 1) * (B₀.bohrWeight u * P u) +
                (exp α_P - 1) * (exp α_w * (B₀.bohrWeight u * P u) +
                  B₀.bohrWeight (u - y) * P (u - y))) := Finset.sum_le_sum fun u _ ↦ hpt_diff u
          _ = (exp α_w - 1) * Z_P + (exp α_P - 1) * (exp α_w * Z_P + Z_P) := by
                simp only [Finset.sum_add_distrib, ← Finset.mul_sum, hsum_trans]
                rfl
          _ = ((exp α_w - 1) + (exp α_P - 1) * (exp α_w + 1)) * Z_P := by ring
      have hrew_sum : ∑ u : G, |μ_P u - μ_P (u - y)| =
          (∑ u : G, |B₀.bohrWeight u * P u - B₀.bohrWeight (u - y) * P (u - y)|) / Z_P := by
        rw [Finset.sum_div]
        refine Finset.sum_congr rfl fun u _ ↦ ?_
        dsimp [μ_P]
        rw [← sub_div, abs_div, abs_of_pos hZ_P_pos]
      rw [hrew_sum, div_le_iff₀ hZ_P_pos]
      refine hsum_raw.trans (mul_le_mul_of_nonneg_right ?_ hZ_P_pos.le)
      have hexp_w_le2 : exp α_w + 1 ≤ 3 := by linarith only [he_w, hε₁]
      have hexpP_nn : 0 ≤ exp α_P - 1 := sub_nonneg.mpr (one_le_exp (by dsimp [α_P]; positivity))
      have hprod_3 : (exp α_P - 1) * (exp α_w + 1) ≤ (ε_spec / 512) * 3 :=
        mul_le_mul he_P hexp_w_le2 (by positivity) (by positivity)
      linarith only [he_w, hprod_3, hε₀]
    have hprod_norm : ‖1 - ψ y‖ * (16⁻¹ : ℝ) ≤ ∑ u : G, |μ_P u - μ_P (u - y)| := by
      calc
        ‖1 - ψ y‖ * (16⁻¹ : ℝ)
          ≤ ‖1 - ψ y‖ * ‖∑ x : G, (μ_P x : ℂ) * ψ x‖ :=
            mul_le_mul_of_nonneg_left hcorr_ψ.le (norm_nonneg _)
        _ = ‖(1 - ψ y) * ∑ x : G, (μ_P x : ℂ) * ψ x‖ := (norm_mul _ _).symm
        _ = ‖∑ u : G, ((μ_P u - μ_P (u - y) : ℝ) : ℂ) * ψ u‖ := by rw [hshift_eq]
        _ ≤ ∑ u : G, ‖((μ_P u - μ_P (u - y) : ℝ) : ℂ) * ψ u‖ := norm_sum_le _ _
        _ = ∑ u : G, |μ_P u - μ_P (u - y)| := by
            refine Finset.sum_congr rfl fun u _ ↦ ?_
            rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, AddChar.norm_apply, mul_one]
    have hfinal := hprod_norm.trans hL1_shift
    linarith only [hfinal]

end RelativeChang

section BohrAlmostPeriodicity
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

omit [AddCommGroup G] [Fintype G] [DecidableEq G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
private lemma th_ap_int_exp_factors {d rk₀ g_card : ℕ} (hrk₀ : rk₀ ≤ d)
    {α₁ α₂ ε : ℝ} (hα₁₀ : 0 < α₁) (hα₁₁ : α₁ ≤ 1) (hα₂₀ : 0 < α₂) (hα₂₁ : α₂ ≤ 1)
    (hε₀ : 0 < ε) (hε₁ : ε ≤ 1)
    (hg_upper : (g_card : ℝ) ≤ 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) :
    let ε_spec : ℝ := ε * α₁ / 16
    let ρ : ℝ := ε_spec / (2 ^ 18 * (rk₀ + 1 : ℝ) ^ 2)
    let δ : ℝ := ε_spec / (2 ^ 10 * (g_card + 1 : ℝ))
    exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε * α₁ / (d + 1 : ℝ)) +
      (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) * 𝓛 (ε * α₁ * α₂))) ≤
    (10⁻¹ : ℝ) ^ (d + g_card) * (δ / 18) ^ g_card * (ρ / 10) ^ d *
      ((1000 * (d + 1 : ℝ))⁻¹) ^ d := by
  intro ε_spec ρ δ
  have hLα₁ : 1 ≤ 𝓛 α₁ := one_le_curlog hα₁₀.le hα₁₁
  have hLα₂ : 1 ≤ 𝓛 α₂ := one_le_curlog hα₂₀.le hα₂₁
  have hεα₁_le1 : ε * α₁ ≤ 1 := (mul_le_of_le_one_right hε₀.le hα₁₁).trans hε₁
  have hα₁₂_le1 : α₁ * α₂ ≤ 1 := (mul_le_of_le_one_right hα₁₀.le hα₂₁).trans hα₁₁
  have hεα₁₂_le1 : ε * α₁ * α₂ ≤ 1 := by
    rw [mul_assoc]; exact (mul_le_of_le_one_right hε₀.le hα₁₂_le1).trans hε₁
  have hL1_ge1 : 1 ≤ 𝓛 (ε * α₁ / (d + 1 : ℝ)) :=
    one_le_curlog (by positivity)
      (div_le_one_of_le₀ (hεα₁_le1.trans (by linarith [Nat.cast_nonneg (α := ℝ) d]))
        (by positivity))
  have hL2_ge1 : 1 ≤ 𝓛 (ε * α₁ * α₂) := one_le_curlog (by positivity) hεα₁₂_le1
  have hρ_pos : 0 < ρ := by dsimp [ρ, ε_spec]; positivity
  have hδ_pos : 0 < δ := by dsimp [δ, ε_spec]; positivity
  have hsplit_pow :
      (10⁻¹ : ℝ) ^ (d + g_card) * (δ / 18) ^ g_card * (ρ / 10) ^ d * ((1000 * (d + 1 : ℝ))⁻¹) ^ d =
      ((ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d) * ((δ / 180) ^ g_card) := by
    rw [pow_add]
    have hd_ne : (d + 1 : ℝ) ≠ 0 := by positivity
    have h_d : (10⁻¹ : ℝ) ^ d * (ρ / 10) ^ d * ((1000 * (d + 1 : ℝ))⁻¹) ^ d =
        (ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d := by
      rw [← mul_pow, ← mul_pow]; congr 1; field_simp [hd_ne]; ring
    have h_g : (10⁻¹ : ℝ) ^ g_card * (δ / 18) ^ g_card = (δ / 180) ^ g_card := by
      rw [← mul_pow]; congr 1; ring
    calc
      (10⁻¹ : ℝ) ^ d * (10⁻¹ : ℝ) ^ g_card * (δ / 18) ^ g_card * (ρ / 10) ^ d *
          ((1000 * (d + 1 : ℝ))⁻¹) ^ d
        = ((10⁻¹ : ℝ) ^ d * (ρ / 10) ^ d * ((1000 * (d + 1 : ℝ))⁻¹) ^ d) *
            ((10⁻¹ : ℝ) ^ g_card * (δ / 18) ^ g_card) := by ring
      _ = ((ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d) * ((δ / 180) ^ g_card) := by rw [h_d, h_g]
  rw [hsplit_pow]
  let u₁ : ℝ := ε * α₁ / (d + 1 : ℝ)
  have hu₁_pos : 0 < u₁ := by dsimp [u₁]; positivity
  have hu₁_le1 : u₁ ≤ 1 := div_le_one_of_le₀
    (hεα₁_le1.trans (by linarith [Nat.cast_nonneg (α := ℝ) d])) (by positivity)
  have hd_term : exp (-2 ^ 7 * (d + 1 : ℝ) * 𝓛 u₁) ≤
      (ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d := by
    have hbase_ge : u₁ ^ 3 / 2 ^ 40 ≤ ρ / (10 ^ 5 * (d + 1 : ℝ)) := by
      dsimp [ρ, ε_spec, u₁]
      have hrk_le : (rk₀ + 1 : ℝ) ≤ d + 1 := by
        have : (rk₀ : ℝ) ≤ d := by exact_mod_cast hrk₀
        linarith
      have hden : 16 * (2 ^ 18 * (rk₀ + 1 : ℝ) ^ 2 * (10 ^ 5 * (d + 1 : ℝ))) ≤
          (d + 1 : ℝ) ^ 3 * 2 ^ 40 := by
        have h10 : (10 ^ 5 : ℝ) ≤ 2 ^ 18 := by norm_num
        have hsq : (rk₀ + 1 : ℝ) ^ 2 ≤ (d + 1 : ℝ) ^ 2 := by gcongr
        calc
          16 * (2 ^ 18 * (rk₀ + 1 : ℝ) ^ 2 * (10 ^ 5 * (d + 1 : ℝ)))
            ≤ 16 * (2 ^ 18 * (d + 1 : ℝ) ^ 2 * (2 ^ 18 * (d + 1 : ℝ))) := by gcongr
          _ = (d + 1 : ℝ) ^ 3 * 2 ^ 40 := by ring
      have hnum : (ε * α₁) ^ 3 ≤ ε * α₁ := by
        have hp2 : (ε * α₁) ^ 2 ≤ 1 := pow_le_one₀ (by positivity) hεα₁_le1
        calc
          (ε * α₁) ^ 3 = (ε * α₁) ^ 2 * (ε * α₁) := by ring
          _ ≤ 1 * (ε * α₁) := mul_le_mul_of_nonneg_right hp2 (by positivity)
          _ = ε * α₁ := one_mul _
      rw [div_pow, div_div, div_div, div_div]
      exact div_le_div₀ (by positivity) hnum (by positivity) hden
    have hexp_base : exp (-43 * 𝓛 u₁) ≤ u₁ ^ 3 / 2 ^ 40 := by
      rw [← exp_log (by positivity : 0 < u₁ ^ 3 / 2 ^ 40)]
      apply exp_le_exp.mpr
      have hlog_eq : log (u₁ ^ 3 / 2 ^ 40) = -3 * log u₁⁻¹ - 40 * log 2 := by
        rw [div_eq_mul_inv, log_mul (by positivity) (by positivity), log_pow, log_inv,
          log_pow, log_inv]
        ring
      rw [hlog_eq]
      have hlog2 : log 2 ≤ 1 := log_two_lt_d9.le.trans (by norm_num)
      have hlog_u1 : 0 ≤ log u₁⁻¹ := log_nonneg ((one_le_inv₀ hu₁_pos).mpr hu₁_le1)
      linarith only [hlog2, hlog_u1]
    calc
      exp (-2 ^ 7 * (d + 1 : ℝ) * 𝓛 u₁)
        ≤ exp (-(d : ℝ) * (43 * 𝓛 u₁)) := by
          apply exp_le_exp.mpr
          have hd_nn : 0 ≤ (d : ℝ) := Nat.cast_nonneg d
          nlinarith only [hd_nn, hL1_ge1]
      _ = (exp (-43 * 𝓛 u₁)) ^ d := by rw [← exp_nat_mul]; congr 1; ring
      _ ≤ (u₁ ^ 3 / 2 ^ 40) ^ d := pow_le_pow_left₀ (exp_pos _).le hexp_base d
      _ ≤ (ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d :=
          pow_le_pow_left₀ (by positivity) hbase_ge d
  let u₂ : ℝ := ε * α₁ * α₂
  have hu₂_pos : 0 < u₂ := by dsimp [u₂]; positivity
  let P_val : ℝ := 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4
  have hP_pos : 0 < P_val := by dsimp [P_val]; positivity
  have hg_P : (g_card : ℝ) ≤ 2 ^ 43 * P_val := by
    have hr : 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 = 2 ^ 43 * P_val := by dsimp [P_val]; ring
    linarith only [hg_upper, hr]
  have hΓ_term : exp (-2 ^ 52 * P_val * 𝓛 u₂) ≤ (δ / 180) ^ g_card := by
    have hΓ1_le : (g_card + 1 : ℝ) ≤ 2 ^ 44 * P_val := by
      have hone_le : 1 ≤ P_val := by
        dsimp [P_val]
        rw [le_div_iff₀ (by positivity)]
        have hε4 : ε ^ 4 ≤ 1 := pow_le_one₀ hε₀.le hε₁
        have hprod1 : 1 ≤ 𝓛 α₁ ^ 3 * 𝓛 α₂ :=
          one_le_mul_of_one_le_of_one_le (one_le_pow₀ hLα₁) hLα₂
        linarith only [hε4, hprod1]
      linarith only [hg_P, hone_le]
    have hδ_ge : u₂ / (2 ^ 67 * P_val) ≤ δ / 180 := by
      dsimp [δ, ε_spec, u₂]
      have hnum : ε * α₁ * α₂ ≤ ε * α₁ := mul_le_of_le_one_right (by positivity) hα₂₁
      have hden : 16 * (2 ^ 10 * (g_card + 1 : ℝ) * 180) ≤ 2 ^ 67 * P_val := by
        calc
          16 * (2 ^ 10 * (g_card + 1 : ℝ) * 180)
            ≤ 16 * (2 ^ 10 * (2 ^ 44 * P_val) * 256) := by gcongr; norm_num
          _ = 2 ^ 66 * P_val := by ring
          _ ≤ 2 ^ 67 * P_val := by linarith only [hP_pos]
      rw [div_div, div_div]
      exact div_le_div₀ (by positivity) hnum (by positivity) hden
    have hexp_δ : exp (-80 * 𝓛 u₂) ≤ u₂ / (2 ^ 67 * P_val) := by
      rw [← exp_log (by positivity : 0 < u₂ / (2 ^ 67 * P_val))]
      apply exp_le_exp.mpr
      have hu₂_le_α₁ : u₂ ≤ α₁ := by
        dsimp [u₂]
        rw [mul_right_comm]
        exact mul_le_of_le_one_left hα₁₀.le ((mul_le_of_le_one_right hε₀.le hα₂₁).trans hε₁)
      have hu₂_le_α₂ : u₂ ≤ α₂ := mul_le_of_le_one_left hα₂₀.le hεα₁_le1
      have hu₂_le_ε : u₂ ≤ ε := by
        dsimp [u₂]; rw [mul_assoc]; exact mul_le_of_le_one_right hε₀.le hα₁₂_le1
      have hlog_L1 : log (𝓛 α₁) ≤ 𝓛 u₂ :=
        (Real.log_le_self (by positivity)).trans (curlog_anti hu₂_pos hu₂_le_α₁)
      have hlog_L2 : log (𝓛 α₂) ≤ 𝓛 u₂ :=
        (Real.log_le_self (by positivity)).trans (curlog_anti hu₂_pos hu₂_le_α₂)
      have hlog_eps : log ε⁻¹ ≤ 𝓛 u₂ := by
        have h1 : 1 + log ε⁻¹ ≤ 𝓛 u₂ := curlog_anti hu₂_pos hu₂_le_ε
        linarith only [h1]
      have hlog2 : log 2 ≤ 1 := log_two_lt_d9.le.trans (by norm_num)
      have hlog_den : log (2 ^ 67 * P_val) ≤ 75 * 𝓛 u₂ := by
        dsimp [P_val]
        rw [log_mul (by positivity) (by positivity), log_div (by positivity) (by positivity),
          log_mul (by positivity) (by positivity), log_pow, log_pow, log_pow]
        have hinv_e : - (4 * log ε) = 4 * log ε⁻¹ := by rw [log_inv]; ring
        linarith only [hlog2, hlog_L1, hlog_L2, hlog_eps, hinv_e, hL2_ge1]
      have hlog_u2 : log u₂ = - log u₂⁻¹ := by rw [log_inv, neg_neg]
      rw [log_div hu₂_pos.ne' (by positivity), hlog_u2]
      dsimp [u₂] at hL2_ge1 ⊢
      linarith only [hlog_den, hL2_ge1]
    calc
      exp (-2 ^ 52 * P_val * 𝓛 u₂)
        ≤ exp (- (g_card : ℝ) * (80 * 𝓛 u₂)) := by
          apply exp_le_exp.mpr
          have h80 : 80 * (g_card : ℝ) ≤ 2 ^ 52 * P_val := by linarith only [hg_P, hP_pos]
          nlinarith only [h80, hL2_ge1]
      _ = (exp (-80 * 𝓛 u₂)) ^ g_card := by rw [← exp_nat_mul]; congr 1; ring
      _ ≤ (u₂ / (2 ^ 67 * P_val)) ^ g_card := pow_le_pow_left₀ (exp_pos _).le hexp_δ g_card
      _ ≤ (δ / 180) ^ g_card := pow_le_pow_left₀ (by positivity) hδ_ge g_card
  calc
    exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 u₁ + P_val * 𝓛 u₂))
      ≤ exp (-2 ^ 7 * (d + 1 : ℝ) * 𝓛 u₁ + (-2 ^ 52 * P_val * 𝓛 u₂)) := by
        apply exp_le_exp.mpr
        have hp1 : 0 ≤ (d + 1 : ℝ) * 𝓛 u₁ := by positivity
        have hp2 : 0 ≤ P_val * 𝓛 u₂ := by positivity
        linarith only [hp1, hp2]
    _ = exp (-2 ^ 7 * (d + 1 : ℝ) * 𝓛 u₁) * exp (-2 ^ 52 * P_val * 𝓛 u₂) := exp_add _ _
    _ ≤ ((ρ / (10 ^ 5 * (d + 1 : ℝ))) ^ d) * ((δ / 180) ^ g_card) :=
        mul_le_mul hd_term hΓ_term (exp_pos _).le (by positivity)

private lemma th_ap_int_fourier_err {B B'' : BohrSet G}
    {A₁ A₂ S T₀ : Finset G} {x₀ s₀ : G} {α₁ ε : ℝ} {k : ℕ}
    (hα₁₀ : 0 < α₁) (hα₁₁ : α₁ ≤ 1) (hε₀ : 0 < ε)
    (hA₁_ne : A₁.Nonempty) (hA₂_ne : A₂.Nonempty)
    (hT₀_ne : T₀.Nonempty)
    (hA₁_card : α₁ * #B.finset ≤ #A₁)
    (hS_card : #S ≤ 2 * #B.finset)
    (hk_pow_le : (2⁻¹ : ℝ) ^ k ≤ ε * α₁ / 32)
    (hT_err : ‖μ ((-s₀) +ᵥ T₀) ∗ᵈ^ k ∗ᵈ
        (μ_[ℂ] (-((-x₀) +ᵥ A₂)) ∗ᵈ 𝟭_[(-(x₀ +ᵥ S) : Finset G)] ∗ᵈ μ A₁) -
        (μ_[ℂ] (-((-x₀) +ᵥ A₂)) ∗ᵈ 𝟭_[(-(x₀ +ᵥ S) : Finset G)] ∗ᵈ μ A₁)‖_[∞] ≤ 3 * ε / 8)
    (hv_spec₀ : ∀ v ∈ B''.finset, ∀ ψ ∈ largeSpec (μ_[ℂ] T₀) 2⁻¹, ‖1 - ψ v‖ ≤ ε * α₁ / 16) :
    |∑ y ∈ S, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y - ∑ y ∈ S, (μ A₁ ○ᵈ μ A₂) y| ≤ ε := by
  let A₂' : Finset G := (-x₀) +ᵥ A₂
  let A : Finset G := -A₂'
  let S' : Finset G := x₀ +ᵥ S
  have hA_ne : A.Nonempty := by simpa [A, A₂'] using hA₂_ne
  have hS'_card : #S' ≤ 2 * #B.finset := by simpa [S', Finset.card_vadd_finset] using hS_card
  let T : Finset G := (-s₀) +ᵥ T₀
  have hT_ne : T.Nonempty := hT₀_ne.vadd_finset
  let F : G → ℂ := μ_[ℂ] A ∗ᵈ 𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁
  let ε_spec : ℝ := ε * α₁ / 16
  have hspec_eq : largeSpec (μ_[ℂ] T) 2⁻¹ = largeSpec (μ_[ℂ] T₀) 2⁻¹ := by
    ext ψ
    simp only [mem_largeSpec, dL1Norm_mu hT_ne, dL1Norm_mu hT₀_ne]
    have hdft_trans : ‖dft (μ_[ℂ] T) ψ‖ = ‖dft (μ_[ℂ] T₀) ψ‖ := by
      have hmu_tr : μ_[ℂ] T = τ (-s₀) (μ T₀) := (translate_mu ℂ (-s₀) T₀).symm
      have hdft_tr : dft (τ (-s₀) (μ_[ℂ] T₀)) ψ = conj (ψ (-s₀)) * dft (μ T₀) ψ := by
        simp only [dft_apply, wInner_one_eq_sum, RCLike.inner_apply, translate_apply,
          Finset.mul_sum]
        refine Fintype.sum_equiv (Equiv.subRight (-s₀)) _ _ fun x ↦ ?_
        have hx : -s₀ + (x - -s₀) = x := by abel
        have hψx : ψ x = ψ (-s₀) * ψ (x - -s₀) := by rw [← map_add_eq_mul, hx]
        simp only [Equiv.subRight_apply, hψx, map_mul]
        ring
      rw [hmu_tr, hdft_tr, norm_mul, RCLike.norm_conj, AddChar.norm_apply, one_mul]
    rw [hdft_trans]
  have hdft_F_L1 : ‖dft F‖ₙ_[1] ≤ 2 / α₁ := by
    have h1 : ‖dft F‖ₙ_[1] ≤ ‖dft (𝟭_[((-S' : Finset G) : Set G), ℂ] ∗ᵈ μ A₁)‖ₙ_[1] := by
      have hcomm : F = μ_[ℂ] A ∗ᵈ (𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁) := by
        dsimp [F]; rw [ddconv_assoc]
      rw [hcomm, dft_ddconv]
      calc
        ‖dft (μ_[ℂ] A) * dft (𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁)‖ₙ_[1]
          ≤ ‖dft (μ_[ℂ] A)‖ₙ_[∞] * ‖dft (𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁)‖ₙ_[1] := cL1Norm_mul_le ∞ 1
        _ ≤ 1 * ‖dft (𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁)‖ₙ_[1] := by
            gcongr
            exact (cLinftyNorm_dft_le_dL1Norm _).trans_eq (dL1Norm_mu hA_ne)
        _ = ‖dft (𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁)‖ₙ_[1] := one_mul _
    have h2 : ‖dft (𝟭_[((-S' : Finset G) : Set G), ℂ] ∗ᵈ μ A₁)‖ₙ_[1] ≤ sqrt ((#S' : ℝ) / #A₁) := by
      rw [dft_ddconv]
      calc
        ‖dft 𝟭_[((-S' : Finset G) : Set G), ℂ] * dft (μ A₁)‖ₙ_[1]
          ≤ ‖dft 𝟭_[((-S' : Finset G) : Set G), ℂ]‖ₙ_[2] * ‖dft (μ A₁)‖ₙ_[2] := cL1Norm_mul_le 2 2
        _ = ‖𝟭_[((-S' : Finset G) : Set G), ℂ]‖_[2] * ‖μ_[ℂ] A₁‖_[2] := by
            rw [cL2Norm_dft, cL2Norm_dft]
        _ = sqrt (#S' : ℝ) * (sqrt (#A₁ : ℝ))⁻¹ := by
            have hind : ‖𝟭_[((-S' : Finset G) : Set G), ℂ]‖_[2] = sqrt (#S' : ℝ) := by
              rw [dL2Norm_indicator_one, Finset.card_neg, Real.sqrt_eq_rpow]
            have hmu2 : ‖μ_[ℂ] A₁‖_[2] = (sqrt (#A₁ : ℝ))⁻¹ := by
              rw [dL2Norm_mu hA₁_ne, Real.sqrt_eq_rpow, ← Real.rpow_neg (by positivity)]
              norm_num
            rw [hind, hmu2]
        _ = sqrt ((#S' : ℝ) / #A₁) := by
            rw [div_eq_mul_inv, Real.sqrt_mul (by positivity), Real.sqrt_inv]
    have hratio : (#S' : ℝ) / #A₁ ≤ 4 / α₁ ^ 2 := by
      have hS'_le : (#S' : ℝ) ≤ 2 * #B.finset := by exact_mod_cast hS'_card
      have h2_le : 2 / α₁ ≤ 4 / α₁ ^ 2 := by
        rw [div_le_div_iff₀ hα₁₀ (by positivity)]
        nlinarith only [hα₁₀, hα₁₁]
      have h_div1 : (#S' : ℝ) / #A₁ ≤ 2 / α₁ := by
        rw [div_le_div_iff₀ (Nat.cast_pos.mpr hA₁_ne.card_pos) hα₁₀]
        nlinarith only [hS'_le, hA₁_card, hα₁₀]
      exact h_div1.trans h2_le
    calc
      ‖dft F‖ₙ_[1] ≤ sqrt ((#S' : ℝ) / #A₁) := h1.trans h2
      _ ≤ sqrt (4 / α₁ ^ 2) := Real.sqrt_le_sqrt hratio
      _ = 2 / α₁ := by
          have hsqrt4 : sqrt (4 : ℝ) = 2 := by
            rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
          rw [Real.sqrt_div (by norm_num), Real.sqrt_sq hα₁₀.le, hsqrt4]
  let G_sm : G → ℂ := μ T ∗ᵈ^ k ∗ᵈ F
  have hFv_sub_F0 : ∀ v ∈ B''.finset, ‖F v - F 0‖ ≤ ε := by
    intro v hv
    have hv_spec : ∀ ψ ∈ largeSpec (μ_[ℂ] T) 2⁻¹, ‖1 - ψ v‖ ≤ ε_spec := by
      intro ψ hψ
      rw [hspec_eq] at hψ
      exact hv_spec₀ v hv ψ hψ
    have hGsm_diff : ‖G_sm v - G_sm 0‖ ≤ ε / 4 := by
      have hinv_diff : G_sm v - G_sm 0 =
          𝔼 ψ : AddChar G ℂ, dft (μ T) ψ ^ k * dft F ψ * (ψ v - 1) := by
        rw [← dft_inversion G_sm v, ← dft_inversion G_sm 0, ← Finset.expect_sub_distrib]
        refine Finset.expect_congr rfl fun ψ _ ↦ ?_
        simp only [G_sm, dft_ddconv_apply, dft_iterConv_apply, map_zero_eq_one]
        ring
      rw [hinv_diff]
      have hpt_ψ : ∀ ψ : AddChar G ℂ,
          ‖dft (μ T) ψ ^ k * dft F ψ * (ψ v - 1)‖ ≤
            (ε_spec + 2 * (2⁻¹ : ℝ) ^ k) * ‖dft F ψ‖ := by
        intro ψ
        rw [norm_mul, norm_mul, norm_pow, norm_sub_rev]
        by_cases hψ : ψ ∈ largeSpec (μ_[ℂ] T) 2⁻¹
        · have hdft_le1 : ‖dft (μ_[ℂ] T) ψ‖ ^ k ≤ 1 :=
            pow_le_one₀ (norm_nonneg _) ((norm_dft_le_dL1Norm _ _).trans_eq (dL1Norm_mu hT_ne))
          have hv_le : ‖1 - ψ v‖ ≤ ε_spec := hv_spec ψ hψ
          have h1 : ‖dft (μ_[ℂ] T) ψ‖ ^ k * ‖dft F ψ‖ * ‖1 - ψ v‖ ≤
              1 * ‖dft F ψ‖ * ε_spec :=
            mul_le_mul (mul_le_mul_of_nonneg_right hdft_le1 (norm_nonneg _))
              hv_le (norm_nonneg _) (by positivity)
          have hnn : 0 ≤ 2 * (2⁻¹ : ℝ) ^ k * ‖dft F ψ‖ := by positivity
          linarith only [h1, hnn]
        · have hdft_lt : ‖dft (μ_[ℂ] T) ψ‖ < 2⁻¹ := by
            simpa [mem_largeSpec, dL1Norm_mu hT_ne, mul_one] using hψ
          have hdft_pow : ‖dft (μ_[ℂ] T) ψ‖ ^ k ≤ (2⁻¹ : ℝ) ^ k :=
            pow_le_pow_left₀ (norm_nonneg _) hdft_lt.le k
          have hv_2 : ‖1 - ψ v‖ ≤ 2 := by
            calc
              ‖1 - ψ v‖ ≤ ‖(1 : ℂ)‖ + ‖ψ v‖ := norm_sub_le _ _
              _ = 2 := by rw [norm_one, AddChar.norm_apply]; norm_num
          have h1 : ‖dft (μ_[ℂ] T) ψ‖ ^ k * ‖dft F ψ‖ * ‖1 - ψ v‖ ≤
              (2⁻¹ : ℝ) ^ k * ‖dft F ψ‖ * 2 :=
            mul_le_mul (mul_le_mul_of_nonneg_right hdft_pow (norm_nonneg _))
              hv_2 (norm_nonneg _) (by positivity)
          have hnn : 0 ≤ ε_spec * ‖dft F ψ‖ := by dsimp [ε_spec]; positivity
          linarith only [h1, hnn]
      calc
        ‖𝔼 ψ : AddChar G ℂ, dft (μ T) ψ ^ k * dft F ψ * (ψ v - 1)‖
          ≤ 𝔼 ψ : AddChar G ℂ, ‖dft (μ T) ψ ^ k * dft F ψ * (ψ v - 1)‖ :=
            norm_expect_le (K := ℝ)
        _ ≤ 𝔼 ψ : AddChar G ℂ, (ε_spec + 2 * (2⁻¹ : ℝ) ^ k) * ‖dft F ψ‖ :=
            Finset.expect_le_expect fun ψ _ ↦ hpt_ψ ψ
        _ = (ε_spec + 2 * (2⁻¹ : ℝ) ^ k) * ‖dft F‖ₙ_[1] := by
            rw [cL1Norm_eq_expect_norm, Finset.mul_expect]
        _ ≤ (ε * α₁ / 16 + 2 * (ε * α₁ / 32)) * (2 / α₁) :=
            mul_le_mul (by dsimp [ε_spec]; linarith only [hk_pow_le]) hdft_F_L1
              (by positivity) (by positivity)
        _ = ε / 4 := by field_simp [hα₁₀.ne']; ring
    have herr_v : ‖G_sm v - F v‖ ≤ 3 * ε / 8 :=
      (norm_le_dLinftyNorm (f := G_sm - F)).trans hT_err
    have herr_0 : ‖G_sm 0 - F 0‖ ≤ 3 * ε / 8 :=
      (norm_le_dLinftyNorm (f := G_sm - F)).trans hT_err
    calc
      ‖F v - F 0‖
        = ‖(F v - G_sm v) + (G_sm v - G_sm 0) + (G_sm 0 - F 0)‖ := by congr 1; ring
      _ ≤ ‖F v - G_sm v‖ + ‖G_sm v - G_sm 0‖ + ‖G_sm 0 - F 0‖ := by
          have hn1 := norm_add_le (F v - G_sm v + (G_sm v - G_sm 0)) (G_sm 0 - F 0)
          have hn2 := norm_add_le (F v - G_sm v) (G_sm v - G_sm 0)
          linarith only [hn1, hn2]
      _ = ‖G_sm v - F v‖ + ‖G_sm v - G_sm 0‖ + ‖G_sm 0 - F 0‖ := by rw [norm_sub_rev]
      _ ≤ 3 * ε / 8 + ε / 4 + 3 * ε / 8 := by linarith only [herr_v, hGsm_diff, herr_0]
      _ = ε := by ring
  let H_real : G → ℝ := μ_[ℝ] A₁ ○ᵈ μ A₂' ○ᵈ 𝟭_[S']
  have hF_eq_H : ∀ x : G, F x = (H_real x : ℂ) := by
    intro x
    have hH : H_real = μ_[ℝ] A ∗ᵈ 𝟭_[(-S' : Finset G)] ∗ᵈ μ A₁ := by
      dsimp [H_real, A]
      rw [dddconv_indicator_one, ← Finset.coe_neg S', ← ddconv_conjneg (μ_[ℝ] A₁), conjneg_mu]
      rw [ddconv_comm (μ_[ℝ] A₁), ddconv_assoc,
        ddconv_comm (μ_[ℝ] A₁) 𝟭_[((-S' : Finset G) : Set G), ℝ], ← ddconv_assoc]
    rw [hH, Complex.ofReal_ddconv, Complex.ofReal_comp_mu]
    have hc1 : Complex.ofReal ∘ (μ_[ℝ] A ∗ᵈ 𝟭_[(-S' : Finset G), ℝ]) =
        μ_[ℂ] A ∗ᵈ 𝟭_[(-S' : Finset G), ℂ] := by
      ext y
      change (((μ_[ℝ] A ∗ᵈ 𝟭_[(-S' : Finset G), ℝ]) y : ℝ) : ℂ) = _
      rw [Complex.ofReal_ddconv, Complex.ofReal_comp_mu, Complex.ofReal_comp_indicator_one]
    rw [hc1]
  have hH_zero : ∑ y ∈ S, (μ_[ℝ] A₁ ○ᵈ μ A₂) y = H_real 0 := by
    have htr : ∀ y : G, (μ_[ℝ] A₁ ○ᵈ μ A₂) y = (μ_[ℝ] A₁ ○ᵈ μ A₂') (y + x₀) := by
      intro y
      have hA₂_eq : A₂ = x₀ +ᵥ A₂' := by simp [A₂']
      have hmu_eq : μ_[ℝ] A₂ = τ x₀ (μ A₂') := by rw [hA₂_eq, translate_mu]
      rw [hmu_eq, dddconv_translate, translate_apply, sub_neg_eq_add]
    have hsum_S' : ∑ y ∈ S, (μ_[ℝ] A₁ ○ᵈ μ A₂) y = ∑ z ∈ S', (μ_[ℝ] A₁ ○ᵈ μ A₂') z := by
      simp_rw [htr]
      refine Finset.sum_bij (fun y _ ↦ x₀ + y) (fun y hy ↦ Finset.mem_vadd_finset.mpr ⟨y, hy, rfl⟩)
        (fun _ _ _ _ h ↦ add_left_cancel h) (fun z hz ↦ ?_) (fun y _ ↦ by rw [add_comm])
      rcases Finset.mem_vadd_finset.mp hz with ⟨y, hy, rfl⟩
      exact ⟨y, hy, rfl⟩
    rw [hsum_S']
    simp [H_real, dddconv_indicator_one_eq_sum]
  have hH_avg' : ∑ y ∈ S, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y =
      𝔼 v ∈ B''.finset, H_real (-v) := by
    have htr : ∀ y : G, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y =
        (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂')) (y + x₀) := by
      intro y
      have hA₂_eq : A₂ = x₀ +ᵥ A₂' := by simp [A₂']
      have hmu_eq : μ_[ℝ] A₂ = τ x₀ (μ A₂') := by rw [hA₂_eq, translate_mu]
      rw [hmu_eq, dddconv_translate, ddconv_translate, translate_apply, sub_neg_eq_add]
    have hsum_S' : ∑ y ∈ S, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y =
        ∑ z ∈ S', (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂')) z := by
      simp_rw [htr]
      refine Finset.sum_bij (fun y _ ↦ x₀ + y) (fun y hy ↦ Finset.mem_vadd_finset.mpr ⟨y, hy, rfl⟩)
        (fun _ _ _ _ h ↦ add_left_cancel h) (fun z hz ↦ ?_) (fun y _ ↦ by rw [add_comm])
      rcases Finset.mem_vadd_finset.mp hz with ⟨y, hy, rfl⟩
      exact ⟨y, hy, rfl⟩
    have hconv_mu : ∀ z : G, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂')) z =
        (#B''.finset : ℝ)⁻¹ * ∑ v ∈ B''.finset, (μ_[ℝ] A₁ ○ᵈ μ A₂') (z - v) := fun z ↦ by
      rw [ddconv_eq_sum_sub']
      simp only [mu_apply, mul_ite, mul_one, mul_zero, ite_mul, zero_mul]
      rw [← Finset.sum_filter, Finset.filter_mem_eq_inter, Finset.univ_inter, ← Finset.mul_sum]
    have hH_val : ∀ v : G, H_real (-v) = ∑ z ∈ S', (μ_[ℝ] A₁ ○ᵈ μ A₂') (z - v) := fun v ↦ by
      simp only [H_real, dddconv_indicator_one_eq_sum, Finset.sum_apply, translate_apply]
      refine Finset.sum_congr rfl fun z _ ↦ ?_
      have : -v - -z = z - v := by abel
      rw [this]
    rw [hsum_S', Finset.expect_eq_sum_div_card, div_eq_inv_mul]
    calc
      ∑ z ∈ S', (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂')) z
        = ∑ z ∈ S', ((#B''.finset : ℝ)⁻¹ * ∑ v ∈ B''.finset, (μ_[ℝ] A₁ ○ᵈ μ A₂') (z - v)) :=
          Finset.sum_congr rfl fun z _ ↦ hconv_mu z
      _ = (#B''.finset : ℝ)⁻¹ * ∑ z ∈ S', ∑ v ∈ B''.finset, (μ_[ℝ] A₁ ○ᵈ μ A₂') (z - v) := by
          rw [← Finset.mul_sum]
      _ = (#B''.finset : ℝ)⁻¹ * ∑ v ∈ B''.finset, ∑ z ∈ S', (μ_[ℝ] A₁ ○ᵈ μ A₂') (z - v) := by
          rw [Finset.sum_comm]
      _ = ((#B''.finset : ℚ≥0) : ℝ)⁻¹ * ∑ v ∈ B''.finset, H_real (-v) := by
          push_cast
          congr 1
          exact Finset.sum_congr rfl fun v _ ↦ (hH_val v).symm
  rw [hH_avg', hH_zero, ← Finset.expect_const B''.finset_nonempty (H_real 0),
    ← Finset.expect_sub_distrib]
  calc
    |𝔼 v ∈ B''.finset, (H_real (-v) - H_real 0)|
      ≤ 𝔼 v ∈ B''.finset, |H_real (-v) - H_real 0| := by
        simpa [Real.norm_eq_abs] using
          (norm_expect_le (K := ℝ) (s := B''.finset) (f := fun v ↦ H_real (-v) - H_real 0))
    _ ≤ 𝔼 _v ∈ B''.finset, ε := by
        refine Finset.expect_le_expect fun v hv ↦ ?_
        have hnv : -v ∈ B''.finset := BohrSet.neg_mem_finset.mpr hv
        have h1 := hFv_sub_F0 (-v) hnv
        rw [hF_eq_H (-v), hF_eq_H 0, ← Complex.ofReal_sub, Complex.norm_real,
          Real.norm_eq_abs] at h1
        exact h1
    _ = ε := Finset.expect_const B''.finset_nonempty ε

/-- Bohr-set almost-periodicity theorem (`th-ap-int` in the blueprint). -/
theorem th_ap_int {B B' : BohrSet G} (hB'_reg : B'.IsRegular)
    (hB'_pos : B'.PosWidth) {d : ℕ} (hB'_rk : B'.rank ≤ d)
    {A₁ A₂ S : Finset G} {x₀ : G} {α₁ α₂ ε : ℝ}
    (hα₁₀ : 0 < α₁) (hα₁₁ : α₁ ≤ 1) (hα₂₀ : 0 < α₂) (hα₂₁ : α₂ ≤ 1)
    (hε₀ : 0 < ε) (hε₁ : ε ≤ 1)
    (hA₁_card : α₁ * #B.finset ≤ #A₁)
    (hA₂_sub : (-x₀) +ᵥ A₂ ⊆ B'.finset) (hA₂_card : α₂ * #B'.finset ≤ #A₂)
    (hS_card : #S ≤ 2 * #B.finset) :
    ∃ B'' : BohrSet G,
      B''.finset ⊆ B'.finset ∧
      B''.IsRegular ∧
      B''.PosWidth ∧
      (B''.rank : ℝ) ≤ d + 2 ^ 44 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 ∧
      exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε * α₁ / (d + 1 : ℝ)) +
        (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) * 𝓛 (ε * α₁ * α₂))) * #B'.finset ≤ #B''.finset ∧
      |∑ y ∈ S, (μ_[ℝ] B''.finset ∗ᵈ (μ A₁ ○ᵈ μ A₂)) y - ∑ y ∈ S, (μ A₁ ○ᵈ μ A₂) y| ≤ ε := by
  have hLα₁ : 1 ≤ 𝓛 α₁ := one_le_curlog hα₁₀.le hα₁₁
  have hLα₂ : 1 ≤ 𝓛 α₂ := one_le_curlog hα₂₀.le hα₂₁
  have hεα₁_le1 : ε * α₁ ≤ 1 := (mul_le_of_le_one_right hε₀.le hα₁₁).trans hε₁
  have hL1_ge1 : 1 ≤ 𝓛 (ε * α₁ / (d + 1 : ℝ)) :=
    one_le_curlog (by positivity)
      (div_le_one_of_le₀ (hεα₁_le1.trans (by linarith [Nat.cast_nonneg (α := ℝ) d]))
        (by positivity))
  have hα₁₂_le1 : α₁ * α₂ ≤ 1 := (mul_le_of_le_one_right hα₁₀.le hα₂₁).trans hα₁₁
  have hεα₁₂_le1 : ε * α₁ * α₂ ≤ 1 := by
    rw [mul_assoc]; exact (mul_le_of_le_one_right hε₀.le hα₁₂_le1).trans hε₁
  have hL2_ge1 : 1 ≤ 𝓛 (ε * α₁ * α₂) :=
    one_le_curlog (by positivity) hεα₁₂_le1
  rcases S.eq_empty_or_nonempty with rfl | hS_ne
  · refine ⟨B', Subset.rfl, hB'_reg, hB'_pos, ?_, ?_, by simp [hε₀.le]⟩
    · have : 0 ≤ 2 ^ 44 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by positivity
      have hd_le : (B'.rank : ℝ) ≤ d := by exact_mod_cast hB'_rk
      linarith
    · have hexp_le1 : exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε * α₁ / (d + 1 : ℝ)) +
          (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) * 𝓛 (ε * α₁ * α₂))) ≤ 1 := by
        apply exp_le_one_iff.mpr
        have hpos : 0 ≤ 2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε * α₁ / (d + 1 : ℝ)) +
          (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) * 𝓛 (ε * α₁ * α₂)) := by positivity
        linarith
      exact mul_le_of_le_one_left (Nat.cast_nonneg _) hexp_le1
  have hB_pos_card : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
  have hB'_pos_card : (0 : ℝ) < #B'.finset := by exact_mod_cast B'.card_finset_pos
  have hA₁_ne : A₁.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]; exact (mul_pos hα₁₀ hB_pos_card).trans_le hA₁_card
  have hA₂_ne : A₂.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]; exact (mul_pos hα₂₀ hB'_pos_card).trans_le hA₂_card
  let A₂' : Finset G := (-x₀) +ᵥ A₂
  let A : Finset G := -A₂'
  let S' : Finset G := x₀ +ᵥ S
  have hA_sub : A ⊆ B'.finset := by
    intro y hy
    rcases Finset.mem_neg.mp hy with ⟨z, hz, rfl⟩
    exact BohrSet.neg_mem_finset.mpr (hA₂_sub hz)
  have hA_card : α₂ * #B'.finset ≤ #A := by
    simpa [A, A₂', Finset.card_neg, Finset.card_vadd_finset] using hA₂_card
  have hA_ne : A.Nonempty := by simpa [A, A₂'] using hA₂_ne
  have hS'_ne : S'.Nonempty := by simpa [S'] using hS_ne
  have hS'_card : #S' ≤ 2 * #B.finset := by simpa [S', Finset.card_vadd_finset] using hS_card
  -- Step 1: Regular `B₀ ⊆ (100 * (d + 1))⁻¹ • B'`
  let κ_step : ℝ := (100 * (d + 1 : ℝ))⁻¹
  have hκ_step_pos : 0 < κ_step := by positivity
  have hκ_step_le1 : κ_step ≤ 1 :=
    inv_le_one_of_one_le₀ (by linarith [Nat.cast_nonneg (α := ℝ) d])
  obtain ⟨ρ₀, hρ₀_lo, hρ₀_hi, hB₀_reg⟩ := BohrSet.regularity (κ_step • B')
  let B₀ : BohrSet G := ρ₀ • (κ_step • B')
  have hB₀_eq : B₀ = (ρ₀ * κ_step) • B' := (mul_smul ρ₀ κ_step B').symm
  have hρ₀_pos : 0 < ρ₀ := by linarith
  have hB₀_pos : B₀.PosWidth := (hB'_pos.smul hκ_step_pos.ne').smul hρ₀_pos.ne'
  have hB₀_rk : B₀.rank ≤ d := by simpa [B₀] using hB'_rk
  have hB₀_sub_step : B₀.finset ⊆ (κ_step • B').finset := by
    rw [hB₀_eq]
    exact BohrSet.smul_finset_mono (by positivity) (mul_le_of_le_one_left hκ_step_pos.le hρ₀_hi)
  have hB₀_sub_B' : B₀.finset ⊆ B'.finset :=
    hB₀_sub_step.trans
      (by simpa [one_smul] using BohrSet.smul_finset_mono hκ_step_pos.le hκ_step_le1)
  -- Doubling bound `σ[A, B₀.finset] ≤ 2 / α₂`
  let K : ℝ := 2 / α₂
  have hK₂ : 2 ≤ K := (le_div_iff₀ hα₂₀).mpr (by linarith)
  have hσ_A : (σ[A, B₀.finset] : ℝ) ≤ K := by
    have hmul_le : (#(A + B₀.finset) : ℝ) ≤ K * #A := by
      have hsum_sub : A + B₀.finset ⊆ ((1 + κ_step) • B').finset := by
        have h1 : A + B₀.finset ⊆ ((1 : ℝ) • B').finset + (κ_step • B').finset := by
          rw [one_smul]
          exact Finset.add_subset_add hA_sub hB₀_sub_step
        exact h1.trans (BohrSet.smul_add_smul_finset_subset zero_le_one hκ_step_pos.le)
      have h100_le : 100 * (B'.rank : ℝ) * κ_step ≤ 1 := by
        have hrk : (B'.rank : ℝ) ≤ d := by exact_mod_cast hB'_rk
        dsimp [κ_step]
        rw [mul_inv_le_iff₀ (by positivity)]
        linarith
      calc
        (#(A + B₀.finset) : ℝ) ≤ #((1 + κ_step) • B').finset := by gcongr
        _ ≤ (1 + 100 * B'.rank * κ_step) * #B'.finset :=
            hB'_reg.card_one_add_smul_le hκ_step_pos.le h100_le
        _ ≤ 2 * #B'.finset :=
            mul_le_mul_of_nonneg_right (by linarith only [h100_le]) (Nat.cast_nonneg _)
        _ = K * (α₂ * #B'.finset) := by dsimp [K]; field_simp [hα₂₀.ne']
        _ ≤ K * #A := mul_le_mul_of_nonneg_left hA_card (by positivity)
    rw [← Finset.cast_addConst_mul_card] at hmul_le
    exact le_of_mul_le_mul_right hmul_le (by exact_mod_cast hA_ne.card_pos)
  -- Step 2: Boosted localized almost-periodicity
  let k₀ : ℕ := ⌈𝓛 (ε * α₁ / 32)⌉₊
  have hk₀_pos : 0 < k₀ := Nat.ceil_pos.mpr
    (curlog_pos (by positivity)
      (div_le_one_of_le₀ (hεα₁_le1.trans (by norm_num)) (by norm_num)))
  let k : ℕ := 2 * k₀
  have hk_ne : k ≠ 0 := by dsimp [k]; omega
  have hk_pow_le : (2⁻¹ : ℝ) ^ k ≤ ε * α₁ / 32 := by
    have h4_le : (4⁻¹ : ℝ) ≤ exp (-1) := by
      rw [exp_neg]
      exact (inv_le_inv₀ (by norm_num) (exp_pos 1)).mpr (by linarith [exp_one_lt_d9])
    calc
      (2⁻¹ : ℝ) ^ k = ((2⁻¹ : ℝ) ^ 2) ^ k₀ := by dsimp [k]; rw [pow_mul]
      _ = (4⁻¹ : ℝ) ^ k₀ := by norm_num
      _ ≤ (exp (-1)) ^ k₀ := pow_le_pow_left₀ (by norm_num) h4_le k₀
      _ = exp (-(k₀ : ℝ)) := by rw [← exp_nat_mul]; ring_nf
      _ ≤ exp (-log ((ε * α₁ / 32)⁻¹)) := by
          apply exp_le_exp.mpr
          have hceil : 1 + log ((ε * α₁ / 32)⁻¹) ≤ k₀ := Nat.le_ceil _
          linarith
      _ = ε * α₁ / 32 := by
          rw [log_inv, neg_neg, exp_log (by positivity)]
  have hk_le : (k : ℝ) ≤ 128 * 𝓛 α₁ / ε := by
    have hcur_le : 𝓛 (ε * α₁ / 32) ≤ 32 / ε * 𝓛 α₁ := by
      calc
        𝓛 (ε * α₁ / 32) ≤ 32 * 𝓛 (ε * α₁) :=
          curlog_div_le (by positivity) hεα₁_le1 (by norm_num)
        _ ≤ 32 * (ε⁻¹ * 𝓛 α₁) :=
          mul_le_mul_of_nonneg_left (curlog_mul_le hε₀ hε₁ hα₁₀ hα₁₁) (by norm_num)
        _ = 32 / ε * 𝓛 α₁ := by ring
    have hceil_le : (k₀ : ℝ) ≤ 2 * 𝓛 (ε * α₁ / 32) := by
      have h1 : 1 ≤ 𝓛 (ε * α₁ / 32) := one_le_curlog (by positivity)
        (div_le_one_of_le₀ ((mul_le_of_le_one_right hε₀.le hα₁₁).trans (hε₁.trans (by norm_num)))
          (by norm_num))
      have hlt : (k₀ : ℝ) < 𝓛 (ε * α₁ / 32) + 1 :=
        Nat.ceil_lt_add_one (zero_le_one.trans h1)
      linarith only [hlt, h1]
    dsimp [k]
    push_cast
    calc
      2 * (k₀ : ℝ) ≤ 4 * 𝓛 (ε * α₁ / 32) := by linarith
      _ ≤ 4 * (32 / ε * 𝓛 α₁) := by linarith
      _ = 128 * 𝓛 α₁ / ε := by ring
  obtain ⟨T₀, s₀, hT₀_sub, hKT, hT_err⟩ :=
    linfty_ap_boosted_sub (B_ind := -S') hA_ne B₀.finset_nonempty hS'_ne.neg hA₁_ne
      (ε := 3 * ε / 8) (by positivity) (by linarith) k hk_ne hK₂ hσ_A
  let η₀ : ℝ :=
    K ^ (-4096 * ⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ * k ^ 2 / (3 * ε / 8) ^ 2 : ℝ)
  have hη₀ : 0 < η₀ := by dsimp [η₀]; positivity
  have hT₀_ne : T₀.Nonempty := by
    rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
    exact (mul_pos hη₀ (Nat.cast_pos.mpr B₀.card_finset_pos)).trans_le hKT
  -- Upper bound on `16 * log (4 / η₀)`
  have hlog_η : 16 * log (4 / η₀) ≤ 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by
    have hratio_ge : α₁ / 2 ≤ min 1 ((#A₁ : ℝ) / #(-S')) := by
      refine le_min (by linarith) ?_
      rw [Finset.card_neg, le_div_iff₀ (Nat.cast_pos.mpr hS'_ne.card_pos)]
      have hS'_le : (#S' : ℝ) ≤ 2 * #B.finset := by exact_mod_cast hS'_card
      have hm1 : (α₁ / 2) * (#S' : ℝ) ≤ (α₁ / 2) * (2 * #B.finset) :=
        mul_le_mul_of_nonneg_left hS'_le (by positivity)
      linarith only [hm1, hA₁_card]
    have hcur_min : 1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹ ≤ 2 * 𝓛 α₁ := by
      calc
        1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹
          ≤ 𝓛 (α₁ / 2) := curlog_anti (by positivity) hratio_ge
        _ ≤ 2 * 𝓛 α₁ := curlog_div_le hα₁₀ hα₁₁ one_le_two
    have hceil_min : (⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ : ℝ) ≤ 4 * 𝓛 α₁ := by
      have hpos_m := one_le_curlog (x := min 1 ((#A₁ : ℝ) / #(-S')))
        (by positivity) (min_le_left _ _)
      have hlt : (⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ : ℝ) <
          (1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹) + 1 := Int.ceil_lt_add_one _
      linarith only [hlt, hpos_m, hcur_min]
    have hlogK : log K ≤ 2 * 𝓛 α₂ := by
      dsimp [K]
      rw [div_eq_mul_inv, log_mul two_ne_zero (by positivity)]
      have hlog2 : log 2 ≤ 1 := log_two_lt_d9.le.trans (by norm_num)
      have hlog_nn : 0 ≤ log α₂⁻¹ := log_nonneg ((one_le_inv₀ hα₂₀).mpr hα₂₁)
      linarith
    have hlog_inv_η : log η₀⁻¹ ≤ 2 ^ 37 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by
      have hexp_eq : η₀⁻¹ = K ^ (4096 * ⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ *
          k ^ 2 / (3 * ε / 8) ^ 2 : ℝ) := by
        dsimp [η₀]
        rw [← Real.rpow_neg (by positivity)]
        congr 1; ring
      rw [hexp_eq, Real.log_rpow (by positivity)]
      have h1 : (0 : ℝ) ≤ ⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ := by
        exact_mod_cast Int.ceil_nonneg (curlog_pos (by positivity) (min_le_left _ _)).le
      have hk_sq : (k : ℝ) ^ 2 ≤ 2 ^ 14 * 𝓛 α₁ ^ 2 / ε ^ 2 := by
        have hsq := pow_le_pow_left₀ (by positivity) hk_le 2
        calc
          (k : ℝ) ^ 2 ≤ (128 * 𝓛 α₁ / ε) ^ 2 := hsq
          _ = 2 ^ 14 * 𝓛 α₁ ^ 2 / ε ^ 2 := by ring
      calc
        (4096 * ⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ * k ^ 2 / (3 * ε / 8) ^ 2) * log K
          ≤ (4096 * (4 * 𝓛 α₁) * (2 ^ 14 * 𝓛 α₁ ^ 2 / ε ^ 2) / (ε ^ 2 / 8)) * (2 * 𝓛 α₂) := by
            have hden : ε ^ 2 / 8 ≤ (3 * ε / 8) ^ 2 := by
              have hsq_nn : 0 ≤ ε ^ 2 := sq_nonneg ε
              have hrew : (3 * ε / 8) ^ 2 = (9 / 64 : ℝ) * ε ^ 2 := by ring
              rw [hrew]
              linarith only [hsq_nn]
            have hlogK_nn : 0 ≤ log K := log_nonneg (by linarith only [hK₂])
            have hnum_le : 4096 * (⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ : ℝ) * (k : ℝ) ^ 2 ≤
                4096 * (4 * 𝓛 α₁) * (2 ^ 14 * 𝓛 α₁ ^ 2 / ε ^ 2) := by
              have hc4 : 4096 * (⌈1 + log (min 1 ((#A₁ : ℝ) / #(-S')))⁻¹⌉ : ℝ) ≤
                  4096 * (4 * 𝓛 α₁) := by linarith only [hceil_min]
              exact mul_le_mul hc4 hk_sq (sq_nonneg _) (by positivity)
            refine mul_le_mul ?_ hlogK hlogK_nn (by positivity)
            exact div_le_div₀ (by positivity) hnum_le (by positivity) hden
        _ = 2 ^ 32 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by field_simp [hε₀.ne']; ring
        _ ≤ 2 ^ 37 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) :=
            mul_le_mul_of_nonneg_right (by norm_num) (by positivity)
        _ = 2 ^ 37 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by ring
    have hlog4 : log (4 / η₀) = log 4 + log η₀⁻¹ := by
      rw [div_eq_mul_inv, log_mul (by norm_num) (by positivity)]
    have hlog4_le : log 4 ≤ 2 := by
      have : (4 : ℝ) = 2 * 2 := by norm_num
      rw [this, log_mul two_ne_zero two_ne_zero]
      linarith [log_two_lt_d9]
    have hone_le_prod : 1 ≤ 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by
      rw [le_div_iff₀ (by positivity)]
      have hε4 : ε ^ 4 ≤ 1 := pow_le_one₀ hε₀.le hε₁
      have hp3 : 1 ≤ 𝓛 α₁ ^ 3 := one_le_pow₀ hLα₁
      have hprod1 : 1 ≤ 𝓛 α₁ ^ 3 * 𝓛 α₂ := one_le_mul_of_one_le_of_one_le hp3 hLα₂
      linarith only [hε4, hprod1]
    rw [hlog4]
    calc
      16 * (log 4 + log η₀⁻¹)
        ≤ 16 * (2 + 2 ^ 37 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by linarith only [hlog4_le, hlog_inv_η]
      _ ≤ 16 * (2 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) + 2 ^ 37 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4)) := by
          have hr37 : 2 ^ 37 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 =
              2 ^ 37 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by ring
          linarith only [hone_le_prod, hr37]
      _ ≤ 2 ^ 43 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by
          have hpos_p : 0 ≤ 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by positivity
          linarith only [hpos_p]
      _ = 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by ring
  -- Step 3: Bohr relative Chang's lemma
  let ε_spec : ℝ := ε * α₁ / 16
  have hε_spec_pos : 0 < ε_spec := by dsimp [ε_spec]; positivity
  have hε_spec_le1 : ε_spec ≤ 1 := by dsimp [ε_spec]; linarith only [hεα₁_le1]
  obtain ⟨Γ, _, hΓ_card, hΓ_approx⟩ :=
    bohr_relative_chang hB₀_reg hB₀_pos hT₀_ne hT₀_sub hη₀ hKT hε_spec_pos hε_spec_le1
  have hΓ_upper : (#Γ : ℝ) ≤ 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := hΓ_card.trans hlog_η
  let ρ : ℝ := ε_spec / (2 ^ 18 * (B₀.rank + 1 : ℝ) ^ 2)
  let δ : ℝ := ε_spec / (2 ^ 10 * (#Γ + 1 : ℝ))
  have hρ_pos : 0 < ρ := by dsimp [ρ]; positivity
  have hρ_le1 : ρ ≤ 1 := by
    refine div_le_one_of_le₀ (hε_spec_le1.trans ?_) (by positivity)
    have hr_nn : (0 : ℝ) ≤ B₀.rank := Nat.cast_nonneg _
    have h1_sq : (1 : ℝ) ≤ (B₀.rank + 1 : ℝ) ^ 2 := one_le_pow₀ (by linarith only [hr_nn])
    linarith only [h1_sq]
  have hδ_pos : 0 < δ := by dsimp [δ]; positivity
  have hδ_le2 : δ ≤ 2 := by
    refine (div_le_one_of_le₀ (hε_spec_le1.trans ?_) (by positivity)).trans one_le_two
    have hg_nn : (0 : ℝ) ≤ #Γ := Nat.cast_nonneg _
    linarith only [hg_nn]
  let B_raw : BohrSet G := (ρ • B₀) ⊓ BohrSet.ofWidth (fun _ ↦ (⟨δ, hδ_pos.le⟩ : ℝ≥0)) Γ
  obtain ⟨ρ_reg, hρ_reg_lo, hρ_reg_hi, hB''_reg⟩ := BohrSet.regularity B_raw
  let B'' : BohrSet G := ρ_reg • B_raw
  have hρ_reg_pos : 0 < ρ_reg := by linarith
  have hB_raw_pos : B_raw.PosWidth :=
    (hB₀_pos.smul hρ_pos.ne').inf
      (BohrSet.posWidth_ofWidth (show (0 : ℝ≥0) < ⟨δ, hδ_pos.le⟩ from hδ_pos))
  have hB''_pos : B''.PosWidth := hB_raw_pos.smul hρ_reg_pos.ne'
  have hB''_sub_raw : B''.finset ⊆ B_raw.finset := by
    simpa [B'', one_smul] using BohrSet.smul_finset_mono hρ_reg_pos.le hρ_reg_hi
  have hB_raw_sub_B₀ : B_raw.finset ⊆ B₀.finset :=
    (BohrSet.finset_mono inf_le_left).trans
      (by simpa [one_smul] using BohrSet.smul_finset_mono hρ_pos.le hρ_le1)
  have hB''_sub_B' : B''.finset ⊆ B'.finset :=
    hB''_sub_raw.trans (hB_raw_sub_B₀.trans hB₀_sub_B')
  -- Rank bound on `B''`
  have hB''_rk_nat : B''.rank ≤ d + #Γ := by
    have h1 : B''.rank = B_raw.rank := rfl
    rw [h1]
    exact (BohrSet.rank_inf_ofWidth_le (ρ • B₀) Γ _).trans (Nat.add_le_add_right hB₀_rk #Γ)
  have hB''_rk_real : (B''.rank : ℝ) ≤ d + 2 ^ 44 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by
    have h1 : (B''.rank : ℝ) ≤ (d : ℝ) + #Γ := by exact_mod_cast hB''_rk_nat
    have hpos_p : 0 ≤ 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 := by positivity
    have hrew1 : 2 ^ 43 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 =
        2 ^ 43 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by ring
    have hrew2 : 2 ^ 44 * 𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4 =
        2 ^ 44 * (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) := by ring
    linarith only [h1, hΓ_upper, hpos_p, hrew1, hrew2]
  -- Size bound on `B''`
  have hB''_size :
      exp (-2 ^ 56 * ((d + 1 : ℝ) * 𝓛 (ε * α₁ / (d + 1 : ℝ)) +
        (𝓛 α₁ ^ 3 * 𝓛 α₂ / ε ^ 4) * 𝓛 (ε * α₁ * α₂))) * #B'.finset ≤ #B''.finset := by
    have h1 : (ρ_reg / 5) ^ B_raw.rank * (#B_raw.finset : ℝ) ≤ #B''.finset :=
      B_raw.le_card_smul hρ_reg_pos hρ_reg_hi
    have h1' : (10⁻¹ : ℝ) ^ (d + #Γ) * (#B_raw.finset : ℝ) ≤ #B''.finset := by
      refine le_trans ?_ h1
      gcongr
      exact (pow_le_pow_of_le_one (by norm_num) (by norm_num) hB''_rk_nat).trans
        (pow_le_pow_left₀ (by norm_num) (by linarith) _)
    have h2 : (δ / 18) ^ #Γ * (#(((2⁻¹ : ℝ) • (ρ • B₀)).finset) : ℝ) ≤ #B_raw.finset :=
      BohrSet.le_card_inf_ofWidth (ρ • B₀) Γ hδ_pos hδ_le2
    have h3 : ((ρ / 2) / 5) ^ B₀.rank * (#B₀.finset : ℝ) ≤ #(((2⁻¹ : ℝ) • (ρ • B₀)).finset) := by
      have hmul_smul : (2⁻¹ : ℝ) • (ρ • B₀) = (ρ / 2) • B₀ := by rw [← mul_smul]; congr 1; ring
      rw [hmul_smul]
      exact B₀.le_card_smul (by positivity) (by linarith)
    have h4 : (ρ₀ * κ_step / 5) ^ B'.rank * (#B'.finset : ℝ) ≤ #B₀.finset := by
      rw [hB₀_eq]
      exact B'.le_card_smul (by positivity)
        ((mul_le_of_le_one_right hρ₀_pos.le hκ_step_le1).trans hρ₀_hi)
    have hcomb_factors :
        (10⁻¹ : ℝ) ^ (d + #Γ) * (δ / 18) ^ #Γ * (ρ / 10) ^ d *
          ((1000 * (d + 1 : ℝ))⁻¹) ^ d * (#B'.finset : ℝ) ≤ #B''.finset := by
      have h3' : (ρ / 10) ^ d * (#B₀.finset : ℝ) ≤ #(((2⁻¹ : ℝ) • (ρ • B₀)).finset) := by
        refine le_trans ?_ h3
        have hrr : ρ / 10 = (ρ / 2) / 5 := by ring
        rw [hrr]
        exact mul_le_mul_of_nonneg_right
          (pow_le_pow_of_le_one (by positivity) (by linarith only [hρ_le1]) hB₀_rk)
          (Nat.cast_nonneg _)
      have h4' : ((1000 * (d + 1 : ℝ))⁻¹) ^ d * (#B'.finset : ℝ) ≤ #B₀.finset := by
        refine le_trans ?_ h4
        gcongr
        have hbase : (1000 * (d + 1 : ℝ))⁻¹ ≤ ρ₀ * κ_step / 5 := by
          dsimp [κ_step]
          rw [inv_eq_one_div, div_le_div_iff₀ (by positivity) (by norm_num)]
          have : ρ₀ * (100 * (d + 1 : ℝ))⁻¹ * (1000 * (d + 1 : ℝ)) = 10 * ρ₀ := by
            field_simp; ring
          linarith
        exact (pow_le_pow_of_le_one (by positivity)
          (hbase.trans (by
            have : ρ₀ * κ_step ≤ 1 := (mul_le_of_le_one_right hρ₀_pos.le hκ_step_le1).trans hρ₀_hi
            linarith)) hB'_rk).trans (pow_le_pow_left₀ (by positivity) hbase _)
      calc
        (10⁻¹ : ℝ) ^ (d + #Γ) * (δ / 18) ^ #Γ * (ρ / 10) ^ d *
            ((1000 * (d + 1 : ℝ))⁻¹) ^ d * (#B'.finset : ℝ)
          = (10⁻¹ : ℝ) ^ (d + #Γ) * ((δ / 18) ^ #Γ * ((ρ / 10) ^ d *
              (((1000 * (d + 1 : ℝ))⁻¹) ^ d * (#B'.finset : ℝ)))) := by ring
        _ ≤ (10⁻¹ : ℝ) ^ (d + #Γ) * ((δ / 18) ^ #Γ * ((ρ / 10) ^ d * (#B₀.finset : ℝ))) := by
              gcongr
        _ ≤ (10⁻¹ : ℝ) ^ (d + #Γ) * ((δ / 18) ^ #Γ *
              (#(((2⁻¹ : ℝ) • (ρ • B₀)).finset) : ℝ)) := by gcongr
        _ ≤ (10⁻¹ : ℝ) ^ (d + #Γ) * (#B_raw.finset : ℝ) := by gcongr
        _ ≤ #B''.finset := h1'
    refine le_trans (mul_le_mul_of_nonneg_right ?_ (Nat.cast_nonneg _)) hcomb_factors
    exact th_ap_int_exp_factors hB₀_rk hα₁₀ hα₁₁ hα₂₀ hα₂₁ hε₀ hε₁ hΓ_upper
  refine ⟨B'', hB''_sub_B', hB''_reg, hB''_pos, hB''_rk_real, hB''_size, ?_⟩
  exact th_ap_int_fourier_err hα₁₀ hα₁₁ hε₀ hA₁_ne hA₂_ne hT₀_ne hA₁_card hS_card
    hk_pow_le hT_err (fun v hv ψ hψ ↦ hΓ_approx ρ δ hρ_pos hδ_pos le_rfl le_rfl v
      (hB''_sub_raw hv) ψ hψ)

end BohrAlmostPeriodicity

end BohrFourier
