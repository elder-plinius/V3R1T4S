/-
Stage 4, Lemma 5: the one-dimensional nested convex comparison.
-/
import Mathlib

namespace Erdos7
open Finset

variable {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]

/-- Increments of a convex function are larger at larger base points and proportional to length. -/
lemma convex_increment_le {f : 𝕜 → 𝕜} (hf : ConvexOn 𝕜 (Set.Ici 0) f)
    {u S a W : 𝕜} (hu : 0 ≤ u) (huS : u ≤ S) (ha : 0 ≤ a) (haW : a ≤ W) (hW : 0 < W) :
    f (u + a) - f u ≤ a / W * (f (S + W) - f S) := by
  rcases ha.eq_or_lt with rfl | ha'
  · simp
  have hS : (0:𝕜) ≤ S := hu.trans huS
  have h1 := hf.secant_mono (a := u) (x := u + a) (y := S + W) (Set.mem_Ici.2 hu)
    (Set.mem_Ici.2 (by positivity)) (Set.mem_Ici.2 (by positivity)) (by linarith) (by linarith)
    (by linarith)
  have h2 := hf.secant_mono (a := S + W) (x := u) (y := S) (Set.mem_Ici.2 (by positivity))
    (Set.mem_Ici.2 hu) (Set.mem_Ici.2 hS) (by linarith) (by linarith) huS
  have e1 : u + a - u = a := by ring
  have e2 : (f u - f (S + W)) / (u - (S + W)) = (f (S + W) - f u) / (S + W - u) := by
    rw [← neg_div_neg_eq]; congr 1 <;> ring
  have e3 : (f S - f (S + W)) / (S - (S + W)) = (f (S + W) - f S) / W := by
    rw [← neg_div_neg_eq]; congr 1 <;> ring
  rw [e1] at h1
  rw [e2, e3] at h2
  have h3 := h1.trans h2
  rw [div_le_iff₀ ha'] at h3
  calc f (u + a) - f u ≤ (f (S + W) - f S) / W * a := h3
    _ = a / W * (f (S + W) - f S) := by ring

/-- Abel summation in the form used below. -/
lemma abel_sum (Q g : ℕ → 𝕜) (n : ℕ) :
    ∑ t ∈ range n, (Q t - Q (t + 1)) * g (t + 1)
      = Q 0 * g 0 - Q n * g n + ∑ t ∈ range n, Q t * (g (t + 1) - g t) := by
  induction n with
  | zero => simp
  | succ n ih => rw [sum_range_succ, sum_range_succ, ih]; ring

/-- **Lemma 5 (1-D nested convex comparison).**
`κ` is a probability weight on a finite set, `A j` are events with levels `l j ∈ {0..e}` and
`κ (A j) ≤ Q (l j)`, where `Q 0 = 1`, `Q (e+1) = 0`.  The right-hand side is the expectation over
a level `T ∈ {0..e}` with `P(T ≥ t) = Q t` of the same expression with the *nested* events
`{l j ≤ T}`.  `f` is convex and increasing on `[0, ∞)`, the weights are nonnegative. -/
theorem nested_convex_comparison {α : Type*} [Fintype α] [DecidableEq α]
    (κ : α → 𝕜) (hκ0 : ∀ x, 0 ≤ κ x) (hκ1 : ∑ x, κ x = 1)
    (e : ℕ) (Q : ℕ → 𝕜) (hQ0 : Q 0 = 1) (hQe : Q (e + 1) = 0)
    (f : 𝕜 → 𝕜) (hf : ConvexOn 𝕜 (Set.Ici 0) f) (hm : MonotoneOn f (Set.Ici 0))
    {ι : Type*} (J : Finset ι) (l : ι → ℕ) (hl : ∀ j ∈ J, l j ≤ e)
    (A : ι → Finset α) (w : ι → 𝕜) (hw : ∀ j ∈ J, 0 ≤ w j) (b : 𝕜) (hb : 0 ≤ b)
    (hA : ∀ j ∈ J, ∑ x ∈ A j, κ x ≤ Q (l j)) :
    ∑ x, κ x * f (b + ∑ j ∈ J, if x ∈ A j then w j else 0) ≤
      ∑ t ∈ range (e + 1), (Q t - Q (t + 1)) * f (b + ∑ j ∈ J, if l j ≤ t then w j else 0) := by
  classical
  -- level sums
  set Wl : ℕ → 𝕜 := fun t => ∑ j ∈ J, if l j = t then w j else 0 with hWl
  set Sx : ℕ → 𝕜 := fun T => b + ∑ j ∈ J, if l j < T then w j else 0 with hSx
  have hWl0 : ∀ t, 0 ≤ Wl t := fun t =>
    sum_nonneg fun j hj => by split_ifs <;> [exact hw j hj; exact le_rfl]
  have hSx_succ : ∀ t, Sx (t + 1) = Sx t + Wl t := by
    intro t
    simp only [hSx, hWl, add_assoc, ← sum_add_distrib]
    congr 1
    refine sum_congr rfl fun j _ => ?_
    rcases lt_trichotomy (l j) t with h | h | h
    · simp [h, Nat.lt_succ_of_lt h, h.ne]
    · simp [h]
    · have : ¬ l j < t + 1 := by omega
      simp [this, h.not_gt, h.ne']
  have hSx0 : Sx 0 = b := by simp [hSx]
  have hSx_nonneg : ∀ t, 0 ≤ Sx t := by
    intro t
    induction t with
    | zero => rw [hSx0]; exact hb
    | succ t ih => rw [hSx_succ]; exact add_nonneg ih (hWl0 t)
  have hSx_le : ∀ t, Sx t ≤ Sx (t + 1) := fun t => by rw [hSx_succ]; linarith [hWl0 t]
  have hSx_eq : ∀ T, Sx T = b + ∑ t ∈ range T, Wl t := by
    intro T
    induction T with
    | zero => simp [hSx0]
    | succ T ih => rw [hSx_succ, ih, sum_range_succ]; ring
  set D : ℕ → 𝕜 := fun t => f (Sx (t + 1)) - f (Sx t) with hD
  have hD0 : ∀ t, 0 ≤ D t := fun t =>
    sub_nonneg.2 (hm (Set.mem_Ici.2 (hSx_nonneg t)) (Set.mem_Ici.2 (hSx_nonneg _)) (hSx_le t))
  set sl : ℕ → 𝕜 := fun t => D t / Wl t with hsl
  have hsl0 : ∀ t, 0 ≤ sl t := fun t => div_nonneg (hD0 t) (hWl0 t)
  have hWsl : ∀ t, Wl t * sl t = D t := by
    intro t
    by_cases h : Wl t = 0
    · have : Sx (t + 1) = Sx t := by rw [hSx_succ, h, add_zero]
      simp [hsl, hD, h, this]
    · simp only [hsl]; field_simp
  -- pointwise linear upper bound
  have hpt : ∀ x : α, f (b + ∑ j ∈ J, if x ∈ A j then w j else 0) ≤
      f b + ∑ j ∈ J, if x ∈ A j then w j * sl (l j) else 0 := by
    intro x
    set ax : ℕ → 𝕜 := fun t => ∑ j ∈ J, if l j = t ∧ x ∈ A j then w j else 0 with hax
    have hax0 : ∀ t, 0 ≤ ax t := fun t =>
      sum_nonneg fun j hj => by split_ifs <;> [exact hw j hj; exact le_rfl]
    have haxW : ∀ t, ax t ≤ Wl t := fun t => sum_le_sum fun j hj => by
      by_cases h1 : l j = t <;> by_cases h2 : x ∈ A j <;> simp [h1, h2, hw j hj]
    have key : ∀ T, f (b + ∑ t ∈ range T, ax t) ≤ f b + ∑ t ∈ range T, ax t * sl t := by
      intro T
      induction T with
      | zero => simp
      | succ T ih =>
        rw [sum_range_succ, sum_range_succ, ← add_assoc, ← add_assoc]
        have hu0 : 0 ≤ b + ∑ t ∈ range T, ax t := add_nonneg hb (sum_nonneg fun t _ => hax0 t)
        have huS : b + ∑ t ∈ range T, ax t ≤ Sx T := by
          rw [hSx_eq]; gcongr with t _; exact haxW t
        rcases (hWl0 T).eq_or_lt with h0 | hpos
        · have : ax T = 0 := le_antisymm (h0 ▸ haxW T) (hax0 T)
          simp [this, ih]
        · have := convex_increment_le hf hu0 huS (hax0 T) (haxW T) hpos
          rw [← hSx_succ] at this
          have e : ax T / Wl T * (f (Sx (T + 1)) - f (Sx T)) = ax T * sl T := by
            simp only [hsl, hD]; ring
          rw [e] at this
          linarith
    have h1 : ∑ t ∈ range (e + 1), ax t = ∑ j ∈ J, if x ∈ A j then w j else 0 := by
      simp only [hax]
      rw [sum_comm]
      refine sum_congr rfl fun j hj => ?_
      have hle := hl j hj
      by_cases h2 : x ∈ A j
      · simp only [h2, and_true, ite_true]
        rw [sum_ite_eq]; simp [Nat.lt_succ_of_le hle]
      · simp [h2]
    have h2 : ∑ t ∈ range (e + 1), ax t * sl t
        = ∑ j ∈ J, if x ∈ A j then w j * sl (l j) else 0 := by
      simp only [hax, sum_mul]
      rw [sum_comm]
      refine sum_congr rfl fun j hj => ?_
      have hle := hl j hj
      by_cases h2 : x ∈ A j
      · simp only [h2, and_true, ite_true]
        have : ∀ t ∈ range (e + 1), (if l j = t then w j else 0) * sl t
            = if l j = t then w j * sl (l j) else 0 := by
          intro t _; by_cases h : l j = t <;> simp [h]
        rw [sum_congr rfl this, sum_ite_eq]; simp [Nat.lt_succ_of_le hle]
      · simp [h2]
    have := key (e + 1)
    rwa [h1, h2] at this
  -- left side
  have hL : ∑ x, κ x * f (b + ∑ j ∈ J, if x ∈ A j then w j else 0)
      ≤ f b + ∑ j ∈ J, w j * sl (l j) * Q (l j) := by
    calc ∑ x, κ x * f (b + ∑ j ∈ J, if x ∈ A j then w j else 0)
        ≤ ∑ x, κ x * (f b + ∑ j ∈ J, if x ∈ A j then w j * sl (l j) else 0) :=
          sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (hpt x) (hκ0 x)
      _ = f b + ∑ j ∈ J, w j * sl (l j) * ∑ x ∈ A j, κ x := by
          simp only [mul_add, sum_add_distrib, ← sum_mul, hκ1, one_mul, mul_sum]
          congr 1
          rw [sum_comm]
          refine sum_congr rfl fun j _ => ?_
          rw [← sum_filter_add_sum_filter_not univ (fun x => x ∈ A j)]
          have : ∑ x ∈ univ.filter (fun x => ¬ x ∈ A j),
              κ x * (if x ∈ A j then w j * sl (l j) else 0) = 0 :=
            sum_eq_zero fun x hx => by simp [(mem_filter.1 hx).2]
          rw [this, add_zero]
          have hfil : univ.filter (fun x => x ∈ A j) = A j := by ext; simp
          rw [hfil]
          refine sum_congr rfl fun x hx => ?_
          simp [hx, mul_comm]
      _ ≤ f b + ∑ j ∈ J, w j * sl (l j) * Q (l j) := by
          gcongr with j hj
          · exact mul_nonneg (hw j hj) (hsl0 _)
          · exact hA j hj
  have hL2 : ∑ j ∈ J, w j * sl (l j) * Q (l j) = ∑ t ∈ range (e + 1), Q t * D t := by
    have : ∀ t ∈ range (e + 1), Q t * D t
        = ∑ j ∈ J, if l j = t then w j * sl (l j) * Q (l j) else 0 := by
      intro t _
      rw [← hWsl t, hWl, sum_mul, mul_sum]
      refine sum_congr rfl fun j _ => ?_
      by_cases h : l j = t
      · simp [h]; ring
      · simp [h]
    rw [sum_congr rfl this, sum_comm]
    refine sum_congr rfl fun j hj => ?_
    rw [sum_ite_eq]; simp [Nat.lt_succ_of_le (hl j hj)]
  -- right side
  have hR : ∑ t ∈ range (e + 1), (Q t - Q (t + 1)) * f (b + ∑ j ∈ J, if l j ≤ t then w j else 0)
      = f b + ∑ t ∈ range (e + 1), Q t * D t := by
    have : ∀ t, b + ∑ j ∈ J, (if l j ≤ t then w j else 0) = Sx (t + 1) := by
      intro t; simp only [hSx, Nat.lt_succ_iff]
    simp only [this]
    rw [abel_sum Q (fun t => f (Sx t)) (e + 1), hQ0, hQe, hSx0]
    simp [hD]
  rw [hR, ← hL2]
  exact hL

end Erdos7
