/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: IEANTN contributors
-/
import ZetaZerosBasic
import Mathlib.Analysis.MellinTransform
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.MeasureTheory.Function.Floor
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals

/-!
# Polynomial growth of `riemannZeta₁` on `-1/2 ≤ Re s` and vertical-line lower bound
-/

namespace ZetaHadamardSolution

open Complex Real MeasureTheory Filter Topology Set GammaSolution

private noncomputable def zetaReal (s : ℝ) : ℝ := ∑' k : ℕ, 1 / ((k : ℝ) + 1) ^ s

private theorem zeta_ofReal {s : ℝ} (hs : 1 < s) : riemannZeta (s : ℂ) = (zetaReal s : ℂ) := by
  rw [zeta_eq_tsum_one_div_nat_add_one_cpow (by simpa using hs), zetaReal, Complex.ofReal_tsum]
  refine tsum_congr fun k ↦ ?_
  have hk : (0 : ℝ) ≤ (k : ℝ) + 1 := by positivity
  rw [Complex.ofReal_div, Complex.ofReal_one, Complex.ofReal_cpow hk]
  push_cast
  ring

/-- Second Bernoulli periodic kernel `P₂(t) = ({t}² - {t}) / 2`. -/
noncomputable def bernP2 (t : ℝ) : ℝ := ((Int.fract t) ^ 2 - Int.fract t) / 2

lemma abs_bernP2_le (t : ℝ) : |bernP2 t| ≤ 1 / 8 := by
  unfold bernP2
  have h0 : 0 ≤ Int.fract t := Int.fract_nonneg t
  have h1 : Int.fract t ≤ 1 := (Int.fract_lt_one t).le
  rw [abs_le]
  constructor
  · nlinarith [sq_nonneg (Int.fract t - 1 / 2)]
  · nlinarith [mul_nonpos_of_nonneg_of_nonpos h0 (sub_nonpos.mpr h1)]

lemma measurable_bernP2 : Measurable bernP2 :=
  ((measurable_fract.pow_const 2).sub measurable_fract).div_const 2

/-- Mellin input `1_{t > 1} · P₂(t) · t⁻¹`. -/
noncomputable def gfr2 (t : ℝ) : ℂ :=
  (Ioi (1 : ℝ)).indicator (fun t ↦ ((bernP2 t * t ^ (-1 : ℝ) : ℝ) : ℂ)) t

/-- Analytic Mellin integral `J₂(s) = ∫₁^∞ P₂(t) t^{-s-2} dt` on `Re s > -1`. -/
noncomputable def Jz2 (s : ℂ) : ℂ := mellin gfr2 (-s)

lemma norm_gfr2_le_eighth (t : ℝ) : ‖gfr2 t‖ ≤ 1 / 8 := by
  unfold gfr2
  by_cases h : t ∈ Ioi (1 : ℝ)
  · have ht1 : 1 < t := h
    have ht0 : 0 < t := lt_trans zero_lt_one ht1
    have hrp : t ^ (-1 : ℝ) ≤ 1 := by
      rw [Real.rpow_neg_one]
      exact inv_le_one_of_one_le₀ ht1.le
    rw [indicator_of_mem h, Complex.norm_real, Real.norm_eq_abs, abs_mul,
      abs_of_nonneg (Real.rpow_nonneg ht0.le _)]
    calc |bernP2 t| * t ^ (-1 : ℝ) ≤ (1 / 8) * 1 :=
          mul_le_mul (abs_bernP2_le t) hrp (Real.rpow_nonneg ht0.le _) (by norm_num)
      _ = 1 / 8 := by ring
  · rw [indicator_of_notMem h, norm_zero]; norm_num

lemma norm_gfr2_le_rpow {t : ℝ} (ht : 1 < t) : ‖gfr2 t‖ ≤ (1 / 8) * t ^ (-1 : ℝ) := by
  have ht0 : 0 < t := lt_trans zero_lt_one ht
  rw [gfr2, indicator_of_mem (show t ∈ Ioi (1 : ℝ) from ht), Complex.norm_real, Real.norm_eq_abs,
    abs_mul, abs_of_nonneg (Real.rpow_nonneg ht0.le _)]
  exact mul_le_mul_of_nonneg_right (abs_bernP2_le t) (Real.rpow_nonneg ht0.le _)

lemma measurable_gfr2 : Measurable gfr2 :=
  (Complex.measurable_ofReal.comp (measurable_bernP2.mul (measurable_id.pow_const (-1 : ℝ)))).indicator
    measurableSet_Ioi

lemma locallyIntegrableOn_gfr2 : LocallyIntegrableOn gfr2 (Ioi 0) := by
  intro x _
  refine ⟨Ioo (x - 1) (x + 1), nhdsWithin_le_nhds (Ioo_mem_nhds (by linarith) (by linarith)), ?_⟩
  exact IntegrableOn.of_bound (by simp) measurable_gfr2.aestronglyMeasurable (1 / 8)
    (Eventually.of_forall norm_gfr2_le_eighth)

theorem differentiableAt_Jz2 {s : ℂ} (hs : -1 < s.re) : DifferentiableAt ℂ Jz2 s := by
  have htop : gfr2 =O[atTop] (fun t : ℝ ↦ t ^ (-(1 : ℝ))) := by
    refine Asymptotics.IsBigO.of_bound (1 / 8) ?_
    filter_upwards [eventually_gt_atTop (1 : ℝ)] with t ht
    have ht0 : 0 < t := lt_trans zero_lt_one ht
    rw [Real.norm_of_nonneg (Real.rpow_nonneg ht0.le _)]
    exact norm_gfr2_le_rpow ht
  have hbot : gfr2 =O[𝓝[>] 0] (fun t : ℝ ↦ t ^ (-(-s.re - 1))) := by
    refine Asymptotics.IsBigO.of_bound 1 ?_
    filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1)] with t ht
    rw [gfr2, indicator_of_notMem (by simp only [mem_Ioi, not_lt]; exact ht.2.le), norm_zero]
    positivity
  have h := mellin_differentiableAt_of_isBigO_rpow (s := -s) locallyIntegrableOn_gfr2 htop
    (by simp; linarith) hbot (by simp)
  exact h.comp s differentiableAt_id.neg

theorem Jz2_ofReal (r : ℝ) :
    Jz2 (r : ℂ) = ((∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2) : ℝ) : ℂ) := by
  rw [Jz2, mellin]
  have h1 : (∫ t in Ioi (0 : ℝ), (t : ℂ) ^ (-(r : ℂ) - 1) • gfr2 t)
      = ∫ t in Ioi (0 : ℝ), (Ioi (1 : ℝ)).indicator
          (fun t ↦ (((bernP2 t * t ^ (-r - 2) : ℝ)) : ℂ)) t := by
    refine setIntegral_congr_fun measurableSet_Ioi fun t ht ↦ ?_
    have ht0 : (0 : ℝ) < t := ht
    by_cases h : t ∈ Ioi (1 : ℝ)
    · rw [gfr2, indicator_of_mem h, indicator_of_mem h, smul_eq_mul]
      have hexp : -(r : ℂ) - 1 = ((-r - 1 : ℝ) : ℂ) := by push_cast; ring
      rw [hexp, ← Complex.ofReal_cpow ht0.le, ← Complex.ofReal_mul]
      congr 1
      calc t ^ (-r - 1) * (bernP2 t * t ^ (-1 : ℝ))
          = bernP2 t * (t ^ (-r - 1) * t ^ (-1 : ℝ)) := by ring
        _ = bernP2 t * t ^ ((-r - 1) + (-1 : ℝ)) := by rw [← Real.rpow_add ht0]
        _ = bernP2 t * t ^ (-r - 2) := by ring_nf
    · rw [gfr2, indicator_of_notMem h, indicator_of_notMem h, smul_zero]
  rw [h1, setIntegral_indicator measurableSet_Ioi,
    show Ioi (0 : ℝ) ∩ Ioi 1 = Ioi 1 by
      ext t; simp only [mem_inter_iff, mem_Ioi]; exact ⟨fun h ↦ h.2, fun h ↦ ⟨by linarith, h⟩⟩]
  exact integral_ofReal

private lemma unit_interval_ibp (k : ℕ) (r : ℝ) :
    (∫ t in ((k : ℝ) + 1)..((k : ℝ) + 2), (t - ((k : ℝ) + 1) - 1 / 2) * t ^ (-r - 1))
      = (r + 1) * ∫ t in ((k : ℝ) + 1)..((k : ℝ) + 2),
          (((t - ((k : ℝ) + 1)) ^ 2 - (t - ((k : ℝ) + 1))) / 2) * t ^ (-r - 2) := by
  set a : ℝ := (k : ℝ) + 1 with ha_def
  have ha1 : 1 ≤ a := by simp [ha_def]
  have hab : a ≤ a + 1 := by linarith
  have hpos : ∀ t ∈ uIcc a (a + 1), 0 < t := by
    intro t ht
    rw [uIcc_of_le hab] at ht
    linarith [ht.1]
  set G : ℝ → ℝ := fun t ↦ (((t - a) ^ 2 - (t - a)) / 2) * t ^ (-r - 1)
  set g1 : ℝ → ℝ := fun t ↦ (t - a - 1 / 2) * t ^ (-r - 1)
  set g2 : ℝ → ℝ := fun t ↦ (((t - a) ^ 2 - (t - a)) / 2) * t ^ (-r - 2)
  have hderiv : ∀ t ∈ uIcc a (a + 1), HasDerivAt G (g1 t - (r + 1) * g2 t) t := by
    intro t ht
    have ht0 : 0 < t := hpos t ht
    have hd1 : HasDerivAt (fun x : ℝ ↦ ((x - a) ^ 2 - (x - a)) / 2) (t - a - 1 / 2) t := by
      have hsub : HasDerivAt (fun x : ℝ ↦ x - a) 1 t := (hasDerivAt_id t).sub_const a
      exact (((hsub.pow 2).sub hsub).div_const 2).congr_deriv (by ring)
    have hd2 : HasDerivAt (fun x : ℝ ↦ x ^ (-r - 1)) ((-r - 1) * t ^ (-r - 2)) t := by
      refine (Real.hasDerivAt_rpow_const (x := t) (p := -r - 1) (Or.inl ht0.ne')).congr_deriv ?_
      rw [show -r - 1 - 1 = -r - 2 by ring]
    refine (hd1.mul hd2).congr_deriv ?_
    simp only [g1, g2]
    ring
  have hg1_int : IntervalIntegrable g1 volume a (a + 1) := by
    refine ContinuousOn.intervalIntegrable ?_
    intro t ht
    exact (continuousAt_id.sub continuousAt_const |>.sub continuousAt_const |>.mul
      (Real.continuousAt_rpow_const _ _ (Or.inl (hpos t ht).ne'))).continuousWithinAt
  have hg2_int : IntervalIntegrable g2 volume a (a + 1) := by
    refine ContinuousOn.intervalIntegrable ?_
    intro t ht
    exact ((((continuousAt_id.sub continuousAt_const).pow 2).sub
      (continuousAt_id.sub continuousAt_const)).div_const 2 |>.mul
      (Real.continuousAt_rpow_const _ _ (Or.inl (hpos t ht).ne'))).continuousWithinAt
  have hftc := intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv (hg1_int.sub (hg2_int.const_mul (r + 1)))
  have hGa : G a = 0 := by simp [G]
  have hGa1 : G (a + 1) = 0 := by simp [G]
  rw [hGa, hGa1, sub_self, intervalIntegral.integral_sub hg1_int (hg2_int.const_mul (r + 1)),
    intervalIntegral.integral_const_mul] at hftc
  have hab2 : a + 1 = (k : ℝ) + 2 := by rw [ha_def]; ring
  rw [← hab2]
  linarith

private lemma riemannZeta₀_ofReal_eq_Jz2 {r : ℝ} (hr : 1 < r) :
    riemannZeta₀ (r : ℂ) = 1 / 2 - (r : ℂ) * ((r : ℂ) + 1) * Jz2 (r : ℂ) := by
  have hr1 : (r : ℂ) ≠ 1 := by exact_mod_cast hr.ne'
  have hz := riemannZeta_eq_inv_sub_add hr1
  rw [zeta_ofReal hr] at hz
  have haux := ZetaAsymptotics.zeta_limit_aux1 hr
  -- First show `termTSum r = 1/(2r) + (r+1) ∫_{1}^∞ bernP2 t * t^{-r-2} dt`.
  have hint2 : IntegrableOn (fun t : ℝ ↦ bernP2 t * t ^ (-r - 2)) (Ioi 1) := by
    refine Integrable.mono' ((integrableOn_Ioi_rpow_of_lt (by linarith : -r - 2 < -1) one_pos).const_mul (1 / 8))
      (measurable_bernP2.mul (measurable_id.pow_const _)).aestronglyMeasurable ?_
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
    have ht0 : 0 < t := lt_trans zero_lt_one ht
    rw [Real.norm_eq_abs, abs_mul, abs_of_nonneg (Real.rpow_nonneg ht0.le _)]
    exact mul_le_mul_of_nonneg_right (abs_bernP2_le t) (Real.rpow_nonneg ht0.le _)
  have hlim2 := intervalIntegral_tendsto_integral_Ioi 1 hint2
    (tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop)
  have hunit : ∀ k : ℕ, ZetaAsymptotics.term (k + 1) r
      = (1 / 2) * (∫ t in ((k : ℝ) + 1)..((k : ℝ) + 2), t ^ (-r - 1))
        + (r + 1) * (∫ t in ((k : ℝ) + 1)..((k : ℝ) + 2), bernP2 t * t ^ (-r - 2)) := by
    intro k
    have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
    have hne : ∀ᵐ t : ℝ ∂volume, t ≠ (k : ℝ) + 2 := by rw [ae_iff]; simp
    have hterm_eq : ZetaAsymptotics.term (k + 1) r
        = ∫ t in ((k : ℝ) + 1)..((k : ℝ) + 2),
            ((t - ((k : ℝ) + 1) - 1 / 2) * t ^ (-r - 1) + (1 / 2) * t ^ (-r - 1)) := by
      rw [ZetaAsymptotics.term]
      push_cast
      rw [show (k : ℝ) + 1 + 1 = (k : ℝ) + 2 by ring]
      refine intervalIntegral.integral_congr fun t ht ↦ ?_
      rw [uIcc_of_le (by linarith)] at ht
      have ht0 : 0 < t := by linarith [ht.1]
      rw [show -r - 1 = -(r + 1) by ring, Real.rpow_neg ht0.le]
      ring
    have hi1 : IntervalIntegrable (fun t : ℝ ↦ (t - ((k : ℝ) + 1) - 1 / 2) * t ^ (-r - 1))
        volume ((k : ℝ) + 1) ((k : ℝ) + 2) := by
      refine ContinuousOn.intervalIntegrable fun t ht ↦ ?_
      rw [uIcc_of_le (by linarith)] at ht
      have ht0 : 0 < t := by linarith [ht.1]
      exact ((continuousAt_id.sub continuousAt_const |>.sub continuousAt_const).mul
        (Real.continuousAt_rpow_const _ _ (Or.inl ht0.ne'))).continuousWithinAt
    have hi2 : IntervalIntegrable (fun t : ℝ ↦ t ^ (-r - 1))
        volume ((k : ℝ) + 1) ((k : ℝ) + 2) := by
      refine ContinuousOn.intervalIntegrable fun t ht ↦ ?_
      rw [uIcc_of_le (by linarith)] at ht
      have ht0 : 0 < t := by linarith [ht.1]
      exact (Real.continuousAt_rpow_const _ _ (Or.inl ht0.ne')).continuousWithinAt
    rw [hterm_eq, intervalIntegral.integral_add hi1 (hi2.const_mul (1 / 2)),
      intervalIntegral.integral_const_mul, unit_interval_ibp k r, add_comm]
    congr 2
    refine intervalIntegral.integral_congr_ae ?_
    filter_upwards [hne] with t htne ht
    rw [uIoc_of_le (by linarith)] at ht
    have hfl : Int.floor t = (k : ℤ) + 1 := by
      rw [Int.floor_eq_iff]; push_cast
      exact ⟨ht.1.le, by linarith [lt_of_le_of_ne ht.2 htne]⟩
    simp only [bernP2, Int.fract, hfl]
    push_cast; ring
  have hint_pow : IntegrableOn (fun t : ℝ ↦ t ^ (-r - 1)) (Ioi 1) :=
    integrableOn_Ioi_rpow_of_lt (by linarith : -r - 1 < -1) one_pos
  have hlim_pow := intervalIntegral_tendsto_integral_Ioi 1 hint_pow
    (tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop)
  have hpart : ∀ N : ℕ, ZetaAsymptotics.termSum r N
      = (1 / 2) * (∫ t in (1 : ℝ)..((N : ℝ) + 1), t ^ (-r - 1))
        + (r + 1) * (∫ t in (1 : ℝ)..((N : ℝ) + 1), bernP2 t * t ^ (-r - 2)) := by
    intro N
    have hadj1 := intervalIntegral.sum_integral_adjacent_intervals
      (f := fun t : ℝ ↦ t ^ (-r - 1)) (μ := volume) (a := fun k : ℕ ↦ (k : ℝ) + 1) (n := N)
      (fun k _ ↦ by
        have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
        exact (intervalIntegrable_iff_integrableOn_Ioc_of_le (by push_cast; linarith)).mpr
          (hint_pow.mono_set fun t ht ↦ by simp only [mem_Ioi]; push_cast at ht; linarith [ht.1]))
    have hadj2 := intervalIntegral.sum_integral_adjacent_intervals
      (f := fun t : ℝ ↦ bernP2 t * t ^ (-r - 2)) (μ := volume) (a := fun k : ℕ ↦ (k : ℝ) + 1) (n := N)
      (fun k _ ↦ by
        have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
        exact (intervalIntegrable_iff_integrableOn_Ioc_of_le (by push_cast; linarith)).mpr
          (hint2.mono_set fun t ht ↦ by simp only [mem_Ioi]; push_cast at ht; linarith [ht.1]))
    simp only [Nat.cast_zero, zero_add] at hadj1 hadj2
    rw [ZetaAsymptotics.termSum, ← hadj1, ← hadj2, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ ↦ ?_
    rw [show ((k + 1 : ℕ) : ℝ) + 1 = (k : ℝ) + 2 by push_cast; ring]
    exact hunit k
  have htend : Tendsto (fun N : ℕ ↦ ZetaAsymptotics.termSum r N) atTop
      (𝓝 ((1 / 2) * (∫ t in Ioi (1 : ℝ), t ^ (-r - 1))
        + (r + 1) * (∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2)))) :=
    ((hlim_pow.const_mul (1 / 2)).add (hlim2.const_mul (r + 1))).congr fun N ↦ (hpart N).symm
  have hsum : HasSum (fun n : ℕ ↦ ZetaAsymptotics.term (n + 1) r)
      ((1 / 2) * (∫ t in Ioi (1 : ℝ), t ^ (-r - 1))
        + (r + 1) * (∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2))) :=
    (hasSum_iff_tendsto_nat_of_nonneg (fun n ↦ ZetaAsymptotics.term_nonneg (n + 1) r) _).mpr htend
  have hval_pow : ∫ t in Ioi (1 : ℝ), t ^ (-r - 1) = 1 / r := by
    rw [integral_Ioi_rpow_of_lt (by linarith : -r - 1 < -1) one_pos, Real.one_rpow,
      show -r - 1 + 1 = -r by ring, div_neg, neg_div, neg_neg]
  have htsum_eq : ZetaAsymptotics.termTSum r
      = (1 / 2) * (1 / r) + (r + 1) * (∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2)) := by
    rw [ZetaAsymptotics.termTSum, hsum.tsum_eq, hval_pow]
  have e : riemannZeta₀ (r : ℂ) = ((zetaReal r - 1 / (r - 1) : ℝ) : ℂ) := by
    rw [eq_sub_of_add_eq' hz.symm]
    push_cast; ring
  have hreal : zetaReal r - 1 / (r - 1)
      = 1 / 2 - r * (r + 1) * ∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2) := by
    rw [zetaReal, haux, htsum_eq]
    have hr0 : r ≠ 0 := by linarith
    rw [show r * ((1 / 2) * (1 / r) + (r + 1) * ∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2))
      = (1 / 2) * (r * (1 / r)) + r * (r + 1) * ∫ t in Ioi (1 : ℝ), bernP2 t * t ^ (-r - 2) by ring,
      mul_one_div_cancel hr0]
    ring
  rw [e, hreal, Jz2_ofReal]
  push_cast
  ring

/-- Analytic continuation identity `riemannZeta₀ s = 1/2 - s(s+1) J₂(s)` on `Re s > -1`. -/
theorem riemannZeta₀_eq_Jz2 {s : ℂ} (hs : -1 < s.re) :
    riemannZeta₀ s = 1 / 2 - s * (s + 1) * Jz2 s := by
  set U : Set ℂ := {z : ℂ | -1 < z.re} with hU
  have hUo : IsOpen U := isOpen_lt continuous_const Complex.continuous_re
  have hf : AnalyticOnNhd ℂ riemannZeta₀ U :=
    differentiable_riemannZeta₀.differentiableOn.analyticOnNhd hUo
  have hg : AnalyticOnNhd ℂ (fun z ↦ 1 / 2 - z * (z + 1) * Jz2 z) U := by
    refine DifferentiableOn.analyticOnNhd (fun z hz ↦ ?_) hUo
    exact ((differentiableAt_const _).sub
      ((differentiableAt_id.mul (differentiableAt_id.add (differentiableAt_const _))).mul
        (differentiableAt_Jz2 hz))).differentiableWithinAt
  have hfreq : ∃ᶠ z in 𝓝[≠] ((3 / 2 : ℝ) : ℂ),
      riemannZeta₀ z = 1 / 2 - z * (z + 1) * Jz2 z := by
    have hu : Tendsto (fun n : ℕ ↦ (((3 / 2 + 1 / ((n : ℝ) + 2)) : ℝ) : ℂ)) atTop
        (𝓝[≠] ((3 / 2 : ℝ) : ℂ)) := by
      refine tendsto_nhdsWithin_iff.mpr ⟨?_, Eventually.of_forall fun n ↦ ?_⟩
      · have h1 : Tendsto (fun n : ℕ ↦ (3 / 2 + 1 / ((n : ℝ) + 2) : ℝ)) atTop (𝓝 (3 / 2 + 0)) :=
          tendsto_const_nhds.add (tendsto_const_nhds.div_atTop
            (tendsto_atTop_add_const_right _ 2 tendsto_natCast_atTop_atTop))
        rw [add_zero] at h1
        exact (Complex.continuous_ofReal.tendsto _).comp h1
      · simp only [mem_compl_iff, mem_singleton_iff]
        intro h
        have h' := Complex.ofReal_injective h
        have : (0 : ℝ) < 1 / ((n : ℝ) + 2) := by positivity
        linarith
    refine hu.frequently (Frequently.of_forall fun n ↦ ?_)
    exact riemannZeta₀_ofReal_eq_Jz2 (by have : (0 : ℝ) < 1 / ((n : ℝ) + 2) := by positivity
                                         linarith)
  exact hf.eqOn_of_preconnected_of_frequently_eq hg (convex_halfSpace_re_gt (-1)).isPreconnected
    (show ((3 / 2 : ℝ) : ℂ) ∈ U by simp [hU]; norm_num) hfreq hs

/-- On `-1/2 ≤ Re s`, `‖Jz2 s‖ ≤ 1 / 4`. -/
theorem norm_Jz2_le_quarter {s : ℂ} (hs : (-1 / 2 : ℝ) ≤ s.re) : ‖Jz2 s‖ ≤ 1 / 4 := by
  rw [Jz2, mellin]
  have heq : (∫ t in Ioi (0 : ℝ), (t : ℂ) ^ (-s - 1) • gfr2 t)
      = ∫ t in Ioi (0 : ℝ), (Ioi (1 : ℝ)).indicator (fun t ↦ (t : ℂ) ^ (-s - 1) • gfr2 t) t := by
    refine setIntegral_congr_fun measurableSet_Ioi fun t _ ↦ ?_
    by_cases h : t ∈ Ioi (1 : ℝ)
    · rw [indicator_of_mem h]
    · rw [indicator_of_notMem h, gfr2, indicator_of_notMem h, smul_zero]
  rw [heq, setIntegral_indicator measurableSet_Ioi,
    show Ioi (0 : ℝ) ∩ Ioi 1 = Ioi 1 by
      ext t; simp only [mem_inter_iff, mem_Ioi]; exact ⟨fun h ↦ h.2, fun h ↦ ⟨by linarith, h⟩⟩]
  have hmaj : IntegrableOn (fun t : ℝ ↦ (1 / 8) * t ^ (-s.re - 2)) (Ioi 1) :=
    (integrableOn_Ioi_rpow_of_lt (by linarith : -s.re - 2 < -1) one_pos).const_mul (1 / 8)
  have hnorm_le : ∀ t ∈ Ioi (1 : ℝ), ‖(t : ℂ) ^ (-s - 1) • gfr2 t‖ ≤ (1 / 8) * t ^ (-s.re - 2) := by
    intro t ht
    have ht1 : 1 < t := ht
    have ht0 : 0 < t := lt_trans zero_lt_one ht1
    rw [norm_smul, Complex.norm_cpow_eq_rpow_re_of_pos ht0]
    simp only [Complex.sub_re, Complex.neg_re, Complex.one_re]
    calc t ^ (-s.re - 1) * ‖gfr2 t‖
        ≤ t ^ (-s.re - 1) * ((1 / 8) * t ^ (-1 : ℝ)) :=
          mul_le_mul_of_nonneg_left (norm_gfr2_le_rpow ht1) (Real.rpow_nonneg ht0.le _)
      _ = (1 / 8) * (t ^ (-s.re - 1) * t ^ (-1 : ℝ)) := by ring
      _ = (1 / 8) * t ^ ((-s.re - 1) + (-1 : ℝ)) := by rw [← Real.rpow_add ht0]
      _ = (1 / 8) * t ^ (-s.re - 2) := by ring_nf
  calc ‖∫ t in Ioi (1 : ℝ), (t : ℂ) ^ (-s - 1) • gfr2 t‖
      ≤ ∫ t in Ioi (1 : ℝ), (1 / 8) * t ^ (-s.re - 2) :=
        norm_integral_le_of_norm_le hmaj
          ((ae_restrict_iff' measurableSet_Ioi).mpr (Eventually.of_forall hnorm_le))
    _ = (1 / 8) * ∫ t in Ioi (1 : ℝ), t ^ (-s.re - 2) := integral_const_mul _ _
    _ = (1 / 8) * (1 / (s.re + 1)) := by
        rw [integral_Ioi_rpow_of_lt (by linarith : -s.re - 2 < -1) one_pos, Real.one_rpow,
          show -s.re - 2 + 1 = -(s.re + 1) by ring, div_neg, neg_div, neg_neg]
    _ ≤ 1 / 4 := by
        have hpos : 0 < s.re + 1 := by linarith
        have hdiv : 1 / (s.re + 1) ≤ 2 := by
          rw [div_le_iff₀ hpos]; linarith
        nlinarith

/-- Explicit cubic bound `‖riemannZeta₁ z‖ ≤ 4 (1 + ‖z‖) ^ 3` on `-1/2 ≤ Re z`. -/
theorem norm_riemannZeta₁_le_cubic {z : ℂ} (hz : (-1 / 2 : ℝ) ≤ z.re) :
    ‖riemannZeta₁ z‖ ≤ 4 * (1 + ‖z‖) ^ 3 := by
  have hz1 : -1 < z.re := by linarith
  rw [riemannZeta₁, riemannZeta₀_eq_Jz2 hz1]
  have hJ : ‖Jz2 z‖ ≤ 1 / 4 := norm_Jz2_le_quarter hz
  have hznn : 0 ≤ ‖z‖ := norm_nonneg z
  have hzm1 : ‖z - 1‖ ≤ 1 + ‖z‖ := by
    calc ‖z - 1‖ ≤ ‖z‖ + ‖(1 : ℂ)‖ := norm_sub_le z 1
      _ = 1 + ‖z‖ := by simp [add_comm]
  have hzp1 : ‖z + 1‖ ≤ 1 + ‖z‖ := by
    calc ‖z + 1‖ ≤ ‖z‖ + ‖(1 : ℂ)‖ := norm_add_le z 1
      _ = 1 + ‖z‖ := by simp [add_comm]
  have h0 : ‖(1 / 2 : ℂ) - z * (z + 1) * Jz2 z‖ ≤ 1 / 2 + ‖z‖ * (1 + ‖z‖) * (1 / 4) := by
    calc ‖(1 / 2 : ℂ) - z * (z + 1) * Jz2 z‖
        ≤ ‖(1 / 2 : ℂ)‖ + ‖z * (z + 1) * Jz2 z‖ := norm_sub_le _ _
      _ = 1 / 2 + ‖z‖ * ‖z + 1‖ * ‖Jz2 z‖ := by norm_num [norm_mul]
      _ ≤ 1 / 2 + ‖z‖ * (1 + ‖z‖) * (1 / 4) := by
          gcongr
  calc ‖(1 : ℂ) + (z - 1) * (1 / 2 - z * (z + 1) * Jz2 z)‖
      ≤ ‖(1 : ℂ)‖ + ‖(z - 1) * (1 / 2 - z * (z + 1) * Jz2 z)‖ := norm_add_le _ _
    _ = 1 + ‖z - 1‖ * ‖(1 / 2 : ℂ) - z * (z + 1) * Jz2 z‖ := by simp
    _ ≤ 1 + (1 + ‖z‖) * (1 / 2 + ‖z‖ * (1 + ‖z‖) * (1 / 4)) := by
        gcongr
    _ ≤ 4 * (1 + ‖z‖) ^ 3 := by nlinarith [pow_nonneg hznn 2, pow_nonneg hznn 3]

/-- On the line `2 + i T`, `‖riemannZeta (2 + T * I)‖ ≥ 1 / 4`. -/
theorem quarter_le_norm_riemannZeta_two_add_im (T : ℝ) :
    (1 / 4 : ℝ) ≤ ‖riemannZeta (2 + (T : ℂ) * I)‖ := by
  set s : ℂ := 2 + (T : ℂ) * I with hs_def
  have hs_re : s.re = 2 := by simp [hs_def]
  have hs1 : 1 < s.re := by rw [hs_re]; norm_num
  rw [zeta_eq_tsum_one_div_nat_add_one_cpow hs1]
  have hsum : Summable (fun n : ℕ ↦ 1 / ((n : ℂ) + 1) ^ s) := by
    have hnorm : Summable (fun n : ℕ ↦ 1 / ((n : ℝ) + 1) ^ (2 : ℝ)) := by
      have h := (Real.summable_one_div_nat_rpow (p := 2)).mpr (by norm_num)
      exact (summable_nat_add_iff (f := fun n : ℕ ↦ 1 / (n : ℝ) ^ (2 : ℝ)) 1).mpr h |>.congr
        fun n ↦ by push_cast; rfl
    refine Summable.of_norm_bounded hnorm fun n ↦ ?_
    have hn : 0 < (n : ℝ) + 1 := by positivity
    have hcast : ((n : ℂ) + 1) = (((n : ℝ) + 1 : ℝ) : ℂ) := by push_cast; ring
    rw [norm_div, norm_one, hcast, Complex.norm_cpow_eq_rpow_re_of_pos hn, hs_re]
  rw [hsum.tsum_eq_zero_add]
  simp only [Nat.cast_zero, zero_add, Complex.one_cpow, div_one]
  set tail1 : ℂ := ∑' n : ℕ, 1 / (((n + 1 : ℕ) : ℂ) + 1) ^ s
  have hsum1 : Summable (fun n : ℕ ↦ 1 / (((n + 1 : ℕ) : ℂ) + 1) ^ s) :=
    (summable_nat_add_iff 1).mpr hsum
  have htail_eq : tail1 = 1 / (2 : ℂ) ^ s + ∑' n : ℕ, 1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s := by
    rw [show tail1 = ∑' n : ℕ, 1 / (((n + 1 : ℕ) : ℂ) + 1) ^ s from rfl, hsum1.tsum_eq_zero_add]
    refine congrArg₂ (· + ·) ?_ (tsum_congr fun n ↦ by congr 2)
    rw [show (((0 + 1 : ℕ) : ℂ) + 1) = (2 : ℂ) by norm_num]
  have hnorm_two : ‖1 / (2 : ℂ) ^ s‖ = 1 / 4 := by
    have h2 : (2 : ℂ) = ((2 : ℝ) : ℂ) := by norm_num
    rw [norm_div, norm_one, h2, Complex.norm_cpow_eq_rpow_re_of_pos (by norm_num), hs_re,
      Real.rpow_two]
    norm_num
  have htel : HasSum (fun n : ℕ ↦ (1 / ((n : ℝ) + 2) - 1 / ((n : ℝ) + 3))) (1 / 2) := by
    set f : ℕ → ℝ := fun n ↦ 1 / ((n : ℝ) + 2)
    have hlim : Tendsto f atTop (𝓝 0) :=
      tendsto_const_nhds.div_atTop (tendsto_atTop_add_const_right _ 2 tendsto_natCast_atTop_atTop)
    have htel_sum : Summable (fun n : ℕ ↦ f n - f (n + 1)) := by
      have hp2 : Summable (fun n : ℕ ↦ 1 / ((n : ℝ) + 2) ^ 2) := by
        have h := (Real.summable_one_div_nat_pow (p := 2)).mpr (by norm_num)
        exact (summable_nat_add_iff (f := fun n : ℕ ↦ 1 / (n : ℝ) ^ 2) 2).mpr h |>.congr
          fun n ↦ by push_cast; rfl
      refine Summable.of_nonneg_of_le (fun n ↦ ?_) (fun n ↦ ?_) hp2
      · simp only [f]
        exact sub_nonneg.mpr (one_div_le_one_div_of_le (by positivity) (by push_cast; linarith))
      · simp only [f]
        have hpos1 : (0 : ℝ) < (n : ℝ) + 2 := by positivity
        have hpos2 : (0 : ℝ) < ((n + 1 : ℕ) : ℝ) + 2 := by positivity
        have hd : 1 / ((n : ℝ) + 2) - 1 / (((n + 1 : ℕ) : ℝ) + 2)
            = 1 / (((n : ℝ) + 2) * ((n : ℝ) + 3)) := by push_cast; field_simp; ring
        rw [hd, one_div_le_one_div (by positivity) (by positivity)]
        nlinarith
    have hs0 := hasSum_sub_succ htel_sum hlim
    have hf0 : f 0 = 1 / 2 := by simp [f]
    rw [hf0] at hs0
    exact hs0.congr_fun fun n ↦ by simp only [f]; push_cast; ring
  have hsum2_norm : Summable (fun n : ℕ ↦ ‖1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖) :=
    summable_norm_iff.mpr (((summable_nat_add_iff 1).mpr hsum1).congr fun _ ↦ rfl)
  have hle_tel : ∀ n : ℕ, ‖1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖
      ≤ 1 / ((n : ℝ) + 2) - 1 / ((n : ℝ) + 3) := by
    intro n
    have hn3 : 0 < (n : ℝ) + 3 := by positivity
    have hcast : (((n + 2 : ℕ) : ℂ) + 1) = (((n : ℝ) + 3 : ℝ) : ℂ) := by push_cast; ring
    rw [norm_div, norm_one, hcast, Complex.norm_cpow_eq_rpow_re_of_pos hn3, hs_re]
    have hd : 1 / ((n : ℝ) + 2) - 1 / ((n : ℝ) + 3) = 1 / (((n : ℝ) + 2) * ((n : ℝ) + 3)) := by
      field_simp; ring
    rw [hd, Real.rpow_two,
      one_div_le_one_div (by positivity) (by positivity)]
    nlinarith
  have htail2 : ‖∑' n : ℕ, 1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖ ≤ 1 / 2 := by
    calc ‖∑' n : ℕ, 1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖
        ≤ ∑' n : ℕ, ‖1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖ := norm_tsum_le_tsum_norm hsum2_norm
      _ ≤ ∑' n : ℕ, (1 / ((n : ℝ) + 2) - 1 / ((n : ℝ) + 3)) :=
          Summable.tsum_le_tsum hle_tel hsum2_norm htel.summable
      _ = 1 / 2 := htel.tsum_eq
  have htail1 : ‖tail1‖ ≤ 3 / 4 := by
    rw [htail_eq]
    calc ‖1 / (2 : ℂ) ^ s + ∑' n : ℕ, 1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖
        ≤ ‖1 / (2 : ℂ) ^ s‖ + ‖∑' n : ℕ, 1 / (((n + 2 : ℕ) : ℂ) + 1) ^ s‖ := norm_add_le _ _
      _ ≤ 1 / 4 + 1 / 2 := by linarith [hnorm_two, htail2]
      _ = 3 / 4 := by ring
  have hsub := norm_sub_norm_le (1 : ℂ) (-tail1)
  simp only [norm_one, norm_neg, sub_neg_eq_add] at hsub
  linarith

/-- On `2 + i T` for `T ≥ 4`, `1 ≤ ‖riemannZeta₁ (2 + T * I)‖`. -/
theorem one_le_norm_riemannZeta₁_two_add_im {T : ℝ} (hT : 4 ≤ T) :
    1 ≤ ‖riemannZeta₁ (2 + (T : ℂ) * I)‖ := by
  have hne1 : (2 : ℂ) + (T : ℂ) * I ≠ 1 := by
    intro h
    have := congrArg Complex.re h
    simp at this
  rw [riemannZeta₁_eq_mul hne1, norm_mul]
  have hm1 : 4 ≤ ‖(2 : ℂ) + (T : ℂ) * I - 1‖ := by
    have him : ((2 : ℂ) + (T : ℂ) * I - 1).im = T := by simp
    have hle := Complex.abs_im_le_norm ((2 : ℂ) + (T : ℂ) * I - 1)
    rw [him, abs_of_nonneg (by linarith)] at hle
    linarith
  have hzeta := quarter_le_norm_riemannZeta_two_add_im T
  nlinarith

end ZetaHadamardSolution
