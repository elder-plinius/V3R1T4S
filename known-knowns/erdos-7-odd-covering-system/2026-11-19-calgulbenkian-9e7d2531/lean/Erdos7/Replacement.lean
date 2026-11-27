/-
Lemma 1 (Berger–Felzenbaum–Fraenkel prime replacement), digit form.

`dig p q e u` rewrites the first `e` base-`p` digits of `u` as base-`q` digits in the same
positions.  For `p ≤ q`, a residue class modulo `q^t` pulls back under `dig p q e` into (at most)
one residue class modulo `p^t`; hence its pull-back to `Fin (p^e)` has at most `p^(e-t)` points.
-/
import Erdos7.Defs

namespace Erdos7

/-- Rewrite the first `e` base-`p` digits of `u` in base `q` (same exponent positions). -/
def dig (p q : ℕ) : ℕ → ℕ → ℕ
  | 0, _ => 0
  | e + 1, u => u % p + q * dig p q e (u / p)

/-- Congruence modulo `q^t` of the replaced numbers forces congruence modulo `p^t`. -/
theorem dig_modEq (p q : ℕ) (hp : 2 ≤ p) (hpq : p ≤ q) :
    ∀ (e t u u' : ℕ), t ≤ e → dig p q e u ≡ dig p q e u' [MOD q ^ t] → u ≡ u' [MOD p ^ t] := by
  intro e
  induction e with
  | zero =>
    intro t u u' ht _
    obtain rfl : t = 0 := by omega
    simp [Nat.modEq_one]
  | succ e ih =>
    intro t u u' ht h
    cases t with
    | zero => simp [Nat.modEq_one]
    | succ t =>
      have hq : 0 < q := by omega
      simp only [dig] at h
      -- reduce modulo q
      have h1 : u % p + q * dig p q e (u / p) ≡ u' % p + q * dig p q e (u' / p) [MOD q] :=
        h.of_dvd (dvd_pow_self q (Nat.succ_ne_zero t))
      have h2 : u % p ≡ u' % p [MOD q] := by
        have ha : u % p + q * dig p q e (u / p) ≡ u % p [MOD q] := by
          simpa using (Nat.ModEq.refl (u % p)).add (Nat.modEq_zero_iff_dvd.2 (dvd_mul_right q _))
        have hb : u' % p + q * dig p q e (u' / p) ≡ u' % p [MOD q] := by
          simpa using (Nat.ModEq.refl (u' % p)).add (Nat.modEq_zero_iff_dvd.2 (dvd_mul_right q _))
        exact ha.symm.trans (h1.trans hb)
      have hup : u % p < q := lt_of_lt_of_le (Nat.mod_lt _ (by omega)) hpq
      have hup' : u' % p < q := lt_of_lt_of_le (Nat.mod_lt _ (by omega)) hpq
      have h3 : u % p = u' % p := by
        have := h2
        unfold Nat.ModEq at this
        rwa [Nat.mod_eq_of_lt hup, Nat.mod_eq_of_lt hup'] at this
      rw [h3] at h
      have h4 : q * dig p q e (u / p) ≡ q * dig p q e (u' / p) [MOD q * q ^ t] := by
        rw [← pow_succ']
        exact Nat.ModEq.add_left_cancel' _ h
      have h5 : dig p q e (u / p) ≡ dig p q e (u' / p) [MOD q ^ t] :=
        Nat.ModEq.mul_left_cancel' (by omega) h4
      have h6 : u / p ≡ u' / p [MOD p ^ t] := ih t _ _ (by omega) h5
      have h7 : p * (u / p) ≡ p * (u' / p) [MOD p * p ^ t] := h6.mul_left' p
      rw [← pow_succ'] at h7
      have h8 := (Nat.ModEq.refl (u' % p) (n := p ^ (t + 1))).add h7
      rw [← h3] at h8
      conv at h8 => lhs; rw [Nat.mod_add_div]
      rw [h3, Nat.mod_add_div] at h8
      exact h8

/-- Counting form of Lemma 1: the pull-back to `Fin (p^e)` of a residue class modulo `q^t`
(`t ≤ e`) under the digit replacement has at most `p^(e-t)` points. -/
theorem dig_class_card (p q : ℕ) (hp : 2 ≤ p) (hpq : p ≤ q) (e t : ℕ) (ht : t ≤ e) (a : ℤ) :
    (Finset.univ.filter (fun u : Fin (p ^ e) => ((q : ℤ) ^ t) ∣ (dig p q e u.val : ℤ) - a)).card
      * p ^ t ≤ p ^ e := by
  classical
  set F := Finset.univ.filter (fun u : Fin (p ^ e) => ((q : ℤ) ^ t) ∣ (dig p q e u.val : ℤ) - a)
    with hF
  have hppos : 0 < p ^ t := pow_pos (by omega) t
  have key : ∀ u ∈ F, ∀ u' ∈ F, u.val % p ^ t = u'.val % p ^ t := by
    intro u hu u' hu'
    rw [hF, Finset.mem_filter] at hu hu'
    have hd : ((q : ℤ) ^ t) ∣ (dig p q e u'.val : ℤ) - (dig p q e u.val : ℤ) := by
      have := dvd_sub hu'.2 hu.2
      simpa using this
    have hm : (dig p q e u.val : ℤ) ≡ (dig p q e u'.val : ℤ) [ZMOD ((q ^ t : ℕ) : ℤ)] := by
      rw [Int.modEq_iff_dvd]; push_cast; exact hd
    exact dig_modEq p q hp hpq e t _ _ ht (Int.natCast_modEq_iff.1 hm)
  have hcard : F.card ≤ (Finset.range (p ^ (e - t))).card := by
    apply Finset.card_le_card_of_injOn (fun u => u.val / p ^ t)
    · intro u _
      simp only [Finset.coe_range, Set.mem_Iio]
      have hu : u.val < p ^ (e - t) * p ^ t := by
        rw [← pow_add, Nat.sub_add_cancel ht]; exact u.isLt
      exact Nat.div_lt_of_lt_mul (by rwa [mul_comm] at hu)
    · intro u hu u' hu' h
      have h1 := key u hu u' hu'
      apply Fin.ext
      have h2 : (u.val / p ^ t) = (u'.val / p ^ t) := h
      rw [← Nat.mod_add_div u.val (p ^ t), ← Nat.mod_add_div u'.val (p ^ t), h1, h2]
  rw [Finset.card_range] at hcard
  calc F.card * p ^ t ≤ p ^ (e - t) * p ^ t := Nat.mul_le_mul_right _ hcard
    _ = p ^ e := by rw [← pow_add, Nat.sub_add_cancel ht]

theorem oddP_eq_zero_of_ge {m : ℕ} (h : 14 ≤ m) : oddP m = 0 := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 14 := ⟨m - 14, by omega⟩
  rfl

theorem three_le_oddP {m : ℕ} (h : m < 14) : 3 ≤ oddP m := by
  interval_cases m <;> simp [oddP]

theorem oddP_gap : ∀ m < 13, ∀ n < 48, oddP m < n → n < oddP (m + 1) →
    (2 ∣ n ∧ n ≠ 2) ∨ (3 ∣ n ∧ n ≠ 3) ∨ (5 ∣ n ∧ n ≠ 5) ∨ (7 ∣ n ∧ n ≠ 7) := by
  have h : ∀ m : Fin 13, ∀ n : Fin 48, oddP m.val < n.val → n.val < oddP (m.val + 1) →
      (2 ∣ n.val ∧ n.val ≠ 2) ∨ (3 ∣ n.val ∧ n.val ≠ 3) ∨ (5 ∣ n.val ∧ n.val ≠ 5) ∨
        (7 ∣ n.val ∧ n.val ≠ 7) := by decide
  intro m hm n hn
  exact h ⟨m, hm⟩ ⟨n, hn⟩

theorem oddP_le_47 (m : ℕ) : oddP m ≤ 47 := by
  by_cases h : m < 14
  · interval_cases m <;> simp [oddP]
  · rw [oddP_eq_zero_of_ge (by omega)]; omega

/-- Strictly increasing odd primes dominate the table of first odd primes, position by position
(same position, no swapping). -/
theorem oddP_le_of_strictMono (q : ℕ → ℕ) (r : ℕ) (hprime : ∀ m, m < r → (q m).Prime)
    (hodd : ∀ m, m < r → Odd (q m)) (hmono : ∀ m, m + 1 < r → q m < q (m + 1)) :
    ∀ m, m < r → oddP m ≤ q m := by
  intro m
  induction m with
  | zero =>
    intro h
    have h2 := (hprime 0 h).two_le
    have h3 : q 0 ≠ 2 := by
      intro h2'; have := hodd 0 h; rw [h2'] at this; exact absurd this (by decide)
    show 3 ≤ q 0
    omega
  | succ m ih =>
    intro h
    by_cases h14 : 14 ≤ m + 1
    · rw [oddP_eq_zero_of_ge h14]; exact Nat.zero_le _
    · have hm := ih (by omega)
      have hlt := hmono m h
      by_contra hcon
      rw [not_le] at hcon
      have hn48 : q (m + 1) < 48 := by
        have := oddP_le_47 (m + 1)
        omega
      have hpr := hprime (m + 1) h
      have hdiv : ∀ d, d ∣ q (m + 1) → d ≠ q (m + 1) → d ≠ 1 → False := by
        intro d hd hne h1
        rcases (Nat.dvd_prime hpr).1 hd with h' | h'
        · exact h1 h'
        · exact hne h'
      rcases oddP_gap m (by omega) (q (m + 1)) hn48 (by omega) hcon with h' | h' | h' | h'
      · exact hdiv 2 h'.1 (Ne.symm h'.2) (by decide)
      · exact hdiv 3 h'.1 (Ne.symm h'.2) (by decide)
      · exact hdiv 5 h'.1 (Ne.symm h'.2) (by decide)
      · exact hdiv 7 h'.1 (Ne.symm h'.2) (by decide)

end Erdos7
