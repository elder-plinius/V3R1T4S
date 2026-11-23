module

public import Mathlib.Analysis.SpecialFunctions.Pow.Real
public import Mathlib.Combinatorics.Additive.AP.Three.Defs

import APAP.BohrIter
import Mathlib.Data.ZMod.Basic
import Mathlib.NumberTheory.Bertrand

open Finset Real

/-- Freiman-isomorphic Bertrand reduction: any bound `(#B : ℝ) ≤ C * p / exp (c * log p ^ e)` for
3AP-free subsets `B ⊆ ZMod p` (`p ≥ 3` prime) implies the integer bound
`(#A : ℝ) ≤ max 1 (4 * C) * N / exp (c * log N ^ e)` for all `A ⊆ range N`, `ThreeAPFree A`. -/
private lemma int_bound_of_zmod_prime {e : ℝ} (he : 0 < e)
    (hzmod : ∃ c > 0, ∃ C > 0, ∀ (p : ℕ) [Fact p.Prime], 3 ≤ p →
      ∀ (B : Finset (ZMod p)), ThreeAPFree (α := ZMod p) B →
        (#B : ℝ) ≤ C * p / exp (c * log p ^ e)) :
    ∃ c > 0, ∃ C > 0, ∀ ⦃A : Finset ℕ⦄ ⦃N : ℕ⦄, A ⊆ range N → ThreeAPFree (α := ℕ) A →
      (#A : ℝ) ≤ C * N / exp (c * log N ^ e) := by
  obtain ⟨c, hc, C, hC, hzp⟩ := hzmod
  refine ⟨c, hc, max 1 (4 * C), by positivity, fun A N hAN hA3 ↦ ?_⟩
  rcases eq_or_ne N 0 with rfl | hN0
  · simp only [range_zero, subset_empty] at hAN
    subst hAN
    simp
  rcases eq_or_ne N 1 with rfl | hN1
  · have hcard : #A ≤ 1 := (card_le_card hAN).trans (by simp)
    have hlog1 : log (1 : ℝ) = 0 := log_one
    simp only [Nat.cast_one, hlog1, zero_rpow he.ne', mul_zero, exp_zero, div_one, mul_one]
    have hcard1 : (#A : ℝ) ≤ 1 := by exact_mod_cast hcard
    exact hcard1.trans (le_max_left 1 (4 * C))
  obtain ⟨p, hp_prime, hp_gt, hp_le⟩ :=
    Nat.exists_prime_lt_and_le_two_mul (2 * N) (by omega)
  have : Fact p.Prime := ⟨hp_prime⟩
  have hp3 : 3 ≤ p := by omega
  let φ : ℕ → ZMod p := fun n ↦ (n : ZMod p)
  have hinj : Set.InjOn φ (A : Set ℕ) := by
    intro x hx y hy hxy
    have hxN : x < N := mem_range.mp (hAN hx)
    have hyN : y < N := mem_range.mp (hAN hy)
    have hxp : x < p := by omega
    have hyp : y < p := by omega
    have hval := congr_arg ZMod.val hxy
    simpa [φ, ZMod.val_natCast, Nat.mod_eq_of_lt hxp, Nat.mod_eq_of_lt hyp] using hval
  let B : Finset (ZMod p) := A.image φ
  have hB_card : #B = #A := card_image_of_injOn hinj
  have hB_3ap : ThreeAPFree (α := ZMod p) B := by
    intro b₁ hb₁ b₂ hb₂ b₃ hb₃ heq
    obtain ⟨a₁, ha₁, rfl⟩ := mem_image.mp hb₁
    obtain ⟨a₂, ha₂, rfl⟩ := mem_image.mp hb₂
    obtain ⟨a₃, ha₃, rfl⟩ := mem_image.mp hb₃
    have h1N : a₁ < N := mem_range.mp (hAN ha₁)
    have h2N : a₂ < N := mem_range.mp (hAN ha₂)
    have h3N : a₃ < N := mem_range.mp (hAN ha₃)
    have hcast : ((a₁ + a₃ : ℕ) : ZMod p) = ((a₂ + a₂ : ℕ) : ZMod p) := by
      dsimp only [φ] at heq
      rwa [← Nat.cast_add, ← Nat.cast_add] at heq
    have h13_lt : a₁ + a₃ < p := by omega
    have h22_lt : a₂ + a₂ < p := by omega
    have hnat : a₁ + a₃ = a₂ + a₂ := by
      have hv := congr_arg ZMod.val hcast
      rw [ZMod.val_natCast, ZMod.val_natCast, Nat.mod_eq_of_lt h13_lt,
        Nat.mod_eq_of_lt h22_lt] at hv
      exact hv
    have ha_eq : a₁ = a₂ := hA3 ha₁ ha₂ ha₃ hnat
    rw [ha_eq]
  have hbound := hzp p hp3 B hB_3ap
  rw [hB_card] at hbound
  have hN_ge2 : (2 : ℝ) ≤ N := by
    have : 2 ≤ N := by omega
    exact_mod_cast this
  have hp_ge_N : (N : ℝ) ≤ p := by
    have : N ≤ p := by omega
    exact_mod_cast this
  have hp_le_4N : (p : ℝ) ≤ 4 * N := by
    have : p ≤ 4 * N := by omega
    exact_mod_cast this
  have hlog_le : log N ^ e ≤ log p ^ e := by
    refine rpow_le_rpow (log_nonneg (by linarith)) ?_ he.le
    exact log_le_log (by positivity) hp_ge_N
  have hexp_le : exp (c * log N ^ e) ≤ exp (c * log p ^ e) :=
    exp_le_exp.mpr (mul_le_mul_of_nonneg_left hlog_le hc.le)
  calc
    (#A : ℝ) ≤ C * p / exp (c * log p ^ e) := hbound
    _ ≤ C * (4 * N) / exp (c * log N ^ e) := by
      refine div_le_div₀ (by positivity) ?_ (exp_pos _) hexp_le
      nlinarith
    _ = (4 * C) * N / exp (c * log N ^ e) := by ring
    _ ≤ max 1 (4 * C) * N / exp (c * log N ^ e) := by
      gcongr
      exact le_max_right 1 (4 * C)

public section

theorem int :
    ∃ c > 0, ∃ C > 0, ∀ ⦃A : Finset ℕ⦄ ⦃N : ℕ⦄, A ⊆ range N → ThreeAPFree (α := ℕ) A →
      (#A : ℝ) ≤ C * N / exp (c * log N ^ (12⁻¹ : ℝ)) :=
  int_bound_of_zmod_prime (by norm_num) BohrIter.zmod_prime_threeAPFree
