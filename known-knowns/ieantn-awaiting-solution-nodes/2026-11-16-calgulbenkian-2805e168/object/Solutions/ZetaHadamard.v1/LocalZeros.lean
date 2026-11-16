/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: IEANTN contributors
-/
import ZetaGrowth
import Mathlib.Analysis.Complex.JensenFormula
import Mathlib.Analysis.Meromorphic.FactorizedRational
import Mathlib.Analysis.Complex.HasPrimitives
import Mathlib.Analysis.Complex.BorelCaratheodory
import Mathlib.Analysis.Complex.AbsMax
import Mathlib.Analysis.Complex.Liouville
import Mathlib.Topology.Algebra.InfiniteSum.Real

/-!
# Local zero multiplicity bounds, summability, and Borel-Caratheodory ordinate selection
-/

namespace ZetaHadamardSolution

open Complex Real Filter Topology Set Finset

/-! ### Conjugation symmetry of `zetaOrder` and divisor comparison -/

theorem zetaOrder_conj {ρ : ℂ} (hρ : ρ ≠ 1) :
    IEANTN.zetaOrder (starRingEnd ℂ ρ) = IEANTN.zetaOrder ρ := by
  have hρc : starRingEnd ℂ ρ ≠ 1 := by
    intro h
    exact hρ (by simpa using congrArg (starRingEnd ℂ) h)
  have h1 := tendsto_sub_mul_F hρ
  have h1c : Tendsto (fun z ↦ starRingEnd ℂ ((z - ρ) * F z)) (𝓝[≠] ρ)
      (𝓝 (starRingEnd ℂ (-((IEANTN.zetaOrder ρ : ℤ) : ℂ)))) :=
    (Complex.continuous_conj.tendsto _).comp h1
  have hmap : Tendsto (starRingEnd ℂ) (𝓝[≠] ρ) (𝓝[≠] (starRingEnd ℂ ρ)) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨(Complex.continuous_conj.tendsto ρ).mono_left
      nhdsWithin_le_nhds, ?_⟩
    filter_upwards [self_mem_nhdsWithin] with z hz
    intro heq
    exact hz (by simpa using congrArg (starRingEnd ℂ) heq)
  have h2 : Tendsto (fun z ↦ (starRingEnd ℂ z - starRingEnd ℂ ρ) * F (starRingEnd ℂ z)) (𝓝[≠] ρ)
      (𝓝 (-((IEANTN.zetaOrder (starRingEnd ℂ ρ) : ℤ) : ℂ))) :=
    (tendsto_sub_mul_F hρc).comp hmap
  have hcongr : (fun z ↦ starRingEnd ℂ ((z - ρ) * F z))
      = fun z ↦ (starRingEnd ℂ z - starRingEnd ℂ ρ) * F (starRingEnd ℂ z) := by
    funext z
    rw [map_mul, map_sub, F_conj]
  rw [hcongr] at h1c
  have hlim := tendsto_nhds_unique h2 h1c
  simp only [map_neg, map_intCast, neg_inj] at hlim
  exact_mod_cast hlim

lemma divisor_riemannZeta₁_nonneg (U : Set ℂ) (u : ℂ) :
    0 ≤ MeromorphicOn.divisor riemannZeta₁ U u := by
  by_cases hu : u ∈ U
  · have hm : MeromorphicOn riemannZeta₁ U :=
      (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ U)).meromorphicOn
    rw [hm.divisor_apply hu, (analyticAt_riemannZeta₁ u).meromorphicOrderAt_eq]
    cases h : analyticOrderAt riemannZeta₁ u with
    | top => simp
    | coe n => simp
  · simp [hu]

lemma divisor_riemannZeta₁_eq_zetaOrder {U : Set ℂ} {u : ℂ} (hu : u ∈ U) (hu1 : u ≠ 1) :
    MeromorphicOn.divisor riemannZeta₁ U u = IEANTN.zetaOrder u := by
  have hm : MeromorphicOn riemannZeta₁ U :=
    (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ U)).meromorphicOn
  rw [hm.divisor_apply hu, meromorphicOrderAt_riemannZeta₁_eq hu1, IEANTN.zetaOrder]
  obtain ⟨n, hn⟩ := WithTop.ne_top_iff_exists.mp (meromorphicOrderAt_riemannZeta_ne_top u)
  rw [← hn]
  rfl

lemma divisor_riemannZeta₁_pos_of_mem_support {U : Set ℂ} {u : ℂ}
    (hu : u ∈ (MeromorphicOn.divisor riemannZeta₁ U).support) :
    1 ≤ MeromorphicOn.divisor riemannZeta₁ U u := by
  have hnn := divisor_riemannZeta₁_nonneg U u
  have hne : MeromorphicOn.divisor riemannZeta₁ U u ≠ 0 := Function.mem_support.mp hu
  omega

lemma riemannZeta₁_eq_zero_of_mem_divisor_support {U : Set ℂ} {u : ℂ}
    (hu : u ∈ (MeromorphicOn.divisor riemannZeta₁ U).support) :
    u ∈ U ∧ riemannZeta₁ u = 0 := by
  have hne : MeromorphicOn.divisor riemannZeta₁ U u ≠ 0 := Function.mem_support.mp hu
  have huU : u ∈ U := by
    by_contra hnot
    exact hne (by simp [hnot])
  refine ⟨huU, ?_⟩
  by_contra hnz
  have h0 : MeromorphicOn.divisor riemannZeta₁ U u = 0 := by
    have hm : MeromorphicOn riemannZeta₁ U :=
      (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ U)).meromorphicOn
    rw [hm.divisor_apply huU, (analyticAt_riemannZeta₁ u).meromorphicOrderAt_eq,
      (analyticAt_riemannZeta₁ u).analyticOrderAt_eq_zero.mpr hnz]
    simp
  exact hne h0

private lemma one_div_24_le_log_24_div_23 : (1 / 24 : ℝ) ≤ Real.log (24 / 23) := by
  have h1 := Real.add_one_le_exp (-1 / 24 : ℝ)
  have h2 : Real.exp (1 / 24 : ℝ) ≤ 24 / 23 := by
    have hexp_pos : 0 < Real.exp (1 / 24 : ℝ) := Real.exp_pos _
    have hmul : (23 / 24 : ℝ) * Real.exp (1 / 24 : ℝ)
        ≤ Real.exp (-1 / 24 : ℝ) * Real.exp (1 / 24 : ℝ) :=
      mul_le_mul_of_nonneg_right (by linarith) hexp_pos.le
    rw [← Real.exp_add, show (-1 / 24 : ℝ) + 1 / 24 = 0 by ring, Real.exp_zero] at hmul
    linarith
  have hlog := Real.log_le_log (Real.exp_pos (1 / 24 : ℝ)) h2
  rwa [Real.log_exp] at hlog

private lemma norm_riemannZeta₁_le_pow7_on_ball {T R : ℝ} (hT : 10 ≤ T)
    (hR : R ≤ 12 / 5) {z : ℂ} (hz : z ∈ Metric.closedBall ((2 : ℂ) + (T : ℂ) * I) R) :
    ‖riemannZeta₁ z‖ ≤ T ^ 7 := by
  set c : ℂ := (2 : ℂ) + (T : ℂ) * I
  have hzc : ‖z - c‖ ≤ 12 / 5 := by
    rw [← dist_eq_norm]
    exact (Metric.mem_closedBall.mp hz).trans hR
  have hre : (-1 / 2 : ℝ) ≤ z.re := by
    have h1 : c.re - z.re ≤ |z.re - c.re| := by rw [abs_sub_comm]; exact le_abs_self _
    have h2 : |z.re - c.re| ≤ ‖z - c‖ := by
      simpa [Complex.sub_re] using Complex.abs_re_le_norm (z - c)
    have hcre : c.re = 2 := by simp [c]
    linarith
  have hcnorm : ‖c‖ ≤ T + 2 := by
    calc ‖(2 : ℂ) + (T : ℂ) * I‖
        ≤ ‖(2 : ℂ)‖ + ‖(T : ℂ) * I‖ := norm_add_le _ _
      _ = 2 + |T| := by simp
      _ = T + 2 := by rw [abs_of_nonneg (by linarith)]; ring
  have hznorm : 1 + ‖z‖ ≤ 2 * T := by
    have h1 : ‖z‖ ≤ ‖c‖ + ‖z - c‖ := norm_le_insert' z c
    linarith
  have hcub := norm_riemannZeta₁_le_cubic hre
  have hpow3 : (1 + ‖z‖) ^ 3 ≤ (2 * T) ^ 3 :=
    pow_le_pow_left₀ (by positivity) hznorm 3
  have hT4 : (32 : ℝ) ≤ T ^ 4 := by
    have : (10 : ℝ) ^ 4 ≤ T ^ 4 := pow_le_pow_left₀ (by norm_num) hT 4
    linarith [show (10 : ℝ) ^ 4 = 10000 by norm_num]
  have hT3 : 0 ≤ T ^ 3 := by positivity
  calc ‖riemannZeta₁ z‖ ≤ 4 * (1 + ‖z‖) ^ 3 := hcub
    _ ≤ 4 * (2 * T) ^ 3 := by linarith
    _ = 32 * T ^ 3 := by ring
    _ ≤ T ^ 4 * T ^ 3 := mul_le_mul_of_nonneg_right hT4 hT3
    _ = T ^ 7 := by ring

/-- Jensen bound on the sum of zero multiplicities of `ζ` in `[0, 1] × [T - 1, T + 1]` (`T ≥ 10`). -/
theorem sum_zetaOrder_band_le {T : ℝ} (hT : 10 ≤ T) (F : Finset ℂ)
    (hF : ∀ u ∈ F, u.re ∈ Set.Icc (0 : ℝ) 1 ∧ |u.im - T| ≤ 1) :
    ∑ u ∈ F, (IEANTN.zetaOrder u : ℝ) ≤ 168 * Real.log T := by
  set c : ℂ := (2 : ℂ) + (T : ℂ) * I
  set r : ℝ := 23 / 10
  set R : ℝ := 12 / 5
  set M : ℝ := T ^ 7
  have hr_abs : |r| = r := abs_of_pos (by norm_num [r])
  have hR_abs : |R| = R := abs_of_pos (by norm_num [R])
  have hfc1 : 1 ≤ ‖riemannZeta₁ c‖ := one_le_norm_riemannZeta₁_two_add_im (by linarith)
  have hfc_ne : riemannZeta₁ c ≠ 0 := fun h ↦ by rw [h, norm_zero] at hfc1; linarith
  have hM1 : 1 ≤ M := by
    have : (10 : ℝ) ^ 7 ≤ T ^ 7 := pow_le_pow_left₀ (by norm_num) hT 7
    linarith [show (1 : ℝ) ≤ (10 : ℝ) ^ 7 by norm_num]
  have hjensen := (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ _)).sum_divisor_le
    (r := r) (R := R) (M := M)
    (by rw [hr_abs]; norm_num [r])
    (by rw [hr_abs, hR_abs]; norm_num [r, R])
    hM1 hfc_ne
    (fun z hz ↦ by
      rw [hR_abs] at hz
      exact norm_riemannZeta₁_le_pow7_on_ball hT le_rfl
        (Metric.sphere_subset_closedBall hz))
  set D := MeromorphicOn.divisor riemannZeta₁ (Metric.closedBall c |r|)
  have hsupp_fin : D.support.Finite := D.finiteSupport (isCompact_closedBall c |r|)
  set S := hsupp_fin.toFinset
  have hsum_eq : ((∑ᶠ u, D u : ℤ) : ℝ) = ∑ u ∈ S, (D u : ℝ) := by
    rw [finsum_eq_sum_of_support_subset D (fun u hu ↦ hsupp_fin.mem_toFinset.mpr hu), Int.cast_sum]
  have hF_in_ball : ∀ u ∈ F, u ∈ Metric.closedBall c |r| ∧ u ≠ 1 := by
    intro u hu
    obtain ⟨⟨hre0, hre1⟩, him⟩ := hF u hu
    have hu1 : u ≠ 1 := by
      intro h; rw [h] at him; simp at him; linarith [abs_le.mp him]
    refine ⟨?_, hu1⟩
    rw [Metric.mem_closedBall, dist_eq_norm, hr_abs]
    have hsq : ‖u - c‖ ^ 2 ≤ (23 / 10 : ℝ) ^ 2 := by
      rw [Complex.sq_norm, Complex.normSq_apply]
      have hre_sub : (u - c).re = u.re - 2 := by simp [c]
      have him_sub : (u - c).im = u.im - T := by simp [c]
      rw [hre_sub, him_sub]
      have him_sq : (u.im - T) ^ 2 ≤ 1 := by nlinarith [abs_le.mp him]
      have hre_sq : (u.re - 2) ^ 2 ≤ 4 := by nlinarith
      linarith
    have hsqrt := Real.sqrt_le_sqrt hsq
    rwa [Real.sqrt_sq (norm_nonneg _), Real.sqrt_sq (by norm_num)] at hsqrt
  have hF_le : ∑ u ∈ F, (IEANTN.zetaOrder u : ℝ) ≤ ∑ u ∈ S, (D u : ℝ) := by
    have hFeq : ∑ u ∈ F, (IEANTN.zetaOrder u : ℝ) = ∑ u ∈ F, (D u : ℝ) := by
      refine Finset.sum_congr rfl fun u hu ↦ ?_
      obtain ⟨hub, hu1⟩ := hF_in_ball u hu
      exact_mod_cast (divisor_riemannZeta₁_eq_zetaOrder hub hu1).symm
    rw [hFeq]
    set F' := F.filter (fun u ↦ D u ≠ 0)
    have hF' : ∑ u ∈ F, (D u : ℝ) = ∑ u ∈ F', (D u : ℝ) := by
      rw [Finset.sum_filter]
      refine Finset.sum_congr rfl fun u _ ↦ ?_
      by_cases h0 : D u = 0 <;> simp [h0]
    rw [hF']
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun u hu ↦ ?_) (fun u _ _ ↦ ?_)
    · exact hsupp_fin.mem_toFinset.mpr (Function.mem_support.mpr (Finset.mem_filter.mp hu).2)
    · exact_mod_cast divisor_riemannZeta₁_nonneg (Metric.closedBall c |r|) u
  have hrhs : Real.log (M / ‖riemannZeta₁ c‖) / Real.log (R / r) ≤ 168 * Real.log T := by
    have hTpos : 0 < T := by linarith
    have hdiv_le : M / ‖riemannZeta₁ c‖ ≤ M := div_le_self (by positivity) hfc1
    have hdiv_pos : 0 < M / ‖riemannZeta₁ c‖ := by positivity
    have hlog_num : Real.log (M / ‖riemannZeta₁ c‖) ≤ 7 * Real.log T := by
      calc Real.log (M / ‖riemannZeta₁ c‖)
          ≤ Real.log M := Real.log_le_log hdiv_pos hdiv_le
        _ = Real.log (T ^ 7) := rfl
        _ = 7 * Real.log T := by rw [Real.log_pow]; ring
    have hRr : R / r = 24 / 23 := by norm_num [R, r]
    have hlog_den : (1 / 24 : ℝ) ≤ Real.log (R / r) := by
      rw [hRr]; exact one_div_24_le_log_24_div_23
    have hlogT_nn : 0 ≤ Real.log T := Real.log_nonneg (by linarith)
    calc Real.log (M / ‖riemannZeta₁ c‖) / Real.log (R / r)
        ≤ (7 * Real.log T) / Real.log (R / r) :=
          div_le_div_of_nonneg_right hlog_num (by linarith)
      _ ≤ (7 * Real.log T) / (1 / 24 : ℝ) :=
          div_le_div_of_nonneg_left (by positivity) (by norm_num) hlog_den
      _ = 168 * Real.log T := by ring
  linarith [hF_le, hsum_eq, hjensen, hrhs]

/-- Symmetric band multiplicity bound for `{u : 0 ≤ Re u ≤ 1, | |Im u| - T | ≤ 1}` (`T ≥ 10`). -/
theorem sum_zetaOrder_abs_band_le {T : ℝ} (hT : 10 ≤ T) (F : Finset ℂ)
    (hF : ∀ u ∈ F, u.re ∈ Set.Icc (0 : ℝ) 1 ∧ |(|u.im| - T)| ≤ 1) :
    ∑ u ∈ F, (IEANTN.zetaOrder u : ℝ) ≤ 336 * Real.log T := by
  set F_pos := F.filter (fun u ↦ 0 ≤ u.im)
  set F_neg := F.filter (fun u ↦ ¬ 0 ≤ u.im)
  have hsplit : ∑ u ∈ F, (IEANTN.zetaOrder u : ℝ)
      = (∑ u ∈ F_pos, (IEANTN.zetaOrder u : ℝ)) + ∑ u ∈ F_neg, (IEANTN.zetaOrder u : ℝ) :=
    (Finset.sum_filter_add_sum_filter_not F (fun u ↦ 0 ≤ u.im) _).symm
  have hpos_le : ∑ u ∈ F_pos, (IEANTN.zetaOrder u : ℝ) ≤ 168 * Real.log T := by
    refine sum_zetaOrder_band_le hT F_pos fun u hu ↦ ?_
    have hmem := Finset.mem_filter.mp hu
    obtain ⟨hre, him⟩ := hF u hmem.1
    rw [abs_of_nonneg hmem.2] at him
    exact ⟨hre, him⟩
  have hneg_le : ∑ u ∈ F_neg, (IEANTN.zetaOrder u : ℝ) ≤ 168 * Real.log T := by
    have hinj : ∀ a ∈ F_neg, ∀ b ∈ F_neg, starRingEnd ℂ a = starRingEnd ℂ b → a = b :=
      fun a _ b _ h ↦ RingHom.injective (starRingEnd ℂ) h
    have himg : ∑ u ∈ F_neg, (IEANTN.zetaOrder u : ℝ)
        = ∑ w ∈ F_neg.image (starRingEnd ℂ), (IEANTN.zetaOrder w : ℝ) := by
      rw [Finset.sum_image hinj]
      refine Finset.sum_congr rfl fun u hu ↦ ?_
      have hlt : u.im < 0 := not_le.mp (Finset.mem_filter.mp hu).2
      have hu1 : u ≠ 1 := fun h ↦ by rw [h] at hlt; simp at hlt
      exact_mod_cast (zetaOrder_conj hu1).symm
    rw [himg]
    refine sum_zetaOrder_band_le hT _ fun w hw ↦ ?_
    obtain ⟨u, hu, rfl⟩ := Finset.mem_image.mp hw
    have hlt : u.im < 0 := not_le.mp (Finset.mem_filter.mp hu).2
    obtain ⟨hre, him⟩ := hF u (Finset.mem_filter.mp hu).1
    rw [abs_of_neg hlt] at him
    simpa using ⟨hre, him⟩
  linarith

/-! ### Unconditional summability of the critical-strip partial-fraction difference -/

theorem summable_critical_strip_diff (s w : ℂ) :
    Summable (fun ρ : IEANTN.zetaZeroesIn (Set.Ioo (0 : ℝ) 1) Set.univ ↦
      (1 / (s - (ρ : ℂ)) - 1 / (w - (ρ : ℂ))) * (IEANTN.zetaOrder (ρ : ℂ) : ℂ)) := by
  set term : IEANTN.zetaZeroesIn (Set.Ioo (0 : ℝ) 1) Set.univ → ℂ :=
    fun ρ ↦ (1 / (s - (ρ : ℂ)) - 1 / (w - (ρ : ℂ))) * (IEANTN.zetaOrder (ρ : ℂ) : ℂ)
  set termC : ℂ → ℝ := fun z ↦ ‖(1 / (s - z) - 1 / (w - z)) * (IEANTN.zetaOrder z : ℂ)‖
  set N₀ : ℕ := 2 * Nat.ceil (|s.im| + |w.im|) + 12
  have hN₀_ge : 12 ≤ N₀ := by omega
  have hlow_fin : {z ∈ Metric.closedBall (0 : ℂ) ((N₀ : ℝ) + 2) | riemannZeta₁ z = 0}.Finite :=
    finite_zeros_riemannZeta₁_of_isCompact (isCompact_closedBall _ _)
  set B_low : ℝ := ∑ z ∈ hlow_fin.toFinset, termC z
  have hp_sum : Summable (fun n : ℕ ↦ (2688 * ‖w - s‖) * (1 / (n : ℝ) ^ (3 / 2 : ℝ))) :=
    ((Real.summable_one_div_nat_rpow (p := 3 / 2)).mpr (by norm_num)).mul_left _
  set B_high : ℝ := ∑' n : ℕ, (2688 * ‖w - s‖) * (1 / (n : ℝ) ^ (3 / 2 : ℝ))
  refine Summable.of_norm (summable_of_sum_le (c := B_low + B_high) (fun _ ↦ norm_nonneg _) ?_)
  intro S
  set T : Finset ℂ := S.image Subtype.val
  have hST : ∑ ρ ∈ S, ‖term ρ‖ = ∑ z ∈ T, termC z := by
    rw [Finset.sum_image (fun a _ b _ h ↦ Subtype.ext h)]
  rw [hST]
  have hT_prop : ∀ z ∈ T, z.re ∈ Set.Icc (0 : ℝ) 1 ∧ riemannZeta₁ z = 0 := by
    intro z hz
    obtain ⟨ρ, -, rfl⟩ := Finset.mem_image.mp hz
    obtain ⟨⟨h0, h1⟩, -, hζ⟩ := ρ.2
    have hne1 : (ρ : ℂ) ≠ 1 := fun h ↦ by rw [h] at h1; simp at h1
    exact ⟨⟨h0.le, h1.le⟩, (riemannZeta_eq_zero_iff_riemannZeta₁ hne1).mp hζ⟩
  set T_low := T.filter (fun z ↦ |z.im| < (N₀ : ℝ))
  set T_high := T.filter (fun z ↦ ¬ |z.im| < (N₀ : ℝ))
  have hsplit : ∑ z ∈ T, termC z = (∑ z ∈ T_low, termC z) + ∑ z ∈ T_high, termC z :=
    (Finset.sum_filter_add_sum_filter_not T (fun z ↦ |z.im| < (N₀ : ℝ)) termC).symm
  have hlow_le : ∑ z ∈ T_low, termC z ≤ B_low := by
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun z hz ↦ ?_) (fun _ _ _ ↦ norm_nonneg _)
    have hm := Finset.mem_filter.mp hz
    obtain ⟨⟨hre0, hre1⟩, hζ1⟩ := hT_prop z hm.1
    rw [hlow_fin.mem_toFinset]
    refine ⟨?_, hζ1⟩
    rw [Metric.mem_closedBall, dist_zero_right]
    calc ‖z‖ ≤ |z.re| + |z.im| := Complex.norm_le_abs_re_add_abs_im z
      _ ≤ 1 + (N₀ : ℝ) := by rw [abs_of_nonneg hre0]; linarith [hm.2]
      _ ≤ (N₀ : ℝ) + 2 := by linarith
  have hhigh_le : ∑ z ∈ T_high, termC z ≤ B_high := by
    set M_sup : ℕ := T_high.sup (fun z ↦ Nat.floor |z.im|) + 1
    have hmaps : ∀ z ∈ T_high, Nat.floor |z.im| ∈ Finset.Ico N₀ M_sup := by
      intro z hz
      have hge : (N₀ : ℝ) ≤ |z.im| := not_lt.mp (Finset.mem_filter.mp hz).2
      rw [Finset.mem_Ico]
      exact ⟨Nat.le_floor hge, Nat.lt_succ_of_le (Finset.le_sup (f := fun w ↦ Nat.floor |w.im|) hz)⟩
    rw [← Finset.sum_fiberwise_of_maps_to hmaps termC]
    have hfiber : ∀ n ∈ Finset.Ico N₀ M_sup,
        (∑ z ∈ T_high with Nat.floor |z.im| = n, termC z)
          ≤ (2688 * ‖w - s‖) * (1 / (n : ℝ) ^ (3 / 2 : ℝ)) := by
      intro n hn
      have hn_ge : N₀ ≤ n := (Finset.mem_Ico.mp hn).1
      have hn12 : (12 : ℝ) ≤ (n : ℝ) := by exact_mod_cast (le_trans hN₀_ge hn_ge)
      have hn_pos : (0 : ℝ) < (n : ℝ) := by linarith
      have hsim : |s.im| + |w.im| ≤ (n : ℝ) / 2 := by
        have hc : |s.im| + |w.im| ≤ (Nat.ceil (|s.im| + |w.im|) : ℝ) :=
          Nat.le_ceil _
        have hN : (2 * Nat.ceil (|s.im| + |w.im|) + 12 : ℝ) ≤ (n : ℝ) := by
          exact_mod_cast hn_ge
        linarith
      set F_n := T_high.filter (fun z ↦ Nat.floor |z.im| = n)
      have hpt : ∀ z ∈ F_n, termC z
          ≤ (4 * ‖w - s‖ / (n : ℝ) ^ 2) * (IEANTN.zetaOrder z : ℝ) := by
        intro z hz
        have hzf := Finset.mem_filter.mp hz
        have hge0 : 0 ≤ |z.im| := abs_nonneg _
        have hfl_le : (n : ℝ) ≤ |z.im| := by
          rw [← hzf.2]; exact Nat.floor_le hge0
        have hsz_ge : (n : ℝ) / 2 ≤ ‖s - z‖ := by
          have h1 : |z.im| - |s.im| ≤ |s.im - z.im| := by
            rw [abs_sub_comm]; exact abs_sub_abs_le_abs_sub z.im s.im
          have h2 : |s.im - z.im| ≤ ‖s - z‖ := by
            simpa [Complex.sub_im] using Complex.abs_im_le_norm (s - z)
          linarith [abs_nonneg w.im]
        have hwz_ge : (n : ℝ) / 2 ≤ ‖w - z‖ := by
          have h1 : |z.im| - |w.im| ≤ |w.im - z.im| := by
            rw [abs_sub_comm]; exact abs_sub_abs_le_abs_sub z.im w.im
          have h2 : |w.im - z.im| ≤ ‖w - z‖ := by
            simpa [Complex.sub_im] using Complex.abs_im_le_norm (w - z)
          linarith [abs_nonneg s.im]
        have hsz_ne : s - z ≠ 0 := fun h ↦ by simp [h] at hsz_ge; linarith
        have hwz_ne : w - z ≠ 0 := fun h ↦ by simp [h] at hwz_ge; linarith
        have hdiff_eq : 1 / (s - z) - 1 / (w - z) = (w - s) / ((s - z) * (w - z)) := by
          field_simp; ring
        have hdiff_le : ‖1 / (s - z) - 1 / (w - z)‖ ≤ 4 * ‖w - s‖ / (n : ℝ) ^ 2 := by
          rw [hdiff_eq, norm_div, norm_mul]
          have hprod : ((n : ℝ) / 2) * ((n : ℝ) / 2) ≤ ‖s - z‖ * ‖w - z‖ :=
            mul_le_mul hsz_ge hwz_ge (by positivity) (norm_nonneg _)
          calc ‖w - s‖ / (‖s - z‖ * ‖w - z‖)
              ≤ ‖w - s‖ / (((n : ℝ) / 2) * ((n : ℝ) / 2)) :=
                div_le_div_of_nonneg_left (norm_nonneg _) (by positivity) hprod
            _ = 4 * ‖w - s‖ / (n : ℝ) ^ 2 := by field_simp; ring
        obtain ⟨⟨_, hre1⟩, hζ1⟩ := hT_prop z (Finset.mem_filter.mp hzf.1).1
        have hzne1 : z ≠ 1 := fun h ↦ by rw [h] at hfl_le; simp at hfl_le; linarith
        have hord_pos : 0 ≤ IEANTN.zetaOrder z :=
          le_trans zero_le_one
            (zetaOrder_pos_of_zeta_eq_zero hzne1 ((riemannZeta_eq_zero_iff_riemannZeta₁ hzne1).mpr hζ1))
        have hord_norm : ‖(IEANTN.zetaOrder z : ℂ)‖ = (IEANTN.zetaOrder z : ℝ) := by
          rw [Complex.norm_intCast, abs_of_nonneg (by exact_mod_cast hord_pos)]
        simp only [termC, norm_mul, hord_norm]
        exact mul_le_mul_of_nonneg_right hdiff_le (by exact_mod_cast hord_pos)
      have hband : ∑ z ∈ F_n, (IEANTN.zetaOrder z : ℝ) ≤ 336 * Real.log (n : ℝ) := by
        refine sum_zetaOrder_abs_band_le (by linarith) F_n fun z hz ↦ ?_
        have hzf := Finset.mem_filter.mp hz
        obtain ⟨hre, _⟩ := hT_prop z (Finset.mem_filter.mp hzf.1).1
        have hfl1 : (n : ℝ) ≤ |z.im| := by rw [← hzf.2]; exact Nat.floor_le (abs_nonneg _)
        have hfl2 : |z.im| < (n : ℝ) + 1 := by
          rw [← hzf.2]; exact Nat.lt_floor_add_one _
        exact ⟨hre, abs_le.mpr ⟨by linarith, by linarith⟩⟩
      have hlog_rpow : Real.log (n : ℝ) ≤ 2 * (n : ℝ) ^ (1 / 2 : ℝ) := by
        have h := Real.log_le_rpow_div (Nat.cast_nonneg n) (by norm_num : (0 : ℝ) < 1 / 2)
        linarith
      have hrpow_id : (n : ℝ) ^ (1 / 2 : ℝ) / (n : ℝ) ^ 2 = 1 / (n : ℝ) ^ (3 / 2 : ℝ) := by
        rw [← Real.rpow_two, ← Real.rpow_sub hn_pos,
          show (1 / 2 : ℝ) - 2 = -(3 / 2 : ℝ) by ring, Real.rpow_neg hn_pos.le, one_div]
      calc ∑ z ∈ F_n, termC z
          ≤ ∑ z ∈ F_n, (4 * ‖w - s‖ / (n : ℝ) ^ 2) * (IEANTN.zetaOrder z : ℝ) :=
            Finset.sum_le_sum hpt
        _ = (4 * ‖w - s‖ / (n : ℝ) ^ 2) * ∑ z ∈ F_n, (IEANTN.zetaOrder z : ℝ) :=
            (Finset.mul_sum _ _ _).symm
        _ ≤ (4 * ‖w - s‖ / (n : ℝ) ^ 2) * (336 * Real.log (n : ℝ)) :=
            mul_le_mul_of_nonneg_left hband (by positivity)
        _ ≤ (4 * ‖w - s‖ / (n : ℝ) ^ 2) * (336 * (2 * (n : ℝ) ^ (1 / 2 : ℝ))) :=
            mul_le_mul_of_nonneg_left (by linarith) (by positivity)
        _ = (2688 * ‖w - s‖) * ((n : ℝ) ^ (1 / 2 : ℝ) / (n : ℝ) ^ 2) := by ring
        _ = (2688 * ‖w - s‖) * (1 / (n : ℝ) ^ (3 / 2 : ℝ)) := by rw [hrpow_id]
    calc ∑ n ∈ Finset.Ico N₀ M_sup, ∑ z ∈ T_high with Nat.floor |z.im| = n, termC z
        ≤ ∑ n ∈ Finset.Ico N₀ M_sup, (2688 * ‖w - s‖) * (1 / (n : ℝ) ^ (3 / 2 : ℝ)) :=
          Finset.sum_le_sum hfiber
      _ ≤ B_high :=
          hp_sum.sum_le_tsum (Finset.Ico N₀ M_sup) (fun _ _ ↦ by positivity)
  linarith

/-! ### Pigeonhole gap selection and Borel-Caratheodory horizontal bound -/

/-- General finite pigeonhole lemma: given a `K`-element set of forbidden centers `vals : α → ℝ`
and `K + 1` grid points separated by `2 * δ`, at least one grid point avoids all `(vals u - δ, vals u + δ)`. -/
private lemma exists_grid_avoiding {α : Type*} [DecidableEq α] (A : Finset α) (vals : α → ℝ)
    (a δ : ℝ) (hδ : 0 < δ) :
    ∃ j ∈ Finset.range (A.card + 1),
      ∀ u ∈ A, δ ≤ |vals u - (a + (2 * (j : ℝ) + 1) * δ)| := by
  classical
  set K := A.card
  set grid := Finset.range (K + 1)
  set pt : ℕ → ℝ := fun j ↦ a + (2 * (j : ℝ) + 1) * δ
  set bad : Finset ℕ := A.biUnion (fun u ↦ grid.filter (fun j ↦ |vals u - pt j| < δ))
  have hcard_each : ∀ u ∈ A, (grid.filter (fun j ↦ |vals u - pt j| < δ)).card ≤ 1 := by
    intro u _
    refine Finset.card_le_one.mpr fun j₁ hj₁ j₂ hj₂ ↦ ?_
    have h1 : |vals u - pt j₁| < δ := (Finset.mem_filter.mp hj₁).2
    have h2 : |vals u - pt j₂| < δ := (Finset.mem_filter.mp hj₂).2
    by_contra hne
    have hsep : 2 * δ ≤ |pt j₁ - pt j₂| := by
      have hsub : pt j₁ - pt j₂ = 2 * ((j₁ : ℝ) - (j₂ : ℝ)) * δ := by simp only [pt]; ring
      rw [hsub, abs_mul, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2), abs_of_pos hδ]
      have hij : (1 : ℝ) ≤ |(j₁ : ℝ) - (j₂ : ℝ)| := by
        rcases lt_or_gt_of_ne hne with hlt | hgt
        · have : (j₁ : ℝ) + 1 ≤ (j₂ : ℝ) := by exact_mod_cast Nat.succ_le_of_lt hlt
          rw [abs_of_neg (by linarith)]; linarith
        · have : (j₂ : ℝ) + 1 ≤ (j₁ : ℝ) := by exact_mod_cast Nat.succ_le_of_lt hgt
          rw [abs_of_pos (by linarith)]; linarith
      nlinarith
    have htri : |pt j₁ - pt j₂| ≤ |vals u - pt j₁| + |vals u - pt j₂| := by
      rw [show pt j₁ - pt j₂ = (vals u - pt j₂) - (vals u - pt j₁) by ring]
      exact (abs_sub _ _).trans_eq (add_comm _ _)
    linarith
  have hbad_lt : bad.card < grid.card := by
    calc bad.card ≤ ∑ u ∈ A, (grid.filter (fun j ↦ |vals u - pt j| < δ)).card :=
          Finset.card_biUnion_le
      _ ≤ ∑ _u ∈ A, 1 := Finset.sum_le_sum hcard_each
      _ = K := by simp [K]
      _ < K + 1 := Nat.lt_succ_self K
      _ = grid.card := (Finset.card_range (K + 1)).symm
  obtain ⟨j, hj_grid, hj_not⟩ := Finset.exists_mem_notMem_of_card_lt_card hbad_lt
  refine ⟨j, hj_grid, fun u hu ↦ not_lt.mp fun hlt ↦ hj_not ?_⟩
  exact Finset.mem_biUnion.mpr ⟨u, hu, Finset.mem_filter.mpr ⟨hj_grid, hlt⟩⟩

private lemma one_le_log_of_twelve_le {N : ℕ} (hN : 12 ≤ N) : 1 ≤ Real.log (N : ℝ) := by
  have he : Real.exp 1 ≤ (N : ℝ) := by
    have h3 : Real.exp 1 ≤ 3 := le_of_lt Real.exp_one_lt_d9 |>.trans (by norm_num)
    have h12 : (12 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
    linarith
  have hlog := Real.log_le_log (Real.exp_pos 1) he
  rwa [Real.log_exp] at hlog

private lemma log_le_two_log_of_le_two_mul {x : ℝ} {N : ℕ} (hx : 1 ≤ x) (hN : 12 ≤ N)
    (hle : x ≤ 2 * (N : ℝ)) : Real.log x ≤ 2 * Real.log (N : ℝ) := by
  have hN1 : 1 ≤ Real.log (N : ℝ) := one_le_log_of_twelve_le hN
  have hN_pos : (0 : ℝ) < (N : ℝ) := by
    have : (12 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
    linarith
  have hlog2 : Real.log 2 ≤ 1 := by
    have h := Real.add_one_le_exp (1 : ℝ)
    have hlt := Real.log_le_log (by norm_num) h
    rw [Real.log_exp, show (1 : ℝ) + 1 = 2 by norm_num] at hlt
    exact hlt
  calc Real.log x ≤ Real.log (2 * (N : ℝ)) := Real.log_le_log (by linarith) hle
    _ = Real.log 2 + Real.log (N : ℝ) := Real.log_mul (by norm_num) hN_pos.ne'
    _ ≤ 1 + Real.log (N : ℝ) := by linarith
    _ ≤ 2 * Real.log (N : ℝ) := by linarith

private lemma eqOn_of_codiscreteWithin_open {U : Set ℂ} (hU : IsOpen U) {f₁ f₂ : ℂ → ℂ}
    (hf₁ : ContinuousOn f₁ U) (hf₂ : ContinuousOn f₂ U)
    (heq : f₁ =ᶠ[codiscreteWithin U] f₂) : Set.EqOn f₁ f₂ U := by
  intro x hx
  have hne : f₁ =ᶠ[𝓝[≠] x] f₂ := by
    filter_upwards [(eventuallyEq_codiscreteWithin_iff_forall_eventually_nhdsNE.mp heq x hx),
      nhdsWithin_le_nhds (hU.mem_nhds hx)] with y hy hyU
    exact hy hyU
  have hc1 : ContinuousAt f₁ x := hf₁.continuousAt (hU.mem_nhds hx)
  have hc2 : ContinuousAt f₂ x := hf₂.continuousAt (hU.mem_nhds hx)
  exact tendsto_nhds_unique (hc1.tendsto.mono_left nhdsWithin_le_nhds)
    ((hc2.tendsto.mono_left nhdsWithin_le_nhds).congr' hne.symm)

private lemma norm_blaschke_num_eq_on_sphere {c u z : ℂ} {R : ℝ} (hR : 0 < R)
    (hz : z ∈ Metric.sphere c R) :
    ‖((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c)) / (R : ℂ)‖ = ‖z - u‖ := by
  have hzR : ‖z - c‖ = R := by simpa [dist_eq_norm] using hz
  have hconj : (z - c) * starRingEnd ℂ (z - c) = (R : ℂ) ^ 2 := by
    rw [Complex.mul_conj', hzR]
  have hid : (R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c)
      = (z - c) * starRingEnd ℂ (z - u) := by
    rw [← hconj, show z - u = (z - c) - (u - c) by ring]
    simp only [map_sub]
    ring
  rw [hid, norm_div, norm_mul, RCLike.norm_conj, hzR, Complex.norm_real,
    Real.norm_of_nonneg hR.le, mul_div_cancel_left₀ _ hR.ne']

/-- Selection of good horizontal ordinates `T_N ∈ [N + 1/4, N + 3/4]` with `‖F(σ + i T_N)‖ ≤ C (log N)^2`
uniformly on `σ ∈ [-1/8, 2]`. -/
theorem exists_good_ordinate :
    ∃ C_H : ℝ, 0 ≤ C_H ∧ ∀ N : ℕ, 12 ≤ N →
      ∃ T : ℝ, (N : ℝ) + 1 / 4 ≤ T ∧ T ≤ (N : ℝ) + 3 / 4 ∧
        (∀ z : ℂ, |z.im| = T → riemannZeta z ≠ 0) ∧
        (∀ σ ∈ Set.Icc (-1 / 8 : ℝ) 2,
          ‖F ((σ : ℂ) + (T : ℂ) * I)‖ ≤ C_H * (Real.log (N : ℝ)) ^ 2) := by
  classical
  refine ⟨7250000, by norm_num, fun N hN ↦ ?_⟩
  have hN_real : (12 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hlogN1 : 1 ≤ Real.log (N : ℝ) := one_le_log_of_twelve_le hN
  -- Step 1: Collect all zeros of `riemannZeta₁` in `[0, 1] × [N - 3, N + 4]`.
  set box : Set ℂ := Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc ((N : ℝ) - 3) ((N : ℝ) + 4)
  have hbox_fin : {z ∈ box | riemannZeta₁ z = 0}.Finite :=
    finite_zeros_riemannZeta₁_of_isCompact (isCompact_Icc.reProdIm isCompact_Icc)
  set Z_box : Finset ℂ := hbox_fin.toFinset
  have hZ_mem : ∀ z : ℂ, riemannZeta₁ z = 0 →
      (N : ℝ) - 3 ≤ z.im → z.im ≤ (N : ℝ) + 4 → z ∈ Z_box := by
    intro z hz1 him1 him2
    rw [hbox_fin.mem_toFinset]
    refine ⟨⟨?_, him1, him2⟩, hz1⟩
    rcases riemannZeta₁_eq_zero_iff.mp hz1 with ⟨⟨h0, h1⟩, -, -⟩ | ⟨k, rfl⟩
    · exact ⟨h0.le, h1.le⟩
    · simp at him1; linarith
  have hZ_mult : ∑ u ∈ Z_box, (IEANTN.zetaOrder u : ℝ) ≤ 1344 * Real.log (N : ℝ) := by
    set B₁ := Z_box.filter (fun u ↦ |u.im - ((N : ℝ) - 2)| ≤ 1)
    set B₂ := Z_box.filter (fun u ↦ |u.im - (N : ℝ)| ≤ 1)
    set B₃ := Z_box.filter (fun u ↦ |u.im - ((N : ℝ) + 2)| ≤ 1)
    set B₄ := Z_box.filter (fun u ↦ |u.im - ((N : ℝ) + 3)| ≤ 1)
    have hcov : Z_box ⊆ B₁ ∪ B₂ ∪ B₃ ∪ B₄ := by
      intro u hu
      obtain ⟨⟨_, him1, him2⟩, _⟩ := hbox_fin.mem_toFinset.mp hu
      simp only [Finset.mem_union, Finset.mem_filter, hu, true_and, B₁, B₂, B₃, B₄]
      by_cases h1 : u.im ≤ (N : ℝ) - 1
      · left; left; left; exact abs_le.mpr ⟨by linarith, by linarith⟩
      · by_cases h2 : u.im ≤ (N : ℝ) + 1
        · left; left; right; exact abs_le.mpr ⟨by linarith, by linarith⟩
        · by_cases h3 : u.im ≤ (N : ℝ) + 3
          · left; right; exact abs_le.mpr ⟨by linarith, by linarith⟩
          · right; exact abs_le.mpr ⟨by linarith, by linarith⟩
    have hnonneg : ∀ u : ℂ, u ∈ Z_box → 0 ≤ (IEANTN.zetaOrder u : ℝ) := by
      intro u hu
      obtain ⟨⟨_, him1, _⟩, hz1⟩ := hbox_fin.mem_toFinset.mp hu
      have hu1 : u ≠ 1 := fun h ↦ by rw [h] at him1; simp at him1; linarith
      exact_mod_cast le_trans zero_le_one
        (zetaOrder_pos_of_zeta_eq_zero hu1 ((riemannZeta_eq_zero_iff_riemannZeta₁ hu1).mpr hz1))
    have hb1 : ∑ u ∈ B₁, (IEANTN.zetaOrder u : ℝ) ≤ 336 * Real.log (N : ℝ) := by
      have h := sum_zetaOrder_band_le (T := (N : ℝ) - 2) (by linarith) B₁ fun u hu ↦ by
        have hm := Finset.mem_filter.mp hu
        exact ⟨(hbox_fin.mem_toFinset.mp hm.1).1.1, hm.2⟩
      have hlog := log_le_two_log_of_le_two_mul (x := (N : ℝ) - 2) (by linarith) hN (by linarith)
      linarith
    have hb2 : ∑ u ∈ B₂, (IEANTN.zetaOrder u : ℝ) ≤ 336 * Real.log (N : ℝ) := by
      have h := sum_zetaOrder_band_le (T := (N : ℝ)) (by linarith) B₂ fun u hu ↦ by
        have hm := Finset.mem_filter.mp hu
        exact ⟨(hbox_fin.mem_toFinset.mp hm.1).1.1, hm.2⟩
      linarith [Real.log_nonneg (by linarith : (1 : ℝ) ≤ (N : ℝ))]
    have hb3 : ∑ u ∈ B₃, (IEANTN.zetaOrder u : ℝ) ≤ 336 * Real.log (N : ℝ) := by
      have h := sum_zetaOrder_band_le (T := (N : ℝ) + 2) (by linarith) B₃ fun u hu ↦ by
        have hm := Finset.mem_filter.mp hu
        exact ⟨(hbox_fin.mem_toFinset.mp hm.1).1.1, hm.2⟩
      have hlog := log_le_two_log_of_le_two_mul (x := (N : ℝ) + 2) (by linarith) hN (by linarith)
      linarith
    have hb4 : ∑ u ∈ B₄, (IEANTN.zetaOrder u : ℝ) ≤ 336 * Real.log (N : ℝ) := by
      have h := sum_zetaOrder_band_le (T := (N : ℝ) + 3) (by linarith) B₄ fun u hu ↦ by
        have hm := Finset.mem_filter.mp hu
        exact ⟨(hbox_fin.mem_toFinset.mp hm.1).1.1, hm.2⟩
      have hlog := log_le_two_log_of_le_two_mul (x := (N : ℝ) + 3) (by linarith) hN (by linarith)
      linarith
    have hsub := Finset.sum_le_sum_of_subset_of_nonneg hcov (fun u hu _ ↦ by
      rcases Finset.mem_union.mp hu with h123 | h4
      · rcases Finset.mem_union.mp h123 with h12 | h3
        · rcases Finset.mem_union.mp h12 with h1 | h2
          · exact hnonneg u (Finset.mem_filter.mp h1).1
          · exact hnonneg u (Finset.mem_filter.mp h2).1
        · exact hnonneg u (Finset.mem_filter.mp h3).1
      · exact hnonneg u (Finset.mem_filter.mp h4).1)
    have hunion1 : ∑ u ∈ B₁ ∪ B₂ ∪ B₃ ∪ B₄, (IEANTN.zetaOrder u : ℝ)
        ≤ (∑ u ∈ B₁, (IEANTN.zetaOrder u : ℝ)) + (∑ u ∈ B₂, (IEANTN.zetaOrder u : ℝ))
          + (∑ u ∈ B₃, (IEANTN.zetaOrder u : ℝ)) + ∑ u ∈ B₄, (IEANTN.zetaOrder u : ℝ) := by
      have sum_u_le : ∀ s₁ s₂ : Finset ℂ, (∀ u ∈ s₂, 0 ≤ (IEANTN.zetaOrder u : ℝ)) →
          ∑ u ∈ s₁ ∪ s₂, (IEANTN.zetaOrder u : ℝ)
            ≤ (∑ u ∈ s₁, (IEANTN.zetaOrder u : ℝ)) + ∑ u ∈ s₂, (IEANTN.zetaOrder u : ℝ) := by
        intro s₁ s₂ hs₂
        have hu := Finset.sum_union_inter (s₁ := s₁) (s₂ := s₂)
          (f := fun u ↦ (IEANTN.zetaOrder u : ℝ))
        have hnn : 0 ≤ ∑ u ∈ s₁ ∩ s₂, (IEANTN.zetaOrder u : ℝ) :=
          Finset.sum_nonneg fun u hu' ↦ hs₂ u (Finset.mem_inter.mp hu').2
        linarith only [hu, hnn]
      have u1 := sum_u_le (B₁ ∪ B₂ ∪ B₃) B₄
        (fun u hu ↦ hnonneg u (Finset.mem_filter.mp hu).1)
      have u2 := sum_u_le (B₁ ∪ B₂) B₃
        (fun u hu ↦ hnonneg u (Finset.mem_filter.mp hu).1)
      have u3 := sum_u_le B₁ B₂
        (fun u hu ↦ hnonneg u (Finset.mem_filter.mp hu).1)
      linarith only [u1, u2, u3]
    linarith
  set K : ℕ := Z_box.card
  have hK_le : (K : ℝ) ≤ 1344 * Real.log (N : ℝ) := by
    have h1 : (K : ℝ) = ∑ _u ∈ Z_box, (1 : ℝ) := by simp [K]
    rw [h1]
    refine le_trans (Finset.sum_le_sum fun u hu ↦ ?_) hZ_mult
    obtain ⟨⟨_, him1, _⟩, hz1⟩ := hbox_fin.mem_toFinset.mp hu
    have hu1 : u ≠ 1 := fun h ↦ by rw [h] at him1; simp at him1; linarith
    exact_mod_cast zetaOrder_pos_of_zeta_eq_zero hu1
      ((riemannZeta_eq_zero_iff_riemannZeta₁ hu1).mpr hz1)
  -- Step 2: Pigeonhole choice of `T ∈ [N + 1/4, N + 3/4]` avoiding `Z_box` ordinates.
  set δ_T : ℝ := 1 / (4 * ((K : ℝ) + 1))
  have hδ_T_pos : 0 < δ_T := by positivity
  obtain ⟨j₀, hj₀_mem, hj₀_gap⟩ := exists_grid_avoiding Z_box Complex.im ((N : ℝ) + 1 / 4) δ_T hδ_T_pos
  set T : ℝ := (N : ℝ) + 1 / 4 + (2 * (j₀ : ℝ) + 1) * δ_T with hT_def
  have hj₀_lt : (j₀ : ℝ) + 1 ≤ (K : ℝ) + 1 := by
    exact_mod_cast Nat.succ_le_of_lt (Finset.mem_range.mp hj₀_mem)
  have hT_lo : (N : ℝ) + 1 / 4 ≤ T := by
    have : 0 ≤ (2 * (j₀ : ℝ) + 1) * δ_T := by positivity
    linarith [hT_def]
  have hT_hi : T ≤ (N : ℝ) + 3 / 4 := by
    have hnum : (2 * (j₀ : ℝ) + 1) ≤ 2 * ((K : ℝ) + 1) := by linarith
    have hprod : (2 * (j₀ : ℝ) + 1) * δ_T ≤ 1 / 2 := by
      simp only [δ_T]
      rw [mul_one_div, div_le_div_iff₀ (by positivity) (by norm_num)]
      linarith
    linarith [hT_def]
  have hgap_all : ∀ z : ℂ, riemannZeta₁ z = 0 → δ_T ≤ |(|z.im| - T)| := by
    intro z hz1
    by_cases hband : (N : ℝ) - 3 ≤ |z.im| ∧ |z.im| ≤ (N : ℝ) + 4
    · by_cases hpos : 0 ≤ z.im
      · have hz_in : z ∈ Z_box := by
          rw [abs_of_nonneg hpos] at hband
          exact hZ_mem z hz1 hband.1 hband.2
        simpa [abs_of_nonneg hpos, T] using hj₀_gap z hz_in
      · have hneg : z.im < 0 := not_le.mp hpos
        have hcz1 : riemannZeta₁ (starRingEnd ℂ z) = 0 := by rw [riemannZeta₁_conj, hz1, map_zero]
        have hcz_im : (starRingEnd ℂ z).im = |z.im| := by simp [abs_of_neg hneg]
        have hz_in : starRingEnd ℂ z ∈ Z_box :=
          hZ_mem _ hcz1 (by linarith [hband.1]) (by linarith [hband.2])
        have hg := hj₀_gap (starRingEnd ℂ z) hz_in
        rwa [hcz_im] at hg
    · have hfar : (2 : ℝ) ≤ |(|z.im| - T)| := by
        by_cases h1 : (N : ℝ) - 3 ≤ |z.im|
        · have h2 : (N : ℝ) + 4 < |z.im| := not_le.mp (fun hc ↦ hband ⟨h1, hc⟩)
          rw [abs_of_nonneg (by linarith)]; linarith
        · have h2 : |z.im| < (N : ℝ) - 3 := not_le.mp h1
          rw [abs_of_neg (by linarith)]; linarith
      have hδ_le : δ_T ≤ 1 / 4 := by
        simp only [δ_T]
        exact one_div_le_one_div_of_le (by norm_num)
          (by have : (0 : ℝ) ≤ K := Nat.cast_nonneg K; linarith)
      linarith
  have hT_zfree : ∀ z : ℂ, |z.im| = T → riemannZeta z ≠ 0 := by
    intro z hzim hz0
    have hzne1 : z ≠ 1 := fun h ↦ by rw [h] at hzim; simp at hzim; linarith
    have hz1 : riemannZeta₁ z = 0 := (riemannZeta_eq_zero_iff_riemannZeta₁ hzne1).mp hz0
    have hg := hgap_all z hz1
    rw [hzim, sub_self, abs_zero] at hg
    linarith
  -- Step 3: Pigeonhole choice of outer radius `(R, R')` in `[47/20, 12/5]` avoiding `Z_box` distances.
  set c : ℂ := (2 : ℂ) + (T : ℂ) * I
  set δ_R : ℝ := 1 / (40 * ((K : ℝ) + 1))
  have hδ_R_pos : 0 < δ_R := by positivity
  obtain ⟨j₁, hj₁_mem, hj₁_gap⟩ :=
    exists_grid_avoiding Z_box (fun u ↦ ‖u - c‖) (47 / 20 : ℝ) δ_R hδ_R_pos
  set R : ℝ := (47 / 20 : ℝ) + (2 * (j₁ : ℝ) + 1) * δ_R with hR_def
  set R' : ℝ := R + δ_R / 2 with hR'_def
  have hj₁_lt : (j₁ : ℝ) + 1 ≤ (K : ℝ) + 1 := by
    exact_mod_cast Nat.succ_le_of_lt (Finset.mem_range.mp hj₁_mem)
  have hR_lo : (47 / 20 : ℝ) ≤ R := by
    have : 0 ≤ (2 * (j₁ : ℝ) + 1) * δ_R := by positivity
    linarith [hR_def]
  have hR'_hi : R' ≤ 12 / 5 := by
    have hprod : (2 * (j₁ : ℝ) + 3 / 2) * δ_R ≤ 1 / 20 := by
      simp only [δ_R]
      rw [mul_one_div, div_le_div_iff₀ (by positivity) (by norm_num)]
      linarith
    linarith [hR_def, hR'_def]
  have hRR' : R < R' := by linarith [hR'_def]
  have hR_pos : 0 < R := by linarith
  have hannulus_zfree : ∀ u : ℂ, riemannZeta₁ u = 0 → ‖u - c‖ < R' → ‖u - c‖ < R := by
    intro u hu1 huR'
    have hu_im : (N : ℝ) - 3 ≤ u.im ∧ u.im ≤ (N : ℝ) + 4 := by
      have him : |u.im - T| ≤ ‖u - c‖ := by
        simpa [c, Complex.sub_im] using Complex.abs_im_le_norm (u - c)
      have h1 := abs_le.mp (him.trans (huR'.le.trans hR'_hi))
      exact ⟨by linarith, by linarith⟩
    have hu_in : u ∈ Z_box := hZ_mem u hu1 hu_im.1 hu_im.2
    have hg : δ_R ≤ |‖u - c‖ - R| := hj₁_gap u hu_in
    by_contra hnot
    have hge : R ≤ ‖u - c‖ := not_lt.mp hnot
    rw [abs_of_nonneg (by linarith)] at hg
    linarith [hR'_def]
  -- Step 4: Factorize `riemannZeta₁` on `U' = ball c R'` and construct Blaschke reflection `h`.
  set U' : Set ℂ := Metric.ball c R'
  have hU'_open : IsOpen U' := Metric.isOpen_ball
  have hmU' : MeromorphicOn riemannZeta₁ U' :=
    (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ U')).meromorphicOn
  set D := MeromorphicOn.divisor riemannZeta₁ U'
  have hD_fin : D.support.Finite :=
    (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ (Metric.closedBall c R'))).meromorphicOn.divisor_ball_support_finite
  set S : Finset ℂ := hD_fin.toFinset
  have hS_props : ∀ u ∈ S, u ∈ Z_box ∧ ‖u - c‖ < R ∧ 1 ≤ D u ∧ ((D u).toNat : ℤ) = D u := by
    intro u hu
    have hsupp : u ∈ D.support := hD_fin.mem_toFinset.mp hu
    obtain ⟨huU', hu1⟩ := riemannZeta₁_eq_zero_of_mem_divisor_support hsupp
    have huR' : ‖u - c‖ < R' := by simpa [U', dist_eq_norm] using huU'
    have huR : ‖u - c‖ < R := hannulus_zfree u hu1 huR'
    have him : |u.im - T| ≤ ‖u - c‖ := by
      simpa [c, Complex.sub_im] using Complex.abs_im_le_norm (u - c)
    have h1 := abs_le.mp (him.trans (huR.le.trans (hRR'.le.trans hR'_hi)))
    have hu_box : u ∈ Z_box := hZ_mem u hu1 (by linarith) (by linarith)
    have hpos : 1 ≤ D u := divisor_riemannZeta₁_pos_of_mem_support hsupp
    exact ⟨hu_box, huR, hpos, Int.toNat_of_nonneg (by omega)⟩
  have hS_mult : ∑ u ∈ S, ((D u).toNat : ℝ) ≤ 1344 * Real.log (N : ℝ) := by
    have hsub : S ⊆ Z_box := fun u hu ↦ (hS_props u hu).1
    have heq : ∑ u ∈ S, ((D u).toNat : ℝ) = ∑ u ∈ S, (IEANTN.zetaOrder u : ℝ) := by
      refine Finset.sum_congr rfl fun u hu ↦ ?_
      have hsupp : u ∈ D.support := hD_fin.mem_toFinset.mp hu
      obtain ⟨huU', _⟩ := riemannZeta₁_eq_zero_of_mem_divisor_support hsupp
      obtain ⟨hu_box, _, _, hnat⟩ := hS_props u hu
      obtain ⟨⟨_, him1, _⟩, _⟩ := hbox_fin.mem_toFinset.mp hu_box
      have hu1 : u ≠ 1 := fun h ↦ by rw [h] at him1; simp at him1; linarith
      have hd := divisor_riemannZeta₁_eq_zetaOrder huU' hu1
      exact_mod_cast (hnat.trans hd)
    rw [heq]
    refine le_trans (Finset.sum_le_sum_of_subset_of_nonneg hsub fun u hu _ ↦ ?_) hZ_mult
    obtain ⟨⟨_, him1, _⟩, hz1⟩ := hbox_fin.mem_toFinset.mp hu
    have hu1 : u ≠ 1 := fun h ↦ by rw [h] at him1; simp at him1; linarith
    exact_mod_cast le_trans zero_le_one
      (zetaOrder_pos_of_zeta_eq_zero hu1 ((riemannZeta_eq_zero_iff_riemannZeta₁ hu1).mpr hz1))
  obtain ⟨g, hg_an, hg_ne, heq_cod⟩ := hmU'.extract_zeros_poles
    (fun u ↦ meromorphicOrderAt_riemannZeta₁_ne_top u.1) hD_fin
  have hprod_eq : (∏ᶠ u, (· - u) ^ D u) = fun z : ℂ ↦ ∏ u ∈ S, (z - u) ^ (D u).toNat := by
    rw [finprod_eq_prod_of_mulSupport_subset _ (s := S) (fun u hu ↦ by
      rw [Finset.mem_coe, hD_fin.mem_toFinset, Function.mem_support]
      intro h0
      exact hu (by simp [h0]))]
    funext z
    rw [Finset.prod_apply]
    refine Finset.prod_congr rfl fun u hu ↦ ?_
    conv_lhs => rw [← (hS_props u hu).2.2.2, zpow_natCast, Pi.pow_apply]
  have hfact : ∀ z ∈ U', riemannZeta₁ z = (∏ u ∈ S, (z - u) ^ (D u).toNat) * g z := by
    refine eqOn_of_codiscreteWithin_open hU'_open
      (analyticOnNhd_riemannZeta₁.mono (Set.subset_univ U')).continuousOn
      ((by fun_prop : ContinuousOn (fun z ↦ ∏ u ∈ S, (z - u) ^ (D u).toNat) U').mul
        hg_an.continuousOn) ?_
    filter_upwards [heq_cod] with z hz
    rw [show MeromorphicOn.divisor riemannZeta₁ U' = D from rfl, hprod_eq] at hz
    simpa [smul_eq_mul] using hz
  -- Construct Blaschke reflection `h`.
  set bfac : ℂ → ℂ → ℂ := fun u z ↦
    ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c)) / (R : ℂ)
  set h : ℂ → ℂ := fun z ↦ (∏ u ∈ S, (bfac u z) ^ (D u).toNat) * g z
  have hh_diff : DifferentiableOn ℂ h U' :=
    ((by dsimp only [bfac]; fun_prop :
      Differentiable ℂ (fun z ↦ ∏ u ∈ S, (bfac u z) ^ (D u).toNat)).differentiableOn).mul
        hg_an.differentiableOn
  have hbfac_ne : ∀ u ∈ S, ∀ z ∈ Metric.ball c R, bfac u z ≠ 0 := by
    intro u hu z hz
    have huR : ‖u - c‖ < R := (hS_props u hu).2.1
    have hzR : ‖z - c‖ < R := by simpa [dist_eq_norm] using hz
    have hprod_lt : ‖starRingEnd ℂ (u - c) * (z - c)‖ < ‖((R : ℂ) ^ 2)‖ := by
      rw [norm_mul, RCLike.norm_conj, norm_pow, Complex.norm_real, Real.norm_of_nonneg hR_pos.le, sq]
      exact mul_lt_mul'' huR hzR (norm_nonneg _) (norm_nonneg _)
    have hnum_ne : (R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c) ≠ 0 := by
      intro h0
      rw [sub_eq_zero.mp h0] at hprod_lt
      exact lt_irrefl _ hprod_lt
    exact div_ne_zero hnum_ne (Complex.ofReal_ne_zero.mpr hR_pos.ne')
  have hh_ne : ∀ z ∈ Metric.ball c R, h z ≠ 0 := by
    intro z hz
    have hzU' : z ∈ U' := Metric.ball_subset_ball hRR'.le hz
    refine mul_ne_zero (Finset.prod_ne_zero_iff.mpr fun u hu ↦ ?_) (hg_ne ⟨z, hzU'⟩)
    exact pow_ne_zero _ (hbfac_ne u hu z hz)
  have hh_bound : ∀ z ∈ Metric.ball c R, ‖h z‖ ≤ T ^ 7 := by
    intro z hz
    refine Complex.norm_le_of_forall_mem_frontier_norm_le Metric.isBounded_ball
      (hh_diff.diffContOnCl_ball (Metric.closedBall_subset_ball hRR')) (fun w hw ↦ ?_)
      (subset_closure hz)
    have hws : w ∈ Metric.sphere c R := by
      have hcl : dist w c ≤ R := Metric.mem_closedBall.mp
        (Metric.isClosed_closedBall.closure_subset_iff.mpr Metric.ball_subset_closedBall hw.1)
      have hnot : ¬ dist w c < R := by
        simpa [Metric.isOpen_ball.interior_eq, Metric.mem_ball] using hw.2
      exact Metric.mem_sphere.mpr (le_antisymm hcl (not_lt.mp hnot))
    have hwU' : w ∈ U' := by
      rw [Metric.mem_ball]
      have hd : dist w c = R := hws
      linarith only [hd, hRR']
    have hnorm_eq : ‖h w‖ = ‖riemannZeta₁ w‖ := by
      simp only [h, hfact w hwU', norm_mul, norm_prod]
      refine congrArg (· * ‖g w‖) (Finset.prod_congr rfl fun u _ ↦ ?_)
      rw [norm_pow, norm_pow, norm_blaschke_num_eq_on_sphere hR_pos hws]
    rw [hnorm_eq]
    exact norm_riemannZeta₁_le_pow7_on_ball (by linarith only [hN_real, hT_lo])
      (hRR'.le.trans hR'_hi) (Metric.sphere_subset_closedBall hws)
  have hhc_ge : 1 ≤ ‖h c‖ := by
    have hcU' : c ∈ U' := Metric.mem_ball_self (by linarith only [hR_pos, hRR'])
    have hζc : 1 ≤ ‖riemannZeta₁ c‖ :=
      one_le_norm_riemannZeta₁_two_add_im (by linarith only [hN_real, hT_lo])
    rw [hfact c hcU', norm_mul, norm_prod] at hζc
    have hle : (∏ u ∈ S, ‖(c - u) ^ (D u).toNat‖) * ‖g c‖
        ≤ (∏ u ∈ S, ‖(bfac u c) ^ (D u).toNat‖) * ‖g c‖ := by
      refine mul_le_mul_of_nonneg_right (Finset.prod_le_prod₀ (fun _ _ ↦ norm_nonneg _) fun u hu ↦ ?_)
        (norm_nonneg _)
      rw [norm_pow, norm_pow]
      refine pow_le_pow_left₀ (norm_nonneg _) ?_ _
      have huR : ‖u - c‖ < R := (hS_props u hu).2.1
      have hbc : ‖bfac u c‖ = R := by
        simp only [bfac, sub_self, mul_zero, sub_zero]
        rw [norm_div, norm_pow, Complex.norm_real, Real.norm_of_nonneg hR_pos.le, sq,
          mul_div_cancel_left₀ _ hR_pos.ne']
      rw [hbc, norm_sub_rev]
      exact huR.le
    simpa only [h, norm_mul, norm_prod] using hζc.trans hle
  -- Step 5: Primitive `φ` of `logDeriv h` on `ball c R` and Borel-Caratheodory + Cauchy estimate.
  have hld_diff : DifferentiableOn ℂ (logDeriv h) (Metric.ball c R) := by
    have hEq : Set.EqOn (logDeriv h) (fun z ↦ deriv h z / h z) (Metric.ball c R) :=
      fun z _ ↦ logDeriv_apply h z
    have hd_sub : DifferentiableOn ℂ h (Metric.ball c R) :=
      hh_diff.mono (Metric.ball_subset_ball hRR'.le)
    exact ((hd_sub.deriv Metric.isOpen_ball).div hd_sub hh_ne).congr hEq
  obtain ⟨φ, hφc, hφ_deriv⟩ := hld_diff.isExactOn_ball.with_val_at c 0
  have hφ_diff : DifferentiableOn ℂ φ (Metric.ball c R) :=
    fun z hz ↦ (hφ_deriv z hz).differentiableAt.differentiableWithinAt
  have hh_exp : ∀ z ∈ Metric.ball c R, h z = h c * Complex.exp (φ z) := by
    have hexp_diff : DifferentiableOn ℂ (fun z ↦ Complex.exp (φ z)) (Metric.ball c R) :=
      Complex.differentiable_exp.comp_differentiableOn hφ_diff
    have hld_eq : Set.EqOn (logDeriv h) (logDeriv (fun z ↦ Complex.exp (φ z))) (Metric.ball c R) := by
      intro z hz
      have hd : HasDerivAt (fun w ↦ Complex.exp (φ w)) (Complex.exp (φ z) * logDeriv h z) z :=
        (Complex.hasDerivAt_exp (φ z)).comp z (hφ_deriv z hz)
      rw [logDeriv_apply (fun w ↦ Complex.exp (φ w)) z, hd.deriv,
        mul_div_cancel_left₀ _ (Complex.exp_ne_zero _)]
    obtain ⟨C₀, _, hC₀_eq⟩ := (logDeriv_eqOn_iff (hh_diff.mono (Metric.ball_subset_ball hRR'.le))
      hexp_diff Metric.isOpen_ball (convex_ball c R).isPreconnected
      (fun z _ ↦ Complex.exp_ne_zero _) hh_ne).mp hld_eq
    have hc_mem : c ∈ Metric.ball c R := Metric.mem_ball_self hR_pos
    have hC₀_val : h c = C₀ := by
      have := hC₀_eq hc_mem
      simpa [hφc] using this
    intro z hz
    simpa [← hC₀_val, smul_eq_mul] using hC₀_eq hz
  have hφ_re : ∀ z ∈ Metric.ball c R, (φ z).re ≤ 7 * Real.log T := by
    intro z hz
    have hexp_eq : ‖h c‖ * Real.exp (φ z).re = ‖h z‖ := by
      conv_rhs => rw [hh_exp z hz, norm_mul, Complex.norm_exp]
    have hexp_le : Real.exp (φ z).re ≤ T ^ 7 := by
      calc Real.exp (φ z).re = 1 * Real.exp (φ z).re := (one_mul _).symm
        _ ≤ ‖h c‖ * Real.exp (φ z).re := mul_le_mul_of_nonneg_right hhc_ge (Real.exp_pos _).le
        _ = ‖h z‖ := hexp_eq
        _ ≤ T ^ 7 := hh_bound z hz
    have hlog := Real.log_le_log (Real.exp_pos _) hexp_le
    rw [Real.log_exp, Real.log_pow] at hlog
    exact_mod_cast hlog
  have hlogT_pos : 0 < 7 * Real.log T := by
    have h1T : 1 < T := by linarith only [hN_real, hT_lo]
    exact mul_pos (by norm_num) (Real.log_pos h1T)
  have hφ_norm_inner : ∀ z : ℂ, ‖z - c‖ ≤ 9 / 4 → ‖φ z‖ ≤ 315 * Real.log T := by
    intro z hz
    set w := z - c
    have hw_le : ‖w‖ ≤ 9 / 4 := hz
    have hw_ball : w ∈ Metric.ball (0 : ℂ) R := by
      rw [Metric.mem_ball, dist_zero_right]
      linarith only [hw_le, hR_lo]
    have hf_diff : DifferentiableOn ℂ (fun u ↦ φ (c + u)) (Metric.ball 0 R) := by
      refine hφ_diff.comp (by fun_prop) fun u hu ↦ ?_
      simpa [Metric.mem_ball, dist_eq_norm] using hu
    have hf_maps : Set.MapsTo (fun u ↦ φ (c + u)) (Metric.ball 0 R)
        {v : ℂ | v.re ≤ 7 * Real.log T} := by
      intro u hu
      exact hφ_re (c + u) (by simpa [Metric.mem_ball, dist_eq_norm] using hu)
    have hbc := Complex.borelCaratheodory_zero hlogT_pos hf_diff hf_maps hR_pos hw_ball
      (by simp [hφc])
    have hcw : c + w = z := by simp [w]
    rw [hcw] at hbc
    have hden : (1 / 10 : ℝ) ≤ R - ‖w‖ := by linarith only [hw_le, hR_lo]
    calc ‖φ z‖ ≤ 2 * (7 * Real.log T) * ‖w‖ / (R - ‖w‖) := hbc
      _ ≤ 2 * (7 * Real.log T) * (9 / 4) / (1 / 10 : ℝ) := by
          have hnum : 2 * (7 * Real.log T) * ‖w‖ ≤ 2 * (7 * Real.log T) * (9 / 4) :=
            mul_le_mul_of_nonneg_left hw_le (by linarith only [hlogT_pos])
          exact le_trans (div_le_div_of_nonneg_right hnum (by linarith only [hden]))
            (div_le_div_of_nonneg_left
              (by linarith only [hlogT_pos]) (by norm_num) hden)
      _ = 315 * Real.log T := by ring
  -- Step 6: Evaluate horizontal bound on `z₀ = σ + T * I` for `σ ∈ [-1/8, 2]`.
  refine ⟨T, hT_lo, hT_hi, hT_zfree, fun σ hσ ↦ ?_⟩
  set z₀ : ℂ := (σ : ℂ) + (T : ℂ) * I
  have hz₀_sub : z₀ - c = ((σ - 2 : ℝ) : ℂ) := by simp [z₀, c]
  have hz₀_dist : ‖z₀ - c‖ ≤ 17 / 8 := by
    rw [hz₀_sub, Complex.norm_real, Real.norm_eq_abs, abs_of_nonpos (by linarith only [hσ.2])]
    linarith only [hσ.1]
  have hz₀_ball : z₀ ∈ Metric.ball c R := by
    rw [Metric.mem_ball, dist_eq_norm]; linarith only [hz₀_dist, hR_lo]
  have hz₀U' : z₀ ∈ U' := Metric.ball_subset_ball hRR'.le hz₀_ball
  -- Cauchy derivative bound for `logDeriv h z₀ = deriv φ z₀`.
  have hld_h_bound : ‖logDeriv h z₀‖ ≤ 6300 * Real.log (N : ℝ) := by
    have hd_eq : deriv φ z₀ = logDeriv h z₀ := (hφ_deriv z₀ hz₀_ball).deriv
    rw [← hd_eq]
    have hsub_ball : Metric.closedBall z₀ (1 / 10) ⊆ Metric.ball c R := by
      intro z hz
      rw [Metric.mem_closedBall, dist_eq_norm] at hz
      rw [Metric.mem_ball, dist_eq_norm]
      have htri : ‖z - c‖ ≤ ‖z - z₀‖ + ‖z₀ - c‖ := by
        simpa using norm_add_le (z - z₀) (z₀ - c)
      linarith only [hz, hz₀_dist, htri, hR_lo]
    have hcauchy := Complex.norm_deriv_le_of_forall_mem_sphere_norm_le
      (c := z₀) (R := 1 / 10) (C := 315 * Real.log T) (by norm_num)
      (hφ_diff.diffContOnCl_ball hsub_ball)
      (fun z hz ↦ hφ_norm_inner z (by
        have hzs : ‖z - z₀‖ = 1 / 10 := by simpa [dist_eq_norm] using hz
        have htri : ‖z - c‖ ≤ ‖z - z₀‖ + ‖z₀ - c‖ := by
          simpa using norm_add_le (z - z₀) (z₀ - c)
        linarith only [hzs, hz₀_dist, htri]))
    have hlogT_le : Real.log T ≤ 2 * Real.log (N : ℝ) :=
      log_le_two_log_of_le_two_mul (by linarith only [hN_real, hT_lo]) hN
        (by linarith only [hN_real, hT_hi])
    calc ‖deriv φ z₀‖ ≤ (315 * Real.log T) / (1 / 10) := hcauchy
      _ = 3150 * Real.log T := by ring
      _ ≤ 3150 * (2 * Real.log (N : ℝ)) := mul_le_mul_of_nonneg_left hlogT_le (by norm_num)
      _ = 6300 * Real.log (N : ℝ) := by ring
  -- Compare `-F z₀ = logDeriv riemannZeta₁ z₀` with `logDeriv h z₀`.
  have hz₀_ne_u : ∀ u ∈ S, z₀ - u ≠ 0 := by
    intro u hu h0
    have hzeq : z₀ = u := sub_eq_zero.mp h0
    obtain ⟨_, hζ1⟩ := hbox_fin.mem_toFinset.mp (hS_props u hu).1
    have hg := hgap_all u hζ1
    have him0 : z₀.im = T := by simp [z₀]
    have hu_pos : 0 ≤ u.im := by rw [← hzeq, him0]; linarith only [hN_real, hT_lo]
    rw [abs_of_nonneg hu_pos, ← hzeq, him0, sub_self, abs_zero] at hg
    linarith only [hg, hδ_T_pos]
  have hld_zeta : logDeriv riemannZeta₁ z₀
      = (∑ u ∈ S, ((D u).toNat : ℂ) * (1 / (z₀ - u))) + logDeriv g z₀ := by
    have hEq : riemannZeta₁ =ᶠ[𝓝 z₀] (fun z ↦ (∏ u ∈ S, (z - u) ^ (D u).toNat) * g z) := by
      filter_upwards [hU'_open.mem_nhds hz₀U'] with z hz
      exact hfact z hz
    have hprod_fn : (fun z : ℂ ↦ ∏ u ∈ S, (z - u) ^ (D u).toNat)
        = ∏ u ∈ S, (fun z : ℂ ↦ (z - u) ^ (D u).toNat) := by
      funext z; simp [Finset.prod_apply]
    rw [(logDeriv_congr_nhds hEq).eq_of_nhds,
      logDeriv_fun_mul z₀
        (Finset.prod_ne_zero_iff.mpr fun u hu ↦ pow_ne_zero _ (hz₀_ne_u u hu))
        (hg_ne ⟨z₀, hz₀U'⟩)
        (by fun_prop)
        (hg_an z₀ hz₀U').differentiableAt,
      hprod_fn,
      logDeriv_prod (𝕜 := ℂ) (s := S) (f := fun u z ↦ (z - u) ^ (D u).toNat) (x := z₀)
        (fun u hu ↦ pow_ne_zero _ (hz₀_ne_u u hu))
        (fun u _ ↦ by fun_prop)]
    refine congrArg (· + logDeriv g z₀) (Finset.sum_congr rfl fun u _ ↦ ?_)
    rw [logDeriv_fun_pow (𝕜 := ℂ) (f := fun z : ℂ ↦ z - u) (x := z₀) (by fun_prop) (D u).toNat,
      logDeriv_apply (fun z ↦ z - u) z₀]
    have hd : deriv (fun z : ℂ ↦ z - u) z₀ = 1 := by simp
    rw [hd]
  have hld_h : logDeriv h z₀
      = (∑ u ∈ S, ((D u).toNat : ℂ) *
          (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))
        + logDeriv g z₀ := by
    have hprod_bf : (fun z : ℂ ↦ ∏ u ∈ S, (bfac u z) ^ (D u).toNat)
        = ∏ u ∈ S, (fun z : ℂ ↦ (bfac u z) ^ (D u).toNat) := by
      funext z; simp [Finset.prod_apply]
    rw [show h = fun z ↦ (∏ u ∈ S, (bfac u z) ^ (D u).toNat) * g z from rfl,
      logDeriv_fun_mul z₀
        (Finset.prod_ne_zero_iff.mpr fun u hu ↦ pow_ne_zero _ (hbfac_ne u hu z₀ hz₀_ball))
        (hg_ne ⟨z₀, hz₀U'⟩)
        (by dsimp only [bfac]; fun_prop)
        (hg_an z₀ hz₀U').differentiableAt,
      hprod_bf,
      logDeriv_prod (𝕜 := ℂ) (s := S) (f := fun u z ↦ (bfac u z) ^ (D u).toNat) (x := z₀)
        (fun u hu ↦ pow_ne_zero _ (hbfac_ne u hu z₀ hz₀_ball))
        (fun u _ ↦ by dsimp only [bfac]; fun_prop)]
    refine congrArg (· + logDeriv g z₀) (Finset.sum_congr rfl fun u _ ↦ ?_)
    rw [logDeriv_fun_pow (𝕜 := ℂ) (f := bfac u) (x := z₀)
      (by dsimp only [bfac]; fun_prop) (D u).toNat]
    refine congrArg (((D u).toNat : ℂ) * ·) ?_
    have hbf_eq : bfac u = fun z ↦
        ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c)) * ((R : ℂ)⁻¹) := by
      funext z; simp [bfac, div_eq_mul_inv]
    rw [hbf_eq, logDeriv_mul_const z₀ _ (inv_ne_zero (Complex.ofReal_ne_zero.mpr hR_pos.ne')),
      logDeriv_apply]
    have hd : HasDerivAt (fun z : ℂ ↦ (R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z - c))
        (-starRingEnd ℂ (u - c)) z₀ := by
      simpa using (((hasDerivAt_id z₀).sub_const c).const_mul (starRingEnd ℂ (u - c))).const_sub
        ((R : ℂ) ^ 2)
    rw [hd.deriv]
  have hdiff_F : F z₀ = -logDeriv h z₀ - ∑ u ∈ S, ((D u).toNat : ℂ) *
      (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c)))) := by
    simp only [F]
    rw [hld_zeta, hld_h]
    have hsub : ∑ u ∈ S, ((D u).toNat : ℂ) *
        (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) /
          ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c)))) =
        (∑ u ∈ S, ((D u).toNat : ℂ) * (1 / (z₀ - u))) -
        ∑ u ∈ S, ((D u).toNat : ℂ) * (-starRingEnd ℂ (u - c) /
          ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))) := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun _ _ ↦ mul_sub _ _ _
    rw [hsub]
    ring
  have hterm_bound : ∀ u ∈ S,
      ‖((D u).toNat : ℂ) * (1 / (z₀ - u) -
          (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖
        ≤ ((D u).toNat : ℝ) * (5385 * Real.log (N : ℝ)) := by
    intro u hu
    obtain ⟨hu_box, huR, _, _⟩ := hS_props u hu
    have h1_bound : ‖1 / (z₀ - u)‖ ≤ 5380 * Real.log (N : ℝ) := by
      have hg : δ_T ≤ |u.im - T| := hj₀_gap u hu_box
      have hzu_ge : δ_T ≤ ‖z₀ - u‖ := by
        have him_le : |z₀.im - u.im| ≤ ‖z₀ - u‖ := by
          simpa [Complex.sub_im] using Complex.abs_im_le_norm (z₀ - u)
        have hzim : z₀.im = T := by simp [z₀]
        rw [hzim, abs_sub_comm] at him_le
        exact hg.trans him_le
      rw [norm_div, norm_one]
      calc 1 / ‖z₀ - u‖ ≤ 1 / δ_T := one_div_le_one_div_of_le hδ_T_pos hzu_ge
        _ = 4 * ((K : ℝ) + 1) := by simp [δ_T]
        _ ≤ 4 * (1344 * Real.log (N : ℝ) + Real.log (N : ℝ)) := by linarith only [hK_le, hlogN1]
        _ = 5380 * Real.log (N : ℝ) := by ring
    have h2_bound : ‖-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))‖
        ≤ 5 * Real.log (N : ℝ) := by
      have hden_ge : (1 / 2 : ℝ) ≤ ‖(R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c)‖ := by
        have htri := norm_sub_norm_le ((R : ℂ) ^ 2) (starRingEnd ℂ (u - c) * (z₀ - c))
        rw [norm_pow, Complex.norm_real, Real.norm_of_nonneg hR_pos.le, norm_mul,
          RCLike.norm_conj] at htri
        have hprod : ‖u - c‖ * ‖z₀ - c‖ ≤ R * (17 / 8) :=
          mul_le_mul huR.le hz₀_dist (norm_nonneg _) hR_pos.le
        have hquad : (1 / 2 : ℝ) ≤ R ^ 2 - R * (17 / 8) := by
          calc (1 / 2 : ℝ) ≤ (47 / 20 : ℝ) * ((47 / 20 : ℝ) - 17 / 8) := by norm_num
            _ ≤ R * (R - 17 / 8) :=
                mul_le_mul hR_lo (by linarith only [hR_lo]) (by norm_num) hR_pos.le
            _ = R ^ 2 - R * (17 / 8) := by ring
        linarith only [htri, hprod, hquad]
      rw [norm_div, norm_neg, RCLike.norm_conj]
      calc ‖u - c‖ / ‖(R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c)‖
          ≤ (12 / 5 : ℝ) / (1 / 2 : ℝ) := by
            have hu12 : ‖u - c‖ ≤ 12 / 5 := huR.le.trans (hRR'.le.trans hR'_hi)
            exact le_trans (div_le_div_of_nonneg_right hu12 (by norm_num))
              (div_le_div_of_nonneg_left (by norm_num) (by norm_num) hden_ge)
        _ ≤ 5 := by norm_num
        _ ≤ 5 * Real.log (N : ℝ) := by linarith only [hlogN1]
    rw [norm_mul, Complex.norm_natCast]
    refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg _)
    calc ‖1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c)))‖
        ≤ ‖1 / (z₀ - u)‖ +
            ‖-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))‖ :=
          norm_sub_le _ _
      _ ≤ 5380 * Real.log (N : ℝ) + 5 * Real.log (N : ℝ) := add_le_add h1_bound h2_bound
      _ = 5385 * Real.log (N : ℝ) := by ring
  have hsum_bound : ‖∑ u ∈ S, ((D u).toNat : ℂ) *
      (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖
      ≤ 7237440 * (Real.log (N : ℝ)) ^ 2 := by
    calc ‖∑ u ∈ S, _‖
        ≤ ∑ u ∈ S, ‖((D u).toNat : ℂ) *
            (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖ :=
          norm_sum_le S _
      _ ≤ ∑ u ∈ S, ((D u).toNat : ℝ) * (5385 * Real.log (N : ℝ)) :=
          Finset.sum_le_sum hterm_bound
      _ = (∑ u ∈ S, ((D u).toNat : ℝ)) * (5385 * Real.log (N : ℝ)) :=
          (Finset.sum_mul _ _ _).symm
      _ ≤ (1344 * Real.log (N : ℝ)) * (5385 * Real.log (N : ℝ)) :=
          mul_le_mul_of_nonneg_right hS_mult (by linarith only [hlogN1])
      _ = 7237440 * (Real.log (N : ℝ)) ^ 2 := by ring
  rw [hdiff_F]
  calc ‖-logDeriv h z₀ - ∑ u ∈ S, ((D u).toNat : ℂ) *
        (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖
      ≤ ‖-logDeriv h z₀‖ + ‖∑ u ∈ S, ((D u).toNat : ℂ) *
          (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖ :=
        norm_sub_le _ _
    _ = ‖logDeriv h z₀‖ + ‖∑ u ∈ S, ((D u).toNat : ℂ) *
          (1 / (z₀ - u) - (-starRingEnd ℂ (u - c) / ((R : ℂ) ^ 2 - starRingEnd ℂ (u - c) * (z₀ - c))))‖ := by
        rw [norm_neg]
    _ ≤ 6300 * Real.log (N : ℝ) + 7237440 * (Real.log (N : ℝ)) ^ 2 :=
        add_le_add hld_h_bound hsum_bound
    _ ≤ 6300 * (Real.log (N : ℝ)) ^ 2 + 7237440 * (Real.log (N : ℝ)) ^ 2 := by
        have hsq : Real.log (N : ℝ) ≤ (Real.log (N : ℝ)) ^ 2 := by
          rw [sq]
          exact le_mul_of_one_le_right (by linarith only [hlogN1]) hlogN1
        linarith only [hsq]
    _ ≤ 7250000 * (Real.log (N : ℝ)) ^ 2 := by
        have hnn : 0 ≤ (Real.log (N : ℝ)) ^ 2 := sq_nonneg _
        linarith only [hnn]

end ZetaHadamardSolution
