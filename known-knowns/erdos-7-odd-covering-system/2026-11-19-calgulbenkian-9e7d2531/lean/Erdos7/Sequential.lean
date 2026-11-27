/-
Stage 4: sequential (coordinate-by-coordinate) weights, the iterated nested comparison, and the
abstract non-covering theorem.
-/
import Erdos7.Convex

namespace Erdos7
open Finset

/-- Prefix spaces: `Space X i = X 0 × ... × X (i-1)` (nested pairs, last coordinate outermost). -/
def Space (X : ℕ → Type) : ℕ → Type
  | 0 => Unit
  | i + 1 => Space X i × X i

section Ex
variable {X : ℕ → Type} [∀ m, Fintype (X m)]

/-- Expectation under the sequentially built weight with fibre kernels `κ`:
the law of coordinate `i` given the prefix `y` is `κ i y`. -/
def Ex (κ : ∀ i, Space X i → X i → ℚ) : ∀ i, (Space X i → ℚ) → ℚ
  | 0, F => F ()
  | i + 1, F => Ex κ i (fun y => ∑ x, κ i y x * F (y, x))

variable (κ : ∀ i, Space X i → X i → ℚ)

lemma Ex_mono (hκ0 : ∀ i y x, 0 ≤ κ i y x) : ∀ (i : ℕ) (F G : Space X i → ℚ),
    (∀ y, F y ≤ G y) → Ex κ i F ≤ Ex κ i G
  | 0, _, _, h => h ()
  | i + 1, _, _, h => Ex_mono hκ0 i _ _ fun y =>
      sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (h (y, x)) (hκ0 i y x)

lemma Ex_const (hκ1 : ∀ i y, ∑ x, κ i y x = 1) : ∀ (i : ℕ) (c : ℚ), Ex κ i (fun _ => c) = c
  | 0, c => rfl
  | i + 1, c => by
      simp only [Ex, ← sum_mul, hκ1, one_mul]; exact Ex_const hκ1 i c

lemma Ex_add : ∀ (i : ℕ) (F G : Space X i → ℚ),
    Ex κ i (fun y => F y + G y) = Ex κ i F + Ex κ i G
  | 0, F, G => rfl
  | i + 1, F, G => by
      simp only [Ex, mul_add, sum_add_distrib]; exact Ex_add i _ _

lemma Ex_mul_left : ∀ (i : ℕ) (c : ℚ) (F : Space X i → ℚ),
    Ex κ i (fun y => c * F y) = c * Ex κ i F
  | 0, c, F => rfl
  | i + 1, c, F => by
      have : ∀ y : Space X i, ∑ x, κ i y x * (c * F (y, x)) = c * ∑ x, κ i y x * F (y, x) := by
        intro y; rw [mul_sum]; exact sum_congr rfl fun x _ => by ring
      simp only [Ex, this]; exact Ex_mul_left i c _

lemma Ex_zero (i : ℕ) : Ex κ i (fun _ => 0) = 0 := by
  have := Ex_mul_left κ i 0 (fun _ => 0); simpa using this

lemma Ex_sum {β : Type*} (i : ℕ) (s : Finset β) (F : β → Space X i → ℚ) :
    Ex κ i (fun y => ∑ b ∈ s, F b y) = ∑ b ∈ s, Ex κ i (F b) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using Ex_zero κ i
  | insert a s ha ih =>
    simp only [sum_insert ha]; rw [Ex_add, ih]

end Ex

/-- Level vectors `T = (T_0, ..., T_{i-1})` with `T_m ∈ {0..e m}`. -/
abbrev TVec (e : ℕ → ℕ) : ℕ → Type := Space (fun m => Fin (e m + 1))

/-- Expectation over independent levels with point weights `q m t`. -/
def ET (e : ℕ → ℕ) (q : ℕ → ℕ → ℚ) (i : ℕ) (F : TVec e i → ℚ) : ℚ :=
  Ex (X := fun m => Fin (e m + 1)) (fun m _ t => q m t.val) i F

/-- Membership of a prefix in a box with the given sides. -/
def InBox {X : ℕ → Type} (side : ∀ m, Finset (X m)) : ∀ i, Space X i → Prop
  | 0, _ => True
  | i + 1, y => InBox side i y.1 ∧ y.2 ∈ side i

/-- The exponent vector `l` is below the level vector `T` on the first `i` coordinates. -/
def LeT {e : ℕ → ℕ} (l : ℕ → ℕ) : ∀ i, TVec e i → Prop
  | 0, _ => True
  | i + 1, T => LeT l i T.1 ∧ l i ≤ T.2.val

/-- `mult i T = prod_{m<i} (1 + T_m)`: the number of exponent vectors below `T`. -/
def mult {e : ℕ → ℕ} : ∀ i, TVec e i → ℕ
  | 0, _ => 1
  | i + 1, T => mult i T.1 * (1 + T.2.val)

lemma mult_pos {e : ℕ → ℕ} : ∀ (i : ℕ) (T : TVec e i), 0 < mult i T
  | 0, _ => Nat.one_pos
  | i + 1, T => Nat.mul_pos (mult_pos i T.1) (by omega)

section comparison
variable {X : ℕ → Type} [∀ m, Fintype (X m)] [∀ m, DecidableEq (X m)]

open Classical in
/-- **Iterated nested convex comparison** (Lemma 5 applied at coordinates `i-1, i-2, ..., 0`).
Real coordinates are replaced by independent nested levels, innermost first, so that every
application of Lemma 5 is to the original convex function composed with a nonnegative
affine map. -/
theorem comparison (κ : ∀ i, Space X i → X i → ℚ)
    (hκ0 : ∀ i y x, 0 ≤ κ i y x) (hκ1 : ∀ i y, ∑ x, κ i y x = 1)
    (e : ℕ → ℕ) (Q : ℕ → ℕ → ℚ) (hQ0 : ∀ m, Q m 0 = 1) (hQe : ∀ m, Q m (e m + 1) = 0)
    (hQanti : ∀ m t, t ≤ e m → Q m (t + 1) ≤ Q m t)
    (f : ℚ → ℚ) (hf : ConvexOn ℚ (Set.Ici 0) f) (hm : MonotoneOn f (Set.Ici 0))
    {ι : Type} (lev : ι → ℕ → ℕ) (side : ι → ∀ m, Finset (X m)) :
    ∀ (i : ℕ) (J : Finset ι) (w : ι → ℚ) (_hw : ∀ j ∈ J, 0 ≤ w j) (b : ℚ) (_hb : 0 ≤ b)
      (_hlev : ∀ j ∈ J, ∀ m, m < i → lev j m ≤ e m)
      (_hside : ∀ j ∈ J, ∀ m, m < i → ∀ y, ∑ x ∈ side j m, κ m y x ≤ Q m (lev j m)),
      Ex κ i (fun y => f (b + ∑ j ∈ J, if InBox (side j) i y then w j else 0)) ≤
        ET e (fun m t => Q m t - Q m (t + 1)) i
          (fun T => f (b + ∑ j ∈ J, if LeT (lev j) i T then w j else 0)) := by
  intro i
  induction i with
  | zero =>
    intro J w _ b _ _ _
    simp [Ex, ET, InBox, LeT]
  | succ i ih =>
    intro J w hw b hb hlev hside
    -- step 1: Lemma 5 on the last coordinate, for each fixed prefix
    have step1 : ∀ y : Space X i,
        ∑ x, κ i y x * f (b + ∑ j ∈ J, if InBox (side j) (i + 1) (y, x) then w j else 0) ≤
        ∑ t ∈ range (e i + 1), (Q i t - Q i (t + 1)) *
          f (b + ∑ j ∈ J, if InBox (side j) i y then (if lev j i ≤ t then w j else 0) else 0) := by
      intro y
      have h := nested_convex_comparison (κ i y) (hκ0 i y) (hκ1 i y) (e i) (Q i) (hQ0 i) (hQe i)
        f hf hm J (fun j => lev j i) (fun j hj => hlev j hj i (Nat.lt_succ_self i))
        (fun j => side j i) (fun j => if InBox (side j) i y then w j else 0)
        (fun j hj => by split_ifs <;> [exact hw j hj; exact le_rfl]) b hb
        (fun j hj => hside j hj i (Nat.lt_succ_self i) y)
      have e1 : ∀ x : X i, ∀ j, (if InBox (side j) (i + 1) (y, x) then w j else 0)
          = if x ∈ side j i then (if InBox (side j) i y then w j else 0) else 0 := by
        intro x j
        by_cases h1 : InBox (side j) i y <;> by_cases h2 : x ∈ side j i <;> simp [InBox, h1, h2]
      have e2 : ∀ t : ℕ, ∀ j, (if InBox (side j) i y then (if lev j i ≤ t then w j else 0) else 0)
          = if lev j i ≤ t then (if InBox (side j) i y then w j else 0) else 0 := by
        intro t j
        by_cases h1 : InBox (side j) i y <;> by_cases h2 : lev j i ≤ t <;> simp [h1, h2]
      simp only [e1, e2]
      exact h
    have hq0 : ∀ t ∈ range (e i + 1), 0 ≤ Q i t - Q i (t + 1) := fun t ht =>
      sub_nonneg.2 (hQanti i t (Nat.lt_succ_iff.1 (mem_range.1 ht)))
    calc Ex κ (i + 1) (fun y => f (b + ∑ j ∈ J, if InBox (side j) (i + 1) y then w j else 0))
        = Ex κ i (fun y => ∑ x, κ i y x *
            f (b + ∑ j ∈ J, if InBox (side j) (i + 1) (y, x) then w j else 0)) := rfl
      _ ≤ Ex κ i (fun y => ∑ t ∈ range (e i + 1), (Q i t - Q i (t + 1)) *
            f (b + ∑ j ∈ J, if InBox (side j) i y then (if lev j i ≤ t then w j else 0) else 0)) :=
          Ex_mono κ hκ0 i _ _ step1
      _ = ∑ t ∈ range (e i + 1), (Q i t - Q i (t + 1)) * Ex κ i (fun y =>
            f (b + ∑ j ∈ J, if InBox (side j) i y then (if lev j i ≤ t then w j else 0) else 0)) := by
          rw [Ex_sum]; exact sum_congr rfl fun t _ => Ex_mul_left κ i _ _
      _ ≤ ∑ t ∈ range (e i + 1), (Q i t - Q i (t + 1)) *
            ET e (fun m t => Q m t - Q m (t + 1)) i (fun T =>
              f (b + ∑ j ∈ J, if LeT (lev j) i T then (if lev j i ≤ t then w j else 0) else 0)) := by
          refine sum_le_sum fun t ht => mul_le_mul_of_nonneg_left ?_ (hq0 t ht)
          exact ih J (fun j => if lev j i ≤ t then w j else 0)
            (fun j hj => by split_ifs <;> [exact hw j hj; exact le_rfl]) b hb
            (fun j hj m hm' => hlev j hj m (Nat.lt_succ_of_lt hm'))
            (fun j hj m hm' => hside j hj m (Nat.lt_succ_of_lt hm'))
      _ = ET e (fun m t => Q m t - Q m (t + 1)) (i + 1)
            (fun T => f (b + ∑ j ∈ J, if LeT (lev j) (i + 1) T then w j else 0)) := by
          have hfin := Fin.sum_univ_eq_sum_range (fun t : ℕ => (Q i t - Q i (t + 1)) *
            ET e (fun m t => Q m t - Q m (t + 1)) i (fun T =>
              f (b + ∑ j ∈ J, if LeT (lev j) i T then (if lev j i ≤ t then w j else 0) else 0)))
            (e i + 1)
          rw [← hfin]
          simp only [ET, Ex]
          rw [Ex_sum]
          refine sum_congr rfl fun t _ => ?_
          rw [← Ex_mul_left]
          congr 1
          funext T
          have e3 : ∀ j, (if LeT (e := e) (lev j) (i + 1) (T, t) then w j else 0)
              = if LeT (lev j) i T then (if lev j i ≤ t.val then w j else 0) else 0 := by
            intro j
            by_cases h1 : LeT (lev j) i T <;> by_cases h2 : lev j i ≤ t.val <;>
              simp [LeT, h1, h2]
          simp only [e3]

end comparison

end Erdos7
