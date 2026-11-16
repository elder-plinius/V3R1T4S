/-
Copyright (c) 2026 IEANTN contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: IEANTN contributors
-/
import Strip
import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
# Gauss series on the punctured plane, trivial-zero sum, and half-plane digamma-log bound
-/

namespace ZetaHadamardSolution

open Complex GammaSolution

private lemma digamma_eq_gaussSum_of_add_re_pos :
    ∀ (m : ℕ) {u : ℂ}, (∀ n : ℕ, u ≠ -(n : ℂ)) → 0 < (u + (m : ℂ)).re →
      Complex.digamma u = gaussSum u
  | 0, u, _, hm => digamma_eq_gaussSum (by simpa using hm)
  | m + 1, u, hu, hm => by
      have hu1 : ∀ n : ℕ, u + 1 ≠ -(n : ℂ) := fun n h ↦
        hu (n + 1) (by push_cast at h ⊢; linear_combination h)
      have hm1 : 0 < ((u + 1) + (m : ℂ)).re := by
        have hEq : (u + 1) + (m : ℂ) = u + ((m + 1 : ℕ) : ℂ) := by push_cast; ring
        rwa [hEq]
      have ih := digamma_eq_gaussSum_of_add_re_pos m hu1 hm1
      have hd := Complex.digamma_apply_add_one u hu
      have hg := gaussSum_add_one hu
      linear_combination ih - hd + hg

/-- Gauss's series `ψ(u) = -γ + ∑' k, (1/(k+1) - 1/(k+u))` holds for every `u` off `{0, -1, -2, ...}`. -/
theorem digamma_eq_gaussSum_of_ne_neg_nat {u : ℂ} (hu : ∀ n : ℕ, u ≠ -(n : ℂ)) :
    Complex.digamma u = gaussSum u := by
  refine digamma_eq_gaussSum_of_add_re_pos (Nat.ceil (1 - u.re)) hu ?_
  have hc : 1 - u.re ≤ (Nat.ceil (1 - u.re) : ℝ) := Nat.le_ceil _
  simp only [Complex.add_re, Complex.natCast_re]
  linarith

lemma half_add_one_ne_neg_nat_of_zeta_ne_zero {s : ℂ} (hs : riemannZeta s ≠ 0) (n : ℕ) :
    s / 2 + 1 ≠ -(n : ℂ) := by
  intro h
  have hs_eq : s = -2 * ((n : ℂ) + 1) := by linear_combination 2 * h
  rw [hs_eq] at hs
  exact hs (riemannZeta_neg_two_mul_nat_add_one n)

/-- Partial-fraction sum over the trivial zeros `-2(k + 1)` in terms of `Complex.digamma`. -/
theorem hasSum_trivial_zeros {s w : ℂ} (hs : riemannZeta s ≠ 0) (hw : riemannZeta w ≠ 0) :
    HasSum (fun k : ℕ ↦ 1 / (s - (-2 * ((k : ℂ) + 1))) - 1 / (w - (-2 * ((k : ℂ) + 1))))
      (-(Complex.digamma (s / 2 + 1) - Complex.digamma (w / 2 + 1)) / 2) := by
  set u₁ : ℂ := s / 2 + 1 with hu₁_def
  set u₂ : ℂ := w / 2 + 1 with hu₂_def
  have hu₁ : ∀ n : ℕ, u₁ ≠ -(n : ℂ) := half_add_one_ne_neg_nat_of_zeta_ne_zero hs
  have hu₂ : ∀ n : ℕ, u₂ ≠ -(n : ℂ) := half_add_one_ne_neg_nat_of_zeta_ne_zero hw
  rw [digamma_eq_gaussSum_of_ne_neg_nat hu₁, digamma_eq_gaussSum_of_ne_neg_nat hu₂]
  have hdiff : HasSum (fun k : ℕ ↦ gaussTerm u₁ k - gaussTerm u₂ k)
      (gaussSum u₁ - gaussSum u₂) := by
    have h := (summable_gaussTerm hu₁).hasSum.sub (summable_gaussTerm hu₂).hasSum
    simpa only [gaussSum, add_sub_add_left_eq_sub] using h
  have hsmul := hdiff.mul_right (-(1 / 2 : ℂ))
  rw [show -(gaussSum u₁ - gaussSum u₂) / 2 = (gaussSum u₁ - gaussSum u₂) * -(1 / 2 : ℂ) by ring]
  refine hsmul.congr_fun fun k ↦ ?_
  have h1 : (k : ℂ) + u₁ ≠ 0 := fun h ↦ hu₁ k (by linear_combination h)
  have h2 : (k : ℂ) + u₂ ≠ 0 := fun h ↦ hu₂ k (by linear_combination h)
  have hs1 : s - (-2 * ((k : ℂ) + 1)) = 2 * ((k : ℂ) + u₁) := by rw [hu₁_def]; ring
  have hw2 : w - (-2 * ((k : ℂ) + 1)) = 2 * ((k : ℂ) + u₂) := by rw [hu₂_def]; ring
  rw [hs1, hw2]
  simp only [gaussTerm]
  field_simp
  ring

/-- Uniform right-half-plane bound `‖ψ(w) - log w‖ ≤ (1 + 3 |Im w|) / Re w` for `1 ≤ Re w`. -/
theorem norm_digamma_sub_log_le_div_re {w : ℂ} (hw : 1 ≤ w.re) :
    ‖Complex.digamma w - Complex.log w‖ ≤ (1 + 3 * |w.im|) / w.re := by
  set u : ℝ := w.re with hu
  have hupos : (0 : ℝ) < u := by linarith
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
  have hcollect : |w.im| * (2 / u) + 1 / u + |w.im| / u = (1 + 3 * |w.im|) / u := by
    field_simp
    ring
  rwa [hcollect] at htri

end ZetaHadamardSolution
