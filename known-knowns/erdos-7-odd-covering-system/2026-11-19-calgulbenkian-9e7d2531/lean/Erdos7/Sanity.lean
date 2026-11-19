/-
Audit aids (not used by the main theorem).

1. The covering predicate is satisfiable once oddness is dropped: Erdős's 1950 covering
   `{0 mod 2, 0 mod 3, 1 mod 4, 5 mod 6, 7 mod 12}` covers `ℤ`, has distinct moduli `> 1`, and
   lcm `12`.  So the definition in `Statement.lean` is not vacuous by accident.
2. The checker can fail: a few negative tests.
3. `#print axioms` for the main theorem of every stage.
-/
import Erdos7.Main
import Erdos7.EnumSigma

namespace Erdos7

def erdos1950 : Finset (ℤ × ℕ) := {(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)}

theorem erdos1950_covers : ∀ x : ℤ, ∃ c ∈ erdos1950, (c.2 : ℤ) ∣ x - c.1 := by
  intro x
  have h : x % 12 = 0 ∨ x % 12 = 1 ∨ x % 12 = 2 ∨ x % 12 = 3 ∨ x % 12 = 4 ∨ x % 12 = 5 ∨
      x % 12 = 6 ∨ x % 12 = 7 ∨ x % 12 = 8 ∨ x % 12 = 9 ∨ x % 12 = 10 ∨ x % 12 = 11 := by omega
  simp only [erdos1950, Finset.mem_insert, Finset.mem_singleton, exists_eq_or_imp, exists_eq_left]
  omega

theorem erdos1950_distinct : ∀ c ∈ erdos1950, ∀ c' ∈ erdos1950, c.2 = c'.2 → c = c' := by decide

theorem erdos1950_one_lt : ∀ c ∈ erdos1950, 1 < c.2 := by decide

theorem erdos1950_lcm : lcmModuli erdos1950 = 12 := by decide +kernel

/-- It is not an odd covering (it has even moduli), as it must not be. -/
theorem erdos1950_not_odd : ¬ IsOddCovering erdos1950 := fun h => by
  have := h.odd (0, 2) (by decide)
  exact absurd this (by decide)

/-- Negative tests: the kernel-evaluated checker rejects wrong certificates. -/
example : checkEntry ([1,1,1,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0,0,0,0,0]) = false := by
  decide +kernel
example : checkEntry ([4,3,2,2,1,1,1,1,1], [0,0,0,0,0,0,0,0,0]) = false := by decide +kernel
/-- cap below 1 (`C = 31/32`) is rejected. -/
example : checkEntry ([1,1,1,1,1], [0,0,31,64,64]) = false := by decide +kernel
/-- mismatched lengths are rejected. -/
example : checkEntry ([1,1,1], [0,0]) = false := by decide +kernel

/-- The split of the table: 2,519 profiles use pure deletion on every coordinate (all caps `0`),
4,517 use capped coordinates. -/
theorem table_split :
    (Cert.table.filter (fun x => x.2.all (fun c => Nat.beq c 0))).length = 2519 ∧
    (Cert.table.filter (fun x => !(x.2.all (fun c => Nat.beq c 0)))).length = 4517 := by
  decide +kernel

-- Stage 1 + final theorem
#print axioms odd_covering_lcm_lower_bound
-- Stage 2
#print axioms Cert.table_checkAll
#print axioms Cert.table_length
#print axioms check_sound
-- Stage 3
#print axioms band_complete
#print axioms sigFrom_zero_eq_sigma
-- Stage 4
#print axioms nested_convex_comparison
#print axioms comparison
#print axioms unif_kernel
#print axioms capped_kernel
#print axioms fibre_kernel
#print axioms abstract_no_cover
#print axioms box_no_cover
#print axioms dig_modEq
#print axioms dig_class_card
#print axioms box_cover_abundant

end Erdos7
