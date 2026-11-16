/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: IEANTN contributors
-/
import IEANTN.Nodes.ZetaHadamard.v1.Conclusions
import LocalZeros

/-!
# Solution for `ZetaHadamard.v1`: Paired Partial-Fraction Expansion of `ζ'/ζ`

Proves `ZetaHadamard.v1.challenge_logDeriv_partial_fractions` by integrating
`g_{s,w}(z) = F(z) (1/(s - z) - 1/(w - z))`, where `F = -logDeriv riemannZeta₁`, around
expanding rectangles `[-1 - 2N, 2 + 2N] × [-T_N, T_N]` along good ordinates `T_N ∈ [N + 1/4, N + 3/4]`.
-/

namespace ZetaHadamardSolution

open scoped Real Interval
open Complex Filter Topology Set

/-! ### Elementary analytic and real-inequality helpers -/

private lemma tendsto_inv_sqrt_nat :
    Tendsto (fun N : ℕ ↦ 1 / Real.sqrt (N : ℝ)) atTop (𝓝 0) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨M, hM⟩ := exists_nat_gt (1 / ε ^ 2)
  refine ⟨M + 1, fun N hN ↦ ?_⟩
  have hM_lt : 1 / ε ^ 2 < (N : ℝ) := lt_of_lt_of_le hM (by exact_mod_cast Nat.le_of_succ_le hN)
  have hN_pos : (0 : ℝ) < (N : ℝ) := lt_trans (by positivity) hM_lt
  have hsq : 1 / ε < Real.sqrt (N : ℝ) := by
    have h1 : 1 / ε = Real.sqrt (1 / ε ^ 2) := by
      rw [one_div (ε ^ 2), Real.sqrt_inv, Real.sqrt_sq hε.le, one_div]
    rw [h1]
    exact Real.sqrt_lt_sqrt (by positivity) hM_lt
  rw [dist_zero_right, Real.norm_of_nonneg (by positivity)]
  have h2 : 1 / Real.sqrt (N : ℝ) < 1 / (1 / ε) :=
    one_div_lt_one_div_of_lt (by positivity) hsq
  simpa using h2

private lemma log_le_two_sqrt {x : ℝ} (hx : 0 ≤ x) :
    Real.log x ≤ 2 * Real.sqrt x := by
  have h := Real.log_le_rpow_div hx (by norm_num : (0 : ℝ) < 1 / 2)
  rw [ ← Real.sqrt_eq_rpow] at h
  linarith only [h]

private lemma log_sq_le_four_nat {N : ℕ} (hN : 1 ≤ N) :
    (Real.log (N : ℝ)) ^ 2 ≤ 4 * (N : ℝ) := by
  have hN_nn : (0 : ℝ) ≤ (N : ℝ) := Nat.cast_nonneg N
  have hlog_nn : 0 ≤ Real.log (N : ℝ) := Real.log_nonneg (by exact_mod_cast hN)
  have hle : Real.log (N : ℝ) ≤ 2 * Real.sqrt (N : ℝ) := log_le_two_sqrt hN_nn
  calc (Real.log (N : ℝ)) ^ 2
      ≤ (2 * Real.sqrt (N : ℝ)) ^ 2 := pow_le_pow_left₀ hlog_nn hle 2
    _ = 4 * (Real.sqrt (N : ℝ)) ^ 2 := by ring
    _ = 4 * (N : ℝ) := by rw [Real.sq_sqrt hN_nn]

private lemma norm_intervalIntegral_le_of_le {a b C : ℝ} {f : ℝ → ℂ} (hab : a ≤ b)
    (h : ∀ x ∈ Set.Icc a b, ‖f x‖ ≤ C) :
    ‖∫ x in a..b, f x‖ ≤ C * (b - a) := by
  have h1 : ‖∫ x in a..b, f x‖ ≤ C * |b - a| :=
    intervalIntegral.norm_integral_le_of_norm_le_const fun x hx ↦
      h x (Set.uIcc_of_le hab ▸ Set.uIoc_subset_uIcc hx)
  rwa [abs_of_nonneg (sub_nonneg.mpr hab)] at h1

private lemma cosh_div_abs_sinh_le_two {t : ℝ} (ht : 1 ≤ |t|) :
    Real.cosh t / |Real.sinh t| ≤ 2 := by
  set u : ℝ := |t|
  have he : 2 ≤ Real.exp u := by
    have := Real.add_one_le_exp u
    linarith only [ht, this]
  have he_pos : 0 < Real.exp u := Real.exp_pos u
  have hinv : Real.exp (-u) ≤ 1 / 2 := by
    rw [Real.exp_neg, ← one_div]
    exact one_div_le_one_div_of_le (by norm_num) he
  have hsinh_u_pos : 0 < Real.sinh u := by
    rw [Real.sinh_eq]
    linarith only [he, hinv]
  have hcosh_eq : Real.cosh t = Real.cosh u := by
    rcases le_or_gt 0 t with h | h
    · simp [u, abs_of_nonneg h]
    · simp [u, abs_of_neg h, Real.cosh_neg]
  have hsinh_eq : |Real.sinh t| = Real.sinh u := by
    rcases le_or_gt 0 t with h | h
    · rw [show t = u by simp [u, abs_of_nonneg h], abs_of_pos hsinh_u_pos]
    · have ht_eq : t = -u := by simp [u, abs_of_neg h]
      rw [ht_eq, Real.sinh_neg, abs_neg, abs_of_pos hsinh_u_pos]
  rw [hcosh_eq, hsinh_eq, div_le_iff₀ hsinh_u_pos, Real.cosh_eq, Real.sinh_eq]
  linarith only [he, hinv]

private lemma cos_ne_and_norm_tan_le_two_of_twelve_le_abs_im {z : ℂ} (hz : 12 ≤ |z.im|) :
    Complex.cos ((Real.pi : ℂ) * (1 - z) / 2) ≠ 0 ∧
      ‖Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)‖ ≤ 2 := by
  set u : ℂ := (Real.pi : ℂ) * (1 - z) / 2
  have hu_eq : u = ((Real.pi / 2 : ℝ) : ℂ) * (1 - z) := by simp [u]; ring
  have hu_im : u.im = -(Real.pi / 2) * z.im := by
    rw [hu_eq]
    simp only [Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im, Complex.sub_im,
      Complex.sub_re, Complex.one_im]
    ring
  have hpi_ge : (2 : ℝ) ≤ Real.pi := Real.two_le_pi
  have hu_abs : 1 ≤ |u.im| := by
    rw [hu_im, abs_mul, abs_neg, abs_of_pos (by linarith only [hpi_ge])]
    nlinarith [hz, hpi_ge]
  have hu_ne : u.im ≠ 0 := fun h0 ↦ by rw [h0, abs_zero] at hu_abs; linarith only [hu_abs]
  exact ⟨cos_ne_zero_of_im_ne_zero hu_ne,
    (norm_tan_le_of_im_ne_zero hu_ne).trans (cosh_div_abs_sinh_le_two hu_abs)⟩

/-! ### Difference kernel `K_sw`, contour integrand `g_sw`, simple poles, and residues -/

noncomputable def K_sw (s w z : ℂ) : ℂ := 1 / (s - z) - 1 / (w - z)

noncomputable def g_sw (s w z : ℂ) : ℂ := F z * K_sw s w z

private lemma analyticAt_K_sw {s w z : ℂ} (hzs : z ≠ s) (hzw : z ≠ w) :
    AnalyticAt ℂ (K_sw s w) z := by
  have h1 : s - z ≠ 0 := sub_ne_zero.mpr hzs.symm
  have h2 : w - z ≠ 0 := sub_ne_zero.mpr hzw.symm
  change AnalyticAt ℂ (fun u ↦ 1 / (s - u) - 1 / (w - u)) z
  exact (analyticAt_const.div (analyticAt_const.sub analyticAt_id) h1).sub
    (analyticAt_const.div (analyticAt_const.sub analyticAt_id) h2)

private lemma meromorphicOn_K_sw (s w : ℂ) : MeromorphicOn (K_sw s w) Set.univ := by
  intro z _
  have hEq : K_sw s w = (fun u ↦ (s - u)⁻¹) - (fun u ↦ (w - u)⁻¹) := by
    funext u; simp [K_sw, one_div]
  rw [hEq]
  exact (((analyticAt_const.sub analyticAt_id).meromorphicAt).inv).sub
    (((analyticAt_const.sub analyticAt_id).meromorphicAt).inv)

private lemma meromorphicOn_g_sw (s w : ℂ) : MeromorphicOn (g_sw s w) Set.univ := by
  intro z hz
  have hEq : g_sw s w = F * K_sw s w := rfl
  rw [hEq]
  exact (meromorphicOn_F z hz).mul (meromorphicOn_K_sw s w z hz)

private lemma meromorphicOrderAt_K_sw_at_s {s w : ℂ} (hsw : s ≠ w) :
    meromorphicOrderAt (K_sw s w) s = (-1 : ℤ) := by
  rw [meromorphicOrderAt_eq_int_iff (meromorphicOn_K_sw s w s trivial)]
  have hws : w - s ≠ 0 := sub_ne_zero.mpr hsw.symm
  refine ⟨fun z ↦ -1 - (z - s) / (w - z), ?_, ?_, ?_⟩
  · exact analyticAt_const.sub
      ((analyticAt_id.sub analyticAt_const).div (analyticAt_const.sub analyticAt_id) hws)
  · simp [sub_self]
  · have hopen : {w}ᶜ ∈ 𝓝[≠] s :=
      nhdsWithin_le_nhds (isOpen_compl_singleton.mem_nhds (show s ∈ ({w}ᶜ : Set ℂ) from hsw))
    filter_upwards [self_mem_nhdsWithin, hopen] with z hzs hzw
    have h1 : s - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzs)
    have h2 : z - s ≠ 0 := sub_ne_zero.mpr hzs
    have h3 : w - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzw)
    simp only [K_sw, zpow_neg_one, smul_eq_mul]
    field_simp
    ring

private lemma meromorphicOrderAt_K_sw_at_w {s w : ℂ} (hsw : s ≠ w) :
    meromorphicOrderAt (K_sw s w) w = (-1 : ℤ) := by
  have hEq : K_sw s w = - K_sw w s := by
    funext z; simp only [ Pi.neg_apply, K_sw ]; ring
  have hneg : - K_sw w s = (fun _ : ℂ ↦ (-1 : ℂ)) • K_sw w s := by
    funext z; simp
  rw [hEq, hneg, meromorphicOrderAt_smul analyticAt_const.meromorphicAt
    (meromorphicOn_K_sw w s w trivial),
    meromorphicOrderAt_eq_zero_of_analytic analyticAt_const (by norm_num),
    zero_add]
  exact meromorphicOrderAt_K_sw_at_s hsw.symm

private lemma hasSimplePolesOn_g_sw {s w : ℂ} (hs1 : s ≠ 1) (hw1 : w ≠ 1)
    (hζs : riemannZeta s ≠ 0) (hζw : riemannZeta w ≠ 0) (hsw : s ≠ w) :
    HasSimplePolesOn (g_sw s w) Set.univ := by
  intro z _
  have hmul : meromorphicOrderAt (g_sw s w) z
      = meromorphicOrderAt F z + meromorphicOrderAt (K_sw s w) z :=
    meromorphicOrderAt_mul (meromorphicOn_F z trivial) (meromorphicOn_K_sw s w z trivial)
  rw [hmul]
  rcases eq_or_ne z s with rfl | hzs
  · rw [meromorphicOrderAt_K_sw_at_s hsw]
    exact le_add_of_nonneg_left (analyticAt_F_of_zeta_ne_zero hs1 hζs).meromorphicOrderAt_nonneg
  · rcases eq_or_ne z w with rfl | hzw
    · rw [meromorphicOrderAt_K_sw_at_w hsw]
      exact le_add_of_nonneg_left (analyticAt_F_of_zeta_ne_zero hw1 hζw).meromorphicOrderAt_nonneg
    · exact le_trans (hasSimplePolesOn_F_univ z trivial)
        (le_add_of_nonneg_right (analyticAt_K_sw hzs hzw).meromorphicOrderAt_nonneg)

private lemma pole_g_sw_imp {s w z : ℂ} (hp : meromorphicOrderAt (g_sw s w) z < 0) :
    z = s ∨ z = w ∨ riemannZeta₁ z = 0 := by
  by_contra hnot
  push Not at hnot
  obtain ⟨hzs, hzw, hζ1⟩ := hnot
  have han : AnalyticAt ℂ (g_sw s w) z :=
    (analyticAt_F hζ1).mul (analyticAt_K_sw hzs hzw)
  exact (not_lt_of_ge han.meromorphicOrderAt_nonneg) hp

private lemma norm_K_sw_le {s w z : ℂ} {N : ℝ} (hN : 0 < N)
    (hs : ‖s‖ ≤ N / 2) (hw : ‖w‖ ≤ N / 2) (hz : N ≤ ‖z‖) :
    ‖K_sw s w z‖ ≤ 4 * ‖w - s‖ / N ^ 2 := by
  have hsz : N / 2 ≤ ‖s - z‖ := by
    have htri := norm_sub_norm_le z s
    rw [norm_sub_rev] at htri
    linarith only [hs, hz, htri]
  have hwz : N / 2 ≤ ‖w - z‖ := by
    have htri := norm_sub_norm_le z w
    rw [norm_sub_rev] at htri
    linarith only [hw, hz, htri]
  have hsz_ne : s - z ≠ 0 := norm_ne_zero_iff.mp (by linarith only [hN, hsz])
  have hwz_ne : w - z ≠ 0 := norm_ne_zero_iff.mp (by linarith only [hN, hwz])
  have hEq : K_sw s w z = (w - s) / ((s - z) * (w - z)) := by
    simp only [K_sw]; field_simp; ring
  rw [hEq, norm_div, norm_mul]
  calc ‖w - s‖ / (‖s - z‖ * ‖w - z‖)
      ≤ ‖w - s‖ / ((N / 2) * (N / 2)) :=
        div_le_div_of_nonneg_left (norm_nonneg _) (by positivity)
          (mul_le_mul hsz hwz (by positivity) (norm_nonneg _))
    _ = 4 * ‖w - s‖ / N ^ 2 := by ring

private lemma F_eq_at_regular {u : ℂ} (hu1 : u ≠ 1) (hζu : riemannZeta u ≠ 0) :
    F u = -(deriv riemannZeta u / riemannZeta u + 1 / (u - 1)) := by
  simp only [F]
  rw [logDeriv_riemannZeta₁_eq hu1 hζu, logDeriv_apply, one_div]

private lemma residue_g_at_s {s w : ℂ} (hs1 : s ≠ 1) (hζs : riemannZeta s ≠ 0) (hsw : s ≠ w) :
    residue (g_sw s w) s = deriv riemannZeta s / riemannZeta s + 1 / (s - 1) := by
  apply residue_eq_of_tendsto
  have hws : w - s ≠ 0 := sub_ne_zero.mpr hsw.symm
  have hcont : ContinuousAt (fun z ↦ F z * (-1 - (z - s) / (w - z))) s :=
    (analyticAt_F_of_zeta_ne_zero hs1 hζs).continuousAt.mul
      (continuousAt_const.sub
        ((continuousAt_id.sub continuousAt_const).div
          (continuousAt_const.sub continuousAt_id) hws))
  have hlim := hcont.tendsto.mono_left (nhdsWithin_le_nhds (s := {s}ᶜ))
  have hval : F s * (-1 - (s - s) / (w - s))
      = deriv riemannZeta s / riemannZeta s + 1 / (s - 1) := by
    rw [F_eq_at_regular hs1 hζs, sub_self, zero_div]
    ring
  rw [hval] at hlim
  refine hlim.congr' ?_
  have hopen : {w}ᶜ ∈ 𝓝[≠] s :=
    nhdsWithin_le_nhds (isOpen_compl_singleton.mem_nhds (show s ∈ ({w}ᶜ : Set ℂ) from hsw))
  filter_upwards [self_mem_nhdsWithin, hopen] with z hzs hzw
  have h1 : s - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzs)
  have h2 : w - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzw)
  simp only [g_sw, K_sw]
  field_simp
  ring

private lemma residue_g_at_w {s w : ℂ} (hw1 : w ≠ 1) (hζw : riemannZeta w ≠ 0) (hsw : s ≠ w) :
    residue (g_sw s w) w = -(deriv riemannZeta w / riemannZeta w + 1 / (w - 1)) := by
  apply residue_eq_of_tendsto
  have hsw' : s - w ≠ 0 := sub_ne_zero.mpr hsw
  have hcont : ContinuousAt (fun z ↦ F z * ((z - w) / (s - z) + 1)) w :=
    (analyticAt_F_of_zeta_ne_zero hw1 hζw).continuousAt.mul
      (((continuousAt_id.sub continuousAt_const).div
        (continuousAt_const.sub continuousAt_id) hsw').add continuousAt_const)
  have hlim := hcont.tendsto.mono_left (nhdsWithin_le_nhds (s := {w}ᶜ))
  have hval : F w * ((w - w) / (s - w) + 1)
      = -(deriv riemannZeta w / riemannZeta w + 1 / (w - 1)) := by
    rw [F_eq_at_regular hw1 hζw, sub_self, zero_div]
    ring
  rw [hval] at hlim
  refine hlim.congr' ?_
  have hopen : {s}ᶜ ∈ 𝓝[≠] w :=
    nhdsWithin_le_nhds (isOpen_compl_singleton.mem_nhds (show w ∈ ({s}ᶜ : Set ℂ) from hsw.symm))
  filter_upwards [self_mem_nhdsWithin, hopen] with z hzw hzs
  have h1 : s - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzs)
  have h2 : w - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hzw)
  simp only [g_sw, K_sw]
  field_simp
  ring

private lemma residue_g_at_zero {s w u : ℂ} (hu1 : u ≠ 1) (hus : u ≠ s) (huw : u ≠ w) :
    residue (g_sw s w) u = -((1 / (s - u) - 1 / (w - u)) * (IEANTN.zetaOrder u : ℂ)) := by
  have h := residue_eq_mul_of_tendsto (h := g_sw s w)
    (analyticAt_K_sw hus huw).continuousAt (tendsto_sub_mul_F hu1)
    (Filter.Eventually.of_forall fun z ↦ mul_comm (F z) (K_sw s w z))
  rw [h]
  simp only [K_sw]
  ring

/-! ### Pointwise bounds on `F` across the rectangle sides -/

private lemma norm_F_le_of_two_le_re {M₁ : ℝ}
    (hM₁ : ∀ u : ℂ, 9 / 8 ≤ u.re → ‖deriv riemannZeta u / riemannZeta u‖ ≤ M₁)
    {z : ℂ} (hz : 2 ≤ z.re) :
    ‖F z‖ ≤ M₁ + 1 := by
  have hz1 : z ≠ 1 := fun h ↦ by rw [h] at hz; norm_num at hz
  have hζ : riemannZeta z ≠ 0 := riemannZeta_ne_zero_of_one_lt_re (by linarith only [hz])
  rw [F_eq_at_regular hz1 hζ, norm_neg]
  have hsub : 1 ≤ ‖z - 1‖ := by
    have hre : 1 ≤ |(z - 1).re| := by
      simp only [Complex.sub_re, Complex.one_re]
      exact le_trans (by linarith only [hz]) (le_abs_self _)
    exact hre.trans (Complex.abs_re_le_norm (z - 1))
  have hinv : ‖1 / (z - 1)‖ ≤ 1 := by
    rw [norm_div, norm_one]
    exact div_le_one_of_le₀ hsub (norm_nonneg _)
  calc ‖deriv riemannZeta z / riemannZeta z + 1 / (z - 1)‖
      ≤ ‖deriv riemannZeta z / riemannZeta z‖ + ‖1 / (z - 1)‖ := norm_add_le _ _
    _ ≤ M₁ + 1 := add_le_add (hM₁ z (by linarith only [hz])) hinv

private lemma norm_clog_one_sub_le {N : ℕ} (hN : 2 ≤ N) {z : ℂ}
    (hre_lo : -1 - 2 * (N : ℝ) ≤ z.re) (hre_hi : z.re ≤ -1 / 8)
    (him : |z.im| ≤ (N : ℝ) + 1) :
    ‖Complex.log (1 - z)‖ ≤ 10 * Real.sqrt (N : ℝ) := by
  have hN_real : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hN_nn : (0 : ℝ) ≤ (N : ℝ) := by linarith only [hN_real]
  have hsqrt1 : 1 ≤ Real.sqrt (N : ℝ) := by
    rw [← Real.sqrt_one]
    exact Real.sqrt_le_sqrt (by linarith only [hN_real])
  have hnorm_lo : 1 ≤ ‖1 - z‖ := by
    have hre : 1 ≤ |(1 - z).re| := by
      simp only [Complex.sub_re, Complex.one_re]
      exact le_trans (by linarith only [hre_hi]) (le_abs_self _)
    exact hre.trans (Complex.abs_re_le_norm (1 - z))
  have hnorm_hi : ‖1 - z‖ ≤ 9 * (N : ℝ) := by
    have htri := Complex.norm_le_abs_re_add_abs_im (1 - z)
    have hre_abs : |(1 - z).re| ≤ 3 * (N : ℝ) := by
      simp only [Complex.sub_re, Complex.one_re]
      rw [abs_of_nonneg (by linarith only [hre_hi])]
      linarith only [hre_lo, hN_real]
    have him_abs : |(1 - z).im| ≤ 2 * (N : ℝ) := by
      simp only [Complex.sub_im, Complex.one_im, zero_sub, abs_neg]
      linarith only [him, hN_real]
    linarith only [htri, hre_abs, him_abs, hN_real]
  have hlog_re : |Real.log ‖1 - z‖| ≤ 6 * Real.sqrt (N : ℝ) := by
    rw [abs_of_nonneg (Real.log_nonneg hnorm_lo)]
    calc Real.log ‖1 - z‖
        ≤ 2 * Real.sqrt ‖1 - z‖ := log_le_two_sqrt (norm_nonneg _)
      _ ≤ 2 * Real.sqrt (9 * (N : ℝ)) :=
          mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt hnorm_hi) (by norm_num)
      _ = 2 * (3 * Real.sqrt (N : ℝ)) := by
          have h9 : Real.sqrt 9 = 3 := by
            rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
          rw [Real.sqrt_mul (by norm_num), h9]
      _ = 6 * Real.sqrt (N : ℝ) := by ring
  have harg : |Complex.arg (1 - z)| ≤ 4 :=
    (Complex.abs_arg_le_pi (1 - z)).trans Real.pi_le_four
  have htri := Complex.norm_le_abs_re_add_abs_im (Complex.log (1 - z))
  rw [Complex.log_re, Complex.log_im] at htri
  linarith only [htri, hlog_re, harg, hsqrt1]

private lemma norm_F_le_left {M₁ : ℝ}
    (hM₁ : ∀ u : ℂ, 9 / 8 ≤ u.re → ‖deriv riemannZeta u / riemannZeta u‖ ≤ M₁)
    {N : ℕ} (hN : 2 ≤ N) {z : ℂ}
    (hre_lo : -1 - 2 * (N : ℝ) ≤ z.re) (hre_hi : z.re ≤ -1 / 8)
    (him : |z.im| ≤ (N : ℝ) + 1)
    (hζ : riemannZeta z ≠ 0)
    (hcos : Complex.cos ((Real.pi : ℂ) * (1 - z) / 2) ≠ 0)
    (htan : ‖Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)‖ ≤ 2) :
    ‖F z‖ ≤ (M₁ + 1 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi)
      + 10 * Real.sqrt (N : ℝ) + (1 + 3 * |z.im|) / (1 - z.re) := by
  have hz1 : z ≠ 1 := fun h ↦ by rw [h] at hre_hi; norm_num at hre_hi
  rw [F_eq_at_regular hz1 hζ, norm_neg,
    logDeriv_ladder_form (by linarith only [hre_hi]) hcos]
  have h1z_re : 9 / 8 ≤ (1 - z).re := by
    simp only [Complex.sub_re, Complex.one_re]; linarith only [hre_hi]
  have hb_zeta : ‖-(deriv riemannZeta (1 - z) / riemannZeta (1 - z))‖ ≤ M₁ := by
    rw [norm_neg]; exact hM₁ (1 - z) h1z_re
  have hb_inv : ‖1 / (z - 1)‖ ≤ 1 := by
    have h1 : 1 ≤ ‖z - 1‖ := by
      have hre : 1 ≤ |(z - 1).re| := by
        simp only [Complex.sub_re, Complex.one_re]
        rw [abs_of_neg (by linarith only [hre_hi])]
        linarith only [hre_hi]
      exact hre.trans (Complex.abs_re_le_norm (z - 1))
    rw [norm_div, norm_one]
    exact div_le_one_of_le₀ h1 (norm_nonneg _)
  have hb_tan : ‖((Real.pi : ℂ) / 2) * Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)‖ ≤ Real.pi := by
    rw [norm_mul, norm_div, Complex.norm_real, Real.norm_of_nonneg Real.pi_pos.le, norm_ofNat]
    have hpi_pos : 0 ≤ Real.pi / 2 := by positivity
    calc (Real.pi / 2) * ‖Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)‖
        ≤ (Real.pi / 2) * 2 := mul_le_mul_of_nonneg_left htan hpi_pos
      _ = Real.pi := by ring
  have hb_dig : ‖Complex.digamma (1 - z)‖
      ≤ 10 * Real.sqrt (N : ℝ) + (1 + 3 * |z.im|) / (1 - z.re) := by
    have hd := norm_digamma_sub_log_le_div_re (w := 1 - z) (by linarith only [h1z_re])
    have him_eq : |(1 - z).im| = |z.im| := by simp
    have hre_eq : (1 - z).re = 1 - z.re := by simp
    rw [him_eq, hre_eq] at hd
    have hlog := norm_clog_one_sub_le hN hre_lo hre_hi him
    have hsplit : Complex.digamma (1 - z)
        = (Complex.digamma (1 - z) - Complex.log (1 - z)) + Complex.log (1 - z) := by ring
    rw [hsplit]
    have htri := norm_add_le (Complex.digamma (1 - z) - Complex.log (1 - z)) (Complex.log (1 - z))
    linarith only [htri, hd, hlog]
  set A := -(deriv riemannZeta (1 - z) / riemannZeta (1 - z))
  set B := Complex.log (2 * (Real.pi : ℂ))
  set C := Complex.digamma (1 - z)
  set D := ((Real.pi : ℂ) / 2) * Complex.tan ((Real.pi : ℂ) * (1 - z) / 2)
  set E := 1 / (z - 1)
  have ht1 := norm_add_le (A + B - C + D) E
  have ht2 := norm_add_le (A + B - C) D
  have ht3 := norm_sub_le (A + B) C
  have ht4 := norm_add_le A B
  linarith only [ht1, ht2, ht3, ht4, hb_zeta, hb_inv, hb_tan, hb_dig]

/-! ### Segment integral `O(1 / √N)` bounds -/

private lemma norm_VIntegral_right_le {M₁ : ℝ} (hM₁_nn : 0 ≤ M₁)
    (hM₁ : ∀ u : ℂ, 9 / 8 ≤ u.re → ‖deriv riemannZeta u / riemannZeta u‖ ≤ M₁)
    {s w : ℂ} {N : ℕ} (hN : 20 ≤ N)
    (hs : ‖s‖ ≤ (N : ℝ) / 2) (hw : ‖w‖ ≤ (N : ℝ) / 2)
    {T : ℝ} (hT_pos : 0 ≤ T) (hT_hi : T ≤ (N : ℝ) + 3 / 4) :
    ‖VIntegral (g_sw s w) (2 + 2 * (N : ℝ)) (-T) T‖
      ≤ (12 * (M₁ + 1) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
  have hN_real : (20 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hN_pos : (0 : ℝ) < (N : ℝ) := by linarith only [hN_real]
  have hsqrt_pos : 0 < Real.sqrt (N : ℝ) := Real.sqrt_pos.mpr hN_pos
  have hsqrt_le : Real.sqrt (N : ℝ) ≤ (N : ℝ) := by
    rw [Real.sqrt_le_iff]
    exact ⟨hN_pos.le, by nlinarith [hN_real]⟩
  rw [VIntegral, norm_smul, Complex.norm_I, one_mul]
  have hbound : ‖∫ y in (-T)..T, g_sw s w (((2 + 2 * (N : ℝ) : ℝ) : ℂ) + (y : ℂ) * I)‖
      ≤ ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (T - (-T)) := by
    refine norm_intervalIntegral_le_of_le (by linarith only [hT_pos]) fun y _ ↦ ?_
    set z : ℂ := ((2 + 2 * (N : ℝ) : ℝ) : ℂ) + (y : ℂ) * I
    have hz_re : z.re = 2 + 2 * (N : ℝ) := by simp [z]
    have hz_norm : (N : ℝ) ≤ ‖z‖ := by
      have hre : (N : ℝ) ≤ |z.re| := by
        rw [hz_re, abs_of_nonneg (by linarith only [hN_real])]
        linarith only [hN_real]
      exact hre.trans (Complex.abs_re_le_norm z)
    rw [g_sw, norm_mul]
    exact mul_le_mul (norm_F_le_of_two_le_re hM₁ (by linarith only [hz_re, hN_real]))
      (norm_K_sw_le hN_pos hs hw hz_norm) (norm_nonneg _) (by linarith only [hM₁_nn])
  have h2T : T - (-T) ≤ 3 * (N : ℝ) := by linarith only [hT_hi, hN_real]
  have hstep : ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (T - (-T))
      ≤ (12 * (M₁ + 1) * ‖w - s‖) * (1 / (N : ℝ)) := by
    calc ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (T - (-T))
        ≤ ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (3 * (N : ℝ)) :=
          mul_le_mul_of_nonneg_left h2T (by positivity)
      _ = (12 * (M₁ + 1) * ‖w - s‖) * ((N : ℝ) / (N : ℝ) ^ 2) := by ring
      _ = (12 * (M₁ + 1) * ‖w - s‖) * (1 / (N : ℝ)) := by
          congr 1; field_simp
  have hinv : 1 / (N : ℝ) ≤ 1 / Real.sqrt (N : ℝ) :=
    one_div_le_one_div_of_le hsqrt_pos hsqrt_le
  exact hbound.trans (hstep.trans (mul_le_mul_of_nonneg_left hinv (by positivity)))

private lemma norm_VIntegral_left_le {M₁ : ℝ} (hM₁_nn : 0 ≤ M₁)
    (hM₁ : ∀ u : ℂ, 9 / 8 ≤ u.re → ‖deriv riemannZeta u / riemannZeta u‖ ≤ M₁)
    {s w : ℂ} {N : ℕ} (hN : 20 ≤ N)
    (hs : ‖s‖ ≤ (N : ℝ) / 2) (hw : ‖w‖ ≤ (N : ℝ) / 2)
    {T : ℝ} (hT_pos : 0 ≤ T) (hT_hi : T ≤ (N : ℝ) + 3 / 4) :
    ‖VIntegral (g_sw s w) (sigmaZeta (N + 1)) (-T) T‖
      ≤ (12 * (M₁ + 13 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi) * ‖w - s‖)
          * (1 / Real.sqrt (N : ℝ)) := by
  have hN_real : (20 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hN_pos : (0 : ℝ) < (N : ℝ) := by linarith only [hN_real]
  have hsqrt1 : 1 ≤ Real.sqrt (N : ℝ) := by
    rw [← Real.sqrt_one]; exact Real.sqrt_le_sqrt (by linarith only [hN_real])
  set C₀ : ℝ := M₁ + 1 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi
  have hC₀_nn : 0 ≤ C₀ := by
    have hlog_nn := norm_nonneg (Complex.log (2 * (Real.pi : ℂ)))
    have hpi_pos := Real.pi_pos
    dsimp only [C₀]; linarith only [hM₁_nn, hlog_nn, hpi_pos]
  have hsig : sigmaZeta (N + 1) = -1 - 2 * (N : ℝ) := by
    simp only [sigmaZeta, Nat.cast_add, Nat.cast_one]; ring
  rw [VIntegral, norm_smul, Complex.norm_I, one_mul]
  have hbound : ‖∫ y in (-T)..T, g_sw s w (((sigmaZeta (N + 1)) : ℂ) + (y : ℂ) * I)‖
      ≤ (((C₀ + 12) * Real.sqrt (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (T - (-T)) := by
    refine norm_intervalIntegral_le_of_le (by linarith only [hT_pos]) fun y hy ↦ ?_
    set z : ℂ := ((sigmaZeta (N + 1)) : ℂ) + (y : ℂ) * I
    have hz_re : z.re = sigmaZeta (N + 1) := by simp [z]
    have hz_re_val : z.re = -1 - 2 * (N : ℝ) := hz_re.trans hsig
    have hz_im : |z.im| ≤ T := by
      simp only [z, Complex.add_im, Complex.ofReal_im, Complex.mul_im, Complex.ofReal_re,
        Complex.I_im, Complex.I_re, mul_one, mul_zero, add_zero, zero_add]
      exact abs_le.mpr hy
    have hz_norm : (N : ℝ) ≤ ‖z‖ := by
      have hre : (N : ℝ) ≤ |z.re| := by
        rw [hz_re_val, abs_of_neg (by linarith only [hN_real])]
        linarith only [hN_real]
      exact hre.trans (Complex.abs_re_le_norm z)
    have hF_pt : ‖F z‖ ≤ (C₀ + 12) * Real.sqrt (N : ℝ) := by
      have h1 := norm_F_le_left hM₁ (N := N) (by omega)
        (by linarith only [hz_re_val]) (by linarith only [hz_re_val, hN_real])
        (by linarith only [hz_im, hT_hi])
        (riemannZeta_ne_zero_on_column (Nat.succ_pos N) hz_re)
        (cos_ne_zero_on_column hz_re)
        ((norm_tan_le_one_on_column hz_re).trans (by norm_num))
      have hdiv_le : (1 + 3 * |z.im|) / (1 - z.re) ≤ 2 := by
        have hden : 2 * (N : ℝ) ≤ 1 - z.re := by linarith only [hz_re_val]
        have hnum : 1 + 3 * |z.im| ≤ 4 * (N : ℝ) := by linarith only [hz_im, hT_hi, hN_real]
        rw [div_le_iff₀ (by linarith only [hN_pos, hden])]
        linarith only [hden, hnum]
      have hC₀_le : C₀ ≤ C₀ * Real.sqrt (N : ℝ) := le_mul_of_one_le_right hC₀_nn hsqrt1
      have h2_le : (2 : ℝ) ≤ 2 * Real.sqrt (N : ℝ) := by linarith only [hsqrt1]
      linarith only [h1, hdiv_le, hC₀_le, h2_le]
    rw [g_sw, norm_mul]
    exact mul_le_mul hF_pt (norm_K_sw_le hN_pos hs hw hz_norm) (norm_nonneg _)
      (mul_nonneg (by linarith only [hC₀_nn]) (Real.sqrt_nonneg _))
  have h2T : T - (-T) ≤ 3 * (N : ℝ) := by linarith only [hT_hi, hN_real]
  have hsq_eq : Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2 = 1 / Real.sqrt (N : ℝ) := by
    have hsqrt_ne : Real.sqrt (N : ℝ) ≠ 0 := (Real.sqrt_pos.mpr hN_pos).ne'
    rw [div_eq_div_iff (pow_ne_zero 2 hN_pos.ne') hsqrt_ne]
    calc Real.sqrt (N : ℝ) * (N : ℝ) * Real.sqrt (N : ℝ)
        = (Real.sqrt (N : ℝ) * Real.sqrt (N : ℝ)) * (N : ℝ) := by ring
      _ = (N : ℝ) * (N : ℝ) := by rw [Real.mul_self_sqrt hN_pos.le]
      _ = 1 * (N : ℝ) ^ 2 := by ring
  calc ‖∫ y in (-T)..T, g_sw s w (((sigmaZeta (N + 1)) : ℂ) + (y : ℂ) * I)‖
      ≤ (((C₀ + 12) * Real.sqrt (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (3 * (N : ℝ)) :=
        hbound.trans (mul_le_mul_of_nonneg_left h2T
          (mul_nonneg (mul_nonneg (by linarith only [hC₀_nn]) (Real.sqrt_nonneg _))
            (by positivity)))
    _ = (12 * (C₀ + 12) * ‖w - s‖) * (Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2) := by ring
    _ = (12 * (M₁ + 13 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi) * ‖w - s‖)
          * (1 / Real.sqrt (N : ℝ)) := by
        rw [hsq_eq]; dsimp only [C₀]; ring

private lemma norm_HIntegral_horiz_le {M₁ C_H : ℝ} (hM₁_nn : 0 ≤ M₁) (hCH_nn : 0 ≤ C_H)
    (hM₁ : ∀ u : ℂ, 9 / 8 ≤ u.re → ‖deriv riemannZeta u / riemannZeta u‖ ≤ M₁)
    {s w : ℂ} {N : ℕ} (hN : 20 ≤ N)
    (hs : ‖s‖ ≤ (N : ℝ) / 2) (hw : ‖w‖ ≤ (N : ℝ) / 2)
    {y : ℝ} (hy_lo : (N : ℝ) + 1 / 4 ≤ |y|) (hy_hi : |y| ≤ (N : ℝ) + 3 / 4)
    (hzero : ∀ z : ℂ, |z.im| = |y| → riemannZeta z ≠ 0)
    (hstrip : ∀ σ ∈ Set.Icc (-1 / 8 : ℝ) 2,
      ‖F ((σ : ℂ) + (y : ℂ) * I)‖ ≤ C_H * (Real.log (N : ℝ)) ^ 2) :
    ‖HIntegral (g_sw s w) (sigmaZeta (N + 1)) (2 + 2 * (N : ℝ)) y‖
      ≤ ((16 * (M₁ + 15 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi)
          + 48 * C_H + 8 * (M₁ + 1)) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
  have hN_real : (20 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hN_pos : (0 : ℝ) < (N : ℝ) := by linarith only [hN_real]
  have hsqrt_pos : 0 < Real.sqrt (N : ℝ) := Real.sqrt_pos.mpr hN_pos
  have hsqrt1 : 1 ≤ Real.sqrt (N : ℝ) := by
    rw [← Real.sqrt_one]; exact Real.sqrt_le_sqrt (by linarith only [hN_real])
  have hsqrt_le : Real.sqrt (N : ℝ) ≤ (N : ℝ) := by
    rw [Real.sqrt_le_iff]; exact ⟨hN_pos.le, by nlinarith [hN_real]⟩
  set C₀ : ℝ := M₁ + 1 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi
  have hC₀_nn : 0 ≤ C₀ := by
    have hlog_nn := norm_nonneg (Complex.log (2 * (Real.pi : ℂ)))
    have hpi_pos := Real.pi_pos
    dsimp only [C₀]; linarith only [hM₁_nn, hlog_nn, hpi_pos]
  set x₀ : ℝ := sigmaZeta (N + 1)
  set x₁ : ℝ := -Real.sqrt (N : ℝ)
  set x₂ : ℝ := -1 / 8
  set x₃ : ℝ := 2
  set x₄ : ℝ := 2 + 2 * (N : ℝ)
  have hx₀_eq : x₀ = -1 - 2 * (N : ℝ) := by
    simp only [x₀, sigmaZeta, Nat.cast_add, Nat.cast_one]; ring
  have hx01 : x₀ ≤ x₁ := by dsimp only [x₁]; linarith only [hx₀_eq, hsqrt_le, hN_real]
  have hx12 : x₁ ≤ x₂ := by dsimp only [x₁, x₂]; linarith only [hsqrt1]
  have hx23 : x₂ ≤ x₃ := by norm_num [x₂, x₃]
  have hx34 : x₃ ≤ x₄ := by dsimp only [x₃, x₄]; linarith only [hN_real]
  set fy : ℝ → ℂ := fun x ↦ g_sw s w ((x : ℂ) + (y : ℂ) * I)
  have hfy_im : ∀ x : ℝ, (((x : ℂ) + (y : ℂ) * I)).im = y := fun x ↦ by simp
  have hfy_norm : ∀ x : ℝ, (N : ℝ) ≤ ‖(x : ℂ) + (y : ℂ) * I‖ := fun x ↦ by
    have him : |(((x : ℂ) + (y : ℂ) * I)).im| ≤ ‖(x : ℂ) + (y : ℂ) * I‖ :=
      Complex.abs_im_le_norm _
    rw [hfy_im] at him
    linarith only [hy_lo, him]
  have hfy_cont : Continuous fy := by
    rw [continuous_iff_continuousAt]
    intro x
    set z : ℂ := (x : ℂ) + (y : ℂ) * I
    have hz_norm : (N : ℝ) ≤ ‖z‖ := hfy_norm x
    have hz1 : z ≠ 1 := fun h ↦ by
      have him1 := congrArg Complex.im h
      simp only [z, Complex.add_im, Complex.ofReal_im, Complex.mul_im, Complex.ofReal_re,
        Complex.I_im, Complex.I_re, mul_one, mul_zero, zero_add, Complex.one_im] at him1
      have hy0 : y = 0 := by linarith only [him1]
      rw [hy0, abs_zero] at hy_lo
      linarith only [hN_real, hy_lo]
    have hzs : z ≠ s := fun h ↦ by rw [h] at hz_norm; linarith only [hs, hz_norm, hN_pos]
    have hzw : z ≠ w := fun h ↦ by rw [h] at hz_norm; linarith only [hw, hz_norm, hN_pos]
    have hζz : riemannZeta z ≠ 0 := hzero z (by rw [hfy_im])
    have hg_cont : ContinuousAt (g_sw s w) z :=
      (analyticAt_F_of_zeta_ne_zero hz1 hζz).continuousAt.mul
        (analyticAt_K_sw hzs hzw).continuousAt
    have hpath : Continuous (fun t : ℝ ↦ (t : ℂ) + (y : ℂ) * I) := by fun_prop
    exact ContinuousAt.comp (g := g_sw s w) (f := fun t : ℝ ↦ (t : ℂ) + (y : ℂ) * I)
      hg_cont hpath.continuousAt
  have hsplit : HIntegral (g_sw s w) x₀ x₄ y
      = (∫ x in x₀..x₁, fy x) + (∫ x in x₁..x₂, fy x)
        + (∫ x in x₂..x₃, fy x) + (∫ x in x₃..x₄, fy x) := by
    rw [HIntegral]
    change ∫ x in x₀..x₄, fy x = _
    rw [← intervalIntegral.integral_add_adjacent_intervals
          (hfy_cont.intervalIntegrable x₀ x₃) (hfy_cont.intervalIntegrable x₃ x₄),
        ← intervalIntegral.integral_add_adjacent_intervals
          (hfy_cont.intervalIntegrable x₀ x₂) (hfy_cont.intervalIntegrable x₂ x₃),
        ← intervalIntegral.integral_add_adjacent_intervals
          (hfy_cont.intervalIntegrable x₀ x₁) (hfy_cont.intervalIntegrable x₁ x₂)]
  have hsq_eq : Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2 = 1 / Real.sqrt (N : ℝ) := by
    rw [div_eq_div_iff (pow_ne_zero 2 hN_pos.ne') hsqrt_pos.ne']
    calc Real.sqrt (N : ℝ) * (N : ℝ) * Real.sqrt (N : ℝ)
        = (Real.sqrt (N : ℝ) * Real.sqrt (N : ℝ)) * (N : ℝ) := by ring
      _ = (N : ℝ) * (N : ℝ) := by rw [Real.mul_self_sqrt hN_pos.le]
      _ = 1 * (N : ℝ) ^ 2 := by ring
  -- Subinterval 1: `[x₀, x₁] = [-1 - 2N, -√N]`
  have hI1 : ‖∫ x in x₀..x₁, fy x‖
      ≤ (12 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
    have hb : ‖∫ x in x₀..x₁, fy x‖
        ≤ (((C₀ + 14) * Real.sqrt (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (x₁ - x₀) := by
      refine norm_intervalIntegral_le_of_le hx01 fun x hx ↦ ?_
      set z : ℂ := (x : ℂ) + (y : ℂ) * I
      have hz_re : z.re = x := by simp [z]
      have hz_im : z.im = y := hfy_im x
      obtain ⟨hcos, htan⟩ := cos_ne_and_norm_tan_le_two_of_twelve_le_abs_im (z := z)
        (by rw [hz_im]; linarith only [hN_real, hy_lo])
      have hF1 := norm_F_le_left hM₁ (N := N) (by omega)
        (by linarith only [hz_re, hx.1, hx₀_eq])
        (by dsimp only [x₁] at hx; linarith only [hz_re, hx.2, hsqrt1])
        (by rw [hz_im]; linarith only [hy_hi])
        (hzero z (by rw [hz_im])) hcos htan
      have hdiv_le : (1 + 3 * |z.im|) / (1 - z.re) ≤ 4 * Real.sqrt (N : ℝ) := by
        have hden : Real.sqrt (N : ℝ) ≤ 1 - z.re := by
          dsimp only [x₁] at hx; linarith only [hz_re, hx.2]
        have hnum : 1 + 3 * |z.im| ≤ 4 * (N : ℝ) := by
          rw [hz_im]; linarith only [hy_hi, hN_real]
        rw [div_le_iff₀ (by linarith only [hsqrt_pos, hden])]
        calc 1 + 3 * |z.im| ≤ 4 * (N : ℝ) := hnum
          _ = 4 * Real.sqrt (N : ℝ) * Real.sqrt (N : ℝ) := by
              rw [mul_assoc, Real.mul_self_sqrt hN_pos.le]
          _ ≤ 4 * Real.sqrt (N : ℝ) * (1 - z.re) :=
              mul_le_mul_of_nonneg_left hden (by positivity)
      have hC₀_le : C₀ ≤ C₀ * Real.sqrt (N : ℝ) := le_mul_of_one_le_right hC₀_nn hsqrt1
      have hF_pt : ‖F z‖ ≤ (C₀ + 14) * Real.sqrt (N : ℝ) := by
        linarith only [hF1, hdiv_le, hC₀_le]
      rw [show fy x = F z * K_sw s w z from rfl, norm_mul]
      exact mul_le_mul hF_pt (norm_K_sw_le hN_pos hs hw (hfy_norm x)) (norm_nonneg _)
        (mul_nonneg (by linarith only [hC₀_nn]) (Real.sqrt_nonneg _))
    have hlen : x₁ - x₀ ≤ 3 * (N : ℝ) := by
      dsimp only [x₁]; linarith only [hx₀_eq, hsqrt_pos, hN_real]
    calc ‖∫ x in x₀..x₁, fy x‖
        ≤ (((C₀ + 14) * Real.sqrt (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (3 * (N : ℝ)) :=
          hb.trans (mul_le_mul_of_nonneg_left hlen
            (mul_nonneg (mul_nonneg (by linarith only [hC₀_nn]) (Real.sqrt_nonneg _))
              (by positivity)))
      _ = (12 * (C₀ + 14) * ‖w - s‖) * (Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2) := by ring
      _ = (12 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by rw [hsq_eq]
  -- Subinterval 2: `[x₁, x₂] = [-√N, -1/8]`
  have hI2 : ‖∫ x in x₁..x₂, fy x‖
      ≤ (4 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
    have hb : ‖∫ x in x₁..x₂, fy x‖
        ≤ (((C₀ + 14) * (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (x₂ - x₁) := by
      refine norm_intervalIntegral_le_of_le hx12 fun x hx ↦ ?_
      set z : ℂ := (x : ℂ) + (y : ℂ) * I
      have hz_re : z.re = x := by simp [z]
      have hz_im : z.im = y := hfy_im x
      obtain ⟨hcos, htan⟩ := cos_ne_and_norm_tan_le_two_of_twelve_le_abs_im (z := z)
        (by rw [hz_im]; linarith only [hN_real, hy_lo])
      have hF1 := norm_F_le_left hM₁ (N := N) (by omega)
        (by dsimp only [x₁] at hx; linarith only [hz_re, hx.1, hsqrt_le, hN_real])
        (by dsimp only [x₂] at hx; linarith only [hz_re, hx.2])
        (by rw [hz_im]; linarith only [hy_hi])
        (hzero z (by rw [hz_im])) hcos htan
      have hdiv_le : (1 + 3 * |z.im|) / (1 - z.re) ≤ 4 * (N : ℝ) := by
        have hden : 1 ≤ 1 - z.re := by dsimp only [x₂] at hx; linarith only [hz_re, hx.2]
        have hnum : 1 + 3 * |z.im| ≤ 4 * (N : ℝ) := by
          rw [hz_im]; linarith only [hy_hi, hN_real]
        rw [div_le_iff₀ (by linarith only [hden])]
        calc 1 + 3 * |z.im| ≤ 4 * (N : ℝ) := hnum
          _ ≤ 4 * (N : ℝ) * (1 - z.re) := le_mul_of_one_le_right (by positivity) hden
      have hC₀_le : C₀ ≤ C₀ * (N : ℝ) :=
        le_mul_of_one_le_right hC₀_nn (by linarith only [hN_real])
      have hF_pt : ‖F z‖ ≤ (C₀ + 14) * (N : ℝ) := by
        linarith only [hF1, hdiv_le, hC₀_le, hsqrt_le]
      rw [show fy x = F z * K_sw s w z from rfl, norm_mul]
      exact mul_le_mul hF_pt (norm_K_sw_le hN_pos hs hw (hfy_norm x)) (norm_nonneg _)
        (mul_nonneg (by linarith only [hC₀_nn]) hN_pos.le)
    have hlen : x₂ - x₁ ≤ Real.sqrt (N : ℝ) := by dsimp only [x₁, x₂]; linarith
    calc ‖∫ x in x₁..x₂, fy x‖
        ≤ (((C₀ + 14) * (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * Real.sqrt (N : ℝ) :=
          hb.trans (mul_le_mul_of_nonneg_left hlen
            (mul_nonneg (mul_nonneg (by linarith only [hC₀_nn]) hN_pos.le) (by positivity)))
      _ = (4 * (C₀ + 14) * ‖w - s‖) * (Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2) := by ring
      _ = (4 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by rw [hsq_eq]
  -- Subinterval 3: `[x₂, x₃] = [-1/8, 2]`
  have hI3 : ‖∫ x in x₂..x₃, fy x‖
      ≤ (48 * C_H * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
    have hlog2 := log_sq_le_four_nat (N := N) (by omega)
    have hb : ‖∫ x in x₂..x₃, fy x‖
        ≤ ((4 * C_H * (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (x₃ - x₂) := by
      refine norm_intervalIntegral_le_of_le hx23 fun x hx ↦ ?_
      have hF_pt : ‖F ((x : ℂ) + (y : ℂ) * I)‖ ≤ 4 * C_H * (N : ℝ) := by
        calc ‖F ((x : ℂ) + (y : ℂ) * I)‖
            ≤ C_H * (Real.log (N : ℝ)) ^ 2 := hstrip x hx
          _ ≤ C_H * (4 * (N : ℝ)) := mul_le_mul_of_nonneg_left hlog2 hCH_nn
          _ = 4 * C_H * (N : ℝ) := by ring
      rw [show fy x = F ((x : ℂ) + (y : ℂ) * I) * K_sw s w ((x : ℂ) + (y : ℂ) * I) from rfl,
        norm_mul]
      exact mul_le_mul hF_pt (norm_K_sw_le hN_pos hs hw (hfy_norm x)) (norm_nonneg _)
        (by positivity)
    have hlen : x₃ - x₂ ≤ 3 * Real.sqrt (N : ℝ) := by
      dsimp only [x₂, x₃]; linarith only [hsqrt1]
    calc ‖∫ x in x₂..x₃, fy x‖
        ≤ ((4 * C_H * (N : ℝ)) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (3 * Real.sqrt (N : ℝ)) :=
          hb.trans (mul_le_mul_of_nonneg_left hlen (by positivity))
      _ = (48 * C_H * ‖w - s‖) * (Real.sqrt (N : ℝ) * (N : ℝ) / (N : ℝ) ^ 2) := by ring
      _ = (48 * C_H * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by rw [hsq_eq]
  -- Subinterval 4: `[x₃, x₄] = [2, 2 + 2N]`
  have hI4 : ‖∫ x in x₃..x₄, fy x‖
      ≤ (8 * (M₁ + 1) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
    have hb : ‖∫ x in x₃..x₄, fy x‖
        ≤ ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (x₄ - x₃) := by
      refine norm_intervalIntegral_le_of_le hx34 fun x hx ↦ ?_
      set z : ℂ := (x : ℂ) + (y : ℂ) * I
      have hz_re : 2 ≤ z.re := by simp [z]; exact hx.1
      rw [show fy x = F z * K_sw s w z from rfl, norm_mul]
      exact mul_le_mul (norm_F_le_of_two_le_re hM₁ hz_re)
        (norm_K_sw_le hN_pos hs hw (hfy_norm x)) (norm_nonneg _) (by linarith only [hM₁_nn])
    have hlen : x₄ - x₃ = 2 * (N : ℝ) := by dsimp only [x₃, x₄]; ring
    have hinv : 1 / (N : ℝ) ≤ 1 / Real.sqrt (N : ℝ) :=
      one_div_le_one_div_of_le hsqrt_pos hsqrt_le
    calc ‖∫ x in x₃..x₄, fy x‖
        ≤ ((M₁ + 1) * (4 * ‖w - s‖ / (N : ℝ) ^ 2)) * (2 * (N : ℝ)) := by rwa [hlen] at hb
      _ = (8 * (M₁ + 1) * ‖w - s‖) * ((N : ℝ) / (N : ℝ) ^ 2) := by ring
      _ = (8 * (M₁ + 1) * ‖w - s‖) * (1 / (N : ℝ)) := by congr 1; field_simp
      _ ≤ (8 * (M₁ + 1) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) :=
          mul_le_mul_of_nonneg_left hinv (by positivity)
  -- Sum the four subintervals
  rw [hsplit]
  set J₁ := ∫ x in x₀..x₁, fy x
  set J₂ := ∫ x in x₁..x₂, fy x
  set J₃ := ∫ x in x₂..x₃, fy x
  set J₄ := ∫ x in x₃..x₄, fy x
  have ht1 := norm_add_le (J₁ + J₂ + J₃) J₄
  have ht2 := norm_add_le (J₁ + J₂) J₃
  have ht3 := norm_add_le J₁ J₂
  have hcollect :
      (12 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ))
      + (4 * (C₀ + 14) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ))
      + (48 * C_H * ‖w - s‖) * (1 / Real.sqrt (N : ℝ))
      + (8 * (M₁ + 1) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ))
      = ((16 * (M₁ + 15 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi)
          + 48 * C_H + 8 * (M₁ + 1)) * ‖w - s‖) * (1 / Real.sqrt (N : ℝ)) := by
    dsimp only [C₀]; ring
  linarith only [ht1, ht2, ht3, hI1, hI2, hI3, hI4, hcollect]

/-! ### Finite zero sets inside the rectangle and residue sum decomposition -/

private abbrev Z_crit : Set ℂ := IEANTN.zetaZeroesIn (Set.Ioo (0 : ℝ) 1) Set.univ

private noncomputable def critFin (T : ℝ) : Finset ℂ :=
  (finite_zeros_riemannZeta₁_of_isCompact
    (K := Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc (-T) T)
    (isCompact_Icc.reProdIm isCompact_Icc)).toFinset

private lemma mem_critFin_iff {T : ℝ} {z : ℂ} :
    z ∈ critFin T ↔ z ∈ Z_crit ∧ |z.im| ≤ T := by
  simp only [critFin, Set.Finite.mem_toFinset, Complex.mem_reProdIm, Set.mem_Icc]
  constructor
  · rintro ⟨⟨⟨hre0, hre1⟩, him1, him2⟩, hz1⟩
    rcases riemannZeta₁_eq_zero_iff.mp hz1 with hz_crit | ⟨k, rfl⟩
    · exact ⟨hz_crit, abs_le.mpr ⟨him1, him2⟩⟩
    · exfalso
      simp only [Complex.mul_re, Complex.neg_re, Complex.re_ofNat, Complex.add_re,
        Complex.natCast_re, Complex.one_re, Complex.add_im, Complex.natCast_im,
        Complex.one_im] at hre0
      have : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
      linarith only [hre0, this]
  · rintro ⟨hz_crit, him⟩
    obtain ⟨⟨h0, h1⟩, -, hζ⟩ := hz_crit
    have hz1 : z ≠ 1 := fun h ↦ by rw [h] at h1; norm_num at h1
    exact ⟨⟨⟨h0.le, h1.le⟩, (abs_le.mp him).1, (abs_le.mp him).2⟩,
      (riemannZeta_eq_zero_iff_riemannZeta₁ hz1).mp hζ⟩

private noncomputable def trivMap (k : ℕ) : ℂ := -2 * ((k : ℂ) + 1)

private lemma trivMap_injective : Function.Injective trivMap := by
  intro a b hab
  have hre := congrArg Complex.re hab
  simp only [trivMap, Complex.mul_re, Complex.neg_re, Complex.re_ofNat, Complex.add_re,
    Complex.natCast_re, Complex.one_re, Complex.add_im, Complex.natCast_im,
    Complex.one_im] at hre
  have hcast : (a : ℝ) = (b : ℝ) := by linarith only [hre]
  exact Nat.cast_injective hcast

private noncomputable def trivFin (N : ℕ) : Finset ℂ :=
  (Finset.range N).image trivMap

/-! ### Main proof of `ZetaHadamard.v1.logDeriv_partial_fractions` -/

theorem logDeriv_partial_fractions_proof : ZetaHadamard.v1.logDeriv_partial_fractions := by
  classical
  intro s w hs1 hw1 hζs hζw
  rcases eq_or_ne s w with rfl | hsw
  · have hval : deriv riemannZeta s / riemannZeta s - deriv riemannZeta s / riemannZeta s
        + (Complex.digamma (s / 2 + 1) - Complex.digamma (s / 2 + 1)) / 2
        + 1 / (s - 1) - 1 / (s - 1) = 0 := by ring
    rw [hval]
    exact hasSum_zero.congr_fun fun ρ ↦ by ring
  -- Choose global vertical bound `M₁` on `Re ≥ 9/8` and good-ordinate sequence `T_seq`.
  obtain ⟨M₁, hM₁_nn, hM₁⟩ :=
    logDeriv_riemannZeta_bounded_of_re_ge (σ₀ := 9 / 8) (by norm_num)
  obtain ⟨C_H, hCH_nn, hgood⟩ := exists_good_ordinate
  let T_seq : ℕ → ℝ := fun N ↦
    if h : 12 ≤ N then Classical.choose (hgood N h) else (N : ℝ) + 1 / 2
  have hT_bounds : ∀ N : ℕ, (N : ℝ) + 1 / 4 ≤ T_seq N ∧ T_seq N ≤ (N : ℝ) + 3 / 4 := by
    intro N
    by_cases h : 12 ≤ N
    · simp only [T_seq, h, ↓reduceDIte]
      have hspec := Classical.choose_spec (hgood N h)
      exact ⟨hspec.1, hspec.2.1⟩
    · simp only [T_seq, h, ↓reduceDIte]
      constructor <;> linarith
  have hT_zero : ∀ N : ℕ, 12 ≤ N → ∀ z : ℂ, |z.im| = T_seq N → riemannZeta z ≠ 0 := by
    intro N hN
    simp only [T_seq, hN, ↓reduceDIte]
    exact (Classical.choose_spec (hgood N hN)).2.2.1
  have hT_strip : ∀ N : ℕ, 12 ≤ N → ∀ y : ℝ, |y| = T_seq N →
      ∀ σ ∈ Set.Icc (-1 / 8 : ℝ) 2,
        ‖F ((σ : ℂ) + (y : ℂ) * I)‖ ≤ C_H * (Real.log (N : ℝ)) ^ 2 := by
    intro N hN y hy σ hσ
    have hspec := (Classical.choose_spec (hgood N hN)).2.2.2 σ hσ
    have hT_nn : 0 ≤ T_seq N := by
      have := (hT_bounds N).1; have := Nat.cast_nonneg (α := ℝ) N; linarith
    have hy_cases : y = T_seq N ∨ y = -T_seq N := by
      rcases le_or_gt 0 y with h0 | h0
      · left; linarith [abs_of_nonneg h0]
      · right; linarith [abs_of_neg h0]
    rcases hy_cases with rfl | rfl
    · simpa only [T_seq, hN, ↓reduceDIte] using hspec
    · have hconj : ((σ : ℂ) + ((-T_seq N : ℝ) : ℂ) * I)
          = starRingEnd ℂ ((σ : ℂ) + (T_seq N : ℂ) * I) := by simp
      rw [hconj, F_conj, RCLike.norm_conj]
      simpa only [T_seq, hN, ↓reduceDIte] using hspec
  have hT_mono : Monotone T_seq := by
    intro m n hmn
    rcases hmn.eq_or_lt with rfl | hlt
    · exact le_rfl
    · have hmn1 : (m : ℝ) + 1 ≤ (n : ℝ) := by exact_mod_cast Nat.succ_le_of_lt hlt
      have hm := (hT_bounds m).2
      have hn := (hT_bounds n).1
      linarith only [hmn1, hm, hn]
  -- Define expanding rectangle corners `z_N` and `w_N`.
  let z_N : ℕ → ℂ := fun N ↦ ((sigmaZeta (N + 1)) : ℂ) + ((-T_seq N : ℝ) : ℂ) * I
  let w_N : ℕ → ℂ := fun N ↦ ((2 + 2 * (N : ℝ) : ℝ) : ℂ) + (T_seq N : ℂ) * I
  let N₀ : ℕ := 4 * Nat.ceil (‖s‖ + ‖w‖) + 20
  have hN₀_ge20 : 20 ≤ N₀ := by omega
  have hs_half : ∀ N : ℕ, N₀ ≤ N → ‖s‖ ≤ (N : ℝ) / 2 := by
    intro N hN
    have hc : ‖s‖ + ‖w‖ ≤ (Nat.ceil (‖s‖ + ‖w‖) : ℝ) := Nat.le_ceil _
    have hN_cast : (N₀ : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
    have hN₀_eq : (N₀ : ℝ) = 4 * (Nat.ceil (‖s‖ + ‖w‖) : ℝ) + 20 := by
      simp [N₀]
    have hw_nn : 0 ≤ ‖w‖ := norm_nonneg w
    linarith only [hc, hN_cast, hN₀_eq, hw_nn]
  have hw_half : ∀ N : ℕ, N₀ ≤ N → ‖w‖ ≤ (N : ℝ) / 2 := by
    intro N hN
    have hc : ‖s‖ + ‖w‖ ≤ (Nat.ceil (‖s‖ + ‖w‖) : ℝ) := Nat.le_ceil _
    have hN_cast : (N₀ : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
    have hN₀_eq : (N₀ : ℝ) = 4 * (Nat.ceil (‖s‖ + ‖w‖) : ℝ) + 20 := by
      simp [N₀]
    have hs_nn : 0 ≤ ‖s‖ := norm_nonneg s
    linarith only [hc, hN_cast, hN₀_eq, hs_nn]
  -- Step 1: `RectangleIntegral' (g_sw s w) (z_N N) (w_N N) → 0` as `N → ∞`.
  have hrect_tendsto :
      Tendsto (fun N : ℕ ↦ RectangleIntegral' (g_sw s w) (z_N N) (w_N N)) atTop (𝓝 0) := by
    set C_H_seg : ℝ := (16 * (M₁ + 15 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi)
      + 48 * C_H + 8 * (M₁ + 1)) * ‖w - s‖
    set C_VR : ℝ := 12 * (M₁ + 1) * ‖w - s‖
    set C_VL : ℝ := 12 * (M₁ + 13 + ‖Complex.log (2 * (Real.pi : ℂ))‖ + Real.pi) * ‖w - s‖
    set C_tot : ℝ := 2 * C_H_seg + C_VR + C_VL
    have hnorm_tendsto :
        Tendsto (fun N : ℕ ↦ ‖RectangleIntegral' (g_sw s w) (z_N N) (w_N N)‖) atTop (𝓝 0) := by
      have hsq0 : Tendsto (fun N : ℕ ↦ C_tot * (1 / Real.sqrt (N : ℝ))) atTop (𝓝 0) := by
        simpa using tendsto_inv_sqrt_nat.const_mul C_tot
      refine squeeze_zero' (Eventually.of_forall fun _ ↦ norm_nonneg _) ?_ hsq0
      filter_upwards [eventually_ge_atTop N₀] with N hN
      have hN20 : 20 ≤ N := le_trans hN₀_ge20 hN
      have hN12 : 12 ≤ N := by omega
      obtain ⟨hT_lo, hT_hi⟩ := hT_bounds N
      have hT_nn : 0 ≤ T_seq N := by
        have := Nat.cast_nonneg (α := ℝ) N; linarith only [hT_lo, this]
      have hz_re : (z_N N).re = sigmaZeta (N + 1) := by simp [z_N]
      have hz_im : (z_N N).im = -T_seq N := by simp [z_N]
      have hw_re : (w_N N).re = 2 + 2 * (N : ℝ) := by simp [w_N]
      have hw_im : (w_N N).im = T_seq N := by simp [w_N]
      have hbot := norm_HIntegral_horiz_le hM₁_nn hCH_nn hM₁ hN20 (hs_half N hN) (hw_half N hN)
        (y := -T_seq N) (by rw [abs_neg, abs_of_nonneg hT_nn]; exact hT_lo)
        (by rw [abs_neg, abs_of_nonneg hT_nn]; exact hT_hi)
        (fun z hz ↦ hT_zero N hN12 z (by rwa [abs_neg, abs_of_nonneg hT_nn] at hz))
        (hT_strip N hN12 (-T_seq N) (by rw [abs_neg, abs_of_nonneg hT_nn]))
      have htop := norm_HIntegral_horiz_le hM₁_nn hCH_nn hM₁ hN20 (hs_half N hN) (hw_half N hN)
        (y := T_seq N) (by rw [abs_of_nonneg hT_nn]; exact hT_lo)
        (by rw [abs_of_nonneg hT_nn]; exact hT_hi)
        (fun z hz ↦ hT_zero N hN12 z (by rwa [abs_of_nonneg hT_nn] at hz))
        (hT_strip N hN12 (T_seq N) (abs_of_nonneg hT_nn))
      have hvR := norm_VIntegral_right_le hM₁_nn hM₁ hN20 (hs_half N hN) (hw_half N hN)
        hT_nn hT_hi
      have hvL := norm_VIntegral_left_le hM₁_nn hM₁ hN20 (hs_half N hN) (hw_half N hN)
        hT_nn hT_hi
      have h2pi_le : ‖(1 : ℂ) / (2 * (Real.pi : ℂ) * I)‖ ≤ 1 := by
        rw [norm_div, norm_one, norm_mul, norm_mul, norm_ofNat, Complex.norm_real,
          Real.norm_of_nonneg Real.pi_pos.le, Complex.norm_I, mul_one]
        have hpi2 : (2 : ℝ) ≤ Real.pi := Real.two_le_pi
        exact div_le_one_of_le₀ (by linarith only [hpi2]) (by positivity)
      rw [RectangleIntegral', norm_smul]
      have hRI_le : ‖RectangleIntegral (g_sw s w) (z_N N) (w_N N)‖
          ≤ C_tot * (1 / Real.sqrt (N : ℝ)) := by
        rw [RectangleIntegral, hz_re, hz_im, hw_re, hw_im]
        set B₁ := HIntegral (g_sw s w) (sigmaZeta (N + 1)) (2 + 2 * (N : ℝ)) (-T_seq N)
        set B₂ := HIntegral (g_sw s w) (sigmaZeta (N + 1)) (2 + 2 * (N : ℝ)) (T_seq N)
        set B₃ := VIntegral (g_sw s w) (2 + 2 * (N : ℝ)) (-T_seq N) (T_seq N)
        set B₄ := VIntegral (g_sw s w) (sigmaZeta (N + 1)) (-T_seq N) (T_seq N)
        have ht1 := norm_sub_le (B₁ - B₂ + B₃) B₄
        have ht2 := norm_add_le (B₁ - B₂) B₃
        have ht3 := norm_sub_le B₁ B₂
        have hsum_eq : C_H_seg * (1 / Real.sqrt (N : ℝ)) + C_H_seg * (1 / Real.sqrt (N : ℝ))
            + C_VR * (1 / Real.sqrt (N : ℝ)) + C_VL * (1 / Real.sqrt (N : ℝ))
            = C_tot * (1 / Real.sqrt (N : ℝ)) := by
          dsimp only [C_tot]; ring
        linarith only [ht1, ht2, ht3, hbot, htop, hvR, hvL, hsum_eq]
      calc ‖(1 : ℂ) / (2 * (Real.pi : ℂ) * I)‖ * ‖RectangleIntegral (g_sw s w) (z_N N) (w_N N)‖
          ≤ 1 * ‖RectangleIntegral (g_sw s w) (z_N N) (w_N N)‖ :=
            mul_le_mul_of_nonneg_right h2pi_le (norm_nonneg _)
        _ ≤ C_tot * (1 / Real.sqrt (N : ℝ)) := by rw [one_mul]; exact hRI_le
    exact tendsto_zero_iff_norm_tendsto_zero.mpr hnorm_tendsto
  -- Step 2: Evaluate `RectangleIntegral'` for `N ≥ N₀` via the Rectangle Residue Theorem.
  let critSubFin : ℕ → Finset Z_crit := fun N ↦ (critFin (T_seq N)).subtype (· ∈ Z_crit)
  let a_crit : Z_crit → ℂ := fun ρ ↦
    (1 / (s - (ρ : ℂ)) - 1 / (w - (ρ : ℂ))) * (IEANTN.zetaOrder (ρ : ℂ) : ℂ)
  let a_triv : ℕ → ℂ := fun k ↦
    1 / (s - trivMap k) - 1 / (w - trivMap k)
  have hrect_eval : ∀ N : ℕ, N₀ ≤ N →
      RectangleIntegral' (g_sw s w) (z_N N) (w_N N)
        = (deriv riemannZeta s / riemannZeta s + 1 / (s - 1))
          - (deriv riemannZeta w / riemannZeta w + 1 / (w - 1))
          - (∑ k ∈ Finset.range N, a_triv k)
          - (∑ ρ ∈ critSubFin N, a_crit ρ) := by
    intro N hN
    have hN20 : 20 ≤ N := le_trans hN₀_ge20 hN
    have hN12 : 12 ≤ N := by omega
    have hN_real : (20 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN20
    obtain ⟨hT_lo, hT_hi⟩ := hT_bounds N
    have hT_pos : 0 < T_seq N := by linarith only [hT_lo, hN_real]
    have hz_re : (z_N N).re = sigmaZeta (N + 1) := by simp [z_N]
    have hz_re_val : (z_N N).re = -1 - 2 * (N : ℝ) := by
      rw [hz_re]; simp only [sigmaZeta, Nat.cast_add, Nat.cast_one]; ring
    have hz_im : (z_N N).im = -T_seq N := by simp [z_N]
    have hw_re : (w_N N).re = 2 + 2 * (N : ℝ) := by simp [w_N]
    have hw_im : (w_N N).im = T_seq N := by simp [w_N]
    have hre_le : (z_N N).re ≤ (w_N N).re := by linarith only [hz_re_val, hw_re, hN_real]
    have him_le : (z_N N).im ≤ (w_N N).im := by linarith only [hz_im, hw_im, hT_pos]
    set Rn : Set ℂ := Rectangle (z_N N) (w_N N)
    set P : Set ℂ := {z : ℂ | meromorphicOrderAt (g_sw s w) z < 0}
    set S2Fin : Finset ℂ := ({s} : Finset ℂ) ∪ {w} ∪ trivFin N ∪ critFin (T_seq N)
    have hs_in_Rn : s ∈ Rn := by
      rw [mem_Rect hre_le him_le, hz_re_val, hw_re, hz_im, hw_im]
      have hs_le := hs_half N hN
      have hre_abs : |s.re| ≤ ‖s‖ := Complex.abs_re_le_norm s
      have him_abs : |s.im| ≤ ‖s‖ := Complex.abs_im_le_norm s
      obtain ⟨h1, h2⟩ := abs_le.mp (hre_abs.trans hs_le)
      obtain ⟨h3, h4⟩ := abs_le.mp (him_abs.trans hs_le)
      exact ⟨by linarith only [h1, hN_real], by linarith only [h2, hN_real],
        by linarith only [h3, hT_lo, hN_real], by linarith only [h4, hT_lo, hN_real]⟩
    have hw_in_Rn : w ∈ Rn := by
      rw [mem_Rect hre_le him_le, hz_re_val, hw_re, hz_im, hw_im]
      have hw_le := hw_half N hN
      have hre_abs : |w.re| ≤ ‖w‖ := Complex.abs_re_le_norm w
      have him_abs : |w.im| ≤ ‖w‖ := Complex.abs_im_le_norm w
      obtain ⟨h1, h2⟩ := abs_le.mp (hre_abs.trans hw_le)
      obtain ⟨h3, h4⟩ := abs_le.mp (him_abs.trans hw_le)
      exact ⟨by linarith only [h1, hN_real], by linarith only [h2, hN_real],
        by linarith only [h3, hT_lo, hN_real], by linarith only [h4, hT_lo, hN_real]⟩
    have htriv_in_Rn : ∀ u ∈ trivFin N, u ∈ Rn := by
      intro u hu
      obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hu
      have hkN : (k : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast Nat.succ_le_of_lt (Finset.mem_range.mp hk)
      have hk_nn : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
      rw [mem_Rect hre_le him_le, hz_re_val, hw_re, hz_im, hw_im]
      have hre_u : (trivMap k).re = -2 * ((k : ℝ) + 1) := by simp [trivMap]
      have him_u : (trivMap k).im = 0 := by simp [trivMap]
      rw [hre_u, him_u]
      exact ⟨by linarith only [hkN], by linarith only [hk_nn, hN_real],
        by linarith only [hT_pos], by linarith only [hT_pos]⟩
    have hcrit_in_Rn : ∀ u ∈ critFin (T_seq N), u ∈ Rn := by
      intro u hu
      obtain ⟨⟨⟨h0, h1⟩, -, -⟩, him⟩ := mem_critFin_iff.mp hu
      obtain ⟨him1, him2⟩ := abs_le.mp him
      rw [mem_Rect hre_le him_le, hz_re_val, hw_re, hz_im, hw_im]
      exact ⟨by linarith only [h0, hN_real], by linarith only [h1, hN_real], him1, him2⟩
    have hS2_sub_Rn : (S2Fin : Set ℂ) ⊆ Rn := by
      intro u hu
      simp only [S2Fin, Finset.coe_union, Finset.coe_singleton, Set.mem_union,
        Set.mem_singleton_iff, Finset.mem_coe] at hu
      rcases hu with ((rfl | rfl) | hu_triv) | hu_crit
      · exact hs_in_Rn
      · exact hw_in_Rn
      · exact htriv_in_Rn u hu_triv
      · exact hcrit_in_Rn u hu_crit
    have hRnP_sub_S2 : Rn ∩ P ⊆ (S2Fin : Set ℂ) := by
      rintro u ⟨hu_Rn, hu_P⟩
      simp only [S2Fin, Finset.coe_union, Finset.coe_singleton, Set.mem_union,
        Set.mem_singleton_iff, Finset.mem_coe]
      rcases pole_g_sw_imp hu_P with rfl | rfl | hζ1
      · exact Or.inl (Or.inl (Or.inl rfl))
      · exact Or.inl (Or.inl (Or.inr rfl))
      · rcases riemannZeta₁_eq_zero_iff.mp hζ1 with hu_crit | ⟨k, rfl⟩
        · refine Or.inr (mem_critFin_iff.mpr ⟨hu_crit, ?_⟩)
          obtain ⟨-, -, him1, him2⟩ := (mem_Rect hre_le him_le u).mp hu_Rn
          rw [hz_im] at him1
          rw [hw_im] at him2
          exact abs_le.mpr ⟨him1, him2⟩
        · refine Or.inl (Or.inr (Finset.mem_image.mpr ⟨k, Finset.mem_range.mpr ?_, rfl⟩))
          obtain ⟨hre1, -, -, -⟩ := (mem_Rect hre_le him_le (-2 * ((k : ℂ) + 1))).mp hu_Rn
          rw [hz_re_val] at hre1
          have hre_k : (-2 * ((k : ℂ) + 1)).re = -2 * ((k : ℝ) + 1) := by simp
          rw [hre_k] at hre1
          have hlt_real : (k : ℝ) < (N : ℝ) := by linarith only [hre1]
          exact_mod_cast hlt_real
    have hset_eq : Rn ∩ P = (S2Fin : Set ℂ) ∩ P := by
      ext u
      exact ⟨fun h ↦ ⟨hRnP_sub_S2 h, h.2⟩, fun h ↦ ⟨hS2_sub_Rn h.1, h.2⟩⟩
    have hno_border : Disjoint (RectangleBorder (z_N N) (w_N N)) P := by
      rw [Set.disjoint_left]
      intro u hu_b hu_P
      have hu_norm : (N : ℝ) ≤ ‖u‖ := by
        obtain ⟨⟨h | h⟩ | h⟩ | h := hu_b
        · have him : u.im = -T_seq N := by simpa [hz_im] using h.2
          have : (N : ℝ) ≤ |u.im| := by rw [him, abs_neg, abs_of_pos hT_pos]; linarith only [hT_lo]
          exact this.trans (Complex.abs_im_le_norm u)
        · have hre : u.re = -1 - 2 * (N : ℝ) := by simpa [hz_re_val] using h.1
          have : (N : ℝ) ≤ |u.re| := by
            rw [hre, abs_of_neg (by linarith only [hN_real])]; linarith only [hN_real]
          exact this.trans (Complex.abs_re_le_norm u)
        · have him : u.im = T_seq N := by simpa [hw_im] using h.2
          have : (N : ℝ) ≤ |u.im| := by rw [him, abs_of_pos hT_pos]; linarith only [hT_lo]
          exact this.trans (Complex.abs_im_le_norm u)
        · have hre : u.re = 2 + 2 * (N : ℝ) := by simpa [hw_re] using h.1
          have : (N : ℝ) ≤ |u.re| := by
            rw [hre, abs_of_pos (by linarith only [hN_real])]; linarith only [hN_real]
          exact this.trans (Complex.abs_re_le_norm u)
      rcases pole_g_sw_imp hu_P with rfl | rfl | hζ1
      · have hs_le := hs_half N hN; linarith only [hu_norm, hs_le, hN_real]
      · have hw_le := hw_half N hN; linarith only [hu_norm, hw_le, hN_real]
      · have hu1 : u ≠ 1 := fun h ↦ by rw [h, norm_one] at hu_norm; linarith only [hu_norm, hN_real]
        have hζ0 : riemannZeta u = 0 := (riemannZeta_eq_zero_iff_riemannZeta₁ hu1).mpr hζ1
        obtain ⟨⟨h | h⟩ | h⟩ | h := hu_b
        · have him : |u.im| = T_seq N := by
            have : u.im = -T_seq N := by simpa [hz_im] using h.2
            rw [this, abs_neg, abs_of_pos hT_pos]
          exact hT_zero N hN12 u him hζ0
        · have hre : u.re = sigmaZeta (N + 1) := by simpa [hz_re] using h.1
          exact riemannZeta_ne_zero_on_column (Nat.succ_pos N) hre hζ0
        · have him : |u.im| = T_seq N := by
            have : u.im = T_seq N := by simpa [hw_im] using h.2
            rw [this, abs_of_pos hT_pos]
          exact hT_zero N hN12 u him hζ0
        · have hre : u.re = 2 + 2 * (N : ℝ) := by simpa [hw_re] using h.1
          exact riemannZeta_ne_zero_of_one_lt_re (by linarith only [hre, hN_real]) hζ0
    have hpoles_fin : (Rn ∩ P).Finite := S2Fin.finite_toSet.subset hRnP_sub_S2
    have hRT := RectangleIntegral'_eq_sumResiduesIn hre_le him_le
      (fun z _ ↦ meromorphicOn_g_sw s w z trivial)
      hno_border hpoles_fin
      ((hasSimplePolesOn_g_sw hs1 hw1 hζs hζw hsw).mono (Set.subset_univ _))
    have hsum_S2 := sumResiduesIn_inter_eq_of_set_eq (F := g_sw s w) hset_eq
      (fun u _ hu_notP ↦ residue_eq_zero_of_not_pole_of_meromorphicAt
        (meromorphicOn_g_sw s w u trivial) (not_lt.mp hu_notP))
    have hsum_fin : sumResiduesIn (g_sw s w) (S2Fin : Set ℂ)
        = ∑ u ∈ S2Fin, residue (g_sw s w) u := by
      rw [sumResiduesIn, tsum_fintype (f := fun p : (S2Fin : Set ℂ) ↦ residue (g_sw s w) p)]
      exact Finset.sum_coe_sort S2Fin (residue (g_sw s w))
    rw [hRT, hsum_S2, hsum_fin]
    -- Split `S2Fin` into its four pairwise disjoint components `{s}`, `{w}`, `trivFin N`, `critFin (T_seq N)`.
    have htriv_zeta0 : ∀ u ∈ trivFin N, riemannZeta u = 0 := by
      intro u hu
      obtain ⟨k, -, rfl⟩ := Finset.mem_image.mp hu
      exact riemannZeta_neg_two_mul_nat_add_one k
    have hcrit_zeta0 : ∀ u ∈ critFin (T_seq N), riemannZeta u = 0 := by
      intro u hu
      exact (mem_critFin_iff.mp hu).1.2.2
    have hdisj_sw : Disjoint ({s} : Finset ℂ) {w} := Finset.disjoint_singleton.mpr hsw
    have hdisj_sw_triv : Disjoint (({s} : Finset ℂ) ∪ {w}) (trivFin N) := by
      rw [Finset.disjoint_left]
      intro u hu htriv
      rcases Finset.mem_union.mp hu with hs_mem | hw_mem
      · rw [Finset.mem_singleton.mp hs_mem] at htriv
        exact hζs (htriv_zeta0 s htriv)
      · rw [Finset.mem_singleton.mp hw_mem] at htriv
        exact hζw (htriv_zeta0 w htriv)
    have hdisj_3_crit : Disjoint (({s} : Finset ℂ) ∪ {w} ∪ trivFin N) (critFin (T_seq N)) := by
      rw [Finset.disjoint_left]
      intro u hu hcrit
      rcases Finset.mem_union.mp hu with hsw_mem | htriv
      · rcases Finset.mem_union.mp hsw_mem with hs_mem | hw_mem
        · rw [Finset.mem_singleton.mp hs_mem] at hcrit
          exact hζs (hcrit_zeta0 s hcrit)
        · rw [Finset.mem_singleton.mp hw_mem] at hcrit
          exact hζw (hcrit_zeta0 w hcrit)
      · obtain ⟨k, -, rfl⟩ := Finset.mem_image.mp htriv
        have hpos : 0 < (trivMap k).re := (mem_critFin_iff.mp hcrit).1.1.1
        have hneg : (trivMap k).re = -2 * ((k : ℝ) + 1) := by simp [trivMap]
        have : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
        linarith only [hpos, hneg, this]
    rw [show S2Fin = (({s} : Finset ℂ) ∪ {w} ∪ trivFin N) ∪ critFin (T_seq N) from rfl,
      Finset.sum_union hdisj_3_crit, Finset.sum_union hdisj_sw_triv, Finset.sum_union hdisj_sw,
      Finset.sum_singleton, Finset.sum_singleton,
      residue_g_at_s hs1 hζs hsw, residue_g_at_w hw1 hζw hsw]
    have htriv_sum : ∑ u ∈ trivFin N, residue (g_sw s w) u = - ∑ k ∈ Finset.range N, a_triv k := by
      rw [trivFin, Finset.sum_image (fun a _ b _ h ↦ trivMap_injective h), ← Finset.sum_neg_distrib]
      refine Finset.sum_congr rfl fun k _ ↦ ?_
      have hk1 : trivMap k ≠ 1 := by
        intro h; have hre := congrArg Complex.re h
        simp only [trivMap, Complex.mul_re, Complex.neg_re, Complex.re_ofNat, Complex.add_re,
          Complex.natCast_re, Complex.one_re, Complex.add_im, Complex.natCast_im,
          Complex.one_im] at hre
        have : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
        linarith only [hre, this]
      have hks : trivMap k ≠ s := fun h ↦ hζs (h ▸ riemannZeta_neg_two_mul_nat_add_one k)
      have hkw : trivMap k ≠ w := fun h ↦ hζw (h ▸ riemannZeta_neg_two_mul_nat_add_one k)
      rw [residue_g_at_zero hk1 hks hkw, show trivMap k = -2 * ((k : ℂ) + 1) from rfl,
        zetaOrder_trivial k]
      simp [a_triv, trivMap]
    have hcrit_sum : ∑ u ∈ critFin (T_seq N), residue (g_sw s w) u
        = - ∑ ρ ∈ critSubFin N, a_crit ρ := by
      have hmem : ∀ u ∈ critFin (T_seq N), u ∈ Z_crit :=
        fun u hu ↦ (mem_critFin_iff.mp hu).1
      rw [← Finset.sum_subtype_of_mem (residue (g_sw s w)) hmem, ← Finset.sum_neg_distrib]
      refine Finset.sum_congr rfl fun ρ _ ↦ ?_
      have hρ1 : (ρ : ℂ) ≠ 1 := fun h ↦ by
        have := ρ.2.1.2; rw [h] at this; norm_num at this
      have hρs : (ρ : ℂ) ≠ s := fun h ↦ hζs (h ▸ ρ.2.2.2)
      have hρw : (ρ : ℂ) ≠ w := fun h ↦ hζw (h ▸ ρ.2.2.2)
      rw [residue_g_at_zero hρ1 hρs hρw]
    rw [htriv_sum, hcrit_sum]
    ring
  -- Step 3: Pass to the limit `N → ∞`.
  have hcritSub_tendsto : Tendsto critSubFin atTop atTop := by
    refine Filter.tendsto_atTop_finset_of_monotone ?_ ?_
    · intro m n hmn ρ hρ
      rw [Finset.mem_subtype, mem_critFin_iff] at hρ ⊢
      exact ⟨hρ.1, hρ.2.trans (hT_mono hmn)⟩
    · intro ρ
      refine ⟨Nat.ceil |(ρ : ℂ).im|, ?_⟩
      rw [Finset.mem_subtype, mem_critFin_iff]
      refine ⟨ρ.2, ?_⟩
      have hc : |(ρ : ℂ).im| ≤ (Nat.ceil |(ρ : ℂ).im| : ℝ) := Nat.le_ceil _
      have hT := (hT_bounds (Nat.ceil |(ρ : ℂ).im|)).1
      linarith only [hc, hT]
  set S_crit : ℂ := ∑' ρ : Z_crit, a_crit ρ
  have hhasSum_crit : HasSum a_crit S_crit := (summable_critical_strip_diff s w).hasSum
  have hcrit_lim : Tendsto (fun N : ℕ ↦ ∑ ρ ∈ critSubFin N, a_crit ρ) atTop (𝓝 S_crit) :=
    hhasSum_crit.comp hcritSub_tendsto
  have htriv_lim : Tendsto (fun N : ℕ ↦ ∑ k ∈ Finset.range N, a_triv k) atTop
      (𝓝 (-(Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2)) :=
    (hasSum_trivial_zeros hζs hζw).tendsto_sum_nat
  have hrhs_lim : Tendsto
      (fun N : ℕ ↦
        (deriv riemannZeta s / riemannZeta s + 1 / (s - 1))
          - (deriv riemannZeta w / riemannZeta w + 1 / (w - 1))
          - (∑ k ∈ Finset.range N, a_triv k)
          - (∑ ρ ∈ critSubFin N, a_crit ρ))
      atTop
      (𝓝 ((deriv riemannZeta s / riemannZeta s + 1 / (s - 1))
          - (deriv riemannZeta w / riemannZeta w + 1 / (w - 1))
          - (-(Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2)
          - S_crit)) :=
    ((tendsto_const_nhds.sub htriv_lim).sub hcrit_lim)
  have hrect_lim2 : Tendsto (fun N : ℕ ↦ RectangleIntegral' (g_sw s w) (z_N N) (w_N N)) atTop
      (𝓝 ((deriv riemannZeta s / riemannZeta s + 1 / (s - 1))
          - (deriv riemannZeta w / riemannZeta w + 1 / (w - 1))
          - (-(Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2)
          - S_crit)) :=
    hrhs_lim.congr' (by filter_upwards [eventually_ge_atTop N₀] with N hN; exact (hrect_eval N hN).symm)
  have hzero_eq := tendsto_nhds_unique hrect_tendsto hrect_lim2
  have hS_val : S_crit =
      deriv riemannZeta s / riemannZeta s - deriv riemannZeta w / riemannZeta w
        + (Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2
        + 1 / (s - 1) - 1 / (w - 1) := by
    have h1 : S_crit = (deriv riemannZeta s / riemannZeta s + 1 / (s - 1))
        - (deriv riemannZeta w / riemannZeta w + 1 / (w - 1))
        - (-(Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2) :=
      (sub_eq_zero.mp hzero_eq.symm).symm
    rw [h1]
    ring
  rwa [hS_val] at hhasSum_crit

end ZetaHadamardSolution

theorem ZetaHadamard.v1.challenge_logDeriv_partial_fractions :
    ZetaHadamard.v1.logDeriv_partial_fractions :=
  ZetaHadamardSolution.logDeriv_partial_fractions_proof
