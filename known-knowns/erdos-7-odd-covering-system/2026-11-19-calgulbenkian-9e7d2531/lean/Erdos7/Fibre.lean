/-
Stage 4: one fibre.  For a coordinate that passes `coordOK`, the kernel of Lemma 4 (uniform on
the complement of the pure part if `cap = 0`, capped otherwise) has all the properties needed by
the abstract theorem, with the tail bounds `Qr` and the stage loss `fS` used by the checker.
-/
import Erdos7.Spec
import Erdos7.Kernels

namespace Erdos7
open Finset
open scoped Classical

/-- Stage loss as a function of the weighted number `z` of active mixed classes:
identity (union bound) on a uniform coordinate, the hinge `C (ρ - δ + z)_+` on a capped one. -/
noncomputable def fS (p e cap : ℕ) (z : ℚ) : ℚ :=
  if cap = 0 then z
  else ((cap:ℚ) / 32) * max 0 ((geom p e : ℚ) / (p:ℚ) ^ e - (1 - 1 / ((cap:ℚ) / 32)) + z)

/-- Weight of an active mixed class of level `t`. -/
noncomputable def ωS (p e cap t : ℕ) : ℚ :=
  if cap = 0 then Qr p e cap t else 1 / (p:ℚ) ^ t

lemma geom_mul (p : ℕ) (hp : 1 ≤ p) : ∀ e, geom p e * (p - 1) + 1 = p ^ e
  | 0 => by simp [geom]
  | e + 1 => by
    have ih := geom_mul p hp e
    obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
    simp only [geom, Nat.add_sub_cancel] at ih ⊢
    rw [pow_succ, ← ih]; ring

lemma sum_Icc_pow (p : ℕ) : ∀ e, ∑ t ∈ Icc 1 e, p ^ (e - t) = geom p e
  | 0 => by simp [geom]
  | e + 1 => by
    rw [sum_Icc_succ_top (by omega), geom, ← sum_Icc_pow p e, mul_sum]
    simp only [Nat.sub_self, pow_zero]
    congr 1
    refine sum_congr rfl fun t ht => ?_
    have := (mem_Icc.1 ht).2
    rw [show e + 1 - t = (e - t) + 1 by omega, pow_succ]; ring

lemma Qr_zero {p e cap : ℕ} (h : 0 < den p e cap) : Qr p e cap 0 = 1 := by
  have : (den p e cap : ℚ) ≠ 0 := by exact_mod_cast h.ne'
  simp [Qr, Qn, this]

lemma Qr_succ_top (p e cap : ℕ) : Qr p e cap (e + 1) = 0 := by
  simp [Qr, Qn]

lemma Qr_nonneg (p e cap t : ℕ) : 0 ≤ Qr p e cap t := by
  unfold Qr; positivity

lemma Qr_unif {p e t : ℕ} (ht1 : 1 ≤ t) (hte : t ≤ e) :
    Qr p e 0 t = ((p ^ (e - t) : ℕ) : ℚ) / (den p e 0 : ℚ) := by
  have h1 : t ≠ 0 := by omega
  have h2 : ¬ e < t := by omega
  simp [Qr, Qn, h1, h2]

lemma Qr_cap {p e cap t : ℕ} (hc : cap ≠ 0) (ht1 : 1 ≤ t) (hte : t ≤ e) :
    Qr p e cap t = ((Nat.min (32 * p ^ e) (cap * p ^ (e - t)) : ℕ) : ℚ) / ((32 * p ^ e : ℕ) : ℚ) := by
  have h1 : t ≠ 0 := by omega
  have h2 : ¬ e < t := by omega
  simp [Qr, Qn, den, h1, h2, hc]

lemma ωS_nonneg (p e cap t : ℕ) : 0 ≤ ωS p e cap t := by
  unfold ωS; split_ifs
  · exact Qr_nonneg _ _ _ _
  · positivity

lemma fS_mono (p e cap : ℕ) : MonotoneOn (fS p e cap) (Set.Ici 0) := by
  intro a _ b _ hab
  unfold fS
  split_ifs
  · exact hab
  · exact mul_le_mul_of_nonneg_left (max_le_max le_rfl (by linarith)) (by positivity)

lemma fS_convex (p e cap : ℕ) : ConvexOn ℚ (Set.Ici 0) (fS p e cap) := by
  refine ⟨convex_Ici 0, ?_⟩
  intro x _ y _ a b ha hb hab
  simp only [smul_eq_mul]
  unfold fS
  split_ifs
  · exact le_rfl
  · set c : ℚ := (geom p e : ℚ) / (p:ℚ) ^ e - (1 - 1 / ((cap:ℚ) / 32)) with hc
    have hC : (0:ℚ) ≤ (cap:ℚ) / 32 := by positivity
    have key : max 0 (c + (a * x + b * y)) ≤ a * max 0 (c + x) + b * max 0 (c + y) := by
      refine max_le ?_ ?_
      · have h1 := le_max_left 0 (c + x)
        have h2 := le_max_left 0 (c + y)
        positivity
      · have h1 := le_max_right 0 (c + x)
        have h2 := le_max_right 0 (c + y)
        have e1 : c + (a * x + b * y) = a * (c + x) + b * (c + y) := by
          have : c = (a + b) * c := by rw [hab, one_mul]
          nlinarith
        rw [e1]
        exact add_le_add (mul_le_mul_of_nonneg_left h1 ha) (mul_le_mul_of_nonneg_left h2 hb)
    calc (cap:ℚ) / 32 * max 0 (c + (a * x + b * y))
        ≤ (cap:ℚ) / 32 * (a * max 0 (c + x) + b * max 0 (c + y)) :=
          mul_le_mul_of_nonneg_left key hC
      _ = _ := by ring

/-- Sum over a union is at most the sum of the sums, for a nonnegative weight. -/
lemma sum_biUnion_le' {α ι : Type} (k : α → ℚ) (hk : ∀ x, 0 ≤ k x) (K : Finset ι)
    (A : ι → Finset α) : ∑ x ∈ K.biUnion A, k x ≤ ∑ j ∈ K, ∑ x ∈ A j, k x := by
  induction K using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [biUnion_insert, sum_insert ha]
    have h1 := sum_union_inter (s₁ := A a) (s₂ := s.biUnion A) (f := k)
    have h2 : 0 ≤ ∑ x ∈ A a ∩ s.biUnion A, k x := sum_nonneg fun x _ => hk x
    linarith

/-- The stage loss evaluated at the worst case `Ω (M - 1)` is the checker's `gnum M / gden`. -/
lemma stage_eq {p e cap : ℕ} (hok : coordOK p e cap = true) {M : ℕ} (hM : 1 ≤ M) :
    fS p e cap ((∑ t ∈ Icc 1 e, ωS p e cap t) * ((M:ℚ) - 1))
      = (gnum p e cap M : ℚ) / (gden p e cap : ℚ) := by
  obtain ⟨h3, he1, hden, hanti, hcap⟩ := coordOK_spec hok
  have hp1 : 1 ≤ p := by omega
  have hgm := geom_mul p hp1 e
  have hpe : 0 < p ^ e := Nat.pow_pos (by omega)
  have hsum := sum_Icc_pow p e
  by_cases hc : cap = 0
  · subst hc
    have hdq : (den p e 0 : ℚ) ≠ 0 := by exact_mod_cast hden.ne'
    have hΩ : ∑ t ∈ Icc 1 e, ωS p e 0 t = (geom p e : ℚ) / (den p e 0 : ℚ) := by
      have : ∀ t ∈ Icc 1 e, ωS p e 0 t = ((p ^ (e - t) : ℕ) : ℚ) / (den p e 0 : ℚ) := by
        intro t ht
        simp only [ωS, ite_true]
        exact Qr_unif (mem_Icc.1 ht).1 (mem_Icc.1 ht).2
      rw [sum_congr rfl this, ← sum_div, ← Nat.cast_sum, hsum]
    have hg : gden p e 0 = den p e 0 := by simp [gden, den]
    have hn : gnum p e 0 M = geom p e * (M - 1) := by simp [gnum]
    rw [hΩ, hg, hn]
    simp only [fS, ite_true]
    push_cast [Nat.cast_sub hM]
    ring
  · rcases hcap with h0 | ⟨hc32, hcδ⟩
    · exact absurd h0 hc
    have hpq : (0:ℚ) < (p:ℚ) ^ e := by positivity
    have hp1q : (0:ℚ) < (p:ℚ) - 1 := by
      have : (3:ℚ) ≤ p := by exact_mod_cast h3
      linarith
    have hcq : (0:ℚ) < (cap:ℚ) := by exact_mod_cast (by omega : 0 < cap)
    have hgmq : (geom p e : ℚ) * ((p:ℚ) - 1) + 1 = (p:ℚ) ^ e := by
      have := congrArg (Nat.cast : ℕ → ℚ) hgm
      push_cast [Nat.cast_sub hp1] at this
      exact this
    have hΩ : ∑ t ∈ Icc 1 e, ωS p e cap t = (geom p e : ℚ) / (p:ℚ) ^ e := by
      have : ∀ t ∈ Icc 1 e, ωS p e cap t = ((p ^ (e - t) : ℕ) : ℚ) / (p:ℚ) ^ e := by
        intro t ht
        have hte := (mem_Icc.1 ht).2
        simp only [ωS, hc, ite_false]
        rw [eq_div_iff hpq.ne']
        push_cast
        have hsplit : (p:ℚ) ^ e = (p:ℚ) ^ (e - t) * (p:ℚ) ^ t := by
          rw [← pow_add]; congr 1; omega
        rw [hsplit]; field_simp
      rw [sum_congr rfl this, ← sum_div, ← Nat.cast_sum, hsum]
    have hg : (gden p e cap : ℚ) = 32 * ((p:ℚ) - 1) * (p:ℚ) ^ e := by
      simp only [gden, hc, ite_false]
      push_cast [Nat.cast_sub hp1]; ring
    have hgpos : (0:ℚ) < 32 * ((p:ℚ) - 1) * (p:ℚ) ^ e := by positivity
    -- the argument of the hinge, in closed form
    have harg : (geom p e : ℚ) / (p:ℚ) ^ e - (1 - 1 / ((cap:ℚ) / 32))
          + (geom p e : ℚ) / (p:ℚ) ^ e * ((M:ℚ) - 1)
        = ((cap:ℚ) * ((p:ℚ) ^ e - 1) * M - ((cap:ℚ) - 32) * ((p:ℚ) - 1) * (p:ℚ) ^ e)
          / ((cap:ℚ) * ((p:ℚ) - 1) * (p:ℚ) ^ e) := by
      rw [← hgmq]; field_simp; ring
    have hn : gnum p e cap M = cap * (p ^ e - 1) * M - (cap - 32) * (p - 1) * p ^ e := by
      simp [gnum, hc]
    rw [hΩ, hg, hn]
    simp only [fS, hc, ite_false]
    rw [harg]
    have hcast1 : ((cap * (p ^ e - 1) * M : ℕ) : ℚ) = (cap:ℚ) * ((p:ℚ) ^ e - 1) * M := by
      push_cast [Nat.cast_sub hpe]; ring
    have hcast2 : (((cap - 32) * (p - 1) * p ^ e : ℕ) : ℚ)
        = ((cap:ℚ) - 32) * ((p:ℚ) - 1) * (p:ℚ) ^ e := by
      push_cast [Nat.cast_sub hp1, Nat.cast_sub hc32.le]; ring
    have hdpos : (0:ℚ) < (cap:ℚ) * ((p:ℚ) - 1) * (p:ℚ) ^ e := by positivity
    by_cases hle : (cap - 32) * (p - 1) * p ^ e ≤ cap * (p ^ e - 1) * M
    · rw [Nat.cast_sub hle, hcast1, hcast2]
      have hnn : (0:ℚ) ≤ (cap:ℚ) * ((p:ℚ) ^ e - 1) * M - ((cap:ℚ) - 32) * ((p:ℚ) - 1) * (p:ℚ) ^ e := by
        rw [← hcast1, ← hcast2, sub_nonneg]; exact_mod_cast hle
      rw [max_eq_right (div_nonneg hnn hdpos.le)]
      field_simp
    · have hlt : cap * (p ^ e - 1) * M < (cap - 32) * (p - 1) * p ^ e := not_le.1 hle
      rw [Nat.sub_eq_zero_of_le hlt.le]
      have hneg : (cap:ℚ) * ((p:ℚ) ^ e - 1) * M - ((cap:ℚ) - 32) * ((p:ℚ) - 1) * (p:ℚ) ^ e ≤ 0 := by
        rw [← hcast1, ← hcast2, sub_nonpos]; exact_mod_cast hlt.le
      rw [max_eq_left (div_nonpos_of_nonpos_of_nonneg hneg hdpos.le)]
      simp

/-- **Lemma 4, one fibre.** `α` is the fibre (`|α| = p^e`), `P` the pure part (`|P| ≤ geom p e`),
`A j` (`j ∈ K`) the sides of the active mixed classes, of levels `1 ≤ l j ≤ e` and sizes
`≤ p^(e - l j)`.  There is a probability weight `k` on `α`, zero on `P`, giving every set `S`
with `|S| p^t ≤ p^e` weight at most `Qr t`, and with loss `k(⋃ A j) ≤ fS (Σ ωS (l j))`. -/
theorem fibre_kernel {α : Type} [Fintype α] (p e cap : ℕ) (hok : coordOK p e cap = true)
    (hcard : Fintype.card α = p ^ e) {ι : Type} (P : Finset α) (hP : P.card ≤ geom p e)
    (K : Finset ι) (l : ι → ℕ) (A : ι → Finset α)
    (hl : ∀ j ∈ K, 1 ≤ l j ∧ l j ≤ e) (hA : ∀ j ∈ K, (A j).card ≤ p ^ (e - l j)) :
    ∃ k : α → ℚ, (∀ x, 0 ≤ k x) ∧ ∑ x, k x = 1 ∧ (∀ x ∈ P, k x = 0) ∧
      (∀ (S : Finset α) (t : ℕ), t ≤ e → S.card * p ^ t ≤ p ^ e → ∑ x ∈ S, k x ≤ Qr p e cap t) ∧
      ∑ x ∈ K.biUnion A, k x ≤ fS p e cap (∑ j ∈ K, ωS p e cap (l j)) := by
  obtain ⟨h3, he1, hden, hanti, hcap⟩ := coordOK_spec hok
  have hp1 : 1 ≤ p := by omega
  have hp0 : 0 < p := by omega
  have hgm := geom_mul p hp1 e
  have hpe : 0 < p ^ e := Nat.pow_pos hp0
  have hpq : (0:ℚ) < (p:ℚ) ^ e := by positivity
  have hScard : ∀ (S : Finset α) (t : ℕ), t ≤ e → S.card * p ^ t ≤ p ^ e →
      S.card ≤ p ^ (e - t) := by
    intro S t hte h
    have : p ^ e = p ^ (e - t) * p ^ t := by rw [← pow_add]; congr 1; omega
    rw [this] at h
    exact Nat.le_of_mul_le_mul_right h (Nat.pow_pos hp0)
  by_cases hc : cap = 0
  · subst hc
    have hs : den p e 0 = p ^ e - geom p e := by simp [den]
    have hsq : (0:ℚ) < (den p e 0 : ℚ) := by exact_mod_cast hden
    obtain ⟨k, hk0, hk1, hkP, hkA⟩ := unif_kernel P (den p e 0) hden (by rw [hcard]; omega)
    refine ⟨k, hk0, hk1, hkP, ?_, ?_⟩
    · intro S t hte hS
      rcases Nat.eq_zero_or_pos t with rfl | ht
      · rw [Qr_zero hden, ← hk1]
        exact sum_le_univ_sum_of_nonneg hk0
      · rw [Qr_unif ht hte]
        refine (hkA S).trans ?_
        apply div_le_div_of_nonneg_right _ hsq.le
        exact_mod_cast hScard S t hte hS
    · simp only [fS, ite_true]
      refine (sum_biUnion_le' k hk0 K A).trans (sum_le_sum fun j hj => ?_)
      simp only [ωS, ite_true]
      rw [Qr_unif (hl j hj).1 (hl j hj).2]
      refine (hkA (A j)).trans ?_
      apply div_le_div_of_nonneg_right _ hsq.le
      exact_mod_cast hA j hj
  · rcases hcap with h0 | ⟨hc32, hcδ⟩
    · exact absurd h0 hc
    have hcq : (0:ℚ) < (cap:ℚ) := by exact_mod_cast (by omega : 0 < cap)
    have hCq : (0:ℚ) < (cap:ℚ) / 32 := by positivity
    have hp1q : (0:ℚ) < (p:ℚ) - 1 := by
      have : (3:ℚ) ≤ p := by exact_mod_cast h3
      linarith
    have hgmq : (geom p e : ℚ) * ((p:ℚ) - 1) + 1 = (p:ℚ) ^ e := by
      have := congrArg (Nat.cast : ℕ → ℚ) hgm
      push_cast [Nat.cast_sub hp1] at this
      exact this
    have hδq : (cap:ℚ) * ((p:ℚ) ^ e - 1) ≤ ((cap:ℚ) - 32) * ((p:ℚ) - 1) * (p:ℚ) ^ e := by
      have := (Nat.cast_le (α := ℚ)).2 hcδ
      push_cast [Nat.cast_sub hp1, Nat.cast_sub hc32.le, Nat.cast_sub hpe] at this
      exact this
    have hCg : (((p ^ e : ℕ) : ℚ)) ≤ (cap:ℚ) / 32 * (((p ^ e : ℕ) : ℚ) - (geom p e : ℚ)) := by
      push_cast
      have h1 : (cap:ℚ) * (geom p e : ℚ) * ((p:ℚ) - 1)
          ≤ ((cap:ℚ) - 32) * (p:ℚ) ^ e * ((p:ℚ) - 1) := by
        have : (p:ℚ) ^ e - 1 = (geom p e : ℚ) * ((p:ℚ) - 1) := by linarith
        rw [this] at hδq; linarith
      have h2 := le_of_mul_le_mul_right h1 hp1q
      linarith
    obtain ⟨k, hk0, hk1, hkP, hkC, hkB⟩ :=
      capped_kernel P (K.biUnion A) (p ^ e) (geom p e) hcard hpe ((cap:ℚ) / 32) hCq hP hCg
    refine ⟨k, hk0, hk1, hkP, ?_, ?_⟩
    · intro S t hte hS
      have hle1 : ∑ x ∈ S, k x ≤ 1 := by
        rw [← hk1]; exact sum_le_univ_sum_of_nonneg hk0
      rcases Nat.eq_zero_or_pos t with rfl | ht
      · rw [Qr_zero hden]; exact hle1
      · rw [Qr_cap hc ht hte]
        have hd : (0:ℚ) < ((32 * p ^ e : ℕ) : ℚ) := by positivity
        rw [le_div_iff₀ hd]
        have hSc : (S.card : ℚ) ≤ ((p ^ (e - t) : ℕ) : ℚ) := by exact_mod_cast hScard S t hte hS
        have h2 : ∑ x ∈ S, k x ≤ S.card * ((cap:ℚ) / 32 / ((p ^ e : ℕ) : ℚ)) := by
          calc ∑ x ∈ S, k x ≤ ∑ _x ∈ S, ((cap:ℚ) / 32 / ((p ^ e : ℕ) : ℚ)) :=
                sum_le_sum fun x _ => hkC x
            _ = _ := by rw [sum_const, nsmul_eq_mul]
        have hmin : ((Nat.min (32 * p ^ e) (cap * p ^ (e - t)) : ℕ) : ℚ)
            = min (((32 * p ^ e : ℕ) : ℚ)) (((cap * p ^ (e - t) : ℕ)) : ℚ) := Nat.cast_min _ _
        rw [hmin]
        refine le_min ?_ ?_
        · have := mul_le_mul_of_nonneg_right hle1 hd.le
          linarith
        · have h3' : S.card * ((cap:ℚ) / 32 / ((p ^ e : ℕ) : ℚ)) * ((32 * p ^ e : ℕ) : ℚ)
              = S.card * (cap:ℚ) := by
            push_cast; field_simp
          have := mul_le_mul_of_nonneg_right h2 hd.le
          rw [h3'] at this
          refine this.trans ?_
          push_cast
          push_cast at hSc
          nlinarith
    · simp only [fS, hc, ite_false]
      refine hkB.trans (mul_le_mul_of_nonneg_left (max_le_max le_rfl ?_) hCq.le)
      have hB : ((K.biUnion A).card : ℚ) / (p:ℚ) ^ e ≤ ∑ j ∈ K, ωS p e cap (l j) := by
        have h1 : ((K.biUnion A).card : ℚ) ≤ ∑ j ∈ K, ((p ^ (e - l j) : ℕ) : ℚ) := by
          have : (K.biUnion A).card ≤ ∑ j ∈ K, p ^ (e - l j) :=
            card_biUnion_le.trans (sum_le_sum hA)
          exact_mod_cast this
        rw [div_le_iff₀ hpq]
        refine h1.trans ?_
        rw [sum_mul]
        refine le_of_eq (sum_congr rfl fun j hj => ?_)
        have hle := (hl j hj).2
        simp only [ωS, hc, ite_false]
        push_cast
        have : (p:ℚ) ^ e = (p:ℚ) ^ (e - l j) * (p:ℚ) ^ (l j) := by
          rw [← pow_add]; congr 1; omega
        rw [this]; field_simp
      push_cast
      have : ((geom p e : ℚ) + (K.biUnion A).card) / (p:ℚ) ^ e
          = (geom p e : ℚ) / (p:ℚ) ^ e + ((K.biUnion A).card : ℚ) / (p:ℚ) ^ e := by ring
      rw [this]; linarith

end Erdos7
