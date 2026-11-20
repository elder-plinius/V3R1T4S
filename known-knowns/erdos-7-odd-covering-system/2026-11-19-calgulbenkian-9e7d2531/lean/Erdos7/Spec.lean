/-
Stage 2 soundness: what a successful run of the natural-number checker `checkEntry` means in
exact rational terms (`check_sound`): all coordinate side conditions hold and the rational bound
`specBound` (the right-hand side of the Lemma 4 / Lemma 5 inequality) is `< 1`.
-/
import Erdos7.Sequential
import Erdos7.Checker

namespace Erdos7
open Finset

/-- Rational tail bound `Q(t)` of a coordinate. -/
def Qr (p e cap t : ℕ) : ℚ := (Qn p e cap t : ℚ) / (den p e cap : ℚ)

section spec
variable (E C : ℕ → ℕ)

/-- Point weights `q m t = Q m t - Q m (t+1)`. -/
def qS (m t : ℕ) : ℚ := Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)

/-- The stage-`i` term of the bound: expectation over independent levels of the stage loss. -/
def stageQ (i : ℕ) : ℚ :=
  ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) i
    (fun T => (gnum (oddP i) (E i) (C i) (mult i T) : ℚ) / (gden (oddP i) (E i) (C i) : ℚ))

def revL : ℕ → List (List ℕ)
  | 0 => []
  | i + 1 => qlist (oddP i) (E i) (C i) :: revL i

def Dn : ℕ → ℕ
  | 0 => 1
  | i + 1 => Dn i * den (oddP i) (E i) (C i)

end spec

/-- The exact rational bound certified for the profile `es` with caps `caps`. -/
def specBound (es caps : List ℕ) : ℚ :=
  ∑ i ∈ range es.length, stageQ (fun m => es.getD m 0) (fun m => caps.getD m 0) i

lemma coordOK_spec {p e cap : ℕ} (h : coordOK p e cap = true) :
    3 ≤ p ∧ 1 ≤ e ∧ 0 < den p e cap ∧ (∀ t, t ≤ e → Qn p e cap (t + 1) ≤ Qn p e cap t) ∧
      (cap = 0 ∨ (32 < cap ∧ cap * (p ^ e - 1) ≤ (cap - 32) * (p - 1) * p ^ e)) := by
  simp only [coordOK, Bool.and_eq_true, Bool.or_eq_true, Nat.ble_eq, Nat.blt_eq,
    List.all_eq_true, List.mem_range] at h
  obtain ⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩ := h
  exact ⟨h1, h2, h3, fun t ht => h4 t (Nat.lt_succ_of_le ht),
    h5.imp (fun h => Nat.eq_of_beq_eq_true h) id⟩

lemma wsum_eq : ∀ (ws : List ℕ) (k : ℕ) (F : ℕ → ℕ),
    wsum ws k F = ∑ j ∈ range ws.length, ws.getD j 0 * F (k + j)
  | [], k, F => by simp [wsum]
  | w :: ws, k, F => by
    rw [wsum, wsum_eq ws (k + 1) F, List.length_cons, sum_range_succ']
    simp only [List.getD_cons_succ, List.getD_cons_zero, add_zero]
    rw [add_comm]
    congr 1
    refine sum_congr rfl fun j _ => ?_
    rw [add_assoc, add_comm 1 j]

lemma wsum_qlist (p e cap : ℕ) (F : ℕ → ℕ) :
    wsum (qlist p e cap) 1 F
      = ∑ t ∈ range (e + 1), (Qn p e cap t - Qn p e cap (t + 1)) * F (1 + t) := by
  rw [wsum_eq]
  have hlen : (qlist p e cap).length = e + 1 := by simp [qlist]
  rw [hlen]
  refine sum_congr rfl fun t ht => ?_
  have ht' : t < e + 1 := mem_range.1 ht
  have : (qlist p e cap).getD t 0 = Qn p e cap t - Qn p e cap (t + 1) := by
    simp [qlist, List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range ht']
  rw [this]

section sound
variable (E C : ℕ → ℕ)

lemma etL_spec (g : ℕ → ℕ) : ∀ (i : ℕ),
    (∀ m, m < i → coordOK (oddP m) (E m) (C m) = true) → ∀ M0 : ℕ,
    (etL g (revL E C i) M0 : ℚ) = (Dn E C i : ℚ) *
      ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) i
        (fun T => (g (M0 * mult i T) : ℚ)) := by
  intro i
  induction i with
  | zero => intro _ M0; simp [etL, revL, Dn, ET, Ex, mult]
  | succ i ih =>
    intro hOK M0
    have hOKi := coordOK_spec (hOK i (Nat.lt_succ_self i))
    obtain ⟨_, _, hden, hanti, _⟩ := hOKi
    have hdenQ : (0:ℚ) < (den (oddP i) (E i) (C i) : ℚ) := by exact_mod_cast hden
    have ih' := ih (fun m hm => hOK m (Nat.lt_succ_of_lt hm))
    have hL : etL g (revL E C (i + 1)) M0
        = ∑ t ∈ range (E i + 1), (Qn (oddP i) (E i) (C i) t - Qn (oddP i) (E i) (C i) (t + 1))
            * etL g (revL E C i) (M0 * (1 + t)) := by
      show wsum (qlist (oddP i) (E i) (C i)) 1 (fun k => etL g (revL E C i) (M0 * k)) = _
      rw [wsum_qlist]
    rw [hL]
    push_cast
    have hR : ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) (i + 1)
          (fun T => (g (M0 * mult (i + 1) T) : ℚ))
        = ∑ t ∈ range (E i + 1),
            (Qr (oddP i) (E i) (C i) t - Qr (oddP i) (E i) (C i) (t + 1)) *
            ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) i
              (fun T => (g (M0 * (1 + t) * mult i T) : ℚ)) := by
      have hfin := Fin.sum_univ_eq_sum_range (fun t : ℕ =>
        (Qr (oddP i) (E i) (C i) t - Qr (oddP i) (E i) (C i) (t + 1)) *
          ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) i
            (fun T => (g (M0 * (1 + t) * mult i T) : ℚ))) (E i + 1)
      rw [← hfin]
      simp only [ET, Ex]
      rw [Ex_sum]
      refine sum_congr rfl fun t _ => ?_
      rw [← Ex_mul_left]
      congr 1
      funext T
      have : M0 * mult (e := E) (i + 1) (T, t) = M0 * (1 + t.val) * mult i T := by
        simp only [mult]; ring
      rw [this]
    rw [hR, mul_sum]
    refine sum_congr rfl fun t ht => ?_
    have ht' : t ≤ E i := Nat.lt_succ_iff.1 (mem_range.1 ht)
    rw [Nat.cast_sub (hanti t ht'), ih' (M0 * (1 + t))]
    simp only [Dn, Qr]
    push_cast
    field_simp

lemma gden_pos {p e cap : ℕ} (h : coordOK p e cap = true) : 0 < gden p e cap := by
  obtain ⟨h3, _, hden, _, hcap⟩ := coordOK_spec h
  unfold gden
  split_ifs with hc
  · simpa [den, hc] using hden
  · have : 0 < p ^ e := Nat.pow_pos (by omega)
    have : 0 < p - 1 := by omega
    positivity

lemma Dn_pos : ∀ (i : ℕ), (∀ m, m < i → coordOK (oddP m) (E m) (C m) = true) → 0 < Dn E C i
  | 0, _ => Nat.one_pos
  | i + 1, h => Nat.mul_pos (Dn_pos i fun m hm => h m (Nat.lt_succ_of_lt hm))
      (coordOK_spec (h i (Nat.lt_succ_self i))).2.2.1

theorem stages_sound : ∀ (es caps : List ℕ) (i A B : ℕ),
    (∀ k, es.getD k 0 = E (i + k)) → (∀ k, caps.getD k 0 = C (i + k)) →
    (∀ m, m < i → coordOK (oddP m) (E m) (C m) = true) → 0 < B →
    stages es caps i (revL E C i) (Dn E C i) A B = true →
    (∀ k, k < es.length → coordOK (oddP (i + k)) (E (i + k)) (C (i + k)) = true) ∧
      (A:ℚ) / B + ∑ k ∈ range es.length, stageQ E C (i + k) < 1 := by
  intro es
  induction es with
  | nil =>
    intro caps i A B _ _ _ hB h
    cases caps with
    | nil =>
      simp only [stages, Nat.blt_eq] at h
      refine ⟨fun k hk => absurd hk (Nat.not_lt_zero k), ?_⟩
      have hB' : (0:ℚ) < B := by exact_mod_cast hB
      simp only [List.length_nil, range_zero, sum_empty, add_zero]
      rw [div_lt_one hB']; exact_mod_cast h
    | cons c cs => simp [stages] at h
  | cons e es ih =>
    intro caps i A B hE hC hOK hB h
    cases caps with
    | nil => simp [stages] at h
    | cons cap caps =>
      have he : e = E i := by simpa using hE 0
      have hc : cap = C i := by simpa using hC 0
      subst he hc
      simp only [stages, Bool.and_eq_true] at h
      obtain ⟨hok, hst⟩ := h
      have hOK' : ∀ m, m < i + 1 → coordOK (oddP m) (E m) (C m) = true := by
        intro m hm
        rcases Nat.lt_succ_iff_lt_or_eq.1 hm with h' | h'
        · exact hOK m h'
        · rw [h']; exact hok
      have hgd := gden_pos hok
      have hD := Dn_pos E C i hOK
      have hB2 : 0 < B * (Dn E C i * gden (oddP i) (E i) (C i)) :=
        Nat.mul_pos hB (Nat.mul_pos hD hgd)
      have hE' : ∀ k, es.getD k 0 = E (i + 1 + k) := by
        intro k; have := hE (k + 1)
        rw [List.getD_cons_succ] at this
        rw [this]; congr 1; omega
      have hC' : ∀ k, caps.getD k 0 = C (i + 1 + k) := by
        intro k; have := hC (k + 1)
        rw [List.getD_cons_succ] at this
        rw [this]; congr 1; omega
      obtain ⟨h1, h2⟩ := ih caps (i + 1) _ _ hE' hC' hOK' hB2 hst
      refine ⟨?_, ?_⟩
      · intro k hk
        cases k with
        | zero => exact hok
        | succ k =>
          have := h1 k (Nat.lt_of_succ_lt_succ hk)
          have e1 : i + (k + 1) = i + 1 + k := by omega
          rw [e1]; exact this
      · have hstage : ((A * (Dn E C i * gden (oddP i) (E i) (C i))
              + etL (gnum (oddP i) (E i) (C i)) (revL E C i) 1 * B : ℕ) : ℚ)
            / ((B * (Dn E C i * gden (oddP i) (E i) (C i)) : ℕ) : ℚ)
            = (A:ℚ) / B + stageQ E C i := by
          have hBq : (B:ℚ) ≠ 0 := by exact_mod_cast hB.ne'
          have hDq : (Dn E C i : ℚ) ≠ 0 := by exact_mod_cast hD.ne'
          have hgq : (gden (oddP i) (E i) (C i) : ℚ) ≠ 0 := by exact_mod_cast hgd.ne'
          have hst' : stageQ E C i = (1 / (gden (oddP i) (E i) (C i) : ℚ)) *
              ET E (fun m t => Qr (oddP m) (E m) (C m) t - Qr (oddP m) (E m) (C m) (t + 1)) i
                (fun T => (gnum (oddP i) (E i) (C i) (1 * mult i T) : ℚ)) := by
            unfold stageQ ET
            rw [← Ex_mul_left]
            congr 1; funext T; rw [one_mul]; ring
          push_cast
          rw [etL_spec E C _ i hOK 1, hst']
          field_simp
        rw [hstage] at h2
        rw [List.length_cons, sum_range_succ']
        have e2 : ∀ k, stageQ E C (i + (k + 1)) = stageQ E C (i + 1 + k) := by
          intro k; congr 1; omega
        simp only [e2, add_zero]
        linarith

end sound

/-- **Soundness of the checker.** If the kernel-evaluated check succeeds then all coordinate side
conditions hold and the exact rational bound is `< 1`. -/
theorem check_sound (es caps : List ℕ) (h : checkEntry (es, caps) = true) :
    (∀ i, i < es.length →
      coordOK (oddP i) (es.getD i 0) (caps.getD i 0) = true) ∧ specBound es caps < 1 := by
  have := stages_sound (fun m => es.getD m 0) (fun m => caps.getD m 0) es caps 0 0 1
    (fun k => by simp) (fun k => by simp) (fun m hm => absurd hm (Nat.not_lt_zero m))
    Nat.one_pos (by simpa [checkEntry, revL, Dn] using h)
  refine ⟨fun i hi => by simpa using this.1 i hi, ?_⟩
  simpa [specBound] using this.2

end Erdos7
