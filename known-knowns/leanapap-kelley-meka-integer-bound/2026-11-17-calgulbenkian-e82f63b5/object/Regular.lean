module

public import APAP.Prereqs.Bohr.Basic

import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Topology.Compactness.Compact

public section

open AddChar Complex Function
open scoped NNReal

namespace BohrSet
variable {G : Type*} [AddCommGroup G] [Finite G] {B : BohrSet G} {x : G}

/-- A Bohr set `B` is *regular* if the dilates of `B` by numbers close to `1` are of comparable size
to `B`. -/
structure IsRegular (B : BohrSet G) : Prop where
  le_card_smul (κ : ℝ) (hκ₀ : 0 ≤ κ) (hκ : κ ≤ (100 * B.rank : ℝ)⁻¹) :
    (1 - 100 * B.rank * κ) * Nat.card B ≤ Nat.card ↥((1 - κ) • B)
  card_smul_le (κ : ℝ) (hκ₀ : 0 ≤ κ) (hκ : κ ≤ (100 * B.rank : ℝ)⁻¹) :
    Nat.card ↥((1 + κ) • B) ≤ (1 + 100 * B.rank * κ) * Nat.card B

section RegularityAux

open scoped Finset

private lemma norm_exp_mul_I_sub_one_sq (t : ℝ) :
    ‖Complex.exp (t * I) - 1‖ ^ 2 = 4 * Real.sin (t / 2) ^ 2 := by
  rw [Complex.exp_mul_I, ← Complex.normSq_eq_norm_sq]
  have hre : (Complex.cos t + Complex.sin t * I - 1).re = Real.cos t - 1 := by
    simp [Complex.cos_ofReal_re, Complex.sin_ofReal_im]
  have him : (Complex.cos t + Complex.sin t * I - 1).im = Real.sin t := by
    simp [Complex.cos_ofReal_im, Complex.sin_ofReal_re]
  rw [Complex.normSq_apply, hre, him]
  have htwo : 2 * (t / 2) = t := by ring
  have h2 := Real.cos_two_mul' (t / 2)
  rw [htwo] at h2
  nlinarith [Real.cos_sq_add_sin_sq t, Real.cos_sq_add_sin_sq (t / 2)]

private lemma norm_exp_mul_I_sub_exp_mul_I_le (a b : ℝ) :
    ‖Complex.exp (a * I) - Complex.exp (b * I)‖ ≤ |a - b| := by
  have hmul : Complex.exp (a * I) - Complex.exp (b * I) =
      Complex.exp (b * I) * (Complex.exp (((a - b : ℝ) : ℂ) * I) - 1) := by
    rw [mul_sub, mul_one, ← Complex.exp_add]
    congr 1
    rw [Complex.ofReal_sub, sub_mul, add_sub_cancel]
  rw [hmul, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul]
  have hsq : ‖Complex.exp (((a - b : ℝ) : ℂ) * I) - 1‖ ^ 2 ≤ |a - b| ^ 2 := by
    rw [norm_exp_mul_I_sub_one_sq (a - b), ← sq_abs (Real.sin ((a - b) / 2))]
    have hsin : |Real.sin ((a - b) / 2)| ≤ |(a - b) / 2| := Real.abs_sin_le_abs
    have hpos : 0 ≤ |Real.sin ((a - b) / 2)| := abs_nonneg _
    have habs : |(a - b) / 2| = |a - b| / 2 := by simp [abs_div]
    rw [habs] at hsin
    nlinarith
  nlinarith [norm_nonneg (Complex.exp (((a - b : ℝ) : ℂ) * I) - 1), abs_nonneg (a - b)]

private lemma abs_arg_le_pi_div_two_mul_norm_one_sub {z : ℂ} (hz : ‖z‖ = 1) :
    |z.arg| ≤ (Real.pi / 2) * ‖1 - z‖ := by
  have hzeq : Complex.exp (z.arg * I) = z := by
    simpa [hz] using Complex.norm_mul_exp_arg_mul_I z
  have hnorm : ‖1 - z‖ ^ 2 = 4 * Real.sin (|z.arg| / 2) ^ 2 := by
    calc
      ‖1 - z‖ ^ 2 = ‖Complex.exp (z.arg * I) - 1‖ ^ 2 := by rw [hzeq, norm_sub_rev]
      _ = 4 * Real.sin (z.arg / 2) ^ 2 := norm_exp_mul_I_sub_one_sq z.arg
      _ = 4 * Real.sin (|z.arg| / 2) ^ 2 := by
        rcases le_total 0 z.arg with h0 | h0
        · rw [abs_of_nonneg h0]
        · have : |z.arg| / 2 = -(z.arg / 2) := by rw [abs_of_nonpos h0]; ring
          rw [this, Real.sin_neg, neg_sq]
  have hu0 : 0 ≤ |z.arg| / 2 := by positivity
  have hu1 : |z.arg| / 2 ≤ Real.pi / 2 := by
    have := Complex.abs_arg_le_pi z
    linarith
  have hsin := Real.mul_le_sin hu0 hu1
  have hpi : 0 < Real.pi := Real.pi_pos
  have h2 : 0 ≤ (2 / Real.pi) * (|z.arg| / 2) := by positivity
  have hsq : ((2 / Real.pi) * |z.arg|) ^ 2 ≤ ‖1 - z‖ ^ 2 := by
    rw [hnorm]
    have : (2 / Real.pi) * |z.arg| = 2 * ((2 / Real.pi) * (|z.arg| / 2)) := by ring
    rw [this]
    nlinarith
  have hle : (2 / Real.pi) * |z.arg| ≤ ‖1 - z‖ := by
    nlinarith [norm_nonneg (1 - z), (show 0 ≤ (2 / Real.pi) * |z.arg| by positivity)]
  rw [div_mul_eq_mul_div, div_le_iff₀' hpi] at hle
  linarith

private lemma norm_addChar_apply (ψ : AddChar G ℂ) (y : G) : ‖ψ y‖ = 1 :=
  congr_arg NNReal.toReal (AddChar.nnnorm_apply ψ y)

private lemma norm_one_sub_apply_sub (ψ : AddChar G ℂ) (x y : G) :
    ‖1 - ψ (x - y)‖ = ‖ψ x - ψ y‖ := by
  have hy : ‖ψ y‖ = 1 := norm_addChar_apply ψ y
  calc
    ‖1 - ψ (x - y)‖ = ‖ψ y‖ * ‖1 - ψ (x - y)‖ := by rw [hy, one_mul]
    _ = ‖ψ y * (1 - ψ (x - y))‖ := (norm_mul _ _).symm
    _ = ‖ψ y - ψ x‖ := by
      congr 1
      rw [mul_sub, mul_one, ← map_add_eq_mul, add_sub_cancel]
    _ = ‖ψ x - ψ y‖ := norm_sub_rev _ _

private lemma card_smul_le_nine_pow_mul (B : BohrSet G) {r R : ℝ}
    (hr : 0 < r) (hR : 0 ≤ R) (hratio : Real.pi * R < 9 * r) :
    Nat.card ↥(R • B) ≤ 9 ^ B.rank * Nat.card ↥(r • B) := by
  classical
  cases nonempty_fintype G
  let Φ : G → (B.frequencies → Fin 9) := fun x ψ ↦
    if B.width ψ.1 = 0 then 0
    else
      ⟨⌊((ψ.1 x).arg + (Real.pi / 2) * R * (B.width ψ.1 : ℝ)) /
          (r * (B.width ψ.1 : ℝ))⌋₊ % 9,
        Nat.mod_lt _ (by omega)⟩
  have hdiff : ∀ {x y : G}, x ∈ (R • B).chordSet → y ∈ (R • B).chordSet →
      Φ x = Φ y → x - y ∈ (r • B).chordSet := by
    intro x y hx hy hxy
    rw [mem_chordSet_iff_norm_width] at hx hy ⊢
    intro ψ hψ
    have hψR : ψ ∈ (R • B).frequencies := hψ
    have hxr : ‖1 - ψ x‖ ≤ R * (B.width ψ : ℝ) := by
      simpa [width_smul_apply, NNReal.coe_mul, Real.coe_nnabs, abs_of_nonneg hR] using hx hψR
    have hyr : ‖1 - ψ y‖ ≤ R * (B.width ψ : ℝ) := by
      simpa [width_smul_apply, NNReal.coe_mul, Real.coe_nnabs, abs_of_nonneg hR] using hy hψR
    have hrw_eq : (((r • B).width ψ : ℝ≥0) : ℝ) = r * (B.width ψ : ℝ) := by
      simp [width_smul_apply, Real.coe_nnabs, abs_of_nonneg hr.le]
    rw [hrw_eq, norm_one_sub_apply_sub]
    by_cases hw0 : B.width ψ = 0
    · simp only [hw0, NNReal.coe_zero, mul_zero] at hxr hyr ⊢
      have hx1 : ψ x = 1 := (sub_eq_zero.mp (norm_le_zero_iff.mp hxr)).symm
      have hy1 : ψ y = 1 := (sub_eq_zero.mp (norm_le_zero_iff.mp hyr)).symm
      simp [hx1, hy1]
    · have hw_pos : 0 < (B.width ψ : ℝ) := NNReal.coe_pos.mpr (pos_iff_ne_zero.mpr hw0)
      have hrw_pos : 0 < r * (B.width ψ : ℝ) := mul_pos hr hw_pos
      let w : ℝ := B.width ψ
      let ux : ℝ := ((ψ x).arg + (Real.pi / 2) * R * w) / (r * w)
      let uy : ℝ := ((ψ y).arg + (Real.pi / 2) * R * w) / (r * w)
      have hx_arg : |(ψ x).arg| ≤ (Real.pi / 2) * R * w := by
        have h1 := abs_arg_le_pi_div_two_mul_norm_one_sub (norm_addChar_apply ψ x)
        exact h1.trans (by nlinarith [Real.pi_pos])
      have hy_arg : |(ψ y).arg| ≤ (Real.pi / 2) * R * w := by
        have h1 := abs_arg_le_pi_div_two_mul_norm_one_sub (norm_addChar_apply ψ y)
        exact h1.trans (by nlinarith [Real.pi_pos])
      have hux0 : 0 ≤ ux := div_nonneg (by linarith [abs_le.mp hx_arg]) hrw_pos.le
      have huy0 : 0 ≤ uy := div_nonneg (by linarith [abs_le.mp hy_arg]) hrw_pos.le
      have hux9 : ux < 9 := by
        rw [div_lt_iff₀ hrw_pos]
        have := (abs_le.mp hx_arg).2
        nlinarith
      have huy9 : uy < 9 := by
        rw [div_lt_iff₀ hrw_pos]
        have := (abs_le.mp hy_arg).2
        nlinarith
      have hfx : ⌊ux⌋₊ < 9 := (Nat.floor_lt hux0).mpr (by norm_cast)
      have hfy : ⌊uy⌋₊ < 9 := (Nat.floor_lt huy0).mpr (by norm_cast)
      have hcoord := congr_arg Fin.val (congr_fun hxy ⟨ψ, hψ⟩)
      simp only [Φ, hw0, ↓reduceIte] at hcoord
      change ⌊ux⌋₊ % 9 = ⌊uy⌋₊ % 9 at hcoord
      rw [Nat.mod_eq_of_lt hfx, Nat.mod_eq_of_lt hfy] at hcoord
      have hfl_eq : (⌊ux⌋₊ : ℝ) = (⌊uy⌋₊ : ℝ) := by exact_mod_cast hcoord
      have hux_lo : (⌊ux⌋₊ : ℝ) ≤ ux := Nat.floor_le hux0
      have hux_hi : ux < (⌊ux⌋₊ : ℝ) + 1 := Nat.lt_floor_add_one ux
      have huy_lo : (⌊uy⌋₊ : ℝ) ≤ uy := Nat.floor_le huy0
      have huy_hi : uy < (⌊uy⌋₊ : ℝ) + 1 := Nat.lt_floor_add_one uy
      have hdiff_u : |ux - uy| ≤ 1 := abs_le.mpr ⟨by linarith, by linarith⟩
      have harg_diff : |(ψ x).arg - (ψ y).arg| ≤ r * w := by
        have hsub : ux - uy = ((ψ x).arg - (ψ y).arg) / (r * w) := by
          dsimp only [ux, uy]
          ring
        rw [hsub, abs_div, abs_of_pos hrw_pos, div_le_one hrw_pos] at hdiff_u
        exact hdiff_u
      have hψx_exp : Complex.exp ((ψ x).arg * I) = ψ x := by
        simpa [norm_addChar_apply ψ x] using Complex.norm_mul_exp_arg_mul_I (ψ x)
      have hψy_exp : Complex.exp ((ψ y).arg * I) = ψ y := by
        simpa [norm_addChar_apply ψ y] using Complex.norm_mul_exp_arg_mul_I (ψ y)
      rw [← hψx_exp, ← hψy_exp]
      exact (norm_exp_mul_I_sub_exp_mul_I_le _ _).trans harg_diff
  let SR : Finset G := (R • B).chordSet.toFinset
  let Sr : Finset G := (r • B).chordSet.toFinset
  have hcardR : Nat.card ↥(R • B) = #SR := by
    rw [Nat.card_eq_fintype_card, Set.toFinset_card]
  have hcardr : Nat.card ↥(r • B) = #Sr := by
    rw [Nat.card_eq_fintype_card, Set.toFinset_card]
  rw [hcardR, hcardr]
  have hpart : #SR = ∑ c : (B.frequencies → Fin 9), #{x ∈ SR | Φ x = c} := by
    rw [← Finset.card_eq_sum_card_fiberwise (f := Φ) (t := Finset.univ)]
    exact fun _ _ ↦ Finset.mem_univ _
  rw [hpart]
  have hfib : ∀ c : (B.frequencies → Fin 9), #{x ∈ SR | Φ x = c} ≤ #Sr := by
    intro c
    rcases ({x ∈ SR | Φ x = c}).eq_empty_or_nonempty with hemp | ⟨x₀, hx₀⟩
    · simp [hemp]
    · obtain ⟨hx₀_SR, hx₀_c⟩ := Finset.mem_filter.mp hx₀
      refine Finset.card_le_card_of_injOn (fun x ↦ x - x₀) (fun x hx ↦ ?_) (fun x _ y _ h ↦ ?_)
      · obtain ⟨hx_SR, hx_c⟩ := Finset.mem_filter.mp hx
        exact Set.mem_toFinset.mpr
          (hdiff (Set.mem_toFinset.mp hx_SR) (Set.mem_toFinset.mp hx₀_SR) (hx_c.trans hx₀_c.symm))
      · exact sub_left_inj.mp h
  calc
    ∑ c : (B.frequencies → Fin 9), #{x ∈ SR | Φ x = c}
      ≤ ∑ _ : (B.frequencies → Fin 9), #Sr := Finset.sum_le_sum fun c _ ↦ hfib c
    _ = Fintype.card (B.frequencies → Fin 9) * #Sr := by
      rw [Finset.sum_const, Finset.card_univ, smul_eq_mul]
    _ = 9 ^ B.rank * #Sr := by
      simp

private lemma greedy_interval_chain (ℐ : Finset (ℝ × ℝ)) {a b : ℝ} (hab : a ≤ b)
    (hcov : ∀ x ∈ Set.Icc a b, ∃ p ∈ ℐ, p.1 < x ∧ x < p.2) :
    ∃ (m : ℕ) (c : ℕ → ℝ × ℝ),
      1 ≤ m ∧
      (∀ i < m, c i ∈ ℐ ∧ (c i).1 < (c i).2) ∧
      (c 0).1 < a ∧
      b < (c (m - 1)).2 ∧
      (∀ i, i + 1 < m → (c (i + 1)).1 < (c i).2) ∧
      (∀ i, i + 2 < m → (c i).2 ≤ (c (i + 2)).1) := by
  classical
  have step : ∀ (k : ℕ) (x : ℝ), a ≤ x → x ≤ b → #{p ∈ ℐ | x < p.2} = k →
      ∃ (m : ℕ) (c : ℕ → ℝ × ℝ),
        1 ≤ m ∧
        (∀ i < m, c i ∈ ℐ ∧ (c i).1 < (c i).2) ∧
        (c 0).1 < x ∧
        x < (c 0).2 ∧
        (1 < m → x ≤ (c 1).1) ∧
        b < (c (m - 1)).2 ∧
        (∀ i, i + 1 < m → (c (i + 1)).1 < (c i).2) ∧
        (∀ i, i + 2 < m → (c i).2 ≤ (c (i + 2)).1) := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
      intro x hax hxb hk
      let Sx : Finset (ℝ × ℝ) := {p ∈ ℐ | p.1 < x ∧ x < p.2}
      have hSx_ne : Sx.Nonempty := by
        obtain ⟨p, hpℐ, hp1, hp2⟩ := hcov x ⟨hax, hxb⟩
        exact ⟨p, Finset.mem_filter.mpr ⟨hpℐ, hp1, hp2⟩⟩
      obtain ⟨p₀, hp₀_Sx, hp₀_max⟩ := Sx.exists_max_image Prod.snd hSx_ne
      obtain ⟨hp₀_ℐ, hp₀_l, hp₀_r⟩ := Finset.mem_filter.mp hp₀_Sx
      by_cases hdone : b < p₀.2
      · refine ⟨1, fun _ ↦ p₀, le_rfl, ?_, hp₀_l, hp₀_r, ?_, hdone, ?_, ?_⟩
        · intro i _
          exact ⟨hp₀_ℐ, hp₀_l.trans hp₀_r⟩
        · intro h1
          omega
        · intro i hi
          omega
        · intro i hi
          omega
      · push Not at hdone
        have hx'a : a ≤ p₀.2 := hax.trans hp₀_r.le
        have hsub : {p ∈ ℐ | p₀.2 < p.2} ⊂ {p ∈ ℐ | x < p.2} := by
          rw [Finset.ssubset_iff_of_subset]
          · refine ⟨p₀, Finset.mem_filter.mpr ⟨hp₀_ℐ, hp₀_r⟩, ?_⟩
            simp
          · intro q hq
            obtain ⟨hqℐ, hqr⟩ := Finset.mem_filter.mp hq
            exact Finset.mem_filter.mpr ⟨hqℐ, hp₀_r.trans hqr⟩
        have hk' : #{p ∈ ℐ | p₀.2 < p.2} < k := hk ▸ Finset.card_lt_card hsub
        obtain ⟨m', c', hm'1, hc'ℐ, hc'0l, hc'0r, hc'1, hc'end, hc'adj, hc'gap⟩ :=
          ih _ hk' p₀.2 hx'a hdone rfl
        have hxc'0 : x ≤ (c' 0).1 := by
          by_contra! hlt
          have hc'0_mem : c' 0 ∈ Sx := by
            refine Finset.mem_filter.mpr ⟨(hc'ℐ 0 (by omega)).1, hlt, hp₀_r.trans hc'0r⟩
          have hle := hp₀_max (c' 0) hc'0_mem
          linarith
        let c : ℕ → ℝ × ℝ := fun i ↦ if i = 0 then p₀ else c' (i - 1)
        refine ⟨m' + 1, c, by omega, ?_, hp₀_l, hp₀_r, ?_, ?_, ?_, ?_⟩
        · intro i hi
          by_cases hi0 : i = 0
          · subst hi0
            exact ⟨hp₀_ℐ, hp₀_l.trans hp₀_r⟩
          · simpa [c, hi0] using hc'ℐ (i - 1) (by omega)
        · intro _
          simpa [c] using hxc'0
        · have hne : m' ≠ 0 := by omega
          simpa [c, hne] using hc'end
        · intro i hi
          by_cases hi0 : i = 0
          · subst hi0
            simpa [c] using hc'0l
          · have h1 : c (i + 1) = c' i := by simp [c]
            have h2 : c i = c' (i - 1) := by simp [c, hi0]
            rw [h1, h2]
            have hstep := hc'adj (i - 1) (by omega)
            have hidx2 : i - 1 + 1 = i := by omega
            rwa [hidx2] at hstep
        · intro i hi
          by_cases hi0 : i = 0
          · subst hi0
            simpa [c] using hc'1 (by omega)
          · have h1 : c i = c' (i - 1) := by simp [c, hi0]
            have h2 : c (i + 2) = c' (i + 1) := by simp [c]
            have hidx3 : i - 1 + 2 = i + 1 := by omega
            rw [h1, h2, ← hidx3]
            exact hc'gap (i - 1) (by omega)
  obtain ⟨m, c, hm1, hcℐ, hc0l, _, _, hcend, hcadj, hcgap⟩ := step _ a le_rfl hab rfl
  exact ⟨m, c, hm1, hcℐ, hc0l, hcend, hcadj, hcgap⟩

private lemma chain_length_le_sum {m : ℕ} {c : ℕ → ℝ × ℝ} (hm : 1 ≤ m)
    (hadj : ∀ i, i + 1 < m → (c (i + 1)).1 < (c i).2) :
    (c (m - 1)).2 - (c 0).1 ≤ ∑ i ∈ Finset.range m, ((c i).2 - (c i).1) := by
  have hprefix : ∀ j < m,
      (c j).2 - (c 0).1 ≤ ∑ i ∈ Finset.range (j + 1), ((c i).2 - (c i).1) := by
    intro j
    induction j with
    | zero =>
      intro _
      simp
    | succ j ih =>
      intro hj
      rw [Finset.sum_range_succ]
      have hprev := ih (by omega)
      have hov := hadj j hj
      linarith
  have hm_eq : m - 1 + 1 = m := by omega
  simpa [hm_eq] using hprefix (m - 1) (by omega)

private lemma chain_sum_mono_le_two_mul {m : ℕ} {c : ℕ → ℝ × ℝ} {g : ℝ → ℝ} {u₀ v₀ : ℝ}
    (hg : Monotone g) (hu₀v₀ : u₀ ≤ v₀)
    (hbounds : ∀ i < m, u₀ ≤ (c i).1 ∧ (c i).1 < (c i).2 ∧ (c i).2 ≤ v₀)
    (hgap : ∀ i, i + 2 < m → (c i).2 ≤ (c (i + 2)).1) :
    ∑ i ∈ Finset.range m, (g (c i).2 - g (c i).1) ≤ 2 * (g v₀ - g u₀) := by
  have hguv : 0 ≤ g v₀ - g u₀ := sub_nonneg.mpr (hg hu₀v₀)
  rcases eq_or_lt_of_le (Nat.zero_le m) with rfl | hm1
  · simp [hguv]
  rcases eq_or_lt_of_le (Nat.succ_le_of_lt hm1) with rfl | hm2
  · simp only [Finset.sum_range_one]
    have hb0 := hbounds 0 (by omega)
    have h1 : g u₀ ≤ g (c 0).1 := hg hb0.1
    have h2 : g (c 0).2 ≤ g v₀ := hg hb0.2.2
    linarith
  have hind : ∀ n, 2 ≤ n → n ≤ m →
      ∑ i ∈ Finset.range n, (g (c i).2 - g (c i).1) ≤
        (g (c (n - 1)).2 - g u₀) + (g (c (n - 2)).2 - g u₀) := by
    intro n hn2
    induction n, hn2 using Nat.le_induction with
    | base =>
      intro _
      rw [Finset.sum_range_succ, Finset.sum_range_one]
      have hb0 := hbounds 0 (by omega)
      have hb1 := hbounds 1 (by omega)
      have h0 : g u₀ ≤ g (c 0).1 := hg hb0.1
      have h1 : g u₀ ≤ g (c 1).1 := hg hb1.1
      linarith
    | succ n _ ih =>
      intro hnm
      rw [Finset.sum_range_succ]
      have hprev := ih (by omega)
      have hg_step : g (c (n - 2)).2 ≤ g (c n).1 := by
        have hidx : n - 2 + 2 = n := by omega
        have := hgap (n - 2) (by omega)
        rw [hidx] at this
        exact hg this
      have hn1 : n + 1 - 1 = n := by omega
      have hn2' : n + 1 - 2 = n - 1 := by omega
      rw [hn1, hn2']
      linarith
  have hfin := hind m hm2 le_rfl
  have hb1 : g (c (m - 1)).2 ≤ g v₀ := hg (hbounds (m - 1) (by omega)).2.2
  have hb2 : g (c (m - 2)).2 ≤ g v₀ := hg (hbounds (m - 2) (by omega)).2.2
  linarith

private lemma card_smul_pos (B : BohrSet G) (t : ℝ) : 0 < (Nat.card ↥(t • B) : ℝ) := by
  have : Nonempty ↥(t • B) := ⟨⟨0, zero_mem⟩⟩
  have h1 : 1 ≤ Nat.card ↥(t • B) := Nat.card_pos
  exact_mod_cast h1

private lemma card_smul_mono (B : BohrSet G) {t₁ t₂ : ℝ} (ht₁ : 0 ≤ t₁) (hle : t₁ ≤ t₂) :
    Nat.card ↥(t₁ • B) ≤ Nat.card ↥(t₂ • B) := by
  classical
  cases nonempty_fintype G
  have hB : t₁ • B ≤ t₂ • B := by
    intro ψ
    simp only [ewidth_smul]
    split_ifs with hψ
    · gcongr
      rw [← NNReal.coe_le_coe, Real.coe_nnabs, Real.coe_nnabs, abs_of_nonneg ht₁,
        abs_of_nonneg (ht₁.trans hle)]
      exact hle
    · exact le_rfl
  rw [Nat.card_eq_fintype_card, Nat.card_eq_fintype_card, ← Set.toFinset_card (t₁ • B).chordSet,
    ← Set.toFinset_card (t₂ • B).chordSet]
  exact Finset.card_le_card (Set.toFinset_subset_toFinset.mpr (chordSet_mono hB))

end RegularityAux

/-- **Bohr Set Regularity**. Any Bohr set can be dilated by a small amount to become a regular Bohr
set. -/
lemma regularity (B : BohrSet G) : ∃ ρ : ℝ, 2⁻¹ ≤ ρ ∧ ρ ≤ 1 ∧ (ρ • B).IsRegular := by
  by_cases hd0 : B.rank = 0
  · refine ⟨1, by norm_num, le_rfl, ?_⟩
    rw [one_smul]
    refine ⟨fun κ hκ₀ hκ ↦ ?_, fun κ hκ₀ hκ ↦ ?_⟩
    · simp only [hd0, Nat.cast_zero, mul_zero, inv_zero] at hκ ⊢
      have rfl_κ : κ = 0 := le_antisymm hκ hκ₀
      subst rfl_κ
      simp
    · simp only [hd0, Nat.cast_zero, mul_zero, inv_zero] at hκ ⊢
      have rfl_κ : κ = 0 := le_antisymm hκ hκ₀
      subst rfl_κ
      simp
  have hd_pos : 0 < B.rank := Nat.pos_of_ne_zero hd0
  let d : ℝ := B.rank
  have hd1 : 1 ≤ d := Nat.one_le_cast.mpr hd_pos
  have hd_pos_r : 0 < d := by positivity
  by_contra! hnot
  let f : ℝ → ℝ := fun t ↦ (Nat.card ↥(t • B) : ℝ)
  let g : ℝ → ℝ := fun t ↦ Real.log (f t)
  have hf_pos : ∀ t : ℝ, 0 < f t := fun t ↦ card_smul_pos B t
  have hg_mono_on : ∀ {t₁ t₂ : ℝ}, 0 ≤ t₁ → t₁ ≤ t₂ → g t₁ ≤ g t₂ := by
    intro t₁ t₂ ht₁ hle
    refine Real.log_le_log (hf_pos t₁) ?_
    dsimp only [f]
    exact Nat.cast_le.mpr (card_smul_mono B ht₁ hle)
  let g_ext : ℝ → ℝ := fun t ↦ g (max 0 t)
  have hg_ext_mono : Monotone g_ext := by
    intro x y hxy
    exact hg_mono_on (le_max_left 0 x) (max_le_max_left 0 hxy)
  have hg_ext_eq : ∀ {t : ℝ}, 0 ≤ t → g_ext t = g t := fun ht ↦ by simp [g_ext, max_eq_right ht]
  have hex_int : ∀ ρ ∈ Set.Icc (2⁻¹ : ℝ) 1, ∃ p : ℝ × ℝ,
      49 / 100 ≤ p.1 ∧ p.1 < ρ ∧ ρ < p.2 ∧ p.2 ≤ 51 / 50 ∧
      40 * d * (p.2 - p.1) < g_ext p.2 - g_ext p.1 := by
    intro ρ ⟨hρ_lo, hρ_hi⟩
    have hfail := hnot ρ hρ_lo hρ_hi
    have hjump : ∃ u v κ : ℝ, 495 / 1000 ≤ u ∧ u ≤ ρ ∧ ρ ≤ v ∧ v ≤ 101 / 100 ∧
        0 < κ ∧ κ ≤ (100 * d)⁻¹ ∧ v - u = κ * ρ ∧ 50 * d * κ ≤ g v - g u := by
      by_contra! hall
      apply hfail
      refine ⟨fun κ hκ₀ hκ ↦ ?_, fun κ hκ₀ hκ ↦ ?_⟩
      · rw [rank_smul] at hκ ⊢
        rcases eq_or_lt_of_le hκ₀ with rfl | hκ_pos
        · simp
        by_contra! hlt
        rw [← mul_smul] at hlt
        have hκ_le : κ ≤ 1 / 100 := hκ.trans (by
          rw [one_div]
          exact inv_anti₀ (by norm_num) (by linarith))
        have hu_lo : 495 / 1000 ≤ (1 - κ) * ρ := by nlinarith
        have h1m : 0 < 1 - 100 * d * κ := by
          have hpos_lhs : 0 < (Nat.card ↥(((1 - κ) * ρ) • B) : ℝ) := hf_pos _
          have hpos_fρ : 0 < (Nat.card ↥(ρ • B) : ℝ) := hf_pos _
          nlinarith
        have hquot : (1 - 100 * d * κ)⁻¹ < f ρ / f ((1 - κ) * ρ) := by
          rw [lt_div_iff₀ (hf_pos _), inv_mul_lt_iff₀ h1m]
          simpa [f, mul_comm] using hlt
        have hlog1 : 100 * d * κ ≤ Real.log ((1 - 100 * d * κ)⁻¹) := by
          have := Real.one_sub_inv_le_log_of_pos (inv_pos.mpr h1m)
          rw [inv_inv] at this
          linarith
        have hlog2 : Real.log ((1 - 100 * d * κ)⁻¹) < g ρ - g ((1 - κ) * ρ) := by
          rw [← Real.log_div (hf_pos _).ne' (hf_pos _).ne']
          exact Real.log_lt_log (inv_pos.mpr h1m) hquot
        have hcontra := hall ((1 - κ) * ρ) ρ κ hu_lo (by nlinarith) le_rfl (by linarith)
          hκ_pos hκ (by ring)
        nlinarith [mul_pos hd_pos_r hκ_pos]
      · rw [rank_smul] at hκ ⊢
        rcases eq_or_lt_of_le hκ₀ with rfl | hκ_pos
        · simp
        by_contra! hgt
        rw [← mul_smul] at hgt
        have hκ_le : κ ≤ 1 / 100 := hκ.trans (by
          rw [one_div]
          exact inv_anti₀ (by norm_num) (by linarith))
        have hv_hi : (1 + κ) * ρ ≤ 101 / 100 := by nlinarith
        have h1p : 0 < 1 + 100 * d * κ := by positivity
        have hquot : 1 + 100 * d * κ < f ((1 + κ) * ρ) / f ρ := by
          rwa [lt_div_iff₀ (hf_pos ρ)]
        have hlog1 : 50 * d * κ ≤ Real.log (1 + 100 * d * κ) := by
          have hle1 : 100 * d * κ ≤ 1 := by
            have := mul_le_mul_of_nonneg_left hκ (by positivity : (0 : ℝ) ≤ 100 * d)
            rwa [mul_inv_cancel₀ (by positivity)] at this
          have h := Real.one_sub_inv_le_log_of_pos h1p
          have hfrac : 50 * d * κ ≤ 1 - (1 + 100 * d * κ)⁻¹ := by
            rw [le_sub_iff_add_le, ← le_sub_iff_add_le', inv_le_iff_one_le_mul₀ h1p]
            nlinarith [mul_pos hd_pos_r hκ_pos]
          linarith
        have hlog2 : Real.log (1 + 100 * d * κ) < g ((1 + κ) * ρ) - g ρ := by
          rw [← Real.log_div (hf_pos _).ne' (hf_pos _).ne']
          exact Real.log_lt_log h1p hquot
        have hcontra := hall ρ ((1 + κ) * ρ) κ (by linarith) le_rfl (by nlinarith) hv_hi
          hκ_pos hκ (by ring)
        linarith
    obtain ⟨u, v, κ, hu_lo, hu_ρ, hρ_v, hv_hi, hκ_pos, _, huv_eq, hgain⟩ := hjump
    have huv_pos : 0 < v - u := by rw [huv_eq]; positivity
    let δ : ℝ := min (1 / 200) ((v - u) / 10)
    have hδ_pos : 0 < δ := lt_min (by norm_num) (by positivity)
    have hδ_le1 : δ ≤ 1 / 200 := min_le_left _ _
    have hδ_le2 : δ ≤ (v - u) / 10 := min_le_right _ _
    refine ⟨(u - δ, v + δ), by linarith, by linarith, by linarith, by linarith, ?_⟩
    dsimp only
    rw [hg_ext_eq (by linarith), hg_ext_eq (by linarith)]
    have hmono1 : g (u - δ) ≤ g u := hg_mono_on (by linarith) (by linarith)
    have hmono2 : g v ≤ g (v + δ) := hg_mono_on (by linarith) (by linarith)
    have hvu_le_κ : v - u ≤ κ := by
      rw [huv_eq]
      nlinarith
    nlinarith
  classical
  choose P hP using fun x : Set.Icc (2⁻¹ : ℝ) 1 ↦ hex_int x.1 x.2
  obtain ⟨S_idx, hcov_sub⟩ := isCompact_Icc.elim_finite_subcover
    (fun x : Set.Icc (2⁻¹ : ℝ) 1 ↦ Set.Ioo (P x).1 (P x).2)
    (fun _ ↦ isOpen_Ioo)
    (fun x hx ↦ Set.mem_iUnion.mpr ⟨⟨x, hx⟩, (hP ⟨x, hx⟩).2.1, (hP ⟨x, hx⟩).2.2.1⟩)
  let ℐ : Finset (ℝ × ℝ) := S_idx.image P
  have hcov : ∀ x ∈ Set.Icc (2⁻¹ : ℝ) 1, ∃ p ∈ ℐ, p.1 < x ∧ x < p.2 := by
    intro x hx
    obtain ⟨i, hi_mem, hi_oo⟩ := Set.mem_iUnion₂.mp (hcov_sub hx)
    exact ⟨P i, Finset.mem_image_of_mem P hi_mem, hi_oo.1, hi_oo.2⟩
  obtain ⟨m, c, hm1, hcℐ, hc0l, hcend, hcadj, hcgap⟩ :=
    greedy_interval_chain ℐ (by norm_num : (2⁻¹ : ℝ) ≤ 1) hcov
  have hc_prop : ∀ i < m, 49 / 100 ≤ (c i).1 ∧ (c i).1 < (c i).2 ∧ (c i).2 ≤ 51 / 50 ∧
      40 * d * ((c i).2 - (c i).1) < g_ext (c i).2 - g_ext (c i).1 := by
    intro i hi
    obtain ⟨idx, _, hP_eq⟩ := Finset.mem_image.mp (hcℐ i hi).1
    have hp := hP idx
    rw [hP_eq] at hp
    exact ⟨hp.1, hp.2.1.trans hp.2.2.1, hp.2.2.2.1, hp.2.2.2.2⟩
  have hlen_gt : (2⁻¹ : ℝ) < ∑ i ∈ Finset.range m, ((c i).2 - (c i).1) := by
    have h1 := chain_length_le_sum hm1 hcadj
    linarith
  have hsum_gt : 20 * d < ∑ i ∈ Finset.range m, (g_ext (c i).2 - g_ext (c i).1) := by
    calc
      20 * d = 40 * d * (2⁻¹ : ℝ) := by ring
      _ < 40 * d * ∑ i ∈ Finset.range m, ((c i).2 - (c i).1) :=
        mul_lt_mul_of_pos_left hlen_gt (by positivity)
      _ = ∑ i ∈ Finset.range m, 40 * d * ((c i).2 - (c i).1) := Finset.mul_sum _ _ _
      _ ≤ ∑ i ∈ Finset.range m, (g_ext (c i).2 - g_ext (c i).1) := by
        refine Finset.sum_le_sum fun i hi ↦ ?_
        exact (hc_prop i (Finset.mem_range.mp hi)).2.2.2.le
  have hsum_le : ∑ i ∈ Finset.range m, (g_ext (c i).2 - g_ext (c i).1) ≤
      2 * (g (51 / 50) - g (49 / 100)) := by
    have h := chain_sum_mono_le_two_mul hg_ext_mono (by norm_num : (49 / 100 : ℝ) ≤ 51 / 50)
      (fun i hi ↦ ⟨(hc_prop i hi).1, (hc_prop i hi).2.1, (hc_prop i hi).2.2.1⟩) hcgap
    rwa [hg_ext_eq (by norm_num), hg_ext_eq (by norm_num)] at h
  have hcov_9 : f (51 / 50) ≤ (9 : ℝ) ^ B.rank * f (49 / 100) := by
    have hratio : Real.pi * (51 / 50 : ℝ) < 9 * (49 / 100 : ℝ) := by
      linarith [Real.pi_le_four]
    dsimp only [f]
    exact_mod_cast card_smul_le_nine_pow_mul B (by norm_num) (by norm_num) hratio
  have hlog9_lt : Real.log 9 < 3 := by
    rw [Real.log_lt_iff_lt_exp (by norm_num)]
    have he1 : (2.71 : ℝ) < Real.exp 1 := by linarith [Real.exp_one_gt_d9]
    have he2 : (7.3 : ℝ) < Real.exp 1 * Real.exp 1 := by nlinarith
    have he3 : Real.exp 3 = Real.exp 1 * Real.exp 1 * Real.exp 1 := by
      rw [← Real.exp_add, ← Real.exp_add]
      norm_num
    rw [he3]
    nlinarith
  have hg_diff_lt : g (51 / 50) - g (49 / 100) < 3 * d := by
    rw [show g (51 / 50) - g (49 / 100) = Real.log (f (51 / 50) / f (49 / 100)) from
      (Real.log_div (hf_pos _).ne' (hf_pos _).ne').symm]
    have hdiv_le : f (51 / 50) / f (49 / 100) ≤ (9 : ℝ) ^ B.rank := by
      rwa [div_le_iff₀ (hf_pos _)]
    calc
      Real.log (f (51 / 50) / f (49 / 100))
        ≤ Real.log ((9 : ℝ) ^ B.rank) :=
          Real.log_le_log (div_pos (hf_pos _) (hf_pos _)) hdiv_le
      _ = d * Real.log 9 := by rw [Real.log_pow]
      _ < 3 * d := by nlinarith
  linarith

end BohrSet
