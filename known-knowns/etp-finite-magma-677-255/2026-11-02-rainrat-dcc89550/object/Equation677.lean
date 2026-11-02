import equational_theories.Equations.All
import equational_theories.ManuallyProved.Equation677
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Finite.Prod

/-!
# Equation 677 & Equation 2910: Conditional Implication Theorems and Separation Witnesses (`p2`)

Extends `equational_theories.ManuallyProved.Equation677` (Chapter 13 of the ETP blueprint)
for the open implication `Equation 677 → Equation 255` (and its dual `Equation 2910 → Equation 47`)
on finite magmas:

* Disjoint fixed-point sets of left translations (`eq677_leftMul_fixed_disjoint`)
* Fixed-point hypothesis implies E255 (`eq255_of_eq677_leftMul_has_fixed_point`)
* Right-cancellative / quasigroup implies E255 (`eq255_of_eq677_right_cancel`, `eq255_of_eq677_quasigroup`)
* Faithfulness of left regular representation (`eq677_leftMul_faithful`)
* Blueprint Lemma 13.3: uniform/linear left translations imply E255 (`eq255_of_eq677_uniform_leftMul`)
* Dual theorems for `Equation2910 → Equation47` (`eq47_of_eq2910_rightMul_has_fixed_point`,
  `eq47_of_eq2910_left_cancel`, `eq47_of_eq2910_quasigroup`)
* Formal separation witnesses (`Sep7` of order 7, `Sep25` of order 25, `Sep55` of order 55)
  proving by `decide` that `EveryLeftMulHasFixedPoint` is neither implied by nor equivalent to
  the translation-conjugacy closure condition (`LeftMulConjugacyClosed`) of ETP Issue #1517
  (nor implied by or equivalent to `RightCancellative`), and that `RightCancellative` /
  `IsQuasigroup` does not imply and is not equivalent to `LeftMulConjugacyClosed`.
-/

namespace Eq677

variable {G : Type*} [Magma G] [Finite G]

/-- A magma is right-cancellative if every right translation `R_x : y ↦ y ◇ x` is injective. -/
def RightCancellative (G : Type*) [Magma G] : Prop :=
  ∀ x : G, Function.Injective (fun y => y ◇ x)

/-- A magma is left-cancellative if every left translation `L_x : y ↦ x ◇ y` is injective. -/
def LeftCancellative (G : Type*) [Magma G] : Prop :=
  ∀ x : G, Function.Injective (fun y => x ◇ y)

/-- A magma is a quasigroup if all left and right translations are bijective. -/
def IsQuasigroup (G : Type*) [Magma G] : Prop :=
  (∀ x : G, Function.Bijective (fun y => x ◇ y)) ∧
  (∀ x : G, Function.Bijective (fun y => y ◇ x))

/-- Every left translation `L_y : x ↦ y ◇ x` has at least one fixed point. -/
def EveryLeftMulHasFixedPoint (G : Type*) [Magma G] : Prop :=
  ∀ y : G, ∃ x : G, y ◇ x = x

/-- Every right translation `R_y : x ↦ x ◇ y` has at least one fixed point. -/
def EveryRightMulHasFixedPoint (G : Type*) [Magma G] : Prop :=
  ∀ y : G, ∃ x : G, x ◇ y = x

/-- The translation-conjugacy closure hypothesis of ETP Issue #1517 / PR #1518:
for all `y₁, y₂`, the conjugate `L_{y₁}⁻¹ ∘ L_{y₂} ∘ L_{y₁}` is again a left translation `L_z`,
stated without inverses as `∀ x, y₂ ◇ (y₁ ◇ x) = y₁ ◇ (z ◇ x)`. -/
def LeftMulConjugacyClosed (G : Type*) [Magma G] : Prop :=
  ∀ y₁ y₂ : G, ∃ z : G, ∀ x : G, y₂ ◇ (y₁ ◇ x) = y₁ ◇ (z ◇ x)

/-- Uniform left-translation equality: if `L_a` and `L_b` agree at one point `x`,
they agree everywhere. Satisfied by all linear/affine magmas `x ◇ y = α x + β y + c`
(Blueprint Lemma 13.3). -/
def UniformLeftMul (G : Type*) [Magma G] : Prop :=
  ∀ a b x : G, a ◇ x = b ◇ x → ∀ z : G, a ◇ z = b ◇ z

/-- In any finite `Equation677` magma, the fixed-point sets `Fix(L_y) = {x | y ◇ x = x}`
of distinct left translations are pairwise disjoint. -/
theorem eq677_leftMul_fixed_disjoint (h : Equation677 G) {y₁ y₂ x : G}
    (h1 : y₁ ◇ x = x) (h2 : y₂ ◇ x = x) : y₁ = y₂ :=
  (eq677_fixer_unique h h1).trans (eq677_fixer_unique h h2).symm

/-- **Primary `p2` Conditional Implication Theorem**: If `G` is a finite `Equation677` magma
in which every left translation `L_y` has a fixed point (`EveryLeftMulHasFixedPoint G`), then
`Equation255 G` holds (and in fact every `L_y` has a unique fixed point). -/
theorem eq255_of_eq677_leftMul_has_fixed_point (h : Equation677 G)
    (hfp : EveryLeftMulHasFixedPoint G) : Equation255 G := by
  let f : G → G := fun y => Classical.choose (hfp y)
  have hf : ∀ y : G, y ◇ f y = f y := fun y => Classical.choose_spec (hfp y)
  have hinj : Function.Injective f := by
    intro y₁ y₂ heq
    have h1 : y₁ ◇ f y₁ = f y₁ := hf y₁
    have h2 : y₂ ◇ f y₁ = f y₁ := by rw [heq]; exact hf y₂
    exact eq677_leftMul_fixed_disjoint h h1 h2
  have hsurj : Function.Surjective f := (Finite.injective_iff_surjective).mp hinj
  intro x
  obtain ⟨y, rfl⟩ := hsurj x
  exact eq255_from_fixer_exists h (f y) ⟨y, hf y⟩

/-- **Conditional Implication Theorem 2**: Any finite right-cancellative `Equation677` magma
satisfies `Equation255`. -/
theorem eq255_of_eq677_right_cancel (h : Equation677 G)
    (hrc : RightCancellative G) : Equation255 G := by
  intro x
  have hsurj : Function.Surjective (fun y => y ◇ x) :=
    (Finite.injective_iff_surjective).mp (hrc x)
  exact eq255_from_fixer_exists h x (hsurj x)

/-- On a finite `Equation677` magma, being a quasigroup is equivalent to right-cancellativity. -/
theorem eq677_quasigroup_iff_right_cancel (h : Equation677 G) :
    IsQuasigroup G ↔ RightCancellative G := by
  constructor
  · rintro ⟨_, hR⟩ x
    exact (hR x).1
  · intro hrc
    refine ⟨fun y => ⟨eq677_leftMul_inj h y, eq677_leftMul_surj h y⟩, fun x => ⟨hrc x, ?_⟩⟩
    exact (Finite.injective_iff_surjective).mp (hrc x)

/-- **Conditional Implication Theorem 3**: Any finite `Equation677` quasigroup satisfies `Equation255`. -/
theorem eq255_of_eq677_quasigroup (h : Equation677 G)
    (hqg : IsQuasigroup G) : Equation255 G :=
  eq255_of_eq677_right_cancel h ((eq677_quasigroup_iff_right_cancel h).mp hqg)

/-- In every finite `Equation677` magma, the left-regular representation `y ↦ L_y` is faithful:
if `a ◇ z = b ◇ z` for all `z : G`, then `a = b`. -/
theorem eq677_leftMul_faithful (h : Equation677 G) {a b : G}
    (hab : ∀ z : G, a ◇ z = b ◇ z) : a = b := by
  have h1 : (a ◇ (a ◇ a)) ◇ a = (b ◇ (b ◇ a)) ◇ b := eq677_star_eq h a (hab a)
  have h_lhs : (a ◇ (a ◇ a)) ◇ a = (b ◇ (b ◇ a)) ◇ a := by
    rw [hab a, hab (b ◇ a)]
  exact eq677_left_cancel h (b ◇ (b ◇ a)) (h_lhs.symm.trans h1)

/-- Any finite `Equation677` magma with `UniformLeftMul` is right-cancellative. -/
theorem eq677_right_cancel_of_uniform_leftMul (h : Equation677 G)
    (hunif : UniformLeftMul G) : RightCancellative G := by
  intro x a b heq
  exact eq677_leftMul_faithful h (hunif a b x heq)

/-- **Blueprint Lemma 13.3**: Any finite `Equation677` magma with `UniformLeftMul`
(in particular, any linear/affine magma `x ◇ y = α x + β y + c`) satisfies `Equation255`. -/
theorem eq255_of_eq677_uniform_leftMul (h : Equation677 G)
    (hunif : UniformLeftMul G) : Equation255 G :=
  eq255_of_eq677_right_cancel h (eq677_right_cancel_of_uniform_leftMul h hunif)

end Eq677

/-!
## Dual Theorems for `Equation2910 → Equation47`
-/

namespace Eq2910

open Eq677

variable {G : Type*} [Magma G]

/-- Right multiplication is surjective in any `Equation2910` magma. -/
theorem eq2910_rightMul_surj (h : Equation2910 G) (y : G) :
    Function.Surjective (fun x => x ◇ y) :=
  fun x => ⟨(y ◇ (x ◇ y)) ◇ x, (h x y).symm⟩

/-- The right-inverse formula for `Equation2910`: `((y ◇ (x ◇ y)) ◇ x) ◇ y = x`. -/
theorem eq2910_rightInv_formula (h : Equation2910 G) (x y : G) :
    ((y ◇ (x ◇ y)) ◇ x) ◇ y = x :=
  (h x y).symm

variable [Finite G]

/-- Right multiplication is injective on finite `Equation2910` magmas. -/
theorem eq2910_rightMul_inj (h : Equation2910 G) (y : G) :
    Function.Injective (fun x => x ◇ y) :=
  (Finite.injective_iff_surjective).mpr (eq2910_rightMul_surj h y)

/-- Right cancellation in finite `Equation2910` magmas: `a ◇ y = b ◇ y → a = b`. -/
theorem eq2910_right_cancel (h : Equation2910 G) (y : G) {a b : G}
    (hab : a ◇ y = b ◇ y) : a = b :=
  eq2910_rightMul_inj h y hab

/-- Fixer uniqueness for `Equation2910`: if `x ◇ y = x` then `y = x ◇ (x ◇ x)`. -/
theorem eq2910_fixer_unique (h : Equation2910 G) {x y : G}
    (hfix : x ◇ y = x) : y = x ◇ (x ◇ x) := by
  have hinv : ((y ◇ x) ◇ x) ◇ y = x := by
    have := eq2910_rightInv_formula h x y; rwa [hfix] at this
  have hxy : x = (y ◇ x) ◇ x := eq2910_right_cancel h y (by rw [hfix, hinv])
  exact eq2910_right_cancel h x (eq2910_right_cancel h x (hxy.symm.trans (h x x)))

/-- `Equation47` holds at `x` whenever `x` is fixed by some right multiplication `R_y`. -/
theorem eq47_from_fixer_exists (h : Equation2910 G) (x : G)
    (hfix : ∃ y : G, x ◇ y = x) : x = x ◇ (x ◇ (x ◇ x)) := by
  obtain ⟨y, hy⟩ := hfix
  rw [← eq2910_fixer_unique h hy]; exact hy.symm

/-- In any finite `Equation2910` magma, fixed-point sets `Fix(R_y) = {x | x ◇ y = x}`
of distinct right translations are pairwise disjoint. -/
theorem eq2910_rightMul_fixed_disjoint (h : Equation2910 G) {y₁ y₂ x : G}
    (h1 : x ◇ y₁ = x) (h2 : x ◇ y₂ = x) : y₁ = y₂ :=
  (eq2910_fixer_unique h h1).trans (eq2910_fixer_unique h h2).symm

/-- **Dual Conditional Implication Theorem 1**: If `G` is a finite `Equation2910` magma in which
every right translation `R_y` has a fixed point (`EveryRightMulHasFixedPoint G`), then
`Equation47 G` holds. -/
theorem eq47_of_eq2910_rightMul_has_fixed_point (h : Equation2910 G)
    (hfp : EveryRightMulHasFixedPoint G) : Equation47 G := by
  let f : G → G := fun y => Classical.choose (hfp y)
  have hf : ∀ y : G, f y ◇ y = f y := fun y => Classical.choose_spec (hfp y)
  have hinj : Function.Injective f := by
    intro y₁ y₂ heq
    have h1 : f y₁ ◇ y₁ = f y₁ := hf y₁
    have h2 : f y₁ ◇ y₂ = f y₁ := by rw [heq]; exact hf y₂
    exact eq2910_rightMul_fixed_disjoint h h1 h2
  have hsurj : Function.Surjective f := (Finite.injective_iff_surjective).mp hinj
  intro x
  obtain ⟨y, rfl⟩ := hsurj x
  exact eq47_from_fixer_exists h (f y) ⟨y, hf y⟩

/-- **Dual Conditional Implication Theorem 2**: Any finite left-cancellative `Equation2910`
magma satisfies `Equation47`. -/
theorem eq47_of_eq2910_left_cancel (h : Equation2910 G)
    (hlc : LeftCancellative G) : Equation47 G := by
  intro x
  have hsurj : Function.Surjective (fun y => x ◇ y) :=
    (Finite.injective_iff_surjective).mp (hlc x)
  exact eq47_from_fixer_exists h x (hsurj x)

/-- **Dual Conditional Implication Theorem 3**: Any finite `Equation2910` quasigroup
satisfies `Equation47`. -/
theorem eq47_of_eq2910_quasigroup (h : Equation2910 G)
    (hqg : IsQuasigroup G) : Equation47 G :=
  eq47_of_eq2910_left_cancel h (fun x => (hqg.1 x).1)

end Eq2910

/-!
## Formal Separation and Logical Independence Witnesses (`Sep7`, `Sep25`, `Sep55`)

We construct three explicit finite `Equation677` magmas and verify their properties by `decide`:
1. `Sep7` (order 7, linear model `x ◇ y = (4x + y) mod 7`):
   satisfies `Equation677`, `Equation255`, `RightCancellative`, and `LeftMulConjugacyClosed`
   (Issue #1517), but **violates** `EveryLeftMulHasFixedPoint`.
2. `Sep25` (order 25, diagonal-split `5 × 5` bundle of two isomorphic order-5 `Equation677`
   quasigroups): satisfies `Equation677`, `Equation255`, `RightCancellative` (it is a quasigroup),
   and `EveryLeftMulHasFixedPoint`, but **violates** `LeftMulConjugacyClosed` (Issue #1517).
3. `Sep55` (order 55, quadratic-residue twisted `11 × 5` fiber bundle over `F_11 × F_5`):
   satisfies `Equation677`, `Equation255`, and `EveryLeftMulHasFixedPoint`, but **violates**
   both `RightCancellative` and `LeftMulConjugacyClosed` (Issue #1517).
-/

namespace Eq677.Separation

open Eq677

/-- Witness 1 (`Sep7`): Order-7 magma `Fin 7` with `x ◇ y = (4x + y) mod 7`. -/
abbrev Sep7 := Fin 7

instance : Magma Sep7 where
  op x y := ⟨(4 * x.val + y.val) % 7, Nat.mod_lt _ (by decide)⟩

theorem sep7_eq677 : Equation677 Sep7 := by decide

theorem sep7_eq255 : Equation255 Sep7 := by decide

theorem sep7_rightCancel : RightCancellative Sep7 := by
  unfold RightCancellative Function.Injective; decide

theorem sep7_conjClosed : LeftMulConjugacyClosed Sep7 := by
  unfold LeftMulConjugacyClosed; decide

theorem sep7_not_leftMulHasFixedPoint : ¬ EveryLeftMulHasFixedPoint Sep7 := by
  unfold EveryLeftMulHasFixedPoint; decide

/-- `EveryLeftMulHasFixedPoint` is not implied by `LeftMulConjugacyClosed`, `RightCancellative`,
or `Equation255` on finite `Equation677` magmas. -/
theorem not_leftMulHasFixedPoint_of_conjClosed :
    ∃ (G : Type) (_ : Magma G) (_ : Finite G),
      Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧
      LeftMulConjugacyClosed G ∧ ¬ EveryLeftMulHasFixedPoint G :=
  ⟨Sep7, inferInstance, Finite.of_fintype Sep7,
    sep7_eq677, sep7_eq255, sep7_rightCancel, sep7_conjClosed, sep7_not_leftMulHasFixedPoint⟩

/-- Helper transposition swapping `0` and `1` on `0..4`. -/
def swap01 (k : Nat) : Nat :=
  if k == 0 then 1 else if k == 1 then 0 else k

/-- Base order-5 `Equation677` operation `(2s + 4t) mod 5`. -/
def op5A (s t : Nat) : Nat :=
  (2 * s + 4 * t) % 5

/-- Conjugate order-5 `Equation677` operation via `swap01`. -/
def op5B (s t : Nat) : Nat :=
  swap01 (op5A (swap01 s) (swap01 t))

/-- Witness 2 (`Sep25`): Order-25 magma `Fin 25` (`5 × 5` diagonal-split quasigroup). -/
def op25Nat (u v : Nat) : Nat :=
  let x1 := u / 5
  let s1 := u % 5
  let x2 := v / 5
  let s2 := v % 5
  let x3 := op5A x1 x2
  let s3 := if x1 == x2 then op5A s1 s2 else op5B s1 s2
  (5 * x3 + s3) % 25

theorem op25Nat_lt (u v : Nat) : op25Nat u v < 25 :=
  Nat.mod_lt _ (by decide)

abbrev Sep25 := Fin 25

instance : Magma Sep25 where
  op u v := ⟨op25Nat u.val v.val, op25Nat_lt u.val v.val⟩

theorem sep25_eq677 : Equation677 Sep25 := by decide

theorem sep25_eq255 : Equation255 Sep25 := by decide

theorem sep25_rightCancel : RightCancellative Sep25 := by
  unfold RightCancellative Function.Injective; decide

theorem sep25_leftMulHasFixedPoint : EveryLeftMulHasFixedPoint Sep25 := by
  unfold EveryLeftMulHasFixedPoint; decide

theorem sep25_not_conjClosed_witness :
    ∀ z : Sep25, ¬ (∀ x : Sep25, (1 : Sep25) ◇ ((0 : Sep25) ◇ x) = (0 : Sep25) ◇ (z ◇ x)) := by
  decide

theorem sep25_not_conjClosed : ¬ LeftMulConjugacyClosed Sep25 := by
  intro hcc
  obtain ⟨z, hz⟩ := hcc 0 1
  exact sep25_not_conjClosed_witness z hz

/-- Neither `RightCancellative` (being a quasigroup) nor `EveryLeftMulHasFixedPoint`
implies `LeftMulConjugacyClosed` (Issue #1517) on finite `Equation677` magmas. -/
theorem not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint :
    ∃ (G : Type) (_ : Magma G) (_ : Finite G),
      Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧
      EveryLeftMulHasFixedPoint G ∧ ¬ LeftMulConjugacyClosed G :=
  ⟨Sep25, inferInstance, Finite.of_fintype Sep25,
    sep25_eq677, sep25_eq255, sep25_rightCancel, sep25_leftMulHasFixedPoint, sep25_not_conjClosed⟩

/-- Quadratic residues modulo 11: `{1, 3, 4, 5, 9}`. -/
def isQR11 (d : Nat) : Bool :=
  d == 1 || d == 3 || d == 4 || d == 5 || d == 9

/-- Witness 3 (`Sep55`): Order-55 magma `Fin 55` (`11 × 5` quadratic-residue twisted bundle). -/
def op55Nat (u v : Nat) : Nat :=
  let x1 := u / 5
  let s1 := u % 5
  let x2 := v / 5
  let s2 := v % 5
  let x3 := (10 * x1 + 2 * x2) % 11
  let d := (x2 + 11 - x1 % 11) % 11
  let s3 :=
    if d == 0 then (2 * s1 + 4 * s2) % 5
    else if isQR11 d then s2
    else (4 * s1 + 4 * s2) % 5
  (5 * x3 + s3) % 55

theorem op55Nat_lt (u v : Nat) : op55Nat u v < 55 :=
  Nat.mod_lt _ (by decide)

abbrev Sep55 := Fin 55

instance : Magma Sep55 where
  op u v := ⟨op55Nat u.val v.val, op55Nat_lt u.val v.val⟩

theorem sep55_eq677 : Equation677 Sep55 := by decide

theorem sep55_eq255 : Equation255 Sep55 := by decide

theorem sep55_idempotent : ∀ y : Sep55, y ◇ y = y := by decide

theorem sep55_leftMulHasFixedPoint : EveryLeftMulHasFixedPoint Sep55 :=
  fun y => ⟨y, sep55_idempotent y⟩

theorem sep55_not_rightCancel : ¬ RightCancellative Sep55 := by
  intro hrc
  have heq : (10 : Sep55) ◇ (0 : Sep55) = (11 : Sep55) ◇ (0 : Sep55) := by decide
  have h10_11 : (10 : Sep55) = (11 : Sep55) := hrc 0 heq
  revert h10_11
  decide

theorem sep55_not_conjClosed_witness :
    ∀ z : Sep55, ¬ (∀ x : Sep55, (1 : Sep55) ◇ ((0 : Sep55) ◇ x) = (0 : Sep55) ◇ (z ◇ x)) := by
  decide

theorem sep55_not_conjClosed : ¬ LeftMulConjugacyClosed Sep55 := by
  intro hcc
  obtain ⟨z, hz⟩ := hcc 0 1
  exact sep55_not_conjClosed_witness z hz

/-- `EveryLeftMulHasFixedPoint` holds on finite `Equation677` magmas that satisfy neither
`RightCancellative` nor `LeftMulConjugacyClosed` (Issue #1517). -/
theorem not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint :
    ∃ (G : Type) (_ : Magma G) (_ : Finite G),
      Equation677 G ∧ Equation255 G ∧ EveryLeftMulHasFixedPoint G ∧
      ¬ RightCancellative G ∧ ¬ LeftMulConjugacyClosed G :=
  ⟨Sep55, inferInstance, Finite.of_fintype Sep55,
    sep55_eq677, sep55_eq255, sep55_leftMulHasFixedPoint,
    sep55_not_rightCancel, sep55_not_conjClosed⟩

end Eq677.Separation

#print axioms Eq677.eq677_leftMul_fixed_disjoint
#print axioms Eq677.eq255_of_eq677_leftMul_has_fixed_point
#print axioms Eq677.eq255_of_eq677_right_cancel
#print axioms Eq677.eq255_of_eq677_quasigroup
#print axioms Eq677.eq677_leftMul_faithful
#print axioms Eq677.eq255_of_eq677_uniform_leftMul
#print axioms Eq2910.eq47_of_eq2910_rightMul_has_fixed_point
#print axioms Eq2910.eq47_of_eq2910_left_cancel
#print axioms Eq2910.eq47_of_eq2910_quasigroup
#print axioms Eq677.Separation.not_leftMulHasFixedPoint_of_conjClosed
#print axioms Eq677.Separation.not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint
#print axioms Eq677.Separation.not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint
