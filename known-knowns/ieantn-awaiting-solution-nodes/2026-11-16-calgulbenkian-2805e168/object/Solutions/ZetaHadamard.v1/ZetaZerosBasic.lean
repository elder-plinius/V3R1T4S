/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: IEANTN contributors
-/
import ResiduePort
import ZetaConjPort
import DigammaTrivial
import IEANTN.Vocabulary.Zeta
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

/-!
# Functional equation, zero classification, and residue formulas for `F = -logDeriv riemannZeta₁`
-/

namespace ZetaHadamardSolution

open scoped Real
open Complex Filter Topology Set

/-- Logarithmic derivative functional equation of `riemannZeta`. -/
theorem logDeriv_riemannZeta_one_sub {s : ℂ} (hsn : ∀ n : ℕ, s ≠ -n) (hs1 : s ≠ 1)
    (hz : riemannZeta s ≠ 0) (hcos : Complex.cos (π * s / 2) ≠ 0) :
    logDeriv riemannZeta s =
      -logDeriv riemannZeta (1 - s) + Complex.log (2 * π) - digamma s
        + π / 2 * Complex.tan (π * s / 2) := by
  have hs0 : s ≠ 0 := by simpa using hsn 0
  have hΓ : Gamma s ≠ 0 := Gamma_ne_zero hsn
  have h2π : (2 * (π : ℂ)) ≠ 0 := mul_ne_zero two_ne_zero (ofReal_ne_zero.mpr Real.pi_ne_zero)
  have hcpow : (2 * (π : ℂ)) ^ (-s) ≠ 0 := by simp [Complex.cpow_eq_zero_iff, h2π]
  have hUopen : IsOpen ({z : ℂ | 1 < z.re} ∪ (Set.range ((↑) : ℤ → ℂ))ᶜ) :=
    (isOpen_lt continuous_const Complex.continuous_re).union
      isClosed_range_intCast.isOpen_compl
  have hsU : s ∈ ({z : ℂ | 1 < z.re} ∪ (Set.range ((↑) : ℤ → ℂ))ᶜ) := by
    by_cases h : s ∈ Set.range ((↑) : ℤ → ℂ)
    · obtain ⟨k, rfl⟩ := h
      refine Or.inl ?_
      have hk0 : 0 < k := by
        by_contra hk
        have hk' : k ≤ 0 := not_lt.mp hk
        obtain ⟨m, rfl⟩ : ∃ m : ℕ, k = -(m : ℤ) := ⟨(-k).toNat, by omega⟩
        exact hsn m (by push_cast; ring)
      have hk1 : k ≠ 1 := fun h => hs1 (by exact_mod_cast h)
      have hk2 : (1 : ℤ) < k := by omega
      simpa using (by exact_mod_cast hk2 : (1 : ℝ) < (k : ℝ))
    · exact Or.inr h
  have hEq : (fun z => riemannZeta (1 - z)) =ᶠ[𝓝 s]
      (fun z => 2 * (2 * π) ^ (-z) * Gamma z * Complex.cos (π * z / 2) * riemannZeta z) := by
    filter_upwards [hUopen.mem_nhds hsU] with z hzU
    rcases hzU with hlt | hnot
    · change 1 < z.re at hlt
      refine riemannZeta_one_sub (fun n hn => ?_) (fun hn => ?_)
      · rw [hn] at hlt; simp at hlt; linarith
      · rw [hn] at hlt; simp at hlt
    · simp only [Set.mem_compl_iff, Set.mem_range, not_exists] at hnot
      exact riemannZeta_one_sub (fun n h => hnot (-n) (by simp [h])) (fun h => hnot 1 (by simp [h]))
  have hlog := (logDeriv_congr_nhds hEq).eq_of_nhds
  have hLHS : logDeriv (fun z => riemannZeta (1 - z)) s = -logDeriv riemannZeta (1 - s) := by
    rw [show (fun z => riemannZeta (1 - z)) = riemannZeta ∘ (fun z => 1 - z) from rfl,
      logDeriv_comp (differentiableAt_riemannZeta (by simpa [sub_eq_iff_eq_add] using hs0))
        (by fun_prop)]; simp
  have hcpowLog : logDeriv (fun z => (2 * (π : ℂ)) ^ (-z)) s = -Complex.log (2 * π) := by
    rw [logDeriv_apply, ((hasDerivAt_neg' s).const_cpow (Or.inl h2π)).deriv]; field_simp
  have hcosLog : logDeriv (fun z => Complex.cos (π * z / 2)) s
      = -(π / 2 * Complex.tan (π * s / 2)) := by
    have hinner : HasDerivAt (fun z : ℂ => (π : ℂ) * z / 2) (π / 2) s := by
      simpa using ((hasDerivAt_id s).const_mul (π : ℂ)).div_const 2
    rw [logDeriv_apply, hinner.ccos.deriv, Complex.tan_eq_sin_div_cos]; field_simp
  rw [hLHS] at hlog
  have hdΓ : DifferentiableAt ℂ Gamma s := differentiableAt_Gamma s hsn
  have hdζ : DifferentiableAt ℂ riemannZeta s := differentiableAt_riemannZeta hs1
  have hd2π : DifferentiableAt ℂ (fun z => (2 * (π : ℂ)) ^ (-z)) s :=
    ((hasDerivAt_neg' s).const_cpow (Or.inl h2π)).differentiableAt
  rw [logDeriv_fun_mul s (by simp [hcpow, hΓ, hcos]) hz (by fun_prop) (by fun_prop),
      logDeriv_fun_mul s (by simp [hcpow, hΓ]) hcos (by fun_prop) (by fun_prop),
      logDeriv_fun_mul s (by simp [hcpow]) hΓ (by fun_prop) (by fun_prop),
      logDeriv_fun_mul s two_ne_zero hcpow (by fun_prop) (by fun_prop)] at hlog
  rw [logDeriv_const, hcpowLog, show logDeriv Gamma s = digamma s from rfl, hcosLog] at hlog
  simp only [Pi.zero_apply] at hlog
  linear_combination -hlog

/-- Functional equation for `ζ'/ζ` at `1 - s` when `Re s < 0`. -/
lemma logDeriv_ladder_form {s : ℂ} (hs : s.re < 0)
    (hcos : Complex.cos ((Real.pi : ℂ) * (1 - s) / 2) ≠ 0) :
    deriv riemannZeta s / riemannZeta s
      = -(deriv riemannZeta (1 - s) / riemannZeta (1 - s))
        + Complex.log (2 * (Real.pi : ℂ)) - Complex.digamma (1 - s)
        + ((Real.pi : ℂ) / 2) * Complex.tan ((Real.pi : ℂ) * (1 - s) / 2) := by
  have hw : (1 : ℝ) < (1 - s).re := by
    simp only [Complex.sub_re, Complex.one_re]; linarith
  have hwn : ∀ n : ℕ, (1 - s) ≠ -n := by
    intro n hn
    rw [hn] at hw
    simp only [Complex.neg_re, Complex.natCast_re] at hw
    have : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
    linarith
  have hw1 : (1 - s) ≠ 1 := by intro hn; rw [hn] at hw; simp at hw
  have hz : riemannZeta (1 - s) ≠ 0 := riemannZeta_ne_zero_of_one_lt_re hw
  have h1 := logDeriv_riemannZeta_one_sub hwn hw1 hz hcos
  simp only [logDeriv_apply] at h1
  rw [show (1 : ℂ) - (1 - s) = s by ring] at h1
  linear_combination h1

/-- Analyticity of `riemannZeta` off `1`. -/
lemma analyticAt_riemannZeta {z : ℂ} (hz : z ≠ 1) : AnalyticAt ℂ riemannZeta z := by
  refine DifferentiableOn.analyticAt (s := ({(1 : ℂ)}ᶜ : Set ℂ)) (fun w hw ↦ ?_) ?_
  · exact (differentiableAt_riemannZeta hw).differentiableWithinAt
  · exact isOpen_compl_singleton.mem_nhds hz

lemma meromorphicAt_riemannZeta_one : MeromorphicAt riemannZeta 1 := by
  have hEq : (fun s : ℂ ↦ (s - 1)⁻¹ + riemannZeta₀ s) =ᶠ[nhdsWithin 1 {(1 : ℂ)}ᶜ] riemannZeta := by
    filter_upwards [self_mem_nhdsWithin] with s hs
    exact (riemannZeta_eq_inv_sub_add hs).symm
  refine MeromorphicAt.congr ?_ hEq
  exact (((analyticAt_id.sub analyticAt_const).meromorphicAt).inv).add
    (DifferentiableOn.analyticAt differentiable_riemannZeta₀.differentiableOn
      Filter.univ_mem).meromorphicAt

lemma meromorphicOn_riemannZeta : MeromorphicOn riemannZeta Set.univ := by
  intro z _
  by_cases hz : z = 1
  · exact hz ▸ meromorphicAt_riemannZeta_one
  · exact (analyticAt_riemannZeta hz).meromorphicAt

lemma meromorphicOrderAt_riemannZeta_ne_top (z : ℂ) :
    meromorphicOrderAt riemannZeta z ≠ ⊤ := by
  have h2ne : riemannZeta 2 ≠ 0 := riemannZeta_ne_zero_of_one_lt_re (by norm_num)
  have h2an : AnalyticAt ℂ riemannZeta 2 := analyticAt_riemannZeta (by norm_num)
  have h2 : meromorphicOrderAt riemannZeta 2 ≠ ⊤ := by
    rw [h2an.meromorphicOrderAt_eq, h2an.analyticOrderAt_eq_zero.mpr h2ne]
    simp
  exact meromorphicOn_riemannZeta.meromorphicOrderAt_ne_top_of_isPreconnected
    isPreconnected_univ (Set.mem_univ 2) (Set.mem_univ z) h2

theorem riemannZeta_eq_riemannZeta₁_div {s : ℂ} (hs : s ≠ 1) :
    riemannZeta s = riemannZeta₁ s / (s - 1) := by
  have hs' : s - 1 ≠ 0 := sub_ne_zero.mpr hs
  rw [riemannZeta_eq_inv_sub_add hs, riemannZeta₁]
  field_simp

theorem riemannZeta₁_eq_mul {s : ℂ} (hs : s ≠ 1) :
    riemannZeta₁ s = (s - 1) * riemannZeta s := by
  have hne : s - 1 ≠ 0 := sub_ne_zero.mpr hs
  rw [riemannZeta_eq_inv_sub_add hs, riemannZeta₁]
  field_simp

theorem riemannZeta_eq_zero_iff_riemannZeta₁ {s : ℂ} (hs : s ≠ 1) :
    riemannZeta s = 0 ↔ riemannZeta₁ s = 0 := by
  rw [riemannZeta_eq_riemannZeta₁_div hs, div_eq_zero_iff]
  simp [sub_eq_zero, hs]

theorem logDeriv_riemannZeta₁_eq {s : ℂ} (hs : s ≠ 1) (hz : riemannZeta s ≠ 0) :
    logDeriv riemannZeta₁ s = logDeriv riemannZeta s + (s - 1)⁻¹ := by
  have hne : s - 1 ≠ 0 := sub_ne_zero.mpr hs
  have hEq : riemannZeta₁ =ᶠ[nhds s] (fun z ↦ (z - 1) * riemannZeta z) := by
    filter_upwards [isOpen_compl_singleton.mem_nhds (show s ∈ ({(1 : ℂ)}ᶜ) from hs)] with z hz'
    exact riemannZeta₁_eq_mul hz'
  have h := (logDeriv_congr_nhds hEq).eq_of_nhds
  have hsub : logDeriv (fun z : ℂ ↦ z - 1) s = (s - 1)⁻¹ := by
    rw [logDeriv_apply]
    have hd : deriv (fun z : ℂ ↦ z - 1) s = 1 := by
      simp
    rw [hd, one_div]
  rw [h, logDeriv_fun_mul s hne hz (by fun_prop) (differentiableAt_riemannZeta hs), hsub]
  ring

/-- Entire pole-free logarithmic derivative `F(s) = -logDeriv riemannZeta₁ s`. -/
noncomputable def F : ℂ → ℂ := fun s ↦ -logDeriv riemannZeta₁ s

lemma analyticAt_riemannZeta₁ (z : ℂ) : AnalyticAt ℂ riemannZeta₁ z :=
  DifferentiableOn.analyticAt differentiable_riemannZeta₁.differentiableOn Filter.univ_mem

lemma analyticOnNhd_riemannZeta₁ : AnalyticOnNhd ℂ riemannZeta₁ Set.univ :=
  fun z _ ↦ analyticAt_riemannZeta₁ z

lemma analyticAt_F {z : ℂ} (hz : riemannZeta₁ z ≠ 0) : AnalyticAt ℂ F z := by
  have hF : F = fun s ↦ -(deriv riemannZeta₁ s / riemannZeta₁ s) := by
    funext s; simp [F, logDeriv_apply]
  rw [hF]
  exact (((analyticAt_riemannZeta₁ z).deriv).div (analyticAt_riemannZeta₁ z) hz).neg

lemma analyticAt_F_one : AnalyticAt ℂ F 1 :=
  analyticAt_F (by rw [riemannZeta₁_one]; norm_num)

lemma analyticAt_F_of_zeta_ne_zero {z : ℂ} (hz1 : z ≠ 1) (h : riemannZeta z ≠ 0) :
    AnalyticAt ℂ F z :=
  analyticAt_F (fun hc ↦ h ((riemannZeta_eq_zero_iff_riemannZeta₁ hz1).mpr hc))

lemma meromorphicOn_F : MeromorphicOn F Set.univ := by
  have h : MeromorphicOn riemannZeta₁ Set.univ :=
    fun w _ ↦ (analyticAt_riemannZeta₁ w).meromorphicAt
  intro z hz
  exact (h.logDeriv z hz).neg

lemma riemannZeta₁_conj (s : ℂ) :
    riemannZeta₁ (starRingEnd ℂ s) = starRingEnd ℂ (riemannZeta₁ s) := by
  rcases eq_or_ne s 1 with rfl | hs
  · simp [riemannZeta₁_one]
  · have hs' : (starRingEnd ℂ s) ≠ 1 := by
      intro h
      exact hs (by simpa using congrArg (starRingEnd ℂ) h)
    rw [riemannZeta₁_eq_mul hs', riemannZeta₁_eq_mul hs, riemannZeta_conj, map_mul, map_sub,
      map_one]

lemma deriv_riemannZeta₁_conj (s : ℂ) :
    deriv riemannZeta₁ (starRingEnd ℂ s) = starRingEnd ℂ (deriv riemannZeta₁ s) := by
  have hfun : riemannZeta₁ = fun z ↦ starRingEnd ℂ (riemannZeta₁ (starRingEnd ℂ z)) := by
    funext z
    rw [riemannZeta₁_conj]
    simp
  conv_lhs => rw [hfun]
  exact deriv_conj_conj' riemannZeta₁ s

lemma F_conj (s : ℂ) : F (starRingEnd ℂ s) = starRingEnd ℂ (F s) := by
  simp only [F, logDeriv_apply, map_neg, neg_inj]
  rw [deriv_riemannZeta₁_conj, riemannZeta₁_conj, map_div₀]

lemma meromorphicOrderAt_riemannZeta₁_ne_top (z : ℂ) :
    meromorphicOrderAt riemannZeta₁ z ≠ ⊤ := by
  have h1an : AnalyticAt ℂ riemannZeta₁ 1 := analyticAt_riemannZeta₁ 1
  have h1 : meromorphicOrderAt riemannZeta₁ 1 ≠ ⊤ := by
    rw [h1an.meromorphicOrderAt_eq,
      h1an.analyticOrderAt_eq_zero.mpr (by rw [riemannZeta₁_one]; norm_num)]
    simp
  have hmero : MeromorphicOn riemannZeta₁ Set.univ :=
    fun w _ ↦ (analyticAt_riemannZeta₁ w).meromorphicAt
  exact hmero.meromorphicOrderAt_ne_top_of_isPreconnected
    isPreconnected_univ (Set.mem_univ 1) (Set.mem_univ z) h1

lemma hasSimplePolesOn_F_univ : HasSimplePolesOn F Set.univ := by
  intro z _
  have hζ : MeromorphicAt riemannZeta₁ z := (analyticAt_riemannZeta₁ z).meromorphicAt
  have hconst : meromorphicOrderAt (fun _ : ℂ ↦ (-1 : ℂ)) z = 0 := by
    rw [analyticAt_const.meromorphicOrderAt_eq, analyticAt_const.analyticOrderAt_eq_zero.mpr
      (by norm_num)]
    rfl
  have hFeq : F = (fun _ : ℂ ↦ (-1 : ℂ)) • logDeriv riemannZeta₁ := by funext w; simp [F]
  have hF : meromorphicOrderAt F z = meromorphicOrderAt (logDeriv riemannZeta₁) z := by
    rw [hFeq, meromorphicOrderAt_smul analyticAt_const.meromorphicAt hζ.logDeriv, hconst, zero_add]
  rw [hF]
  by_cases h0 : meromorphicOrderAt riemannZeta₁ z = 0
  · refine le_trans ?_ (meromorphicOrderAt_logDeriv_nonneg hζ h0)
    decide
  · rw [meromorphicOrderAt_logDeriv_eq_neg_one hζ h0 (meromorphicOrderAt_riemannZeta₁_ne_top z)]
    norm_cast

theorem riemannZeta₁_ne_zero_codiscrete :
    ∀ᶠ z in codiscreteWithin (Set.univ : Set ℂ), riemannZeta₁ z ≠ 0 := by
  rcases analyticOnNhd_riemannZeta₁.eqOn_zero_or_eventually_ne_zero_of_preconnected
    isPreconnected_univ with h | h
  · exact absurd (h (Set.mem_univ 1)) (by simp [riemannZeta₁_one])
  · exact h

theorem finite_zeros_riemannZeta₁_of_isCompact {K : Set ℂ} (hK : IsCompact K) :
    {z ∈ K | riemannZeta₁ z = 0}.Finite := by
  have hmem : {z : ℂ | riemannZeta₁ z ≠ 0} ∈ codiscreteWithin K :=
    Filter.codiscreteWithin_mono (Set.subset_univ K) riemannZeta₁_ne_zero_codiscrete
  refine (hK.finite_sdiff_of_mem_codiscreteWithin hmem).subset fun z hz ↦ ⟨hz.1, ?_⟩
  simpa using hz.2

/-- In the closed left half-plane `Re s ≤ 0`, the only zeros of `riemannZeta` are `-2(n+1)`. -/
theorem riemannZeta_ne_zero_of_re_le_zero {s : ℂ} (hs : s.re ≤ 0)
    (h : ∀ n : ℕ, s ≠ -2 * ((n : ℂ) + 1)) : riemannZeta s ≠ 0 := by
  rcases eq_or_ne s 0 with rfl | hs0
  · rw [riemannZeta_zero]; norm_num
  have hpi : (Real.pi : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr Real.pi_ne_zero
  obtain ⟨w, rfl⟩ : ∃ w : ℂ, s = 1 - w := ⟨1 - s, by ring⟩
  have hw : 1 ≤ w.re := by simp only [Complex.sub_re, Complex.one_re] at hs; linarith
  have hw1 : w ≠ 1 := fun hn ↦ hs0 (by rw [hn]; ring)
  have hwn : ∀ n : ℕ, w ≠ -n := by
    intro n hn
    rw [hn] at hw
    simp only [Complex.neg_re, Complex.natCast_re] at hw
    have : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
    linarith
  have hcos : Complex.cos ((Real.pi : ℂ) * w / 2) ≠ 0 := by
    rw [Ne, Complex.cos_eq_zero_iff]
    rintro ⟨k, hk⟩
    have h2 : (Real.pi : ℂ) * w = (Real.pi : ℂ) * (2 * (k : ℂ) + 1) := by linear_combination 2 * hk
    have hwk : w = 2 * (k : ℂ) + 1 := mul_left_cancel₀ hpi h2
    have hkpos : 0 < k := by
      by_contra hk0
      have hk0' : k ≤ 0 := not_lt.mp hk0
      rcases hk0'.eq_or_lt with rfl | hkneg
      · exact hw1 (by rw [hwk]; simp)
      · rw [hwk] at hw
        simp only [Complex.add_re, Complex.mul_re, Complex.intCast_re, Complex.intCast_im,
          Complex.one_re, Complex.re_ofNat, Complex.im_ofNat] at hw
        have : (k : ℝ) ≤ -1 := by exact_mod_cast Int.le_sub_one_of_lt hkneg
        linarith
    obtain ⟨m, rfl⟩ : ∃ m : ℕ, k = (m : ℤ) + 1 := ⟨(k - 1).toNat, by omega⟩
    exact h m (by rw [hwk]; push_cast; ring)
  rw [riemannZeta_one_sub hwn hw1]
  refine mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero two_ne_zero ?_) ?_) hcos) ?_
  · simp [Complex.cpow_eq_zero_iff, mul_ne_zero two_ne_zero hpi]
  · exact Complex.Gamma_ne_zero hwn
  · exact riemannZeta_ne_zero_of_one_le_re hw

/-- Exact partition of the zeros of the entire function `riemannZeta₁`: either nontrivial
(`0 < Re z < 1`) or trivial (`z = -2(k+1)`). -/
theorem riemannZeta₁_eq_zero_iff {z : ℂ} :
    riemannZeta₁ z = 0 ↔
      z ∈ IEANTN.zetaZeroesIn (Set.Ioo (0 : ℝ) 1) Set.univ ∨
        ∃ k : ℕ, z = -2 * ((k : ℂ) + 1) := by
  constructor
  · intro hz1
    have hne1 : z ≠ 1 := by
      intro h; rw [h, riemannZeta₁_one] at hz1; exact one_ne_zero hz1
    have hz : riemannZeta z = 0 := (riemannZeta_eq_zero_iff_riemannZeta₁ hne1).mpr hz1
    have hlt1 : z.re < 1 := by
      by_contra hge
      exact riemannZeta_ne_zero_of_one_le_re (not_lt.mp hge) hz
    rcases le_or_gt z.re 0 with hle0 | hgt0
    · refine Or.inr ?_
      by_contra htriv
      push Not at htriv
      exact riemannZeta_ne_zero_of_re_le_zero hle0 htriv hz
    · exact Or.inl ⟨⟨hgt0, hlt1⟩, Set.mem_univ _, hz⟩
  · rintro (⟨⟨h0, h1⟩, -, hz⟩ | ⟨k, rfl⟩)
    · have hne1 : z ≠ 1 := fun h ↦ by rw [h] at h1; simp at h1
      exact (riemannZeta_eq_zero_iff_riemannZeta₁ hne1).mp hz
    · have hne1 : (-2 * ((k : ℂ) + 1)) ≠ 1 := by
        intro h
        have hre := congrArg Complex.re h
        simp only [Complex.mul_re, Complex.neg_re, Complex.re_ofNat,
          Complex.add_re, Complex.natCast_re, Complex.one_re, Complex.add_im,
          Complex.natCast_im, Complex.one_im] at hre
        have : (0 : ℝ) ≤ k := Nat.cast_nonneg k
        linarith
      exact (riemannZeta_eq_zero_iff_riemannZeta₁ hne1).mp (riemannZeta_neg_two_mul_nat_add_one k)

/-- Odd negative integer columns `sigmaZeta n = 1 - 2n`. -/
noncomputable def sigmaZeta (n : ℕ) : ℝ := 1 - 2 * n

lemma riemannZeta_ne_zero_on_column {n : ℕ} (hn : 1 ≤ n) {z : ℂ} (hz : z.re = sigmaZeta n) :
    riemannZeta z ≠ 0 := by
  have hn1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hre : z.re ≤ 0 := by rw [hz]; simp only [sigmaZeta]; linarith
  refine riemannZeta_ne_zero_of_re_le_zero hre ?_
  intro m hm
  have : z.re = -2 * ((m : ℝ) + 1) := by rw [hm]; simp
  rw [hz] at this
  simp only [sigmaZeta] at this
  have hcast : (1 : ℝ) - 2 * n = -2 * m - 2 := by linarith
  have : (1 : ℤ) - 2 * n = -2 * m - 2 := by exact_mod_cast hcast
  omega

lemma cos_ne_zero_on_column {n : ℕ} {s : ℂ} (hs : s.re = sigmaZeta n) :
    Complex.cos ((Real.pi : ℂ) * (1 - s) / 2) ≠ 0 := by
  rw [Ne, Complex.cos_eq_zero_iff]
  rintro ⟨k, hk⟩
  have him : s.im = 0 := by
    have := congrArg Complex.im hk
    simp only [Complex.div_im, Complex.mul_im, Complex.mul_re, Complex.sub_im, Complex.sub_re,
      Complex.one_im, Complex.one_re, Complex.ofReal_im, Complex.ofReal_re, Complex.add_im,
      Complex.add_re, Complex.intCast_im, Complex.intCast_re, Complex.re_ofNat,
      Complex.im_ofNat, Complex.normSq_apply] at this
    nlinarith [this, Real.pi_pos]
  have hre := congrArg Complex.re hk
  simp only [Complex.div_re, Complex.mul_re, Complex.mul_im, Complex.sub_re, Complex.sub_im,
    Complex.one_re, Complex.one_im, Complex.ofReal_re, Complex.ofReal_im, Complex.add_re,
    Complex.add_im, Complex.intCast_re, Complex.intCast_im, Complex.re_ofNat, Complex.im_ofNat,
    Complex.normSq_apply, him, hs, sigmaZeta] at hre
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have h2n : (2 : ℝ) * n = 2 * k + 1 := by field_simp at hre; nlinarith [hre, Real.pi_pos]
  have : (2 : ℤ) * n = 2 * k + 1 := by exact_mod_cast h2n
  omega

theorem norm_cos_sq (w : ℂ) :
    ‖Complex.cos w‖ ^ 2 = Real.cos w.re ^ 2 + Real.sinh w.im ^ 2 := by
  have h := Complex.cos_add_mul_I (w.re : ℂ) (w.im : ℂ)
  rw [Complex.re_add_im] at h
  rw [h, ← Complex.ofReal_cos, ← Complex.ofReal_cosh, ← Complex.ofReal_sin,
    ← Complex.ofReal_sinh, ← Complex.ofReal_mul, ← Complex.ofReal_mul]
  rw [Complex.sq_norm, Complex.normSq_apply]
  simp only [Complex.sub_re, Complex.sub_im, Complex.ofReal_re, Complex.ofReal_im,
    Complex.mul_re, Complex.mul_im, Complex.I_re, Complex.I_im]
  nlinarith [Real.cosh_sq w.im, Real.sin_sq_add_cos_sq w.re,
    sq_nonneg (Real.cos w.re), sq_nonneg (Real.sinh w.im)]

theorem norm_sin_sq (w : ℂ) :
    ‖Complex.sin w‖ ^ 2 = Real.sin w.re ^ 2 + Real.sinh w.im ^ 2 := by
  have h := Complex.sin_add_mul_I (w.re : ℂ) (w.im : ℂ)
  rw [Complex.re_add_im] at h
  rw [h, ← Complex.ofReal_sin, ← Complex.ofReal_cosh, ← Complex.ofReal_cos,
    ← Complex.ofReal_sinh, ← Complex.ofReal_mul, ← Complex.ofReal_mul]
  rw [Complex.sq_norm, Complex.normSq_apply]
  simp only [Complex.add_re, Complex.add_im, Complex.ofReal_re, Complex.ofReal_im,
    Complex.mul_re, Complex.mul_im, Complex.I_re, Complex.I_im]
  nlinarith [Real.cosh_sq w.im, Real.sin_sq_add_cos_sq w.re,
    sq_nonneg (Real.sin w.re), sq_nonneg (Real.sinh w.im)]

lemma cos_ne_zero_of_im_ne_zero {w : ℂ} (h : w.im ≠ 0) : Complex.cos w ≠ 0 := by
  intro hc
  have hnorm := norm_cos_sq w
  rw [hc] at hnorm
  have hs : Real.sinh w.im ≠ 0 := fun hz ↦ h (Real.sinh_eq_zero.mp hz)
  have hpos : 0 < Real.sinh w.im ^ 2 := by positivity
  simp only [norm_zero] at hnorm
  nlinarith [sq_nonneg (Real.cos w.re)]

theorem norm_tan_le_of_im_ne_zero {w : ℂ} (h : w.im ≠ 0) :
    ‖Complex.tan w‖ ≤ Real.cosh w.im / |Real.sinh w.im| := by
  have hsinh : Real.sinh w.im ≠ 0 := fun hc ↦ h (Real.sinh_eq_zero.mp hc)
  have habs : 0 < |Real.sinh w.im| := abs_pos.mpr hsinh
  have hcos : ‖Complex.cos w‖ ≠ 0 := by
    intro hc
    have := norm_cos_sq w
    rw [hc] at this
    nlinarith [sq_nonneg (Real.cos w.re), sq_abs (Real.sinh w.im), habs]
  rw [Complex.tan_eq_sin_div_cos, norm_div, div_le_div_iff₀ (by positivity) habs]
  have h1 : ‖Complex.sin w‖ ^ 2 ≤ Real.cosh w.im ^ 2 := by
    rw [norm_sin_sq]
    nlinarith [Real.sin_sq_add_cos_sq w.re, Real.cosh_sq w.im, sq_nonneg (Real.cos w.re)]
  have h2 : |Real.sinh w.im| ^ 2 ≤ ‖Complex.cos w‖ ^ 2 := by
    rw [norm_cos_sq, sq_abs]
    nlinarith [sq_nonneg (Real.cos w.re)]
  have hsin_le : ‖Complex.sin w‖ ≤ Real.cosh w.im := by
    have := Real.sqrt_le_sqrt h1
    rwa [Real.sqrt_sq (norm_nonneg _), Real.sqrt_sq (Real.cosh_pos _).le] at this
  have hsinh_le : |Real.sinh w.im| ≤ ‖Complex.cos w‖ := by
    have := Real.sqrt_le_sqrt h2
    rwa [Real.sqrt_sq (abs_nonneg _), Real.sqrt_sq (norm_nonneg _)] at this
  exact mul_le_mul hsin_le hsinh_le (abs_nonneg _) (Real.cosh_pos _).le

theorem norm_tan_le_one_of_sin_re_eq_zero {w : ℂ} (h : Real.sin w.re = 0) :
    ‖Complex.tan w‖ ≤ 1 := by
  have hcos_sq : Real.cos w.re ^ 2 = 1 := by
    have := Real.sin_sq_add_cos_sq w.re
    nlinarith [h]
  have hs : ‖Complex.sin w‖ ^ 2 = Real.sinh w.im ^ 2 := by rw [norm_sin_sq, h]; ring
  have hc : ‖Complex.cos w‖ ^ 2 = 1 + Real.sinh w.im ^ 2 := by rw [norm_cos_sq, hcos_sq]
  have hcpos : 0 < ‖Complex.cos w‖ := by
    have hsq : (0 : ℝ) < ‖Complex.cos w‖ ^ 2 := by rw [hc]; positivity
    nlinarith [norm_nonneg (Complex.cos w)]
  rw [Complex.tan_eq_sin_div_cos, norm_div, div_le_one hcpos]
  nlinarith [norm_nonneg (Complex.sin w), norm_nonneg (Complex.cos w), hs, hc]

theorem norm_tan_le_one_on_column {n : ℕ} {z : ℂ} (hz : z.re = sigmaZeta n) :
    ‖Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)‖ ≤ 1 := by
  refine norm_tan_le_one_of_sin_re_eq_zero ?_
  have hEq : (Real.pi : ℂ) * (1 - z) / 2 = ((Real.pi / 2 : ℝ) : ℂ) * (1 - z) := by
    push_cast; ring
  have hre : ((Real.pi : ℂ) * (1 - z) / 2).re = (n : ℝ) * Real.pi := by
    rw [hEq]
    simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, Complex.sub_re,
      Complex.sub_im, Complex.one_re, Complex.one_im, hz, sigmaZeta]
    ring
  rw [hre]
  exact Real.sin_nat_mul_pi n

/-- Uniform boundedness of `ζ'/ζ` on any closed half-plane `σ₀ ≤ Re w` with `1 < σ₀`. -/
theorem logDeriv_riemannZeta_bounded_of_re_ge {σ₀ : ℝ} (hσ₀ : 1 < σ₀) :
    ∃ M : ℝ, 0 ≤ M ∧ ∀ w : ℂ, σ₀ ≤ w.re → ‖deriv riemannZeta w / riemannZeta w‖ ≤ M := by
  have hsum0 : Summable
      (fun n ↦ ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) (σ₀ : ℂ) n‖) :=
    summable_norm_iff.mpr (ArithmeticFunction.LSeriesSummable_vonMangoldt (by simpa using hσ₀))
  refine ⟨∑' n, ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) (σ₀ : ℂ) n‖,
    tsum_nonneg (fun _ ↦ norm_nonneg _), fun w hw ↦ ?_⟩
  have h1 : 1 < w.re := lt_of_lt_of_le hσ₀ hw
  have hle : ∀ n, ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w n‖
      ≤ ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) (σ₀ : ℂ) n‖ := by
    intro n
    refine LSeries.norm_term_le_of_re_le_re _ ?_ n
    simpa using hw
  have hsumw : Summable
      (fun n ↦ ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w n‖) :=
    hsum0.of_nonneg_of_le (fun _ ↦ norm_nonneg _) hle
  have key : deriv riemannZeta w / riemannZeta w
      = -LSeries (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w := by
    rw [ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div h1]; ring
  rw [key, norm_neg]
  calc ‖LSeries (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w‖
      = ‖∑' n, LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w n‖ := rfl
    _ ≤ ∑' n, ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) w n‖ :=
        norm_tsum_le_tsum_norm hsumw
    _ ≤ ∑' n, ‖LSeries.term (fun n ↦ (ArithmeticFunction.vonMangoldt n : ℂ)) (σ₀ : ℂ) n‖ :=
        Summable.tsum_mono hsumw hsum0 hle

/-- Residue limit of a logarithmic derivative at a point of finite meromorphic order. -/
theorem tendsto_sub_mul_logDeriv {f : ℂ → ℂ} {x : ℂ} {n : ℤ} (hf : MeromorphicAt f x)
    (hord : meromorphicOrderAt f x = n) :
    Tendsto (fun z ↦ (z - x) * logDeriv f z) (𝓝[≠] x) (𝓝 (n : ℂ)) := by
  rw [meromorphicOrderAt_eq_int_iff hf] at hord
  obtain ⟨g, hga, hg0, (hg : f =ᶠ[𝓝[≠] x] fun z ↦ (z - x) ^ n • g z)⟩ := hord
  have hderiv : ∀ᶠ z in 𝓝[≠] x,
      deriv f z = (z - x) ^ (n - 1) * ((n : ℂ) * g z + (z - x) * deriv g z) := by
    filter_upwards [hga.eventually_analyticAt.filter_mono nhdsWithin_le_nhds,
      eventually_mem_nhdsWithin, hg.nhdsNE_deriv] with z hgz hmem hz
    have hzx : z - x ≠ 0 := by simpa [sub_eq_zero] using hmem
    calc deriv f z = deriv (fun z ↦ (z - x) ^ n • g z) z := hz
      _ = (z - x) ^ n • deriv g z + deriv ((· ^ n) ∘ (· - x)) z • g z :=
        deriv_fun_smul (by fun_prop (disch := grind)) hgz.differentiableAt
      _ = (z - x) ^ n • deriv g z + (n * (z - x) ^ (n - 1)) • g z := by
        rw [deriv_comp _ (by fun_prop (disch := grind)) (by fun_prop)]
        simp [deriv_zpow]
      _ = (z - x) ^ (n - 1) * ((n : ℂ) * g z + (z - x) * deriv g z) := by
        simp only [smul_eq_mul]
        rw [show (z - x) ^ n = (z - x) ^ (n - 1) * (z - x) by
          rw [← zpow_add_one₀ hzx]; ring_nf]
        ring
  have hlim : Tendsto (fun z ↦ ((n : ℂ) * g z + (z - x) * deriv g z) / g z) (𝓝[≠] x)
      (𝓝 (((n : ℂ) * g x + (x - x) * deriv g x) / g x)) := by
    have hc : ContinuousAt (fun z ↦ ((n : ℂ) * g z + (z - x) * deriv g z) / g z) x :=
      ((continuousAt_const.mul hga.continuousAt).add
        ((continuousAt_id.sub continuousAt_const).mul hga.deriv.continuousAt)).div
        hga.continuousAt hg0
    exact hc.tendsto.mono_left nhdsWithin_le_nhds
  have hval : ((n : ℂ) * g x + (x - x) * deriv g x) / g x = n := by
    rw [sub_self, zero_mul, add_zero]; field_simp
  rw [hval] at hlim
  refine hlim.congr' ?_
  filter_upwards [hderiv, hg, eventually_mem_nhdsWithin,
    hga.continuousAt.eventually_ne hg0 |>.filter_mono nhdsWithin_le_nhds] with z hdz hfz hmem hgz
  have hzx : z - x ≠ 0 := by simpa [sub_eq_zero] using hmem
  rw [logDeriv_apply, hdz, hfz, smul_eq_mul]
  rw [show (z - x) ^ n = (z - x) ^ (n - 1) * (z - x) by
    rw [← zpow_add_one₀ hzx]; ring_nf]
  have hp : (z - x) ^ (n - 1) ≠ 0 := zpow_ne_zero _ hzx
  field_simp

theorem meromorphicOrderAt_riemannZeta₁_eq {ρ : ℂ} (hρ : ρ ≠ 1) :
    meromorphicOrderAt riemannZeta₁ ρ = meromorphicOrderAt riemannZeta ρ := by
  have hEq : riemannZeta₁ =ᶠ[𝓝[≠] ρ] (fun z ↦ (z - 1) * riemannZeta z) := by
    filter_upwards [nhdsWithin_le_nhds (isOpen_compl_singleton.mem_nhds
      (show ρ ∈ ({(1 : ℂ)}ᶜ) from hρ))] with z hz
    exact riemannZeta₁_eq_mul hz
  rw [meromorphicOrderAt_congr hEq,
    show (fun z ↦ (z - 1) * riemannZeta z) = (fun z ↦ z - 1) * riemannZeta from rfl,
    meromorphicOrderAt_mul (by fun_prop) (meromorphicOn_riemannZeta ρ (Set.mem_univ ρ))]
  have h1 : AnalyticAt ℂ (fun z : ℂ ↦ z - 1) ρ := by fun_prop
  have h0 : meromorphicOrderAt (fun z : ℂ ↦ z - 1) ρ = 0 := by
    rw [h1.meromorphicOrderAt_eq, h1.analyticOrderAt_eq_zero.mpr (sub_ne_zero.mpr hρ)]
    simp
  rw [h0, zero_add]

theorem tendsto_sub_mul_F {ρ : ℂ} (hρ : ρ ≠ 1) :
    Tendsto (fun z ↦ (z - ρ) * F z) (𝓝[≠] ρ) (𝓝 (-((IEANTN.zetaOrder ρ : ℤ) : ℂ))) := by
  obtain ⟨n, hn⟩ := WithTop.ne_top_iff_exists.mp (meromorphicOrderAt_riemannZeta_ne_top ρ)
  have hord : meromorphicOrderAt riemannZeta₁ ρ = n := by
    rw [meromorphicOrderAt_riemannZeta₁_eq hρ, ← hn]
  have hz : IEANTN.zetaOrder ρ = n := by rw [IEANTN.zetaOrder, ← hn]; rfl
  have h := (tendsto_sub_mul_logDeriv (analyticAt_riemannZeta₁ ρ).meromorphicAt hord).neg
  rw [hz]
  exact h.congr fun z ↦ by simp [F]

theorem meromorphicOrderAt_eq_zero_of_analytic {f : ℂ → ℂ} {x : ℂ} (hf : AnalyticAt ℂ f x)
    (hx : f x ≠ 0) : meromorphicOrderAt f x = 0 := by
  rw [hf.meromorphicOrderAt_eq, hf.analyticOrderAt_eq_zero.mpr hx]
  simp

theorem meromorphicOrderAt_riemannZeta_trivial (k : ℕ) :
    meromorphicOrderAt riemannZeta (-2 * ((k : ℂ) + 1)) = 1 := by
  set s₀ : ℂ := 2 * (k : ℂ) + 3 with hs₀
  have hs₀re : 1 < s₀.re := by
    simp [hs₀]; linarith [(Nat.cast_nonneg k : (0 : ℝ) ≤ k)]
  have hopen : IsOpen {s : ℂ | 1 < s.re} := isOpen_lt continuous_const Complex.continuous_re
  have hloc : (fun s ↦ riemannZeta (1 - s)) =ᶠ[𝓝 s₀]
      (fun s ↦ 2 * (2 * (Real.pi : ℂ)) ^ (-s) * Complex.Gamma s * Complex.cos (Real.pi * s / 2)
        * riemannZeta s) := by
    filter_upwards [hopen.mem_nhds hs₀re] with s hs
    have hs' : 1 < s.re := hs
    refine riemannZeta_one_sub (fun n hn ↦ ?_) (fun h ↦ ?_)
    · have : s.re = -(n : ℝ) := by rw [hn]; simp
      have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
      linarith
    · rw [h] at hs'; simp at hs'
  have hcomp : meromorphicOrderAt (fun s ↦ riemannZeta (1 - s)) s₀
      = meromorphicOrderAt riemannZeta (-2 * ((k : ℂ) + 1)) := by
    have hg : AnalyticAt ℂ (fun s : ℂ ↦ 1 - s) s₀ := by fun_prop
    have hd : deriv (fun s : ℂ ↦ 1 - s) s₀ ≠ 0 := by
      rw [deriv_const_sub, deriv_id'']; norm_num
    have h := meromorphicOrderAt_comp_of_deriv_ne_zero (f := riemannZeta) hg hd
    rw [show (1 : ℂ) - s₀ = -2 * ((k : ℂ) + 1) by rw [hs₀]; ring] at h
    exact h
  have hΓpole : ∀ m : ℕ, s₀ ≠ -(m : ℂ) := by
    intro m hm
    have : s₀.re = -(m : ℝ) := by rw [hm]; simp
    have : (0 : ℝ) ≤ m := Nat.cast_nonneg m
    linarith
  have hΓa : AnalyticAt ℂ Complex.Gamma s₀ := by
    have hΓd : DifferentiableOn ℂ Complex.Gamma {s : ℂ | 1 < s.re} := fun s hs ↦
      (Complex.differentiableAt_Gamma s (fun m hm ↦ by
        have hs' : 1 < s.re := hs
        have : s.re = -(m : ℝ) := by rw [hm]; simp
        have : (0 : ℝ) ≤ m := Nat.cast_nonneg m
        linarith)).differentiableWithinAt
    exact hΓd.analyticOnNhd hopen s₀ hs₀re
  have hΓne : Complex.Gamma s₀ ≠ 0 := Complex.Gamma_ne_zero hΓpole
  have hζa : AnalyticAt ℂ riemannZeta s₀ := by
    have hd : DifferentiableOn ℂ riemannZeta {s : ℂ | 1 < s.re} := fun s hs ↦
      (differentiableAt_riemannZeta (by
        intro h; have hs' : 1 < s.re := hs; rw [h] at hs'; simp at hs')).differentiableWithinAt
    exact hd.analyticOnNhd hopen s₀ hs₀re
  have hζne : riemannZeta s₀ ≠ 0 := riemannZeta_ne_zero_of_one_lt_re hs₀re
  have hpowa : AnalyticAt ℂ (fun s : ℂ ↦ (2 * (Real.pi : ℂ)) ^ (-s)) s₀ := by
    have h2π : (2 * (Real.pi : ℂ)) ≠ 0 := by simp [Real.pi_ne_zero]
    exact (differentiable_id.neg.const_cpow (Or.inl h2π)).analyticAt s₀
  have hpowne : (2 * (Real.pi : ℂ)) ^ (-s₀) ≠ 0 := by
    have h2π : (2 * (Real.pi : ℂ)) ≠ 0 := by simp [Real.pi_ne_zero]
    exact (Complex.cpow_ne_zero_iff_of_exponent_ne_zero (by
      intro h; have := congrArg Complex.re h; simp [hs₀] at this; linarith [this])).mpr h2π
  have hcosa : AnalyticAt ℂ (fun s : ℂ ↦ Complex.cos (Real.pi * s / 2)) s₀ := by fun_prop
  have hcos0 : Complex.cos (Real.pi * s₀ / 2) = 0 := by
    rw [Complex.cos_eq_zero_iff]
    exact ⟨k + 1, by rw [hs₀]; push_cast; ring⟩
  have hcosd : deriv (fun s : ℂ ↦ Complex.cos (Real.pi * s / 2)) s₀ ≠ 0 := by
    have hd : HasDerivAt (fun s : ℂ ↦ Complex.cos (Real.pi * s / 2))
        (-Complex.sin (Real.pi * s₀ / 2) * (Real.pi / 2)) s₀ := by
      have h1 : HasDerivAt (fun s : ℂ ↦ (Real.pi : ℂ) * s / 2) ((Real.pi : ℂ) / 2) s₀ := by
        simpa using ((hasDerivAt_id s₀).const_mul (Real.pi : ℂ)).div_const 2
      exact (Complex.hasDerivAt_cos _).comp s₀ h1
    rw [hd.deriv]
    have hsin : Complex.sin (Real.pi * s₀ / 2) ≠ 0 := by
      intro h
      have := Complex.sin_sq_add_cos_sq (Real.pi * s₀ / 2)
      rw [h, hcos0] at this; norm_num at this
    exact mul_ne_zero (neg_ne_zero.mpr hsin) (by simp [Real.pi_ne_zero])
  have hcos1 : meromorphicOrderAt (fun s : ℂ ↦ Complex.cos (Real.pi * s / 2)) s₀ = 1 := by
    rw [hcosa.meromorphicOrderAt_eq, hcosa.analyticOrderAt_eq_one_of_zero_deriv_ne_zero hcos0 hcosd]
    rfl
  have hR : meromorphicOrderAt
      (fun s ↦ 2 * (2 * (Real.pi : ℂ)) ^ (-s) * Complex.Gamma s * Complex.cos (Real.pi * s / 2)
        * riemannZeta s) s₀ = 1 := by
    have e : (fun s ↦ 2 * (2 * (Real.pi : ℂ)) ^ (-s) * Complex.Gamma s
        * Complex.cos (Real.pi * s / 2) * riemannZeta s)
        = ((((fun _ : ℂ ↦ (2 : ℂ)) * fun s : ℂ ↦ (2 * (Real.pi : ℂ)) ^ (-s)) * Complex.Gamma)
          * fun s : ℂ ↦ Complex.cos (Real.pi * s / 2)) * riemannZeta := by
      funext s; simp [Pi.mul_apply]
    rw [e, meromorphicOrderAt_mul (by fun_prop) hζa.meromorphicAt,
      meromorphicOrderAt_mul (by fun_prop) hcosa.meromorphicAt,
      meromorphicOrderAt_mul (by fun_prop) hΓa.meromorphicAt,
      meromorphicOrderAt_mul analyticAt_const.meromorphicAt hpowa.meromorphicAt,
      meromorphicOrderAt_eq_zero_of_analytic analyticAt_const (by norm_num),
      meromorphicOrderAt_eq_zero_of_analytic hpowa hpowne,
      meromorphicOrderAt_eq_zero_of_analytic hΓa hΓne, hcos1,
      meromorphicOrderAt_eq_zero_of_analytic hζa hζne]
    rfl
  rw [← hcomp, meromorphicOrderAt_congr (hloc.filter_mono nhdsWithin_le_nhds), hR]

theorem zetaOrder_trivial (k : ℕ) : IEANTN.zetaOrder (-2 * ((k : ℂ) + 1)) = 1 := by
  rw [IEANTN.zetaOrder, meromorphicOrderAt_riemannZeta_trivial]
  rfl

theorem zetaOrder_eq_zero_of_ne {z : ℂ} (hz1 : z ≠ 1) (hζ : riemannZeta z ≠ 0) :
    IEANTN.zetaOrder z = 0 := by
  rw [IEANTN.zetaOrder, meromorphicOrderAt_eq_zero_of_analytic (analyticAt_riemannZeta hz1) hζ]
  rfl

theorem zetaOrder_pos_of_zeta_eq_zero {z : ℂ} (hz1 : z ≠ 1) (hz : riemannZeta z = 0) :
    1 ≤ IEANTN.zetaOrder z := by
  have han : AnalyticAt ℂ riemannZeta z := analyticAt_riemannZeta hz1
  have hne_top : analyticOrderAt riemannZeta z ≠ ⊤ := by
    intro htop
    have hm : meromorphicOrderAt riemannZeta z = ⊤ := by
      rw [han.meromorphicOrderAt_eq, htop]; rfl
    exact meromorphicOrderAt_riemannZeta_ne_top z hm
  obtain ⟨m, hm⟩ := ENat.ne_top_iff_exists.mp hne_top
  have hm0 : m ≠ 0 := by
    intro hm0
    subst hm0
    have h0 : analyticOrderAt riemannZeta z = 0 := by simpa using hm.symm
    exact (han.analyticOrderAt_eq_zero.mp h0) hz
  have hm_pos : 1 ≤ m := Nat.one_le_iff_ne_zero.mpr hm0
  have hmo : meromorphicOrderAt riemannZeta z = (m : ℤ) := by
    rw [han.meromorphicOrderAt_eq, ← hm]
    rfl
  rw [IEANTN.zetaOrder, hmo]
  change 1 ≤ (m : ℤ)
  exact_mod_cast hm_pos

theorem residue_eq_mul_of_tendsto {f g h : ℂ → ℂ} {p c : ℂ} (hg : ContinuousAt g p)
    (hf : Tendsto (fun s ↦ (s - p) * f s) (𝓝[≠] p) (𝓝 c))
    (hev : ∀ᶠ s in 𝓝[≠] p, h s = g s * f s) :
    residue h p = g p * c := by
  apply residue_eq_of_tendsto
  have hlim := (hg.tendsto.mono_left nhdsWithin_le_nhds).mul hf
  refine hlim.congr' ?_
  filter_upwards [hev] with s hs
  rw [hs]; ring

end ZetaHadamardSolution
