/-
Stage 1: the statement.  Everything a human needs to audit is in this file.
-/
import Mathlib.Algebra.GCDMonoid.Finset
import Mathlib.Algebra.GCDMonoid.Nat
import Mathlib.Algebra.Ring.Parity

namespace Erdos7

/-- A finite system of congruences is a finite set of pairs `(a, n)`;
the pair `(a, n)` stands for the residue class `a + nℤ = {x : ℤ | n ∣ x - a}`.

`S` is an *odd covering system* when
* every modulus is odd,
* every modulus is greater than `1`,
* the moduli are pairwise distinct (two members with the same modulus are the same member),
* every integer lies in at least one of the classes. -/
structure IsOddCovering (S : Finset (ℤ × ℕ)) : Prop where
  odd : ∀ c ∈ S, Odd c.2
  one_lt : ∀ c ∈ S, 1 < c.2
  distinct : ∀ c ∈ S, ∀ c' ∈ S, c.2 = c'.2 → c = c'
  covers : ∀ x : ℤ, ∃ c ∈ S, (c.2 : ℤ) ∣ x - c.1

/-- The least common multiple of the moduli of the system. -/
def lcmModuli (S : Finset (ℤ × ℕ)) : ℕ := S.lcm (fun c => c.2)

/-- **The filed result.** Every covering of `ℤ` by finitely many congruences with pairwise distinct
odd moduli `> 1` has `lcm` of the moduli at least `168,131,152,814,625`. -/
def MainStatement : Prop :=
  ∀ S : Finset (ℤ × ℕ), IsOddCovering S → 168131152814625 ≤ lcmModuli S

end Erdos7
