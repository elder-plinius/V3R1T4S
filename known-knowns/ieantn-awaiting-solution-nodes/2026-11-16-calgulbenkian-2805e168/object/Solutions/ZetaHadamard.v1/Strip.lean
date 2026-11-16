/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Terence Tao
-/
import Analytic

/-!
# Stage 3: the strip bound

The node's conclusion. For each height `H` there is a `C` with

  `‖ψ w - log w‖ ≤ C / ‖w‖`   whenever `1 ≤ Re w` and `|Im w| ≤ H`.

## The shape of the argument

Everything goes through the point directly to the left, `u := Re w`, where Stage 1 already has the
answer. Writing the difference as three pieces,

  `ψ(w) - log w = (ψ(w) - ψ(u)) + (ψ(u) - log u) + (log u - log w)`,

each is `O(1/u)` for a different reason:

* `‖ψ(w) - ψ(u)‖ ≤ 2|Im w|/u` — **from the series**, not from a derivative. Termwise the
  difference is `(w-u)/((k+u)(k+w))`, and `‖k + w‖ ≥ Re (k + w) = k + u`, so the comparison is
  against `1/(k+u)²`, which the same telescoping bound as Stage 2f sums to `2/u`.
* `‖ψ(u) - log u‖ ≤ 1/u` — **Stage 1**, through `digamma_ofReal`.
* `‖log u - log w‖ ≤ |Im w|/u` — **the mean value inequality**. On the convex set `Re z ≥ u` the
  logarithm is differentiable with `‖(log)' z‖ = 1/‖z‖ ≤ 1/u`.

Total `(1 + 3|Im w|)/u`, and `u ≥ 1` with `|Im w| ≤ H` turns `1/u` into `(1+H)/‖w‖`, so
`C = (1 + 3H)(1 + H)` works.

## Two things that did not have to happen

**No derivative of `ψ` is needed.** The obvious route to `ψ(w) - ψ(u)` is to integrate `ψ'` along
the vertical segment, which would mean differentiating the Gauss series term by term to get
`ψ'(s) = ∑ 1/(k+s)²`. Differencing the series instead gives the same bound with no new analysis —
the `1/(k+1)` in each term cancels, exactly as in Stage 2f.

**No case split on the size of `u`.** `Complex.norm_log_one_add_half_le_self` would bound
`‖log(w/u)‖` by `(3/2)|Im w|/u`, but only once `|Im w|/u ≤ 1/2`, leaving the region
`1 ≤ u ≤ 2H` to a compactness argument. The mean value inequality covers the whole strip at once,
which is why it is used instead of the sharper local bound.

## The height may be negative

`H` is an arbitrary real, so `|Im w| ≤ H` can be unsatisfiable. The constant is built from
`max H 0` rather than `H`, which costs nothing and keeps the vacuous case honest.
-/

namespace GammaSolution

open Complex

/-- The termwise difference of two Gauss series, for arbitrary complex arguments off the poles. -/
theorem gaussTerm_sub_of_ne {a b : ℂ} (ha : ∀ n : ℕ, a ≠ -n) (hb : ∀ n : ℕ, b ≠ -n) (k : ℕ) :
    gaussTerm a k - gaussTerm b k = (a - b) / (((k : ℂ) + a) * ((k : ℂ) + b)) := by
  have h1 : ((k : ℂ) + a) ≠ 0 := fun h ↦ ha k (by linear_combination h)
  have h2 : ((k : ℂ) + b) ≠ 0 := fun h ↦ hb k (by linear_combination h)
  simp only [gaussTerm]
  field_simp
  ring

/-- **The `ψ` step across the strip**: `‖ψ(w) - ψ(Re w)‖ ≤ 2 |Im w| / Re w`.

Proved from the series, not from `ψ'`. -/
theorem norm_digamma_sub_digamma_re_le {w : ℂ} (hw : 1 ≤ w.re) :
    ‖Complex.digamma w - Complex.digamma ((w.re : ℝ) : ℂ)‖ ≤ |w.im| * (2 / w.re) := by
  set u : ℝ := w.re with hu
  have hu1 : (1 : ℝ) ≤ u := hw
  have hupos : (0 : ℝ) < u := by linarith
  have hwmem : w ∈ rightHalfPlane := mem_rightHalfPlane_iff.mpr hupos
  have humem : ((u : ℝ) : ℂ) ∈ rightHalfPlane := by
    refine mem_rightHalfPlane_iff.mpr ?_
    simpa using hupos
  have hsa : ∀ n : ℕ, w ≠ -(n : ℂ) := ne_neg_natCast_of_mem hwmem
  have hsb : ∀ n : ℕ, ((u : ℝ) : ℂ) ≠ -(n : ℂ) := ne_neg_natCast_of_mem humem
  -- Replace both digammas by their series.
  rw [digamma_eq_gaussSum hupos, digamma_eq_gaussSum (by simpa using hupos)]
  -- The difference of the two series, term by term.
  have hHS : HasSum (fun k ↦ gaussTerm w k - gaussTerm ((u : ℝ) : ℂ) k)
      (gaussSum w - gaussSum ((u : ℝ) : ℂ)) := by
    have h := (summable_gaussTerm hsa).hasSum.sub (summable_gaussTerm hsb).hasSum
    simpa only [gaussSum, add_sub_add_left_eq_sub] using h
  -- `w - u = i (Im w)`, so the numerator has norm `|Im w|`.
  have hnum : ‖w - ((u : ℝ) : ℂ)‖ = |w.im| := by
    have hEq : w - ((u : ℝ) : ℂ) = ((w.im : ℝ) : ℂ) * Complex.I := by
      apply Complex.ext <;> simp [hu]
    rw [hEq, norm_mul, Complex.norm_I, mul_one, Complex.norm_real, Real.norm_eq_abs]
  have hbound : ∀ k : ℕ, ‖gaussTerm w k - gaussTerm ((u : ℝ) : ℂ) k‖
      ≤ |w.im| * (2 * (((k : ℝ) + u) * ((k : ℝ) + u + 1))⁻¹) := by
    intro k
    have hkn : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
    have hku : (0 : ℝ) < (k : ℝ) + u := by linarith
    have hkupos : (0 : ℝ) < ((k : ℝ) + u) * ((k : ℝ) + u + 1) := by positivity
    -- `‖k + u‖ = k + u`, and `‖k + w‖ ≥ Re (k + w) = k + u`.
    have hnb : ‖(k : ℂ) + ((u : ℝ) : ℂ)‖ = (k : ℝ) + u := by
      have hc : ((k : ℂ) + ((u : ℝ) : ℂ)) = (((k : ℝ) + u : ℝ) : ℂ) := by push_cast; ring
      rw [hc, Complex.norm_real, Real.norm_of_nonneg hku.le]
    have hna : (k : ℝ) + u ≤ ‖(k : ℂ) + w‖ := by
      refine le_trans ?_ (Complex.re_le_norm _)
      simp [hu]
    rw [gaussTerm_sub_of_ne hsa hsb k, norm_div, norm_mul, hnb, hnum]
    have hden : (0 : ℝ) < ‖(k : ℂ) + w‖ * ((k : ℝ) + u) :=
      mul_pos (lt_of_lt_of_le hku hna) hku
    rw [div_le_iff₀ hden]
    -- `(k+u)(k+u+1) ≤ 2(k+u)²`, because `k + u ≥ 1`.
    have hsq : (1 : ℝ)
        ≤ 2 * (((k : ℝ) + u) * ((k : ℝ) + u + 1))⁻¹ * (((k : ℝ) + u) * ((k : ℝ) + u)) := by
      have hEq : 2 * (((k : ℝ) + u) * ((k : ℝ) + u + 1))⁻¹ * (((k : ℝ) + u) * ((k : ℝ) + u))
          = (2 * (((k : ℝ) + u) * ((k : ℝ) + u))) / (((k : ℝ) + u) * ((k : ℝ) + u + 1)) := by
        field_simp
      rw [hEq, le_div_iff₀ hkupos]
      nlinarith
    have hmono : ((k : ℝ) + u) * ((k : ℝ) + u) ≤ ‖(k : ℂ) + w‖ * ((k : ℝ) + u) :=
      mul_le_mul_of_nonneg_right hna hku.le
    have hcoef : (0 : ℝ) ≤ 2 * (((k : ℝ) + u) * ((k : ℝ) + u + 1))⁻¹ := by positivity
    have hX : (1 : ℝ)
        ≤ 2 * (((k : ℝ) + u) * ((k : ℝ) + u + 1))⁻¹ * (‖(k : ℂ) + w‖ * ((k : ℝ) + u)) :=
      le_trans hsq (mul_le_mul_of_nonneg_left hmono hcoef)
    have habs : (0 : ℝ) ≤ |w.im| := abs_nonneg _
    nlinarith [hX, habs]
  have hle := hHS.norm_le_of_bounded (hasSum_comparison hu1 |w.im|) hbound
  simpa [div_eq_mul_inv] using hle

/-- **The `log` step across the strip**: `‖log w - log (Re w)‖ ≤ |Im w| / Re w`.

The mean value inequality on `{z | Re z ≥ Re w}`, which is convex, contains both points, and on
which `‖(log)' z‖ = 1/‖z‖ ≤ 1/Re w`. -/
theorem norm_log_sub_log_re_le {w : ℂ} (hw : 1 ≤ w.re) :
    ‖Complex.log w - Complex.log ((w.re : ℝ) : ℂ)‖ ≤ |w.im| / w.re := by
  set u : ℝ := w.re with hu
  have hu1 : (1 : ℝ) ≤ u := hw
  have hupos : (0 : ℝ) < u := by linarith
  have hconv : Convex ℝ {z : ℂ | u ≤ z.re} := convex_halfSpace_re_ge u
  have hmemw : w ∈ {z : ℂ | u ≤ z.re} := by simp [hu]
  have hmemu : ((u : ℝ) : ℂ) ∈ {z : ℂ | u ≤ z.re} := by simp
  have hslit : ∀ z ∈ {z : ℂ | u ≤ z.re}, z ∈ Complex.slitPlane := by
    intro z hz
    exact Complex.mem_slitPlane_iff.mpr (Or.inl (lt_of_lt_of_le hupos hz))
  have hdiff : ∀ z ∈ {z : ℂ | u ≤ z.re}, DifferentiableAt ℂ Complex.log z := fun z hz ↦
    (Complex.hasDerivAt_log (hslit z hz)).differentiableAt
  have hbound : ∀ z ∈ {z : ℂ | u ≤ z.re}, ‖fderiv ℂ Complex.log z‖ ≤ 1 / u := by
    intro z hz
    have hzpos : (0 : ℝ) < ‖z‖ := lt_of_lt_of_le hupos (le_trans hz (Complex.re_le_norm z))
    have huz : u ≤ ‖z‖ := le_trans hz (Complex.re_le_norm z)
    rw [← norm_deriv_eq_norm_fderiv, (Complex.hasDerivAt_log (hslit z hz)).deriv, norm_inv]
    rw [inv_eq_one_div, div_le_div_iff₀ hzpos hupos]
    linarith
  have := hconv.norm_image_sub_le_of_norm_fderiv_le hdiff hbound hmemu hmemw
  -- `‖w - u‖ = |Im w|`.
  have hnum : ‖w - ((u : ℝ) : ℂ)‖ = |w.im| := by
    have hEq : w - ((u : ℝ) : ℂ) = ((w.im : ℝ) : ℂ) * Complex.I := by
      apply Complex.ext <;> simp [hu]
    rw [hEq, norm_mul, Complex.norm_I, mul_one, Complex.norm_real, Real.norm_eq_abs]
  rw [hnum] at this
  calc ‖Complex.log w - Complex.log ((u : ℝ) : ℂ)‖ ≤ 1 / u * |w.im| := this
    _ = |w.im| / u := by ring

/-- **Stage 1, transported**: `‖ψ(x) - log x‖ ≤ 1/x` for a positive real `x`, as a statement about
the complex `ψ` and `log`. -/
theorem norm_digamma_sub_log_ofReal_le {x : ℝ} (hx : 0 < x) :
    ‖Complex.digamma ((x : ℝ) : ℂ) - Complex.log ((x : ℝ) : ℂ)‖ ≤ 1 / x := by
  rw [digamma_ofReal hx, ← Complex.ofReal_log hx.le, ← Complex.ofReal_sub, Complex.norm_real,
    Real.norm_eq_abs]
  exact abs_deriv_log_Gamma_sub_log_le hx

/-- **The node's conclusion.** -/
theorem digamma_sub_log_strip (H : ℝ) :
    ∃ C : ℝ, ∀ w : ℂ, 1 ≤ w.re → |w.im| ≤ H →
      ‖Complex.digamma w - Complex.log w‖ ≤ C / ‖w‖ := by
  set H' : ℝ := max H 0 with hH'
  have hH'0 : (0 : ℝ) ≤ H' := le_max_right _ _
  have hHH' : H ≤ H' := le_max_left _ _
  refine ⟨(1 + 3 * H') * (1 + H'), fun w hw him ↦ ?_⟩
  set u : ℝ := w.re with hu
  have hu1 : (1 : ℝ) ≤ u := hw
  have hupos : (0 : ℝ) < u := by linarith
  have habs : |w.im| ≤ H' := le_trans him hHH'
  have habs0 : (0 : ℝ) ≤ |w.im| := abs_nonneg _
  -- The three pieces.
  have h1 := norm_digamma_sub_digamma_re_le hw
  have h2 := norm_digamma_sub_log_ofReal_le hupos
  have h3 := norm_log_sub_log_re_le hw
  have hsplit : Complex.digamma w - Complex.log w
      = (Complex.digamma w - Complex.digamma ((u : ℝ) : ℂ))
        + (Complex.digamma ((u : ℝ) : ℂ) - Complex.log ((u : ℝ) : ℂ))
        - (Complex.log w - Complex.log ((u : ℝ) : ℂ)) := by ring
  have htri : ‖Complex.digamma w - Complex.log w‖
      ≤ |w.im| * (2 / u) + 1 / u + |w.im| / u := by
    rw [hsplit]
    refine le_trans (norm_sub_le _ _) ?_
    have := norm_add_le (Complex.digamma w - Complex.digamma ((u : ℝ) : ℂ))
      (Complex.digamma ((u : ℝ) : ℂ) - Complex.log ((u : ℝ) : ℂ))
    linarith
  -- `(1 + 3|Im w|)/u`, and then `1/u ≤ (1+H')/‖w‖`.
  have hcollect : |w.im| * (2 / u) + 1 / u + |w.im| / u = (1 + 3 * |w.im|) / u := by
    field_simp
    ring
  have hnormpos : (0 : ℝ) < ‖w‖ := lt_of_lt_of_le hupos (Complex.re_le_norm w)
  have hnorm_le : ‖w‖ ≤ u * (1 + H') := by
    refine le_trans (Complex.norm_le_abs_re_add_abs_im w) ?_
    have hre : |w.re| = u := abs_of_pos hupos
    rw [hre]
    nlinarith
  rw [hcollect] at htri
  rw [le_div_iff₀ hnormpos]
  have hA : (0 : ℝ) ≤ (1 + 3 * |w.im|) / u := by positivity
  calc ‖Complex.digamma w - Complex.log w‖ * ‖w‖
      ≤ ((1 + 3 * |w.im|) / u) * ‖w‖ := mul_le_mul_of_nonneg_right htri hnormpos.le
    _ ≤ ((1 + 3 * |w.im|) / u) * (u * (1 + H')) := mul_le_mul_of_nonneg_left hnorm_le hA
    _ = (1 + 3 * |w.im|) * (1 + H') := by field_simp
    _ ≤ (1 + 3 * H') * (1 + H') := by nlinarith

end GammaSolution
