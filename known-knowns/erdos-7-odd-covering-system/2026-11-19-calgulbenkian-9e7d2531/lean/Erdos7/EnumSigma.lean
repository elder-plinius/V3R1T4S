/-
Optional reading aid for Stage 3: `sigFrom 0 es` is the true sum of divisors of `valFrom 0 es`
(for profiles of length at most 14, the range where `oddP` is a prime).
-/
import Erdos7.Defs

namespace Erdos7

theorem geom_eq_sum_range (p : ℕ) : ∀ e, geom p e = ∑ x ∈ Finset.range e, p ^ x
  | 0 => by simp [geom]
  | e + 1 => by
    rw [geom, geom_eq_sum_range p e, Finset.sum_range_succ', Finset.mul_sum]
    simp [pow_succ']

theorem oddP_prime {i : ℕ} (hi : i < 14) : (oddP i).Prime := by
  interval_cases i <;> simp only [oddP] <;> norm_num

theorem oddP_coprime {i j : ℕ} (hj : j < i) (hi : i < 14) : Nat.Coprime (oddP j) (oddP i) := by
  interval_cases i <;> interval_cases j <;> simp only [oddP] <;> norm_num

theorem coprime_valFrom (j : ℕ) : ∀ (es : List ℕ) (i : ℕ), j < i → i + es.length ≤ 14 →
    Nat.Coprime (oddP j) (valFrom i es)
  | [], _, _, _ => by simp [valFrom]
  | e :: es, i, hj, hl => by
    simp only [List.length_cons] at hl
    rw [valFrom]
    exact Nat.Coprime.mul_right (Nat.Coprime.pow_right _ (oddP_coprime hj (by omega)))
      (coprime_valFrom j es (i + 1) (by omega) (by omega))

theorem sigFrom_eq_sum_divisors : ∀ (es : List ℕ) (i : ℕ), i + es.length ≤ 14 →
    sigFrom i es = ∑ d ∈ (valFrom i es).divisors, d
  | [], _, _ => by simp [sigFrom, valFrom]
  | e :: es, i, hl => by
    simp only [List.length_cons] at hl
    rw [sigFrom, valFrom,
      Nat.Coprime.sum_divisors_mul
        (Nat.Coprime.pow_left _ (coprime_valFrom i es (i + 1) (by omega) (by omega))),
      ← sigFrom_eq_sum_divisors es (i + 1) (by omega),
      Nat.sum_divisors_prime_pow (oddP_prime (by omega)), geom_eq_sum_range]

/-- `sigFrom 0 es` is `σ(valFrom 0 es)`, the sum of the divisors. -/
theorem sigFrom_zero_eq_sigma (es : List ℕ) (hl : es.length ≤ 14) :
    sigFrom 0 es = ∑ d ∈ (valFrom 0 es).divisors, d :=
  sigFrom_eq_sum_divisors es 0 (by omega)

#print axioms sigFrom_zero_eq_sigma

end Erdos7
