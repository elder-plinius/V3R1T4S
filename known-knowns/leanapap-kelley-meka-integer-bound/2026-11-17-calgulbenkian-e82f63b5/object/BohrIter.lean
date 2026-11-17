module

public import APAP.BohrStep
public import Mathlib.Analysis.SpecialFunctions.Pow.Real
public import Mathlib.Combinatorics.Additive.AP.Three.Defs

import AddCombi.Mathlib.Algebra.GroupWithZero.Indicator
import AddCombi.Mathlib.Algebra.Order.GroupWithZero.Indicator
import APAP.Prereqs.Convolution.Discrete.Basic
import APAP.Prereqs.LpNorm.Discrete.Basic
import Mathlib.Algebra.Group.Action.Pointwise.Finset
import Mathlib.Analysis.Complex.ExponentialBounds

/-!
# Density-increment iteration on Bohr sets in `ZMod q` (`q ≥ 3` prime)
-/

public section

attribute [-simp] Real.log_inv

open Finset hiding card
open Fintype (card)
open Function MeasureTheory RCLike Real
open scoped NNReal ENNReal BigOperators ComplexConjugate Pointwise Indicator translate mu

local notation3 "𝓛" x:arg => 1 + Real.log x⁻¹

namespace BohrIter

/-- Irreducible constant `2 ^ 100` keeping all polynomial exponents small (`≤ 14`) so that
`ring`, `norm_num`, `linarith`, and kernel `whnf` never unfold large powers on `ℝ`. -/
@[irreducible] def M100 : ℝ := 2 ^ 100

lemma M100_eq : M100 = 2 ^ 100 := by unfold M100; rfl

lemma M100_pos : 0 < M100 := by rw [M100_eq]; positivity

lemma one_le_M100 : 1 ≤ M100 := by rw [M100_eq]; norm_num

lemma two_pow_le_M100 {k : ℕ} (hk : k ≤ 100) : (2 : ℝ) ^ k ≤ M100 := by
  rw [M100_eq]
  exact pow_le_pow_right₀ (by norm_num) hk

section GeneralHelpers
variable {G : Type*} [AddCommGroup G]

lemma isRegular_top [Finite G] : (⊤ : BohrSet G).IsRegular where
  le_card_smul κ _ _ := by simp [BohrSet.smul_top]
  card_smul_le κ _ _ := by simp [BohrSet.smul_top]

lemma threeAPFree_vadd_subset [DecidableEq G] {A S : Finset G} {x : G}
    (hA : ThreeAPFree (α := G) (A : Set G)) (hS : S ⊆ x +ᵥ A) :
    ThreeAPFree (α := G) (S : Set G) := by
  intro a ha b hb c hc habc
  rcases mem_vadd_finset.mp (hS ha) with ⟨a', ha', rfl⟩
  rcases mem_vadd_finset.mp (hS hb) with ⟨b', hb', rfl⟩
  rcases mem_vadd_finset.mp (hS hc) with ⟨c', hc', rfl⟩
  simp only [vadd_eq_add] at habc ⊢
  have habc' : a' + c' = b' + b' := by
    have h1 : (x + a') + (x + c') = (x + b') + (x + b') := habc
    have h2 : (2 • x) + (a' + c') = (2 • x) + (b' + b') := by
      simpa [two_smul, add_assoc, add_left_comm, add_comm] using h1
    exact add_left_cancel h2
  rw [hA ha' hb' hc' habc']

lemma card_reg_dilate_ge [Finite G] {X : BohrSet G} {d : ℕ} (hrk : X.rank ≤ d)
    {α κ ρ : ℝ} (hα₀ : 0 < α) (hα₁ : α ≤ 1)
    (hκ_lo : 2⁻¹ ^ 20 * α / (d + 1 : ℝ) ≤ κ) (hκ_hi : κ ≤ 1)
    (hρ_lo : 2⁻¹ ≤ ρ) (hρ_hi : ρ ≤ 1) :
    exp (-32 * (d + 1 : ℝ) * (𝓛 α + log (d + 1 : ℝ))) * #X.finset ≤
      #((ρ • (κ • X)).finset) := by
  have hd_pos : 0 < (d + 1 : ℝ) := by positivity
  have hκ_pos : 0 < κ := (by positivity : 0 < 2⁻¹ ^ 20 * α / (d + 1 : ℝ)).trans_le hκ_lo
  have hρ_pos : 0 < ρ := by positivity
  have hsmul_eq : ρ • (κ • X) = (ρ * κ) • X := (mul_smul ρ κ X).symm
  rw [hsmul_eq]
  have hcard := X.le_card_smul (mul_pos hρ_pos hκ_pos)
    ((mul_le_of_le_one_right hρ_pos.le hκ_hi).trans hρ_hi)
  refine le_trans (mul_le_mul_of_nonneg_right ?_ (Nat.cast_nonneg _)) hcard
  set β : ℝ := 2⁻¹ ^ 24 * α * (d + 1 : ℝ)⁻¹
  have hβ_pos : 0 < β := by dsimp [β]; positivity
  have hβ_le1 : β ≤ 1 := by
    dsimp [β]
    have hd1 : (d + 1 : ℝ)⁻¹ ≤ 1 :=
      inv_le_one_of_one_le₀ (by linarith [Nat.cast_nonneg (α := ℝ) d])
    nlinarith
  have hβ_le_rk : β ≤ ρ * κ / 5 := by
    dsimp [β]
    have h1 : 2⁻¹ * (2⁻¹ ^ 20 * α / (d + 1 : ℝ)) / 5 ≤ ρ * κ / 5 := by gcongr
    refine le_trans ?_ h1
    have hrew : 2⁻¹ * (2⁻¹ ^ 20 * α / (d + 1 : ℝ)) / 5 =
        (2⁻¹ * 2⁻¹ ^ 20 / 5) * (α * (d + 1 : ℝ)⁻¹) := by ring
    rw [hrew, mul_assoc]
    exact mul_le_mul_of_nonneg_right (by norm_num) (by positivity)
  have hpow1 : β ^ d ≤ (ρ * κ / 5) ^ X.rank :=
    (pow_le_pow_of_le_one hβ_pos.le hβ_le1 hrk).trans (pow_le_pow_left₀ hβ_pos.le hβ_le_rk _)
  refine le_trans ?_ hpow1
  rw [← exp_log (pow_pos hβ_pos d), log_pow]
  apply exp_le_exp.mpr
  have hlog_inv : log β = -log β⁻¹ := by rw [log_inv, neg_neg]
  rw [hlog_inv]
  have hβ_inv_ge1 : 1 ≤ β⁻¹ := (one_le_inv₀ hβ_pos).2 hβ_le1
  have hlog_nn : 0 ≤ log β⁻¹ := log_nonneg hβ_inv_ge1
  have hβ_inv_eq : β⁻¹ = (2 : ℝ) ^ 24 * α⁻¹ * (d + 1 : ℝ) := by
    dsimp [β]; field_simp [hα₀.ne', hd_pos.ne']
  have hlog_split : log β⁻¹ = log ((2 : ℝ) ^ 24) + log α⁻¹ + log (d + 1 : ℝ) := by
    rw [hβ_inv_eq, log_mul (by positivity) hd_pos.ne', log_mul (by positivity) (by positivity)]
  have hlog24 : log ((2 : ℝ) ^ 24) ≤ 24 := by
    rw [log_pow]; push_cast
    linarith [Real.log_two_lt_d9]
  have hlog_le : log β⁻¹ ≤ 32 * (𝓛 α + log (d + 1 : ℝ)) := by
    have hlog_α : 0 ≤ log α⁻¹ := log_nonneg ((one_le_inv₀ hα₀).2 hα₁)
    have hlog_d : 0 ≤ log (d + 1 : ℝ) :=
      log_nonneg (by linarith [Nat.cast_nonneg (α := ℝ) d])
    calc
      log β⁻¹ = log ((2 : ℝ) ^ 24) + log α⁻¹ + log (d + 1 : ℝ) := hlog_split
      _ ≤ 24 + log α⁻¹ + log (d + 1 : ℝ) := by gcongr
      _ ≤ 32 + 32 * log α⁻¹ + 32 * log (d + 1 : ℝ) := by linarith
      _ = 32 * (𝓛 α + log (d + 1 : ℝ)) := by ring
  have hd_le : (d : ℝ) ≤ d + 1 := by linarith
  have hmul := mul_le_mul hd_le hlog_le hlog_nn hd_pos.le
  linarith [show (d + 1 : ℝ) * (32 * (𝓛 α + log (d + 1 : ℝ))) =
    32 * (d + 1 : ℝ) * (𝓛 α + log (d + 1 : ℝ)) by ring]

lemma exists_vadd_inter_card_ge [Fintype G] [DecidableEq G]
    [MeasurableSpace G] [DiscreteMeasurableSpace G]
    {K : BohrSet G} {S : Finset G} {R : ℝ}
    (h : R ≤ ‖𝟭_[(S : Set G), ℝ] ∗ᵈ μ K.finset‖_[∞]) :
    ∃ y : G, R * #K.finset ≤ #((-y +ᵥ S) ∩ K.finset) := by
  have : Nonempty G := ⟨0⟩
  rw [dLinftyNorm_eq_iSup_norm, ← Finset.sup'_univ_eq_ciSup, Finset.le_sup'_iff] at h
  obtain ⟨y, -, hy⟩ := h
  have hnn : 0 ≤ (𝟭_[(S : Set G), ℝ] ∗ᵈ μ K.finset) y :=
    ddconv_apply_nonneg' Set.indicator_one_nonneg mu_nonneg y
  rw [Real.norm_of_nonneg hnn] at hy
  have hK_pos : (0 : ℝ) < #K.finset := by exact_mod_cast K.card_finset_pos
  have hconv_eq : (𝟭_[(S : Set G), ℝ] ∗ᵈ μ K.finset) y =
      (#((-y +ᵥ S) ∩ K.finset) : ℝ) / #K.finset := by
    rw [ddconv_eq_sum_sub']
    have hsum_S : ∑ z : G, 𝟭_[(S : Set G), ℝ] z * μ_[ℝ] K.finset (y - z) =
        ∑ z ∈ S, μ_[ℝ] K.finset (y - z) := by
      rw [← Finset.sum_subset (Finset.subset_univ S)]
      · exact Finset.sum_congr rfl fun z hz ↦ by simp [hz]
      · intro z _ hz; simp [hz]
    rw [hsum_S]
    have hterm : ∀ z ∈ S, μ_[ℝ] K.finset (y - z) =
        (#K.finset : ℝ)⁻¹ * ite (z - y ∈ K.finset) 1 0 := fun z _ ↦ by
      rw [mu_apply]
      congr 2
      exact propext ⟨fun h ↦ by simpa [neg_sub] using BohrSet.neg_mem_finset.mpr h,
        fun h ↦ by simpa [neg_sub] using BohrSet.neg_mem_finset.mpr h⟩
    rw [Finset.sum_congr rfl hterm, ← Finset.mul_sum]
    simp only [sum_boole, div_eq_inv_mul]
    congr 2
    refine Finset.card_bij (fun z _ ↦ -y + z)
      (fun z hz ↦ by
        obtain ⟨hzS, hzK⟩ := mem_filter.mp hz
        refine mem_inter.mpr ⟨mem_vadd_finset.mpr ⟨z, hzS, rfl⟩, ?_⟩
        simpa [sub_eq_add_neg, add_comm] using hzK)
      (fun _ _ _ _ h ↦ add_left_cancel h)
      (fun w hw ↦ by
        obtain ⟨hwS, hwK⟩ := mem_inter.mp hw
        rcases mem_vadd_finset.mp hwS with ⟨z, hzS, rfl⟩
        refine ⟨z, mem_filter.mpr ⟨hzS, ?_⟩, rfl⟩
        simpa [vadd_eq_add, sub_eq_add_neg, add_comm] using hwK)
  rw [hconv_eq, le_div_iff₀ hK_pos] at hy
  exact ⟨y, hy⟩

end GeneralHelpers

section ArithHelpers

private lemma step_d_ub {i d : ℕ} {L : ℝ} (hL : 1 ≤ L)
    (hi : (i : ℝ) ≤ 2 ^ 13 * L) (hd : (d : ℝ) ≤ (i : ℝ) * (M100 ^ 3 * L ^ 8)) :
    (d + 1 : ℝ) ≤ M100 ^ 4 * L ^ 9 := by
  have hM_pos : 0 < M100 := M100_pos
  have hM_ge1 : 1 ≤ M100 := one_le_M100
  have h1 : (d : ℝ) ≤ (2 ^ 13 * L) * (M100 ^ 3 * L ^ 8) :=
    hd.trans (mul_le_mul_of_nonneg_right hi (by positivity))
  have h2 : (1 : ℝ) ≤ M100 ^ 3 * L ^ 9 :=
    one_le_mul_of_one_le_of_one_le (one_le_pow₀ hM_ge1) (one_le_pow₀ hL)
  have h3 : (2 ^ 13 + 1 : ℝ) ≤ M100 := by
    rw [M100_eq]; norm_num
  calc
    (d + 1 : ℝ) ≤ (2 ^ 13 * L) * (M100 ^ 3 * L ^ 8) + M100 ^ 3 * L ^ 9 := by linarith
    _ = (2 ^ 13 + 1 : ℝ) * (M100 ^ 3 * L ^ 9) := by ring
    _ ≤ M100 * (M100 ^ 3 * L ^ 9) := mul_le_mul_of_nonneg_right h3 (by positivity)
    _ = M100 ^ 4 * L ^ 9 := by ring

private lemma step_log_d_ub {d : ℕ} {L : ℝ} (hL : 1 ≤ L)
    (hd : (d + 1 : ℝ) ≤ M100 ^ 4 * L ^ 9) :
    log (d + 1 : ℝ) ≤ M100 * L := by
  have hM_pos : 0 < M100 := M100_pos
  have hd1_pos : 0 < (d + 1 : ℝ) := by positivity
  have hlogM : log M100 ≤ 100 := by
    rw [M100_eq, log_pow]
    push_cast
    linarith [Real.log_two_lt_d9]
  have h409 : (409 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
  calc
    log (d + 1 : ℝ) ≤ log (M100 ^ 4 * L ^ 9) := log_le_log hd1_pos hd
    _ = log (M100 ^ 4) + log (L ^ 9) := log_mul (by positivity) (by positivity)
    _ = 4 * log M100 + 9 * log L := by rw [log_pow, log_pow]; norm_num
    _ ≤ 4 * 100 + 9 * L := by
        gcongr
        exact Real.log_le_self (by positivity)
    _ ≤ 409 * L := by linarith
    _ ≤ M100 * L := mul_le_mul_of_nonneg_right h409 (by positivity)

private lemma step_size_exp {d : ℕ} {L : ℝ} (hL : 1 ≤ L)
    (hd : (d + 1 : ℝ) ≤ M100 ^ 4 * L ^ 9) (hlog_d : log (d + 1 : ℝ) ≤ M100 * L) :
    M100 ^ 4 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10) ≤ M100 ^ 10 * L ^ 11 := by
  have hM_pos : 0 < M100 := M100_pos
  have hM_ge1 : 1 ≤ M100 := one_le_M100
  have h8 : (8 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
  have hL_le_sq : L ≤ L ^ 2 := le_self_pow₀ hL (by omega)
  have hlog_sq : log (d + 1 : ℝ) ≤ M100 * L ^ 2 :=
    hlog_d.trans (mul_le_mul_of_nonneg_left hL_le_sq hM_pos.le)
  have hsum : L ^ 2 + log (d + 1 : ℝ) ≤ 2 * M100 * L ^ 2 := by
    have : 1 * L ^ 2 ≤ M100 * L ^ 2 := mul_le_mul_of_nonneg_right hM_ge1 (by positivity)
    linarith
  have hlog_nn : 0 ≤ log (d + 1 : ℝ) :=
    log_nonneg (by linarith [Nat.cast_nonneg (α := ℝ) d])
  have hprod : (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) ≤ 2 * M100 ^ 5 * L ^ 11 := by
    calc
      (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ))
        ≤ (M100 ^ 4 * L ^ 9) * (2 * M100 * L ^ 2) :=
          mul_le_mul hd hsum (by positivity) (by positivity)
      _ = 2 * M100 ^ 5 * L ^ 11 := by ring
  have hL10 : L ^ 10 ≤ M100 ^ 5 * L ^ 11 := by
    have h1 : L ^ 10 ≤ L ^ 11 := by
      rw [pow_succ]; exact le_mul_of_one_le_right (by positivity) hL
    exact h1.trans (le_mul_of_one_le_left (by positivity) (one_le_pow₀ hM_ge1))
  calc
    M100 ^ 4 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10)
      ≤ M100 ^ 4 * (3 * M100 ^ 5 * L ^ 11) :=
        mul_le_mul_of_nonneg_left (by linarith) (by positivity)
    _ = 3 * (M100 ^ 9 * L ^ 11) := by ring
    _ ≤ M100 * (M100 ^ 9 * L ^ 11) :=
        mul_le_mul_of_nonneg_right (by linarith) (by positivity)
    _ = M100 ^ 10 * L ^ 11 := by ring

private lemma step_term_bound {i d q : ℕ} {α L B_card : ℝ}
    (hα₀ : 0 < α) (hα₁ : α ≤ 1) (hL_eq : L = 𝓛 α)
    (hi : (i : ℝ) ≤ 2 ^ 13 * L) (hd : (d + 1 : ℝ) ≤ M100 ^ 4 * L ^ 9)
    (hlog_d : log (d + 1 : ℝ) ≤ M100 * L)
    (hB_sz : exp (-(i : ℝ) * (M100 ^ 10 * L ^ 11)) * q ≤ B_card)
    (h_term : exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * B_card ≤ 8 * α⁻¹ ^ 2) :
    (q : ℝ) ≤ exp (M100 ^ 12 * L ^ 12) := by
  have hM_pos : 0 < M100 := M100_pos
  have hM_ge1 : 1 ≤ M100 := one_le_M100
  have hL : 1 ≤ L := by rw [hL_eq]; exact BohrFourier.one_le_curlog hα₀.le hα₁
  have h64 : (64 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
  have h2_13 : (2 : ℝ) ^ 13 ≤ M100 := by rw [M100_eq]; norm_num
  have hd_loss : 32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤ M100 ^ 6 * L ^ 12 := by
    have hsum : L + log (d + 1 : ℝ) ≤ 2 * M100 * L := by
      have : 1 * L ≤ M100 * L := mul_le_mul_of_nonneg_right hM_ge1 (by positivity)
      linarith
    have hlog_nn : 0 ≤ log (d + 1 : ℝ) :=
      log_nonneg (by linarith [Nat.cast_nonneg (α := ℝ) d])
    have hL10_12 : L ^ 10 ≤ L ^ 12 := pow_le_pow_right₀ hL (by omega)
    have hprod : (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤ 2 * M100 ^ 5 * L ^ 10 := by
      calc
        (d + 1 : ℝ) * (L + log (d + 1 : ℝ))
          ≤ (M100 ^ 4 * L ^ 9) * (2 * M100 * L) :=
            mul_le_mul hd hsum (by positivity) (by positivity)
        _ = 2 * M100 ^ 5 * L ^ 10 := by ring
    calc
      32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))
        = 32 * ((d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by ring
      _ ≤ 32 * (2 * M100 ^ 5 * L ^ 10) := mul_le_mul_of_nonneg_left hprod (by norm_num)
      _ = 64 * M100 ^ 5 * L ^ 10 := by ring
      _ ≤ M100 * M100 ^ 5 * L ^ 12 := by gcongr
      _ = M100 ^ 6 * L ^ 12 := by ring
  have hi_loss : (i : ℝ) * (M100 ^ 10 * L ^ 11) ≤ M100 ^ 11 * L ^ 12 := by
    calc
      (i : ℝ) * (M100 ^ 10 * L ^ 11)
        ≤ ((2 : ℝ) ^ 13 * L) * (M100 ^ 10 * L ^ 11) :=
          mul_le_mul_of_nonneg_right hi (by positivity)
      _ = (2 : ℝ) ^ 13 * (M100 ^ 10 * L ^ 12) := by ring
      _ ≤ M100 * (M100 ^ 10 * L ^ 12) := mul_le_mul_of_nonneg_right h2_13 (by positivity)
      _ = M100 ^ 11 * L ^ 12 := by ring
  have h8_ub : 8 * α⁻¹ ^ 2 ≤ exp (5 * L ^ 12) := by
    have h8 : (8 : ℝ) ≤ exp 3 := by
      have he1 : (2.71 : ℝ) < exp 1 := by linarith [exp_one_gt_d9]
      have he3 : exp 3 = exp 1 * exp 1 * exp 1 := by rw [← exp_add, ← exp_add]; norm_num
      rw [he3]; nlinarith
    have hinv_exp : α⁻¹ ^ 2 = exp (2 * log α⁻¹) := by
      rw [← exp_log (pow_pos (inv_pos.mpr hα₀) 2), log_pow]
      norm_num
    rw [hinv_exp]
    calc
      8 * exp (2 * log α⁻¹) ≤ exp 3 * exp (2 * log α⁻¹) :=
        mul_le_mul_of_nonneg_right h8 (exp_pos _).le
      _ = exp (3 + 2 * log α⁻¹) := (exp_add _ _).symm
      _ ≤ exp (5 * L ^ 12) := by
          apply exp_le_exp.mpr
          have hL12 : L ≤ L ^ 12 := le_self_pow₀ hL (by omega)
          have hlog_nn : 0 ≤ log α⁻¹ := log_nonneg ((one_le_inv₀ hα₀).2 hα₁)
          linarith
  have hq_chain :
      exp (-M100 ^ 6 * L ^ 12) * (exp (-M100 ^ 11 * L ^ 12) * q) ≤ exp (5 * L ^ 12) := by
    have he1 : exp (-M100 ^ 6 * L ^ 12) ≤ exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) :=
      exp_le_exp.mpr (by linarith)
    have he2 : exp (-M100 ^ 11 * L ^ 12) ≤ exp (-(i : ℝ) * (M100 ^ 10 * L ^ 11)) :=
      exp_le_exp.mpr (by linarith)
    have hB_nn : 0 ≤ B_card :=
      (mul_nonneg (exp_pos _).le (Nat.cast_nonneg q)).trans hB_sz
    calc
      exp (-M100 ^ 6 * L ^ 12) * (exp (-M100 ^ 11 * L ^ 12) * q)
        ≤ exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) *
            (exp (-(i : ℝ) * (M100 ^ 10 * L ^ 11)) * q) := by gcongr
      _ ≤ exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * B_card := by gcongr
      _ ≤ 8 * α⁻¹ ^ 2 := h_term
      _ ≤ exp (5 * L ^ 12) := h8_ub
  rw [← mul_assoc, ← exp_add] at hq_chain
  set S : ℝ := M100 ^ 6 * L ^ 12 + M100 ^ 11 * L ^ 12
  have hq_iso : (q : ℝ) ≤ exp (5 * L ^ 12) * exp S := by
    have h1 := mul_le_mul_of_nonneg_right hq_chain (exp_pos S).le
    have hcancel : exp (-M100 ^ 6 * L ^ 12 + -M100 ^ 11 * L ^ 12) * exp S = 1 := by
      rw [← exp_add, show -M100 ^ 6 * L ^ 12 + -M100 ^ 11 * L ^ 12 + S = 0 by dsimp [S]; ring,
        exp_zero]
    rwa [mul_right_comm, hcancel, one_mul] at h1
  refine hq_iso.trans ?_
  rw [← exp_add]
  apply exp_le_exp.mpr
  dsimp [S]
  have h5_le : 5 * L ^ 12 ≤ M100 ^ 11 * L ^ 12 := by
    have h5M : (5 : ℝ) ≤ M100 ^ 11 :=
      (by linarith : (5 : ℝ) ≤ M100).trans (le_self_pow₀ hM_ge1 (by omega))
    exact mul_le_mul_of_nonneg_right h5M (by positivity)
  have h6_le : M100 ^ 6 * L ^ 12 ≤ M100 ^ 11 * L ^ 12 :=
    mul_le_mul_of_nonneg_right (pow_le_pow_right₀ hM_ge1 (by omega)) (by positivity)
  calc
    5 * L ^ 12 + (M100 ^ 6 * L ^ 12 + M100 ^ 11 * L ^ 12)
      ≤ 3 * (M100 ^ 11 * L ^ 12) := by linarith
    _ ≤ M100 * (M100 ^ 11 * L ^ 12) :=
        mul_le_mul_of_nonneg_right (by linarith) (by positivity)
    _ = M100 ^ 12 * L ^ 12 := by ring

end ArithHelpers

section ZModPrime
variable {q : ℕ} [Fact q.Prime]

/-- Upper and lower bounds on `⟪μ U ∗ᵈ μ U, μ (2 · W)⟫` when `U, W` are subsets of a
`3AP`-free set in `ZMod q` (`q ≥ 3` prime). -/
lemma threeAPFree_inner_sub (hq : 3 ≤ q) {A_x U W : Finset (ZMod q)}
    (h3 : ThreeAPFree (α := ZMod q) (A_x : Set (ZMod q)))
    (hU : U ⊆ A_x) (hW : W ⊆ A_x) (hW_ne : W.Nonempty) :
    let C := W.image (fun z ↦ (2 : ZMod q) * z)
    0 ≤ ⟪μ_[ℝ] U ∗ᵈ μ U, μ C⟫_[ℝ] ∧
      ⟪μ_[ℝ] U ∗ᵈ μ U, μ C⟫_[ℝ] ≤ ((#U : ℝ) ^ 2)⁻¹ := by
  let : MeasurableSpace (ZMod q) := ⊤
  intro C
  have hC_card : #C = #W :=
    Finset.card_image_of_injective W (BohrSet.twoEquiv hq).injective
  refine ⟨?_, ?_⟩
  · rw [wInner_one_eq_sum]
    refine Finset.sum_nonneg fun y _ ↦ ?_
    simp only [inner_apply', conj_to_real]
    exact mul_nonneg (ddconv_apply_nonneg' mu_nonneg mu_nonneg y) (mu_nonneg y)
  · rcases U.eq_empty_or_nonempty with rfl | hU_ne
    · simp
    have hW_pos : (0 : ℝ) < #W := by exact_mod_cast hW_ne.card_pos
    have honly_diag : ∀ u₁ u₃ : ZMod q,
        μ_[ℝ] U u₁ * (μ_[ℝ] U u₃ * μ_[ℝ] C (u₁ + u₃)) ≠ 0 →
          u₁ ∈ U ∩ W ∧ u₃ = u₁ := by
      intro u₁ u₃ hne
      have hu₁ : u₁ ∈ U := mu_apply_ne_zero.mp (left_ne_zero_of_mul hne)
      have h23 := right_ne_zero_of_mul hne
      have hu₃ : u₃ ∈ U := mu_apply_ne_zero.mp (left_ne_zero_of_mul h23)
      have hsumC : u₁ + u₃ ∈ C := mu_apply_ne_zero.mp (right_ne_zero_of_mul h23)
      rcases mem_image.mp hsumC with ⟨w, hw, hw_eq⟩
      have h3ap_eq : u₁ + u₃ = w + w := by rw [← hw_eq, two_mul]
      have hu₁_eq_w : u₁ = w := h3 (hU hu₁) (hW hw) (hU hu₃) h3ap_eq
      subst hu₁_eq_w
      exact ⟨mem_inter.mpr ⟨hu₁, hw⟩, add_left_cancel h3ap_eq⟩
    have hexp : ⟪μ_[ℝ] U ∗ᵈ μ U, μ C⟫_[ℝ] =
        ∑ u₁ : ZMod q, ∑ u₃ : ZMod q,
          μ_[ℝ] U u₁ * (μ_[ℝ] U u₃ * μ_[ℝ] C (u₁ + u₃)) := by
      rw [wInner_one_eq_sum]
      simp only [inner_apply', conj_to_real]
      rw [sum_ddconv_mul]
      simp_rw [mul_assoc]
    rw [hexp]
    have houter :
        ∑ u₁ : ZMod q, ∑ u₃ : ZMod q, μ_[ℝ] U u₁ * (μ_[ℝ] U u₃ * μ_[ℝ] C (u₁ + u₃)) =
          ∑ u₁ ∈ U ∩ W, ((#U : ℝ) ^ 2)⁻¹ * (#W : ℝ)⁻¹ := by
      rw [← Finset.sum_subset (Finset.subset_univ (U ∩ W))]
      · refine Finset.sum_congr rfl fun u₁ hu₁ ↦ ?_
        obtain ⟨hu₁U, hu₁W⟩ := mem_inter.mp hu₁
        have hinner :
            ∑ u₃ : ZMod q, μ_[ℝ] U u₁ * (μ_[ℝ] U u₃ * μ_[ℝ] C (u₁ + u₃)) =
              μ_[ℝ] U u₁ * (μ_[ℝ] U u₁ * μ_[ℝ] C (u₁ + u₁)) := by
          rw [← Finset.sum_subset (Finset.subset_univ {u₁})]
          · simp
          · intro u₃ _ hu₃_ne
            by_contra hne
            exact hu₃_ne (mem_singleton.mpr (honly_diag u₁ u₃ hne).2)
        have h2u₁ : u₁ + u₁ ∈ C := by
          rw [← two_mul]
          exact mem_image_of_mem _ hu₁W
        rw [hinner]
        simp only [mu_apply, hu₁U, h2u₁, ite_true, mul_one, hC_card]
        ring
      · intro u₁ _ hu₁_not
        refine Finset.sum_eq_zero fun u₃ _ ↦ ?_
        by_contra hne
        exact hu₁_not (honly_diag u₁ u₃ hne).1
    rw [houter, Finset.sum_const, nsmul_eq_mul]
    have hUW_le : (#(U ∩ W) : ℝ) ≤ #W := by
      exact_mod_cast Finset.card_le_card inter_subset_right
    calc
      (#(U ∩ W) : ℝ) * (((#U : ℝ) ^ 2)⁻¹ * (#W : ℝ)⁻¹)
        ≤ (#W : ℝ) * (((#U : ℝ) ^ 2)⁻¹ * (#W : ℝ)⁻¹) :=
          mul_le_mul_of_nonneg_right hUW_le (by positivity)
      _ = ((#U : ℝ) ^ 2)⁻¹ := by field_simp [hW_pos.ne']

/-- Second half of `bohr_step_dichotomy`: given the Hölder-lifted `L^p` lower bound on
`(μ U - μ B') ∗ᵈ (μ U - μ B')` against a regular Bohr set `C_bohr`, pass via
`pos_def_measures`, `Lp_orth`, and `prop_it` to a density-incrementing regular Bohr set `K₃`. -/
private lemma bohr_step_from_lifting [MeasurableSpace (ZMod q)] [DiscreteMeasurableSpace (ZMod q)]
    {B B' C_bohr : BohrSet (ZMod q)} {d p : ℕ}
    (hB'_reg : B'.IsRegular) (hB'_rk : B'.rank ≤ d)
    (hC_bohr_reg : C_bohr.IsRegular) (hC_bohr_pos : C_bohr.PosWidth) (hC_bohr_rk : C_bohr.rank ≤ d)
    {A U : Finset (ZMod q)} {x : ZMod q}
    (hU_sub_B' : U ⊆ B'.finset) (hU_ne : U.Nonempty) (hU_sub_vxA : U ⊆ -x +ᵥ A)
    (hA_3ap : ThreeAPFree (α := ZMod q) (A : Set (ZMod q)))
    {α α_B α_U κ₁ L : ℝ}
    (hα₀ : 0 < α) (hα_le1 : α ≤ 1) (hα_B_pos : 0 < α_B) (hα_B_le1 : α_B ≤ 1)
    (hL_def : L = 𝓛 α)
    (hκ₁_def : κ₁ = 2⁻¹ ^ 20 * α_B / (d + 1 : ℝ))
    (hC_bohr_sub : C_bohr.finset ⊆ ((2 * κ₁) • B').finset)
    (hC_sz2 : (exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)))) ^ 2 * #B.finset ≤ #C_bohr.finset)
    (hα_U_def : α_U = (#U : ℝ) / #B'.finset)
    (hα_U_ge : (1 - 1024⁻¹ : ℝ) * α_B ≤ α_U)
    (hα_U_half : α / 2 ≤ α_U)
    (hp_ne : p ≠ 0) (hp_even : Even p) (hp_upper : (p : ℝ) ≤ 8 * L)
    (hhl : (2⁻¹ : ℝ) / (4 * #B'.finset) ≤
      ‖(μ_[ℝ] U - μ B'.finset) ∗ᵈ (μ U - μ B'.finset)‖_[p, μ C_bohr.finset]) :
    ∃ (B_next : BohrSet (ZMod q)) (A_next : Finset (ZMod q)),
      B_next.IsRegular ∧
      B_next.PosWidth ∧
      (B_next.rank : ℝ) ≤ d + M100 ^ 3 * L ^ 8 ∧
      exp (-M100 ^ 4 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10)) * #B.finset ≤
        #B_next.finset ∧
      A_next ⊆ B_next.finset ∧
      ThreeAPFree (α := ZMod q) (A_next : Set (ZMod q)) ∧
      (1 + 2048⁻¹ : ℝ) * α_B * #B_next.finset ≤ #A_next := by
  have hM_pos : 0 < M100 := M100_pos
  have hM_ge1 : 1 ≤ M100 := one_le_M100
  have hLα : 1 ≤ L := by rw [hL_def]; exact BohrFourier.one_le_curlog hα₀.le hα_le1
  have hd_pos : 0 < (d + 1 : ℝ) := by positivity
  have hd_nn : 0 ≤ (d : ℝ) := Nat.cast_nonneg d
  have hlog_d_nn : 0 ≤ log (d + 1 : ℝ) := log_nonneg (by linarith only [hd_nn])
  have hB'_pos_card : (0 : ℝ) < #B'.finset := by exact_mod_cast B'.card_finset_pos
  have hα_U_pos : 0 < α_U := (half_pos hα₀).trans_le hα_U_half
  have hκ₁_pos : 0 < κ₁ := by rw [hκ₁_def]; positivity
  -- Regular sub-Bohr sets `K₁` and `K₂` inside `C_bohr`
  set κ₃ : ℝ := (400 * (d + 1 : ℝ))⁻¹ with hκ₃_def
  have hκ₃_pos : 0 < κ₃ := by rw [hκ₃_def]; positivity
  have hκ₃_le1 : κ₃ ≤ 1 := by
    rw [hκ₃_def]; exact inv_le_one_of_one_le₀ (by linarith only [hd_nn])
  obtain ⟨ρ₃, hρ₃_lo, hρ₃_hi, hK₁_reg⟩ := BohrSet.regularity (κ₃ • C_bohr)
  set K₁ : BohrSet (ZMod q) := ρ₃ • (κ₃ • C_bohr) with hK₁_def
  have hρ₃_pos : 0 < ρ₃ := by positivity
  have hK₁_pos : K₁.PosWidth := (hC_bohr_pos.smul hκ₃_pos.ne').smul hρ₃_pos.ne'
  have hK₁_rk : K₁.rank ≤ d := by simpa [hK₁_def] using hC_bohr_rk
  have hK₁_sub_κ₃ : K₁.finset ⊆ (κ₃ • C_bohr).finset := by
    simpa [hK₁_def, one_smul] using BohrSet.smul_finset_mono hρ₃_pos.le hρ₃_hi
  have hK₁_size :
      exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * #C_bohr.finset ≤ #K₁.finset := by
    rw [hL_def]
    refine card_reg_dilate_ge hC_bohr_rk hα₀ hα_le1 ?_ hκ₃_le1 hρ₃_lo hρ₃_hi
    rw [hκ₃_def, show (400 * (d + 1 : ℝ))⁻¹ = 400⁻¹ / (d + 1 : ℝ) by rw [mul_inv, div_eq_mul_inv]]
    exact div_le_div_of_nonneg_right (by linarith only [hα_le1]) hd_pos.le
  set κ₄ : ℝ := (100 * (d + 1 : ℝ))⁻¹ with hκ₄_def
  have hκ₄_pos : 0 < κ₄ := by rw [hκ₄_def]; positivity
  have hκ₄_le1 : κ₄ ≤ 1 := by
    rw [hκ₄_def]; exact inv_le_one_of_one_le₀ (by linarith only [hd_nn])
  obtain ⟨ρ₄, hρ₄_lo, hρ₄_hi, hK₂_reg⟩ := BohrSet.regularity (κ₄ • K₁)
  set K₂ : BohrSet (ZMod q) := ρ₄ • (κ₄ • K₁) with hK₂_def
  have hρ₄_pos : 0 < ρ₄ := by positivity
  have hK₂_pos : K₂.PosWidth := (hK₁_pos.smul hκ₄_pos.ne').smul hρ₄_pos.ne'
  have hK₂_rk : K₂.rank ≤ d := by simpa [hK₂_def] using hK₁_rk
  have hK₂_sub_κ₄ : K₂.finset ⊆ (κ₄ • K₁).finset := by
    simpa [hK₂_def, one_smul] using BohrSet.smul_finset_mono hρ₄_pos.le hρ₄_hi
  have hK₂_sub_K₁ : K₂.finset ⊆ K₁.finset :=
    hK₂_sub_κ₄.trans (by simpa [one_smul] using BohrSet.smul_finset_mono hκ₄_pos.le hκ₄_le1)
  have hK₂_sub_κ₃ : K₂.finset ⊆ (κ₃ • C_bohr).finset := hK₂_sub_K₁.trans hK₁_sub_κ₃
  have hK₂_size :
      exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * #K₁.finset ≤ #K₂.finset := by
    rw [hL_def]
    refine card_reg_dilate_ge hK₁_rk hα₀ hα_le1 ?_ hκ₄_le1 hρ₄_lo hρ₄_hi
    rw [hκ₄_def, show (100 * (d + 1 : ℝ))⁻¹ = 100⁻¹ / (d + 1 : ℝ) by rw [mul_inv, div_eq_mul_inv]]
    exact div_le_div_of_nonneg_right (by linarith only [hα_le1]) hd_pos.le
  -- Positive-definite measure step (`pos_def_measures`)
  have hC_rk_real : (C_bohr.rank : ℝ) ≤ d := by exact_mod_cast hC_bohr_rk
  have hκ₃_400 : 100 * (C_bohr.rank : ℝ) * (4 * κ₃) ≤ 1 := by
    rw [hκ₃_def]
    have hrew : 100 * (C_bohr.rank : ℝ) * (4 * (400 * (d + 1 : ℝ))⁻¹) =
        (400 * C_bohr.rank) / (400 * (d + 1 : ℝ)) := by ring
    rw [hrew, div_le_one (by positivity)]
    linarith only [hC_rk_real]
  have hpdm := BohrFourier.pos_def_measures hC_bohr_reg hp_ne hp_even
    (μ_[ℝ] U - μ B'.finset) K₁.finset_nonempty K₂.finset_nonempty
    hκ₃_pos.le hκ₃_400 hK₁_sub_κ₃ hK₂_sub_κ₃
  set ν := (μ_[ℝ≥0] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset) with hν_def
  have hnorm_16 : (16⁻¹ : ℝ) ≤ (#B'.finset : ℝ) *
      ‖(μ_[ℝ] U - μ B'.finset) ○ᵈ (μ U - μ B'.finset)‖_[p, ν] := by
    have hhl' : (8 * #B'.finset : ℝ)⁻¹ ≤
        ‖(μ_[ℝ] U - μ B'.finset) ∗ᵈ (μ U - μ B'.finset)‖_[p, μ C_bohr.finset] := by
      rwa [show (2⁻¹ : ℝ) / (4 * #B'.finset) = (8 * #B'.finset : ℝ)⁻¹ by ring] at hhl
    have hcomb := (mul_le_mul_of_nonneg_left hhl' (by norm_num : (0 : ℝ) ≤ 2⁻¹)).trans hpdm
    rw [show (2⁻¹ : ℝ) * (8 * #B'.finset : ℝ)⁻¹ = (16⁻¹ : ℝ) / #B'.finset by ring,
      div_le_iff₀ hB'_pos_card] at hcomb
    rwa [mul_comm]
  -- `Lp_orth` on `B'`
  let h_pd : ZMod q → ℂ := μ_[ℂ] K₁.finset ∗ᵈ μ K₂.finset
  have hν_pd : h_pd ○ᵈ h_pd = (↑) ∘ ν := by
    symm
    have hcast : (↑) ∘ ν =
        (μ_[ℂ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset) := by
      ext y
      change ((ν y : ℝ) : ℂ) = _
      simp only [hν_def, ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply,
        NNReal.coe_sum, NNReal.coe_mul, NNReal.coe_mu, Complex.ofReal_sum,
        Complex.ofReal_mul, Complex.ofReal_mu]
    rw [hcast]
    apply dft_injective
    ext ψ
    simp only [h_pd, dft_ddconv_apply, dft_dddconv_apply, map_mul]
    ring
  have hν_sum : ∑ y : ZMod q, ν y = 1 := by
    have hreal : ∑ y : ZMod q, (ν y : ℝ) = 1 := by
      have hνR : (fun y ↦ (ν y : ℝ)) =
          (μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset) := by
        ext y
        simp only [hν_def, ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply,
          NNReal.coe_sum, NNReal.coe_mul, NNReal.coe_mu]
      rw [show (∑ y : ZMod q, (ν y : ℝ)) = ∑ y, ((μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ
          (μ K₂.finset ○ᵈ μ K₂.finset)) y by simp_rw [← hνR],
        sum_ddconv, sum_dddconv, sum_dddconv]
      simp [sum_mu ℝ K₁.finset_nonempty, sum_mu ℝ K₂.finset_nonempty]
    exact_mod_cast hreal
  have hK₁_sub_2κ₁ : K₁.finset ⊆ ((2 * κ₁) • B').finset :=
    (hK₁_sub_κ₃.trans (by simpa [one_smul] using
      BohrSet.smul_finset_mono hκ₃_pos.le hκ₃_le1)).trans hC_bohr_sub
  have hK₂_sub_2κ₁ : K₂.finset ⊆ ((2 * κ₁) • B').finset := hK₂_sub_K₁.trans hK₁_sub_2κ₁
  have hν_supp : ∀ y : ZMod q, ν y ≠ 0 → y ∈ ((8 * κ₁) • B').finset := by
    intro y hy
    have hyR :
        ((μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)) y ≠ 0 := by
      have heq :
          ((μ_[ℝ] K₁.finset ○ᵈ μ K₁.finset) ∗ᵈ (μ K₂.finset ○ᵈ μ K₂.finset)) y =
            (ν y : ℝ) := by
        simp only [hν_def, ddconv_eq_sum_sub', dddconv_eq_sum_sub', conj_mu_apply,
          NNReal.coe_sum, NNReal.coe_mul, NNReal.coe_mu]
      rw [heq]; exact_mod_cast hy
    rcases support_ddconv_subset _ _ hyR with ⟨u, hu, v, hv, rfl⟩
    rcases support_dddconv_subset' _ _ hu with ⟨a₁, ha₁, a₂, ha₂, rfl⟩
    rcases support_dddconv_subset' _ _ hv with ⟨b₁, hb₁, b₂, hb₂, rfl⟩
    have ha₁' : a₁ ∈ ((2 * κ₁) • B').finset := hK₁_sub_2κ₁ (by simpa using ha₁)
    have ha₂' : -a₂ ∈ ((2 * κ₁) • B').finset :=
      BohrSet.neg_mem_finset.mpr (hK₁_sub_2κ₁ (by simpa using ha₂))
    have hb₁' : b₁ ∈ ((2 * κ₁) • B').finset := hK₂_sub_2κ₁ (by simpa using hb₁)
    have hb₂' : -b₂ ∈ ((2 * κ₁) • B').finset :=
      BohrSet.neg_mem_finset.mpr (hK₂_sub_2κ₁ (by simpa using hb₂))
    have h12 : a₁ - a₂ ∈ ((4 * κ₁) • B').finset := by
      have hm := BohrSet.smul_add_smul_finset_subset (by positivity) (by positivity)
        (Finset.add_mem_add ha₁' ha₂')
      simpa [show (2 * κ₁ + 2 * κ₁ : ℝ) = 4 * κ₁ by ring, ← sub_eq_add_neg] using hm
    have h34 : b₁ - b₂ ∈ ((4 * κ₁) • B').finset := by
      have hm := BohrSet.smul_add_smul_finset_subset (by positivity) (by positivity)
        (Finset.add_mem_add hb₁' hb₂')
      simpa [show (2 * κ₁ + 2 * κ₁ : ℝ) = 4 * κ₁ by ring, ← sub_eq_add_neg] using hm
    have h1234 := BohrSet.smul_add_smul_finset_subset (by positivity) (by positivity)
      (Finset.add_mem_add h12 h34)
    simpa [show (4 * κ₁ + 4 * κ₁ : ℝ) = 8 * κ₁ by ring] using h1234
  have hB'_rk_real : (B'.rank : ℝ) ≤ d := by exact_mod_cast hB'_rk
  have hB'_rk_div : (B'.rank : ℝ) / (d + 1 : ℝ) ≤ 1 :=
    div_le_one_of_le₀ (hB'_rk_real.trans (le_add_of_nonneg_right zero_le_one)) hd_pos.le
  have hB'_rk_div_nn : 0 ≤ (B'.rank : ℝ) / (d + 1 : ℝ) :=
    div_nonneg (Nat.cast_nonneg _) hd_pos.le
  have h8κ₁_100 : 100 * (B'.rank : ℝ) * (8 * κ₁) ≤ 1 := by
    calc
      100 * (B'.rank : ℝ) * (8 * κ₁)
        = (800 * 2⁻¹ ^ 20) * α_B * ((B'.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
      _ ≤ (800 * 2⁻¹ ^ 20) * 1 * 1 :=
          mul_le_mul (mul_le_mul_of_nonneg_left hα_B_le1 (by norm_num))
            hB'_rk_div hB'_rk_div_nn (by norm_num)
      _ ≤ 1 := by norm_num
  have h8κ₁_1200 : 1200 * (B'.rank : ℝ) * (8 * κ₁) ≤ 16⁻¹ * α_U := by
    calc
      1200 * (B'.rank : ℝ) * (8 * κ₁)
        = (9600 * 2⁻¹ ^ 20) * α_B * ((B'.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
      _ ≤ (9600 * 2⁻¹ ^ 20) * α_B * 1 :=
          mul_le_mul_of_nonneg_left hB'_rk_div (mul_nonneg (by norm_num) hα_B_pos.le)
      _ ≤ 16⁻¹ * ((1 - 1024⁻¹) * α_B) := by
          rw [mul_one, ← mul_assoc]
          exact mul_le_mul_of_nonneg_right (by norm_num) hα_B_pos.le
      _ ≤ 16⁻¹ * α_U := mul_le_mul_of_nonneg_left hα_U_ge (by norm_num)
  obtain ⟨p', hp'1, hp'_upper, hlp_orth⟩ :=
    BohrStep.Lp_orth hB'_reg hU_sub_B' hU_ne hp_ne hα_U_def
      (by norm_num : (0 : ℝ) < 16⁻¹) (by norm_num) (mul_nonneg (by norm_num) hκ₁_pos.le)
      h8κ₁_100 h8κ₁_1200 hν_pd hν_sum hν_supp hnorm_16
  -- `prop_it` on `(B', K₁, K₂)`
  have hκ₄_100 : 100 * (d : ℝ) * κ₄ ≤ 1 := by
    rw [hκ₄_def, mul_inv_le_iff₀ (by positivity)]
    linarith only [hd_nn]
  have hlp_64 : 1 + (64⁻¹ : ℝ) ≤ (#B'.finset : ℝ) * ‖μ_[ℝ] U ○ᵈ μ U‖_[p', ν] := by
    rwa [show (1 + (16⁻¹ : ℝ) / 4) = 1 + 64⁻¹ by norm_num] at hlp_orth
  obtain ⟨K₃, _, hK₃_reg, hK₃_pos, hK₃_rk, hK₃_sz, hK₃_dens⟩ :=
    BohrStep.prop_it hK₁_reg hK₂_reg hK₂_pos hK₁_rk hK₂_rk
      hκ₄_pos.le hκ₄_100 hK₂_sub_κ₄ hU_sub_B' hU_ne hα_U_def
      (by norm_num : (0 : ℝ) < 64⁻¹) (by norm_num) hp'1 hlp_64
  -- Package `K₃` and translate of `U`
  have hp'_Lα : (p' : ℝ) ≤ 2 ^ 21 * L := by
    calc
      (p' : ℝ) ≤ 2 ^ 10 * (16⁻¹ : ℝ)⁻¹ ^ 2 * p := hp'_upper
      _ = 2 ^ 18 * (p : ℝ) := by ring
      _ ≤ 2 ^ 18 * (8 * L) := mul_le_mul_of_nonneg_left hp_upper (by positivity)
      _ = 2 ^ 21 * L := by ring
  have hL_U_le : 𝓛 α_U ≤ 2 * L := by
    rw [hL_def]
    calc
      𝓛 α_U ≤ 𝓛 (α / 2) := BohrFourier.curlog_anti (half_pos hα₀) hα_U_half
      _ ≤ 2 * 𝓛 α := BohrFourier.curlog_div_le hα₀ hα_le1 (by norm_num)
  have hα_U_le1 : α_U ≤ 1 := by
    rw [hα_U_def]
    exact div_le_one_of_le₀ (by exact_mod_cast Finset.card_le_card hU_sub_B') hB'_pos_card.le
  have hL_U_nn : 0 ≤ 𝓛 α_U :=
    zero_le_one.trans (BohrFourier.one_le_curlog hα_U_pos.le hα_U_le1)
  have hK₃_rk_final : (K₃.rank : ℝ) ≤ d + M100 ^ 3 * L ^ 8 := by
    have h200 : (2 : ℝ) ^ 128 / (64⁻¹ : ℝ) ^ 12 = M100 ^ 2 := by rw [M100_eq]; norm_num
    have h88 : ((2 : ℝ) ^ 21) ^ 4 * 2 ^ 4 ≤ M100 := by rw [M100_eq]; norm_num
    calc
      (K₃.rank : ℝ)
        ≤ d + 2 ^ 128 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 / (64⁻¹ : ℝ) ^ 12 := hK₃_rk
      _ = d + (2 ^ 128 / (64⁻¹ : ℝ) ^ 12) * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 := by ring
      _ = d + M100 ^ 2 * (p' : ℝ) ^ 4 * 𝓛 α_U ^ 4 := by rw [h200]
      _ ≤ d + M100 ^ 2 * (2 ^ 21 * L) ^ 4 * (2 * L) ^ 4 := by gcongr
      _ = d + M100 ^ 2 * (((2 : ℝ) ^ 21) ^ 4 * 2 ^ 4) * L ^ 8 := by ring
      _ ≤ d + M100 ^ 2 * M100 * L ^ 8 := by gcongr
      _ = d + M100 ^ 3 * L ^ 8 := by ring
  have hK₃_sz_final :
      exp (-M100 ^ 4 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10)) * #B.finset ≤
        #K₃.finset := by
    set E_dil : ℝ := exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)))
    have hE_dil_pos : 0 < E_dil := exp_pos _
    have h4_dil : E_dil ^ 4 * #B.finset ≤ #K₂.finset := by
      calc
        E_dil ^ 4 * #B.finset
          = E_dil * (E_dil * (E_dil ^ 2 * #B.finset)) := by ring
        _ ≤ E_dil * (E_dil * #C_bohr.finset) := by gcongr
        _ ≤ E_dil * #K₁.finset := by gcongr
        _ ≤ #K₂.finset := hK₂_size
    set E_prop : ℝ := exp (-2 ^ 140 * ((d + 1 : ℝ) *
      ((p' : ℝ) / (64⁻¹ : ℝ) ^ 2 * 𝓛 α_U + log (d + 1 : ℝ)) +
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 / (64⁻¹ : ℝ) ^ 14))
    have htot : E_prop * E_dil ^ 4 * #B.finset ≤ #K₃.finset := by
      rw [mul_assoc]
      exact (mul_le_mul_of_nonneg_left h4_dil (exp_pos _).le).trans hK₃_sz
    refine le_trans (mul_le_mul_of_nonneg_right ?_ (Nat.cast_nonneg _)) htot
    have hE_eq : E_prop * E_dil ^ 4 = exp (
        -2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
          (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84) +
        -128 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by
      dsimp [E_prop, E_dil]
      rw [← exp_nat_mul, ← exp_add]
      congr 1
      push_cast
      ring
    rw [hE_eq]
    apply exp_le_exp.mpr
    have h140_half : (2 : ℝ) ^ 140 ≤ 2⁻¹ * M100 ^ 2 := by rw [M100_eq]; norm_num
    have h34 : (2 : ℝ) ^ 34 ≤ M100 := two_pow_le_M100 (by omega)
    have h194 : (2 : ℝ) ^ 194 ≤ M100 ^ 2 := by rw [M100_eq]; norm_num
    have h128_base : (128 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
    have h128_M : (128 : ℝ) ≤ M100 ^ 3 :=
      h128_base.trans (le_self_pow₀ hM_ge1 (by omega))
    have h2M : (2 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
    have hp'L_prod : (p' : ℝ) * 2 ^ 12 * 𝓛 α_U ≤ M100 * L ^ 2 := by
      calc
        (p' : ℝ) * 2 ^ 12 * 𝓛 α_U
          ≤ (2 ^ 21 * L) * 2 ^ 12 * (2 * L) := by gcongr
        _ = (2 : ℝ) ^ 34 * L ^ 2 := by ring
        _ ≤ M100 * L ^ 2 := mul_le_mul_of_nonneg_right h34 (by positivity)
    have hp'5_prod : (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84 ≤ M100 ^ 2 * L ^ 10 := by
      calc
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84
          ≤ (2 ^ 21 * L) ^ 5 * (2 * L) ^ 5 * 2 ^ 84 := by gcongr
        _ = (2 : ℝ) ^ 194 * L ^ 10 := by ring
        _ ≤ M100 ^ 2 * L ^ 10 := mul_le_mul_of_nonneg_right h194 (by positivity)
    have hL_le_sq : L ≤ L ^ 2 := le_self_pow₀ hLα (by omega)
    set Q : ℝ := (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10
    have hQ_nn : 0 ≤ Q := by dsimp [Q]; positivity
    have hpart1_tight :
        2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
          (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84) ≤ 2⁻¹ * M100 ^ 4 * Q := by
      have hsub1 : (p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ) ≤
          M100 * (L ^ 2 + log (d + 1 : ℝ)) := by
        have hM_log : 1 * log (d + 1 : ℝ) ≤ M100 * log (d + 1 : ℝ) :=
          mul_le_mul_of_nonneg_right hM_ge1 hlog_d_nn
        have hrew : M100 * (L ^ 2 + log (d + 1 : ℝ)) =
            M100 * L ^ 2 + M100 * log (d + 1 : ℝ) := by ring
        linarith only [hp'L_prod, hM_log, hrew]
      have hsub2 : (d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
          (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84 ≤ M100 ^ 2 * Q := by
        have hm1 := mul_le_mul_of_nonneg_left hsub1 hd_pos.le
        have hm2 : M100 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ))) ≤
            M100 ^ 2 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ))) :=
          mul_le_mul_of_nonneg_right (le_self_pow₀ hM_ge1 (by omega)) (by positivity)
        have hr1 : (d + 1 : ℝ) * (M100 * (L ^ 2 + log (d + 1 : ℝ))) =
            M100 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ))) := by ring
        have hr2 : M100 ^ 2 * Q =
            M100 ^ 2 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ))) + M100 ^ 2 * L ^ 10 := by
          dsimp [Q]; ring
        linarith only [hm1, hm2, hp'5_prod, hr1, hr2]
      calc
        2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
            (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84)
          ≤ (2⁻¹ * M100 ^ 2) * (M100 ^ 2 * Q) :=
            mul_le_mul h140_half hsub2 (by positivity) (by positivity)
        _ = 2⁻¹ * M100 ^ 4 * Q := by ring
    have hpart2 : 128 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤ M100 ^ 3 * Q := by
      have hsub : (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤ Q := by
        dsimp [Q]
        have h1 : (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤
            (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) := by gcongr
        have h2 : 0 ≤ L ^ 10 := by positivity
        linarith only [h1, h2]
      calc
        128 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))
          = 128 * ((d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by ring
        _ ≤ M100 ^ 3 * Q := mul_le_mul h128_M hsub (by positivity) (by positivity)
    have hpart2_half : M100 ^ 3 * Q ≤ 2⁻¹ * M100 ^ 4 * Q := by
      have h1 : 2 * (M100 ^ 3 * Q) ≤ M100 * (M100 ^ 3 * Q) :=
        mul_le_mul_of_nonneg_right h2M (by positivity)
      have h2 : M100 * (M100 ^ 3 * Q) = M100 ^ 4 * Q := by ring
      linarith only [h1, h2]
    have hn1 : -128 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) =
        -(128 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by ring
    have hn2 : -2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84) =
      -(2 ^ 140 * ((d + 1 : ℝ) * ((p' : ℝ) * 2 ^ 12 * 𝓛 α_U + log (d + 1 : ℝ)) +
        (p' : ℝ) ^ 5 * 𝓛 α_U ^ 5 * 2 ^ 84)) := by ring
    have hn3 : -M100 ^ 4 * Q = -(2⁻¹ * M100 ^ 4 * Q) + -(2⁻¹ * M100 ^ 4 * Q) := by ring
    linarith only [hpart1_tight, hpart2, hpart2_half, hn1, hn2, hn3]
  have hK₃_inf' :
      (1 + 2048⁻¹ : ℝ) * α_B ≤ ‖𝟭_[(U : Set (ZMod q)), ℝ] ∗ᵈ μ K₃.finset‖_[∞] := by
    have h1 : (1 + 2048⁻¹ : ℝ) * α_B ≤ (1 + (64⁻¹ : ℝ) / 8) * α_U := by
      calc
        (1 + 2048⁻¹ : ℝ) * α_B
          ≤ (1 + (64⁻¹ : ℝ) / 8) * ((1 - 1024⁻¹ : ℝ) * α_B) := by
            rw [← mul_assoc]
            exact mul_le_mul_of_nonneg_right (by norm_num) hα_B_pos.le
        _ ≤ (1 + (64⁻¹ : ℝ) / 8) * α_U :=
            mul_le_mul_of_nonneg_left hα_U_ge (by norm_num)
    exact h1.trans hK₃_dens
  obtain ⟨y, hy⟩ := exists_vadd_inter_card_ge hK₃_inf'
  have hU_vadd_A : (-y +ᵥ U) ∩ K₃.finset ⊆ (-y + -x) +ᵥ A := by
    intro z hz
    rcases mem_vadd_finset.mp (mem_inter.mp hz).1 with ⟨u, hu, rfl⟩
    rcases mem_vadd_finset.mp (hU_sub_vxA hu) with ⟨a, ha, rfl⟩
    refine mem_vadd_finset.mpr ⟨a, ha, ?_⟩
    simp only [vadd_eq_add]; abel
  exact ⟨K₃, (-y +ᵥ U) ∩ K₃.finset, hK₃_reg, hK₃_pos, hK₃_rk_final,
    hK₃_sz_final, inter_subset_right, threeAPFree_vadd_subset hA_3ap hU_vadd_A, hy⟩

/-- Full single-step dichotomy on a regular Bohr set `B` in `ZMod q` (`q ≥ 3` prime):
either `#B.finset` is bounded in terms of `α⁻²` (up to one regular dilation), or we pass to a
regular `PosWidth` Bohr set `B_next` on which a translate of `A` has density
`≥ (1 + 2048⁻¹) * α_B` with controlled rank and size. -/
lemma bohr_step_dichotomy (hq : 3 ≤ q) {B : BohrSet (ZMod q)}
    (hB_reg : B.IsRegular) (hB_pos : B.PosWidth) {d : ℕ} (hB_rk : B.rank ≤ d)
    {A : Finset (ZMod q)} (hAB : A ⊆ B.finset)
    (hA_3ap : ThreeAPFree (α := ZMod q) (A : Set (ZMod q)))
    {α α_B : ℝ} (hα₀ : 0 < α) (hα_le : α ≤ α_B)
    (hα_B : α_B = (#A : ℝ) / #B.finset) :
    (exp (-32 * (d + 1 : ℝ) * (𝓛 α + log (d + 1 : ℝ))) * #B.finset ≤ 8 * α⁻¹ ^ 2) ∨
    (∃ (B_next : BohrSet (ZMod q)) (A_next : Finset (ZMod q)),
      B_next.IsRegular ∧
      B_next.PosWidth ∧
      (B_next.rank : ℝ) ≤ d + M100 ^ 3 * 𝓛 α ^ 8 ∧
      exp (-M100 ^ 4 * ((d + 1 : ℝ) * (𝓛 α ^ 2 + log (d + 1 : ℝ)) + 𝓛 α ^ 10)) * #B.finset ≤
        #B_next.finset ∧
      A_next ⊆ B_next.finset ∧
      ThreeAPFree (α := ZMod q) (A_next : Set (ZMod q)) ∧
      (1 + 2048⁻¹ : ℝ) * α_B * #B_next.finset ≤ #A_next) := by
  let : MeasurableSpace (ZMod q) := ⊤
  have hM_pos : 0 < M100 := M100_pos
  have hM_ge1 : 1 ≤ M100 := one_le_M100
  have hB_card_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
  have hA_le_B : (#A : ℝ) ≤ #B.finset := by exact_mod_cast Finset.card_le_card hAB
  have hα_B_pos : 0 < α_B := hα₀.trans_le hα_le
  have hα_B_le1 : α_B ≤ 1 := by rw [hα_B]; exact div_le_one_of_le₀ hA_le_B hB_card_pos.le
  have hα_le1 : α ≤ 1 := hα_le.trans hα_B_le1
  obtain ⟨L, hL_def⟩ : ∃ L : ℝ, L = 𝓛 α := ⟨𝓛 α, rfl⟩
  rw [← hL_def]
  have hLα : 1 ≤ L := by rw [hL_def]; exact BohrFourier.one_le_curlog hα₀.le hα_le1
  have hd_pos : 0 < (d + 1 : ℝ) := by positivity
  have hd_nn : 0 ≤ (d : ℝ) := Nat.cast_nonneg d
  have hlog_d_nn : 0 ≤ log (d + 1 : ℝ) := log_nonneg (by linarith only [hd_nn])
  -- Regular sub-Bohr sets `B'` and `B''`
  set κ₁ : ℝ := 2⁻¹ ^ 20 * α_B / (d + 1 : ℝ) with hκ₁_def
  have hκ₁_pos : 0 < κ₁ := by rw [hκ₁_def]; positivity
  have hκ₁_le1 : κ₁ ≤ 1 := by rw [hκ₁_def, div_le_one hd_pos]; linarith only [hα_B_le1, hd_nn]
  obtain ⟨ρ₁, hρ₁_lo, hρ₁_hi, hB'_reg⟩ := BohrSet.regularity (κ₁ • B)
  set B' : BohrSet (ZMod q) := ρ₁ • (κ₁ • B) with hB'_def
  have hρ₁_pos : 0 < ρ₁ := by positivity
  have hB'_pos : B'.PosWidth := (hB_pos.smul hκ₁_pos.ne').smul hρ₁_pos.ne'
  have hB'_rk : B'.rank ≤ d := by simpa [hB'_def] using hB_rk
  have hB'_sub : B'.finset ⊆ (κ₁ • B).finset := by
    simpa [hB'_def, one_smul] using BohrSet.smul_finset_mono hρ₁_pos.le hρ₁_hi
  have hB'_size :
      exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * #B.finset ≤ #B'.finset := by
    rw [hL_def]
    exact card_reg_dilate_ge hB_rk hα₀ hα_le1
      (by rw [hκ₁_def]; gcongr) hκ₁_le1 hρ₁_lo hρ₁_hi
  obtain ⟨ρ₂, hρ₂_lo, hρ₂_hi, hB''_reg⟩ := BohrSet.regularity (κ₁ • B')
  set B'' : BohrSet (ZMod q) := ρ₂ • (κ₁ • B') with hB''_def
  have hρ₂_pos : 0 < ρ₂ := by positivity
  have hB''_pos : B''.PosWidth := (hB'_pos.smul hκ₁_pos.ne').smul hρ₂_pos.ne'
  have hB''_rk : B''.rank ≤ d := by simpa [hB''_def] using hB'_rk
  have hB''_sub_B' : B''.finset ⊆ B'.finset := by
    have h1 : B''.finset ⊆ (κ₁ • B').finset := by
      simpa [hB''_def, one_smul] using BohrSet.smul_finset_mono hρ₂_pos.le hρ₂_hi
    exact h1.trans (by simpa [one_smul] using BohrSet.smul_finset_mono hκ₁_pos.le hκ₁_le1)
  have hB''_sub_κB : B''.finset ⊆ (κ₁ • B).finset := hB''_sub_B'.trans hB'_sub
  have hB''_size :
      exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * #B'.finset ≤ #B''.finset := by
    rw [hL_def]
    exact card_reg_dilate_ge hB'_rk hα₀ hα_le1
      (by rw [hκ₁_def]; gcongr) hκ₁_le1 hρ₂_lo hρ₂_hi
  -- Helper to package immediate Bourgain density-increment branches (`B'` or `B''`)
  have h_early_branch : ∀ (K : BohrSet (ZMod q)), K.IsRegular → K.PosWidth → K.rank ≤ d →
      exp (-64 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) * #B.finset ≤ #K.finset →
      (1 + (2⁻¹ ^ 9 : ℝ) / 4) * α_B ≤ ‖𝟭_[(A : Set (ZMod q)), ℝ] ∗ᵈ μ K.finset‖_[∞] →
      ∃ (B_next : BohrSet (ZMod q)) (A_next : Finset (ZMod q)),
        B_next.IsRegular ∧ B_next.PosWidth ∧
        (B_next.rank : ℝ) ≤ d + M100 ^ 3 * L ^ 8 ∧
        exp (-M100 ^ 4 * ((d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10)) * #B.finset ≤
          #B_next.finset ∧
        A_next ⊆ B_next.finset ∧ ThreeAPFree (α := ZMod q) (A_next : Set (ZMod q)) ∧
        (1 + 2048⁻¹ : ℝ) * α_B * #B_next.finset ≤ #A_next := by
    intro K hK_reg hK_pos hK_rk hK_sz hK_inf
    have hK_inf' :
        (1 + 2048⁻¹ : ℝ) * α_B ≤ ‖𝟭_[(A : Set (ZMod q)), ℝ] ∗ᵈ μ K.finset‖_[∞] := by
      rwa [show (1 + (2⁻¹ ^ 9 : ℝ) / 4) = 1 + 2048⁻¹ by norm_num] at hK_inf
    obtain ⟨y, hy⟩ := exists_vadd_inter_card_ge hK_inf'
    refine ⟨K, (-y +ᵥ A) ∩ K.finset, hK_reg, hK_pos, ?_, ?_, inter_subset_right,
      threeAPFree_vadd_subset hA_3ap inter_subset_left, hy⟩
    · have h1 : (K.rank : ℝ) ≤ d := by exact_mod_cast hK_rk
      have h2 : 0 ≤ M100 ^ 3 * L ^ 8 := by positivity
      linarith only [h1, h2]
    · refine le_trans (mul_le_mul_of_nonneg_right (exp_le_exp.mpr ?_) (Nat.cast_nonneg _)) hK_sz
      have h64_M : (64 : ℝ) ≤ M100 := by rw [M100_eq]; norm_num
      have h64_le : (64 : ℝ) ≤ M100 ^ 4 := h64_M.trans (le_self_pow₀ hM_ge1 (by omega))
      have hL_sq : L ≤ L ^ 2 := le_self_pow₀ hLα (by omega)
      have hterm_le : (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤
          (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) + L ^ 10 := by
        have h1 : (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) ≤
            (d + 1 : ℝ) * (L ^ 2 + log (d + 1 : ℝ)) := by gcongr
        have h2 : 0 ≤ L ^ 10 := by positivity
        linarith only [h1, h2]
      have hmul := mul_le_mul h64_le hterm_le (by positivity) (by positivity)
      have hr1 : (64 : ℝ) * ((d + 1 : ℝ) * (L + log (d + 1 : ℝ))) =
          64 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) := by ring
      linarith only [hmul, hr1]
  -- Verify Bourgain trick hypotheses
  have hB_rk_real : (B.rank : ℝ) ≤ d := by exact_mod_cast hB_rk
  have hB_rk_div : (B.rank : ℝ) / (d + 1 : ℝ) ≤ 1 :=
    div_le_one_of_le₀ (hB_rk_real.trans (le_add_of_nonneg_right zero_le_one)) hd_pos.le
  have hB_rk_div_nn : 0 ≤ (B.rank : ℝ) / (d + 1 : ℝ) :=
    div_nonneg (Nat.cast_nonneg _) hd_pos.le
  have hκ₁_100 : 100 * (B.rank : ℝ) * κ₁ ≤ 1 := by
    calc
      100 * (B.rank : ℝ) * κ₁
        = (100 * 2⁻¹ ^ 20) * α_B * ((B.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
      _ ≤ (100 * 2⁻¹ ^ 20) * 1 * 1 :=
          mul_le_mul (mul_le_mul_of_nonneg_left hα_B_le1 (by norm_num))
            hB_rk_div hB_rk_div_nn (by norm_num)
      _ ≤ 1 := by norm_num
  have hκ₁_200 : 200 * (B.rank : ℝ) * κ₁ ≤ 2⁻¹ ^ 9 * α_B / 8 := by
    calc
      200 * (B.rank : ℝ) * κ₁
        = (200 * 2⁻¹ ^ 20) * α_B * ((B.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
      _ ≤ (200 * 2⁻¹ ^ 20) * α_B * 1 :=
          mul_le_mul_of_nonneg_left hB_rk_div (mul_nonneg (by norm_num) hα_B_pos.le)
      _ ≤ 2⁻¹ ^ 9 * α_B / 8 := by
          rw [mul_one, show 2⁻¹ ^ 9 * α_B / 8 = (2⁻¹ ^ 9 / 8) * α_B by ring]
          exact mul_le_mul_of_nonneg_right (by norm_num) hα_B_pos.le
  rcases BohrSet.bourgain_trick hB_reg hAB B'.finset_nonempty B''.finset_nonempty
      (BohrSet.neg_finset B') (BohrSet.neg_finset B'') hα_B (by norm_num : (0 : ℝ) < 2⁻¹ ^ 9)
      hκ₁_pos.le hκ₁_100 hκ₁_200 hB'_sub hB''_sub_κB with hbr1 | hbr2 | ⟨x, hU_card, hW_card⟩
  · refine Or.inr (h_early_branch B' hB'_reg hB'_pos hB'_rk ?_ hbr1)
    refine le_trans (mul_le_mul_of_nonneg_right (exp_le_exp.mpr ?_) (Nat.cast_nonneg _)) hB'_size
    have hnn : 0 ≤ (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) := by positivity
    have hr1 : -64 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) =
        -64 * ((d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by ring
    have hr2 : -32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)) =
        -32 * ((d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by ring
    linarith only [hnn, hr1, hr2]
  · refine Or.inr (h_early_branch B'' hB''_reg hB''_pos hB''_rk ?_ hbr2)
    have hcomb : exp (-64 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) =
        exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) *
          exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ))) := by
      rw [← exp_add]; congr 1; ring
    rw [hcomb, mul_assoc]
    exact (mul_le_mul_of_nonneg_left hB'_size (exp_pos _).le).trans hB''_size
  · set A_x : Finset (ZMod q) := -x +ᵥ A
    have hAx_3ap : ThreeAPFree (α := ZMod q) (A_x : Set (ZMod q)) :=
      threeAPFree_vadd_subset hA_3ap Subset.rfl
    set U : Finset (ZMod q) := A_x ∩ B'.finset
    set W : Finset (ZMod q) := A_x ∩ B''.finset
    have hB'_pos_card : (0 : ℝ) < #B'.finset := by exact_mod_cast B'.card_finset_pos
    have hB''_pos_card : (0 : ℝ) < #B''.finset := by exact_mod_cast B''.card_finset_pos
    set α_U : ℝ := (#U : ℝ) / #B'.finset with hα_U_def
    set γ : ℝ := (#W : ℝ) / #B''.finset with hγ_def
    have h1024 : (1 - (2⁻¹ ^ 9 : ℝ) / 2) = 1 - 1024⁻¹ := by norm_num
    rw [h1024] at hU_card hW_card
    have hα_U_ge : (1 - 1024⁻¹ : ℝ) * α_B ≤ α_U := by
      rw [hα_U_def, le_div_iff₀ hB'_pos_card]; exact hU_card
    have hγ_ge : (1 - 1024⁻¹ : ℝ) * α_B ≤ γ := by
      rw [hγ_def, le_div_iff₀ hB''_pos_card]; exact hW_card
    have hα_U_half : α / 2 ≤ α_U := by linarith only [hα_le, hα_U_ge, hα₀]
    have hγ_half : α / 2 ≤ γ := by linarith only [hα_le, hγ_ge, hα₀]
    have hγ_pos : 0 < γ := (half_pos hα₀).trans_le hγ_half
    have hU_ne : U.Nonempty := by
      rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
      have : 0 < (1 - 1024⁻¹ : ℝ) * α_B * #B'.finset :=
        mul_pos (mul_pos (by norm_num) hα_B_pos) hB'_pos_card
      exact this.trans_le hU_card
    have hW_ne : W.Nonempty := by
      rw [← Finset.card_pos, ← @Nat.cast_pos ℝ]
      have : 0 < (1 - 1024⁻¹ : ℝ) * α_B * #B''.finset :=
        mul_pos (mul_pos (by norm_num) hα_B_pos) hB''_pos_card
      exact this.trans_le hW_card
    -- Dichotomy on `#U ^ 2` vs `2 * #B'.finset`
    by_cases hU_small : (#U : ℝ) ^ 2 ≤ 2 * #B'.finset
    · refine Or.inl (hB'_size.trans ?_)
      have hU_lb : (α / 2) * #B'.finset ≤ #U := by
        have := mul_le_mul_of_nonneg_right hα_U_half hB'_pos_card.le
        rwa [hα_U_def, div_mul_cancel₀ _ hB'_pos_card.ne'] at this
      have hsq : (α / 2) ^ 2 * (#B'.finset : ℝ) ^ 2 ≤ 2 * #B'.finset := by
        have h1 : ((α / 2) * #B'.finset) ^ 2 ≤ (#U : ℝ) ^ 2 :=
          pow_le_pow_left₀ (mul_nonneg (half_pos hα₀).le hB'_pos_card.le) hU_lb 2
        have hr : ((α / 2) * #B'.finset) ^ 2 = (α / 2) ^ 2 * (#B'.finset : ℝ) ^ 2 := by ring
        linarith only [h1, hU_small, hr]
      have hdiv : (α / 2) ^ 2 * (#B'.finset : ℝ) ≤ 2 := by
        nlinarith only [hsq, hB'_pos_card]
      have hr_inv : (α / 2) ^ 2 * (#B'.finset : ℝ) = 4⁻¹ * ((#B'.finset : ℝ) * α ^ 2) := by ring
      have hinv : (#B'.finset : ℝ) * α ^ 2 ≤ 8 := by linarith only [hdiv, hr_inv]
      calc
        (#B'.finset : ℝ) = ((#B'.finset : ℝ) * α ^ 2) * (α ^ 2)⁻¹ := by
          field_simp [hα₀.ne']
        _ ≤ 8 * (α ^ 2)⁻¹ := mul_le_mul_of_nonneg_right hinv (by positivity)
        _ = 8 * α⁻¹ ^ 2 := by rw [inv_pow]
    · push Not at hU_small
      refine Or.inr ?_
      set C_bohr : BohrSet (ZMod q) := BohrSet.twoBohr hq B'' with hC_bohr_def
      have hC_bohr_reg : C_bohr.IsRegular := BohrSet.twoBohr_isRegular hq hB''_reg
      have hC_bohr_pos : C_bohr.PosWidth := BohrSet.twoBohr_posWidth hq hB''_pos
      have hC_bohr_rk : C_bohr.rank ≤ d := by simpa [hC_bohr_def] using hB''_rk
      have hC_bohr_card : #C_bohr.finset = #B''.finset := BohrSet.card_twoBohr_finset hq B''
      have hC_bohr_sub : C_bohr.finset ⊆ ((2 * κ₁) • B').finset := by
        intro z hz
        have hz2 : z ∈ ((2 : ℝ) • B'').finset :=
          BohrSet.twoBohr_finset_subset_two_smul hq B'' hz
        have hB''_smul : (2 : ℝ) • B'' = (2 * ρ₂ * κ₁) • B' := by
          rw [hB''_def, smul_smul, smul_smul]
        rw [hB''_smul] at hz2
        have h2ρ : 2 * ρ₂ * κ₁ ≤ 2 * κ₁ :=
          mul_le_mul_of_nonneg_right (by linarith only [hρ₂_hi]) hκ₁_pos.le
        exact BohrSet.smul_finset_mono (by positivity) h2ρ hz2
      have hC_sz2 :
          (exp (-32 * (d + 1 : ℝ) * (L + log (d + 1 : ℝ)))) ^ 2 * #B.finset ≤
            #C_bohr.finset := by
        rw [hC_bohr_card, sq, mul_assoc]
        exact (mul_le_mul_of_nonneg_left hB'_size (exp_pos _).le).trans hB''_size
      set C : Finset (ZMod q) := W.image (fun z ↦ (2 : ZMod q) * z)
      have hC_sub_bohr : C ⊆ C_bohr.finset := by
        rw [hC_bohr_def, BohrSet.twoBohr_finset hq B'']
        exact Finset.image_subset_image inter_subset_right
      have hC_card_W : #C = #W :=
        Finset.card_image_of_injective W (BohrSet.twoEquiv hq).injective
      have hγ_C : γ * #C_bohr.finset ≤ #C := by
        rw [hC_bohr_card, hC_card_W, hγ_def, div_mul_cancel₀ _ hB''_pos_card.ne']
      obtain ⟨_, hinner_ub⟩ :=
        threeAPFree_inner_sub hq hAx_3ap inter_subset_left inter_subset_left hW_ne
      have hUC_dev : (2⁻¹ : ℝ) ≤ |(#B'.finset : ℝ) * ⟪μ_[ℝ] U ∗ᵈ μ U, μ C⟫_[ℝ] - 1| := by
        have hU_sq_pos : 0 < (#U : ℝ) ^ 2 := pow_pos (Nat.cast_pos.mpr hU_ne.card_pos) 2
        have hlt_half : (#B'.finset : ℝ) * ⟪μ_[ℝ] U ∗ᵈ μ U, μ C⟫_[ℝ] ≤ 2⁻¹ := by
          have h1 := mul_le_mul_of_nonneg_left hinner_ub hB'_pos_card.le
          refine h1.trans ?_
          rw [mul_inv_le_iff₀ hU_sq_pos]
          linarith only [hU_small]
        rw [abs_sub_comm, abs_of_nonneg (by linarith only [hlt_half])]
        linarith only [hlt_half]
      have hB'_rk_real : (B'.rank : ℝ) ≤ d := by exact_mod_cast hB'_rk
      have hB'_rk_div : (B'.rank : ℝ) / (d + 1 : ℝ) ≤ 1 :=
        div_le_one_of_le₀ (hB'_rk_real.trans (le_add_of_nonneg_right zero_le_one)) hd_pos.le
      have hB'_rk_div_nn : 0 ≤ (B'.rank : ℝ) / (d + 1 : ℝ) :=
        div_nonneg (Nat.cast_nonneg _) hd_pos.le
      have h2κ₁_100 : 100 * (B'.rank : ℝ) * (2 * κ₁) ≤ 1 := by
        calc
          100 * (B'.rank : ℝ) * (2 * κ₁)
            = (200 * 2⁻¹ ^ 20) * α_B * ((B'.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
          _ ≤ (200 * 2⁻¹ ^ 20) * 1 * 1 :=
              mul_le_mul (mul_le_mul_of_nonneg_left hα_B_le1 (by norm_num))
                hB'_rk_div hB'_rk_div_nn (by norm_num)
          _ ≤ 1 := by norm_num
      have h2κ₁_1200 : 1200 * (B'.rank : ℝ) * (2 * κ₁) ≤ 2⁻¹ * α_U := by
        calc
          1200 * (B'.rank : ℝ) * (2 * κ₁)
            = (2400 * 2⁻¹ ^ 20) * α_B * ((B'.rank : ℝ) / (d + 1 : ℝ)) := by rw [hκ₁_def]; ring
          _ ≤ (2400 * 2⁻¹ ^ 20) * α_B * 1 :=
              mul_le_mul_of_nonneg_left hB'_rk_div (mul_nonneg (by norm_num) hα_B_pos.le)
          _ ≤ 2⁻¹ * ((1 - 1024⁻¹) * α_B) := by
              rw [mul_one, ← mul_assoc]
              exact mul_le_mul_of_nonneg_right (by norm_num) hα_B_pos.le
          _ ≤ 2⁻¹ * α_U := mul_le_mul_of_nonneg_left hα_U_ge (by norm_num)
      have hhl := BohrStep.hoelder_lifting hB'_reg inter_subset_right hU_ne hC_sub_bohr
        hα_U_def hγ_pos hγ_C C_bohr.finset_nonempty (by norm_num : (0 : ℝ) < 2⁻¹)
        (mul_nonneg zero_le_two hκ₁_pos.le) h2κ₁_100 h2κ₁_1200
        (hC_sub_bohr.trans hC_bohr_sub) hUC_dev
      set p : ℕ := 2 * ⌈𝓛 γ⌉₊ with hp_def
      have hp_even : Even p := even_two_mul _
      have hγ_le1 : γ ≤ 1 := by
        rw [hγ_def]
        exact div_le_one_of_le₀ (by exact_mod_cast Finset.card_le_card inter_subset_right)
          hB''_pos_card.le
      have hp_ne : p ≠ 0 := by
        rw [hp_def]
        exact mul_ne_zero two_ne_zero
          (Nat.ceil_pos.mpr (BohrFourier.curlog_pos hγ_pos.le hγ_le1)).ne'
      have hp_upper : (p : ℝ) ≤ 8 * L := by
        have hLγ_le : 𝓛 γ ≤ 2 * L := by
          rw [hL_def]
          calc
            𝓛 γ ≤ 𝓛 (α / 2) := BohrFourier.curlog_anti (half_pos hα₀) hγ_half
            _ ≤ 2 * 𝓛 α := BohrFourier.curlog_div_le hα₀ hα_le1 (by norm_num)
        have h1_Lγ := BohrFourier.one_le_curlog hγ_pos.le hγ_le1
        have hceil : (⌈𝓛 γ⌉₊ : ℝ) ≤ 𝓛 γ + 1 :=
          (Nat.ceil_lt_add_one (zero_le_one.trans h1_Lγ)).le
        have hp_cast : (p : ℝ) = 2 * (⌈𝓛 γ⌉₊ : ℝ) := by
          rw [hp_def, Nat.cast_mul, Nat.cast_ofNat]
        linarith only [hp_cast, hLγ_le, h1_Lγ, hLα, hceil]
      exact bohr_step_from_lifting hB'_reg hB'_rk hC_bohr_reg hC_bohr_pos hC_bohr_rk
        inter_subset_right hU_ne inter_subset_left hA_3ap hα₀ hα_le1 hα_B_pos hα_B_le1
        hL_def hκ₁_def hC_bohr_sub hC_sz2 hα_U_def hα_U_ge hα_U_half
        hp_ne hp_even hp_upper hhl

/-- The Kelley-Meka `1/12` upper bound for `3AP`-free subsets of `ZMod q` (`q ≥ 3` prime). -/
theorem zmod_prime_threeAPFree :
    ∃ c > 0, ∃ C > 0, ∀ (q : ℕ) [Fact q.Prime], 3 ≤ q →
      ∀ (A₀ : Finset (ZMod q)), ThreeAPFree (α := ZMod q) A₀ →
        (#A₀ : ℝ) ≤ C * q / exp (c * log q ^ (12⁻¹ : ℝ)) := by
  have hM_pos : 0 < M100 := M100_pos
  let c : ℝ := ((2 * M100 ^ 12) ^ (12⁻¹ : ℝ))⁻¹
  let C : ℝ := exp 1
  refine ⟨c, by positivity, C, exp_pos 1, fun q _ hq A₀ hA₀_3ap ↦ ?_⟩
  rcases A₀.eq_empty_or_nonempty with rfl | hA₀_ne
  · simp only [card_empty, CharP.cast_eq_zero]; positivity
  have hq_card : #(Finset.univ : Finset (ZMod q)) = q := by simp [ZMod.card]
  have hq_pos : (0 : ℝ) < q := by positivity
  have hA₀_le_q : (#A₀ : ℝ) ≤ q := by
    have hc : #A₀ ≤ q := (Finset.card_le_card (subset_univ A₀)).trans_eq hq_card
    exact_mod_cast hc
  set α : ℝ := (#A₀ : ℝ) / q with hα_def
  have hα₀ : 0 < α := by
    rw [hα_def]
    have : (0 : ℝ) < #A₀ := by exact_mod_cast hA₀_ne.card_pos
    positivity
  have hα₁ : α ≤ 1 := by rw [hα_def]; exact div_le_one_of_le₀ hA₀_le_q hq_pos.le
  obtain ⟨L, hL_def⟩ : ∃ L : ℝ, L = 𝓛 α := ⟨𝓛 α, rfl⟩
  have hLα : 1 ≤ L := by rw [hL_def]; exact BohrFourier.one_le_curlog hα₀.le hα₁
  set r_inc : ℝ := 1 + 2048⁻¹
  have hr_gt1 : 1 < r_inc := by dsimp [r_inc]; norm_num
  have hlog_r_pos : 0 < log r_inc := log_pos hr_gt1
  have hlog_r_lb : (2⁻¹ ^ 12 : ℝ) ≤ log r_inc := by
    have h1 := Real.one_sub_inv_le_log_of_pos (by positivity : 0 < r_inc)
    have h2 : (2⁻¹ ^ 12 : ℝ) ≤ 1 - r_inc⁻¹ := by dsimp [r_inc]; norm_num
    exact h2.trans h1
  set T : ℕ := ⌊L / log r_inc⌋₊ + 1 with hT_def
  have hT_ub : (T : ℝ) ≤ 2 ^ 13 * L := by
    have hdiv_ub : L / log r_inc ≤ 2 ^ 12 * L := by
      rw [div_le_iff₀ hlog_r_pos]
      calc
        L = (2 : ℝ) ^ 12 * L * 2⁻¹ ^ 12 := by ring
        _ ≤ (2 : ℝ) ^ 12 * L * log r_inc :=
          mul_le_mul_of_nonneg_left hlog_r_lb (by positivity)
    have hfl : (⌊L / log r_inc⌋₊ : ℝ) ≤ 2 ^ 12 * L :=
      (Nat.floor_le (by positivity)).trans hdiv_ub
    rw [hT_def]; push_cast; linarith
  -- Finite density-increment loop invariant `P i` (`0 ≤ i ≤ T`)
  let P (i : ℕ) : Prop :=
    ((q : ℝ) ≤ exp (M100 ^ 12 * L ^ 12)) ∨
    (∃ (B : BohrSet (ZMod q)) (A : Finset (ZMod q)),
      B.IsRegular ∧ B.PosWidth ∧
      (B.rank : ℝ) ≤ (i : ℝ) * (M100 ^ 3 * L ^ 8) ∧
      exp (-(i : ℝ) * (M100 ^ 10 * L ^ 11)) * q ≤ #B.finset ∧
      A ⊆ B.finset ∧
      ThreeAPFree (α := ZMod q) (A : Set (ZMod q)) ∧
      r_inc ^ i * α * #B.finset ≤ #A)
  have hP0 : P 0 := by
    refine Or.inr ⟨⊤, A₀, isRegular_top, BohrSet.posWidth_top, ?_, ?_, ?_, hA₀_3ap, ?_⟩
    · simp
    · simp [BohrSet.top_finset, hq_card]
    · simp [BohrSet.top_finset]
    · simp [BohrSet.top_finset, hq_card, hα_def, div_mul_cancel₀ _ hq_pos.ne']
  have hP_step : ∀ i : ℕ, i < T → P i → P (i + 1) := by
    intro i hiT hPi
    rcases hPi with hdone | ⟨B, A, hB_reg, hB_pos, hB_rk, hB_sz, hAB, hA_3ap, hA_dens⟩
    · exact Or.inl hdone
    have hi_real : (i : ℝ) ≤ 2 ^ 13 * L := (Nat.cast_le.mpr hiT.le).trans hT_ub
    have hd_ub : (B.rank + 1 : ℝ) ≤ M100 ^ 4 * L ^ 9 := step_d_ub hLα hi_real hB_rk
    have hlog_d_ub : log (B.rank + 1 : ℝ) ≤ M100 * L := step_log_d_ub hLα hd_ub
    have hB_card_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
    set α_B : ℝ := (#A : ℝ) / #B.finset with hα_B_def
    have hα_B_ge_pow : r_inc ^ i * α ≤ α_B := by
      rw [hα_B_def, le_div_iff₀ hB_card_pos]; exact hA_dens
    have hα_le_B : α ≤ α_B := by
      have hr_pow : 1 ≤ r_inc ^ i := one_le_pow₀ hr_gt1.le
      exact (le_mul_of_one_le_left hα₀.le hr_pow).trans hα_B_ge_pow
    have hstep :=
      bohr_step_dichotomy hq hB_reg hB_pos le_rfl hAB hA_3ap hα₀ hα_le_B hα_B_def
    rw [← hL_def] at hstep
    rcases hstep with
      h_term | ⟨B_next, A_next, hBn_reg, hBn_pos, hBn_rk, hBn_sz, hAn_sub, hAn_3ap, hAn_dens⟩
    · exact Or.inl (step_term_bound hα₀ hα₁ hL_def hi_real hd_ub hlog_d_ub hB_sz h_term)
    · refine Or.inr ⟨B_next, A_next, hBn_reg, hBn_pos, ?_, ?_, hAn_sub, hAn_3ap, ?_⟩
      · calc
          (B_next.rank : ℝ) ≤ B.rank + M100 ^ 3 * L ^ 8 := hBn_rk
          _ ≤ (i : ℝ) * (M100 ^ 3 * L ^ 8) + M100 ^ 3 * L ^ 8 := by gcongr
          _ = ((i + 1 : ℕ) : ℝ) * (M100 ^ 3 * L ^ 8) := by push_cast; ring
      · have hstep_exp := step_size_exp hLα hd_ub hlog_d_ub
        have hexp_split : exp (-((i + 1 : ℕ) : ℝ) * (M100 ^ 10 * L ^ 11)) * q =
            exp (-M100 ^ 10 * L ^ 11) * (exp (-(i : ℝ) * (M100 ^ 10 * L ^ 11)) * q) := by
          rw [← mul_assoc (exp _), ← exp_add]
          congr 2; push_cast; ring
        rw [hexp_split]
        have hexp_le : exp (-M100 ^ 10 * L ^ 11) ≤
            exp (-M100 ^ 4 * ((B.rank + 1 : ℝ) * (L ^ 2 + log (B.rank + 1 : ℝ)) + L ^ 10)) := by
          apply exp_le_exp.mpr
          linarith [show -M100 ^ 10 * L ^ 11 = -(M100 ^ 10 * L ^ 11) by ring,
            show -M100 ^ 4 * ((B.rank + 1 : ℝ) * (L ^ 2 + log (B.rank + 1 : ℝ)) + L ^ 10) =
              -(M100 ^ 4 * ((B.rank + 1 : ℝ) * (L ^ 2 + log (B.rank + 1 : ℝ)) + L ^ 10))
              by ring]
        exact (mul_le_mul hexp_le hB_sz (by positivity) (exp_pos _).le).trans hBn_sz
      · calc
          r_inc ^ (i + 1) * α * #B_next.finset
            = r_inc * (r_inc ^ i * α) * #B_next.finset := by rw [pow_succ']; ring
          _ ≤ r_inc * α_B * #B_next.finset := by gcongr
          _ ≤ #A_next := hAn_dens
  have hPT : P T := by
    have hind : ∀ i : ℕ, i ≤ T → P i := by
      intro i
      induction i with
      | zero => intro _; exact hP0
      | succ i ih => intro hi; exact hP_step i (Nat.lt_of_succ_le hi) (ih (Nat.le_of_succ_le hi))
    exact hind T le_rfl
  have hq_exp_bound : (q : ℝ) ≤ exp (M100 ^ 12 * L ^ 12) := by
    rcases hPT with hdone | ⟨B, A, -, -, -, -, hAB, -, hA_dens⟩
    · exact hdone
    · exfalso
      have hB_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
      have hA_le_B : (#A : ℝ) ≤ #B.finset := by exact_mod_cast Finset.card_le_card hAB
      have hle1 : r_inc ^ T * α ≤ 1 := by
        have := hA_dens.trans hA_le_B
        exact (mul_le_iff_le_one_left hB_pos).mp (by linarith)
      have hT_gt : log α⁻¹ / log r_inc < T := by
        have h1 : log α⁻¹ / log r_inc < L / log r_inc :=
          div_lt_div_of_pos_right (by linarith) hlog_r_pos
        exact h1.trans (by rw [hT_def]; push_cast; exact Nat.lt_floor_add_one _)
      have hmul_gt : log α⁻¹ < T * log r_inc := (div_lt_iff₀ hlog_r_pos).mp hT_gt
      have hexp_gt : α⁻¹ < r_inc ^ T := by
        rw [← exp_log (inv_pos.mpr hα₀), ← exp_log (pow_pos (by positivity) T), log_pow]
        exact exp_lt_exp.mpr hmul_gt
      have hgt1 : 1 < r_inc ^ T * α := by
        have := mul_lt_mul_of_pos_right hexp_gt hα₀
        rwa [inv_mul_cancel₀ hα₀.ne'] at this
      linarith
  -- Final algebra from `q ≤ exp (M100 ^ 12 * L ^ 12)` to `#A₀ ≤ C * q / exp (...)`
  have hq_gt1 : (1 : ℝ) < q := by exact_mod_cast (by omega : 1 < q)
  have hlog_q_pos : 0 < log (q : ℝ) := log_pos hq_gt1
  have hlog_q_ub : log (q : ℝ) ≤ 2 * M100 ^ 12 * L ^ 12 := by
    have h1 : log (q : ℝ) ≤ M100 ^ 12 * L ^ 12 :=
      (log_le_iff_le_exp hq_pos).mpr hq_exp_bound
    have : 0 ≤ M100 ^ 12 * L ^ 12 := by positivity
    linarith [show 2 * M100 ^ 12 * L ^ 12 = 2 * (M100 ^ 12 * L ^ 12) by ring]
  have hrpow : log (q : ℝ) ^ (12⁻¹ : ℝ) ≤ (2 * M100 ^ 12) ^ (12⁻¹ : ℝ) * L := by
    calc
      log (q : ℝ) ^ (12⁻¹ : ℝ)
        ≤ (2 * M100 ^ 12 * L ^ 12) ^ (12⁻¹ : ℝ) :=
          rpow_le_rpow hlog_q_pos.le hlog_q_ub (by norm_num)
      _ = (2 * M100 ^ 12) ^ (12⁻¹ : ℝ) * (L ^ 12) ^ (12⁻¹ : ℝ) :=
          mul_rpow (by positivity) (by positivity)
      _ = (2 * M100 ^ 12) ^ (12⁻¹ : ℝ) * L := by
          rw [← rpow_natCast L 12, ← rpow_mul (by positivity)]
          norm_num
  have hc_log : c * log (q : ℝ) ^ (12⁻¹ : ℝ) ≤ 1 + log α⁻¹ := by
    rw [← hL_def]
    have hc_nn : 0 ≤ ((2 * M100 ^ 12) ^ (12⁻¹ : ℝ))⁻¹ := by positivity
    have hbase_ne : (2 * M100 ^ 12) ^ (12⁻¹ : ℝ) ≠ 0 := by positivity
    calc
      c * log (q : ℝ) ^ (12⁻¹ : ℝ)
        ≤ ((2 * M100 ^ 12) ^ (12⁻¹ : ℝ))⁻¹ * ((2 * M100 ^ 12) ^ (12⁻¹ : ℝ) * L) :=
          mul_le_mul_of_nonneg_left hrpow hc_nn
      _ = L := inv_mul_cancel_left₀ hbase_ne L
  have hexp_c : exp (c * log (q : ℝ) ^ (12⁻¹ : ℝ)) ≤ C * α⁻¹ := by
    have h1 := exp_le_exp.mpr hc_log
    rwa [exp_add, exp_log (inv_pos.mpr hα₀)] at h1
  rw [le_div_iff₀ (exp_pos _)]
  have hα_inv_eq : α⁻¹ = (q : ℝ) / #A₀ := by rw [hα_def, inv_div]
  have hA₀_pos : (0 : ℝ) < #A₀ := by exact_mod_cast hA₀_ne.card_pos
  rw [hα_inv_eq, mul_div_assoc', le_div_iff₀ hA₀_pos] at hexp_c
  linarith

end ZModPrime

end BohrIter
